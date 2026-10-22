"""T-1609: the landing page's hero opens on an inline SVG poster of the proof chain, drawn by site/build.py from
site/data/stats.json (tasks done, evidence, proofs, commits as stations sized by their totals): the first paint, and
the still that T-1610's scene sits over."""
import html
import importlib.util
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import unittest

from helpers import PLUGIN, headless_chrome, read_json, read_text

ROOT = os.path.dirname(PLUGIN)
KEYS = ("tasks_done", "evidence", "proofs", "commits")


def build_module():
    spec = importlib.util.spec_from_file_location("site_build_hero", os.path.join(ROOT, "site", "build.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_copy(tmp, totals=None, edit_index=None):
    """Build a copy of site/ the way the workflow does, its stats.json totals updated with `totals` and its
    index.html passed through `edit_index`; the finished process."""
    shutil.copytree(os.path.join(ROOT, "site"), os.path.join(tmp, "site"), ignore=shutil.ignore_patterns("__pycache__"))
    for d in ("demo", "plugin"):
        os.symlink(os.path.join(ROOT, d), os.path.join(tmp, d))
    if totals:
        path = os.path.join(tmp, "site", "data", "stats.json")
        stats = read_json(path)
        stats["totals"].update(totals)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(stats, f)
    if edit_index:
        path = os.path.join(tmp, "site", "index.html")
        page = edit_index(read_text(path))
        with open(path, "w", encoding="utf-8") as f:
            f.write(page)
    return subprocess.run([sys.executable, os.path.join(tmp, "site", "build.py"), os.path.join(tmp, "out")],
                          capture_output=True, text=True, timeout=120)


def built_index(tmp, totals=None):
    r = build_copy(tmp, totals)
    if r.returncode:
        raise AssertionError(r.stdout + r.stderr)
    return read_text(os.path.join(tmp, "out", "index.html"))


def hero_poster(page, cls="poster"):
    """The SVG of this class inside the hero (between the hero's opening tag and the first section), or ''."""
    start = page.index('class="wrap hero"')
    hero = page[start:page.index("<section", start)]
    m = re.search(rf'<svg class="{cls}"[^>]*>.*?</svg>', hero, re.S)
    return m.group(0) if m else ""


def sides(svg):
    """Each station's side, in order: a square turned 45°, the site's diamond."""
    found = re.findall(r'<rect class="st"[^>]* width="([\d.]+)"[^>]* transform="rotate\(45 [^"]*\)"', svg)
    return [float(s) for s in found]


def label(svg):
    return html.unescape(re.search(r'<svg [^>]*aria-label="([^"]*)"', svg)[1])


class Hero(unittest.TestCase):
    def test_the_built_hero_is_an_inline_poster_of_the_real_totals(self):
        totals = read_json(os.path.join(ROOT, "site", "data", "stats.json"))["totals"]
        with tempfile.TemporaryDirectory() as tmp:
            svg = hero_poster(built_index(tmp))
        self.assertTrue(svg, "no <svg class=\"poster\"> in the built hero")
        self.assertRegex(svg[:svg.index(">")], r'\brole="img"')
        for k in KEYS:
            self.assertIn(f"{totals[k]:,}", label(svg), k)  # screen readers hear the real numbers
            self.assertIn(f">{totals[k]:,}<", svg, k)  # and they are drawn as text, not baked into a picture
        self.assertEqual(build_module().outside_loads(svg, ".svg"), [])
        self.assertNotRegex(svg, r"\b(?:src|href)=", "the poster fetches nothing")

    def test_a_changed_stats_json_changes_the_poster(self):
        changed = {"tasks_done": 12345, "evidence": 7, "proofs": 0, "commits": 999999}
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            before, after = hero_poster(built_index(a)), hero_poster(built_index(b, changed))
        self.assertNotEqual(before, after)
        for k, v in changed.items():
            self.assertIn(f"{v:,}", label(after), k)
            self.assertIn(f">{v:,}<", after, k)

    def test_each_station_is_a_diamond_sized_by_its_total_in_one_hue(self):
        build = build_module()
        totals = {"tasks_done": 734, "evidence": 2684, "proofs": 250, "commits": 570}
        svg = build.poster(totals)
        side = sides(svg)
        self.assertEqual(len(side), 4)
        self.assertEqual(sorted(range(4), key=lambda i: side[i]), sorted(range(4), key=lambda i: totals[KEYS[i]]))
        self.assertNotIn("Gradient", svg, "the counts aren't states: no red-to-green traffic light")
        # nothing yet (all zeros, or a stats.json from before a key existed) draws zeros instead of dividing by zero
        for odd in ({}, {k: 0 for k in KEYS}):
            with self.subTest(odd=odd):
                self.assertIn("0 tasks done", label(build.poster(odd)))

    def test_phones_get_a_two_by_two_poster_without_the_date(self):
        build = build_module()
        compact = build.poster({"tasks_done": 734, "evidence": 2684, "proofs": 250, "commits": 570}, "2026-10-20", 2)
        self.assertEqual(len(sides(compact)), 4)
        centres = [m.split() for m in re.findall(r'rotate\(45 ([^)]*)\)', compact)]
        self.assertEqual(len({x for x, _ in centres}), 2, "two columns")
        self.assertEqual(len({y for _, y in centres}), 2, "two rows")
        self.assertNotIn('class="kick"', compact)
        self.assertIn("2026-10-20", label(compact), "the date stays in what a screen reader hears")
        with tempfile.TemporaryDirectory() as tmp:
            self.assertTrue(hero_poster(built_index(tmp), "poster compact"), "the built hero carries both")

    def test_an_index_without_the_poster_mark_fails_the_build(self):
        # review: a lost mark built a hero with no poster and exit 0
        build = build_module()
        with tempfile.TemporaryDirectory() as tmp:
            r = build_copy(tmp, edit_index=lambda page: page.replace(build.POSTER_MARK, ""))
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("site/index.html lost the poster mark", r.stderr)


def hero_scene(page):
    """T-1610: the hero's scene box (both posters and the canvas) and its inline script, or ('', '')."""
    start = page.index('class="wrap hero"')
    hero = page[start:page.index("<section", start)]
    box = re.search(r'<div class="hero-scene"[^>]*>.*?</div>', hero, re.S)
    script = re.search(r"<script type=\"module\">(.*?)</script>", hero, re.S)
    return (box.group(0) if box else ""), (script.group(1) if script else "")


# Run after the scene's module script: wait for the first frame, read the canvas, lose the context and get it back.
PROBE = """<script>(async () => {
  const box = document.querySelector(".hero-scene"), c = box.querySelector("canvas");
  const wait = s => new Promise(r => { let n = 300; const t = setInterval(() => {
    if (box.dataset.state === s || !n--) { clearInterval(t); r(box.dataset.state); } }, 10); });
  const got = { first: await wait("live"), hidden: c.getAttribute("aria-hidden"), dpr: c.width / c.clientWidth };
  const lose = c.getContext("webgl2").getExtension("WEBGL_lose_context");
  lose.loseContext(); got.lost = await wait("lost");
  lose.restoreContext(); got.back = await wait("live");
  document.body.insertAdjacentHTML("beforeend", "<pre id=probe>" + JSON.stringify(got) + "</pre>");
})();</script>"""


class Scene(unittest.TestCase):
    """T-1610: a single-file WebGL2 scene over the poster; the poster stays without WebGL2 or with reduced motion."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.page = built_index(cls.tmp)
        cls.out = os.path.join(cls.tmp, "out")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_the_built_hero_carries_the_scene_inline_over_the_poster(self):
        box, script = hero_scene(self.page)
        self.assertTrue(box, 'no <div class="hero-scene"> in the built hero')
        self.assertIn('data-state="poster"', box[:box.index(">")], "the poster is the first paint")
        canvas = re.search(r"<canvas[^>]*>", box)
        self.assertTrue(canvas, "no canvas in the scene box")
        self.assertLess(box.index('<svg class="poster"'), canvas.start(), "the canvas sits over the poster")
        self.assertLess(box.index('<svg class="poster compact"'), canvas.start())
        tag = canvas.group(0)
        self.assertRegex(tag, r'\brole="img"')
        self.assertRegex(tag, r'\baria-label="[^"]{20,}"')
        self.assertRegex(tag, r'\baria-hidden="true"', "hidden from screen readers while the poster shows")
        self.assertTrue(script.strip(), "no inline module script in the hero")
        for need in ('getContext("webgl2"', "prefers-reduced-motion: reduce", "webglcontextlost",
                     "webglcontextrestored", "preventDefault", "devicePixelRatio", "IntersectionObserver",
                     "visibilitychange"):
            self.assertIn(need, script)
        self.assertNotRegex(self.page, r"<script[^>]*\bsrc=[\"'](?!site\.js)", "no other script file")
        self.assertEqual(build_module().outside_loads(self.page, ".html"), [])
        self.assertFalse(os.path.exists(os.path.join(self.out, "hero-scene.js")), "inlined, not shipped twice")
        css = read_text(os.path.join(ROOT, "site", "style.css"))
        self.assertRegex(css, r"\.hero-scene canvas \{[^}]*opacity: 0", "the canvas is invisible until live")
        self.assertRegex(css, r'\.hero-scene\[data-state="live"\] canvas \{[^}]*opacity: 1')
        if shutil.which("node"):  # the scene parses as a module
            js = os.path.join(self.tmp, "scene.mjs")
            with open(js, "w", encoding="utf-8") as f:
                f.write(script)
            r = subprocess.run(["node", "--check", js], capture_output=True, text=True, timeout=60)
            self.assertEqual(r.returncode, 0, r.stderr)

    def browse(self, *flags, page=None, shot=None):
        """The built index (or `page`) in a headless Chromium at 1280x1100, 12 s of virtual time (a whole pass): the
        dumped DOM, the box's data-state and the page's console lines; with `shot`, a screenshot there instead."""
        browser = headless_chrome()
        if not browser:
            self.skipTest("no headless Chromium (FOREMAN_CHROME, chrome-headless-shell or Playwright's download)")
        try:  # its own process group: a timeout kills the GPU and renderer children too
            p = subprocess.Popen([browser, "--headless", "--use-angle=swiftshader", "--enable-unsafe-swiftshader",
                                  "--window-size=1280,1100", "--hide-scrollbars", "--virtual-time-budget=12000",
                                  "--enable-logging=stderr", "--v=0", *flags,
                                  "--user-data-dir=" + tempfile.mkdtemp(dir=self.tmp),
                                  "--screenshot=" + shot if shot else "--dump-dom",
                                  "file://" + (page or os.path.join(self.out, "index.html"))],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
            out, err = p.communicate(timeout=120)
        except OSError as e:
            self.skipTest(f"{browser} didn't run: {e}")
        except subprocess.TimeoutExpired:
            os.killpg(p.pid, signal.SIGKILL)
            p.communicate()
            self.fail("headless Chromium timed out after 120 s")
        if not (os.path.isfile(shot) if shot else 'class="wrap hero"' in out):  # a root sandbox, no display libs
            self.skipTest(f"{browser} printed no page: {err[-300:]}")
        state = re.search(r'<div class="hero-scene" data-state="([^"]*)"', out)
        return out, (state.group(1) if state else ""), [ln for ln in err.splitlines() if ":CONSOLE" in ln]

    def test_reduced_motion_and_no_webgl2_keep_the_poster_still(self):
        for flags, want in ((["--force-prefers-reduced-motion"], "still"), (["--disable-3d-apis"], "no-webgl2")):
            with self.subTest(flags=flags):
                out, state, console = self.browse(*flags)
                self.assertEqual(state, want)
                self.assertEqual(console, [], "nothing logged, nothing thrown")
                self.assertRegex(re.search(r"<canvas[^>]*>", out).group(0), r'aria-hidden="true"')

    def test_with_webgl2_the_scene_goes_live_survives_a_lost_context_and_caps_the_pixel_ratio(self):
        page = os.path.join(self.out, "probe.html")  # beside style.css, so it is styled
        with open(page, "w", encoding="utf-8") as f:
            f.write(self.page.replace("</body>", PROBE + "</body>"))
        out, _, console = self.browse("--force-device-scale-factor=3", page=page)
        got = re.search(r"<pre id=\"probe\">(.*?)</pre>", out)
        self.assertTrue(got, "the probe never finished")
        got = json.loads(html.unescape(got.group(1)))
        self.assertEqual((got["first"], got["lost"], got["back"]), ("live", "lost", "live"), got)
        self.assertIsNone(got["hidden"], "live, the canvas is named to screen readers")
        self.assertLessEqual(got["dpr"], 2.01, "the device pixel ratio is capped at 2")
        self.assertEqual([ln for ln in console if "scene" in ln.lower() or "Uncaught" in ln], [], console)

    def test_after_its_pass_the_scene_is_the_poster_lit(self):
        # the first build drew the track black (a NaN in a uniform) and every DOM check still passed: look at it.
        # At rest, the track keeps the poster's --rule and each diamond is a lit form: its upper-left facet
        # brighter than its lower-right, both the signal's amber, where the poster's flat diamond is one colour
        import fmimg
        page = os.path.join(self.out, "where.html")
        with open(page, "w", encoding="utf-8") as f:
            f.write(self.page.replace("</body>", WHERE + "</body>"))
        where = re.search(r'<pre id="where">(.*?)</pre>', self.browse(page=page)[0])
        self.assertTrue(where, "the geometry probe never finished")
        where = json.loads(html.unescape(where.group(1)))
        shot, still = os.path.join(self.tmp, "rest.png"), os.path.join(self.out, "rest.html")
        with open(still, "w", encoding="utf-8") as f:  # the fade runs in real time, not virtual: catch it mid-way and
            f.write(self.page.replace("</head>", NO_FADE + "</head>"))  # the poster shows through
        self.browse(page=still, shot=shot)
        img = fmimg.load(shot)
        px = lambda x, y: img.rgba[(round(y) * img.width + round(x)) * 4:][:3]
        lum = lambda c: 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
        rule = bytes.fromhex(re.search(r"--rule: #(\w{6})", read_text(os.path.join(ROOT, "site", "style.css")))[1])
        (x0, _, h0), (x1, _, h1) = where["st"][:2]
        track = px((x0 + h0 + x1 - h1) / 2, where["y"])
        self.assertLessEqual(max(abs(a - b) for a, b in zip(track, rule)), 16, f"track {tuple(track)}, --rule {tuple(rule)}, {where}")
        for i, (x, y, h) in enumerate(where["st"]):
            lit, shade = px(x - h / 4, y - h / 4), px(x + h / 4, y + h / 4)
            with self.subTest(station=i, lit=tuple(lit), shade=tuple(shade)):
                self.assertGreater(lum(lit), lum(shade) + 25, "faceted and lit, not the flat poster")
                self.assertGreater(lum(shade), 60, "not black")
                for c in (lit, shade):
                    self.assertGreater(c[0] - c[2], 80, "the signal's amber")


NO_FADE = "<style>.hero-scene * { transition: none !important; }</style>"
# Where the wide poster draws its stations and track, in CSS pixels: [centre x, centre y, half-diagonal] each.
WHERE = """<script>addEventListener("load", () => {
  const svg = document.querySelector("svg.poster:not(.compact)"), box = r => r.getBoundingClientRect();
  const st = [...svg.querySelectorAll(".st")].map(e => { const b = box(e); return [b.x + b.width / 2, b.y + b.height / 2, b.width / 2]; });
  const t = box(svg.querySelector(".track"));
  document.body.insertAdjacentHTML("beforeend", "<pre id=where>" + JSON.stringify({ st, y: t.y + t.height / 2 }) + "</pre>");
});</script>"""


if __name__ == "__main__":
    unittest.main()
