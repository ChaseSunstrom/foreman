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
properties = ["opacity", "transform"]
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


@unittest.skipUnless(shutil.which("node"), "no node to run the score's ease(p)")
class Sample(ForemanTestCase):
    """T-1627: samples taken under fm smoke's frozen profile, asserted against the Motion Score within tolerance."""

    def setUp(self):
        super().setUp()
        self.score = os.path.join(self.repo, "motion.toml")
        with open(self.score, "w") as f:
            f.write(SCORE)

    def test_sampled_values_within_tolerance_pass(self):
        got = fmmotion.verify(self.score, [
            frames("menu-enter", "opacity", 0, 1, [[50, 0.25], [100, 0.5], [150, 0.761]]),
            frames("menu-enter", "transform", [1, 0, 0, 1, 0, 8], [1, 0, 0, 1, 0, 0],
                   [[50, [1, 0, 0, 1, 0, 6]], [100, [1, 0, 0, 1, 0, 4.1]]])])
        self.assertEqual((got["problems"], got["drifts"], got["checked"]), ([], [], 5))
        self.assertIn("motion verify: clean, 5 sample(s)", fmmotion.report(got))

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
                                           frames("sheet-up", "color", [0, 0, 0], [255, 0, 0], [[100, [9, 0, 0]]]),
                                           {"motion": "menu-enter", "at": "x"}, "junk",
                                           frames("menu-enter", "transform", [1, 0], [1, 0, 0], [[10, [1, 0]]])])
        self.assertEqual(got["drifts"], [])
        text = " | ".join(p["problem"] for p in got["problems"])
        for want in ("not in the score", "color, which the score doesn't list", "sample 3", "sample 4",
                     "can't be compared"):
            self.assertIn(want, text)

    def test_no_browser_says_so_and_checks_only_the_score(self):
        got = fmmotion.verify(self.score, None, why="no browser: no Playwright in this checkout")
        text = fmmotion.report(got)
        self.assertIn("no browser: no Playwright in this checkout; checked the score only", text)
        self.assertEqual((got["problems"], got["checked"]), ([], 0))
        with open(self.score, "a") as f:
            f.write('[[motion]]\nname = "bad"\nduration = 100\neasing = "linear"\nproperties = ["opacity"]\n')
        self.assertIn("bad: no reduced form", fmmotion.report(fmmotion.verify(self.score, None, why="no browser")))

    def test_the_pages_sampler_writes_what_verify_reads(self):
        # smoke_web.cjs's sampleMotion against a stand-in page: a linear 200 ms motion-menu-enter whose transform ends
        # at none; what it returns must verify clean, so the two sides agree on the sample format
        js = os.path.join(self.tmp, "fake.cjs")
        with open(js, "w") as f:
            f.write("const { sampleMotion } = require(%s);\n" % json.dumps(fmsmoke.SCRIPT) + """
const a = { animationName: "motion-menu-enter", currentTime: 0, effect: { target: {}, pseudoElement: null,
  getTiming: () => ({ duration: 200, delay: 0 }), getKeyframes: () => [{ offset: 0, opacity: "0", transform: "x" }] } };
global.document = { getAnimations: () => [a, { animationName: "other", effect: a.effect }] };
global.getComputedStyle = () => ({ getPropertyValue: (p) => {
  const t = Math.min(a.currentTime / 200, 1);
  return p === "opacity" ? String(t) : t === 1 ? "none" : `matrix(1, 0, 0, 1, 0, ${8 - 8 * t})`;
} });
console.log(JSON.stringify(sampleMotion("desktop start")));
""")
        p = subprocess.run([shutil.which("node"), js], capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 0, p.stderr)
        samples = json.loads(p.stdout)
        self.assertEqual([(s["motion"], s["property"], len(s["at"])) for s in samples],
                         [("menu-enter", "opacity", 7), ("menu-enter", "transform", 7)])
        got = fmmotion.verify(self.score, samples)
        self.assertEqual((got["problems"], got["drifts"], got["checked"]), ([], [], 14))

    def test_cli_reads_samples_or_the_frozen_crawl_and_says_when_there_is_no_browser(self):
        sp = os.path.join(self.tmp, "samples.json")
        with open(sp, "w") as f:
            json.dump([frames("menu-enter", "opacity", 0, 1, [[75, 0.25]])], f)
        p = self.fm("motion", "verify", "--samples", sp, check=False)
        self.assertEqual(p.returncode, 1, p.stderr)
        self.assertIn("expected 0.375, sampled 0.25", p.stdout)
        self.fm("init")
        p = self.fm("motion", "verify", check=False, env={"FOREMAN_PLAYWRIGHT": ""})
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("no fm smoke web URL", p.stdout)
        self.fm("smoke", "set", "web", "http://127.0.0.1:8199/")
        runner = os.path.join(self.tmp, "runner.py")
        with open(runner, "w") as f:
            f.write("import json, sys\nassert sys.argv[-1] == 'frozen', sys.argv\nprint(json.dumps({'views': ['desktop "
                    "start'], 'defects': [], 'motion': " + repr([frames("menu-enter", "opacity", 0, 1, [[100, 0.5]])])
                    + "}))\n")
        p = self.fm("motion", "verify", check=False, env={"FOREMAN_SMOKE_RUNNER": f"{sys.executable} {runner}"})
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("clean, 1 sample(s)", p.stdout)


if __name__ == "__main__":
    unittest.main()
