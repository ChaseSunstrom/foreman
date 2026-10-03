"""T-0113: a resumed task is told which paths and code names its brief cites that existed when it started and are gone
now (renamed, deleted), so it doesn't act on a stale plan; a file the task means to create isn't flagged."""
import json
import os
import subprocess
import unittest

from helpers import ForemanTestCase


class StaleRefs(ForemanTestCase):
    def test_refs_gone_since_the_start_are_named_on_resume(self):
        os.makedirs(os.path.join(self.repo, "src"))
        with open(os.path.join(self.repo, "src", "util.py"), "w") as f:
            f.write("def helper_fn():\n    return 1\n")
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "util"], check=True)
        self.fm("init")
        self.fm("task", "new", "Rework", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true",
                "--step", "change `helper_fn` in src/util.py and add src/new_mod.py", "--focus")
        os.remove(os.path.join(self.repo, "src", "util.py"))  # renamed away by other work
        out = self.fm("resume").stdout
        self.assertIn("stale", out.lower())
        self.assertIn("src/util.py", out)
        self.assertIn("helper_fn", out)
        self.assertNotIn("src/new_mod.py", out.split("tale")[-1], "a file it means to create isn't stale")
        ctx = json.loads(self.hook("SessionStart", {"source": "resume"}).stdout)["hookSpecificOutput"]["additionalContext"]
        self.assertIn("src/util.py", ctx.split("tale", 1)[-1])


if __name__ == "__main__":
    unittest.main()
