"""T-1541: the site builds byte for byte the same twice from one commit; each recorded fm code run becomes a case-study
page; the Releases page has a wall of generated covers; a task proved red then green gets a title card."""
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

from helpers import PLUGIN, ForemanTestCase, read_text

ROOT = os.path.dirname(PLUGIN)


def site(name):
    sys.path.insert(0, os.path.join(ROOT, "site"))
    try:
        spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "site", name + ".py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    finally:
        sys.path.pop(0)


RUN = [{"event": "start", "request": "FIX: <b>total</b> ignores qty", "worker": "claude", "ts": 100.0},
       {"event": "plan", "plan": {"type": "FIX", "tier": "S", "title": "total() counts qty", "steps": ["test", "fix"],
                                  "criteria": [{"text": "qty counts", "verify": "python3 -m unittest"}]}, "ts": 101.0},
       {"event": "verify", "criterion": 1, "label": "before", "exit": 1, "cmd": "python3 -m unittest", "ts": 102.0},
       {"event": "step", "step": 1, "text": "step 1: write the test", "ts": 103.0},
       {"event": "changed", "step": 1, "files": ["cart.py"], "stat": {"cart.py": [1, 1]}, "ts": 110.0},
       {"event": "verify", "criterion": 1, "label": "verify", "exit": 0, "cmd": "python3 -m unittest", "ts": 170.0},
       {"event": "closed", "task": "T-0001", "text": "T-0001 closed; committed abc1234", "ts": 171.0}]


class Reproducible(unittest.TestCase):
    def test_two_builds_are_byte_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            outs = [os.path.join(tmp, d) for d in ("a", "b")]
            for out in outs:
                p = subprocess.run([sys.executable, os.path.join(ROOT, "site", "build.py"), out], capture_output=True,
                                   text=True, timeout=300)
                self.assertEqual(p.returncode, 0, p.stderr)
            files = [sorted(os.path.relpath(os.path.join(d, f), out) for d, _, fs in os.walk(out) for f in fs)
                     for out in outs]
            self.assertEqual(files[0], files[1])
            self.assertTrue(any(f.startswith("stories" + os.sep) for f in files[0]))
            for rel in files[0]:
                with open(os.path.join(outs[0], rel), "rb") as a, open(os.path.join(outs[1], rel), "rb") as b:
                    self.assertTrue(a.read() == b.read(), f"{rel} differs between two builds")


class Stories(unittest.TestCase):
    def test_a_case_study_renders_from_a_fixture_ledger(self):
        build = site("build")
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "fix.jsonl")
            with open(path, "w") as f:
                f.write("".join(json.dumps(e) + "\n" for e in RUN))
            page = build.case_study_html("fix", "Fix a bug", build.load_example(path))
        self.assertIn("&lt;b&gt;total&lt;/b&gt; ignores qty", page)
        self.assertNotIn("<b>total</b>", page)
        self.assertIn('<li class="fail"><span class="at">2s</span> <b>before</b> fails: <code>python3 -m unittest', page)
        self.assertIn('<li class="pass"><span class="at">1m10s</span> <b>check</b> passes', page)
        self.assertIn("<b>changed</b> <code>cart.py</code>", page)
        self.assertIn("<b>closed</b> T-0001 closed; committed abc1234", page)

    def test_the_releases_wall_draws_a_cover_per_release(self):
        wall = site("pages")._wall({"releases": [{"version": "1.2.3", "day": "2026-01-01", "tests": 50},
                                                 {"version": "1.2.4", "day": "2026-01-02", "tests": 100}]})
        self.assertEqual(wall.count("<svg "), 2)
        self.assertIn('width="63.0"', wall)
        self.assertIn('width="126.0"', wall)
        self.assertEqual(site("pages")._wall({"releases": []}), "")


class Motion(unittest.TestCase):
    """T-1615: the bench and stats charts draw themselves once when seen, only with motion allowed and JavaScript on."""

    def test_charts_carry_their_motion_and_are_whole_without_it(self):
        build = site("build")
        self.assertIn('class="viz grow-x"', build.hbars("t", "", [("a", 1), ("b", 2)]))
        rows = [{"d": "x", "v": 1}, {"d": "y", "v": 3}]
        self.assertIn('class="viz draw"', build.line("t", "", rows, "v", "d"))
        self.assertIn('pathLength="1"', build.line("t", "", rows, "v", "d"))
        css, js = read_text(os.path.join(ROOT, "site", "style.css")), read_text(os.path.join(ROOT, "site", "site.js"))
        at = css.index("T-1615")
        self.assertIn("scaleX(0)", css[at:])
        self.assertTrue(css[:at].rstrip().endswith("@media (prefers-reduced-motion: no-preference) { /*"),
                        "the motion only where it's allowed")
        self.assertLess(js.index("if (still ||"), js.index('classList.add("armed")'), "armed after the still check")


class TitleCard(ForemanTestCase):
    def test_a_proved_task_gets_its_card_and_an_unproved_one_doesnt(self):
        self.fm("init")
        tid = json.loads(self.fm("task", "new", "Totals count the <qty> of every line item", "--type", "FIX", "--tier",
                                 "S", "--ac", "it counts :: test -f proved.txt", "--step", "fix it", "--json").stdout)["id"]
        self.fm("focus", tid)
        p = self.fm("task", "card", tid, check=False)
        self.assertNotEqual(p.returncode, 0, "no proof yet")
        self.fm("task", "evidence", tid, "--step", "1", "--run", "test -f proved.txt", check=False)
        with open(os.path.join(self.repo, "proved.txt"), "w") as f:
            f.write("ok\n")
        self.fm("task", "evidence", tid, "--step", "1", "--run", "test -f proved.txt")
        out = os.path.join(self.tmp, "card.svg")
        self.fm("task", "card", tid, "--out", out)
        svg = read_text(out)
        self.assertTrue(svg.startswith("<svg "))
        self.assertIn("&lt;qty&gt;", svg)
        self.assertNotIn("<qty>", svg)
        self.assertIn("✗ before · ✓ after: test -f proved.txt", svg)
        self.assertIn("cursive", svg)


def build_esc(text):
    import html
    return html.escape(text)


def media_blocks(css, query):
    """The text of each @media block whose query contains `query`, braces matched."""
    out, at = [], css.find(query)
    while at >= 0:
        start = css.index("{", at)
        depth, i = 1, start + 1
        while depth:
            depth += {"{": 1, "}": -1}.get(css[i], 0)
            i += 1
        out.append(css[start:i])
        at = css.find(query, i)
    return out


class Landing(unittest.TestCase):
    """T-2040: the landing page types no count by hand and no inline style, every animation has a still form, and the
    reel opens on the session, not on Claude Code's folder-trust question."""

    def test_asset_urls_change_with_their_content(self):  # T-2060, T-2063: a browser keeps a file by its URL
        import hashlib
        def v(rel):
            with open(os.path.join(ROOT, "site", rel), "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()[:8]
        tags = (rf'<link rel="icon" href="(\.\./)?assets/foreman\.svg\?v={v("assets/foreman.svg")}"',
                rf'<img src="(\.\./)?assets/foreman\.svg\?v={v("assets/foreman.svg")}"',
                rf'<link rel="stylesheet" href="(\.\./)?style\.css\?v={v("style.css")}"',
                rf'<script src="(\.\./)?site\.js\?v={v("site.js")}"')
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "o")
            p = subprocess.run([sys.executable, os.path.join(ROOT, "site", "build.py"), out], capture_output=True,
                               text=True, timeout=300)
            self.assertEqual(p.returncode, 0, p.stderr)
            for rel in ("index.html", os.path.join("features", "index.html"), os.path.join("features", "benchmarks.html"),
                        os.path.join("stories", "fix.html")):
                page = read_text(os.path.join(out, rel))
                for tag in tags:
                    self.assertRegex(page, tag, rel)
            page = read_text(os.path.join(out, "genesis", "index.html"))  # T-2087: it shares style.css, not site.js
            for tag in tags[:3]:
                self.assertRegex(page, tag, "genesis")

    def test_the_code_page_is_drawn_from_todays_tui(self):  # T-2061: a committed recording goes stale
        sys.path.insert(0, os.path.join(PLUGIN, "lib"))
        import fmcodetui
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "o")
            p = subprocess.run([sys.executable, os.path.join(ROOT, "site", "build.py"), out], capture_output=True,
                               text=True, timeout=300)
            self.assertEqual(p.returncode, 0, p.stderr)
            page = read_text(os.path.join(out, "features", "code.html"))
            self.assertIn("<animate", read_text(os.path.join(out, "assets", "code-tui-tour.svg")))
        self.assertNotIn(".mp4", page, "a video recorded once shows an old fm code")
        self.assertIn('src="../assets/code-tui-tour.svg"', page)
        self.assertIn('media="(prefers-reduced-motion: reduce)" srcset="../assets/code-tui.svg"', page)
        labels = dict(fmcodetui.COMMAND_LABELS)
        for cmd in set(fmcodetui.DEFAULTS["keys"].values()):
            self.assertIn(build_esc(labels.get(cmd, cmd)), page, f"the key for {cmd} isn't on the page")

    def test_the_landing_runs_shader_cards_live(self):  # T-2062: the shaders only ran on their own page
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "o")
            p = subprocess.run([sys.executable, os.path.join(ROOT, "site", "build.py"), out], capture_output=True,
                               text=True, timeout=300)
            self.assertEqual(p.returncode, 0, p.stderr)
            page = read_text(os.path.join(out, "index.html"))
        tiles = re.findall(r'<figure class="sketch" data-shader="(sh-shader-[a-z-]+)"', page)
        self.assertEqual(len(tiles), 4, "four live tiles on the landing")
        for sid in tiles:
            self.assertIn(f'<script type="x-shader/x-fragment" id="{sid}">', page, f"{sid} has no source")
        self.assertEqual(page.count('class="fallback"'), 4, "each tile keeps its card's words for no WebGL2")
        self.assertIn("prefers-reduced-motion: reduce", page, "one still frame for a reader who asked for less motion")
        self.assertIn('href="features/shaders.html"', page)

    def test_its_counts_come_from_the_build_and_its_styles_from_the_sheet(self):
        src = read_text(os.path.join(ROOT, "site", "index.html"))
        self.assertNotRegex(src, r"\sstyle=", "a class in style.css, not an inline style")
        for stale in ("744", "2,000+", "All 15 feature", "27 areas", "Over a thousand"):
            self.assertNotIn(stale, src, "a count typed by hand goes stale; build.py fills it from the data")
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "o")
            p = subprocess.run([sys.executable, os.path.join(ROOT, "site", "build.py"), out], capture_output=True,
                               text=True, timeout=300)
            self.assertEqual(p.returncode, 0, p.stderr)
            page = read_text(os.path.join(out, "index.html"))
        with open(os.path.join(ROOT, "site", "data", "stats.json"), encoding="utf-8") as f:
            stats = json.load(f)
        build = site("build")
        self.assertNotIn("{{", page, "a count left unfilled")
        self.assertIn(build.fmt(stats["totals"]["tasks_done"]), page)
        self.assertIn(build.fmt(stats["code"]["tests"]), page)
        self.assertIn(build.fmt(sum(stats["cards"].values())) + " stack cards", page)
        self.assertIn(f"{len(stats['cards'])} areas", page)
        self.assertIn(f"All {len(site('pages').PAGES)} feature pages", page)

    def test_every_animation_runs_only_where_motion_is_allowed(self):
        css = read_text(os.path.join(ROOT, "site", "style.css"))
        allowed = "".join(media_blocks(css, "@media (prefers-reduced-motion: no-preference)"))
        uses = re.findall(r"(?m)^\s*[^{}]*\{[^}]*\banimation(?:-name|-timeline)?:\s*(?!none)[^;}]+", css)
        self.assertTrue(uses, "the page has motion")
        for use in uses:
            self.assertIn(use.strip(), allowed, "an animation outside @media (prefers-reduced-motion: no-preference)")
        self.assertRegex(allowed, r"animation-timeline:\s*view\(\)", "reveals ride the scroll, not a script")
        js = read_text(os.path.join(ROOT, "site", "site.js"))  # T-2063: script motion too waits past the still return
        guard = js.index("prefers-reduced-motion: reduce")
        for motion in ("requestAnimationFrame", "pointermove", "setTimeout(function () { li.classList"):
            self.assertGreater(js.index(motion), js.index("return;", guard), motion)

    def test_the_reel_opens_on_the_session_not_the_trust_question(self):
        spec = importlib.util.spec_from_file_location("record_live", os.path.join(ROOT, "demo", "record_live.py"))
        rec = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(rec)
        trust = "\x1b[1mDo you trust the files in this folder?\x1b[0m\n> 1. Yes, I trust this folder"
        self.assertEqual(rec.kept([(0.0, trust), (1.0, "? for shortcuts")]), [(1.0, "? for shortcuts")])
        self.assertEqual(rec.kept([[0.5, "o", trust], [1.0, "o", "x"]]), [[1.0, "o", "x"]], "--from-cast too")
        with open(os.path.join(ROOT, "demo", "live.cast"), encoding="utf-8") as f:
            self.assertNotIn("trust this folder", f.read().lower(), "the committed reel still opens on the question")
        svg = read_text(os.path.join(ROOT, "demo", "live.svg"))  # the README's reel, one <text> per word
        self.assertNotIn(">trust?<", svg, "live.svg is rendered from the cast: render it again")


class ProductLines(unittest.TestCase):
    """T-2173: Foreman is a discipline layer for coding agents; Claude Code is one surface, so no product line (README
    headline, the site's title and fine print, the marketplace entry, INSTALL.md) says it is for Claude Code alone."""

    def test_no_product_line_is_claude_code_only(self):
        for path in ("README.md", "site/index.html", "site/build.py", "site/genesis/index.html",
                     ".claude-plugin/marketplace.json", "INSTALL.md", "MASTER.md"):
            text = read_text(os.path.join(ROOT, path))
            for line in ("discipline layer for Claude Code", "Foreman for Claude Code", "community plugin for Claude Code",
                         "local Claude Code plugin", "`claude` (Claude Code) and"):
                self.assertNotIn(line, text, path)
        self.assertIn("discipline layer for coding agents", read_text(os.path.join(ROOT, "README.md")))
        self.assertIn("<span>fm code</span>", read_text(os.path.join(ROOT, "site", "index.html")))


class NoBareNulls(unittest.TestCase):
    """T-2057: stats.json's duel cases render on the benchmarks page, and no built page prints a bare empty value."""
    def test_cases_show_and_no_page_prints_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = subprocess.run([sys.executable, os.path.join(ROOT, "site", "build.py"), tmp], capture_output=True,
                               text=True, timeout=300)
            self.assertEqual(p.returncode, 0, p.stderr)
            stats = json.loads(read_text(os.path.join(ROOT, "site", "data", "stats.json")))
            names = {c["case"] for d in stats["duels"] for c in d.get("cases") or []}
            bench = os.path.join(tmp, "features", "benchmarks.html")
            if not os.path.exists(bench):
                bench = os.path.join(tmp, "features", "benchmarks", "index.html")
            page = read_text(bench)
            for n in sorted(names):
                self.assertIn(n, page, f"duel case {n} is missing from the benchmarks page")
            # a whole line (tags cut to line breaks) that is the word, or a value after a colon / in parentheses
            bare = re.compile(r"^(None|null|undefined|NaN)$|:\s*(None|null|undefined|NaN)\b|\((None|null|undefined|NaN)\)")
            for d, _, fs in os.walk(tmp):
                for fn in fs:
                    if fn.endswith(".html"):
                        html = re.sub(r"(?is)<(script|style)\b.*?</\1>", "", read_text(os.path.join(d, fn)))
                        for line in re.sub(r"(?s)<[^>]*>", "\n", html).splitlines():
                            self.assertIsNone(bare.search(line.strip()), f"{fn} prints a bare empty value: {line.strip()[:80]}")


if __name__ == "__main__":
    unittest.main()

