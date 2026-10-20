"""T-1214: fm code --worker. Fake worker CLIs (small scripts on PATH) do the work; the harness judges what they changed
(the guard on each file, Git's own config and hooks restored) and its own verify decides. No real CLI, no model."""
import json
import os
import shutil
import subprocess
import sys
import time
import unittest

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

    def test_a_worker_cannot_change_the_files_the_verify_names(self):  # T-1271
        spec = os.path.join(self.repo, "test_calc.py")
        before = read_text(spec)
        self.cli("cheat", 'sed -i "s/a - b/a + b/" calc.py\necho "print(\'ok\')" > test_calc.py\n')
        r = self.work("make calc.add add", "--worker", "cheat {prompt}", "--verify", VERIFY)
        self.assertEqual(read_text(spec), before)
        self.assertIn("reverted test_calc.py", r.stdout)
        self.assertIn("return a + b", self.calc())
        self.assertEqual(self.task()["status"], "done", r.stdout + r.stderr)

    def test_a_folder_the_verify_names_is_protected_too(self):  # T-1271
        os.makedirs(os.path.join(self.repo, "tests"))
        t = os.path.join(self.repo, "tests", "test_x.py")
        with open(t, "w") as f:
            f.write("import unittest\n\n\nclass T(unittest.TestCase):\n    def test_t(self):\n        pass\n")
        subprocess.run(["git", "add", "-A"], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-qm", "tests"], cwd=self.repo, check=True)
        self.cli("cheat", 'sed -i "s/a - b/a + b/" calc.py\necho "assert 1" > tests/test_x.py\n')
        r = self.work("make calc.add add", "--worker", "cheat {prompt}", "--verify",
                      "python3 test_calc.py && python3 -m unittest discover -s tests")
        self.assertIn("def test_t", read_text(t))
        self.assertIn("reverted tests/test_x.py", r.stdout)

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

    def test_no_preset_auto_approves_a_workers_shell_commands(self):
        # security review: gemini --yolo and aider --yes-always ran any shell command the CLI chose, which Foreman's
        # guard never sees (it judges the files afterwards, not the commands)
        import fmcode
        self.assertNotIn("--yolo", fmcode.WORKERS["gemini"])
        self.assertIn("--approval-mode auto_edit", fmcode.WORKERS["gemini"])
        self.assertIn("--no-suggest-shell-commands", fmcode.WORKERS["aider"])
        self.assertNotIn("opencode", fmcode.WORKERS, "its run mode doesn't confine shell commands")

    def test_a_worker_gets_no_forge_cloud_or_registry_credentials(self):
        out = os.path.join(self.tmp, "env")
        self.cli("envy", f'env > {out}\nsed -i "s/a - b/a + b/" calc.py\n')
        self.code("make calc.add add", "--worker", "envy {prompt}", "--verify", VERIFY,
                  env={"PATH": self.bin + os.pathsep + os.environ["PATH"], "GITHUB_TOKEN": "ghp_x1",
                       "AWS_SECRET_ACCESS_KEY": "aws1", "NPM_TOKEN": "npm1",  # pragma: allowlist secret
                       "OPENAI_API_KEY": "sk-keep1",  # pragma: allowlist secret
                       "PGPASSWORD": "pg1", "STRIPE_API_KEY": "st1", "MYSQL_PWD": "my1"})  # pragma: allowlist secret
        seen = read_text(out)
        for gone in ("GITHUB_TOKEN", "AWS_SECRET_ACCESS_KEY", "NPM_TOKEN", "PGPASSWORD", "STRIPE_API_KEY", "MYSQL_PWD"):
            self.assertNotIn(gone + "=", seen)
        self.assertIn("OPENAI_API_KEY=sk-keep1", seen, "a model key stays, so the CLI can log in")

    def test_a_write_hidden_by_a_gitignore_line_is_still_judged(self):
        # the builder's open item: a worker adds a .gitignore line, then writes the path it hides
        self.cli("hider", 'sed -i "s/a - b/a + b/" calc.py\necho ".claude/" >> .gitignore\nmkdir -p .claude\n'
                          'echo "{}" > .claude/settings.json\n')
        r = self.work("make calc.add add", "--worker", "hider {prompt}", "--verify", VERIFY)
        self.assertFalse(os.path.exists(os.path.join(self.repo, ".claude", "settings.json")), r.stdout + r.stderr)
        self.assertIn("reverted .claude/settings.json", r.stdout)

    # -- the review's findings (research T-1214-review)
    def git(self, *a):
        return subprocess.run(["git", "-C", self.repo, *a], capture_output=True, text=True).stdout.strip()

    def commit_files(self, files):
        for name, text in files.items():
            with open(os.path.join(self.repo, name), "w") as f:
                f.write(text)
        self.git("add", "-f", *files)
        self.git("commit", "-qm", "setup")

    @unittest.skipUnless(sys.platform.startswith("linux") and shutil.which("setsid"), "the subreaper is Linux's")
    def test_a_process_the_worker_detached_dies_with_its_turn(self):
        # setsid left the process group, so it outlived the kill and could plant a hook after the judge
        pid = os.path.join(self.tmp, "pid")
        self.cli("detach", f'setsid sleep 60 &\necho $! > {pid}\nsed -i "s/a - b/a + b/" calc.py\n')
        self.work("make calc.add add", "--worker", "detach {prompt}", "--verify", VERIFY)
        with self.assertRaises(ProcessLookupError):
            os.kill(int(read_text(pid)), 0)

    def test_the_verify_runs_without_the_credentials_the_worker_never_got(self):
        seen = os.path.join(self.tmp, "seen")
        self.cli("leak", 'sed -i "s/a - b/a + b/" calc.py\n'
                         f"cat > probe.py <<EOF\nimport os\nopen('{seen}', 'w').write("
                         "os.environ.get('GITHUB_TOKEN', 'none'))\nEOF\n")  # a new file: --verify doesn't name it yet
        self.code("make calc.add add", "--worker", "leak {prompt}", "--verify", VERIFY + " && python3 probe.py",
                  env={"PATH": self.bin + os.pathsep + os.environ["PATH"], "GITHUB_TOKEN": "ghp_x1"})
        self.assertEqual(read_text(seen), "none")

    def test_a_credential_file_git_ignores_is_put_back(self):
        self.commit_files({".gitignore": ".env\nnode_modules/\n"})
        with open(os.path.join(self.repo, ".env"), "w") as f:
            f.write("SECRET=mine\n")
        self.cli("envw", 'sed -i "s/a - b/a + b/" calc.py\necho "SECRET=pwned" > .env\n')
        r = self.work("make calc.add add", "--worker", "envw {prompt}", "--verify", VERIFY)
        self.assertEqual(read_text(os.path.join(self.repo, ".env")), "SECRET=mine\n")
        self.assertIn("reverted .env", r.stdout)

    def test_a_big_ignored_build_folder_keeps_the_fix_and_a_hidden_write_is_still_judged(self):
        self.commit_files({".gitignore": "node_modules/\n"})
        self.cli("npm", 'sed -i "s/a - b/a + b/" calc.py\nmkdir -p node_modules/x\n'
                        'for i in $(seq 400); do echo $i > node_modules/x/f$i.js; done\n'
                        'echo ".claude/" >> .gitignore\nmkdir -p .claude\necho "{}" > .claude/settings.json\n')
        r = self.work("make calc.add add", "--worker", "npm {prompt}", "--verify", VERIFY)
        self.assertIn("return a + b", self.calc())
        self.assertEqual(len(os.listdir(os.path.join(self.repo, "node_modules", "x"))), 400)
        self.assertFalse(os.path.exists(os.path.join(self.repo, ".claude", "settings.json")), r.stdout)
        self.assertEqual(self.task()["status"], "done", r.stdout + r.stderr)

    def test_a_change_hidden_with_assume_unchanged_is_seen_and_committed(self):
        self.cli("hide", 'git update-index --assume-unchanged calc.py\nsed -i "s/a - b/a + b/" calc.py\n')
        r = self.work("make calc.add add", "--worker", "hide {prompt}", "--verify", VERIFY)
        self.assertEqual(self.task()["status"], "done", r.stdout + r.stderr)
        self.assertIn("calc.py", self.last_commit())
        self.assertTrue(self.git("ls-files", "-v", "calc.py").startswith("H "))

    def test_a_planted_hook_in_a_read_only_hooks_folder_is_still_removed(self):
        self.cli("lock", 'sed -i "s/a - b/a + b/" calc.py\nprintf "#!/bin/sh\\n" > .git/hooks/pre-commit\n'
                         'chmod +x .git/hooks/pre-commit\nchmod 555 .git/hooks\n')
        r = self.work("make calc.add add", "--worker", "lock {prompt}", "--verify", VERIFY, check=False)
        self.assertNotIn("Traceback", r.stderr)
        self.assertFalse(os.path.exists(os.path.join(self.repo, ".git", "hooks", "pre-commit")))

    def test_a_sensitive_repo_never_goes_to_a_worker(self):
        self.fm("sensitive", "on")
        self.cli("claude", "echo hi\n")
        r = self.work("make calc.add add", "--worker", "claude", "--verify", VERIFY, check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn("sensitive", r.stderr)
        self.assertNotEqual(self.fm("task", "show", "T-0001", check=False).returncode, 0)

    def test_the_users_own_hooks_link_and_global_git_config_are_kept_and_put_back(self):
        ext = os.path.join(self.tmp, "githooks")
        os.makedirs(ext)
        hooks = os.path.join(self.repo, ".git", "hooks")
        shutil.rmtree(hooks)
        os.symlink(ext, hooks)
        self.cli("glob", 'sed -i "s/a - b/a + b/" calc.py\n'
                         'printf "[core]\\n\\tfsmonitor = /nonexistent/evil\\n" >> "$HOME/.gitconfig"\n')
        r = self.work("make calc.add add", "--worker", "glob {prompt}", "--verify", VERIFY)
        self.assertTrue(os.path.islink(hooks))
        self.assertFalse(os.path.exists(os.path.join(self.fake_home, ".gitconfig")), r.stdout)

    def test_a_branch_switch_from_a_detached_head_leaves_that_branch_alone(self):
        sha = self.git("rev-parse", "HEAD")
        self.git("branch", "other")
        self.git("checkout", "-q", "--detach")
        self.cli("hop", 'git switch -q other\ngit commit -q --allow-empty -m mine\nsed -i "s/a - b/a + b/" calc.py\n')
        self.work("make calc.add add", "--worker", "hop {prompt}", "--verify", VERIFY, check=False)
        self.assertNotEqual(self.git("rev-parse", "other"), sha)  # its commit stays on it
        self.assertEqual(self.git("symbolic-ref", "-q", "HEAD"), "")  # detached again

    def test_worker_argv(self):
        import fmcode
        self.assertEqual(fmcode.worker_argv("codex", "do it", which=False), ["codex", "exec", "--full-auto", "do it"])
        self.assertEqual(fmcode.worker_argv("my-cli --msg={prompt} -q", "a b", which=False),
                         ["my-cli", "--msg=a b", "-q"])
        self.assertEqual(fmcode.worker_argv("plain", "x y", which=False), ["plain", "x y"])


if __name__ == "__main__":
    import unittest
    unittest.main()
