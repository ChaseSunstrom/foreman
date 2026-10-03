"""T-0094: fm help lists every command once, in tiers (the everyday ones first); fm alone prints it."""
import argparse
import os
import sys
import unittest

from helpers import ForemanTestCase

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))


class Help(ForemanTestCase):
    def test_every_command_once_in_tiers_everyday_first(self):
        import fmcli
        sub = next(a for a in fmcli.build_parser()._actions if isinstance(a, argparse._SubParsersAction))
        out = self.fm("help").stdout
        lines = [ln.split()[0] for ln in out.splitlines() if ln.startswith("  ")]
        self.assertEqual(sorted(lines), sorted(sub.choices), "every command, each once (a new one needs a tier)")
        self.assertTrue(out.startswith("Every task"), out[:80])
        self.assertLess(out.index("  next "), out.index("  sentinel "))
        self.assertEqual(self.fm().stdout, out, "fm alone prints it")


if __name__ == "__main__":
    unittest.main()
