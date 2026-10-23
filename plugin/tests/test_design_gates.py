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


if __name__ == "__main__":
    unittest.main()
