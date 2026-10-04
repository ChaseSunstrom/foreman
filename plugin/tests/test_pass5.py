"""Self-improvement pass 5: fm replay --cmd asks the guard about one command without running it; the pre-audit's
security code patterns read code files only."""
import json
import os

from helpers import ForemanTestCase


class Probe(ForemanTestCase):
    def test_one_commands_verdict_without_running_it(self):
        cmd = "mkdir -p ~/fm-replay-probe-never-made && rm -rf ~/fm-replay-probe-never-made"
        res = json.loads(self.fm("replay", "--cmd", cmd, "--cwd", self.repo, "--json").stdout)
        self.assertEqual(res["verdict"], "rm-outside")
        self.assertIn("fm-replay-probe-never-made", res["detail"])
        self.assertFalse(os.path.exists(os.path.expanduser("~/fm-replay-probe-never-made")))  # asked, never run
        out = self.fm("replay", "--cmd", "ls -la", "--cwd", self.repo).stdout
        self.assertIn("allow", out)


class Patterns(ForemanTestCase):
    def test_docs_naming_the_patterns_dont_flag_a_change(self):
        import fmcore as c
        doc = "diff --git a/MASTER.md b/MASTER.md\n--- a/MASTER.md\n+++ b/MASTER.md\n@@ -1 +1 @@\n" \
              "+the pre-audit flags `urlopen(` and `requests.get(` calls\n"
        code = "diff --git a/get.py b/get.py\n--- a/get.py\n+++ b/get.py\n@@ -1 +1 @@\n" \
               "+    return urllib.request.urlopen(url).read()\n"
        self.assertEqual(c.sensitive(["MASTER.md"], doc), [])
        self.assertEqual(c.sensitive(["get.py"], code), ["urlopen("])
        self.assertEqual(c.sensitive(["MASTER.md", "get.py"], doc + code), ["urlopen("])
