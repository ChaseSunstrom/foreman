"""T-1640: fm stories CHART builds one page with a cell per state a state chart lists (default, hover, error…), each
state reached by fm flow steps and shot through fmshot.Browser; with no browser the page lists the states and says why.
Stories drives test_flow's stub browser (taught to answer Page.captureScreenshot); Untrusted feeds it hostile charts;
InABrowser uses a real Chromium."""
import argparse
import contextlib
import io
import json
import os
import re
import stat
import time
import unittest
from unittest import mock

from helpers import ForemanTestCase

import fmshot
import fmstories
import test_flow

PNG = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
HOOK = '        elif msg["method"] == "Input.insertText":'
assert HOOK in test_flow.STUB
STUB = test_flow.STUB.replace(HOOK, f'        elif msg["method"] == "Page.captureScreenshot":\n'
                                    f'            res = {{"data": os.environ.get("STUB_PNG", {PNG!r})}}\n{HOOK}')
CHART = {"component": "Sign-up form", "page": "form.html", "states": [
    {"name": "default"},
    {"name": "hover", "steps": ["goto form.html?state=hover"]},
    {"name": "error", "steps": ['type "#email" bad', 'click "#go"', 'expect "#err" "invalid"']}]}
CELL = re.compile(r'<figure class="cell" data-state="([^"]*)"')


class StubCase(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        with open(os.path.join(self.repo, "form.html"), "w") as f:
            f.write("<p>form</p>")
        self.log = os.path.join(self.tmp, "stub.jsonl")
        self.stub = os.path.join(self.tmp, "chrome")
        with open(self.stub, "w") as f:
            f.write(STUB)
        os.chmod(self.stub, stat.S_IRWXU)
        self.out = os.path.join(self.repo, "matrix.html")

    def env(self, **more):
        dom = {"#email": "", "#go": "Go"}
        return dict({"FOREMAN_CHROME": self.stub, "STUB_LOG": self.log, "STUB_DOM": json.dumps(dom),
                     "STUB_CLICK": json.dumps({"#go": {"#err": "Email is invalid"}})}, **more)

    def no_browser(self):
        empty = os.path.join(self.tmp, "empty")
        os.makedirs(empty, exist_ok=True)
        return {"FOREMAN_CHROME": "", "PATH": empty, "HOME": empty, "PLAYWRIGHT_BROWSERS_PATH": empty}

    def stories(self, chart, *args, env=None, raw=False):
        path = os.path.join(self.repo, "form.chart.json")
        with open(path, "w") as f:
            f.write(chart if raw else json.dumps(chart))
        return self.fm("stories", path, *(args or ("--out", self.out)), env=dict(self.env(), **(env or {})),
                       check=False)

    def page(self):
        with open(self.out, encoding="utf-8") as f:
            return f.read()

    def calls(self, method):
        with open(self.log) as f:
            return [x["params"] for x in map(json.loads, f) if x["method"] == method]


class Stories(StubCase):
    def test_a_chart_of_3_states_builds_a_page_with_3_cells(self):
        r = self.stories(CHART, "--out", self.out, "--json")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        data = json.loads(r.stdout)
        self.assertEqual([s["name"] for s in data["states"]], ["default", "hover", "error"])
        self.assertTrue(all(s["shot"] for s in data["states"]), data)
        page = self.page()
        self.assertEqual(CELL.findall(page), ["default", "hover", "error"])
        self.assertEqual(page.count('src="data:image/png;base64,' + PNG), 3)
        urls = [c["url"] for c in self.calls("Page.navigate")]
        self.assertEqual(urls[::2], ["about:blank"] * 3)  # a fresh page each state: a #fragment goto reloads too
        self.assertEqual(len(urls), 6)  # each state starts from the page: goto form.html prepended
        self.assertTrue(urls[1].startswith("file:///") and urls[1].endswith("/form.html"), urls)
        self.assertTrue(urls[3].endswith("/form.html?state=hover"), urls)
        self.assertEqual(self.calls("Input.insertText"), [{"text": "bad"}])
        self.assertEqual(len(self.calls("Page.captureScreenshot")), 3)

    def test_the_page_is_one_file_that_loads_nothing_from_another_host(self):
        self.assertEqual(self.stories(CHART).returncode, 0)
        page = self.page()
        self.assertIn("default-src 'none'", page)  # a CSP: only inline style and data: images
        self.assertNotRegex(page, r"(?i)(src|href)=\"(?!data:|#)")
        self.assertNotRegex(page, r"(?i)https?://|@import|url\(")
        self.assertIn("Sign-up form", page)

    def test_with_no_browser_the_page_lists_the_states_says_why_and_exits_2(self):
        r = self.stories(CHART, "--out", self.out, "--json", env=self.no_browser())
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)  # no step ran: never a pass
        self.assertFalse(json.loads(r.stdout)["ok"])
        r = self.stories(CHART, env=self.no_browser())
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn("no browser", r.stdout)
        self.assertIn("not run, not a pass", r.stdout)
        page = self.page()
        self.assertEqual(CELL.findall(page), ["default", "hover", "error"])
        self.assertNotIn("<img", page)
        self.assertIn("no browser found", page)
        self.assertIn("type &quot;#email&quot; bad", page)  # how to reach each state, listed
        self.assertFalse(os.path.exists(self.log))

    def test_a_browser_that_never_starts_still_writes_the_listing_and_exits_2(self):
        fake = os.path.join(self.tmp, "not-a-browser")
        with open(fake, "w") as f:
            f.write("x")
        os.chmod(fake, stat.S_IRWXU)
        r = self.stories(CHART, env=dict(self.no_browser(), FOREMAN_CHROME=fake))
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn("did not start", r.stdout)
        self.assertIn("not run, not a pass", r.stdout)
        self.assertEqual(CELL.findall(self.page()), ["default", "hover", "error"])

    def test_the_whole_run_has_a_deadline_inside_a_state_too(self):
        chart = {"page": "form.html", "states": [{"name": "slow", "steps": ["wait 400"] * 5}, {"name": "next"}]}
        path = os.path.join(self.repo, "slow.json")
        with open(path, "w") as f:
            json.dump(chart, f)
        args = argparse.Namespace(chart=path, out=self.out, json=True, project=None)
        out, code, start = io.StringIO(), 0, time.monotonic()
        with mock.patch.dict(os.environ, self.env()), mock.patch.object(fmstories, "TOTAL_S", 1), \
                contextlib.redirect_stdout(out):
            try:
                fmstories.cmd_stories(args)
            except SystemExit as e:
                code = e.code
        self.assertLess(time.monotonic() - start, 5)
        self.assertEqual(code, 1)
        slow, nxt = json.loads(out.getvalue())["states"]
        self.assertIn("time ran out", slow["error"])
        self.assertIn("not shot: the run passed 1 s", nxt["error"])

    def test_the_inline_shots_have_a_total_cap(self):
        png = fmstories.PNG_MAGIC + b"x" * 70
        chart = {"title": "t", "states": [{"name": n, "lines": [], "png": png} for n in ("a", "b")]}
        with mock.patch.object(fmstories, "MAX_TOTAL_PNG", 100):
            page = fmstories.page_html(chart, "note")
        self.assertEqual(page.count("<img"), 1)
        self.assertIn("not inlined: the shots in all passed", page)

    def test_a_state_whose_steps_fail_is_named_and_the_run_exits_1(self):
        chart = dict(CHART, states=CHART["states"] + [{"name": "gone", "steps": ['expect "#nope"']}])
        r = self.stories(chart)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("✗ gone", r.stdout)
        self.assertIn("no element matches #nope", r.stdout)
        page = self.page()
        self.assertEqual(CELL.findall(page), ["default", "hover", "error", "gone"])
        self.assertIn("no element matches #nope", page)
        self.assertEqual(page.count("<img"), 4)  # shot as it stood, the failure beside it

    def test_the_default_path_is_in_the_project_state_and_a_rerun_replaces_it(self):
        r = self.stories(CHART, "--json")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        path = json.loads(r.stdout)["path"]
        self.assertTrue(path.endswith(os.path.join("stories", "form-chart.html")), path)
        self.assertTrue(os.path.isfile(path))
        self.assertEqual(json.loads(self.stories(CHART, "--json").stdout)["path"], path)


class Untrusted(StubCase):
    def test_malformed_charts_are_refused_before_any_browser_starts(self):
        many = [{"name": f"s{i}"} for i in range(fmstories.MAX_STATES + 1)]
        bad = ["not json", "[]", "[" * 30000 + "]" * 30000, {"states": []}, {"page": "form.html"},
               {"page": "form.html", "states": [{}]},
               {"page": "form.html", "states": [{"name": "a"}], "extra": 1},
               {"page": "form.html", "states": [{"name": "a", "colour": "red"}]},
               {"page": "form.html", "states": many},
               {"page": "form.html", "states": [{"name": "a"}, {"name": "A"}]},
               {"page": "form.html", "states": [{"name": "x" * (fmstories.MAX_NAME + 1)}]},
               {"page": "form.html", "states": [{"name": "a\x1b[2J"}]},
               {"page": "form.html", "states": [{"name": "a", "steps": "click a"}]},
               {"page": "form.html", "states": [{"name": "a", "steps": [1]}]},
               {"page": "form.html", "states": [{"name": "a", "steps": ["click a\ngoto https://example.com/"]}]},
               {"page": "form.html", "states": [{"name": "a", "steps": ["eval x"]}]},
               {"page": "form.html", "states": [{"name": "a", "steps": ["click a\u2028goto https://example.com/"]}]},
               {"page": "form.html", "states": [{"name": "a\u2029b"}]},
               {"page": "form.html", "states": [{"name": "a", "steps": ["click a"] * (fmstories.MAX_STEPS + 1)}]},
               {"page": "https://example.com/", "states": [{"name": "a"}]},
               {"page": "../outside.html", "states": [{"name": "a"}]},
               {"states": [{"name": "a", "steps": ["click a"]}]},  # no page and no goto: nowhere to start
               {"page": "form.html", "component": 3, "states": [{"name": "a"}]}]
        for chart in bad:
            r = self.stories(chart, raw=isinstance(chart, str))
            self.assertEqual(r.returncode, 1, chart)
            self.assertIn("fm stories", r.stderr, chart)
            self.assertNotIn("Traceback", r.stderr, chart)
        self.assertFalse(os.path.exists(self.log))
        self.assertFalse(os.path.exists(self.out))
        r = self.stories(" " * (fmstories.MAX_BYTES + 1), raw=True)
        self.assertIn("over", r.stderr)

    def test_names_and_steps_are_escaped_in_the_page(self):
        chart = {"component": "<script>alert(1)</script>", "page": "form.html",
                 "states": [{"name": '"><img src=x onerror=alert(1)>'}]}
        r = self.stories(chart)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        page = self.page()
        self.assertNotIn("<script>alert", page)
        self.assertNotIn("<img src=x", page)

    def test_out_never_replaces_a_file_it_did_not_write_or_a_link(self):
        with open(self.out, "w") as f:
            f.write("<p>mine</p>")
        r = self.stories(CHART)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(self.page(), "<p>mine</p>")
        os.unlink(self.out)
        os.symlink(os.path.join(self.repo, "form.html"), self.out)
        self.assertEqual(self.stories(CHART).returncode, 1)
        os.unlink(self.out)
        self.assertEqual(self.stories(CHART).returncode, 0)
        self.assertEqual(self.stories(CHART).returncode, 0, "its own page is replaced")

    def test_a_screenshot_that_is_not_a_png_is_not_embedded(self):
        r = self.stories(CHART, env={"STUB_PNG": "PHNjcmlwdD4="})  # "<script>"
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertNotIn("<img", self.page())
        self.assertIn("not a PNG", self.page())


@unittest.skipUnless(fmshot.chrome(), "no headless Chromium here")
class InABrowser(ForemanTestCase):
    def test_three_states_in_a_real_browser_are_three_different_shots(self):
        self.fm("init")
        with open(os.path.join(self.repo, "btn.html"), "w") as f:
            f.write('<style>body{margin:40px} .hover{background:#06c;color:#fff} #err{color:#c00}</style>'
                    '<input id="email"><button id="go" onclick="document.getElementById(\'err\').textContent='
                    '\'Email is invalid\'">Go</button><p id="err"></p>'
                    '<script>if (location.search.includes("hover")) document.getElementById("go").className='
                    '"hover"</script>')
        chart = {"page": "btn.html", "states": [
            {"name": "default"}, {"name": "hover", "steps": ["goto btn.html?state=hover"]},
            {"name": "error", "steps": ['type "#email" bad', 'click "#go"', 'expect "#err" invalid']}]}
        path, out = os.path.join(self.repo, "btn.chart.json"), os.path.join(self.repo, "m.html")
        with open(path, "w") as f:
            json.dump(chart, f)
        r = self.fm("stories", path, "--out", out, check=False)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        with open(out, encoding="utf-8") as f:
            page = f.read()
        self.assertEqual(CELL.findall(page), ["default", "hover", "error"])
        shots = re.findall(r'src="data:image/png;base64,([^"]+)"', page)
        self.assertEqual(len(set(shots)), 3)


if __name__ == "__main__":
    unittest.main()
