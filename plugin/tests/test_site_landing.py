"""T-2759: the landing page in the forge world (SAMPO.md, Design): the Sampo mill turns in the hero over a forge glow
while runes write themselves into the headline, the proof ledger reads as gears and dials of Sampo's real totals, a
forge scene strikes beside the Smith section, and the Kalevala paragraph says once where the names come from. Every
layer is progressive: the HTML is the whole page, CSS moves only where motion is allowed, site.js only adds the glow."""
import glob
import html
import math
import os
import re
import shutil
import sys
import tempfile
import unittest

from helpers import PLUGIN, headless_chrome, read_text
from test_site_build import media_blocks
from test_site_hero import KEYS, ROOT, build_copy, build_module, hero

sys.path.insert(0, os.path.join(PLUGIN, "lib"))
from sampo import design  # noqa: E402

MYTH = ("Kalevala", "Ilmarinen", "Väinämöinen", "Louhi", "Smith", "Rune", "Moons", "Underworld", "Ward")


def reading(n):
    """A dial's reading, 0 to 1: decades evenly spaced from 1 to 100,000, so a count of 7 and one of 7,000 both move."""
    return round(min(math.log10(max(n, 1)) / 5, 1), 3)


def dials(page):
    """The hero's dials as {label: (figure, reading)}."""
    return {html.unescape(dt): (html.unescape(dd), float(v)) for v, dt, dd in re.findall(
        r'<div style="--v:([\d.]+)"><dt>(.*?)</dt><dd>(.*?)</dd></div>', hero(page))}


def text(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", fragment))).strip()


class Landing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        r = build_copy(cls.tmp)
        if r.returncode:
            raise AssertionError(r.stdout + r.stderr)
        cls.out = os.path.join(cls.tmp, "out")
        cls.page = read_text(os.path.join(cls.out, "index.html"))
        cls.css = read_text(os.path.join(cls.out, "style.css"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_nothing_loads_from_another_host(self):
        self.assertEqual(build_module().outside_hosts(self.out), [])

    def test_every_animation_has_a_still(self):
        allowed = "".join(media_blocks(self.css, "@media (prefers-reduced-motion: no-preference)"))
        for use in re.findall(r"(?m)^\s*[^{}]*\{[^}]*\banimation(?:-name|-timeline)?:\s*(?!none)[^;}]+", self.css):
            self.assertIn(use.strip(), allowed, "an animation outside @media (prefers-reduced-motion: no-preference)")
        for motion in ("@keyframes carve", "@keyframes rune", "@keyframes sweep", "@keyframes strike"):
            self.assertIn(motion, allowed, "the headline's runes, the dials and the forge scene each move")
        mill = re.search(r'<picture class="mill">(.*?)</picture>', hero(self.page), re.S)
        self.assertTrue(mill, "the mill turns in the hero")
        self.assertRegex(mill.group(1), r'<source media="\(prefers-reduced-motion: reduce\)" srcset="assets/mark\.svg[?"]',
                         "the turning mill's still is the mark itself")
        self.assertRegex(mill.group(1), r'<img src="assets/mark-animated\.svg[?"][^>]* alt=""')
        for name in ("mark.svg", "mark-animated.svg"):
            self.assertIn("<svg", read_text(os.path.join(self.out, "assets", name)), name)
        js = read_text(os.path.join(ROOT, "site", "site.js"))  # the glow waits past the still return
        still = js.index("return;", js.index("prefers-reduced-motion: reduce"))
        self.assertGreater(js.index('getContext("webgl")'), still)
        for pause in ("visibilitychange", "--autoplay-limit", "IntersectionObserver"):
            self.assertIn(pause, js[still:], "the glow rests offscreen, in a hidden tab and after the autoplay limit")

    def test_the_hero_is_whole_without_script(self):
        top = hero(self.page)
        h1 = re.search(r"<h1>(.*?)</h1>", top, re.S).group(1)
        self.assertEqual(text(h1), "Your coding agent, with a smith on the job.", "the runes resolve into real words")
        self.assertEqual(len(re.findall(r'class="w"', h1)), 9, "one rune per word")
        self.assertIn('<div class="hearth"', top, "the forge's still glow is CSS, there with no script")
        self.assertNotIn("<canvas", top, "site.js adds the shader's canvas; the HTML never needs it")
        self.assertNotIn("hero-scene", self.page)

    def test_the_myth_is_told_once_on_the_landing_page(self):
        pages = {os.path.relpath(p, self.out): read_text(p) for p in glob.glob(os.path.join(self.out, "**", "*.html"),
                                                                                 recursive=True)}
        told = {rel: page.count("Ilmarinen") for rel, page in pages.items() if "Ilmarinen" in page}
        self.assertEqual(told, {"index.html": 1}, "the myth paragraph once, on the landing page only")
        para = re.search(r"<p[^>]*>[^<]*Ilmarinen.*?</p>", self.page, re.S).group(0)
        for name in MYTH:
            self.assertIn(name, para)

    def test_the_dials_read_stats_json(self):
        stats = build_module()
        with open(os.path.join(ROOT, "site", "data", "stats.json"), encoding="utf-8") as f:
            import json
            totals = json.load(f)["totals"]
        got = dials(self.page)
        self.assertEqual(len(got), 4, got)
        for key, label in stats.STATIONS:
            self.assertEqual(got[label], (f"{totals[key]:,}", reading(totals[key])), label)
        src = read_text(os.path.join(ROOT, "site", "index.html"))
        self.assertNotIn("--v:", src, "a reading typed by hand goes stale; build.py fills it from the data")
        with tempfile.TemporaryDirectory() as tmp:  # other totals, other readings: 0 and past the scale's end too
            r = build_copy(tmp, {"tasks_done": 7, "evidence": 0, "proofs": 100000, "commits": 12345678})
            self.assertEqual(r.returncode, 0, r.stderr)
            moved = dials(read_text(os.path.join(tmp, "out", "index.html")))
        self.assertEqual([moved[label][1] for _, label in stats.STATIONS], [0.169, 0.0, 1.0, 1.0])
        self.assertEqual(moved["commits"][0], "12,345,678")
        self.assertEqual(KEYS, tuple(k for k, _ in stats.STATIONS))

    def test_the_forge_scene_sits_beside_the_smith(self):
        lanes = self.page[self.page.index('<section id="lanes">'):self.page.index('<section id="more">')]
        self.assertIn("one Smith", lanes)
        self.assertRegex(lanes, r'<figure class="smithy" aria-hidden="true">\s*<svg')

    def test_design_lint_passes(self):
        found = design.lint([os.path.join(self.out, "index.html"), os.path.join(self.out, "style.css")])
        self.assertEqual(found, [], found)

    def test_phone_width_and_contrast_in_both_themes(self):
        browser = headless_chrome()
        if not browser:
            self.skipTest("no headless Chromium (FOREMAN_CHROME, chrome-headless-shell or Playwright's download)")
        from sampo import shot
        probe = """(() => {
          const solid = el => { for (; el; el = el.parentElement) { const c = getComputedStyle(el).backgroundColor;
            if (!/^rgba\\(.*,\\s*0(\\.0+)?\\)$|transparent/.test(c) && !/^rgba/.test(c)) return c; }
            return getComputedStyle(document.body).backgroundColor; };
          const pairs = [];
          for (const s of [".hero h1", ".hero .lede", ".proof dd", ".proof dt", ".proof p", "#names p"])
            for (const e of document.querySelectorAll(s)) pairs.push([s, getComputedStyle(e).color, solid(e)]);
          return {w: document.documentElement.scrollWidth, glow: !!document.querySelector(".hearth canvas"), pairs};
        })()"""
        rgb = lambda c: tuple(int(x) / 255 for x in re.findall(r"[\d.]+", c)[:3])
        for scheme in ("light", "dark"):
            for reduced in (True, False):
                b = shot.Browser(browser, (320, 640), reduced=reduced)
                try:
                    b.call("Emulation.setEmulatedMedia", b.sid, features=[
                        {"name": "prefers-color-scheme", "value": scheme},
                        {"name": "prefers-reduced-motion", "value": "reduce" if reduced else "no-preference"}])
                    shot.load(b,"file://" + os.path.join(self.out, "index.html"))
                    got = b.call("Runtime.evaluate", b.sid, expression=probe, returnByValue=True)["result"]["value"]
                finally:
                    b.close()
                where = f"{scheme}, reduced motion {reduced}"
                self.assertLessEqual(got["w"], 320, f"the page scrolls sideways at 320 px ({where})")
                if reduced:
                    self.assertFalse(got["glow"], f"no shader under reduced motion ({where})")
                    self.assertTrue(got["pairs"])
                    for sel, fg, bg in got["pairs"]:
                        self.assertGreaterEqual(design.contrast(rgb(fg), rgb(bg)), 4.5, f"{sel}: {fg} on {bg} ({where})")


if __name__ == "__main__":
    unittest.main()
