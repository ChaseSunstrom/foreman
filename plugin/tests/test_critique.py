"""T-1642: fm critique URL|FILE takes a computed-style census of a page (every colour, font, size, radius, shadow and
spacing value in use, with counts) from a browser already here, or from a census JSON file, and critiques it against
DESIGN.md's tokens: values no token names, near-duplicates and outliers. --why SELECTOR prints the cascade behind one
element's look. Census and Cascade run on canned data; InABrowser on a real one when there is one."""
import json
import os
import unittest

from helpers import ForemanTestCase

import fmcritique
import fmshot

DESIGN = """# DESIGN.md

## Tokens

| Token | Kind | Light | Dark | Source |
|---|---|---|---|---|
| `--ink` | colour | `#1a1a1a` #1A1A1A |  | ui/t.css:2 |
| `--paper` | colour | `#ffffff` #FFFFFF | `#111111` #111111 | ui/t.css:3 |
| `--accent` | colour | `oklch(0.5 0.15 260)` #3366CC |  | ui/t.css:4 |
| `--font-body` | font | `Inter, sans-serif` |  | ui/t.css:5 |
| `--font-size-base` | font | `1rem` |  | ui/t.css:6 |
| `--radius` | length | `8px` |  | ui/t.css:7 |
| `--space-2` | length | `0.5rem` |  | ui/t.css:8 |
| `--space-4` | length | `16px` |  | ui/t.css:9 |
| `--shadow-1` | shadow | `0 1px 2px rgba(0,0,0,.1)` |  | ui/t.css:10 |
"""

CENSUS = {"url": "https://example.test/", "elements": 120, "values": {
    "colour": {"rgb(26, 26, 26)": 80, "rgb(255, 255, 255)": 40, "rgb(51, 102, 204)": 12, "rgb(52, 102, 205)": 3,
               "rgb(225, 29, 72)": 1},
    "font": {"Inter, sans-serif": 100, "\"Comic Sans MS\", cursive": 1},
    "size": {"16px": 90, "15px": 4},
    "radius": {"8px": 10, "8px 4px": 3, "calc(1px + 2px)": 3},
    "shadow": {"rgba(0, 0, 0, 0.1) 0px 1px 2px 0px": 5},
    "spacing": {"8px": 30, "16px": 20, "13px": 2}}}


class Case(ForemanTestCase):
    def setUp(self):
        super().setUp()
        with open(os.path.join(self.repo, "DESIGN.md"), "w") as f:
            f.write(DESIGN)

    def census_file(self, data=CENSUS, name="census.json"):
        path = os.path.join(self.tmp, name)
        with open(path, "w") as f:
            json.dump(data, f)
        return path


class Census(Case):
    def test_a_canned_census_lists_the_styles_in_use_and_flags_what_design_md_does_not_name(self):
        r = self.fm("critique", self.census_file(), check=False)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)  # findings: exit 1
        out = r.stdout
        self.assertIn("#1A1A1A ×80 --ink", out)  # the census, each value with its count and the token naming it
        self.assertIn("16px ×90", out)
        unnamed = out.split("Not named by DESIGN.md")[1].split("\n\n")[0]
        self.assertIn("#E11D48", unnamed)
        self.assertIn("comic sans ms", unnamed)
        self.assertIn("15px", unnamed)
        self.assertIn("13px", unnamed)
        listed = {ln.strip().split(" ", 1)[1].rsplit(" ×", 1)[0] for ln in unnamed.splitlines()[1:]}
        for named in ("#1A1A1A", "#3366CC", "inter", "16px", "8px"):  # 0.5rem and 1rem are 8px and 16px
            self.assertNotIn(named, listed)
        self.assertNotIn("shadow", unnamed)  # the computed form of --shadow-1 is still --shadow-1

    def test_findings_in_json(self):
        data = json.loads(self.fm("critique", self.census_file(), "--json", check=False).stdout)
        unnamed = {(u["kind"], u["value"]) for u in data["unnamed"]}
        self.assertEqual(unnamed, {("colour", "#3466CD"), ("colour", "#E11D48"), ("font", "comic sans ms"),
                                   ("size", "15px"), ("spacing", "13px"), ("radius", "8px 4px"),
                                   ("radius", "calc(1px + 2px)")})  # read as text, never as a length
        near = {(n["kind"], n["a"], n["b"]) for n in data["near"]}
        self.assertIn(("colour", "#3366CC", "#3466CD"), near)
        self.assertIn(("size", "16px", "15px"), near)
        self.assertNotIn(("spacing", "16px", "13px"), near)
        rare = {(o["kind"], o["value"]) for o in data["outliers"]}
        self.assertEqual(rare, {("colour", "#E11D48"), ("font", "comic sans ms"), ("spacing", "13px")})
        self.assertEqual(data["tokens"], 9)

    def test_without_design_md_it_still_finds_near_duplicates_and_outliers(self):
        os.unlink(os.path.join(self.repo, "DESIGN.md"))
        data = json.loads(self.fm("critique", self.census_file(), "--json", check=False).stdout)
        self.assertEqual(data["unnamed"], [])
        self.assertIn("no DESIGN.md", " ".join(data["notes"]))
        self.assertTrue(data["near"])

    def test_page_text_is_cleaned_and_capped(self):
        evil = {"url": "https://x.test/\x1b[2J", "elements": 1, "values": {
            "font": {"\x1b]0;pwned\x07Evil" + "x" * 5000: 1},
            "colour": {f"rgb({i % 256}, {i // 256}, 0)": 1 for i in range(5000)}}}
        r = self.fm("critique", self.census_file(evil), check=False)
        self.assertEqual(r.returncode, 1)
        self.assertNotIn("\x1b", r.stdout)
        self.assertNotIn("\x07", r.stdout)
        self.assertLess(len(r.stdout), 20000)
        self.assertNotIn("x" * 200, r.stdout)

    def test_a_clean_census_exits_0(self):
        clean = {"url": "file:///p.html", "elements": 3, "values": {"colour": {"rgb(26, 26, 26)": 3},
                                                                    "spacing": {"8px": 4, "16px": 4}}}
        r = self.fm("critique", self.census_file(clean))
        self.assertIn("clean", r.stdout)

    def test_a_malformed_census_is_refused(self):
        for bad in ([1, 2], {"values": {"colour": {"red": "many"}}}, {"values": "x"}):
            r = self.fm("critique", self.census_file(bad), check=False)
            self.assertEqual(r.returncode, 2, bad)
            self.assertIn("census", r.stderr)
        r = self.fm("critique", self.census_file(CENSUS), "--why", "p", check=False)
        self.assertEqual(r.returncode, 2)  # --why needs a page, not a census

    def test_no_browser_says_not_run(self):
        page = os.path.join(self.repo, "p.html")
        with open(page, "w") as f:
            f.write("<p>hi</p>")
        empty = os.path.join(self.tmp, "empty")
        os.makedirs(empty)
        env = {"FOREMAN_CHROME": "", "PATH": empty, "HOME": empty, "PLAYWRIGHT_BROWSERS_PATH": empty}
        r = self.fm("critique", page, env=env, check=False)
        self.assertEqual(r.returncode, 2)
        self.assertIn("not run", r.stdout)
        self.assertIn("no browser", r.stdout)

    def test_only_files_and_localhost_unless_any_url(self):
        empty = os.path.join(self.tmp, "empty")
        os.makedirs(empty)
        env = {"FOREMAN_CHROME": "", "PATH": empty, "HOME": empty, "PLAYWRIGHT_BROWSERS_PATH": empty}
        for url in ("https://example.com/", "javascript:alert(1)", "http://user@localhost/", "data:text/html,x"):
            r = self.fm("critique", url, env=env, check=False)
            self.assertEqual(r.returncode, 2, url)
            self.assertNotIn("not run", r.stdout, url)  # refused before any browser is looked for
            self.assertIn("localhost", r.stderr, url)
        r = self.fm("critique", "https://example.com/", "--any-url", env=env, check=False)
        self.assertIn("not run", r.stdout)  # allowed: it got as far as looking for a browser

    def test_an_explicit_design_that_cannot_be_read_exits_2(self):
        r = self.fm("critique", self.census_file(), "--design", os.path.join(self.tmp, "nope.md"), check=False)
        self.assertEqual(r.returncode, 2)
        self.assertIn("nope.md", r.stderr)
        bare = os.path.join(self.tmp, "BARE.md")
        with open(bare, "w") as f:
            f.write("# DESIGN.md\n\n## Direction\n\nCalm.\n")
        r = self.fm("critique", self.census_file(), "--design", bare, check=False)
        self.assertEqual(r.returncode, 2)
        self.assertIn("## Tokens", r.stderr)

    def test_no_tokens_says_not_checked_against_design_md(self):
        with open(os.path.join(self.repo, "DESIGN.md"), "w") as f:
            f.write("# DESIGN.md\n\n## Direction\n\nCalm.\n")
        clean = {"url": "file:///p.html", "elements": 3, "values": {"colour": {"rgb(26, 26, 26)": 3}}}
        r = self.fm("critique", self.census_file(clean))
        last = r.stdout.strip().splitlines()[-1]
        self.assertIn("not checked against DESIGN.md", last)

    def test_values_the_page_dropped_are_noted(self):
        data = json.loads(self.fm("critique", self.census_file(dict(CENSUS, dropped={"colour": 5, "font": 2})),
                                  "--json", check=False).stdout)
        self.assertIn("7 more value(s)", " ".join(data["notes"]))

    def test_near_duplicates_use_a_relative_bound_and_keep_the_true_count(self):
        res = fmcritique.critique(fmcritique.load({"values": {"spacing": {"1px": 9, "2px": 9, "100px": 5,
                                                                            "106px": 5, "120px": 1}}}))
        self.assertEqual({(n["a"], n["b"]) for n in res["near"]}, {("100px", "106px")})
        many = {"values": {"colour": {f"rgb(100, 100, {100 + i})": 1 for i in range(40)}}}
        res = fmcritique.critique(fmcritique.load(many))
        self.assertEqual(len(res["near"]), fmcritique.MAX_NEAR)
        self.assertGreater(res["near_total"], fmcritique.MAX_NEAR)


class Pseudo(unittest.TestCase):
    def test_longer_bracketed_and_placeholders_kept(self):
        for s in ("Save changes", "Hello {name}, you have %d items", "Delete %(n)s files <b>now</b> ${x}", "{0} of {1}"):
            p = fmcritique.pseudo(s)
            self.assertGreaterEqual(len(p), len(s) * 1.3, s)
            self.assertTrue(p.startswith("[") and p.endswith("]"), p)
            for ph in fmcritique.PLACEHOLDER.findall(s):
                self.assertIn(ph, p)
        self.assertNotIn("Save", fmcritique.pseudo("Save changes"))

    def test_empty_and_huge(self):
        self.assertEqual(fmcritique.pseudo(""), "")
        self.assertLessEqual(len(fmcritique.pseudo("a" * 10**6)), fmcritique.MAX_STRESS * 2 + 20)

    def test_profiles(self):
        for name, p in fmcritique.PROFILES.items():
            self.assertTrue(p["width"] > 0 and p["height"] > 0 and p["scale"] > 0, name)
        self.assertEqual(set(fmcritique.PROFILES), {"tv", "eink", "car", "wrist"})


class Clean(unittest.TestCase):
    def test_format_and_private_characters_are_stripped(self):
        for ch in ("\U000E0041", "⁠", "⁤", "﻿", "­", "؜", "", "‮", "\x1b", "\x85"):
            self.assertNotIn(ch, fmcritique.clean(f"a{ch}b"), repr(ch))
            self.assertNotIn(ch, fmshot.safe(f"a{ch}b"), repr(ch))
        self.assertEqual(fmcritique.clean("Inter Ünïcode"), "Inter Ünïcode")


class Cascade(unittest.TestCase):
    """CSS.getMatchedStylesForNode's answer, cut down: rules lowest precedence first, inline style last."""
    MATCHED = {
        "inlineStyle": {"cssProperties": [{"name": "padding-top", "value": "2px"}]},
        "matchedCSSRules": [
            {"rule": {"origin": "user-agent", "selectorList": {"selectors": [{"text": "p"}]},
                      "style": {"cssProperties": [{"name": "margin-top", "value": "1em"},
                                                  {"name": "display", "value": "block"}]}}, "matchingSelectors": [0]},
            {"rule": {"origin": "regular", "selectorList": {"selectors": [{"text": ".x"}, {"text": ".card p"}]},
                      "style": {"styleSheetId": "s1", "range": {"startLine": 11},
                                "cssProperties": [{"name": "margin-top", "value": "0", "important": True},
                                                  {"name": "padding-top", "value": "9px"},
                                                  {"name": "color", "value": "red", "parsedOk": False}]}},
             "matchingSelectors": [1]},
            {"rule": {"origin": "regular", "selectorList": {"selectors": [{"text": "p"}]},
                      "style": {"cssProperties": [{"name": "margin-top", "value": "4px"}]}}, "matchingSelectors": [0]}],
        "inherited": [{"matchedCSSRules": [
            {"rule": {"origin": "regular", "selectorList": {"selectors": [{"text": "body"}]},
                      "style": {"cssProperties": [{"name": "color", "value": "var(--ink)"},
                                                  {"name": "margin-left", "value": "3px"}]}},
             "matchingSelectors": [0]}]}]}

    def test_the_winning_declaration_per_property(self):
        win = {w["property"]: w for w in fmcritique.cascade(self.MATCHED)["winners"]}
        self.assertEqual(win["margin-top"]["value"], "0")  # !important beats the later 4px
        self.assertEqual(win["margin-top"]["selector"], ".card p")
        self.assertEqual(win["padding-top"]["selector"], "style attribute")  # inline beats a rule
        self.assertEqual(win["display"]["origin"], "user-agent")
        self.assertEqual(win["color"]["value"], "var(--ink)")  # unparsed red skipped; inherited from body
        self.assertTrue(win["color"]["inherited"])
        self.assertNotIn("margin-left", win)  # margins don't inherit
        rules = fmcritique.cascade(self.MATCHED)["rules"]
        self.assertEqual([r["selector"] for r in rules], ["style attribute", "p", ".card p", "p"])  # winner first
        self.assertEqual(rules[2]["line"], 12)

    def test_stylesheet_sources_and_layers(self):
        sheets = {"s1": {"sourceURL": "https://x.test/css/site.css?v=2", "isInline": False, "startLine": 0}}
        res = fmcritique.cascade(self.MATCHED, sheets=sheets)
        self.assertEqual(res["rules"][2]["source"], "site.css:12")
        self.assertEqual(res["notes"], [])
        layered = json.loads(json.dumps(self.MATCHED))
        layered["matchedCSSRules"][1]["rule"]["layers"] = [{"text": "base"}]
        self.assertIn("@layer", " ".join(fmcritique.cascade(layered)["notes"]))

    def test_the_report_is_capped(self):
        rules = [{"selector": f".r{i}", "origin": "regular", "line": i, "source": None, "inherited": False}
                 for i in range(50)]
        winners = [dict(rules[0], property=f"--p{i}", value="1", important=False, computed=None) for i in range(100)]
        text = fmcritique.why_report({"rules": rules, "winners": winners, "notes": []}, "file:///p", "p", [])
        self.assertIn(f"… {50 - fmcritique.WHY_RULES} more (--json)", text)
        self.assertIn(f"… {100 - fmcritique.WHY_WINNERS} more (--json)", text)
        self.assertLess(len(text.splitlines()), fmcritique.WHY_RULES + fmcritique.WHY_WINNERS + 10)


@unittest.skipUnless(fmshot.chrome(), "no headless Chromium here")
class InABrowser(Case):
    def test_a_real_page_census_and_why(self):
        page = os.path.join(self.repo, "p.html")
        with open(page, "w") as f:
            f.write("<style>:root{--ink:#1a1a1a} body{color:var(--ink);font-family:Inter,sans-serif;margin:16px}"
                    ".card{padding:8px;border-radius:8px;background:#e11d48} .card p{margin:0 !important}"
                    "p{margin:4px}</style><div class=card><p id=t>hi</p></div>")
        data = json.loads(self.fm("critique", page, "--json", check=False).stdout)
        self.assertIn("#E11D48", {u["value"] for u in data["unnamed"]}, data)
        self.assertEqual(data["census"]["values"]["colour"]["#1A1A1A"], 1)
        why = self.fm("critique", page, "--why", "#t").stdout
        self.assertIn(".card p", why)
        self.assertIn("margin-top: 0px !important  ← .card p", why)  # the longhand, beating the later p's 4px
        self.assertNotIn("style attribute", why)  # #t has none
        self.assertIn("color: var(--ink)", why)
        self.assertIn("p.html:1", why)  # the rule's stylesheet: the page's own <style>
        r = self.fm("critique", page, "--why", "#nope", check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn("matches nothing", r.stdout + r.stderr)

    def test_frozen_before_the_census_blocked_requests_and_a_moved_page_noted(self):
        page = os.path.join(self.repo, "a.html")
        with open(page, "w") as f:
            f.write("<style>@keyframes k{from{background:#ff0000}to{background:#00ff00}}"
                    "div{height:40px;animation:k 30s forwards}</style><div></div>"
                    "<img src='http://example.com/x.png'><script>history.replaceState(null, '', '#moved')</script>")
        data = json.loads(self.fm("critique", page, "--json", check=False).stdout)
        colours = data["census"]["values"]["colour"]
        self.assertIn("#00FF00", colours, colours)  # the finite animation finished, as fm shot --frozen holds it
        self.assertNotIn("#FF0000", colours)
        notes = " ".join(data["notes"])
        self.assertIn("blocked http://example.com/x.png", notes)
        self.assertIn("#moved", notes)  # location.href differs from the URL asked for


if __name__ == "__main__":
    unittest.main()
