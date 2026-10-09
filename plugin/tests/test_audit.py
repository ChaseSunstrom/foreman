"""T-0723: the diff a reviewer reads (fm audit prep) leaves out what it needn't read in full: a change repeated in
synced copies, the far end of long context lines, fixtures and lockfiles. Changed lines always stay whole."""
from helpers import ForemanTestCase

import fmcli


def block(path, body):
    return f"diff --git a/{path} b/{path}\nindex 1111111..2222222 100644\n--- a/{path}\n+++ b/{path}\n{body}"


RULE = "@@ -1,3 +1,3 @@\n same\n-old rule\n+new rule\n"


class CompactDiff(ForemanTestCase):
    def test_copies_long_context_and_fixtures_shrink_and_changes_stay_whole(self):
        long_ctx, long_add = " " + "c" * 500, "+" + "a" * 500
        diff = (block("plugin/rules/foreman.md", RULE) + block("plugin/evals/x/prompt.md", RULE)
                + block("plugin/evals/y/prompt.md", RULE)
                + block("MASTER.md", f"@@ -1,2 +1,2 @@\n{long_ctx}\n-a\n{long_add}\n")
                + block("plugin/tests/fixtures/run.txt", "@@ -0,0 +1,3 @@\n+f1\n+f2\n+f3\n")
                + block("package-lock.json", "@@ -1 +1 @@\n-x\n+y\n"))
        out = fmcli._compact_diff(diff)
        self.assertEqual(out.count("+new rule"), 1, "one copy of a repeated change")
        self.assertIn("plugin/evals/x/prompt.md: the same change as plugin/rules/foreman.md", out)
        self.assertIn("plugin/evals/y/prompt.md: the same change as plugin/rules/foreman.md", out)
        self.assertNotIn("c" * 300, out, "long context is cut")
        self.assertIn(long_add, out, "a changed line stays whole")
        self.assertNotIn("+f2", out)
        self.assertIn("plugin/tests/fixtures/run.txt: a fixture or lockfile, +3 −0 lines, left out", out)
        self.assertIn("package-lock.json: a fixture or lockfile, +1 −1 lines, left out", out)
        self.assertLess(len(out), len(diff))

    def test_a_plain_diff_is_unchanged(self):
        diff = block("a.py", "@@ -1 +1 @@\n-x = 1\n+x = 2\n")
        self.assertEqual(fmcli._compact_diff(diff), diff)
