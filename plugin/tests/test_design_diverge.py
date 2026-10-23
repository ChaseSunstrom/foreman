"""T-1536: fm design diverge N writes N variant briefs in looks far apart (the best-ranked, then each the look farthest
from its nearest pick); fm design diverge pick LOOK keeps the winner in the taste ledger."""
import json
import os
import unittest

from helpers import ForemanTestCase, read_text

import fmtaste


class Diverge(ForemanTestCase):
    def test_three_variants_in_looks_far_apart_then_a_pick(self):
        out = os.path.join(self.tmp, "variants")
        got = json.loads(self.fm("design", "diverge", "3", "the", "pricing", "page", "--out", out, "--json").stdout)
        names = [v["look"] for v in got["variants"]]
        self.assertEqual(len(set(names)), 3)
        known = fmtaste.looks()
        self.assertEqual(names[1], fmtaste.opposite(names[0], known)[0][1], "the second is the farthest from the first")
        files = sorted(os.listdir(out))
        self.assertEqual(files, [f"variant-{k}-{n}.md" for k, n in enumerate(names, 1)])
        brief = read_text(os.path.join(out, files[0]))
        self.assertIn(f"Build the pricing page in the look {known[names[0]]['title']}", brief)
        self.assertIn(f"fm design diverge pick {names[0]}", brief)
        self.fm("design", "diverge", "pick", names[2])
        top = json.loads(self.fm("looks", "--json").stdout)["looks"][0]
        self.assertEqual((top["look"], top.get("kept")), (names[2], 1))
        for bad in (["9"], ["pick"]):
            self.assertNotEqual(self.fm("design", "diverge", *bad, check=False).returncode, 0, bad)

    def test_no_out_prints_the_briefs(self):
        text = self.fm("design", "diverge", "2").stdout
        self.assertEqual(text.count("# Variant "), 2)
        self.assertIn("Build the screen in the look", text)


if __name__ == "__main__":
    unittest.main()
