"""T-1653: showpieces, one-file 3D pages built on the scene template's survival contract. fm page city: the repo as a
city from fm map's data, each file a building (height by lines, lit windows by churn) on a district per folder."""
import html
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest

from helpers import PLUGIN, SPY, ForemanTestCase, devtools, headless_chrome, read_text

import fmcore as c
import fmpage

FILES = [  # fixture: what fmpage.city_files reads from a repo (path, lines, commits in 180 days)
    {"path": "plugin/lib/fmcore.py", "lines": 9000, "churn": 120},
    {"path": "plugin/lib/fmcli.py", "lines": 6200, "churn": 300},
    {"path": "plugin/lib/fmpage.py", "lines": 280, "churn": 4},
    {"path": "plugin/tests/test_core.py", "lines": 3100, "churn": 40},
    {"path": "plugin/tests/test_page.py", "lines": 160, "churn": 0},
    {"path": "site/build.py", "lines": 700, "churn": 9},
    {"path": "README.md", "lines": 400, "churn": 2},
    {"path": "MASTER.md", "lines": 90, "churn": 0},
] + [{"path": f"plugin/skills/library/cards/card{i}.md", "lines": 30 + i, "churn": i % 3} for i in range(24)]
# The template's survival code, which the city copies (as site/hero-scene.js does): neither may drift alone.
SURVIVAL = (r'"webglcontextlost", e => \{ e\.preventDefault\(\)', r'"webglcontextrestored"',
            r'Math\.min\(window\.devicePixelRatio \|\| 1, matchMedia\("\(pointer: coarse\)"\)\.matches \? 1\.5 : 2\)',
            r'on\(document, "visibilitychange"',
            r"new IntersectionObserver\(entries => \{ onscreen = entries\.at\(-1\)\.isIntersecting",
            r'matchMedia\("\(prefers-reduced-motion: reduce\)"\)', r"failIfMajorPerformanceCaveat: true")
TEMPLATE = os.path.join(PLUGIN, "skills", "playbooks", "references", "ui", "templates", "scene.html")


def data_of(page):
    return json.loads(re.search(r'<script type="application/json" id="city">(.*?)</script>', page, re.S).group(1))


class City(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.page = fmpage.city_html(FILES, "Foreman")

    def test_one_file_with_the_poster_first_and_nothing_from_another_host(self):
        page = self.page
        self.assertNotRegex(page, r"__[A-Z]+__", "every placeholder filled")
        fig = re.search(r'<figure class="city"[^>]*>', page).group(0)
        self.assertIn('data-state="poster"', fig, "the poster is the first paint")
        self.assertLess(page.index('<svg class="poster"'), page.index("<canvas"), "the canvas sits over the poster")
        self.assertIsNone(re.search(r"""<(?:link|script|img|iframe)\b[^>]*\b(?:href|src)=["']?(?:https?:)?//""", page))
        self.assertNotRegex(page, r"<script[^>]*\bsrc=", "inlined: no script file")
        self.assertNotIn("@import", page)
        self.assertNotIn("url(http", page)
        self.assertEqual(page.count("</script>"), 2, "the data block and the module only")

    def test_a_hostile_folder_and_file_name_is_escaped_everywhere_it_shows(self):
        # review: the hostile name sits where it reaches the output: the second-biggest district, the hottest file
        folder, name = 'evil"><b>dir', 'a"><img src=x onerror=1>.py'
        page = fmpage.city_html(FILES + [{"path": f"{folder}/{name}", "lines": 5000, "churn": 999},
                                         {"path": f"{folder}/</script><b>.py", "lines": 4000, "churn": 1}], "Foreman")
        for raw in ("<img src=x", "<b>dir", "</script><b>"):
            self.assertNotIn(raw, page)
        self.assertEqual(page.count("</script>"), 2, "a path can't close a tag")
        label = re.search(r'<canvas[^>]*aria-label="([^"]*)"', page).group(1)
        twin = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", page, re.S).group(1)
        poster = re.search(r'<svg class="poster".*?</svg>', page, re.S).group(0)
        for where, text in (("label", label), ("twin", twin)):
            self.assertIn(html.escape(name), text, where)
            self.assertIn(html.escape(folder), text, where)
        self.assertIn('<text class="tag" ', poster)
        self.assertIn(f">{html.escape(folder)}</text>", poster)
        self.assertIn(folder, [d["name"] for d in data_of(page)["d"]], "the JSON keeps the name, '<' escaped")
        self.assertIn("evil\\\">\\u003cb>dir", page)

    def test_a_leak_names_the_path(self):
        with self.assertRaisesRegex(fmpage.Leak, r"/home/someone/x\.py"):
            fmpage.city_html(FILES + [{"path": "/home/someone/x.py", "lines": 3, "churn": 0}], "x")

    def test_history_unavailable_is_not_every_window_dark(self):
        page = fmpage.city_html([dict(f, churn=0) for f in FILES], "Foreman", history=False)
        label = html.unescape(re.search(r'<canvas[^>]*aria-label="([^"]*)"', page).group(1))
        self.assertIn("history unavailable", label)
        self.assertNotIn("every window is dark", label)

    def test_estimated_lines_past_the_read_budget_are_said_on_the_page(self):
        page = fmpage.city_html(FILES, "Foreman", estimated=7)
        twin = html.unescape(re.search(r"<figcaption[^>]*>(.*?)</figcaption>", page, re.S).group(1))
        self.assertRegex(twin, r"7 files.*estimated from their size.*256 MB")

    def test_the_intro_is_short_and_any_input_ends_it(self):
        script = re.search(r'<script type="module">(.*?)</script>', self.page, re.S).group(1)
        self.assertLessEqual(float(re.search(r"\bPASS = ([\d.]+)", script).group(1)), 5, "WCAG 2.2.2: 5 s or a control")
        self.assertRegex(script, r"const turn = [^\n]*pass = PASS", "the first drag or key ends the intro")
        key = re.search(r'<p class="key"[^>]*>(.*?)</p>', self.page, re.S).group(1)
        self.assertIn("drag or arrow keys", key)
        self.assertRegex(self.page, r'\.city\[data-state="live"\] canvas \{[^}]*cursor: grab')

    def test_the_label_summarises_the_biggest_areas_and_the_text_twin_holds_them(self):
        canvas = re.search(r"<canvas[^>]*>", self.page).group(0)  # the template's way: named, focusable once live
        self.assertRegex(canvas, r'\brole="img"')
        self.assertNotIn("aria-hidden", canvas)
        label = html.unescape(re.search(r'aria-label="([^"]*)"', canvas).group(1))
        self.assertIn(f"{len(FILES)} files", label)
        self.assertIn("plugin/lib", label, "the biggest district by lines comes first")
        self.assertLess(label.index("plugin/lib"), label.index("plugin/tests"))
        self.assertIn("fmcli.py", label, "the most changed file is named")
        self.assertRegex(re.search(r"<svg class=\"poster\"[^>]*>", self.page).group(0), r'aria-hidden="true"')
        twin = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", self.page, re.S).group(1)
        for name in ("plugin/lib", "plugin/tests", "site", "plugin/skills/library/cards"):
            self.assertIn(name, html.unescape(twin))

    def test_a_building_per_file_sized_by_lines_on_its_folders_district(self):
        d = data_of(self.page)
        self.assertEqual(len(d["b"]), len(FILES))
        names = [x["name"] for x in d["d"]]
        self.assertEqual(sorted(names), sorted({"plugin/lib", "plugin/tests", "site", "plugin/skills/library/cards",
                                                "."}), "one district per folder; root files on '.'")
        heights = [b[3] for b in d["b"]]
        self.assertEqual(heights, sorted(heights, reverse=True), "biggest file first, tallest")
        self.assertAlmostEqual(heights[0], d["hmax"], places=1)
        self.assertGreater(heights[0], heights[2] * 1.2, "9000 lines stands taller than 3100")
        heat = [b[4] for b in d["b"]]
        self.assertEqual(max(heat), heat[1], "fmcli.py, the most changed, burns brightest")
        self.assertEqual(heat[[f["path"] for f in sorted(FILES, key=lambda f: -f["lines"])].index("MASTER.md")], 0)
        for b in d["b"]:  # every building stands inside its district's plate
            x, z, w, _, _, delay, di = b
            plate = d["d"][di]
            self.assertLessEqual(abs(x - plate["x"]) + w / 2, plate["w"] / 2 + 1e-6, (b, plate))
            self.assertLessEqual(abs(z - plate["z"]) + w / 2, plate["d"] / 2 + 1e-6, (b, plate))
            self.assertTrue(0 <= delay <= 1)
        plates = [(p["x"] - p["w"] / 2, p["x"] + p["w"] / 2, p["z"] - p["d"] / 2, p["z"] + p["d"] / 2) for p in d["d"]]
        for i, a in enumerate(plates):  # districts never overlap
            for b in plates[i + 1:]:
                self.assertTrue(a[1] <= b[0] or b[1] <= a[0] or a[3] <= b[2] or b[3] <= a[2], (a, b))
        self.assertEqual(len(re.findall(r'<path class="b', self.page)), 2 * len(FILES), "the poster draws each one")

    def test_reduced_motion_no_webgl2_and_the_templates_survival_code(self):
        script = re.search(r'<script type="module">(.*?)</script>', self.page, re.S).group(1)
        template = read_text(TEMPLATE)
        for marker in SURVIVAL:
            for name, text in (("city.html", script), ("templates/scene.html", template)):
                self.assertTrue(re.search(marker, text), f"{name} lost {marker}")
        self.assertIn('setState("still")', script, "reduced motion keeps the poster, with no context")
        self.assertIn('setState("no-webgl2")', script)
        self.assertLess(script.index('setState("still")'), script.index('getContext("webgl2"'),
                        "reduced motion returns before any context is made")
        self.assertRegex(self.page, r"@media \(prefers-reduced-motion: reduce\)")
        if shutil.which("node"):
            js = os.path.join(self.tmp, "city.mjs")
            with open(js, "w", encoding="utf-8") as f:
                f.write(script)
            r = subprocess.run(["node", "--check", js], capture_output=True, text=True, timeout=60)
            self.assertEqual(r.returncode, 0, r.stderr)

    def test_design_lint_is_clean(self):
        import fmdesign
        path = os.path.join(self.tmp, "city.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.page)
        self.assertEqual(fmdesign.lint([path]), [])

    def test_an_absolute_path_is_refused(self):
        with self.assertRaises(fmpage.Leak):
            fmpage.city_html(FILES + [{"path": "/home/someone/x.py", "lines": 3, "churn": 0}], "x")

    def test_fm_page_city_reads_the_repo_and_never_overwrites_a_foreign_file(self):
        self.fm("init")
        for path, lines in (("src/app.py", 120), ("src/util.py", 30), ("docs/guide.md", 60), ("setup.py", 8)):
            os.makedirs(os.path.join(self.repo, os.path.dirname(path) or "."), exist_ok=True)
            with open(os.path.join(self.repo, path), "w") as f:
                f.write("x\n" * lines)
        with open(os.path.join(self.repo, "logo.png"), "wb") as f:
            f.write(b"\x89PNG\0\0\0binary")
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "files"], check=True)
        with open(os.path.join(self.repo, "src", "app.py"), "a") as f:
            f.write("y\n")
        subprocess.run(["git", "-C", self.repo, "commit", "-qam", "again"], check=True)
        r = json.loads(self.fm("page", "city", "--json").stdout)
        p = c.find_project(self.repo)
        self.assertEqual(r["path"], os.path.join(p.dir, "city.html"))
        d = data_of(read_text(r["path"]))
        tracked = subprocess.run(["git", "-C", self.repo, "ls-files"], capture_output=True, text=True).stdout.split()
        self.assertIn("logo.png", tracked)
        self.assertEqual(r["files"], len(tracked) - 1, "the binary file is no building")
        self.assertEqual(len(d["b"]), r["files"])
        self.assertEqual(sorted(x["name"] for x in d["d"]), [".", "docs", "src"])
        self.assertEqual(max(b[4] for b in d["b"]), d["b"][0][4], "app.py: the tallest and the most changed")
        self.assertNotIn(self.tmp, read_text(r["path"]))
        self.fm("page", "city")  # a second run replaces its own page
        mine = os.path.join(self.tmp, "mine.html")
        with open(mine, "w") as f:
            f.write("<p>mine</p>")
        r = self.fm("page", "city", "--out", mine, check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(read_text(mine), "<p>mine</p>")

    def _commit(self, path, text, msg):
        os.makedirs(os.path.dirname(os.path.join(self.repo, path)), exist_ok=True)
        with open(os.path.join(self.repo, path), "a") as f:
            f.write(text)
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", msg], check=True)

    def test_a_project_in_a_subfolder_gets_its_own_churn(self):
        # review: ls-files paths are relative to the project, git log's to the repo root without --relative
        self._commit("sub/app.py", "x\n", "one")
        self._commit("sub/app.py", "y\n", "two")
        self._commit("other.py", "z\n", "three")
        files, info = fmpage.city_files(os.path.join(self.repo, "sub"))
        self.assertEqual([(f["path"], f["lines"], f["churn"]) for f in files], [("app.py", 2, 2)])
        self.assertTrue(info["history"])

    def test_a_failed_git_log_is_history_unavailable(self):
        from unittest import mock
        import fmmap
        self._commit("app.py", "x\n", "one")
        real = fmmap._git
        broken = lambda root, *a, **kw: (subprocess.CompletedProcess(a, 124, "", "timed out") if "log" in a
                                         else real(root, *a, **kw))
        with mock.patch.object(fmmap, "_git", broken):
            files, info = fmpage.city_files(self.repo)
        self.assertFalse(info["history"])
        self.assertEqual([f["path"] for f in files if f["path"] == "app.py"], ["app.py"])

    def test_past_the_read_budget_lines_are_estimated_from_size(self):
        from unittest import mock
        for i in range(3):  # 10, 20 and 30 KB: past the 8 KB head every file gets
            self._commit(f"f{i}.txt", ("x" * 99 + "\n") * (100 * (i + 1)), f"c{i}")
        with mock.patch.object(fmpage, "READ_BUDGET", 16000):
            files, info = fmpage.city_files(self.repo)
        lines = {f["path"]: f["lines"] for f in files}
        self.assertEqual(lines["f2.txt"], 300, "read in full: inside the budget")
        self.assertGreater(info["estimated"], 0)
        self.assertAlmostEqual(lines["f0.txt"], 100, delta=5, msg="estimated from bytes per line so far")


class CityBrowser(unittest.TestCase):
    """The city in a real headless Chromium over DevTools, real time (virtual time never runs frame callbacks)."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.path = os.path.join(cls.tmp, "city.html")
        with open(cls.path, "w", encoding="utf-8") as f:
            f.write(fmpage.city_html(FILES, "Foreman"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def spied(self, at, media=(), init="", expr=None):
        browser = headless_chrome()
        if not browser:
            self.skipTest("no headless Chromium (FOREMAN_CHROME, chrome-headless-shell or Playwright's download)")
        try:
            return devtools(browser, "file://" + self.path, tempfile.mkdtemp(dir=self.tmp), SPY + init, media, at,
                            expr or "({ ...window.__spy, state: document.querySelector('.city').dataset.state })")
        except (EOFError, BrokenPipeError, FileNotFoundError, PermissionError) as e:  # a root sandbox, no libs
            self.skipTest(f"{browser} didn't take DevTools over a pipe: {e!r}")

    def test_it_draws_frames_in_real_time_then_rests(self):
        early, mid, late = self.spied((3, 10, 12))  # the pass is 4.5 s: slack for a loaded machine's late start
        self.assertEqual(early["state"], "live", early)
        self.assertIn("webgl2", early["contexts"])
        self.assertGreater(early["raf"], 10, "the rise and the turn draw frames in real time")
        self.assertEqual(mid["raf"], late["raf"], "after its pass the city rests: no frames")

    def test_the_first_key_ends_the_intro(self):
        # review (WCAG 2.2.2): input stops the auto motion; frames stop once the turn it asked for settles
        probe = """(() => { const s = window.__spy; s.n = (s.n || 0) + 1;
          if (s.n === 1) document.querySelector('.city canvas').dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight' }));
          return s.raf; })()"""
        # the key at 1.5 s; the step it asks for settles in about a second; the pass, begun at the first frame after
        # the load, would run past 4.5 s
        _, settled, later = self.spied((1.5, 3.8, 4.5), expr=probe)
        self.assertEqual(settled, later, "no frames before the 4.5 s pass would have ended")

    def test_reduced_motion_and_no_webgl2_keep_the_poster_still(self):
        still, = self.spied((3,), [("prefers-reduced-motion", "reduce")])
        self.assertEqual((still["state"], still["raf"]), ("still", 0))
        self.assertNotIn("webgl2", still["contexts"], "reduced motion asks for no WebGL context at all")
        none = """const get = HTMLCanvasElement.prototype.getContext;
          HTMLCanvasElement.prototype.getContext = function (t, ...r) { return t === "webgl2" ? null : get.call(this, t, ...r); };"""
        flat, = self.spied((3,), init=none)
        self.assertEqual((flat["state"], flat["raf"]), ("no-webgl2", 0))

    def test_a_lost_context_shows_the_poster_and_comes_back(self):
        probe = """(() => { const f = document.querySelector('.city'), s = window.__spy; s.n = (s.n || 0) + 1;
          s.ext = s.ext || f.querySelector('canvas').getContext('webgl2').getExtension('WEBGL_lose_context');
          const was = f.dataset.state; if (s.n === 1) s.ext.loseContext(); if (s.n === 2) s.ext.restoreContext();
          return was; })()"""
        self.assertEqual(self.spied((5, 6.5, 9), expr=probe), ["live", "lost", "live"])


if __name__ == "__main__":
    unittest.main()
