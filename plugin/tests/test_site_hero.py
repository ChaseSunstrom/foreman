"""T-1609, T-2040: the landing page's hero: a proof ledger of the four totals site/build.py reads from
site/data/stats.json, and a session drawn as text in the site's palette that site.js replays line by line (a recorded
video of a themed terminal smeared its colours). No JS or reduced motion shows the whole transcript."""
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


def build_copy(tmp, totals=None, edit_index=None, edit_stats=None):
    """Build a copy of site/ the way the workflow does, its stats.json totals updated with `totals` and its
    index.html passed through `edit_index`; the finished process."""
    shutil.copytree(os.path.join(ROOT, "site"), os.path.join(tmp, "site"), ignore=shutil.ignore_patterns("__pycache__"))
    for d in ("demo", "plugin"):
        os.symlink(os.path.join(ROOT, d), os.path.join(tmp, d))
    if totals or edit_stats:
        path = os.path.join(tmp, "site", "data", "stats.json")
        stats = read_json(path)
        stats["totals"].update(totals or {})
        (edit_stats or (lambda s: s))(stats)
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


def hero(page):
    start = page.index('class="wrap hero"')
    return page[start:page.index("<section", start)]


def ledger(page):
    """The hero's proof ledger as {label: figure}."""
    box = re.search(r'<div class="proof">.*?</dl></div>', hero(page), re.S)
    return {html.unescape(dt): html.unescape(dd) for dt, dd in re.findall(r"<dt>(.*?)</dt><dd>(.*?)</dd>", box.group(0))}


class Proof(unittest.TestCase):
    def test_the_built_hero_shows_the_real_totals_inline(self):
        with tempfile.TemporaryDirectory() as tmp:
            page = built_index(tmp)
        totals = read_json(os.path.join(ROOT, "site", "data", "stats.json"))["totals"]
        want = {label: f"{totals.get(k) or 0:,}" for k, label in build_module().STATIONS}
        self.assertEqual(ledger(page), want)
        self.assertNotIn("hero-scene", page)
        self.assertNotRegex(hero(page), r'(?:src|href)="https?:')

    def test_a_changed_stats_json_changes_the_ledger_and_zero_shows_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            got = ledger(built_index(tmp, {"tasks_done": 123456, "proofs": 0}))
        self.assertEqual((got["tasks done"], got["proofs"]), ("123,456", "0"))
        self.assertEqual(build_module().proof({}).count("<dd>0</dd>"), 4)

    def test_an_index_without_the_proof_mark_fails_the_build(self):
        mark = build_module().PROOF_MARK
        with tempfile.TemporaryDirectory() as tmp:
            r = build_copy(tmp, edit_index=lambda s: s.replace(mark, ""))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("lost the proof mark", r.stdout + r.stderr)

    def test_a_stats_json_without_the_test_count_fails_the_build(self):
        # review: the hero's "{{tests}} tests" line would have shipped as "0 tests"
        with tempfile.TemporaryDirectory() as tmp:
            r = build_copy(tmp, edit_stats=lambda s: s.pop("code", None))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("no code.tests", r.stdout + r.stderr)


class Session(unittest.TestCase):
    """T-2040: the hero's session is text, so it is crisp at any size and follows the theme."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.page = built_index(cls.tmp)
        cls.out = os.path.join(cls.tmp, "out")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_the_hero_draws_the_session_as_text_with_no_video(self):
        h = hero(self.page)
        self.assertIn('id="session"', h)
        self.assertNotIn("<video", h)
        self.assertNotIn("{{", h)
        self.assertFalse(os.path.exists(os.path.join(self.out, "hero-scene.js")))

    def test_the_pane_walks_the_eight_stations_in_order(self):
        h = hero(self.page)
        names = re.findall(r"<b>(\w+)</b>", self.page[self.page.index('id="stations"'):])[:8]
        self.assertEqual(re.findall(r"<li[^>]*>(\w+)</li>", h[h.index('class="stage"'):]), [n.lower() for n in names])
        stations = [int(s) for s in re.findall(r'class="ln[^"]*" data-s="(\d)"', h)]
        self.assertEqual(len(stations), h.count('class="ln'))  # every line names its station
        self.assertEqual(stations, sorted(stations))
        self.assertEqual((stations[0], stations[-1]), (0, 8))

    def test_only_the_live_replay_hides_lines(self):
        css = read_text(os.path.join(self.out, "style.css"))
        hiders = re.findall(r"([^{}]*\.ln[^{}]*)\{[^}]*opacity:\s*0", css)
        self.assertTrue(hiders)
        for sel in hiders:
            self.assertIn(".session.live", sel)  # no JS, no hidden transcript

    def test_the_newest_playwright_build_is_the_one_used(self):
        # review: sorted as text, a build 999 would beat 1243; with nothing on PATH the newest download runs
        from unittest import mock
        with tempfile.TemporaryDirectory() as home:
            for build in ("999", "1243", "1100", "beta"):
                d = os.path.join(home, ".cache", "ms-playwright", f"chromium_headless_shell-{build}", "chrome-headless-shell-linux64")
                os.makedirs(d)
                with open(os.path.join(d, "chrome-headless-shell"), "w") as f:
                    f.write("#!/bin/sh\n")
                os.chmod(os.path.join(d, "chrome-headless-shell"), 0o755)
            with mock.patch.dict(os.environ, {"HOME": home, "PATH": home, "FOREMAN_CHROME": ""}), \
                    mock.patch("helpers._starts", return_value=True):  # the fakes can't start; the order is under test
                self.assertIn("chromium_headless_shell-1243", headless_chrome())

    def browse(self, *flags, budget=4000):
        """The built index in a headless Chromium at 1280x1100 after `budget` ms of virtual time: the dumped DOM."""
        browser = headless_chrome()
        if not browser:
            self.skipTest("no headless Chromium (FOREMAN_CHROME, chrome-headless-shell or Playwright's download)")
        try:  # its own process group: a timeout kills the renderer children too
            p = subprocess.Popen([browser, "--headless", "--window-size=1280,1100", f"--virtual-time-budget={budget}",
                                  *flags, "--user-data-dir=" + tempfile.mkdtemp(dir=self.tmp), "--dump-dom",
                                  "file://" + os.path.join(self.out, "index.html")],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
            out, err = p.communicate(timeout=120)
        except OSError as e:
            self.skipTest(f"{browser} didn't run: {e}")
        except subprocess.TimeoutExpired:
            os.killpg(p.pid, signal.SIGKILL)
            p.communicate()
            self.fail("headless Chromium timed out after 120 s")
        if 'class="wrap hero"' not in out:  # a root sandbox, no display libs
            self.skipTest(f"{browser} printed no page: {err[-300:]}")
        return out

    def test_the_session_replays_and_reduced_motion_shows_it_whole(self):
        dom = self.browse()
        self.assertIn('class="session live"', dom)
        shown, total = len(re.findall(r'class="ln[^"]* on', dom)), dom.count('class="ln')
        self.assertTrue(0 < shown < total, (shown, total))
        self.assertIn('<li class="now">', dom)
        still = self.browse("--force-prefers-reduced-motion")
        self.assertNotIn("session live", still)
        self.assertEqual(still.count('<li class="done">'), 8)


if __name__ == "__main__":
    unittest.main()
