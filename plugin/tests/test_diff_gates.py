"""T-0071 round A: what the diff itself tells fm — scope drift, security-sensitive changes, weak verify commands,
outlines of big files and a mechanical pre-audit."""
import json
import os

from helpers import ForemanTestCase

import fmcore as c


class DiffGates(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def task(self, *extra):
        self.fm("task", "new", "change it", "--type", "FEATURE", "--tier", "S", "--step", "do it", "--ac", "works",
                *extra, "--focus")

    def touch(self, rel, text="x = 1\n"):
        path = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)
        with open(os.path.join(self.p.dir, "ledger.jsonl"), "a") as f:  # as the PostToolUse hook records an Edit
            f.write(json.dumps({"ts": c.now(), "task": "T-0001", "event": "touched",
                                "data": {"file": path, "tool": "Edit"}}) + "\n")

    def finish(self, *lenses):
        self.fm("task", "evidence", "T-0001", "--ac", "1", "pytest", "ok")
        self.fm("task", "ac", "T-0001", "check", "1")
        self.fm("task", "step", "T-0001", "done", "1", "--evidence", "pytest", "ok")
        for lens in ("self",) + lenses:
            self.fm("task", "audit", "T-0001", lens, "checked", "ok")
        return self.fm("task", "done", "T-0001", check=False)

    def test_edits_outside_scope_need_a_reason(self):
        self.task("--scope", "src/**")
        self.touch("src/app.py")
        self.touch("setup.cfg")
        p = self.finish()
        self.assertEqual(p.returncode, 2)
        self.assertIn("edited outside scope [src/**]: setup.cfg", p.stderr)
        self.assertNotIn("src/app.py", p.stderr)
        self.fm("task", "log", "T-0001", "scope: the build config names the new module")
        self.assertEqual(self.fm("task", "done", "T-0001", check=False).returncode, 0)

    def test_security_sensitive_change_needs_the_adversary_lens(self):
        self.task()
        self.touch("auth/login.py")
        p = self.finish()
        self.assertEqual(p.returncode, 2)
        self.assertIn("audit missing: adversary", p.stderr)
        self.assertIn("security-sensitive: auth/login.py", p.stderr)
        self.fm("task", "audit", "T-0001", "adversary", "abuse cases", "ok")
        self.assertEqual(self.fm("task", "done", "T-0001", check=False).returncode, 0)

    def test_plain_change_needs_only_the_tier_audits(self):
        self.task()
        self.touch("docs/notes.py")
        self.assertEqual(self.finish().returncode, 0)

    def test_weak_verify_commands_are_flagged_when_written(self):
        p = self.fm("task", "new", "t", "--type", "FEATURE", "--tier", "S", "--ac", "a :: echo ok",
                    "--ac", "b :: pytest -q | tail -3", "--ac", "c :: nosuchtool-xyz --run", "--ac", "d :: git status")
        self.assertIn("`echo ok`: it can't fail", p.stderr)
        self.assertIn("last piped program's", p.stderr)
        self.assertIn("nosuchtool-xyz isn't on PATH", p.stderr)
        self.assertNotIn("git status", p.stderr)
        p = self.fm("task", "ac", "T-0001", "add", "e :: true")
        self.assertIn("can't fail", p.stderr)
        self.assertEqual(c.lint_verify("set -o pipefail; git log | head -1", self.repo), [])
        self.assertEqual(c.lint_verify("cd sub && FOO=1 git status", self.repo), [])

    def test_outline_lists_definitions_with_line_ranges(self):
        py = os.path.join(self.repo, "m.py")
        with open(py, "w") as f:
            f.write("import os\n\n\nclass A:\n    def f(self):\n        return 1\n\n\ndef g():\n    pass\n")
        data = self.fm_json("outline", py)
        self.assertEqual([(d["start"], d["end"], d["depth"], d["name"]) for d in data["defs"]],
                         [(4, 6, 0, "class A"), (5, 6, 1, "def f"), (9, 10, 0, "def g")])
        js = os.path.join(self.repo, "m.js")
        with open(js, "w") as f:
            f.write("export function a() {\n  return 1;\n}\n\nclass B {\n}\n")
        out = self.fm("outline", js).stdout
        self.assertIn("1-3", out)
        self.assertIn("function a", out)
        self.assertIn("class B", out)
        self.assertEqual(self.fm("outline", "nope.py", check=False).returncode, 1)

    def test_audit_prep_lists_mechanical_findings_and_adds_adversary_for_risky_small_changes(self):
        self.task()
        self.touch("auth/token.py", "def check(t):\n    breakpoint()\n    # TODO tighten\n    return eval(t)\n")
        out = self.fm_json("audit", "prep", "T-0001")
        joined = "\n".join(out["pre_audit"])
        for want in ("debug leftover in auth/token.py", "new TODO in auth/token.py",
                     "source changed with no test changed", "security-sensitive"):
            self.assertIn(want, joined)
        self.assertEqual(out["lenses"], ["self", "adversary"])
        with open(out["brief"]) as f:
            self.assertIn("Pre-audit (mechanical", f.read())

    def test_whole_read_of_a_big_file_gets_one_outline_note(self):
        big = os.path.join(self.repo, "big.py")
        with open(big, "w") as f:
            f.write("x = 1\n" * 700)

        def read(**extra):
            r = self.hook("PostToolUse", {"tool_name": "Read", "tool_input": dict(file_path=big, **extra)})
            return json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"] if r.stdout.strip() else ""
        self.assertEqual(read(offset=1, limit=50), "")
        self.assertIn("fm outline", read())
        self.assertEqual(read(), "", "once per session")
