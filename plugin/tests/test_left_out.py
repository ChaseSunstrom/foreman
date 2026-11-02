"""T-2673: a list fmcli cuts at N says how many it left out. c.more() is the helper; the scan fails on any
join(...[:N]) in fmcli with no 'more', 'left out' or 'len(' on its line, the one before or the two after,
unless the line says `# not a list: <why>`."""
import os
import re
import unittest

from helpers import ForemanTestCase

import fmcore as c

LIB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib", "fmcli.py")


def silent_sites():
    lines = open(LIB, encoding="utf-8").read().split("\n")
    out = []
    for i, l in enumerate(lines):
        if not re.search(r"join\(.*\[:[0-9]+\]\)", l) or "# not a list:" in l:
            continue
        near = " ".join(lines[max(0, i - 1):i + 3])
        if not any(k in near for k in ("more", "left out", "len(")):
            out.append("%d: %s" % (i + 1, l.strip()[:120]))
    return out


class LeftOut(ForemanTestCase):
    def test_more_cut_and_whole(self):
        self.assertEqual(c.more([1, 2, 3], 2, "--all"), ([1, 2], "1 left out (--all)"))
        self.assertEqual(c.more([1, 2, 3], 1), ([1], "2 left out"))
        self.assertEqual(c.more([1, 2], 2, "--all"), ([1, 2], ""))
        self.assertEqual(c.more([], 0), ([], ""))

    def test_no_silent_cut_in_fmcli(self):
        self.assertEqual(silent_sites(), [])


if __name__ == "__main__":
    unittest.main()
