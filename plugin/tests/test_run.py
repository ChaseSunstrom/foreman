"""T-0808: run.py takes test module names positionally, so fm check affected can hand it {names}."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import run  # noqa: E402


class Args(unittest.TestCase):
    def test_names_are_k_patterns(self):
        self.assertEqual(sorted(run.parse(["test_lanes", "-k", "Stop", "test_cli"]).k), ["Stop", "test_cli", "test_lanes"])
        self.assertEqual(run.parse([]).k, [])
