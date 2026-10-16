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


class Annotations(unittest.TestCase):
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
