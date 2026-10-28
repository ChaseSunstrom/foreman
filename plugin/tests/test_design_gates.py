"""T-1645: fm design check: design gates a project opts into in DESIGN.md, advisory unless marked blocking; the first is
the executable brief: the Knobs' colours, type families and durations, and any must: line, found in the UI code."""
import json
import os
import subprocess
import sys
import unittest

from helpers import FM, ForemanTestCase

import fmdesign

DESIGN = """# DESIGN.md: Kilnroom

## Direction
Field guide, audacity bold.
- must: prefers-reduced-motion

## Knobs
- Type: "Fraunces" for headings, "Inter Tight" for text; base 1rem.
- Colour: paper #F3ECE0: background; ink #2B2420: text; iron #8C3B23: errors only.
- Motion: 200 ms ease-out on booking confirmation; under reduced motion the change is instant.

## Gates
- brief: {mode}
"""
CSS = """:root { --paper: #f3ece0; --ink: #2B2420; }
h1 { font-family: "Fraunces", serif; }
body { font-family: 'Inter Tight', sans-serif; transition: color 200ms ease-out; }
@media (prefers-reduced-motion: reduce) { * { transition: none; } }
"""


class Brief(ForemanTestCase):
    def project(self, mode="advisory", css=CSS):
        root = os.path.join(self.tmp, "site")
        os.makedirs(os.path.join(root, "src"), exist_ok=True)
        with open(os.path.join(root, "DESIGN.md"), "w") as f:
            f.write(DESIGN.format(mode=mode))
        with open(os.path.join(root, "src", "app.css"), "w") as f:
            f.write(css)
        return root

    def check(self, root, *a):
        return subprocess.run([sys.executable, FM, "design", "check", root, *a], capture_output=True, text=True,
                              cwd=root)

    def test_the_brief_gate_reports_each_must_have_with_a_reason(self):
        got = fmdesign.check_gates(self.project())
        brief = got["gates"][0]
        self.assertEqual((brief["gate"], brief["mode"]), ("brief", "advisory"))
        by = {m["must"]: m for m in brief["musts"]}
        self.assertTrue(by["colour #F3ECE0"]["pass"], "found case-blind")
        self.assertFalse(by["colour #8C3B23"]["pass"])
        self.assertIn("not in", by["colour #8C3B23"]["why"])
        self.assertTrue(by["font Fraunces"]["pass"] and by["font Inter Tight"]["pass"])
        self.assertTrue(by["duration 200ms"]["pass"])
        self.assertTrue(by["has prefers-reduced-motion"]["pass"])
        self.assertIn("src/app.css", by["font Fraunces"]["why"])

    def test_advisory_exits_0_with_its_findings_and_blocking_exits_1(self):
        p = self.check(self.project("advisory"))
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("✗ colour #8C3B23", p.stdout)
        self.assertIn("advisory", p.stdout)
        p = self.check(self.project("blocking"))
        self.assertEqual(p.returncode, 1)
        p = self.check(self.project("blocking", CSS + ".err { color: #8c3b23; }\n"))
        self.assertEqual(p.returncode, 0, p.stdout)

    def test_no_gates_section_means_nothing_is_checked(self):
        root = self.project()
        with open(os.path.join(root, "DESIGN.md")) as f:
            text = f.read().split("## Gates")[0]
        with open(os.path.join(root, "DESIGN.md"), "w") as f:
            f.write(text)
        p = self.check(root, "--json")
        self.assertEqual(p.returncode, 0)
        self.assertEqual(json.loads(p.stdout)["gates"], [])
        self.assertIn("no design gates", self.check(root).stdout)

    def test_design_md_text_reaches_the_terminal_cleaned(self):
        root = self.project()
        with open(os.path.join(root, "DESIGN.md")) as f:
            text = f.read().replace("- must: prefers-reduced-motion", "- must: evil\x1b]0;x\x07‮")
        with open(os.path.join(root, "DESIGN.md"), "w") as f:
            f.write(text)
        out = self.check(root).stdout
        self.assertNotIn("\x1b", out)
        self.assertNotIn("‮", out)

    def test_the_other_actions_still_need_their_argument(self):
        p = subprocess.run([sys.executable, FM, "design", "lint"], capture_output=True, text=True, cwd=self.tmp)
        self.assertEqual(p.returncode, 2)
        self.assertIn("needs an argument", p.stderr)

    def test_an_unknown_gate_or_mode_is_a_finding_not_a_crash(self):
        root = self.project("strict")
        with open(os.path.join(root, "DESIGN.md"), "a") as f:
            f.write("- vibes: blocking\n")
        p = self.check(root)
        self.assertEqual(p.returncode, 0)  # an unknown mode reads as advisory, and says so
        self.assertIn("unknown mode 'strict'", p.stdout)
        self.assertIn("unknown gate 'vibes'", p.stdout)


class Trial(ForemanTestCase):
    """T-1669: a gate on trial runs advisory and counts its would-blocks; it blocks once 10 are logged with under 10%
    marked wrong (fm design check --wrong GATE), and the same rule puts it back."""
    TAIL = "brief (trial: {acts}; {n} would-block{s}, {w} overridden; blocks after 10 at under 10%)"

    def setUp(self):
        super().setUp()
        self.fm("init")
        self.n = 0
        with open(os.path.join(self.repo, "DESIGN.md"), "w") as f:
            f.write(DESIGN.format(mode="trial"))
        self.change()

    def change(self):
        """New UI code that still misses the iron colour: a new would-block."""
        self.n += 1
        os.makedirs(os.path.join(self.repo, "src"), exist_ok=True)
        with open(os.path.join(self.repo, "src", "app.css"), "w") as f:
            f.write(CSS + f"/* edit {self.n} */\n")

    def check(self, *a):
        return self.fm("design", "check", self.repo, *a, check=False)

    def line(self, acts, n, w):
        return self.TAIL.format(acts=acts, n=n, s="" if n == 1 else "s", w=w)

    def test_a_trial_gate_is_advisory_and_shows_its_rate(self):
        p = self.check()
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn(self.line("advisory", 1, 0), p.stdout)
        self.assertIn("✗ colour #8C3B23", p.stdout)
        self.assertIn(self.line("advisory", 1, 0), self.check().stdout, "an unchanged rerun adds no would-block")

    def test_ten_would_blocks_block_and_a_wrong_one_demotes(self):
        for _ in range(9):
            self.assertEqual(self.check().returncode, 0)
            self.change()
        p = self.check()
        self.assertEqual(p.returncode, 1, p.stdout)
        self.assertIn(self.line("blocking", 10, 0), p.stdout)
        p = self.check("--wrong", "brief", "--why", "iron is for errors; there are none yet")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("advisory", p.stdout)
        p = self.check()
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertIn(self.line("advisory", 10, 1), p.stdout)

    def test_wrong_needs_a_would_block_to_mark(self):
        with open(os.path.join(self.repo, "src", "app.css"), "a") as f:
            f.write(".err { color: #8c3b23; }\n")
        self.assertEqual(self.check().returncode, 0)
        p = self.check("--wrong", "brief")
        self.assertEqual(p.returncode, 1)
        self.assertIn("no would-block", p.stderr)

    def test_outside_a_project_a_trial_stays_advisory_and_says_so(self):
        root = os.path.join(self.tmp, "site")
        os.makedirs(os.path.join(root, "src"))
        with open(os.path.join(root, "DESIGN.md"), "w") as f:
            f.write(DESIGN.format(mode="trial"))
        with open(os.path.join(root, "src", "app.css"), "w") as f:
            f.write(CSS)
        p = self.fm("design", "check", root, check=False, cwd=root)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("no Foreman project", p.stdout)


class Audit(ForemanTestCase):
    """T-1646: the a11y gate (contrast pairs, a reduced-motion path, focus styles) and the debt sweep (untokened
    literals per file under a budget), both over the lint's own parse."""

    def project(self, gates, files):
        root = os.path.join(self.tmp, "site")
        os.makedirs(os.path.join(root, "src"), exist_ok=True)
        with open(os.path.join(root, "DESIGN.md"), "w") as f:
            f.write("# DESIGN.md\n\n## Gates\n" + "".join(f"- {g}\n" for g in gates))
        for name, text in files.items():
            with open(os.path.join(root, "src", name), "w") as f:
                f.write(text)
        return root

    def gate(self, root, name):
        got = fmdesign.check_gates(root)
        return next(g for g in got["gates"] if g["gate"] == name), got

    def musts(self, root, name):
        return {m["must"]: m for m in self.gate(root, name)[0]["musts"]}

    def test_the_audit_flags_a_missing_reduced_motion_path(self):
        moving = ".card { transition: transform 200ms ease-out; }\n"
        by = self.musts(self.project(["a11y: advisory"], {"app.css": moving}), "a11y")
        self.assertFalse(by["reduced motion"]["pass"])
        self.assertIn("src/app.css:1", by["reduced motion"]["why"])
        still = moving + "@media (prefers-reduced-motion: reduce) { .card { transition: none; } }\n"
        by = self.musts(self.project(["a11y: advisory"], {"app.css": still}), "a11y")
        self.assertTrue(by["reduced motion"]["pass"])

    def test_contrast_pairs_come_from_the_project_tokens(self):
        css = ":root { --text: #777777; --surface: #ffffff; }\n"
        by = self.musts(self.project(["a11y: blocking"], {"tokens.css": css}), "a11y")
        self.assertFalse(by["contrast"]["pass"])
        self.assertIn("text/surface", by["contrast"]["why"])
        css = ":root { --text: #111111; --surface: #ffffff; }\n"
        by = self.musts(self.project(["a11y: blocking"], {"tokens.css": css}), "a11y")
        self.assertTrue(by["contrast"]["pass"], by["contrast"]["why"])
        _, got = self.gate(self.project(["a11y: advisory"], {"tokens.css": "a { color: red; }\n"}), "a11y")
        self.assertTrue(any("contrast" in n for n in got["notes"]), "no role tokens: said, not a silent pass")

    def test_interactive_elements_need_a_focus_style(self):
        page = "<button>Book</button>\n"
        by = self.musts(self.project(["a11y: advisory"], {"index.html": page}), "a11y")
        self.assertFalse(by["focus styles"]["pass"])
        killed = page + "<style>button:focus { outline: none; }</style>\n"
        by = self.musts(self.project(["a11y: advisory"], {"index.html": killed}), "a11y")
        self.assertFalse(by["focus styles"]["pass"], "outline: none alone is no focus style")
        shown = page + "<style>button:focus-visible { outline: 2px solid var(--accent); }</style>\n"
        by = self.musts(self.project(["a11y: advisory"], {"index.html": shown}), "a11y")
        self.assertTrue(by["focus styles"]["pass"])
        tw = '<button class="focus-visible:ring-2">Book</button>\n'
        by = self.musts(self.project(["a11y: advisory"], {"index.html": tw}), "a11y")
        self.assertTrue(by["focus styles"]["pass"], "a Tailwind focus-visible: variant counts")

    def test_shadcn_tokens_are_roles_and_a_blocking_audit_never_passes_unchecked(self):
        css = (":root { --background: #ffffff; --foreground: #111111; --primary: #2563eb; "
               "--primary-foreground: #ffffff; --muted-foreground: #999999; --accent: #f4f4f5; "
               "--accent-foreground: #18181b; --border: #e4e4e7; }\n")
        by = self.musts(self.project(["a11y: advisory"], {"tokens.css": css}), "a11y")
        self.assertFalse(by["contrast"]["pass"])
        self.assertIn("muted-foreground/background", by["contrast"]["why"])
        self.assertNotIn("accent/", by["contrast"]["why"], "shadcn's --accent is a surface, not a text colour")
        self.assertNotIn("border/", by["contrast"]["why"])
        css = ":root { --text: #111111; --surface: #ffffff; --text-muted: something(1) }\n"
        by = self.musts(self.project(["a11y: advisory"], {"tokens.css": css}), "a11y")
        self.assertIn("1 pair(s) skipped", by["contrast"]["why"])
        root = self.project(["a11y: blocking"], {"tokens.css": "a { color: red; }\n"})
        by = self.musts(root, "a11y")
        self.assertFalse(by["contrast"]["pass"], "blocking with no pair checked fails")
        self.assertIn("not checked", by["contrast"]["why"])
        p = subprocess.run([sys.executable, FM, "design", "check", root], capture_output=True, text=True, cwd=root)
        self.assertEqual(p.returncode, 1, p.stdout)

    def test_a_dark_theme_failure_flashes_and_missing_alt_are_musts(self):
        css = (":root { --text: #111111; --surface: #ffffff; }\n"
               ".dark { --text: #333333; --surface: #222222; }\n")
        by = self.musts(self.project(["a11y: advisory"], {"tokens.css": css}), "a11y")
        self.assertFalse(by["contrast"]["pass"])
        self.assertIn("(dark)", by["contrast"]["why"])
        page = ('<img src="a.png">\n<style>@keyframes blink { 50% { opacity: 0; } }\n'
                ".x { animation: blink .1s infinite; }</style>\n")
        by = self.musts(self.project(["a11y: advisory"], {"tokens.css": "", "index.html": page}), "a11y")
        self.assertFalse(by["no fast flashes"]["pass"])
        self.assertFalse(by["img alt text"]["pass"])
        self.assertIn("src/index.html:1", by["img alt text"]["why"])

    def test_focus_within_and_not_focus_visible_are_no_focus_style(self):
        for css in ("form:focus-within { background: #eee; }", ":focus:not(:focus-visible) { color: red; }",
                    "button:focus { z-index: 2; }", "button:focus-visible { outline: 2px solid transparent; }"):
            page = f"<button>Book</button>\n<style>{css}</style>\n"
            by = self.musts(self.project(["a11y: advisory"], {"index.html": page}), "a11y")
            self.assertFalse(by["focus styles"]["pass"], css)
        for cls in ("focus:outline-hidden", "focus-visible:shadow-none", "focus:ring-transparent", "focus-within:ring-2"):
            page = f'<button class="{cls}">Book</button>\n'
            by = self.musts(self.project(["a11y: advisory"], {"index.html": page}), "a11y")
            self.assertFalse(by["focus styles"]["pass"], cls)
        for code in ("const xs: Array<A> = [];\n<Button>Go</Button>\n", "for (i = 0; i<a.length; i++) {}\n"):
            by = self.musts(self.project(["a11y: advisory"], {"index.html": "", "app.tsx": code}), "a11y")
            self.assertTrue(by["focus styles"]["pass"], f"no interactive element in {code!r}")
            self.assertIn("no interactive element", by["focus styles"]["why"])

    def test_tokened_colours_and_one_radius_shorthand_are_not_debt(self):
        root = self.project(["debt: advisory"], {
            "a.css": ":root { --fg: 222 47% 11%; --c: 1 2 3; }\n"
                     ".a { color: hsl(var(--fg)); background: rgb(var(--c) / .5); border-color: rgba($ink, .5); }\n"
                     "@property --x { syntax: '<color>'; inherits: false; initial-value: #fff; }\n",
            "b.css": ".b { border-radius: 8px 8px 0 0; }\n"})
        g, _ = self.gate(root, "debt")
        self.assertEqual(g["files"], [{"file": "src/b.css", "count": 1, "kinds": {"radius": 1}}])
        with open(os.path.join(root, "src", "big.css"), "w") as f:
            f.write(".x { color: #123456; }\n" * 50_000)
        _, got = self.gate(root, "debt")
        self.assertIn("1 file(s) not read", " ".join(got["notes"]), "a skipped file is said, the count is short")

    def test_the_sweep_counts_untokened_literals_per_file(self):
        root = self.project(["debt: advisory 3"], {
            "a.css": ":root { --ink: #222; --dur: 200ms; }\n"
                     ".a { color: #333; background: rgb(1, 2, 3); border-radius: 8px; transition: opacity 150ms; }\n"
                     ".b { color: var(--ink, #000); transition: opacity var(--dur); border-radius: 0; }\n",
            "b.css": ".c { border-color: #fff; }\n"})
        g, _ = self.gate(root, "debt")
        self.assertEqual(g["files"][0], {"file": "src/a.css", "count": 4,
                                         "kinds": {"colour": 2, "duration": 1, "radius": 1}})
        self.assertEqual(g["files"][1]["count"], 1)
        (m,) = g["musts"]
        self.assertFalse(m["pass"])
        self.assertIn("5 untokened", m["why"])
        self.assertIn("src/a.css 4", m["why"])
        p = subprocess.run([sys.executable, FM, "design", "check", root], capture_output=True, text=True, cwd=root)
        self.assertEqual(p.returncode, 0, p.stderr)  # advisory
        self.assertIn("src/a.css", p.stdout)
        with open(os.path.join(root, "DESIGN.md"), "w") as f:
            f.write("## Gates\n- debt: blocking 5\n")
        self.assertTrue(self.gate(root, "debt")[0]["musts"][0]["pass"], "at the budget passes")
        with open(os.path.join(root, "DESIGN.md"), "w") as f:
            f.write("## Gates\n- debt: blocking\n")
        p = subprocess.run([sys.executable, FM, "design", "check", root, "--json"], capture_output=True, text=True,
                           cwd=root)
        self.assertEqual(p.returncode, 1, "no budget is a budget of 0")
        self.assertEqual(json.loads(p.stdout)["gates"][0]["gate"], "debt")
        with open(os.path.join(root, "DESIGN.md"), "w") as f:
            f.write("## Gates\n- debt: advisory 40x\n")
        g, got = self.gate(root, "debt")
        self.assertIn("can't read the budget '40x'", " ".join(got["notes"]))
        self.assertFalse(g["musts"][0]["pass"])


if __name__ == "__main__":
    unittest.main()
