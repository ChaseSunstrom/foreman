"""T-1615: fm desk draws the project's glance as a desk card for an e-paper panel or an old phone: a valid SVG (an
HTML copy that reloads itself, a PNG with rsvg-convert), black on white, and never a listener on a port."""
import os
import shutil
import xml.etree.ElementTree as ET

from helpers import PLUGIN, ForemanTestCase, read_text

import fmintegrations as I

SVG = "{http://www.w3.org/2000/svg}"


def words(svg):
    return [t.text for t in ET.fromstring(svg).iter(SVG + "text")]


class Card(ForemanTestCase):
    def test_the_card_draws_the_task_its_step_and_the_counts(self):
        g = {"project": "shop-1a2b3c", "task": "T-0007", "title": "Make <checkout> & totals agree", "step": "2/4",
             "queue": 3, "inbox": 5, "blocked": 1, "lanes": 0, "class": "active"}
        svg = I.desk_svg(g, when="09:30")
        root = ET.fromstring(svg)
        self.assertEqual((root.get("width"), root.get("height")), ("800", "480"))
        got = words(svg)
        for want in ("shop-1a2b3c", "working", "T-0007", "Make <checkout> & totals agree", "step 2/4", "3", "5",
                     "queued", "at 09:30"):
            self.assertIn(want, got)
        fills = {el.get("fill") for el in root.iter() if el.get("fill")}
        self.assertLessEqual(fills, {"#000", "#fff"}, "black and white only: an e-paper panel draws it as is")
        bar = [r for r in root.iter(SVG + "rect") if r.get("fill") is None]
        self.assertAlmostEqual(float(bar[0].get("width")), (800 - 64) / 2, places=0)
        idle = words(I.desk_svg({"project": "shop", "class": "idle", "queue": 0}, size=(400, 240)))
        self.assertIn("No active task", idle)

    def test_the_verb_writes_svg_html_and_png_and_opens_no_port(self):
        self.fm("init")
        out = os.path.join(self.tmp, "card.svg")
        self.fm("desk", "--out", out)
        self.assertTrue(ET.fromstring(read_text(out)).tag.endswith("svg"))
        page = os.path.join(self.tmp, "card.html")
        self.fm("desk", "--out", page, "--size", "400x300")
        self.assertIn('http-equiv="refresh"', read_text(page))
        self.assertIn('width="400" height="300"', read_text(page))
        png = os.path.join(self.tmp, "card.png")
        p = self.fm("desk", "--out", png, check=False)
        if shutil.which("rsvg-convert"):
            with open(png, "rb") as f:
                self.assertEqual(f.read(8), b"\x89PNG\r\n\x1a\n")
        else:
            self.assertIn("rsvg-convert", p.stderr)
        for bad in (["--size", "10x10"], ["--size", "wide"], ["--every", "1", "--out", out]):
            self.assertNotEqual(self.fm("desk", *bad, check=False).returncode, 0, bad)
        source = read_text(os.path.join(PLUGIN, "lib", "fmintegrations.py"))
        self.assertNotIn("socket", source)
        self.assertNotIn("http.server", source)
