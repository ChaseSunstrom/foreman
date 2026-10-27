"""T-1555: fm marks: the icon set shares one 24 grid and one stroke, the empty states are built from it, the wordmark is
valid SVG with its name escaped, and the font shelf marks the vetted pairings installed here."""
import json
import os
import re
import unittest
import xml.etree.ElementTree as ET

from helpers import ForemanTestCase

import fmmarks

SVG = "{http://www.w3.org/2000/svg}"


class Marks(ForemanTestCase):
    def test_icons_share_one_grid_and_one_stroke(self):
        out = os.path.join(self.tmp, "icons")
        got = json.loads(self.fm("marks", "icons", "--out", out, "--json").stdout)
        self.assertEqual(len(got["files"]), len(fmmarks.ICONS) + 1)
        for name in fmmarks.ICONS:
            root = ET.parse(os.path.join(out, f"{name}.svg")).getroot()
            self.assertEqual((root.get("viewBox"), root.get("stroke-width"), root.get("fill"), root.get("stroke"),
                              root.get("stroke-linecap")), ("0 0 24 24", "2", "none", "currentColor", "round"), name)
            self.assertEqual([el.tag for el in root], [SVG + "path"], name)
            nums = [float(x) for x in re.findall(r"-?\d*\.?\d+", root[0].get("d"))]
            self.assertTrue(all(-21 <= n <= 23 for n in nums), (name, nums))
        sprite = ET.parse(os.path.join(out, "icons.svg")).getroot()
        self.assertEqual([s.get("id") for s in sprite], list(fmmarks.ICONS))
        self.fm("marks", "icons", "--out", out, "--stroke", "1.5")
        self.assertEqual(ET.parse(os.path.join(out, "home.svg")).getroot().get("stroke-width"), "1.5")
        self.assertNotEqual(self.fm("marks", "icons", "--stroke", "9", check=False).returncode, 0)

    def test_empty_states_are_drawn_from_the_icons(self):
        out = os.path.join(self.tmp, "empty")
        self.fm("marks", "empty", "--out", out)
        for name, (icon, title, line) in fmmarks.EMPTY.items():
            self.assertLessEqual(len(line), fmmarks.LINE, name)  # it fits the 240 width
            root = ET.parse(os.path.join(out, f"{name}.svg")).getroot()
            g = root.find(SVG + "g")
            self.assertEqual(g[0].get("d"), fmmarks.ICONS[icon])
            self.assertAlmostEqual(float(g.get("stroke-width")) * 3, 2.0, places=3)  # the icons' stroke, scaled back
            self.assertIn(title, [t.text for t in root.iter(SVG + "text")])

    def test_the_wordmark_is_valid_svg_and_the_same_for_the_same_name(self):
        text = self.fm("marks", "wordmark", "R&D <Lab>").stdout
        root = ET.fromstring(text)
        self.assertEqual(root.get("aria-label"), "R&D <Lab>")
        self.assertEqual([t.text for t in root.iter(SVG + "text")], ["R", "R&D <Lab>"])
        self.assertEqual(fmmarks.wordmark("R&D <Lab>"), fmmarks.wordmark("R&D  <Lab>"))
        self.assertNotEqual(fmmarks.wordmark("Atlas"), fmmarks.wordmark("Beacon"))

    def test_the_font_shelf_marks_what_is_installed(self):
        rows = fmmarks.shelf({"Inter", "Noto Sans", "Noto Serif"})
        self.assertEqual(rows[0]["have"], [True, False])
        self.assertIn({"heading": "Noto Sans", "body": "Noto Serif", "have": [True, True]},
                      [{k: r[k] for k in ("heading", "body", "have")} for r in rows])
        self.assertEqual(self.fm("marks", "fonts", check=False).returncode, 0)
        try:
            import fontTools  # noqa: F401
        except ImportError:
            p = self.fm("marks", "fonts", "--subset", "x.ttf", "--text", "abc", "--out", "y.woff2", check=False)
            self.assertNotEqual(p.returncode, 0)
            self.assertIn("fontTools", p.stderr + p.stdout)


if __name__ == "__main__":
    unittest.main()
