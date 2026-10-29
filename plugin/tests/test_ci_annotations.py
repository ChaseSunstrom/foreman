"""T-1248: on GitHub Actions, run.py turns each failing test into its own ::error annotation (a run's log needs a
login; its annotations are public). One annotation per class showed only its last failure: a class with two failures
hid one."""
import unittest

import run

ERR = """
======================================================================
FAIL: test_a (test_x.C.test_a)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/r/test_x.py", line 5, in test_a
    self.assertLess(t, 0.08)
AssertionError: 0.109 not less than 0.08

======================================================================
ERROR: test_b (test_x.C.test_b)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/r/test_x.py", line 9, in test_b
    open("/proc/1/stat")
FileNotFoundError: [Errno 2] No such file or directory: '/proc/1/stat'

----------------------------------------------------------------------
Ran 2 tests in 0.1s

FAILED (failures=1, errors=1)
"""


class SummaryNotes(unittest.TestCase):
    """T-1809: a job that hits its cap prints nothing, so the run's time and slowest classes go out as public notices,
    with a warning before the suite outgrows its deadline."""

    def test_the_slowest_classes_go_out_as_a_notice_and_a_near_deadline_run_warns(self):
        results = [(f"test_m.C{i}", 0, "", 2, float(i)) for i in range(8)]
        notes = run.summary_notes(results, 800, 1000)
        self.assertTrue(notes[0].startswith("::notice title=run.py::Ran 16 tests in 800s"))
        self.assertIn("C7 7s, C6 6s, C5 5s, C4 4s, C3 3s", notes[0])
        self.assertTrue(notes[1].startswith("::warning title=run.py::"))
        self.assertIn("80% of its 1000s deadline", notes[1])
        self.assertEqual(len(run.summary_notes(results, 500, 1000)), 1)
        self.assertEqual(len(run.summary_notes(results, 900, None)), 1)

    def test_classes_the_deadline_left_unstarted_are_one_error(self):
        results = [("test_m.A", 0, "", 2, 5.0), ("test_m.B", 1, run.NOT_STARTED, 0, 0.0),
                   ("test_m.C", 1, run.NOT_STARTED, 0, 0.0)]
        notes = run.summary_notes(results, 990, 1000)
        self.assertIn("::error title=run.py::2 classes never started: the run reached its 1000s deadline", notes)


    def test_every_failed_class_is_named_in_one_error(self):  # T-1911: macOS shard 2 failed with no ::error at all
        results = [("test_m.A", 0, "", 2, 5.0), ("test_m.B", 1, "x", 1, 1.0), ("test_m.C", -9, "", 0, 9.0),
                   ("test_m.D", 1, run.NOT_STARTED, 0, 0.0)]
        notes = run.summary_notes(results, 100, 1000)
        self.assertIn("::error title=run.py::2 classes failed: test_m.B (exit 1), test_m.C (exit -9)", notes)
        self.assertFalse(any("classes failed" in n for n in run.summary_notes(results[:1], 100, 1000)))


class Annotations(unittest.TestCase):
    def test_a_silent_class_still_says_something_and_a_long_line_is_cut(self):  # T-1911
        self.assertEqual(run.annotations("test_z", ""), ["::error title=test_z::no output"])
        self.assertLess(len(run.annotations("test_z", "E" * 50000)[0]), 600)

    def test_each_failing_test_gets_its_own_annotation(self):
        lines = run.annotations("test_x.C", ERR)
        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[0].startswith("::error title=test_x.C.test_a::"), lines[0])
        self.assertIn("self.assertLess(t, 0.08)", lines[0])
        self.assertIn("0.109 not less than 0.08", lines[0])
        self.assertIn("FileNotFoundError", lines[1])

    def test_output_with_no_test_blocks_keeps_its_tail(self):
        lines = run.annotations("test_y", "ImportError: no module named z\n")
        self.assertEqual(lines, ["::error title=test_y::ImportError: no module named z"])


if __name__ == "__main__":
    unittest.main()
