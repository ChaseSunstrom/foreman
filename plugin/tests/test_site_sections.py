"""T-2767: the Louhi, Moons and Underworld pages, drawn from the tower's own records: Louhi's scorecard from exam.jsonl,
the Moons catalogue from moonshot.md with each moon's stage, the Underworld from not-yet.md. site/stats.py reads them
into stats.json; site/pages.py draws each page's dials, scroll scene and lists from it, so other records give other
numbers and nothing is typed into a page. Each page meets the landing page's bar (SAMPO.md, Design)."""
import html
import inspect
import json
import math
import os
import re
import shutil
import tempfile
import unittest

from helpers import headless_chrome, read_text
from test_site_build import media_blocks, site
from test_site_hero import ROOT, build_copy, build_module
from test_site_sampo import names_foreman

from sampo import design, shot

SLUGS = {"louhi": ("aurora", "trial"), "moons": ("stars", "moon"), "underworld": ("river", "rune")}
DIAL = r'<div style="--v:([\d.]+)"><dt>(.*?)</dt><dd>(.*?)</dd></div>'

EXAM = "\n".join([
    '{"run": "s0-001", "gen": 1, "agent": "foreman", "keyed": 4, "found": 3, "false_alarms": 1, "fixable": 2, '
    '"fixed": 1, "scenarios": 5, "brier_n": 4, "brier_sum": 1.0}',
    '{"run": "s0-001", "gen": 1, "agent": "oracle", "keyed": 4, "found": 4, "false_alarms": 0, "scenarios": 5}',
    "not json",
    '{"run": "s1-002", "gen": 2, "agent": "foreman", "keyed": 6, "found": true, "false_alarms": "2", "scenarios": 7, '
    '"brier_n": 2, "brier_sum": 1.5}',
    '{"run": "s1-002", "gen": true, "agent": "plain", "keyed": 6, "found": 2, "scenarios": 7}',
    '{"run": "x", "keyed": 1}',
    '{"agent": "plain", "run": 7, "keyed": 1, "found": 1, "scenarios": 1}',
    "[1, 2]", ""])
MORE_EXAM = EXAM + '{"run": "s2-003", "gen": 3, "agent": "sampo", "keyed": 9, "found": 5, "scenarios": 11}\n'

MOONS = """# Moonshots

Toward 100 moonshots.

### M-01 · Quote, commit to and insure a product
- Tier: massive
- Needs: M-02, T-0001
- Stage: kill — the kill test ran

### M-02 · Foreman keeps code as a cache of intent
- Tier: high
- Needs: none
- Stage: idea

### M-03 · Forecast every close
- Tier: extreme
- Needs: M-01
- Stage: not-yet — its kill test failed
"""
MORE_MOONS = MOONS + "\n### M-04 · Ship it whole\n- Tier: low\n- Stage: full\n"
RATED = {"M-02": {"tier": "low"}, "M-03": {"tier": "galactic"}}

NOT_YET = """# Not yet

What waits for a better day: each entry has a blocker, what was tried, and what unblocks it.

## Idea one
- blocker: unevaluated: no exam arm has run it on Foreman's own history (`fm exam` has no arm for it)
- unblocks-with: an arm
- added: gen-2, a note

## Idea two
- blocker: its kill test found no stale proof in research/genesis/x.md; more text. Another sentence
- tried: first way (a; b); second way;
- retried: gen-3, re-checked
- retried: gen-4, again
- added: gen-3, from a brainstorm

## Long one
- blocker: """ + "word " * 100 + """
- added: gen-3

## Removed
- Gone idea: built in T-0001
"""
MORE_NOT_YET = NOT_YET.replace("## Removed", "## Idea four\n- blocker: needs a second machine\n- tried: x; y; z\n\n"
                                             "## Removed")

LOUHI = {"trials": 5,
         "runs": [{"run": "s0-001", "trials": 2, "scenarios": 10, "keyed": 8, "found": 7},
                  {"run": "s1-002", "trials": 2, "scenarios": 14, "keyed": 12, "found": 2}],
         "gens": [{"gen": 1, "trials": 1, "keyed": 4, "found": 3}, {"gen": 2, "trials": 1, "keyed": 6, "found": 0}],
         "agents": [{"agent": "foreman", "trials": 2, "scenarios": 12, "keyed": 10, "found": 3, "false_alarms": 1,
                     "fixable": 2, "fixed": 1, "brier": 0.417},
                    {"agent": "plain", "trials": 2, "scenarios": 8, "keyed": 7, "found": 3, "false_alarms": 0,
                     "fixable": 0, "fixed": 0, "brier": None},
                    {"agent": "oracle", "trials": 1, "scenarios": 5, "keyed": 4, "found": 4, "false_alarms": 0,
                     "fixable": 0, "fixed": 0, "brier": None}]}
MOON_ROWS = [{"id": "M-01", "title": "Quote, commit to and insure a product", "tier": "massive", "stage": "kill",
              "needs": ["M-02"]},
             {"id": "M-02", "title": "Foreman keeps code as a cache of intent", "tier": "low", "stage": "idea",
              "needs": []},
             {"id": "M-03", "title": "Forecast every close", "tier": "extreme", "stage": "not-yet", "needs": ["M-01"]}]

DIALS = {"louhi": {"trials": "5", "exam runs": "2", "scenarios graded": "25", "faults Sampo found": "3"},
         "moons": {"moons": "3", "ideas": "1", "kill-tested": "2", "built": "0"},
         "underworld": {"waiting ideas": "3", "approaches tried": "2", "re-checks": "2", "unevaluated": "1"}}
MORE_DIALS = {"louhi": {"trials": "6", "exam runs": "3", "scenarios graded": "36", "faults Sampo found": "8"},
              "moons": {"moons": "4", "ideas": "1", "kill-tested": "3", "built": "1"},
              "underworld": {"waiting ideas": "4", "approaches tried": "5", "re-checks": "2", "unevaluated": "1"}}


def reading(n):
    return round(min(math.log10(max(n, 1)) / 5, 1), 3)


def tower(root, exam=EXAM, moons=MOONS, not_yet=NOT_YET, rated=RATED):
    """A project state folder holding the tower's three records (and the moon ratings store beside them)."""
    g = os.path.join(root, "research", "genesis")
    os.makedirs(g, exist_ok=True)
    for name, text in (("exam.jsonl", exam), ("moonshot.md", moons), ("not-yet.md", not_yet)):
        if text is not None:
            with open(os.path.join(g, name), "w", encoding="utf-8") as f:
                f.write(text)
    if rated is not None:
        with open(os.path.join(root, "genesis-moonshot-rate.json"), "w", encoding="utf-8") as f:
            json.dump(rated, f)
    return root


def collect(stats, state):
    return {"louhi": stats.louhi(state), "moons": stats.moons(state), "underworld": stats.underworld(state)}


def dials(page):
    """A page's dials as {label: figure}, each needle checked against its figure."""
    box = re.search(r'<div class="proof">.*?</dl></div>', page, re.S)
    got = {}
    for v, dt, dd in re.findall(DIAL, box.group(0) if box else ""):
        fig = html.unescape(dd)
        if re.fullmatch(r"[\d,]+", fig):
            assert float(v) == reading(int(fig.replace(",", ""))), (dt, v, fig)
        got[html.unescape(dt)] = fig
    return got


def scene(page, slug):
    sky, mark = SLUGS[slug]
    m = re.search(r'<figure class="sky" data-sky="(\w+)" aria-hidden="true">\s*<svg(.*?)</svg>\s*</figure>', page, re.S)
    assert m, f"{slug}: no scene"
    assert m.group(1) == sky, (slug, m.group(1))
    return len(re.findall(rf'class="mk {mark}\b', m.group(2)))


class Collect(unittest.TestCase):
    """stats.py reads the tower's records: counts, stages and short reasons, never a path."""

    def setUp(self):
        self.stats = site("stats")
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def test_louhi_scores_every_trial_and_skips_what_isnt_one(self):
        got = self.stats.louhi(tower(self.tmp))
        self.assertEqual(got, LOUHI)

    def test_moons_carry_the_reviewers_tier_and_their_stage(self):
        self.assertEqual(self.stats.moons(tower(self.tmp)), MOON_ROWS)

    def test_the_underworld_keeps_each_waiting_idea_short_and_pathless(self):
        got = self.stats.underworld(tower(self.tmp))
        self.assertEqual([x["idea"] for x in got], ["Idea one", "Idea two", "Long one"], "the Removed list is gone")
        one, two, long_ = got
        self.assertEqual(one, {"idea": "Idea one", "blocker": "unevaluated: no exam arm has run it on Foreman's own "
                                                              "history", "tries": 0, "rechecks": 0, "added": "gen-2"})
        self.assertEqual((two["tries"], two["rechecks"], two["added"]), (2, 2, "gen-3"))
        self.assertTrue(two["blocker"].startswith("its kill test found no stale proof in"), two)
        for x in got:
            self.assertNotIn("/", x["blocker"], "a path stays in the record")
            self.assertNotIn("`", x["blocker"])
        self.assertLessEqual(len(long_["blocker"]), 160)
        self.assertTrue(long_["blocker"].endswith("…"), long_)

    def test_missing_or_broken_records_give_empty_sections(self):
        empty = tower(self.tmp, exam=None, moons=None, not_yet=None, rated=None)
        self.assertEqual(collect(self.stats, empty), {"louhi": {"trials": 0, "runs": [], "agents": [], "gens": []},
                                                      "moons": [], "underworld": []})
        tower(self.tmp, moons=MOONS, rated=["not", "a", "dict"])
        self.assertEqual([m["tier"] for m in self.stats.moons(self.tmp)], ["massive", "high", "extreme"])

    def test_main_writes_the_three_sections_and_the_committed_data_has_them(self):
        src = inspect.getsource(self.stats.main)
        for key in ("louhi", "moons", "underworld"):
            self.assertIn(f'"{key}": {key}(state)', src)
        data = json.loads(read_text(os.path.join(ROOT, "site", "data", "stats.json")))
        self.assertGreater(data["louhi"]["trials"], 0, "run python3 site/stats.py: the real exam record")
        self.assertTrue(data["moons"] and data["underworld"])
        for m in data["moons"]:
            self.assertEqual(set(m), {"id", "title", "tier", "stage", "needs"})


class Pages(unittest.TestCase):
    """pages.py draws each page from its stats section: the fixture's figures, and other figures from other records."""

    @classmethod
    def setUpClass(cls):
        cls.build, cls.pages, stats = site("build"), site("pages"), site("stats")
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            cls.data = collect(stats, tower(a))
            cls.more = collect(stats, tower(b, MORE_EXAM, MORE_MOONS, MORE_NOT_YET))

    def render(self, slug, data):
        page = next(p for p in self.pages.PAGES if p["slug"] == slug)
        return self.build.render_page(page, data, self.pages.PAGES)

    def test_each_page_is_in_the_nav(self):
        slugs = [p["slug"] for p in self.pages.PAGES]
        for slug in SLUGS:
            self.assertIn(slug, slugs)
            self.assertIn(f'href="../features/{slug}.html" aria-current="page"', self.render(slug, self.data))
        self.assertIn('href="../features/moons.html"', self.render("louhi", {}))

    def test_the_dials_read_the_records_and_move_with_them(self):
        for slug in SLUGS:
            with self.subTest(slug=slug):
                self.assertEqual(dials(self.render(slug, self.data)), DIALS[slug])
                self.assertEqual(dials(self.render(slug, self.more)), MORE_DIALS[slug])
                self.assertEqual(set(dials(self.render(slug, {})).values()), {"0"}, "no record: zeros, not typed ones")

    def test_each_scene_draws_one_mark_per_record(self):
        for slug, n in (("louhi", len(LOUHI["runs"])), ("moons", 3), ("underworld", 3)):
            with self.subTest(slug=slug):
                self.assertEqual(scene(self.render(slug, self.data), slug), n)
                self.assertEqual(scene(self.render(slug, {}), slug), 0)
        many = {"louhi": dict(LOUHI, runs=LOUHI["runs"] * 50)}
        self.assertEqual(scene(self.render("louhi", many), "louhi"), 60, "a scene stays bounded")

    def test_louhi_shows_the_scorecard_and_the_trend_by_generation(self):
        page = self.render("louhi", self.data)
        self.assertIn("<td>Sampo</td>", page, "the harness's own arm, by its name")
        self.assertIn("<td>oracle</td>", page)
        self.assertIn("0.417", page)
        for gen in ("gen 1", "gen 2"):
            self.assertIn(gen, page)

    def test_moons_lists_each_moon_with_its_stage(self):
        page = self.render("moons", self.data)
        box = re.search(r'<ol class="moons">(.*?)</ol>', page, re.S).group(1)
        self.assertEqual(re.findall(r'<li data-stage="([\w-]+)"', box), ["kill", "idea", "not-yet"])
        for word in ("M-01", "M-02", "M-03", "massive", "low", "extreme", "Sampo keeps code"):
            self.assertIn(word, box)

    def test_the_underworld_lists_what_waits_and_why(self):
        page = self.render("underworld", self.data)
        box = re.search(r'<ol class="waiting">(.*?)</ol>', page, re.S).group(1)
        self.assertEqual(len(re.findall(r"<li\b", box)), 3)
        self.assertIn("Sampo&#x27;s own history", box)
        self.assertNotIn("Gone idea", page)

    def test_each_page_names_its_verb_and_neither_the_old_name_nor_the_myth(self):
        for slug in SLUGS:
            for data in (self.data, {}):
                page = self.render(slug, data)
                self.assertIn(f"sampo {slug}", page)
                self.assertNotIn("Ilmarinen", page, "the myth is told once, on the landing page")
                self.assertFalse(names_foreman(page), names_foreman(page))


class Built(unittest.TestCase):
    """The built pages meet the landing page's bar: no other hosts, a still for every scene, whole with no script,
    light and dark, 320 px, AA contrast and fm design lint."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        r = build_copy(cls.tmp)
        if r.returncode:
            raise AssertionError(r.stdout + r.stderr)
        cls.out = os.path.join(cls.tmp, "out")
        cls.paths = {s: os.path.join(cls.out, "features", s + ".html") for s in SLUGS}
        cls.built = {s: read_text(p) for s, p in cls.paths.items()}
        cls.css = read_text(os.path.join(cls.out, "style.css"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_nothing_loads_from_another_host(self):
        self.assertEqual(build_module().outside_hosts(self.out), [])

    def test_every_scene_moves_only_where_motion_is_allowed(self):
        allowed = "".join(media_blocks(self.css, "@media (prefers-reduced-motion: no-preference)"))
        for use in re.findall(r"(?m)^\s*[^{}]*\{[^}]*\banimation(?:-name|-timeline)?:\s*(?!none)[^;}]+", self.css):
            self.assertIn(use.strip(), allowed, "an animation outside @media (prefers-reduced-motion: no-preference)")
        for name in ("trial", "forged", "waken"):
            self.assertIn(f"@keyframes {name} ", allowed)
            self.assertRegex(allowed, rf"animation(?:-name)?:\s*(?:[^;}}]*\s)?{name}\b", f"{name} is used")
        self.assertIn("animation-timeline: view()", allowed, "the scenes play as they scroll into view")
        for sky in ("aurora", "stars", "river"):
            self.assertIn(f'[data-sky="{sky}"]', self.css, "each sky has its own still colours")
        js = read_text(os.path.join(ROOT, "site", "site.js"))
        still = js.index("return;", js.index("prefers-reduced-motion: reduce"))
        for word in ("data-sky", "aurora", "stars", "river"):
            self.assertIn(word, js[still:], "the skies' shaders run only past the still return")
        for fetch in ("fetch(", "XMLHttpRequest", "stats.json"):
            self.assertNotIn(fetch, js, "nothing is fetched at view time")

    def test_the_pages_are_whole_without_script(self):
        for slug, page in self.built.items():
            with self.subTest(slug=slug):
                self.assertNotIn("<canvas", page, "site.js adds the shader; the HTML never needs it")
                scene(page, slug)
                self.assertEqual(len(dials(page)), 4)
                self.assertNotIn("Ilmarinen", page)
                self.assertFalse(names_foreman(page), names_foreman(page))

    def test_the_built_dials_read_the_committed_stats_and_other_stats_move_them(self):
        data = json.loads(read_text(os.path.join(ROOT, "site", "data", "stats.json")))
        self.assertEqual(dials(self.built["louhi"])["trials"], f'{data["louhi"]["trials"]:,}')
        self.assertEqual(dials(self.built["louhi"])["exam runs"], f'{len(data["louhi"]["runs"]):,}')
        self.assertEqual(dials(self.built["moons"])["moons"], f'{len(data["moons"]):,}')
        self.assertEqual(dials(self.built["underworld"])["waiting ideas"], f'{len(data["underworld"]):,}')
        with tempfile.TemporaryDirectory() as tmp:
            r = build_copy(tmp, edit_stats=lambda s: s.update(louhi=LOUHI, moons=MOON_ROWS, underworld=[]))
            self.assertEqual(r.returncode, 0, r.stderr)
            for slug, want in (("louhi", DIALS["louhi"]), ("moons", DIALS["moons"])):
                self.assertEqual(dials(read_text(os.path.join(tmp, "out", "features", slug + ".html"))), want)
            under = dials(read_text(os.path.join(tmp, "out", "features", "underworld.html")))
            self.assertEqual(set(under.values()), {"0"})

    def test_design_lint_passes(self):
        found = design.lint(list(self.paths.values()) + [os.path.join(self.out, "style.css")])
        self.assertEqual(found, [], found)

    def test_phone_width_and_contrast_in_both_themes(self):
        browser = headless_chrome()
        if not browser:
            self.skipTest("no headless Chromium (FOREMAN_CHROME, chrome-headless-shell or Playwright's download)")
        probe = """(() => {
          const solid = el => { for (; el; el = el.parentElement) { const c = getComputedStyle(el).backgroundColor;
            if (!/^rgba\\(.*,\\s*0(\\.0+)?\\)$|transparent/.test(c) && !/^rgba/.test(c)) return c; }
            return getComputedStyle(document.body).backgroundColor; };
          const pairs = [];
          for (const s of [".feature h1", ".feature .lede", ".proof dd", ".proof dt", ".proof p", ".moons li",
                           ".moons li > *", ".waiting li", ".waiting li > *"])
            for (const e of document.querySelectorAll(s)) pairs.push([s, getComputedStyle(e).color, solid(e)]);
          const marks = [...document.querySelectorAll(".sky .mk")];
          return {w: document.documentElement.scrollWidth, glow: !!document.querySelector(".sky canvas"), pairs,
                  marks: marks.length, shown: marks.filter(e => +getComputedStyle(e).opacity > 0.5).length};
        })()"""
        rgb = lambda c: tuple(int(x) / 255 for x in re.findall(r"[\d.]+", c)[:3])
        for scheme in ("light", "dark"):
            for reduced in (True, False):
                b = shot.Browser(browser, (320, 640), reduced=reduced)
                try:
                    b.call("Emulation.setEmulatedMedia", b.sid, features=[
                        {"name": "prefers-color-scheme", "value": scheme},
                        {"name": "prefers-reduced-motion", "value": "reduce" if reduced else "no-preference"}])
                    for slug, path in self.paths.items():
                        shot.load(b, "file://" + path)
                        got = b.call("Runtime.evaluate", b.sid, expression=probe, returnByValue=True)["result"]["value"]
                        where = f"{slug}, {scheme}, reduced motion {reduced}"
                        self.assertLessEqual(got["w"], 320, f"the page scrolls sideways at 320 px ({where})")
                        if reduced:
                            self.assertFalse(got["glow"], f"no shader under reduced motion ({where})")
                            self.assertTrue(got["marks"], where)
                            self.assertEqual(got["shown"], got["marks"], f"the still shows the whole scene ({where})")
                            self.assertTrue(got["pairs"])
                            for sel, fg, bg in got["pairs"]:
                                self.assertGreaterEqual(design.contrast(rgb(fg), rgb(bg)), 4.5,
                                                        f"{sel}: {fg} on {bg} ({where})")
                finally:
                    b.close()


if __name__ == "__main__":
    unittest.main()
