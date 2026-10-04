"""fm bench (T-0212): finished tasks replayed as benchmark cases — the repo at the task commit's parent, the original
request, a fresh Foreman state, the candidate plugin; graded by the task's own tests and verify commands."""
import json
import os
import subprocess

from helpers import ForemanTestCase, read_text

import fmcore as c

STUB = r'''#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
with open(os.environ["STUB_LOG"], "a") as f:
    f.write(json.dumps({"args": args, "cwd": os.getcwd(), "state": os.environ.get("FOREMAN_STATE"),
                        "path": os.environ.get("PATH", "").split(os.pathsep)[0],
                        "creds": [k for k in ("GITHUB_TOKEN", "AWS_SECRET_ACCESS_KEY") if k in os.environ],
                        "login": os.environ.get("CLAUDE_CODE_OAUTH_TOKEN")}) + "\n")
if os.environ.get("STUB_DIAG"):  # behave a little like a Foreman session: a task, and one guard block
    import subprocess
    subprocess.run(["fm", "task", "new", "Fix double", "--type", "FIX", "--tier", "S"], capture_output=True)
    with open(os.path.join(os.environ["FOREMAN_STATE"], "events.jsonl"), "a") as f:
        f.write(json.dumps({"kind": "guard_block", "category": "rm-outside", "tool": "Bash"}) + "\n")
if os.environ.get("STUB_SOLVE"):
    with open("calc.py", "w") as f:
        f.write("def double(x):\n    return 2 * x\n")
print(json.dumps({"type": "result", "is_error": False, "total_cost_usd": 0.42, "num_turns": 7, "duration_ms": 1234,
                  "result": "done"}))
'''


def git(cwd, *args):
    return subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True, check=True).stdout.strip()


class Bench(ForemanTestCase):
    def setUp(self):
        super().setUp()
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        self.log = os.path.join(self.tmp, "stub.log")
        self.env = {"PATH": bindir + os.pathsep + os.environ["PATH"], "STUB_LOG": self.log}
        self.fm("init")
        self.write("calc.py", "def double(x):\n    return x + x + 1\n")
        git(self.repo, "add", "calc.py")
        git(self.repo, "commit", "-qm", "calc")
        self.base = git(self.repo, "rev-parse", "HEAD")
        self.tid = self.finished_task("double() is off by one", "PYTHONPATH=. python3 tests/test_calc.py")
        self.write("calc.py", "def double(x):\n    return x * 2\n")
        self.write("tests/test_calc.py", "from calc import double\nassert double(3) == 6, double(3)\nprint('ok')\n")
        git(self.repo, "add", "-A", "calc.py", "tests")
        git(self.repo, "commit", "-qm", f"double() is right ({self.tid})")

    def write(self, rel, text):
        path = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)

    def finished_task(self, title, verify):
        tid = json.loads(self.fm("task", "new", title, "--type", "FIX", "--tier", "S", "--ac", f"fixed :: {verify}",
                                 "--step", "fix it", "--json").stdout)["id"]
        self.fm("task", "set", tid, "--section", "Raw request", "--text", f"> {title}; fix it")
        self.fm("focus", tid)
        self.fm("task", "step", tid, "done", "1", "--evidence", "x", "ok")
        self.fm("task", "ac", tid, "check", "1", "--evidence", "x", "ok")
        self.fm("task", "audit", tid, "self", "x", "ok")
        self.fm("task", "set", tid, "--section", "Regression test", "--text", "none: fixture")
        self.fm("task", "done", tid)
        return tid

    def calls(self):
        return [json.loads(l) for l in read_text(self.log).splitlines()]

    def test_build_keeps_cases_that_fail_before_and_pass_after(self):
        res = json.loads(self.fm("bench", "build", "--json", env=self.env).stdout)
        self.assertEqual([x["id"] for x in res["cases"]], [self.tid])
        case = res["cases"][0]
        self.assertEqual(case["base"], self.base)
        self.assertEqual(case["tests"], ["tests/test_calc.py"])
        self.assertEqual(case["verify"], ["PYTHONPATH=. python3 tests/test_calc.py"])
        self.assertIn("off by one", case["prompt"])
        self.assertEqual(git(self.repo, "worktree", "list").count("\n"), 0, "validation worktrees are removed")

    def test_a_case_that_passes_without_the_change_is_dropped(self):
        tid = self.finished_task("add a readme", "true")
        self.write("README.md", "hi\n")
        self.write("tests/test_readme.py", "print('ok')\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-qm", f"readme ({tid})")
        res = json.loads(self.fm("bench", "build", "--json", env=self.env).stdout)
        self.assertNotIn(tid, [x["id"] for x in res["cases"]])
        self.assertIn(tid, " ".join(res["skipped"]))

    def test_tests_the_commit_deleted_are_not_hidden_tests(self):
        # T-0212 review: a deleted test made `git checkout` fail and the grade ran without the hidden tests
        self.write("tests/test_old.py", "print('old')\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-qm", "old test")
        tid = self.finished_task("triple() exists", "PYTHONPATH=. python3 tests/test_triple.py")
        os.remove(os.path.join(self.repo, "tests", "test_old.py"))
        self.write("calc.py", "def double(x):\n    return x * 2\n\n\ndef triple(x):\n    return 3 * x\n")
        self.write("tests/test_triple.py", "from calc import triple\nassert triple(2) == 6\nprint('ok')\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-qm", f"triple ({tid})")
        res = json.loads(self.fm("bench", "build", "--ids", tid, "--json", env=self.env).stdout)
        self.assertEqual(res["cases"][0]["tests"], ["tests/test_triple.py"])
        self.fm("bench", "build", "--ids", self.tid, env=self.env)
        cases = json.loads(self.fm("bench", "list", "--json", env=self.env).stdout)["cases"]
        self.assertEqual(sorted(x["id"] for x in cases), sorted([tid, self.tid]), "--ids adds, it doesn't replace")

    def test_a_crashing_case_keeps_the_others_results(self):
        self.fm("bench", "build", env=self.env)
        broken = os.path.join(self.tmp, "broken")
        os.makedirs(os.path.join(broken, ".claude-plugin"))
        os.makedirs(os.path.join(broken, "hooks"))
        os.makedirs(os.path.join(broken, "lib"))
        for rel, text in ((".claude-plugin/plugin.json", '{"name": "broken"}'), ("lib/fmguard.py", ""),
                          ("hooks/hooks.json", '{"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": []}]}}')):
            with open(os.path.join(broken, rel), "w") as f:
                f.write(text)
        out = self.fm("bench", "run", "--plugin", broken, "--label", "broken", "--json", env=self.env, check=False)
        res = json.loads(out.stdout)
        self.assertFalse(res["cases"][0]["pass"])
        self.assertTrue(res["cases"][0]["error"], "no bin/fm: recorded as the case's error, not a crash")
        self.assertIn("broken", self.fm("bench", "list", env=self.env).stdout, "the results file was written")
        self.assertEqual(git(self.repo, "worktree", "list").count("\n"), 0)

    def test_a_replay_says_what_its_foreman_did(self):
        # T-0220: a failure pinned to a stage: did it plan, verify, get blocked?
        self.fm("bench", "build", env=self.env)
        res = json.loads(self.fm("bench", "run", "--label", "diag", "--json", env=dict(self.env, STUB_DIAG="1"),
                                 check=False).stdout)
        diag = res["cases"][0]["diag"]
        self.assertEqual(list(diag["tasks"].values()), ["FIX S planned"])
        self.assertEqual(diag["guard_blocks"], {"rm-outside": 1})
        self.assertGreaterEqual(diag["ledger"].get("capture", 0) + diag["ledger"].get("task_new", 0), 1)
        out = self.fm("bench", "show", "diag", env=self.env).stdout
        self.assertIn("FIX S planned", out)
        self.assertIn("rm-outside", out)

    def test_a_plugin_without_the_guard_or_credentials_never_runs(self):
        # security review: replays run in bypass mode like the user's sessions, so the guard must come with them
        self.fm("bench", "build", env=self.env)
        bare = os.path.join(self.tmp, "bare")
        os.makedirs(os.path.join(bare, ".claude-plugin"))
        with open(os.path.join(bare, ".claude-plugin", "plugin.json"), "w") as f:
            f.write('{"name": "bare"}')
        out = self.fm("bench", "run", "--plugin", bare, env=self.env, check=False)
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("guard", out.stdout + out.stderr)
        self.assertFalse(os.path.exists(self.log), "no session started")
        self.fm("bench", "run", "--label", "creds", env=dict(self.env, GITHUB_TOKEN="ghp_x", AWS_SECRET_ACCESS_KEY="y",
                                                              CLAUDE_CODE_OAUTH_TOKEN="keep", STUB_SOLVE="1"))
        self.assertEqual(self.calls()[-1]["creds"], [], "cloud and forge credentials stay behind")
        self.assertEqual(self.calls()[-1]["login"], "keep", "claude's own login goes along")

    def test_run_replays_in_isolation_and_grades_by_hidden_tests(self):
        self.fm("bench", "build", env=self.env)
        fail = json.loads(self.fm("bench", "run", "--label", "nofix", "--json", env=self.env, check=False).stdout)
        self.assertFalse(fail["cases"][0]["pass"], "the stub changed nothing: the hidden test fails")
        good = json.loads(self.fm("bench", "run", "--label", "fix", "--json",
                                  env=dict(self.env, STUB_SOLVE="1")).stdout)
        case = good["cases"][0]
        self.assertTrue(case["pass"], case)
        self.assertEqual((case["cost_usd"], case["turns"]), (0.42, 7))
        call = self.calls()[-1]
        self.assertIn("--plugin-dir", call["args"])
        self.assertEqual(call["args"][call["args"].index("--plugin-dir") + 1], c.PLUGIN_ROOT)
        self.assertIn("off by one", " ".join(call["args"]))
        self.assertNotEqual(os.path.realpath(call["cwd"]), os.path.realpath(self.repo))
        self.assertTrue(call["state"] and not call["state"].startswith(c.state_dir()), "a fresh Foreman state")
        self.assertEqual(call["path"], os.path.join(c.PLUGIN_ROOT, "bin"), "the candidate's fm comes first")
        self.assertEqual(git(self.repo, "worktree", "list").count("\n"), 0, "the replay worktree is removed")
        self.assertEqual(read_text(os.path.join(self.repo, "calc.py")), "def double(x):\n    return x * 2\n")
        out = self.fm("bench", "compare", "nofix", "fix", env=self.env).stdout
        self.assertIn("0/1", out)
        self.assertIn("1/1", out)
