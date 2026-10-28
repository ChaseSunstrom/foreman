"""T-1624: the Motion Score. motion.toml (or a .json with the same schema) names each motion the UI uses: its duration
(ms, or a token from DESIGN.md's Tokens table), easing, the properties it animates and its reduced form; fm motion check
lists what's wrong with it."""
import json
import os
import re
import shutil
import subprocess

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


def module_data(text):
    """The JSON object a waapi or three module exports as motion."""
    return json.loads(text.split("export const motion = ", 1)[1].split(";\n", 1)[0])


def css_vars(text):
    """({name: value} in :root, {name: value} in the prefers-reduced-motion block) of a compiled stylesheet."""
    body, media = text.split("@media (prefers-reduced-motion: reduce)", 1)
    pairs = lambda s: dict(re.findall(r"(--motion-[\w-]+?-(?:duration|easing|transition|animation)): ([^;]+);", s))
    return pairs(body.split(":root {", 1)[1].split("}", 1)[0]), pairs(media.split("}", 1)[0])


class Compile(ForemanTestCase):
    """T-1625: fm motion compile turns one score into CSS, WAAPI or three.js parameters, every target carrying the
    score's durations and easings, and each motion's reduced form (none: rest state, never played; instant: the end
    state at once; fade: opacity only, same duration)."""
    score = Format.score
    problems = Format.problems

    def targets(self, text=GOOD, **kw):
        path = self.score(text, **kw)
        out = {to: fmmotion.compile_score(path, to) for to in fmmotion.TARGETS}
        self.assertTrue(all(problems == [] for _, problems in out.values()), out)
        return {to: t for to, (t, _) in out.items()}

    def test_every_target_carries_the_scores_durations_and_easings(self):
        got = self.targets()
        motions = fmmotion.check(os.path.join(self.repo, "motion.toml"))["motions"]
        css, _ = css_vars(got["css"])
        for m in motions:
            n = m["name"]
            with self.subTest(motion=n):
                self.assertEqual(css[f"--motion-{n}-duration"], f"{m['ms']}ms")
                self.assertEqual(css[f"--motion-{n}-easing"], m["curve"])
                self.assertEqual(css[f"--motion-{n}-transition"],
                                 ", ".join(f"{p} {m['ms']}ms {m['curve']}" for p in m["properties"]))
                self.assertEqual(css[f"--motion-{n}-animation"], f"motion-{n} {m['ms']}ms {m['curve']} backwards")
                for to in ("waapi", "three"):
                    d = module_data(got[to])[n]
                    self.assertEqual((d["duration"], d["easing"], d["properties"]), (m["ms"], m["curve"], m["properties"]))
        for to, text in got.items():
            with self.subTest(to=to):
                # a code target goes inline in a page, so no </ at all; the lab is the page (Lab checks its one </script>)
                self.assertTrue(text.isascii() and (to == "lab" or "</" not in text) and "\x1b" not in text, to)

    def test_reduced_forms_keep_their_meanings_in_every_target(self):
        got = self.targets()
        _, css = css_vars(got["css"])
        enter = "cubic-bezier(0.05, 0.7, 0.1, 1)"
        want = {"menu-enter": {"form": "fade", "duration": 220, "easing": enter, "properties": ["opacity"]},
                "row-move": {"form": "instant", "duration": 0, "easing": "cubic-bezier(0.45, 0, 0.2, 1)",
                             "properties": ["transform"]},
                "badge-pulse": {"form": "none", "duration": 0, "easing": "cubic-bezier(0.2, 0, 0, 1)", "properties": []}}
        for to in ("waapi", "three"):
            data = module_data(got[to])
            self.assertEqual({n: {k: v for k, v in m["reduced"].items() if k != "curve"} for n, m in data.items()}, want)
        self.assertEqual((css["--motion-menu-enter-duration"], css["--motion-menu-enter-transition"],
                          css["--motion-menu-enter-animation"]),
                         ("220ms", f"opacity 220ms {enter}", f"reduced-motion-menu-enter 220ms {enter} backwards"))
        self.assertIn("@keyframes reduced-motion-menu-enter {\n  from { opacity: var(--motion-menu-enter-from-opacity, 0); }",
                      got["css"])
        self.assertEqual((css["--motion-row-move-duration"], css["--motion-row-move-transition"]),
                         ("0ms", "transform 0ms cubic-bezier(0.45, 0, 0.2, 1)"))  # instant: the end state at once
        self.assertEqual((css["--motion-badge-pulse-duration"], css["--motion-badge-pulse-transition"],
                          css["--motion-badge-pulse-animation"]), ("0ms", "all 0s", "none"))  # none: never played
        # `transition: var(--motion-row-move-transition), var(--motion-badge-pulse-transition)` stays a valid list:
        # none is only valid alone there, so it would void the whole declaration
        both = ", ".join(css[f"--motion-{n}-transition"] for n in ("row-move", "badge-pulse"))
        self.assertEqual(both, "transform 0ms cubic-bezier(0.45, 0, 0.2, 1), all 0s")
        self.assertIn(':root[data-motion="reduce"]', got["css"])  # the app's setting wins, as the playbook says

    def test_the_header_label_cant_end_its_comment(self):
        for name in ("x*/a{}</*.toml", "a*", "</style>"):
            with self.subTest(name=name):
                label = fmmotion._label(name)
                self.assertNotIn("*/", label)
                self.assertNotIn("</", label)
        css = self.targets(name="a*.toml")["css"]
        self.assertEqual(css.count("*/"), 1, css[:400])  # the header's own end

    def test_names_and_properties_are_ascii(self):
        text = '[motion."café"]\nduration = 100\neasing = "linear"\nproperties = ["opacité"]\nreduced = "fade"\n'
        got = "\n".join(self.problems(text))
        self.assertIn("name 'café' must be letters", got)
        self.assertIn("property 'opacité' is not a CSS property name", got)

    def test_three_maps_steps_and_linear_to_ease_functions(self):
        text = "".join(f'[motion.m{i}]\nduration = {100 * i}\neasing = "{e}"\nproperties = ["opacity"]\nreduced = "fade"\n'
                       for i, e in enumerate(("steps(4)", "steps(3, jump-none)", "linear(0, 0.25 75%, 1)", "ease-in-out",
                                              "step-start", "linear(0, 0.5 25% 75%, 1)", "linear"), 1))
        three = self.targets(text)["three"]
        data = module_data(three)
        self.assertEqual([data[f"m{i}"]["curve"] for i in (1, 2, 3, 5)],
                         [["steps", 4, "jump-end"], ["steps", 3, "jump-none"],
                          ["linear", [[0.0, 0.0], [0.75, 0.25], [1.0, 1.0]]], ["steps", 1, "jump-start"]])
        self.assertEqual([data[f"m{i}"]["curve"] for i in (4, 6, 7)],
                         [["bezier", 0.42, 0.0, 0.58, 1.0], ["linear", [[0.0, 0.0], [0.25, 0.5], [0.75, 0.5], [1.0, 1.0]]],
                          ["linear", [[0.0, 0.0], [1.0, 1.0]]]])
        node = shutil.which("node")
        if not node:
            self.skipTest("no node to run the module's ease functions")
        mod = os.path.join(self.repo, "motion.mjs")
        with open(mod, "w") as f:
            f.write(three + '\nconst xs = [0, 0.1, 0.3, 0.5, 0.75, 0.9, 1];\nconsole.log(JSON.stringify(Object.fromEntries('
                    'Object.entries(motion).map(([n, m]) => [n, xs.map(x => Math.round(m.ease(x) * 1e4) / 1e4)]))));\n')
        p = subprocess.run([node, mod], capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 0, p.stderr)
        got = json.loads(p.stdout)
        self.assertEqual(got["m1"], [0, 0, 0.25, 0.5, 0.75, 0.75, 1])  # steps(4): jump at each quarter's end
        self.assertEqual(got["m2"], [0, 0, 0, 0.5, 1, 1, 1])  # jump-none: 0, 0.5, 1
        self.assertEqual(got["m3"], [0, 0.0333, 0.1, 0.1667, 0.25, 0.7, 1])
        self.assertEqual(got["m4"][::3], [0, 0.5, 1])  # ease-in-out is symmetric
        self.assertTrue(got["m4"][1] < 0.1 and got["m4"][5] > 0.9, got["m4"])
        self.assertEqual(got["m5"], [1, 1, 1, 1, 1, 1, 1])  # step-start: the end value from the first frame
        self.assertEqual(got["m6"], [0, 0.2, 0.5, 0.5, 0.5, 0.8, 1])
        self.assertEqual(got["m7"], [0, 0.1, 0.3, 0.5, 0.75, 0.9, 1])

    def test_waapi_play_keeps_each_reduced_form(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("no node to run the module")
        mod = os.path.join(self.repo, "motion.mjs")
        frames = '[{opacity: 0, transform: "scale(0.9)", scale: 0.5}, {opacity: 1, transform: "none", scale: 1}]'
        with open(mod, "w") as f:
            f.write(self.targets()["waapi"] + f"""
const el = {{ animate: (frames, options) => ({{ frames, options }}) }};
const run = () => ["menu-enter", "row-move", "badge-pulse"].map((n) => play(el, n, {frames}));
const full = run();
globalThis.matchMedia = () => ({{ matches: true }});
const reduce = run();
const as = (system, set) => {{  // what reduced() says for this system setting and <html data-motion>
  globalThis.matchMedia = () => ({{ matches: system }});
  globalThis.document = {{ documentElement: {{ dataset: set === undefined ? {{}} : {{ motion: set }} }} }};
  return reduced();
}};
const sets = [[true, "full"], [true, "other"], [true, ""], [false, "reduce"], [false, "other"], [true, undefined]];
const table = sets.map(([s, v]) => as(s, v));
as(true, "full");
console.log(JSON.stringify({{ full, reduce, app: run(), table }}));
""")
        p = subprocess.run([node, mod], capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 0, p.stderr)
        got = json.loads(p.stdout)
        self.assertEqual([a["options"]["duration"] for a in got["full"]], [220, 300, 300])
        self.assertEqual(got["full"][0]["frames"][0], {"opacity": 0, "transform": "scale(0.9)"})  # scale isn't listed
        self.assertEqual(got["full"][2]["frames"][1], {"scale": 1})
        fade, instant, none = got["reduce"]
        self.assertEqual((fade["options"]["duration"], fade["frames"]), (220, [{"opacity": 0}, {"opacity": 1}]))
        self.assertEqual((instant["options"]["duration"], instant["frames"][1]), (0, {"transform": "none"}))
        self.assertIsNone(none)  # never played
        self.assertEqual(got["app"], got["full"])  # <html data-motion="full"> wins over the system
        # as the CSS: reduced when the system asks unless data-motion="full", and always with data-motion="reduce"
        self.assertEqual(got["table"], [False, True, True, True, False, True])

    def test_a_score_with_problems_compiles_nothing(self):
        text, problems = fmmotion.compile_score(self.score(GOOD.replace('reduced = "none"\n', "")), "css")
        self.assertIsNone(text)
        self.assertIn("badge-pulse", problems[0]["motion"])

    def test_cli_prints_writes_and_refuses(self):
        self.score(GOOD)
        css = self.fm("motion", "compile").stdout
        self.assertIn("@keyframes motion-menu-enter", css)
        out = os.path.join(self.repo, "out", "motion.js")
        os.makedirs(os.path.dirname(out))
        self.fm("motion", "compile", "motion.toml", "--to", "waapi", "--out", out)
        with open(out) as f:
            self.assertEqual(module_data(f.read())["row-move"]["duration"], 300)
        p = self.fm("motion", "compile", "--to", "three", "--out", "motion.toml", check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("is the score", p.stderr)
        self.score(GOOD.replace('reduced = "none"\n', ""))
        p = self.fm("motion", "compile", "--out", out, check=False)
        self.assertEqual((p.returncode, p.stdout), (1, ""))
        self.assertIn("badge-pulse: no reduced form", p.stderr)
        with open(out) as f:
            self.assertIn("export const motion", f.read())  # not replaced
        p = self.fm("motion", "compile", "--json", check=False)
        self.assertEqual(p.returncode, 1)
        self.assertEqual(json.loads(p.stdout)["problems"][0]["motion"], "badge-pulse")
        for flag in (["--to", "css"], ["--out", out]):
            with self.subTest(flag=flag):
                p = self.fm("motion", "check", *flag, check=False)
                self.assertEqual(p.returncode, 2)
                self.assertIn(f"{flag[0]} is for compile", p.stderr)


class Lab(ForemanTestCase):
    """T-1626: fm motion compile --to lab is one self-contained page that plays each motion, scrubs it by drag and
    edits its duration and bezier handles into score lines to paste back."""
    score = Format.score

    def page(self, text=GOOD):
        page, problems = fmmotion.compile_score(self.score(text), "lab")
        self.assertEqual(problems, [])
        return page

    def test_the_page_carries_every_motion_as_the_score_resolves_it(self):
        page = self.page()
        self.assertTrue(page.startswith("<!doctype html>"))
        self.assertNotIn("<script src", page)  # self-contained: opens from a file, offline
        data = json.loads(re.search(r"const MOTIONS = (.*);\n", page).group(1))
        want = fmmotion.check(os.path.join(self.repo, "motion.toml"))["motions"]
        self.assertEqual([(m["name"], m["ms"], m["curve"], m["reduced"]) for m in data],
                         [(m["name"], m["ms"], m["curve"], m["reduced"]) for m in want])
        self.assertEqual(data[1]["bezier"], [0.45, 0, 0.2, 1])  # handles to drag
        for hook in ("pointerdown", "currentTime", "cubic-bezier(", "prefers-reduced-motion", "duration = "):
            self.assertIn(hook, page)

    def test_steps_and_linear_curves_get_no_handles_and_the_script_parses(self):
        page = self.page(GOOD.replace('"cubic-bezier(0.45, 0, 0.2, 1)"', '"steps(4, end)"'))
        data = json.loads(re.search(r"const MOTIONS = (.*);\n", page).group(1))
        self.assertIsNone(data[1]["bezier"])
        self.assertEqual(page.count("</script>"), 1)
        node = shutil.which("node")
        if not node:
            self.skipTest("no node to parse the page's script")
        js = os.path.join(self.repo, "lab.js")
        with open(js, "w") as f:
            f.write(re.search(r"<script>(.*)</script>", page, re.S).group(1))
        p = subprocess.run([node, "--check", js], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)

    def test_the_cli_writes_the_page_with_out(self):
        self.score(GOOD)
        self.fm("motion", "compile", "--to", "lab", "--out", "lab.html")
        with open(os.path.join(self.repo, "lab.html")) as f:
            self.assertIn("menu-enter", f.read())


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
