"""Self-improvement pass 1 (T-0269): a guard false positive from the friction digest (T-0265), small tasks that grow
past small (T-0266) and prompt-cache-friendly brainstorm children (T-0267)."""
import json
import os

from helpers import ForemanTestCase
from test_guard import GuardCase


class Stash(GuardCase):
    def test_listing_and_showing_are_read_only(self):
        self.run_table([
            ("cd {fhome} && git stash list", None),
            ("cd {fhome} && git stash show -p stash@{{0}}", None),
            ("git -C {fhome} stash list", None),
            ("cd {fhome} && git stash", "core"),
            ("cd {fhome} && git stash pop", "core"),
            ("cd {fhome} && git stash apply", "core"),
            ("cd {fhome} && git stash drop", "core"),
            ("cd {fhome} && git stash push -m x", "core"),
        ], lambda cmd: self.bash(cmd))

    def test_git_s_own_write_and_exec_channels_are_checked(self):  # T-0269 review: not only stash
        for cmd in (
            "cd {fhome} && git stash show -p --output=plugin/lib/fmguard.py",
            "git diff --output={fhome}/plugin/lib/fmguard.py",
            "git -C {fhome} log -p --output plugin/lib/x.py",
            "git -c core.pager='cp /tmp/a {fhome}/plugin/lib/fmguard.py' -p log",
            "git -c diff.external='cp /tmp/a {fhome}/plugin/lib/fmguard.py' diff --ext-diff",
            "GIT_EXTERNAL_DIFF='cp /tmp/a {fhome}/plugin/lib/fmguard.py' git diff",
            "git -c 'alias.x=!cp /tmp/a {fhome}/plugin/lib/fmguard.py' x",
            "git -C {fhome} -c alias.co=checkout co -- plugin/lib/fmguard.py",
            "git -C {fhome} --config-env a=B checkout -- plugin/lib/fmguard.py",
            "git --exec-path=/tmp/evil status",
            "GIT_EXEC_PATH=/tmp/evil git status",
            "GIT_CONFIG_PARAMETERS=\"'core.sshCommand=cp /tmp/a {fhome}/plugin/lib/x.py'\" git fetch",
            "git -c 'credential.https://x.helper=!cp /tmp/a {fhome}/plugin/lib/x.py' fetch",
        ):
            with self.subTest(cmd=cmd):
                self.assertIsNotNone(self.bash(cmd), cmd)
        for cmd in ("git -c core.pager=less log", "git -c user.name=x commit --allow-empty -m x", "git diff --stat",
                    "git -c alias.st=status st", "git stash list --output=/tmp/stashes.txt"):
            with self.subTest(cmd=cmd):
                self.assertIsNone(self.bash(cmd), cmd)


class Outgrown(ForemanTestCase):
    def test_an_s_task_touching_three_files_is_told_to_retier(self):
        self.fm("init")
        tid = json.loads(self.fm("task", "new", "Rename the flag", "--type", "FIX", "--tier", "S", "--ac", "x :: true",
                                 "--step", "rename", "--json").stdout)["id"]
        self.fm("focus", tid)
        for n, name in enumerate(("a.py", "b.py", "tests/test_a.py")):
            path = os.path.join(self.repo, name)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            self.hook("PostToolUse", {"tool_name": "Write", "tool_input": {"file_path": path, "content": "x"},
                                      "tool_response": {}})
        self.assertNotIn("outgrown", self.fm("next").stdout)  # two source files and a test: still small
        self.hook("PostToolUse", {"tool_name": "Write", "tool_input": {"file_path": os.path.join(self.repo, "c.py"),
                                                                        "content": "x"}, "tool_response": {}})
        out = self.fm("next").stdout
        self.assertIn("outgrown", out)
        self.assertIn(f"fm task set {tid} tier=M", out)


class Prefix(ForemanTestCase):
    def test_siblings_and_later_rounds_share_the_pack_prefix(self):
        import fmideas
        pack = "# pack\n" + "context line\n" * 50
        a, b = fmideas.child_prompt("bold bets", pack), fmideas.child_prompt("reliability", pack)
        shared = os.path.commonprefix([a, b])
        self.assertIn(pack, shared)
        later = fmideas.child_prompt("bold bets", fmideas.later_round_pack(pack, ["idea one"], 2))
        self.assertIn(pack, os.path.commonprefix([a, later]))
