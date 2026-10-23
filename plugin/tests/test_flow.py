"""T-1639: fm flow FILE runs a user journey (goto, click, type, expect, wait) in the headless Chromium fm shot finds,
as a verify command: exit 1 naming the step that failed, 2 with no browser (never a vacuous pass). Journey drives a
stub browser whose page is a dict of selector → text; Untrusted feeds it hostile flow files; InABrowser uses a real one."""
import json
import os
import stat
import sys
import unittest

from helpers import ForemanTestCase

import fmflow
import fmshot

LIB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib")
# A stand-in for Chromium's --remote-debugging-pipe. Its page: STUB_DOM, a JSON {selector: text}; STUB_CLICK, a JSON
# {selector: {selector: text}} of elements a click adds. Runtime.evaluate must be fmflow's ACT called with JSON
# arguments (anything else is answered as a thrown exception); every call is logged to STUB_LOG.
STUB = f"""#!{sys.executable}
import json, os, sys
sys.path.insert(0, {LIB!r})
import fmflow
log = open(os.environ["STUB_LOG"], "a")
dom = json.loads(os.environ.get("STUB_DOM", "{{}}"))
clicks = json.loads(os.environ.get("STUB_CLICK", "{{}}"))
head, focused, buf = "(" + fmflow.ACT + ")(...", None, b""
def send(msg):
    os.write(4, json.dumps(msg).encode() + b"\\0")
def act(op, sel, text):
    global focused
    if sel.endswith("["):
        return {{"bad": "not a valid selector"}}
    if sel not in dom:
        return {{"missing": True}}
    if op == "click":
        dom.update(clicks.get(sel, {{}}))
    if op == "type":
        focused = sel
    if op == "expect":
        return {{"ok": text is None or text in dom[sel], "text": dom[sel]}}
    return {{"ok": True}}
while True:
    chunk = os.read(3, 65536)
    if not chunk:
        break
    buf += chunk
    while b"\\0" in buf:
        line, buf = buf.split(b"\\0", 1)
        msg = json.loads(line)
        p = msg.get("params", {{}})
        log.write(json.dumps({{"method": msg["method"], "params": p}}) + "\\n")
        log.flush()
        res = {{}}
        if msg["method"] == "Target.createTarget":
            res = {{"targetId": "t1"}}
        elif msg["method"] == "Target.attachToTarget":
            res = {{"sessionId": "s1"}}
        elif msg["method"] == "Page.navigate" and "missing" in p["url"]:
            res = {{"errorText": "net::ERR_FILE_NOT_FOUND"}}
        elif msg["method"] == "Input.insertText":
            dom[focused] += p["text"]
        elif msg["method"] == "Runtime.evaluate":
            e = p["expression"]
            if e.startswith(head) and e.endswith(")"):
                res = {{"result": {{"type": "object", "value": act(*json.loads(e[len(head):-1]))}}}}
            else:
                res = {{"result": {{}}, "exceptionDetails": {{"text": "not fmflow.ACT"}}}}
        send({{"id": msg["id"], "result": res}})
        if msg["method"] == "Page.navigate":
            send({{"method": "Page.loadEventFired", "sessionId": "s1", "params": {{}}}})
"""


class StubCase(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.page = os.path.join(self.repo, "page.html")
        with open(self.page, "w") as f:
            f.write("<p>hi</p>")
        self.log = os.path.join(self.tmp, "stub.jsonl")
        self.stub = os.path.join(self.tmp, "chrome")
        with open(self.stub, "w") as f:
            f.write(STUB)
        os.chmod(self.stub, stat.S_IRWXU)

    def flow(self, text, *args, dom=None, clicks=None, check=False, env=None):
        path = os.path.join(self.repo, "journey.flow")
        with open(path, "w") as f:
            f.write(text)
        e = {"FOREMAN_CHROME": self.stub, "STUB_LOG": self.log, "STUB_DOM": json.dumps(dom or {}),
             "STUB_CLICK": json.dumps(clicks or {})}
        return self.fm("flow", path, "--timeout", "1", *args, env=dict(e, **(env or {})), check=check)

    def calls(self, method):
        with open(self.log) as f:
            return [x["params"] for x in map(json.loads, f) if x["method"] == method]


SIGNUP = """# sign up
goto page.html
type "#email" "a@b.c"
click "#go"
expect "#done" "Thanks"
wait 10
"""


class Journey(StubCase):
    def test_a_journey_that_holds_exits_0(self):
        r = self.flow(SIGNUP, dom={"#email": "", "#go": "Go"}, clicks={"#go": {"#done": "Thanks, a@b.c"}})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("5 steps", r.stdout)
        [nav] = self.calls("Page.navigate")
        self.assertTrue(nav["url"].startswith("file:///") and nav["url"].endswith("/page.html"), nav)  # beside the flow
        self.assertEqual(self.calls("Input.insertText"), [{"text": "a@b.c"}])

    def test_an_expect_that_misses_its_selector_exits_1_naming_the_step(self):
        r = self.flow(SIGNUP, "--json", dom={"#email": "", "#go": "Go"})  # the click adds nothing
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        data = json.loads(r.stdout)
        self.assertFalse(data["ok"])
        self.assertEqual(data["failed"], 4)
        self.assertEqual(data["steps"][-1]["line"], 5)
        self.assertIn("no element matches #done", data["steps"][-1]["error"])
        self.assertEqual(len(data["steps"]), 4, "nothing after the failed step runs")
        text = self.flow(SIGNUP, dom={"#email": "", "#go": "Go"}).stdout
        self.assertIn("✗ step 4 (line 5) expect #done", text)
        self.assertIn("1 step not run", text)

    def test_expect_text_that_differs_names_what_it_shows(self):
        r = self.flow('goto page.html\nexpect h1 "Welcome"\n', dom={"h1": "Error 500"})
        self.assertEqual(r.returncode, 1)
        self.assertIn('shows "Error 500"', r.stdout)

    def test_click_and_type_fail_on_a_missing_element(self):
        for line in ('click "#nope"', 'type "#nope" x'):
            r = self.flow("goto page.html\n" + line + "\n")
            self.assertEqual(r.returncode, 1, line)
            self.assertIn("step 2 (line 2)", r.stdout)
            self.assertIn("no element matches #nope", r.stdout)

    def test_a_page_that_does_not_load_fails_its_goto(self):
        r = self.flow("goto missing.html\n")  # parse refuses a missing file before any browser starts
        self.assertEqual(r.returncode, 1)
        self.assertIn("missing.html", r.stderr)
        r = self.flow("goto file:///nowhere/missing.html\n")
        self.assertEqual(r.returncode, 1)
        self.assertIn("ERR_FILE_NOT_FOUND", r.stdout)

    def test_with_no_browser_it_exits_2_and_says_so(self):
        empty = os.path.join(self.tmp, "empty")
        os.makedirs(empty)
        r = self.flow(SIGNUP, env={"FOREMAN_CHROME": "", "PATH": empty, "HOME": empty,
                                   "PLAYWRIGHT_BROWSERS_PATH": empty})
        self.assertEqual(r.returncode, 2)
        self.assertIn("no browser", r.stdout)
        self.assertIn("not a pass", r.stdout)
        self.assertFalse(os.path.exists(self.log))

    def test_a_browser_that_never_starts_exits_2(self):
        empty = os.path.join(self.tmp, "empty")
        os.makedirs(empty)
        env = {"FOREMAN_CHROME": self.page, "PATH": empty, "HOME": empty, "PLAYWRIGHT_BROWSERS_PATH": empty}
        r = self.flow(SIGNUP, env=env)  # not a program: no browser found at all
        self.assertEqual(r.returncode, 2)
        self.assertIn("isn't an executable file", r.stdout)
        os.chmod(self.page, stat.S_IRWXU)  # executable, but not a program it can start
        r = self.flow(SIGNUP, env=env)
        self.assertEqual(r.returncode, 2)
        self.assertIn("did not start", r.stdout)


class Untrusted(StubCase):
    def test_selectors_and_text_reach_the_page_as_json_data(self):
        evil = '"); document.title = "pwned"; ("'
        r = self.flow(f"goto page.html\nexpect '{evil}' '{evil}'\n", dom={evil: evil})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)  # the stub decodes the args only from ACT(...JSON)
        exprs = [c["expression"] for c in self.calls("Runtime.evaluate")]
        self.assertTrue(all(e.startswith("(" + fmflow.ACT + ")(...") for e in exprs), exprs)

    def test_a_bad_selector_is_named(self):
        r = self.flow("goto page.html\nexpect 'a['\n")
        self.assertEqual(r.returncode, 1)
        self.assertIn("not a valid selector", r.stdout)

    def test_only_local_urls_unless_any_url(self):
        for url in ("https://example.com/", "http://localhost.evil.com/", "http://localhost@evil.com/",
                    "http://127.0.0.1.evil.com/", "javascript:alert(1)", "data:text/html,x", "file://evil/x",
                    "chrome://settings"):
            r = self.flow(f"goto {url}\n")
            self.assertEqual(r.returncode, 1, url)
            self.assertIn("line 1", r.stderr, url)
            self.assertFalse(os.path.exists(self.log), url)  # refused before any browser starts
        for url in ("http://localhost:8000/x", "http://127.0.0.1/", "http://[::1]:3000/"):
            self.assertEqual(fmflow.target(url, self.repo, False), url)
        self.assertEqual(fmflow.target("https://example.com/", self.repo, True), "https://example.com/")
        self.assertRaises(ValueError, fmflow.target, "javascript:alert(1)", self.repo, True)

    def test_the_vocabulary_arity_and_caps(self):
        bad = ["eval 'alert(1)'", "click", "click a b", "type a", "expect", "expect a b c", "wait", "wait -1",
               "wait 99999", "wait soon", 'type a "unclosed', "click " + "x" * (fmflow.MAX_ARG + 1),
               "goto page.html\n" * (fmflow.MAX_STEPS + 1), "", "# only a comment\n"]
        for text in bad:
            r = self.flow(text)
            self.assertEqual(r.returncode, 1, text[:40])
            self.assertIn("fm flow", r.stderr, text[:40])
        self.assertFalse(os.path.exists(self.log))
        r = self.flow("x" * (fmflow.MAX_BYTES + 1))
        self.assertIn("over", r.stderr)
        for t in ("0", "61", "x"):
            self.assertNotEqual(self.flow("goto page.html\n", "--timeout", t).returncode, 0, t)

    def test_a_flow_that_is_not_a_regular_file_is_refused(self):
        r = self.fm("flow", self.tmp, check=False)
        self.assertEqual(r.returncode, 1)
        fifo = os.path.join(self.tmp, "fifo")
        os.mkfifo(fifo)
        r = self.fm("flow", fifo, check=False)  # would block on open
        self.assertEqual(r.returncode, 1)

    def test_control_characters_never_reach_the_terminal(self):
        r = self.flow('goto page.html\nexpect "#\x1b[2J"\n')
        self.assertEqual(r.returncode, 1)
        self.assertNotIn("\x1b", r.stdout)


@unittest.skipUnless(fmshot.chrome(), "no headless Chromium here")
class InABrowser(ForemanTestCase):
    def test_a_real_journey_passes_and_a_missing_element_fails(self):
        self.fm("init")
        with open(os.path.join(self.repo, "form.html"), "w") as f:
            f.write('<input id="name" value="Ada"><button id="go" onclick="document.getElementById(\'out\').textContent = '
                    '\'Hello, \' + document.getElementById(\'name\').value">Go</button><p id="out"></p>')
        path = os.path.join(self.repo, "j.flow")
        with open(path, "w") as f:
            f.write('goto form.html\ntype "#name" " Lovelace"\nclick "#go"\nexpect "#out" "Hello, Ada Lovelace"\n')
        r = self.fm("flow", path, check=False)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        with open(path, "a") as f:
            f.write('expect "#gone"\n')
        r = self.fm("flow", path, "--timeout", "1", check=False)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("step 5 (line 5) expect #gone", r.stdout)


if __name__ == "__main__":
    unittest.main()
