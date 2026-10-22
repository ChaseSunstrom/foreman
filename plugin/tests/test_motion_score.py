"""T-1624: the Motion Score. motion.toml (or a .json with the same schema) names each motion the UI uses: its duration
(ms, or a token from DESIGN.md's Tokens table), easing, the properties it animates and its reduced form; fm motion check
lists what's wrong with it."""
import json
import os

from helpers import ForemanTestCase

import fmmotion

DESIGN = """# DESIGN.md: demo

## Tokens

| Token | Kind | Light | Dark | Source |
|---|---|---|---|---|
| `--dur-enter` | duration | `220ms` |  | tokens.css:2 |
| `--dur-slow` | duration | `0.3s` |  | tokens.css:3 |
| `--ease-brand` | other | `cubic-bezier(0.2, 0, 0, 1)` |  | tokens.css:4 |
| `--brand` | colour | `#3366cc` #3366CC |  | tokens.css:5 |

## Next
"""

GOOD = """# the menu
[[motion]]
name = "menu-enter"
duration = "--dur-enter"
easing = "ease-enter"
properties = ["opacity", "transform"]
reduced = "fade"

[[motion]]
name = "row-move"
duration = 300
easing = "cubic-bezier(0.45, 0, 0.2, 1)"
properties = ["transform"]
reduced = "instant"

[[motion]]
name = "badge-pulse"
duration = "dur-slow"
easing = "--ease-brand"
properties = ["scale"]
reduced = "none"
"""


class Format(ForemanTestCase):
    def score(self, text, name="motion.toml", design=DESIGN):
        if design is not None:
            with open(os.path.join(self.repo, "DESIGN.md"), "w") as f:
                f.write(design)
        path = os.path.join(self.repo, name)
        with open(path, "w") as f:
            f.write(text)
        return path

    def problems(self, text, **kw):
        return [f"{p['motion']}: {p['problem']}" for p in fmmotion.check(self.score(text, **kw))["problems"]]

    def test_a_motion_without_a_reduced_form_fails_naming_it(self):
        text = GOOD.replace('reduced = "instant"\n', "")
        got = self.problems(text)
        self.assertEqual(len(got), 1, got)
        self.assertIn("row-move", got[0])
        self.assertIn("reduced", got[0])

    def test_a_good_score_resolves_its_tokens(self):
        got = fmmotion.check(self.score(GOOD))
        self.assertEqual(got["problems"], [])
        by = {m["name"]: m for m in got["motions"]}
        self.assertEqual([by[n]["ms"] for n in ("menu-enter", "row-move", "badge-pulse")], [220, 300, 300])
        self.assertEqual(by["menu-enter"]["curve"], "cubic-bezier(0.05, 0.7, 0.1, 1)")  # the playbook's default
        self.assertEqual(by["badge-pulse"]["curve"], "cubic-bezier(0.2, 0, 0, 1)")
        self.assertEqual(got["design"], os.path.join(self.repo, "DESIGN.md"))

    def test_each_problem_is_named(self):
        bad = GOOD.replace('"ease-enter"', '"wobbly"').replace("300\n", "2500\n").replace('"badge-pulse"', '"menu-enter"')
        bad += '[[motion]]\nname = "toast"\nduration = "--dur-toast"\neasing = "cubic-bezier(1.5, 0, 0, 1)"\n' \
               'properties = ["all"]\nreduced = "spin"\n'
        got = "\n".join(self.problems(bad))
        for want in ("menu-enter: unknown easing 'wobbly'", "row-move: duration 2500 ms is outside 0–2000",
                     "menu-enter: the name is used twice", "toast: DESIGN.md has no token '--dur-toast'",
                     "toast: easing 'cubic-bezier(1.5, 0, 0, 1)': x1 and x2 must lie in 0–1",
                     "toast: properties: list them, not all",
                     "toast: reduced form 'spin' is not none, fade or instant"):
            self.assertIn(want, got)

    def test_a_token_with_no_design_md_says_so(self):
        got = self.problems(GOOD, design=None)
        self.assertTrue(any("menu-enter" in p and "no DESIGN.md" in p for p in got), got)
        self.assertFalse(any("row-move" in p for p in got), got)

    def test_shape_slips_are_problems_not_crashes(self):
        for text, want in (('[motion.x]\nduration = 1\n', "[[motion]]"), ("", "no [[motion]]"),
                           ('title = "x"\n[[motion]]\nname = "a"\n', "unknown key 'title'"),
                           ('motion = [1]\n', "motion 1: not a table")):
            with self.subTest(text=text):
                got = "\n".join(self.problems(text))
                self.assertIn(want, got)
        got = "\n".join(self.problems('[[motion]]\nname = "a b"\nduration = true\nproperties = "opacity"\n'
                                      'reduced = "fade"\neasing = "linear"\nreduce = 1\n'))
        for want in ("motion 1: name 'a b'", "duration", "properties", "unknown key 'reduce'"):
            self.assertIn(want, got)

    def test_json_has_the_same_schema(self):
        motions = [{"name": "fade-in", "duration": 150, "easing": "ease-out", "properties": ["opacity"]}]
        got = self.problems(json.dumps({"motion": motions}), name="motion.json")
        self.assertEqual(got, ["fade-in: no reduced form (none, fade or instant)"])

    def test_unreadable_scores_raise(self):
        for text, name in (("[[motion]\n", "motion.toml"), ("{", "m.json"), ("[1]", "m.json")):
            with self.subTest(text=text), self.assertRaises(ValueError):
                fmmotion.check(self.score(text, name=name))

    def test_reads_the_table_fm_design_extract_writes(self):
        with open(os.path.join(self.repo, "tokens.css"), "w") as f:
            f.write(":root {\n  --dur-enter: 220ms;\n  --ease-brand: cubic-bezier(0.2, 0, 0, 1);\n"
                    "  --dur-slow: .3s;\n}\n")
        self.fm("design", "extract", "tokens.css")
        got = fmmotion.check(self.score(GOOD, design=None))
        self.assertEqual(got["problems"], [])
        self.assertEqual([(m["ms"], m["curve"]) for m in got["motions"]][::2],
                         [(220, "cubic-bezier(0.05, 0.7, 0.1, 1)"), (300, "cubic-bezier(0.2, 0, 0, 1)")])


class Cli(ForemanTestCase):
    def test_check_reads_motion_toml_at_the_root_and_exits_1_on_problems(self):
        with open(os.path.join(self.repo, "motion.toml"), "w") as f:
            f.write('[[motion]]\nname = "x"\nduration = 100\neasing = "linear"\nproperties = ["opacity"]\n')
        os.makedirs(os.path.join(self.repo, "src"))
        p = self.fm("motion", "check", cwd=os.path.join(self.repo, "src"), check=False)
        self.assertEqual(p.returncode, 1, p.stderr)
        self.assertIn("x: no reduced form", p.stdout)
        p = self.fm("motion", "check", "motion.toml", "--json", check=False)
        self.assertEqual(json.loads(p.stdout)["problems"][0]["motion"], "x")
        with open(os.path.join(self.repo, "motion.toml"), "a") as f:
            f.write('reduced = "fade"\n')
        self.assertIn("clean", self.fm("motion", "check").stdout)

    def test_a_missing_or_broken_score_exits_2(self):
        p = self.fm("motion", "check", check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("motion.toml", p.stderr)
        with open(os.path.join(self.repo, "motion.toml"), "w") as f:
            f.write("[[motion]\n")
        p = self.fm("motion", "check", check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("line 1", p.stderr)
