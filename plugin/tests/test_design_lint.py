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


    def test_each_img_on_a_line_is_judged(self):
        path = self.write("a.html", '<img src="a.png" alt=""><img src="b.png">\n<img src="c.png" alt="c">\n')
        self.assertEqual([(f["rule"], f["line"]) for f in fmdesign.lint([path])], [("img-alt", 1)])

    def test_hostile_input_stays_linear(self):
        import time
        paths = [self.write("a.html", "<img {" * 50000 + "<style>" * 50000 + "<!--" * 50000),
                 self.write("b.css", "x{font:" + "1" * 200000 + "px a}" + "/*" * 50000),
                 self.write("c.css", "@keyframes k{" * 50000)]
        t = time.monotonic()
        fmdesign.lint(paths)
        self.assertLess(time.monotonic() - t, 5)

    def test_non_ui_files_are_not_linted(self):
        self.assertEqual(fmdesign.lint([self.write("gen.py", "x = Math.random()\n")]), [])

    def test_alt_in_a_value_is_not_an_alt(self):
        path = self.write("a.html", '<img src="alt.png" data-alt="x">\n')
        self.assertEqual([f["rule"] for f in fmdesign.lint([path])], ["img-alt"])


class Site(unittest.TestCase):
    def test_foremans_own_site_is_clean(self):
        found = fmdesign.lint([SITE])
        self.assertEqual(found, [], "\n".join(fmdesign.render(found)))


if __name__ == "__main__":
    unittest.main()
