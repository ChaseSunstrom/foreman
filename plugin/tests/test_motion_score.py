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
CURVE_ENTER = "cubic-bezier(0.05, 0.7, 0.1, 1)"

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
        for text, want in (('motion = "x"\n', "[[motion]] entries or [motion.NAME] tables"), ("", "no motions"),
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
        for text, name in (("[[motion]\n", "motion.toml"), ("{", "m.json"), ("[1]", "m.json"),
                           ("[" * 100000 + "]" * 100000, "deep.json")):
            with self.subTest(text=text[:20]), self.assertRaises(ValueError):
                fmmotion.check(self.score(text, name=name))
        fifo, big, latin = (os.path.join(self.repo, n) for n in ("fifo.toml", "big.toml", "latin.toml"))
        os.mkfifo(fifo)  # read with O_NONBLOCK: refused, never waited on
        with open(big, "w") as f:
            f.write("#" * 1_000_001)
        with open(latin, "wb") as f:
            f.write(b'[[motion]]\nname = "caf\xe9"\n')
        for path, want in ((fifo, "not a regular file"), (big, "over 1000 KB"), (latin, "not UTF-8")):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, want):
                fmmotion.check(path)

    def test_named_tables_work_like_entries(self):
        text = ('[motion.menu-enter]\nduration = 220\neasing = " Ease-Out "\nproperties = ["opacity"]\nreduced = "none"\n'
                '[motion.row]\nname = "other"\nduration = 100\neasing = "linear"\nproperties = ["opacity"]\n'
                'reduced = "fade"\n')
        got = fmmotion.check(self.score(text))
        self.assertEqual([(m["name"], m["curve"]) for m in got["motions"]], [("menu-enter", "ease-out"), ("row", "linear")])
        self.assertEqual([f"{p['motion']}: {p['problem']}" for p in got["problems"]],
                         ["row: name 'other' differs from its table key"])

    def test_durations_say_what_they_mean(self):
        for dur, want in (("0.3", "bare numbers are ms; write '0.3s'"), ("5", "bare numbers are ms; write '5s'"),
                          ('"220"', "duration '220' has no unit"), ('"-5ms"', "duration '-5ms' is negative"),
                          ("0", None), ("10", None), ('"0.25s"', None), ('" 90 ms "', None)):
            text = f'[motion.a]\nduration = {dur}\neasing = "linear"\nproperties = ["opacity"]\nreduced = "fade"\n'
            with self.subTest(dur=dur):
                got = "\n".join(self.problems(text))
                if want:
                    self.assertIn(want, got)
                else:
                    self.assertEqual(got, "")

    def test_easings_take_steps_linear_and_any_case(self):
        good = {"steps(4)": "steps(4)", "STEPS( 3 , jump-none )": "steps(3, jump-none)", "  EASE-IN-OUT ": "ease-in-out",
                "Cubic-Bezier(0.2, 0, 0, 1)": "cubic-bezier(0.2, 0, 0, 1)", "EASE-ENTER": CURVE_ENTER,
                "linear(0, 0.25 75%, 1)": "linear(0, 0.25 75%, 1)", "linear(0,0.5 25% 75%,1)": "linear(0, 0.5 25% 75%, 1)"}
        bad = ["steps(0)", "steps(1, jump-none)", "steps(2, sideways)", "linear(1)", "linear(0, 1",
               "linear(" + "0, " * 200 + "1)", "linear(0, 1 50% 60% 70%)"]
        for easing in [*good, *bad]:
            text = f'[motion.a]\nduration = 100\neasing = "{easing}"\nproperties = ["opacity"]\nreduced = "fade"\n'
            with self.subTest(easing=easing):
                got = fmmotion.check(self.score(text))
                if easing in good:
                    self.assertEqual((got["problems"], got["motions"][0]["curve"]), ([], good[easing]))
                else:
                    self.assertIn("easing", got["problems"][0]["problem"])

    def test_a_hand_written_value_table_and_a_second_table_are_read(self):
        extra = ("Hand-written:\n\n| token | Value | Job |\n|:--|--:|---|\n| `--dur-tap` | 90 ms | press |\n"
                 "| --ease-soft | `linear(0, 0.5 50%, 1)` | settle |\n\n## Next")
        text = '[motion.tap]\nduration = "--dur-tap"\neasing = "--ease-soft"\nproperties = ["-webkit-transform"]\n' \
               'reduced = "instant"\n[motion.in]\nduration = "--dur-enter"\neasing = "linear"\nproperties = ["opacity"]\n' \
               'reduced = "fade"\n'
        for design in (DESIGN.replace("## Next", extra), DESIGN.replace("## Next", extra).replace("## Tokens", "## TOKENS")):
            with self.subTest(design=design[:30]):
                got = fmmotion.check(self.score(text, design=design))
                self.assertEqual(got["problems"], [])
                self.assertEqual([(m["ms"], m["curve"]) for m in got["motions"]],
                                 [(90, "linear(0, 0.5 50%, 1)"), (220, "linear")])

    def test_a_table_without_a_value_column_is_named(self):
        design = "# D\n\n## Tokens\n\n| Token | Job |\n|---|---|\n| `--dur-tap` | press |\n"
        got = "\n".join(self.problems('[motion.tap]\nduration = "--dur-tap"\neasing = "linear"\nproperties = ["opacity"]\n'
                                      'reduced = "fade"\n', design=design))
        self.assertIn("tap: duration '--dur-tap': DESIGN.md's Tokens table at line 5 has no Light or Value column", got)

    def test_a_truncated_token_says_so(self):
        design = DESIGN.replace("| `--brand`", "| `--ease-long` | other | `linear(0, 0.1, 0.2, 0.3, 0.4, 0.5…` |  | t:6 |\n"
                                               "| `--dur-cut` | duration | `12…` |  | t:7 |\n| `--brand`")
        got = self.problems('[motion.a]\nduration = "--dur-cut"\neasing = "--ease-long"\nproperties = ["opacity"]\n'
                            'reduced = "fade"\n', design=design)
        self.assertEqual(len(got), 2, got)
        self.assertTrue(all("truncated by fm design extract" in p for p in got), got)

    def test_extract_keeps_long_curves_whole(self):
        curve = "linear(0, 0.009, 0.035 2.1%, 0.141, 0.281 6.7%, 0.723 12.9%, 0.938 16.7%, 1.017, 1.077, 1.121, 1)"
        with open(os.path.join(self.repo, "tokens.css"), "w") as f:
            f.write(f":root {{\n  --ease-spring: {curve};\n}}\n")
        self.fm("design", "extract", "tokens.css")
        got = fmmotion.check(self.score('[motion.a]\nduration = 300\neasing = "--ease-spring"\nproperties = ["opacity"]\n'
                                        'reduced = "fade"\n', design=None))
        self.assertEqual((got["problems"], got["motions"][0]["curve"]), ([], curve))

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

    def test_escape_sequences_never_reach_the_terminal(self):
        with open(os.path.join(self.repo, "DESIGN.md"), "w") as f:
            f.write("## Tokens\n\n| Token | Value |\n|---|---|\n| --dur-x | \x1b[2J |\n| --ease-x | \x1b[31m… |\n")
        with open(os.path.join(self.repo, "motion.toml"), "w") as f:
            f.write('[[motion]]\nname = "\\u001b[2Jx"\nduration = "\\u001b]0;t\\u0007"\neasing = "\\u001b[31m"\n'
                    'properties = ["\\u001b[1m"]\nreduced = "\\u001b"\n"\\u001bkey" = 1\n'
                    '[[motion]]\nname = "y"\nduration = "--dur-x"\neasing = "--ease-x"\nproperties = ["opacity"]\n'
                    'reduced = "fade"\n')
        p = self.fm("motion", "check", check=False)
        self.assertEqual(p.returncode, 1, p.stderr)
        self.assertIn("y: duration token '--dur-x' is '\\x1b[2J'", p.stdout)
        self.assertNotIn("\x1b", p.stdout + p.stderr)

    def test_a_missing_or_broken_score_exits_2(self):
        p = self.fm("motion", "check", check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("motion.toml", p.stderr)
        with open(os.path.join(self.repo, "motion.toml"), "w") as f:
            f.write("[[motion]\n")
        p = self.fm("motion", "check", check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("line 1", p.stderr)
