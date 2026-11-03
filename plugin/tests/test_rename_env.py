"""T-2742 step 2 (SAMPO.md): every SAMPO_* variable is read, with its FOREMAN_* twin as the fallback (SAMPO_ wins when
both are set), and commits carry a Sampo-Task trailer while both it and Foreman-Task are read, forever."""
import os
import subprocess
import sys

from helpers import FM, ForemanTestCase


class RenameEnv(ForemanTestCase):
    def run_fm(self, env, *args):
        """fm with no FOREMAN_* or SAMPO_* but these, and a scratch HOME, so a name it ignores never reaches a real home."""
        e = {k: v for k, v in os.environ.items() if not k.startswith(("FOREMAN_", "SAMPO_"))}
        e.update(HOME=os.path.join(self.tmp, "nohome"), FOREMAN_NO_LINK="1", FOREMAN_INHIBITED="1", **env)
        e.pop("CLAUDE_CODE_SESSION_ID", None)
        return subprocess.run([sys.executable, FM, *args], cwd=self.repo, env=e, capture_output=True, text=True,
                              timeout=60)

    def test_sampo_home_names_the_home(self):
        home = os.path.join(self.tmp, "sampo-home")
        r = self.run_fm({"SAMPO_HOME": home}, "init")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(os.path.isdir(os.path.join(home, "state", "projects")), "SAMPO_HOME is read")
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "nohome", ".claude", "foreman", "state")))

    def test_sampo_wins_over_its_foreman_twin_and_the_old_name_still_works(self):
        new, old = os.path.join(self.tmp, "new"), os.path.join(self.tmp, "old")
        self.run_fm({"SAMPO_HOME": new, "FOREMAN_HOME": old}, "init")
        self.assertTrue(os.path.isdir(os.path.join(new, "state", "projects")))
        self.assertFalse(os.path.exists(os.path.join(old, "state")))
        self.run_fm({"FOREMAN_HOME": old}, "init")
        self.assertTrue(os.path.isdir(os.path.join(old, "state", "projects")), "FOREMAN_HOME alone still works")

    def test_both_trailers_name_a_tasks_commits(self):
        self.fm("init")
        tid = self.fm_json("task", "new", "Export CSV", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true",
                           "--step", "do")["id"]
        for key in ("Sampo-Task", "Foreman-Task"):
            subprocess.run(["git", "-C", self.repo, "commit", "--allow-empty", "-qm", f"Work under {key}", "-m",
                            f"{key}: {tid}"], check=True, capture_output=True)
        self.assertIn("2 commit(s)", self.fm("task", "revert", tid).stdout)
