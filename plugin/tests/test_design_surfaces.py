"""T-1651: fm design tokens compiles DESIGN.md's ## Tokens table (the one fm design extract writes) to CSS custom
properties, an fm code app theme ([colors] for tui.toml, checked the way fm settings checks it) and the Claude Code
pane's palette (the C object in mods/foreman-ui/hooks/kit.ts)."""
import json
import os
import re

from helpers import PLUGIN, ForemanTestCase, read_text

import fmsettings

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.join(HERE, "fixtures", "design-surfaces", "DESIGN.md")
UI = os.path.join(HERE, "fixtures", "design-tokens", "ui")
KIT = os.path.join(os.path.dirname(PLUGIN), "mods", "foreman-ui", "hooks", "kit.ts")


class Tokens(ForemanTestCase):
    def tokens(self, *args, path=DESIGN, check=True):
        return self.fm("design", "tokens", path, *args, check=check)

    def copy(self, old, new):
        path = os.path.join(self.tmp, "DESIGN.md")
        text = read_text(DESIGN)
        self.assertIn(old, text)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text.replace(old, new))
        return path

    def accepted(self, text):
        """What fm settings makes of `text` as the user's tui.toml: ({colors.X: value}, problems), each one read."""
        with open(os.path.join(self.home, "tui.toml"), "w", encoding="utf-8") as f:
            f.write(text)
        problems = []
        got = fmsettings.written(problems)
        colors = {k: v for (s, k), (v, e, read) in got.items() if s == "app" and k.startswith("colors.")}
        unread = [k for (s, k), (v, e, read) in got.items() if s == "app" and not read]
        self.assertEqual(unread, [], text)
        self.assertEqual([p for p in problems if p[0] == "app"], [], text)
        return colors

    def test_css_variables_light_in_root_dark_in_the_media_query(self):
        css = self.tokens("--to", "css").stdout
        root, dark = css.split("@media (prefers-color-scheme: dark)")
        self.assertIn("--surface: #f2f5f9;", root)
        self.assertIn("--accent: #21539c;", root)
        self.assertIn('--font-body: "Source Sans 3", system-ui, sans-serif;', root)  # every kind, not colours alone
        self.assertIn("--step-0: 1rem;", root)
        self.assertIn("--odd: a | b 'c';", root)  # the table's escaped pipe, unescaped
        self.assertIn("--surface: var(--n-18);", dark)
        self.assertIn("--accent: #83adea;", dark)
        self.assertNotIn("--border", dark)  # no dark value: the light one stands
        self.assertNotIn("--step-0", dark)
        self.assertNotIn("body {", css)  # a value that would close the block is left out, and said
        self.assertRegex(css, r"/\*[^*]*--sneaky[^*]*\*/")
        self.assertNotRegex(css, r"(?m)^\s*--sneaky:")
        self.assertNotIn("--not-a-token", css)  # a table under another heading isn't the Tokens table
        self.assertEqual(css.count("{"), css.count("}"))

    def test_app_theme_is_one_fm_settings_accepts(self):
        toml = self.tokens("--to", "app").stdout
        colors = self.accepted(toml)
        self.assertEqual(colors["colors.screen"]["bg"].upper(), "#0E1216")  # dark values by default
        self.assertEqual(colors["colors.screen"]["fg"].upper(), "#E4E8ED")
        self.assertEqual(colors["colors.strong"]["fg"].upper(), "#E4E8ED")
        self.assertEqual(colors["colors.dim"]["fg"].upper(), "#8C939B")  # --text-muted, not --accent-subtle
        self.assertEqual(colors["colors.accent"]["fg"].upper(), "#83ADEA")
        self.assertTrue(colors["colors.accent"].get("bold"))  # the preset's weight is kept
        self.assertEqual(colors["colors.select"]["bg"].upper(), "#83ADEA")
        self.assertEqual(colors["colors.ok"]["fg"].upper(), "#6FCF8E")
        self.assertEqual(colors["colors.bad"]["fg"].upper(), "#FF8A80")
        self.assertEqual(colors["colors.warn"]["fg"].upper(), "#F5C04A")
        self.assertEqual(colors["colors.border"]["fg"].upper(), "#6B727B")  # light only: it stands for dark too
        self.assertEqual(colors["colors.header"]["bg"].upper(), "#171B1F")
        self.assertEqual(colors["colors.bar"]["bg"].upper(), "#171B1F")
        m = re.search(r"^# not mapped.*: (.+)$", toml, re.M)
        self.assertTrue(m, toml)
        self.assertIn("shade", m.group(1))
        self.assertNotIn("colors.screen", m.group(1))

    def test_light_values_on_the_paper_theme(self):
        toml = self.tokens("--to", "app", "--light").stdout
        self.assertIn('theme = "paper"', toml)
        colors = self.accepted(toml)
        self.assertEqual(colors["colors.screen"]["bg"].upper(), "#F2F5F9")
        self.assertEqual(colors["colors.accent"]["fg"].upper(), "#21539C")

    def test_a_style_too_faint_is_left_out_and_named(self):
        path = self.copy("`#8c939b` #8C939B", "`#1a1e22` #1A1E22")  # muted nearly the screen's own colour
        toml = self.tokens("--to", "app", path=path).stdout
        colors = self.accepted(toml)
        self.assertNotIn("colors.dim", colors)
        self.assertRegex(toml, r"# left out: colors\.dim: .*too faint")
        self.assertEqual(colors["colors.accent"]["fg"].upper(), "#83ADEA")

    def test_pane_palette_uses_the_kits_keys(self):
        pal = json.loads(self.tokens("--to", "pane").stdout)
        kit = read_text(KIT)
        block = re.search(r"export const C = \{(.*?)\n\}", kit, re.S).group(1)
        keys = set(re.findall(r"^\s*(\w+):", block, re.M))
        self.assertLessEqual(set(pal), keys)
        self.assertEqual(pal["accent"].upper(), "#83ADEA")
        self.assertEqual(pal["err"].upper(), "#FF8A80")
        self.assertEqual(pal["muted"].upper(), "#8C939B")
        self.assertEqual(pal["track"].upper(), "#6B727B")
        self.assertTrue(all(re.fullmatch(r"#[0-9A-Fa-f]{6}", v) for v in pal.values()), pal)

    def test_reads_what_extract_writes(self):
        out = os.path.join(self.tmp, "DESIGN.md")
        self.fm("design", "extract", UI, "--out", out)
        css = self.tokens("--to", "css", path=out).stdout
        self.assertIn("--surface: var(--n-97);", css)
        self.assertIn("--n-97: oklch(0.97 0.006 250);", css)
        colors = self.accepted(self.tokens("--to", "app", path=out).stdout)
        self.assertEqual(colors["colors.screen"]["bg"].upper(), "#0E1216")
        self.assertEqual(colors["colors.accent"]["fg"].upper(), "#83ADEA")

    def test_no_tokens_table_is_an_error(self):
        path = os.path.join(self.tmp, "DESIGN.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write("# DESIGN.md\n\n## Direction\n\nCalm.\n")
        p = self.tokens("--to", "css", path=path, check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("## Tokens", p.stderr)
        p = self.tokens("--to", "css", path=os.path.join(self.tmp, "none.md"), check=False)
        self.assertEqual(p.returncode, 2)

    def table(self, rows, head="| Token | Kind | Light | Dark | Source |"):
        """A DESIGN.md whose Tokens table holds rows: (name, kind, light cell, dark cell)."""
        path = os.path.join(self.tmp, "T.md")
        lines = ["# DESIGN.md", "", "## Tokens", "", head, "|---|---|---|---|---|"]
        lines += [f"| `{n}` | {k} | {lt} | {dk} | t.css:1 |" for n, k, lt, dk in rows]
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        return path

    def test_css_value_that_could_escape_its_declaration_falls_back(self):
        bad = ["calc(1px + 2px", "[x", "x)", '"open', "</style><script>x</script>", "url(https://x.test/a.png)",
               "@import 'x.css'", r"a\62 c", "red; } body { color: red", "a /* x", "x */ y"]
        rows = [(f"--bad-{i}", "other", f"`{v.replace('|', chr(92) + '|')}`", "") for i, v in enumerate(bad)]
        rows += [("--bad-col", "colour", "`url(x)` #112233", "`calc(1px` #445566"),
                 ("--good", "length", "`calc(100% - (2 * var(--step-0)))`", ""),
                 ("--font", "font", "`\"Bob's Sans\", serif`", ""), ("--dark-only", "other", "", "`[x`")]
        css = self.tokens("--to", "css", path=self.table(rows)).stdout
        for i, v in enumerate(bad):
            with self.subTest(v=v):
                self.assertNotRegex(css, rf"(?m)^\s*--bad-{i}:")
                self.assertIn(f"--bad-{i} (light)", css)
        self.assertIn("--bad-col: #112233;", css)  # a colour falls back to its hex
        self.assertIn("--bad-col: #445566;", css)
        self.assertIn("--good: calc(100% - (2 * var(--step-0)));", css)
        self.assertIn("--font: \"Bob's Sans\", serif;", css)
        self.assertIn("--dark-only (dark)", css)  # a dark value refused is said, not dropped
        for bit in ("</style", "url(", "@import", "\\"):
            self.assertNotIn(bit, css.split("/* left out")[0])

    def test_css_dark_values_also_under_the_class_and_data_theme(self):
        css = self.tokens("--to", "css").stdout
        self.assertRegex(css, r'\.dark, \[data-theme="dark"\] \{[^}]*--accent: #83adea;')
        p = self.tokens("--to", "css", "--light")
        self.assertIn("--light", p.stderr)  # said, not silently ignored

    def test_columns_are_read_by_their_header(self):
        path = self.table([("--surface", "`#f2f5f9` #F2F5F9", "`#0e1216` #0E1216", "colour"),  # the table() slots
                           ("--accent", "`#21539c` #21539C", "`#83adea` #83ADEA", "colour")],  # hold Light, Dark, Kind
                          head="| Token | Light | Dark | Kind | Source |")
        css = self.tokens("--to", "css", path=path).stdout
        self.assertIn("--surface: #f2f5f9;", css)
        self.assertIn("--accent: #83adea;", css.split("@media")[1])

    def test_light_token_file_picks_the_paper_preset_and_checks_every_style(self):
        path = self.table([("--surface", "colour", "`#ffffff` #FFFFFF", ""), ("--text", "colour", "`#111111` #111111", ""),
                           ("--accent", "colour", "`#1d4ed8` #1D4ED8", "")])
        toml = self.tokens("--to", "app", path=path).stdout
        self.assertIn('theme = "paper"', toml)  # a white screen: night's pastels would be unreadable on it
        self.accepted(toml)
        self.assertNotRegex(toml, r"# too faint")
        dark = self.tokens("--to", "app", "--dark", path=path).stdout
        self.assertIn('theme = "night"', dark)
        m = re.search(r"^# too faint on this screen.*: (.+)$", dark, re.M)
        self.assertTrue(m, dark)  # night's own styles, never written, checked against the white screen all the same
        self.assertIn("ok", m.group(1))
        self.accepted(dark)

    def test_shadcn_names_map_to_their_roles(self):
        c = lambda lt, dk: (f"`{lt}` {lt.upper()}", f"`{dk}` {dk.upper()}")
        rows = [("--background", "colour", *c("#ffffff", "#0a0a0a")), ("--foreground", "colour", *c("#0a0a0a", "#fafafa")),
                ("--muted", "colour", *c("#f5f5f5", "#262626")),
                ("--muted-foreground", "colour", *c("#737373", "#a3a3a3")),
                ("--accent", "colour", *c("#f5f5f5", "#262626")),
                ("--accent-foreground", "colour", *c("#171717", "#fafafa")),
                ("--primary", "colour", *c("#2563eb", "#60a5fa")),
                ("--primary-foreground", "colour", *c("#fafafa", "#0a0a0a")),
                ("--destructive", "colour", *c("#dc2626", "#f87171")), ("--card", "colour", *c("#ffffff", "#171717")),
                ("--border", "colour", *c("#e5e5e5", "#404040"))]
        colors = self.accepted(self.tokens("--to", "app", path=self.table(rows)).stdout)
        self.assertEqual(colors["colors.screen"]["bg"].upper(), "#0A0A0A")
        self.assertEqual(colors["colors.screen"]["fg"].upper(), "#FAFAFA")
        self.assertEqual(colors["colors.dim"]["fg"].upper(), "#A3A3A3")  # --muted-foreground, not the --muted surface
        self.assertEqual(colors["colors.accent"]["fg"].upper(), "#60A5FA")  # --primary, not the --accent surface
        self.assertEqual(colors["colors.bad"]["fg"].upper(), "#F87171")
        self.assertEqual(colors["colors.header"]["bg"].upper(), "#171717")

    def test_text_muted_beats_a_muted_surface_listed_first(self):
        c = lambda h: (f"`{h}` {h.upper()}", "")
        rows = [("--surface", "colour", *c("#0e1216")), ("--surface-muted", "colour", *c("#1a1e22")),
                ("--text", "colour", *c("#e4e8ed")), ("--text-muted", "colour", *c("#8c939b"))]
        colors = self.accepted(self.tokens("--to", "app", path=self.table(rows)).stdout)
        self.assertEqual(colors["colors.dim"]["fg"].upper(), "#8C939B")

    def test_a_worker_of_fm_code_may_compile(self):
        p = self.fm("design", "tokens", DESIGN, "--to", "pane", env={"FOREMAN_WORKER_OF": "run-1"})
        self.assertIn('"accent"', p.stdout)
