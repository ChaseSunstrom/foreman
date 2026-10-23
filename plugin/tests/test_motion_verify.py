"""T-1628: the afterglow rule of fm design lint: a state change with no transition reads as a glitch. T-1627: fm motion
verify, sampled frames asserted against the Motion Score."""
import json
import os
import shutil
import subprocess
import sys
import unittest

from helpers import ForemanTestCase

import fmdesign
import fmmotion
import fmsmoke

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "design", "afterglow")


class Afterglow(ForemanTestCase):
    def found(self, name):
        return [f["line"] for f in fmdesign.lint([os.path.join(FIX, name)]) if f["rule"] == "afterglow"]

    def test_hover_colour_change_with_no_transition_is_flagged(self):
        self.assertEqual(self.found("slop.css"), [2, 4, 5, 6, 9, 11, 13, 14, 15, 17])
        msg = fmdesign.lint([os.path.join(FIX, "slop.css")])[0]["detail"]
        self.assertIn("design-lint: allow afterglow", msg)

    def test_transition_animation_or_reduced_motion_is_clean(self):
        self.assertEqual(self.found("crafted.css"), [])

    def test_a_duration_token_counts_as_a_transition(self):
        # T-1707: the web template times its button with var(--dur-quick), as the lint itself asks; a 0s one still flags
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t.css")
            with open(p, "w") as f:
                f.write(".b { transition: transform var(--dur-quick) var(--ease-out); }\n"
                        ".b:hover { transform: translateY(-1px); }\n"
                        ".c { transition: color 0s; }\n.c:hover { color: red; }\n")
            self.assertEqual([x["line"] for x in fmdesign.lint([p]) if x["rule"] == "afterglow"], [4])

    def test_an_ancestor_or_descendant_state_matches_the_element_that_moves(self):
        # T-1707: the looks gallery's false findings; a transition only on a different element still flags
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t.css")
            with open(p, "w") as f:
                f.write(".k .mark { transition: background-color 120ms; }\n"
                        ".k .tile:hover .mark { background: red; }\n"
                        ".t button { transition: background-color 120ms; }\n"
                        ".t [aria-pressed=\"true\"] { background: red; }\n"
                        ".x .b { transition: color 120ms; }\n"
                        ".b:hover { color: red; }\n")
            self.assertEqual([x["line"] for x in fmdesign.lint([p]) if x["rule"] == "afterglow"], [6])


SCORE = """[[motion]]
name = "menu-enter"
duration = 200
easing = "linear"
properties = ["opacity", "transform", "color"]
reduced = "fade"

[[motion]]
name = "sheet-up"
duration = 200
easing = "ease-enter"
properties = ["opacity"]
reduced = "instant"
"""


def frames(motion, prop, frm, to, at, where="desktop start"):
    return {"motion": motion, "property": prop, "where": where, "from": frm, "to": to, "at": at}


needs_node = unittest.skipUnless(shutil.which("node"), "no node to run the score's ease(p)")

FAKE_PAGE = """
// a stand-in page: motion-menu-enter, linear over 200 ms and repeating forever, its transform ending at none; a
// reduced-motion form and another animation it must skip; one whose keyframes throw
const timing = { duration: 200, delay: 0, iterations: Infinity, direction: "normal", fill: "none" };
const effect = { target: {}, pseudoElement: null, getTiming: () => ({ ...timing }),
  updateTiming: (t) => Object.assign(timing, t), getKeyframes: () => [{ offset: 0, opacity: "0", transform: "x" }] };
const a = { animationName: "motion-menu-enter", currentTime: 0, effect };
const broken = { animationName: "motion-sheet-up", effect: { ...effect, getKeyframes: () => { throw new Error("gone"); } } };
global.document = { getAnimations: () => [a, { animationName: "reduced-motion-menu-enter", effect },
                                          { animationName: "other", effect }, broken] };
global.getComputedStyle = () => ({ getPropertyValue: (p) => {
  const t = timing.iterations === 1 ? Math.min(a.currentTime / 200, 1) : (a.currentTime % 200) / 200;
  return p === "opacity" ? String(t) : t === 1 ? "none" : `matrix(1, 0, 0, 1, 0, ${8 - 8 * t})`;
} });
const got = sampleMotion("desktop start");
console.log(JSON.stringify({ ...got, iterations: String(timing.iterations), fill: timing.fill, at: a.currentTime }));
"""


class Sample(ForemanTestCase):
    """T-1627: samples taken under fm smoke's frozen profile, asserted against the Motion Score within tolerance."""

    def setUp(self):
        super().setUp()
        self.score = os.path.join(self.repo, "motion.toml")
        with open(self.score, "w") as f:
            f.write(SCORE)

    @needs_node
    def test_sampled_values_within_tolerance_pass(self):
        got = fmmotion.verify(self.score, [
            frames("menu-enter", "opacity", 0, 1, [[50, 0.25], [100, 0.5], [150, 0.761]]),
            frames("menu-enter", "transform", [1, 0, 0, 1, 0, 8], [1, 0, 0, 1, 0, 0],
                   [[50, [1, 0, 0, 1, 0, 6]], [100, [1, 0, 0, 1, 0, 4.1]]])])
        self.assertEqual((got["problems"], got["drifts"], got["checked"]), ([], [], 5))
        self.assertIn("motion verify: clean, 5 sample(s)", fmmotion.report(got))

    @needs_node
    def test_a_changed_timing_shows_in_the_diff(self):
        # the CSS ran menu-enter over 300 ms, not the score's 200: at 75 ms it is a quarter in, not three eighths
        got = fmmotion.verify(self.score, [frames("menu-enter", "opacity", 0, 1, [[75, 0.25], [150, 0.5]]),
                                           frames("sheet-up", "opacity", 0, 1, [[100, 0.5]])])
        self.assertEqual([(d["motion"], d["property"], d["ms"]) for d in got["drifts"]],
                         [("menu-enter", "opacity", 75), ("menu-enter", "opacity", 150), ("sheet-up", "opacity", 100)])
        text = fmmotion.report(got)
        self.assertIn("menu-enter opacity at 75 ms (desktop start): expected 0.375, sampled 0.25 (tolerance ±0.02)",
                      text)
        self.assertIn("sheet-up opacity at 100 ms", text)  # ease-enter is far past half way at half time
        self.assertIn("3 drift(s)", text)

    def test_unknown_motions_unlisted_properties_and_bad_samples_are_problems(self):
        got = fmmotion.verify(self.score, [frames("ghost", "opacity", 0, 1, [[10, 0.1]]),
                                           frames("sheet-up", "transform", [0], [1], [[100, [9]]]),
                                           {"motion": "menu-enter", "at": "x"}, "junk",
                                           frames("menu-enter", "opacity", 0, 1, [[10, "half"]])])
        self.assertEqual((got["drifts"], got["checked"]), ([], 0))
        text = " | ".join(p["problem"] for p in got["problems"])
        for want in ("not in the score", "transform, which the score doesn't list", "sample 3", "sample 4",
                     "sample 5: opacity's values aren't numbers"):
            self.assertIn(want, text)

    def test_colours_rotations_and_mismatched_values_are_noted_not_failed(self):
        # a rotation's matrix and a colour don't move linearly between their ends: comparing them would flag good CSS
        got = fmmotion.verify(self.score, [
            frames("menu-enter", "transform", [1, 0, 0, 1, 0, 0], [0, 1, -1, 0, 0, 0],
                   [[100, [0.707, 0.707, -0.707, 0.707, 0, 0]]]),
            frames("menu-enter", "color", [0, 0, 0], [255, 0, 0, 0.5], [[100, [128, 0, 0, 0.7]]]),
            frames("menu-enter", "color", [0, 0, 0], [255, 0, 0], [[100, [128, 0, 0]]], where="phone start"),
            frames("menu-enter", "transform", [1, 0, 0, 1, 0, 8], [1, 0, 0, 1, 0, 0, 0], [[100, [1, 0]]])])
        self.assertEqual((got["problems"], got["drifts"], got["checked"]), ([], [], 0))
        self.assertEqual(len(got["notes"]), 2)  # one per motion and property
        text = fmmotion.report(got)
        self.assertIn("menu-enter transform: not comparable", text)
        self.assertIn("menu-enter color: not comparable", text)
        self.assertIn("nothing checked", text)

    def test_no_browser_says_so_and_checks_only_the_score(self):
        got = fmmotion.verify(self.score, None, why="no browser: no Playwright in this checkout")
        text = fmmotion.report(got)
        self.assertIn("no browser: no Playwright in this checkout; checked the score only", text)
        self.assertEqual((got["problems"], got["checked"]), ([], 0))
        with open(self.score, "a") as f:
            f.write('[[motion]]\nname = "bad"\nduration = 100\neasing = "linear"\nproperties = ["opacity"]\n')
        self.assertIn("bad: no reduced form", fmmotion.report(fmmotion.verify(self.score, None, why="no browser")))

    @needs_node
    def test_the_pages_sampler_writes_what_verify_reads(self):
        # smoke_web.cjs's sampleMotion against FAKE_PAGE: its end is read as one iteration (an infinite one seeked to
        # 200 ms is back at its start), its timing put back, and what it returns verifies clean
        js = os.path.join(self.tmp, "fake.cjs")
        with open(js, "w") as f:
            f.write("const { sampleMotion } = require(%s);\n" % json.dumps(fmsmoke.SCRIPT) + FAKE_PAGE)
        p = subprocess.run([shutil.which("node"), js], capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        self.assertEqual([(s["motion"], s["property"], len(s["at"])) for s in out["samples"]],
                         [("menu-enter", "opacity", 7), ("menu-enter", "transform", 7)])
        self.assertEqual((out["iterations"], out["fill"], out["at"]), ("Infinity", "none", 0))
        self.assertEqual(len(out["notes"]), 1)
        self.assertIn("motion-sheet-up: not sampled: gone", out["notes"][0])
        got = fmmotion.verify(self.score, out["samples"])
        self.assertEqual((got["problems"], got["drifts"], got["checked"]), ([], [], 14))

    def test_cli_with_no_url_or_no_playwright_says_so_and_checks_the_score(self):
        self.fm("init")
        p = self.fm("motion", "verify", check=False, env={"FOREMAN_PLAYWRIGHT": ""})
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("no fm smoke web URL", p.stdout)
        self.fm("smoke", "set", "web", "http://127.0.0.1:8199/")
        p = self.fm("motion", "verify", check=False, env={"FOREMAN_PLAYWRIGHT": ""})
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("no browser: no Playwright", p.stdout)
        self.assertIn("checked the score only: clean", p.stdout)

    @needs_node
    def test_cli_reads_samples_or_the_frozen_crawl(self):
        sp = os.path.join(self.tmp, "samples.json")
        with open(sp, "w") as f:
            json.dump([frames("menu-enter", "opacity", 0, 1, [[75, 0.25]])], f)
        p = self.fm("motion", "verify", "--samples", sp, check=False)
        self.assertEqual(p.returncode, 1, p.stderr)
        self.assertIn("expected 0.375, sampled 0.25", p.stdout)
        self.fm("init")
        self.fm("smoke", "set", "web", "http://127.0.0.1:8199/")
        runner = os.path.join(self.tmp, "runner.py")
        with open(runner, "w") as f:
            f.write("import json, sys\nassert sys.argv[-1] == 'frozen', sys.argv\nprint(json.dumps({'views': ['desktop "
                    "start'], 'defects': [], 'motion': " + repr([frames("menu-enter", "opacity", 0, 1, [[100, 0.5]])])
                    + ", 'motion_notes': ['desktop start: sampled the first 50 of 70 animations']}))\n")
        env = {"FOREMAN_SMOKE_RUNNER": f"{sys.executable} {runner}"}
        p = self.fm("motion", "verify", check=False, env=env)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("clean, 1 sample(s)", p.stdout)
        self.assertIn("sampled the first 50 of 70 animations", p.stdout)
        # fm smoke's own --json keeps its shape: the samples are verify's, not the gate's
        out = json.loads(self.fm("smoke", "--profile", "frozen", "--json", env=env, check=False).stdout)
        self.assertEqual(out["profiles"][0]["views"], ["desktop start"])
        self.assertNotIn("motion", json.dumps(out))


if __name__ == "__main__":
    unittest.main()
