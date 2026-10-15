"""T-0870: fm demo shows Foreman work on a seeded bug in a throwaway repo: no model, no trace left behind."""
import os
import time
import unittest
from unittest import mock

from helpers import ForemanTestCase, read_text

import fmdemo


class Demo(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.tmpdir = os.path.join(self.tmp, "tmpdir")  # where the demo's temp folder must come and go
        os.makedirs(self.tmpdir)

    def test_runs_end_to_end_in_plain_words_and_leaves_nothing(self):
        before = sorted(os.listdir(self.home))
        t0 = time.time()
        p = self.fm("demo", env={"TMPDIR": self.tmpdir})
        self.assertLess(time.time() - t0, 20)
        out = p.stdout
        for stage in ("no active task", "rm -rf ~", "blocked rm-outside", "T-0001", "red", "green", "not finished",
                      "closed", "nothing was left behind"):
            self.assertIn(stage, out)
        self.assertLess(out.index("red"), out.index("green"))  # the test fails before the fix, passes after
        self.assertEqual(os.listdir(self.tmpdir), [])
        self.assertEqual(sorted(os.listdir(self.home)), before)  # the user's Foreman state is never touched
        self.assertNotIn("claude was called", out + p.stderr)

    def test_ctrl_c_still_cleans_up(self):
        with mock.patch.object(fmdemo.tempfile, "tempdir", self.tmpdir), \
                mock.patch.object(fmdemo, "_hook", side_effect=KeyboardInterrupt):
            self.assertEqual(fmdemo.cmd_demo(None), 130)
        self.assertEqual(os.listdir(self.tmpdir), [])

    def test_listed_where_a_newcomer_starts(self):
        self.assertIn("fm demo", self.fm("--help").stdout)
        self.assertIn("demo", self.fm("help", "--all").stdout)
        self.assertIn("fm demo", read_text(os.path.join(os.path.dirname(fmdemo.__file__), "..", "..", "README.md")))


if __name__ == "__main__":
    unittest.main()
