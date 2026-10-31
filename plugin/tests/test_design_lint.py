"""T-1506: fm design lint flags the tells of generated design and craft slips in UI source. Each rule ships a slop and a
crafted fixture under fixtures/design/<rule>/: the slop's lines marked `expect` are exactly the rule's findings, and the
crafted twin draws no finding at all (precision first: a rule that can't be precise is left out)."""
import glob
import json
import os
import unittest

from helpers import ForemanTestCase

import fmdesign

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures", "design")
SITE = os.path.join(os.path.dirname(os.path.dirname(HERE)), "site")


def expected_lines(path):
    with open(path, encoding="utf-8") as f:
        return {i for i, line in enumerate(f, 1) if "expect" in line}


class Rules(ForemanTestCase):
    def test_every_rule_has_a_fixture_pair(self):
        self.assertEqual(sorted(os.listdir(FIX)), sorted(r["id"] for r in fmdesign.RULES))

    def test_slop_flagged_on_the_marked_lines(self):
        for rule in fmdesign.RULES:
            slops = glob.glob(os.path.join(FIX, rule["id"], "slop*"))
            self.assertTrue(slops, rule["id"])
            for path in slops:
                with self.subTest(path=os.path.relpath(path, FIX)):
                    found = [f for f in fmdesign.lint([path]) if f["rule"] == rule["id"]]
                    self.assertEqual({f["line"] for f in found}, expected_lines(path))
                    for f in found:
                        self.assertEqual(f["file"], path)
                        self.assertTrue(f["fix"] and f["why"])

    def test_crafted_twin_is_clean(self):
        for rule in fmdesign.RULES:
            crafted = glob.glob(os.path.join(FIX, rule["id"], "crafted*"))
            self.assertTrue(crafted, rule["id"])
            for path in crafted:
                with self.subTest(path=os.path.relpath(path, FIX)):
                    self.assertEqual(fmdesign.lint([path]), [])

    def test_rules_have_id_why_fix(self):
        for r in fmdesign.RULES:
            self.assertTrue(r["id"] and r["why"] and r["fix"], r)

    def test_verb_exits_1_with_rule_file_line_and_fix(self):
        slop = os.path.join(FIX, "img-alt", "slop.html")
        p = self.fm("design", "lint", slop, check=False)
        self.assertEqual(p.returncode, 1, p.stderr)
        self.assertIn(f"{slop}:5: img-alt", p.stdout)
        self.assertIn("fix:", p.stdout)
        data = json.loads(self.fm("design", "lint", slop, "--json", check=False).stdout)
        self.assertEqual(data["findings"][0]["rule"], "img-alt")

    def test_verb_clean_exits_0(self):
        p = self.fm("design", "lint", os.path.join(FIX, "img-alt", "crafted.html"))
        self.assertIn("clean", p.stdout)

    def test_missing_path_is_an_error_not_clean(self):
        p = self.fm("design", "lint", os.path.join(self.tmp, "nope"), check=False)
        self.assertEqual(p.returncode, 2)

    def test_help_lists_every_rule(self):
        out = self.fm("design", "--help").stdout
        for r in fmdesign.RULES:
            self.assertIn(r["id"], out)
            self.assertIn(r["why"], " ".join(out.split()))

    def test_a_worker_of_fm_code_may_run_it(self):
        p = self.fm("design", "lint", os.path.join(FIX, "img-alt", "crafted.html"), env={"FOREMAN_WORKER_OF": "run-1"})
        self.assertIn("clean", p.stdout)


class Allow(ForemanTestCase):  # and the edges of what gets linted
    def write(self, name, text):
        path = os.path.join(self.tmp, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path

    def test_allow_with_a_reason_silences_one_finding(self):
        path = self.write("a.html", '<!-- design-lint: allow img-alt the caption below describes it -->\n'
                                    '<img src="a.png">\n<img src="b.png">\n')
        self.assertEqual([(f["rule"], f["line"]) for f in fmdesign.lint([path])], [("img-alt", 3)])

    def test_allow_on_the_same_line(self):
        path = self.write("a.html", '<img src="a.png"> <!-- design-lint: allow img-alt decorative in a figure -->\n')
        self.assertEqual(fmdesign.lint([path]), [])

    def test_allow_without_a_reason_does_not_silence(self):
        path = self.write("a.html", '<img src="a.png"> <!-- design-lint: allow img-alt -->\n')
        self.assertEqual([f["rule"] for f in fmdesign.lint([path])], ["img-alt"])

    def test_allow_names_its_rule(self):
        path = self.write("a.html", '<img src="a.png"> <!-- design-lint: allow flash not this one -->\n')
        self.assertEqual([f["rule"] for f in fmdesign.lint([path])], ["img-alt"])

    def test_directory_walk_skips_vendored_and_other_types(self):
        os.makedirs(os.path.join(self.tmp, "ui", "node_modules"))
        self.write(os.path.join("ui", "node_modules", "x.html"), '<img src="a.png">\n')
        self.write(os.path.join("ui", "x.py"), '<img src="a.png">\n')
        b = self.write(os.path.join("ui", "b.vue"), '<template><img src="a.png"></template>\n')
        self.assertEqual([f["file"] for f in fmdesign.lint([os.path.join(self.tmp, "ui")])], [b])


    def test_same_line_allow_covers_only_its_line(self):
        path = self.write("a.html", '<img src="a.png"> <!-- design-lint: allow img-alt decorative -->\n'
                                    '<img src="b.png">\n')
        self.assertEqual([(f["rule"], f["line"]) for f in fmdesign.lint([path])], [("img-alt", 2)])

    def test_fifo_and_device_link_neither_hang_nor_count(self):
        ui = os.path.join(self.tmp, "ui")
        os.makedirs(ui)
        os.mkfifo(os.path.join(ui, "pipe.css"))
        os.symlink("/dev/zero", os.path.join(ui, "zero.css"))
        self.write(os.path.join("ui", "a.css"), ".a { color: red; }\n")
        p = self.fm("design", "lint", ui, "--json")
        data = json.loads(p.stdout)
        self.assertEqual((data["files"], data["findings"]), (1, []))
        self.assertIn(os.path.join(ui, "zero.css"), [x["file"] for x in data["skipped"]])

    @unittest.skipIf(os.geteuid() == 0, "root reads everything")
    def test_unreadable_file_is_skipped_not_a_crash(self):
        path = self.write("b.css", ".b { color: red; }\n")
        self.write("a.css", ".a { color: red; }\n")
        os.chmod(path, 0)
        p = self.fm("design", "lint", self.tmp + "/a.css", path, "--json")
        self.assertEqual([x["file"] for x in json.loads(p.stdout)["skipped"]], [path])

    def test_a_brace_inside_a_string_doesnt_end_the_block(self):
        # T-1507 review: content: "}" closed @keyframes early, so its 50% frame fell outside and the flash went unseen
        path = self.write("a.css", '@keyframes blink { 0% { content: "}"; } 50% { opacity: 0; } }\n'
                                   ".alert { animation: blink .2s infinite; }\n"
                                   "@media (prefers-reduced-motion: reduce) { .alert { animation: none; } }\n"
                                   ".x { content: '{'; }\n@keyframes grow { to { width: 10px; } }\n")
        self.assertEqual(sorted((f["rule"], f["line"]) for f in fmdesign.lint([path])),
                         [("flash", 2), ("layout-animation", 5)])

    def test_the_same_file_twice_counts_once(self):
        path = self.write("a.css", "".join(f".c{i} {{ border-radius: 8px; }}\n" for i in range(3)))
        self.assertEqual(fmdesign.lint([path, path, os.path.join(self.tmp, ".", "a.css")]), [])

    def test_build_output_and_environments_are_skipped(self):
        for d in ("build", "out", "target", "venv", ".venv", "bower_components"):
            os.makedirs(os.path.join(self.tmp, d))
            self.write(os.path.join(d, "x.html"), '<img src="a">\n')
        self.write("ok.html", '<img src="a" alt="">\n')
        self.assertEqual(fmdesign.lint([self.tmp]), [])

    def test_file_count_is_capped(self):
        for n in range(3):
            self.write(f"{n}.html", '<img src="a">\n')
        old, fmdesign.MAX_FILES = fmdesign.MAX_FILES, 2
        try:
            found, linted, skipped, *_ = fmdesign.run([self.tmp])
        finally:
            fmdesign.MAX_FILES = old
        self.assertEqual((len(found), len(linted)), (2, 2))
        self.assertIn("over 2 files", skipped[0]["why"])

    def test_a_path_with_no_ui_files_exits_2(self):
        self.write("gen.py", "x = 1\n")
        p = self.fm("design", "lint", self.tmp, check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("no UI files under", p.stderr)

    def test_tailwind_font_sans_counts_unless_the_config_sets_fonts(self):
        self.write("a.html", '<body class="font-sans"></body>\n')
        self.assertEqual([f["rule"] for f in fmdesign.lint([self.tmp])], ["generic-font"])
        self.write("tailwind.config.js", "module.exports = { theme: { fontFamily: { sans: ['Brand'] } } };\n")
        self.assertEqual(fmdesign.lint([self.tmp]), [])

    def test_commented_reduced_motion_hook_does_not_count(self):
        path = self.write("a.tsx", "/* useReducedMotion */\n// prefers-reduced-motion\n"
                                   "const C = () => <div style={{ transition: 'transform .2s' }} />;\n")
        self.assertEqual([f["rule"] for f in fmdesign.lint([path])], ["reduced-motion"])

    def test_each_img_on_a_line_is_judged(self):
        path = self.write("a.html", '<img src="a.png" alt=""><img src="b.png">\n<img src="c.png" alt="c">\n')
        self.assertEqual([(f["rule"], f["line"]) for f in fmdesign.lint([path])], [("img-alt", 1)])

    def test_hostile_input_stays_linear(self):
        import time
        paths = [self.write("a.html", "<img {" * 50000 + "<style>" * 50000 + "<!--" * 50000),
                 self.write("b.css", "x{font:" + "1" * 200000 + "px a}" + "/*" * 50000),
                 self.write("c.css", "@keyframes k{" * 50000),
                 self.write("d.tsx", "className={`" * 40000 + "import {" * 40000 + "cn(" * 40000 +
                            "const X = () => { Math.random(); " * 2000 + "{" * 100000)]
        t = time.process_time()
        fmdesign.lint(paths)
        self.assertLess(time.process_time() - t, 5)  # CPU: in-process complexity bar

    def test_non_ui_files_are_not_linted(self):
        self.assertEqual(fmdesign.lint([self.write("gen.py", "x = Math.random()\n")]), [])

    def test_alt_in_a_value_is_not_an_alt(self):
        path = self.write("a.html", '<img src="alt.png" data-alt="x">\n')
        self.assertEqual([f["rule"] for f in fmdesign.lint([path])], ["img-alt"])


class UnusedTokens(ForemanTestCase):
    """T-1874: fm design lint names the DESIGN.md tokens no linted file uses; report only."""

    def put(self, name, text):
        path = os.path.join(self.repo, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path

    def test_lint_names_tokens_no_linted_file_uses_and_keeps_its_exit(self):
        rows = "".join(f"| `--{n}` | colour | `#112233` | `#445566` |\n" for n in
                       ("surface", "text", "color-brand", "spare", "color-ghost", "text-2"))
        self.put("DESIGN.md", "# App\n\n## Tokens\n\n| Token | Kind | Light | Dark |\n|---|---|---|---|\n" + rows)
        self.put("ui/app.css", ":root { --surface: #fff; --spare: #000; --text-2: #333; }\n"
                               "body { background: var(--surface); color: var( --text , #111); }\n")
        self.put("ui/App.jsx", 'export const A = () => <b className="bg-brand md:text-brand/50">hi</b>;\n')
        r = self.fm("design", "lint", "ui")
        self.assertEqual(r.returncode, 0, r.stdout)  # report only: a clean lint stays clean
        self.assertIn("DESIGN.md: 3 token(s) unused in the 2 file(s) linted: --spare, --color-ghost, --text-2",
                      r.stdout)  # a definition isn't a use; --text isn't --text-2; bg-brand uses --color-brand
        d = json.loads(self.fm("design", "lint", "ui", "--json").stdout)
        self.assertEqual(d["unused_tokens"], ["--spare", "--color-ghost", "--text-2"])
        self.put("ui/more.css", "a { color: var(--spare); border-color: var(--text-2) }\n")
        self.put("ui/tailwind.config.js", "module.exports = {theme: {colors: {ghost: 'hsl(var(--color-ghost))'}}}\n")
        self.assertNotIn("unused", self.fm("design", "lint", "ui").stdout)
        mine = self.put("elsewhere/TOKENS.md", "# Mine\n\n## Tokens\n\n| Token | Kind | Light | Dark |\n|---|---|---|---|\n"
                                               "| `--only` | colour | `#000000` | `#ffffff` |\n")
        self.assertIn("TOKENS.md: 1 token(s) unused", self.fm("design", "lint", "ui", "--tokens", mine).stdout)
        os.remove(os.path.join(self.repo, "DESIGN.md"))
        self.assertNotIn("token(s)", self.fm("design", "lint", "ui").stdout)  # no DESIGN.md: nothing said
        self.put("DESIGN.md", "# App\n\n## Direction\n\nquiet\n")
        self.assertNotIn("token(s)", self.fm("design", "lint", "ui").stdout)  # no ## Tokens: nothing said
        r = self.fm("design", "lint", "ui", "--tokens", os.path.join(self.repo, "DESIGN.md"), check=False)
        self.assertEqual((r.returncode, "--tokens:" in r.stderr, "Traceback" in r.stderr), (2, True, False), r.stderr)

    def test_unused_tokens_reads_tailwind_theme_names_and_breakpoints(self):
        texts = ['<div class="md:flex rounded-xl font-display max-sm:hidden">', ".a{color:var(--x)} .b{--y: 1px}"]
        self.assertEqual(fmdesign.unused_tokens(["--breakpoint-md", "--radius-xl", "--font-display", "--x", "--y",
                                                 "--breakpoint-lg", "--shadow-xl", "--breakpoint-sm"], texts),
                         ["--y", "--breakpoint-lg"])  # rounded-xl ends -xl, so --shadow-xl reads as used (the ceiling)


class Site(unittest.TestCase):
    def test_foremans_own_site_is_clean(self):
        found = fmdesign.lint([SITE])
        self.assertEqual(found, [], "\n".join(fmdesign.render(found)))


if __name__ == "__main__":
    unittest.main()
