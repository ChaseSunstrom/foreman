"""T-1507: design tokens. fm design palette makes a light/dark role palette from one seed colour (OKLCH maths by hand),
proves each pair's contrast on the sRGB hex a browser paints (WCAG 2.x relative luminance) and exports DTCG JSON, CSS
variables or a Tailwind v4 theme; fm design contrast proves a token file's pairs; fm design extract writes a repo's
:root custom properties into DESIGN.md's Tokens section and leaves every other section alone."""
import json
import os
import random
import re
import shutil
import unittest

from helpers import PLUGIN, ForemanTestCase, read_text

import fmcodetui
import fmdesign

HERE = os.path.dirname(os.path.abspath(__file__))
UI = os.path.join(HERE, "fixtures", "design-tokens", "ui")
SEEDS = ["#3366cc", "#e11d48", "#facc15", "#16a34a", "#777777", "#fafafa", "#050505", "oklch(0.62 0.25 145)",
         "hsl(280 90% 55%)", "rgb(0 200 255)", "oklch(70% 0.4 30deg)", "white"]


def ratio_of(proofs, fg, bg, theme):
    return next(p["ratio"] for p in proofs if (p["fg"], p["bg"], p["theme"]) == (fg, bg, theme))


class Palette(ForemanTestCase):
    def test_oklch_lands_on_the_playbooks_hex(self):
        # type-and-colour.md's worked example lists the sRGB hex each ramp value lands on
        for value, hexed in (("oklch(0.97 0.006 250)", "#F2F5F9"), ("oklch(0.22 0.010 250)", "#171B1F"),
                             ("oklch(0.45 0.130 258)", "#21539C"), ("oklch(0.74 0.100 258)", "#83ADEA"),
                             ("oklch(0.50 0.170 27)", "#B02B27"), ("oklch(1 0 0)", "#FFFFFF"),
                             ("oklch(0 0 0)", "#000000")):
            with self.subTest(value=value):
                self.assertEqual(fmdesign.hex_of(fmdesign.parse_colour(value)), hexed)

    def test_contrast_is_wcag_2_relative_luminance(self):
        self.assertAlmostEqual(fmdesign.contrast((1, 1, 1), (0, 0, 0)), 21.0, places=6)
        self.assertAlmostEqual(fmdesign.contrast((1, 1, 1), (1, 1, 1)), 1.0, places=6)
        rnd = random.Random(1507)
        for _ in range(300):  # an independent implementation: fm code's theme check, on 8-bit hex
            a, b = ("#%06x" % rnd.randrange(1 << 24) for _ in range(2))
            self.assertAlmostEqual(fmdesign.contrast(fmdesign.parse_colour(a), fmdesign.parse_colour(b)),
                                   fmcodetui.contrast(a, b), places=9)

    def test_srgb_to_oklch_round_trips(self):
        rnd = random.Random(7)
        for _ in range(200):
            h = "#%06X" % rnd.randrange(1 << 24)
            L, C, hue = fmdesign.oklch_of(fmdesign.parse_colour(h))
            self.assertEqual(fmdesign.hex_of(fmdesign.parse_colour(f"oklch({L} {C} {hue})")), h)

    def test_every_seed_gives_passing_pairs_in_both_themes(self):
        for seed in SEEDS:
            with self.subTest(seed=seed):
                pal = fmdesign.palette(seed)
                self.assertEqual(set(pal["light"]), set(fmdesign.ROLES))
                self.assertEqual(set(pal["dark"]), set(fmdesign.ROLES))
                self.assertEqual([p for p in pal["proofs"] if not p["pass"]], [])
                for surface in ("surface", "surface-raised", "surface-sunken"):
                    self.assertGreaterEqual(ratio_of(pal["proofs"], "text", surface, "light"), 4.5)
                    self.assertGreaterEqual(ratio_of(pal["proofs"], "text", surface, "dark"), 7)
                for theme in ("light", "dark"):
                    for role, tok in pal[theme].items():
                        self.assertRegex(tok["hex"], r"^#[0-9A-F]{6}$")
                        self.assertTrue(fmdesign.in_gamut(*tok["oklch"]), (theme, role, tok))

    def test_every_solved_pair_clears_its_floor_by_a_margin(self):
        # one 8-bit channel step can move a ratio by a few hundredths: a pair landing at exactly 4.50 isn't safe
        for seed in SEEDS:
            for p in fmdesign.palette(seed)["proofs"]:
                with self.subTest(seed=seed, pair=(p["fg"], p["bg"], p["theme"])):
                    self.assertGreaterEqual(p["ratio"], p["need"] + 0.03)

    def test_the_accent_keeps_the_seeds_hue(self):
        pal = fmdesign.palette("oklch(0.55 0.15 30)")
        for theme in ("light", "dark"):
            L, C, h = pal[theme]["accent"]["oklch"]
            self.assertAlmostEqual(h, 30, delta=1)
            self.assertGreater(C, 0.08)
        self.assertGreater(pal["dark"]["accent"]["oklch"][0], pal["light"]["accent"]["oklch"][0])

    def test_css_export_round_trips_through_fm_design_contrast(self):
        css = self.fm("design", "palette", "#3366cc").stdout
        self.assertIn(":root {", css)
        self.assertRegex(css, r"--text:\s+light-dark\(oklch\([\d. ]+\), oklch\([\d. ]+\)\);")
        path = os.path.join(self.tmp, "colour.css")
        with open(path, "w", encoding="utf-8") as f:
            f.write(css)
        p = self.fm("design", "contrast", path, "--json")
        data = json.loads(p.stdout)
        self.assertEqual(data["failed"], 0)
        pal = fmdesign.palette("#3366cc")
        for x in data["proofs"]:  # the file proves the same numbers palette printed
            self.assertAlmostEqual(x["ratio"], ratio_of(pal["proofs"], x["fg"], x["bg"], x["theme"]), places=6)

    def test_dtcg_export(self):
        data = json.loads(self.fm("design", "palette", "#3366cc", "--format", "dtcg").stdout)
        pal = fmdesign.palette("#3366cc")
        for theme in ("light", "dark"):
            for role in fmdesign.ROLES:
                tok = data[theme][role]
                self.assertEqual(tok["$type"], "color")
                self.assertEqual(tok["$value"]["colorSpace"], "oklch")
                self.assertEqual(tok["$value"]["components"], list(pal[theme][role]["oklch"]))
                self.assertEqual(tok["$value"]["hex"], pal[theme][role]["hex"].lower())

    def test_tailwind_export(self):
        out = self.fm("design", "palette", "#3366cc", "--format", "tailwind").stdout
        self.assertIn("@theme inline {", out)
        for role in fmdesign.ROLES:
            self.assertIn(f"--color-{role}: var(--{role});", out)
            self.assertIn(f"--{role}: light-dark(", out)

    def test_proofs_go_to_stderr_so_the_export_can_be_redirected(self):
        p = self.fm("design", "palette", "#3366cc")
        self.assertIn("pass", p.stderr)
        self.assertNotIn("pass", p.stdout)
        data = json.loads(self.fm("design", "palette", "#3366cc", "--json").stdout)
        self.assertEqual(set(data), {"seed", "light", "dark", "proofs", "export"})

    def test_a_seed_it_cant_read_is_an_error(self):
        for seed in ("nope", "#12", "oklch(a b c)", "color(display-p3 1 0 0)", "rgb(var(--x))"):
            with self.subTest(seed=seed):
                p = self.fm("design", "palette", seed, check=False)
                self.assertEqual(p.returncode, 2, p.stdout)
                self.assertIn("can't read", p.stderr)

    def test_a_worker_of_fm_code_may_run_palette_and_contrast(self):
        p = self.fm("design", "palette", "#3366cc", env={"FOREMAN_WORKER_OF": "run-1"})
        self.assertIn(":root", p.stdout)


class Extract(ForemanTestCase):
    def section(self, path):
        text = read_text(path)
        return text.split("\n## Tokens\n", 1)[1].split("\n## ", 1)[0]

    def row(self, section, name):
        rows = [ln for ln in section.splitlines() if ln.startswith(f"| `{name}` |")]
        self.assertEqual(len(rows), 1, (name, section))
        return rows[0]

    def test_writes_the_token_table_from_root_custom_properties(self):
        out = os.path.join(self.tmp, "DESIGN.md")
        self.fm("design", "extract", UI, "--out", out)
        text = read_text(out)
        self.assertTrue(text.startswith("# DESIGN.md: "), text[:80])
        sec = self.section(out)
        self.assertIn("| Token | Kind | Light | Dark | Source |", sec)
        self.assertIn("#F2F5F9", self.row(sec, "--surface"))
        self.assertIn("#0E1216", self.row(sec, "--surface"))
        brand = self.row(sec, "--brand")  # a [data-theme="dark"] block is the dark value
        self.assertIn("#21539C", brand)
        self.assertIn("#83ADEA", brand)
        self.assertIn("| colour |", brand)
        self.assertIn("| length |", self.row(sec, "--step-1"))
        self.assertIn("| duration |", self.row(sec, "--dur-tap"))
        self.assertIn("| font |", self.row(sec, "--font-body"))
        self.assertIn("tokens.css:", self.row(sec, "--text"))
        self.assertNotIn("--pad", sec)  # a component's own variable
        self.assertNotIn("--fake", sec)  # in a comment
        odd = self.row(sec, "--odd")  # a | or a backquote in a value can't break the table
        self.assertEqual(odd.count(" | "), 4, odd)
        self.assertIn("#3366CC", self.row(sec, "--color-brand-500"))  # tailwind.config colours
        self.assertIn("#3366CC", self.row(sec, "--color-brand"))  # DEFAULT is the bare name
        self.assertIn("#141E28", self.row(sec, "--color-brand-ink-strong"))
        self.assertIn("#F3ECE0", self.row(sec, "--color-paper"))
        self.assertNotIn("--color-muted", sec)  # commented out
        self.assertNotIn("gutter", sec)  # not a colour
        # the contrast of each text/surface pair, as DESIGN.md's Colour knob asks
        m = re.search(r"`text` on `surface-sunken`: ([\d.]+):1 light, ([\d.]+):1 dark", sec)
        self.assertTrue(m, sec)
        self.assertEqual((m.group(1), m.group(2)), ("14.07", "12.24"))  # the playbook's measured table

    def test_updates_only_its_own_section_and_a_second_run_changes_nothing(self):
        out = os.path.join(self.tmp, "DESIGN.md")
        before = ("# DESIGN.md: Kilnroom\n\n## Point of view\nA glaze notebook.\n\n## Knobs\n- Type: a serif.\n\n"
                  "```markdown\n## Tokens\nnot a heading: inside a fence\n```\n\n## Tokens\nstale table\n\n"
                  "## Banned\n- gradients\n")
        with open(out, "w", encoding="utf-8") as f:
            f.write(before)
        self.fm("design", "extract", UI, "--out", out)
        first = read_text(out)
        self.assertNotIn("stale table", first)
        self.assertIn("not a heading: inside a fence", first)
        self.assertTrue(first.startswith(before.split("\n## Tokens\nstale")[0]))
        self.assertTrue(first.endswith("## Banned\n- gradients\n"), first[-200:])
        self.assertEqual(first.count("\n## Tokens\n"), 2)  # the fenced one and the real one
        self.fm("design", "extract", UI, "--out", out)
        self.assertEqual(read_text(out), first)

    def test_a_design_md_without_the_section_gets_it_after_the_knobs(self):
        out = os.path.join(self.tmp, "DESIGN.md")
        with open(out, "w", encoding="utf-8") as f:
            f.write("# DESIGN.md: X\n\n## Knobs\n- Colour: ink.\n\n## Banned\n- gradients\n")
        self.fm("design", "extract", UI, "--out", out)
        text = read_text(out)
        self.assertLess(text.index("- Colour: ink."), text.index("## Tokens"))
        self.assertLess(text.index("## Tokens"), text.index("## Banned"))
        self.assertTrue(text.endswith("## Banned\n- gradients\n"))

    def test_default_out_is_the_repo_roots_design_md(self):
        ui = os.path.join(self.repo, "web", "ui")
        shutil.copytree(UI, ui)
        p = self.fm("design", "extract", "ui", cwd=os.path.join(self.repo, "web"))
        self.assertTrue(os.path.isfile(os.path.join(self.repo, "DESIGN.md")), p.stdout)
        self.assertFalse(os.path.exists(os.path.join(self.repo, "web", "DESIGN.md")))
        self.assertIn("web/ui/tokens.css:", self.section(os.path.join(self.repo, "DESIGN.md")))
        os.makedirs(os.path.join(self.repo, "docs"))
        os.rename(os.path.join(self.repo, "DESIGN.md"), os.path.join(self.repo, "docs", "DESIGN.md"))
        self.fm("design", "extract", ui)  # an existing docs/DESIGN.md is the one to update
        self.assertFalse(os.path.exists(os.path.join(self.repo, "DESIGN.md")))

    def test_out_dash_prints_and_writes_nothing(self):
        p = self.fm("design", "extract", UI, "--out", "-", cwd=self.repo)
        self.assertIn("## Tokens", p.stdout)
        self.assertFalse(os.path.exists(os.path.join(self.repo, "DESIGN.md")))

    def test_no_tokens_is_an_error_and_writes_nothing(self):
        os.makedirs(os.path.join(self.tmp, "bare"))
        with open(os.path.join(self.tmp, "bare", "a.css"), "w") as f:
            f.write(".a { --x: 1px; color: red; }\n")
        out = os.path.join(self.tmp, "DESIGN.md")
        p = self.fm("design", "extract", os.path.join(self.tmp, "bare"), "--out", out, check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("no :root custom properties", p.stderr)
        self.assertFalse(os.path.exists(out))
        p = self.fm("design", "extract", os.path.join(self.tmp, "nope"), "--out", out, check=False)
        self.assertEqual(p.returncode, 2)

    def test_edges_neither_crash_nor_corrupt(self):
        bare = os.path.join(self.tmp, "bare")
        os.makedirs(bare)
        with open(os.path.join(bare, "a.css"), "w") as f:  # a text role but no surface: no proofs, still a table
            f.write(":root { --text: #111; --link: var(--nope, var(--text)); }\n")
        out = os.path.join(self.tmp, "DESIGN.md")
        self.fm("design", "extract", bare, "--out", out)
        self.assertIn("#111111", self.row(self.section(out), "--link"))  # a fallback that is itself a var()
        with open(out, "w") as f:
            f.write("# D\n\n```\nnever closed\n")
        p = self.fm("design", "extract", bare, "--out", out, check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("never closed", p.stderr)
        self.assertEqual(read_text(out), "# D\n\n```\nnever closed\n")
        p = self.fm("design", "extract", bare, "--out", self.tmp, check=False)  # a directory
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertNotIn("Traceback", p.stderr)
        for seed in ("oklch(0.5 1e999 30)", "oklch(1 0.4 0)", "oklch(0 0 0)"):  # not finite; the ends of L
            p = self.fm("design", "palette", seed, check=False)
            self.assertNotIn("Traceback", p.stderr)
            self.assertEqual(p.returncode, 2 if "e999" in seed else 0, (seed, p.stderr))

    def tokens_of(self, css):
        path = os.path.join(self.tmp, "t.css")
        with open(path, "w", encoding="utf-8") as f:
            f.write(css)
        return fmdesign.read_tokens(path)

    def test_which_blocks_hold_tokens(self):
        base, dark = self.tokens_of(
            ":root { --a: #fff !important; @media (prefers-color-scheme: dark) { --a: #000; } &.dark { --b: #111; } }\n"
            "html body .btn { --pad: 1px; }\n[data-lang=html] { --q: 1; }\n.card :root { --r: 2; }\n"
            "html.dark { --c: #222; }\n:root[data-theme='dark'] { --d: #333; }\n:host(.dark) { --e: #444; }\n"
            "@layer base { :root { --f: #555; } }\n@media (min-width: 40em) { :root { --a: #abc; } }\n")
        self.assertEqual(base, {"--a": "#fff", "--f": "#555"})
        self.assertEqual(dark, {"--a": "#000", "--b": "#111", "--c": "#222", "--d": "#333", "--e": "#444"})

    def test_deep_nesting_stays_linear(self):
        import time
        t = time.monotonic()
        base, _ = self.tokens_of(":root{" * 80_000 + "--a:1;" * 80_000)
        self.assertEqual(base, {"--a": "1"})
        self.assertLess(time.monotonic() - t, 5)

    def test_skipped_files_are_reported(self):
        ui = os.path.join(self.tmp, "ui")
        os.makedirs(ui)
        with open(os.path.join(ui, "a.css"), "w") as f:
            f.write(":root { --x: #fff; }\n")
        with open(os.path.join(ui, "big.css"), "w") as f:
            f.write(":root { --y: #000; }\n" + "/* pad */\n" * 120_000)
        data = json.loads(self.fm("design", "extract", ui, "--out", "-", "--json").stdout)
        self.assertEqual([x["file"] for x in data["skipped"]], [os.path.join(ui, "big.css")])
        self.assertIn("skipped:", self.fm("design", "extract", ui, "--out", os.path.join(self.tmp, "D.md")).stdout)

    def test_no_absolute_path_outside_the_design_md_folder(self):
        out = os.path.join(self.repo, "DESIGN.md")
        self.fm("design", "extract", UI, "--out", out)
        text = read_text(out)
        self.assertNotIn(HERE, text)
        self.assertNotIn(os.path.expanduser("~"), text)
        self.assertIn("ui/tokens.css:", self.row(self.section(out), "--text"))

    def test_design_md_is_kept_as_written(self):
        out = os.path.join(self.tmp, "DESIGN.md")
        with open(out, "wb") as f:  # not UTF-8: refused, never rewritten as mojibake
            f.write(b"# DESIGN.md: caf\xe9\n")
        p = self.fm("design", "extract", UI, "--out", out, check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("UTF-8", p.stderr)
        with open(out, "rb") as f:
            self.assertEqual(f.read(), b"# DESIGN.md: caf\xe9\n")
        with open(out, "wb") as f:  # CRLF stays CRLF
            f.write(b"# DESIGN.md: X\r\n\r\n## Knobs\r\n- Type: a serif.\r\n\r\n## Banned\r\n- gradients\r\n")
        self.fm("design", "extract", UI, "--out", out)
        with open(out, "rb") as f:
            data = f.read()
        self.assertIn(b"## Tokens\r\n", data)
        self.assertNotIn(b"\n", data.replace(b"\r\n", b""))
        self.assertTrue(data.endswith(b"## Banned\r\n- gradients\r\n"))
        real = os.path.join(self.tmp, "docs", "design.md")  # a symlink is written through, not replaced
        os.makedirs(os.path.dirname(real))
        with open(real, "w") as f:
            f.write("# DESIGN.md: X\n")
        link = os.path.join(self.tmp, "LINKED.md")
        os.symlink(real, link)
        self.fm("design", "extract", UI, "--out", link)
        self.assertTrue(os.path.islink(link))
        self.assertIn("## Tokens", read_text(real))

    def test_long_hostile_lines_stay_linear(self):
        import time
        path = os.path.join(self.tmp, "big")
        os.makedirs(path)
        with open(os.path.join(path, "tailwind.config.js"), "w") as f:
            f.write("colors: { " + "a" * 400_000 + " }\n" + "'" + "b" * 300_000 + "\n")
        with open(os.path.join(path, "a.css"), "w") as f:
            f.write(":root { --x: oklch(" + "1" * 200_000 + "x); }\n" + ":not(" * 50_000 + "{ }\n" + "#{" * 50_000)
        t = time.monotonic()
        fmdesign.extract([path])
        fmdesign.check_pairs(fmdesign.read_tokens(os.path.join(path, "a.css")), ["x/x"], strict=False)
        self.assertLess(time.monotonic() - t, 5)

    def test_a_worker_of_fm_code_may_not_extract(self):
        p = self.fm("design", "extract", UI, "--out", os.path.join(self.tmp, "D.md"), check=False,
                    env={"FOREMAN_WORKER_OF": "run-1"})
        self.assertNotEqual(p.returncode, 0)
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "D.md")))

    def test_contrast_checks_the_pairs_given(self):
        tokens = os.path.join(UI, "tokens.css")
        data = json.loads(self.fm("design", "contrast", tokens, "text/surface-sunken:7", "border/surface-sunken:3",
                                  "--json").stdout)
        self.assertEqual(data["failed"], 0)
        self.assertAlmostEqual(ratio_of(data["proofs"], "text", "surface-sunken", "light"), 14.07, delta=0.005)
        self.assertAlmostEqual(ratio_of(data["proofs"], "border", "surface-sunken", "dark"), 3.10, delta=0.005)
        p = self.fm("design", "contrast", tokens, "border/surface-sunken:4.5", check=False)
        self.assertEqual(p.returncode, 1)
        self.assertRegex(p.stdout, r"FAIL\s+light\s+border/surface-sunken\s+3\.9\d:1")
        p = self.fm("design", "contrast", tokens, "text/surface:4.5,7")  # light, dark floors
        self.assertIn("(needs 7)", p.stdout)

    def test_contrast_without_pairs_checks_the_known_roles(self):
        data = json.loads(self.fm("design", "contrast", os.path.join(UI, "tokens.css"), "--json").stdout)
        pairs = {(x["fg"], x["bg"]) for x in data["proofs"]}
        self.assertIn(("text", "surface-sunken"), pairs)
        self.assertIn(("on-accent", "accent"), pairs)
        dark_text = [x for x in data["proofs"] if x["fg"] == "text" and x["theme"] == "dark"]
        self.assertEqual({x["need"] for x in dark_text}, {7})

    def test_contrast_names_what_it_cant_read(self):
        path = os.path.join(self.tmp, "t.css")
        for body, word in ((":root { --text: var(--a); --a: var(--text); --surface: #fff; }", "loop"),
                           (":root { --text: color-mix(in oklch, red, blue); --surface: #fff; }", "--text"),
                           (":root { --surface: #fff; }", "--text")):
            with self.subTest(body=body):
                with open(path, "w") as f:
                    f.write(body)
                p = self.fm("design", "contrast", path, "text/surface", check=False)
                self.assertEqual(p.returncode, 2, p.stdout)
                self.assertIn(word, p.stderr)

    def test_contrast_warns_on_a_value_outside_srgb(self):
        path = os.path.join(self.tmp, "t.css")
        with open(path, "w") as f:
            f.write(":root { --text: oklch(0.3 0.4 30); --surface: #fff; }")
        p = self.fm("design", "contrast", path, "text/surface")
        self.assertIn("outside sRGB", p.stdout)

    def test_contrast_runs_without_foreman_for_ci(self):
        import subprocess
        import sys
        p = subprocess.run([sys.executable, os.path.join(PLUGIN, "lib", "fmdesign.py"), "contrast",
                            os.path.join(UI, "tokens.css"), "text/surface:4.5,7"], capture_output=True, text=True,
                           timeout=30)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("pass", p.stdout)

    def test_the_playbooks_proof_table_is_what_the_verb_measures(self):
        # T-1489's lesson: a playbook's numbers come from running its own tool on its own example
        text = read_text(os.path.join(PLUGIN, "skills", "playbooks", "references", "ui", "type-and-colour.md"))
        path = os.path.join(self.tmp, "colour.css")
        with open(path, "w", encoding="utf-8") as f:
            f.write(re.search(r"(?ms)^```css\n(.*?)^```", text).group(1))
        tokens = fmdesign.read_tokens(path)
        rows = re.findall(r"(?m)^\| `([\w-]+)`(?: \(links\))? on `([\w-]+)` \| [^|]+ \| ([\d.]+) \| ([\d.]+) \|$", text)
        self.assertGreaterEqual(len(rows), 12)
        for fg, bg, light, dark in rows:
            proofs, _ = fmdesign.check_pairs(tokens, [f"{fg}/{bg}"])
            with self.subTest(pair=(fg, bg)):
                self.assertEqual((f"{ratio_of(proofs, fg, bg, 'light'):.2f}", f"{ratio_of(proofs, fg, bg, 'dark'):.2f}"),
                                 (light, dark))

    def test_the_skill_is_user_started_and_points_at_the_verbs(self):
        text = read_text(os.path.join(PLUGIN, "skills", "design-extract", "SKILL.md"))
        meta = text.split("---")[1]
        self.assertIn("name: design-extract", meta)
        self.assertIn("disable-model-invocation: true", meta)  # the 2,000-character listing has no room for it
        for verb in ("fm design extract", "fm design palette", "fm design contrast", "DESIGN.md"):
            self.assertIn(verb, text)
        playbook = read_text(os.path.join(PLUGIN, "skills", "playbooks", "references", "ui", "type-and-colour.md"))
        self.assertIn("fm design contrast", playbook)
        self.assertIn("fm design palette", playbook)
        self.assertNotIn("contrast_proof.py", playbook)
        self.assertIn("Python 3.11", playbook)  # the copied file's regexes are possessive
        directions = read_text(os.path.join(PLUGIN, "skills", "directions", "SKILL.md"))
        direction_md = read_text(os.path.join(PLUGIN, "skills", "playbooks", "references", "ui", "design-direction.md"))
        for doc in (directions, direction_md):  # a Tokens-only DESIGN.md is a palette, not a direction
            self.assertIn("fm design extract", doc)
            self.assertIn("`## Direction` section", doc)
        self.assertIn("## Tokens", direction_md)
        self.assertTrue(fmdesign.has_direction("# D\n\n## Direction\nPoster, audacity wild.\n"))
        self.assertFalse(fmdesign.has_direction("# D\n\n## Tokens\n\n```\n## Direction\n```\n"))


if __name__ == "__main__":
    unittest.main()
