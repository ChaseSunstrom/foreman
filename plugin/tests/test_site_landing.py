"""T-2759, T-2851: the landing page in the illustrated forge (SAMPO.md, Design): the hero is a night forge, an anvil on
a rune stone, the headline struck line by line; the proof ledger reads Sampo's real totals; the Moons section is built
from the catalogue; and the Kalevala paragraph says once where the names come from. Every layer is progressive: the
HTML is the whole page (the drawings wait in <noscript> and are real DOM without script), CSS moves only where motion
is allowed, forge.js only adds the sky, the flames and the sparks."""
import glob
import html
import json
import os
import re
import shutil
import sys
import tempfile
import unittest

from helpers import PLUGIN, headless_chrome, read_text
from test_site_build import media_blocks
from test_site_hero import ROOT, build_copy, build_module, hero, ledger

sys.path.insert(0, os.path.join(PLUGIN, "lib"))
from sampo import design  # noqa: E402

MYTH = ("Kalevala", "Ilmarinen", "Väinämöinen", "Louhi", "Smith", "Rune", "Moons", "Underworld", "Ward")


def text(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", fragment))).strip()


MYTH_LINE = "Ilmarinen the smith forged it"  # the paragraph's own sentence; decision rows may name him (T-2829)


class Landing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        # T-2829: real decision rows name Ilmarinen too (the rename's own steers); the myth check must not count them
        row = {"date": "2026-11-03", "text": "Ilmarinen's forge leads the site", "later": None, "confidence": None,
               "kind": "reversible"}
        r = build_copy(cls.tmp, edit_stats=lambda s: s.setdefault("decisions", []).insert(0, row))
        if r.returncode:
            raise AssertionError(r.stdout + r.stderr)
        cls.out = os.path.join(cls.tmp, "out")
        cls.page = read_text(os.path.join(cls.out, "index.html"))
        cls.css = read_text(os.path.join(cls.out, "style.css")) + read_text(os.path.join(cls.out, "forge.css"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_nothing_loads_from_another_host(self):
        self.assertEqual(build_module().outside_hosts(self.out), [])

    def test_every_animation_has_a_still(self):
        allowed = "".join(media_blocks(self.css, "@media (prefers-reduced-motion: no-preference)"))
        for use in re.findall(r"(?m)^\s*[^{}]*\{[^}]*\banimation(?:-name|-timeline)?:\s*(?!none)[^;}]+", self.css):
            self.assertIn(use.strip(), allowed, "an animation outside @media (prefers-reduced-motion: no-preference)")
        for motion in ("@keyframes strike", "@keyframes rune", "@keyframes burn", "@keyframes arrive"):
            self.assertIn(motion, allowed, "the headline, the runes, the flames and the arrivals each move")
        top = hero(self.page)  # the reduced-motion still is 12's own drawing, real DOM in <noscript> for script to set
        self.assertRegex(top, r'<noscript class="laysrc">\s*<svg')
        js = read_text(os.path.join(ROOT, "site", "forge.js"))
        self.assertIn("classList.contains('anim')", js, "the sky, the fire and the sparks run only when .anim is set")
        for pause in ("visibilitychange", "--autoplay-limit", "IntersectionObserver"):
            self.assertIn(pause, js, "the forge rests offscreen, in a hidden tab and after the autoplay limit")

    def test_the_hero_is_whole_without_script(self):
        top = hero(self.page)
        h1 = re.search(r'<h1 class="struck" id="h1">(.*?)</h1>', top, re.S).group(1)
        self.assertEqual(text(h1), "Your coding agent, with a smith on the job.", "the struck lines are real words")
        self.assertEqual(len(re.findall(r'<span class="ln">', h1)), 3, "one struck line per span")
        self.assertIn('<div class="scene" id="scene" role="img"', top, "the forge scene is there with no script")
        for canvas in ("firecv", "fx"):  # empty, aria-hidden: the elements forge.js draws into
            self.assertRegex(top, rf'<canvas class="\w+" id="{canvas}" aria-hidden="true"></canvas>')
        self.assertNotIn("hero-scene", self.page)

    def test_the_myth_is_told_once_on_the_landing_page(self):
        pages = {os.path.relpath(p, self.out): read_text(p) for p in glob.glob(os.path.join(self.out, "**", "*.html"),
                                                                                 recursive=True)}
        told = {rel: page.count(MYTH_LINE) for rel, page in pages.items() if MYTH_LINE in page}
        self.assertEqual(told, {"index.html": 1}, "the myth paragraph once, on the landing page only")
        para = re.search(r"<p[^>]*>[^<]*Ilmarinen.*?</p>", self.page, re.S).group(0)
        for name in MYTH:
            self.assertIn(name, para)

    def test_the_ledger_reads_stats_json(self):
        stats = build_module()
        self.assertNotIn("--v:", read_text(os.path.join(ROOT, "site", "index.html")), "a reading typed by hand goes stale")
        with tempfile.TemporaryDirectory() as tmp:  # other totals, other figures
            r = build_copy(tmp, {"tasks_done": 7, "evidence": 0, "proofs": 100000, "commits": 12345678})
            self.assertEqual(r.returncode, 0, r.stderr)
            moved = ledger(read_text(os.path.join(tmp, "out", "index.html")))
        self.assertEqual([moved[label] for _, label in stats.STATIONS], ["7", "0", "100,000", "12,345,678"])

    def test_the_forge_scene_sits_beside_the_smith(self):
        lanes = self.page[self.page.index('<section id="lanes">'):self.page.index('<section id="more">')]
        self.assertIn("one Smith", lanes)
        self.assertRegex(lanes, r'<figure class="smithy" aria-hidden="true">\s*<svg')

    def moons(self, page):
        sec = page[page.index('<section class="sec" id="moons"'):]
        sec = sec[:sec.index("</section>")]
        return sec, re.findall(r'<li( class="kt")?><b>(M-\d+)</b><span>(.*?)<i>wild (\d) of 5 · (\w[\w ]*)</i>', sec)

    def test_moons_come_from_the_catalogue(self):
        """T-2851: the wild 4s and 5s of genesis.json's moonshots, the wildest first, counts from the data."""
        rows = [{"id": f"M-{i:02d}", "title": f"Moon number {i}", "wild": w, "stage": st}
                for i, (w, st) in enumerate([(2, "idea"), (5, "idea"), (4, "kill"), (5, "idea"), (3, "idea"), (4, "idea")], 1)]

        def edit(d):
            d["moonshots"]["rows"] = rows
            d["moonshots"]["total"] = len(rows)
        with tempfile.TemporaryDirectory() as tmp:
            r = build_copy(tmp, edit_genesis=edit)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            sec, got = self.moons(read_text(os.path.join(tmp, "out", "index.html")))
        self.assertEqual([g[1] for g in got], ["M-02", "M-04", "M-03", "M-06"], "wild 4 and 5 only, wildest first, then by id")
        self.assertEqual([bool(g[0]) for g in got], [False, False, True, False], "a kill test carries the kt class")
        self.assertIn("6 moonshots over the forge", sec)
        self.assertIn("It holds 6", sec)
        self.assertNotIn("{{", sec)

    def test_moons_follow_the_real_catalogue(self):
        with open(os.path.join(ROOT, "site", "genesis", "genesis.json"), encoding="utf-8") as f:
            rows = json.load(f)["moonshots"]["rows"]
        want = [r["id"] for r in sorted((r for r in rows if r["wild"] >= 4), key=lambda r: (-r["wild"], r["id"]))]
        sec, got = self.moons(self.page)
        self.assertEqual([g[1] for g in got], want)
        self.assertIn(f"{len(rows)} moonshots over the forge", sec)

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
          for (const s of [".hero h1", ".hero .lede", ".proof dd", ".proof dt", ".foot p"])
            for (const e of document.querySelectorAll(s)) pairs.push([s, getComputedStyle(e).color, solid(e)]);
          return {w: document.documentElement.scrollWidth, anim: document.documentElement.classList.contains("anim"), pairs};
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
                    self.assertFalse(got["anim"], f"the forge stays still under reduced motion ({where})")
                    self.assertTrue(got["pairs"])
                    for sel, fg, bg in got["pairs"]:
                        self.assertGreaterEqual(design.contrast(rgb(fg), rgb(bg)), 4.5, f"{sel}: {fg} on {bg} ({where})")


if __name__ == "__main__":
    unittest.main()
