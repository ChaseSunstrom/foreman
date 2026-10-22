"""fm audit run (T-1186): the audit lenses as headless claude -p reviewers over fm audit prep's brief."""
import json
import os
import time

from test_hooks import HookCase

import fmbudget as bud
import fmcore as c

STUB = r'''#!/usr/bin/env python3
import json, os, sys
args, stdin = sys.argv[1:], sys.stdin.read()
lens = next(l for l in stdin.splitlines() if l.startswith("Review only the lens: "))[22:].strip()
with open(os.environ["STUB_LOG"], "a") as f:
    f.write(json.dumps({"args": args, "stdin": stdin, "cwd": os.getcwd(), "lens": lens}) + "\n")
if lens == os.environ.get("STUB_FAIL_LENS"):
    sys.exit(3)
if lens == os.environ.get("STUB_BAD_LENS"):
    print(f"## {lens}: changes needed\n- HIGH a.py:3 the thing breaks on empty input\n- MEDIUM b.py:9 it is slow")
else:
    print(f"## {lens}: ok")
'''


class AuditRun(HookCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.tid = self.task(tier="M")
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        self.log = os.path.join(self.tmp, "stub.log")
        self.env = {"PATH": bindir + os.pathsep + os.environ["PATH"], "STUB_LOG": self.log}
        with open(os.path.join(self.repo, "a.py"), "w") as f:
            f.write("x = 1\n")

    def run_audit(self, *a, env=None, check=True):
        return self.fm("audit", "run", self.tid, *a, env=dict(self.env, **(env or {})), check=check)

    def calls(self):
        return [json.loads(x) for x in open(self.log)] if os.path.exists(self.log) else []

    def audits(self):
        return sorted({x[0] for x in next(b for b in c.load_briefs(self.project()) if b.id == self.tid).audits()})

    def test_one_verdict_per_lens_and_the_findings(self):
        self.run_audit(env={"STUB_BAD_LENS": "edge"})
        want = [x for x in c.AUDIT_LENSES if x != "self"]
        self.assertEqual(sorted(x["lens"] for x in self.calls()), sorted(want))
        self.assertEqual(self.audits(), sorted(want))
        for call in self.calls():
            a = call["args"]
            self.assertEqual(a[a.index("--tools") + 1], "Read,Grep,Glob", "read-only reviewers")
            self.assertIn("--strict-mcp-config", a)
            self.assertIn("--max-budget-usd", a)
            self.assertIn("Diff to review:", call["stdin"], "the frozen prep brief goes in on stdin")
        ev = [e for e in c.ledger_tail(self.project(), 200) if e.get("event") == "finding"]
        self.assertEqual(len(ev), 2)
        self.assertEqual({e["data"]["lens"] for e in ev}, {"edge"})
        block = next(b for b in c.load_briefs(self.project()) if b.id == self.tid)
        self.assertTrue(any("changes needed" in l and "audit edge" in l for l in block.evidence()))
        self.assertTrue(any("audit intent" in l and "→ ok" in l for l in block.evidence()))

    def test_one_lens_only_and_a_failed_reviewer_records_nothing_for_it(self):
        p = self.run_audit("--lens", "edge", "--lens", "intent", env={"STUB_FAIL_LENS": "intent"}, check=False)
        self.assertEqual(sorted(x["lens"] for x in self.calls()), ["edge", "intent"])
        self.assertEqual(self.audits(), ["edge"], "a reviewer that failed is no verdict")
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("intent", p.stderr)

    def test_refuses_when_the_budget_is_spent(self):
        self.fm("budget", "set", "--day", "1")
        bud.record("ideas", 5.0, project=self.project().slug)
        p = self.run_audit(check=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("budget", p.stderr)
        self.assertEqual(self.calls(), [])
        self.assertEqual(self.audits(), [])

    def test_does_not_run_once_the_contract_is_over(self):
        self.fm("contract", "--until", "23:59")
        pr = self.project()
        c.update_meta(pr, contract={**c.read_meta(pr)["contract"], "until": time.time() - 5})
        p = self.run_audit(check=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("contract", p.stderr)
        self.assertEqual(self.calls(), [])
        self.assertEqual(self.audits(), [])

    def test_prep_diff_holds_uncommitted_edits_beside_a_lane_branch_commit(self):  # T-1296
        import subprocess
        g = lambda *a: subprocess.run(["git", "-C", self.repo, *a], check=True, capture_output=True)  # noqa: E731
        g("add", "a.py")
        g("commit", "-qm", "a")
        with open(os.path.join(self.repo, "a.py"), "w") as f:
            f.write("x = 2\n")  # uncommitted edit
        g("branch", "foreman/lane")
        g("checkout", "-q", "foreman/lane")
        with open(os.path.join(self.repo, "CHANGELOG.md"), "w") as f:
            f.write("- a line\n")
        g("add", "CHANGELOG.md")
        g("commit", "-qm", "changelog")
        g("checkout", "-q", "main")
        b = next(x for x in c.load_briefs(self.project()) if x.id == self.tid)
        b.meta["lane_branch"] = "foreman/lane"
        c.save_brief(self.project(), b)
        self.fm("audit", "prep", self.tid)
        diff = open(os.path.join(self.project().dir, "audits", f"{self.tid}.diff")).read()
        self.assertIn("CHANGELOG.md", diff)
        self.assertIn("+x = 2", diff, "the uncommitted a.py edit is in the diff too")

    def test_prep_diff_of_a_lane_task_leaves_out_another_tasks_uncommitted_edits(self):  # T-1579
        import subprocess
        g = lambda *a: subprocess.run(["git", "-C", self.repo, *a], check=True, capture_output=True)  # noqa: E731
        g("add", "a.py")
        g("commit", "-qm", "a")
        g("branch", "foreman/lane")
        g("checkout", "-q", "foreman/lane")
        with open(os.path.join(self.repo, "CHANGELOG.md"), "w") as f:
            f.write("- a line\n")
        g("add", "CHANGELOG.md")
        g("commit", "-qm", "changelog")
        g("checkout", "-q", "main")
        with open(os.path.join(self.repo, "a.py"), "w") as f:
            f.write("x = 2\n")  # the main checkout's own task, not the lane's
        b = next(x for x in c.load_briefs(self.project()) if x.id == self.tid)
        b.meta.update(lane_branch="foreman/lane", lane=os.path.join(self.repo, ".claude", "worktrees", "lane"))
        c.save_brief(self.project(), b)
        self.fm("audit", "prep", self.tid)
        diff = open(os.path.join(self.project().dir, "audits", f"{self.tid}.diff")).read()
        self.assertIn("CHANGELOG.md", diff)
        self.assertNotIn("+x = 2", diff, "another task's uncommitted edit isn't the lane's")
