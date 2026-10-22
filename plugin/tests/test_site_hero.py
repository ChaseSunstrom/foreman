"""T-1609: the landing page's hero opens on an inline SVG poster of the proof chain, drawn by site/build.py from
site/data/stats.json (tasks done, evidence, proofs, commits as stations sized by their totals): the first paint, and
the still that T-1610's scene sits over."""
import html
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

from helpers import PLUGIN, read_json, read_text

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


if __name__ == "__main__":
    unittest.main()
