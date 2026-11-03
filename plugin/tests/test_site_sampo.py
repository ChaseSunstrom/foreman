"""T-2753 (T-2742 step 7a): the site wears Sampo's design system. Its colours, type and motion come from
design/sampo/tokens.json through one generated block at the top of site/style.css (`python3 site/build.py --tokens`
writes it; the build refuses a stale one), its icon, favicon and share card are the Runestone files the build copies
from design/sampo/logo, and no page names Foreman outside the forms kept as aliases."""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

from helpers import PLUGIN, read_text
from test_rename_scan import KEPT, leftover
from test_site_build import site

ROOT = os.path.dirname(PLUGIN)
LOGO = os.path.join(ROOT, "design", "sampo", "logo")
CSS = os.path.join(ROOT, "site", "style.css")
REPO = re.compile(r"chasesunstrom(?:\.github\.io)?/foreman", re.I)  # the repo's address moves only when it is renamed
KEY = re.compile(r"\.foreman\b")  # a data key the exporter in plugin/lib writes; it renames with the internals (T-2748)
QUOTED = re.compile(  # text a built page quotes verbatim from files this task leaves alone: it renames with its source
    r"duel-\w+-foreman-\d{8}"  # recorded bench run ids, which sampo bench repro takes as they are
    r"|every Foreman project"  # plugin/lib/sampo/smithtui.py's key map (T-2748)
    r"|Foreman(?:&#x27;|')s own|In Foreman, start it"  # the playbooks under plugin/skills/playbooks
    r'|<ol class="tape".*?</ol>')  # the Decisions page's tape: decisions as they were recorded


def tokens():
    with open(os.path.join(ROOT, "design", "sampo", "tokens.json"), encoding="utf-8") as f:
        return json.load(f)


def roles(theme):
    return {k: v["$value"] for k, v in tokens()[theme]["color"].items() if not k.startswith("$")}


def names_foreman(text):
    return re.search(r"\bforeman\b", KEPT.sub("", KEY.sub("", REPO.sub("", text))), re.I)


class Tokens(unittest.TestCase):
    def setUp(self):
        self.build = site("build")
        self.block = self.build.tokens_css()

    def test_style_css_carries_the_block_tokens_json_makes(self):
        self.assertIn(self.block, read_text(CSS), "run python3 site/build.py --tokens")

    def test_every_role_lands_in_its_theme(self):
        light, dark = self.block.split("@media (prefers-color-scheme: dark)", 1)
        for theme, part in (("light", light), ("dark", dark)):
            for role, value in roles(theme).items():
                self.assertIn(f"--{role}: {value};", part, theme)
        self.assertEqual(dark.count("--surface: " + roles("dark")["surface"]), 2, "the system's dark and the toggle's")
        self.assertIn(':root[data-theme="dark"]', dark)
        self.assertIn(':root:not([data-theme="light"])', dark)

    def test_type_and_motion_come_from_the_tokens(self):
        t = tokens()
        for face in ("display", "text", "mono"):
            stack = re.search(rf"--font-{face}: ([^;]+);", self.block).group(1)
            self.assertEqual([s.strip().strip('"') for s in stack.split(",")], t["font"][face]["$value"])
        self.assertIn('"Iowan Old Style"', self.block)
        self.assertIn(", serif;", self.block, "a generic family stays a keyword")
        ratio = t["font"]["scale"]["ratio"]["$value"]
        self.assertIn(f"--step-2: {round(ratio ** 2, 3)}rem;", self.block)
        for name, d in t["motion"]["duration"].items():
            if not name.startswith("$"):
                self.assertIn(f"--dur-{name}: {d['$value']};", self.block)
        for name, e in t["motion"]["easing"].items():
            if not name.startswith("$"):
                self.assertIn(f"--ease-{name}: cubic-bezier({', '.join(str(x) for x in e['$value'])});", self.block)
        self.assertIn("--autoplay-limit: 5000ms;", self.block)

    def test_a_stale_block_stops_the_build_and_the_writer_mends_it(self):
        css = read_text(CSS)
        stale = css.replace(f"--surface: {roles('light')['surface']};", "--surface: #FFFFFF;", 1)
        self.assertNotEqual(stale, css)
        with self.assertRaises(SystemExit):
            self.build.check_tokens(stale)
        self.build.check_tokens(css)
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "style.css")
            with open(path, "w", encoding="utf-8") as f:
                f.write(stale)
            self.build.write_tokens(path)
            self.build.write_tokens(path)  # a second run changes nothing
            self.assertEqual(read_text(path), css)

    def test_no_colour_easing_old_face_or_endless_loop_is_typed_by_hand(self):
        css = read_text(CSS).replace(self.block, "")
        for name in ("style.css", os.path.join("genesis", "genesis.css")):
            text = css if name == "style.css" else read_text(os.path.join(ROOT, "site", name))
            # the one exception: the charts' categorical palette (--s1 to --s6), which tokens.json doesn't hold
            rest = re.sub(r"--s\d: #[0-9A-Fa-f]{6};", "", text)
            self.assertEqual(re.findall(r"[^\n]*#[0-9A-Fa-f]{3,8}\b[^\n]*", rest), [], name + ": colours live in tokens.json")
            for banned in ("cubic-bezier(", "Barlow", "condensed", "infinite"):
                self.assertNotIn(banned, text, name)
        self.assertIn("var(--ease-enter)", css)
        self.assertIn("var(--dur-small)", css)

    def test_the_browser_bar_takes_the_surface(self):
        page = read_text(os.path.join(ROOT, "site", "index.html"))
        for theme in ("light", "dark"):
            self.assertIn(f'<meta name="theme-color" content="{roles(theme)["surface"]}" '
                          f'media="(prefers-color-scheme: {theme})">', page)

    def test_every_link_in_site_stays_in_the_repo(self):  # the build copies a link's target: one outside would publish
        root = os.path.realpath(ROOT)
        for d, dirs, files in os.walk(os.path.join(ROOT, "site")):
            for name in dirs + files:
                path = os.path.join(d, name)
                if os.path.islink(path):
                    self.assertTrue(os.path.realpath(path).startswith(root + os.sep), f"{path} leaves the repo")


class Built(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.out = os.path.join(cls.tmp, "o")
        p = subprocess.run([sys.executable, os.path.join(ROOT, "site", "build.py"), cls.out], capture_output=True,
                           text=True, timeout=300)
        assert p.returncode == 0, p.stderr

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_the_logo_files_are_the_runestone_ones(self):
        for rel, src in (("sampo.svg", "icon-16.svg"), ("favicon.ico", "favicon.ico"), ("share.png", "share.png"),
                         ("foreman.svg", "icon-16.svg")):  # the old icon URL keeps working, and shows the new mark
            with open(os.path.join(self.out, "assets", rel), "rb") as a, open(os.path.join(LOGO, src), "rb") as b:
                self.assertEqual(a.read(), b.read(), rel)
        for rel in ("index.html", os.path.join("features", "index.html"), os.path.join("genesis", "index.html"),
                    os.path.join("stories", "fix.html")):
            page = read_text(os.path.join(self.out, rel))
            self.assertRegex(page, r'<link rel="icon" href="(\.\./)?assets/sampo\.svg\?v=\w{8}" type="image/svg\+xml">',
                             rel)
            self.assertRegex(page, r'<link rel="icon" href="(\.\./)?assets/favicon\.ico\?v=\w{8}" sizes="32x32">', rel)
            self.assertRegex(page, r'<img src="(\.\./)?assets/sampo\.svg\?v=\w{8}"', rel)
            self.assertIn(">Sampo</a>", page, rel)
            self.assertNotIn("assets/foreman.svg", page, rel)
        self.assertFalse(os.path.exists(os.path.join(ROOT, "site", "share.html")), "the old card's source")

    def test_no_page_names_foreman_outside_the_kept_forms(self):
        rows = [r for r in leftover() if r[0].startswith("site/") and names_foreman(r[1])]
        self.assertEqual(rows, [], "a source page still says Foreman")
        said = []
        for d, _, files in os.walk(self.out):
            if os.path.relpath(d, self.out).split(os.sep)[0] == "gallery":  # the UI playbooks' own worked examples
                continue
            for name in files:
                if name.endswith((".html", ".js", ".css")):
                    path = os.path.join(d, name)
                    said += [f"{os.path.relpath(path, self.out)}: {ln.strip()[:90]}"
                             for ln in read_text(path).splitlines() if names_foreman(QUOTED.sub("", ln))]
        self.assertEqual(said, [], "a built page still says Foreman")
        self.assertTrue(any("formerly Foreman" in ln for ln in read_text(os.path.join(self.out, "index.html")).splitlines()),
                        "the install section says what Sampo was called")


if __name__ == "__main__":
    unittest.main()
