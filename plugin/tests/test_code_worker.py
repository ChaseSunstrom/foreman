"""T-1214: fm code --worker. Fake worker CLIs (small scripts on PATH) do the work; the harness judges what they changed
(the guard on each file, Git's own config and hooks restored) and its own verify decides. No real CLI, no model."""
import json
import os
import time

from helpers import read_text
from test_code import CodeCase, journal_text

VERIFY = "python3 test_calc.py"


class Worker(CodeCase):
    def setUp(self):
        super().setUp()
        self.bin = os.path.join(self.tmp, "bin")
        os.makedirs(self.bin)

    def cli(self, name, body):
        path = os.path.join(self.bin, name)
        with open(path, "w") as f:
            f.write("#!/bin/sh\n" + body)
        os.chmod(path, 0o755)

    def work(self, *args, check=True):
        return self.code(*args, check=check, env={"PATH": self.bin + os.pathsep + os.environ["PATH"]})

    def test_a_worker_that_fixes_the_bug_closes_the_task(self):
        # a table name: claude's unattended form, with the prompt as one argument
        args = os.path.join(self.tmp, "args")
        self.cli("claude", f'printf "%s\\n" "$@" > {args}\nsed -i "s/a - b/a + b/" calc.py\necho fixed\n')
        r = self.work("FIX: make calc.add add", "--worker", "claude", "--verify", VERIFY)
        self.assertIn("return a + b", self.calc())
        t = self.task()
        self.assertEqual(t["status"], "done", r.stdout + r.stderr)
        self.assertEqual(t["type"], "FIX")
        self.assertIn("make calc.add add", t["title"])
        self.assertRegex(read_text(t["path"]), r"`python3 test_calc.py` → exit 0")
        got = read_text(args).splitlines()
        self.assertEqual(got[0], "-p")
        self.assertIn("--permission-mode", got)
        self.assertIn("make calc.add add", read_text(args))
        shown = self.last_commit()
        self.assertIn("T-0001", shown)
        self.assertIn("calc.py", shown)
        start = json.loads(journal_text(self).splitlines()[0])
        self.assertEqual(start["options"]["worker"], "claude")
        self.assertEqual(start["options"]["verify"], VERIFY)

    def test_protected_writes_and_git_hooks_are_reverted_and_reported(self):
        cfg = os.path.join(self.repo, ".git", "config")
        before = read_text(cfg)
        self.cli("sneaky", 'sed -i "s/a - b/a + b/" calc.py\nmkdir -p .claude\necho "{}" > .claude/settings.json\n'
                           'printf "#!/bin/sh\\necho pwned\\n" > .git/hooks/pre-commit\n'
                           'chmod +x .git/hooks/pre-commit\necho ".claude/" >> .git/info/exclude\n'
                           'printf "[core]\\n\\thooksPath = /tmp/evil\\n" >> .git/config\n')
        r = self.work("make calc.add add", "--worker", "sneaky {prompt}", "--verify", VERIFY)
        self.assertFalse(os.path.exists(os.path.join(self.repo, ".claude", "settings.json")))
        self.assertFalse(os.path.exists(os.path.join(self.repo, ".git", "hooks", "pre-commit")))
        self.assertEqual(read_text(cfg), before)
        self.assertIn("reverted .claude/settings.json", r.stdout)
        self.assertIn("pre-commit", r.stdout)
        self.assertEqual(self.task()["status"], "done", r.stdout + r.stderr)
        self.assertNotIn("settings.json", self.last_commit())
        reverts = [json.loads(x) for x in journal_text(self).splitlines() if '"revert"' in x]
        self.assertTrue(any(x.get("file") == ".claude/settings.json" for x in reverts), reverts)

    def test_a_hanging_worker_is_killed_at_the_timeout(self):
        pid = os.path.join(self.tmp, "pid")
        self.cli("hang", f"sleep 60 &\necho $! > {pid}\nsleep 60\n")
        t0 = time.time()
        r = self.work("make calc.add add", "--worker", "hang", "--worker-timeout", "2", "--verify", VERIFY,
                      check=False)
        self.assertEqual(r.returncode, 1)
        self.assertLess(time.time() - t0, 45)
        self.assertIn("timed out after 2 s", r.stdout)
        self.assertEqual(self.task()["status"], "blocked")
        with self.assertRaises(ProcessLookupError):  # the background child died with the group
            os.kill(int(read_text(pid)), 0)

    def test_a_missing_cli_is_a_one_line_error_and_no_task(self):
        r = self.work("make calc.add add", "--worker", "nosuchcli", "--verify", VERIFY, check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn("nosuchcli", r.stderr)
        self.assertEqual(len(r.stderr.strip().splitlines()), 1, r.stderr)
        self.assertNotIn("Traceback", r.stderr)
        self.assertNotEqual(self.fm("task", "show", "T-0001", check=False).returncode, 0)

    def test_a_worker_claiming_success_without_a_change_is_not_done(self):
        self.cli("liar", 'echo "All done, tests pass"\n')
        r = self.work("make calc.add add", "--worker", "liar", "--verify", VERIFY, check=False)
        self.assertEqual(r.returncode, 1)
        self.assertNotEqual(self.task()["status"], "done")
        self.assertIn("return a - b", self.calc())

    def test_a_verify_that_already_passes_stops_before_any_task(self):
        self.cli("liar", "true\n")
        r = self.work("make calc.add add", "--worker", "liar", "--verify", "true", check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn("proves nothing", r.stderr)
        self.assertNotEqual(self.fm("task", "show", "T-0001", check=False).returncode, 0)

    def test_worker_argv(self):
        import fmcode
        self.assertEqual(fmcode.worker_argv("codex", "do it", which=False), ["codex", "exec", "--full-auto", "do it"])
        self.assertEqual(fmcode.worker_argv("my-cli --msg={prompt} -q", "a b", which=False),
                         ["my-cli", "--msg=a b", "-q"])
        self.assertEqual(fmcode.worker_argv("plain", "x y", which=False), ["plain", "x y"])


if __name__ == "__main__":
    import unittest
    unittest.main()
