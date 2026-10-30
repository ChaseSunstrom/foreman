#!/usr/bin/env python3
# T-2222: a close that changed a path the repo's .fmproved lists needs a red→green proof, whatever the task's type
import os
import tempfile
import unittest
from unittest import mock
from types import SimpleNamespace

from helpers import ForemanTestCase  # noqa: F401  (puts plugin/lib on sys.path)
import fmcli
import fmcore as c

RED = "python3 plugin/tests/run.py test_exam"


def brief(type_="FEATURE", red=False, regression=""):
    b = c.Brief.new("T-0001", "a score change", type_, "S", raw="x")
    if red:  # the test failed first; the close's run (then) is its green
        b.add_evidence(RED, "✗ exit 1 · FAILED (1 classes)", ac=1, ran=True)
    if regression:
        b.set_section("Regression test", regression)
    return b


def gaps(changed, b, listed="# scores\nplugin/lib/fmexam.py\nsite/*.py\n", then=()):
    with tempfile.TemporaryDirectory() as root:
        if listed is not None:
            with open(os.path.join(root, ".fmproved"), "w") as f:
                f.write(listed)
        with mock.patch.object(fmcli.c, "git_root", return_value=root), \
                mock.patch.object(fmcli.c, "task_base", return_value="abc"), \
                mock.patch("fmmap.changed", return_value=changed):
            return fmcli._proved_gaps(SimpleNamespace(root=root), b, then=list(then))


class ProvedPaths(unittest.TestCase):
    def test_a_listed_path_without_a_proof_is_refused(self):
        (g,) = gaps(["plugin/lib/fmexam.py"], brief())
        self.assertIn("plugin/lib/fmexam.py is listed in .fmproved", g)
        self.assertIn("red→green", g)

    def test_a_glob_matches_and_names_what_it_matched(self):
        self.assertIn("site/pages.py", gaps(["site/pages.py", "README.md"], brief())[0])

    def test_a_red_then_green_or_a_regression_note_satisfies_it(self):
        self.assertEqual(gaps(["plugin/lib/fmexam.py"], brief(red=True), then=[RED]), [])
        self.assertEqual(gaps(["plugin/lib/fmexam.py"], brief(regression="none: docs-only wording")), [])

    def test_unlisted_paths_no_file_and_fix_tasks_are_left_alone(self):
        self.assertEqual(gaps(["plugin/lib/fmdoctor.py"], brief()), [])
        self.assertEqual(gaps(["plugin/lib/fmexam.py"], brief(), listed=None), [])
        self.assertEqual(gaps(["plugin/lib/fmexam.py"], brief("FIX")), [])  # FIX has its own red→green gate


if __name__ == "__main__":
    unittest.main()
