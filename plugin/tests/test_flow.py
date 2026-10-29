"""T-1639: fm flow FILE runs a user journey (goto, click, type, expect, wait) in the headless Chromium fm shot finds,
as a verify command: exit 1 naming the step that failed, 2 with no browser (never a vacuous pass). Journey drives a
stub browser whose page is a dict of selector → text; Untrusted feeds it hostile flow files and pages; InABrowser
uses a real one, where fmflow.ACT itself runs."""
import argparse
import contextlib
import io
import json
import os
import signal
import stat
import sys
import time
import unittest
from unittest import mock

from helpers import ForemanTestCase, headless_chrome

import fmflow
import fmshot

LIB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib")
# A stand-in for Chromium's --remote-debugging-pipe. Its page: STUB_DOM, a JSON {selector: text}; STUB_CLICK, a JSON
# {selector: {selector: text}} of elements a click adds; STUB_REQUESTS, a JSON {selector: [[url, resourceType]...]} of
# requests a click makes (each held as Fetch.requestPaused, as a navigation's own is). Runtime.evaluate must be
# fmflow's ACT called with JSON arguments (anything else is answered as a thrown exception). STUB_MODE=odd answers
# Runtime.evaluate without its result. Every call is logged to STUB_LOG.
STUB = f"""#!{sys.executable}
import json, os, sys
sys.path.insert(0, {LIB!r})
import fmflow
log = open(os.environ["STUB_LOG"], "a")
dom = json.loads(os.environ.get("STUB_DOM", "{{}}"))
clicks = json.loads(os.environ.get("STUB_CLICK", "{{}}"))
reqs = json.loads(os.environ.get("STUB_REQUESTS", "{{}}"))
head, focused, buf, rid = "(" + fmflow.ACT + ")(...", None, b"", 0
def send(msg):
    os.write(4, json.dumps(msg).encode() + b"\\0")
def held(url, kind):  # like Chrome, the request waits for its answer (the next message: fm flow is mid-call)
    global rid, buf
    rid += 1
    send({{"method": "Fetch.requestPaused", "sessionId": "s1",
           "params": {{"requestId": f"r{{rid}}", "request": {{"url": url}}, "resourceType": kind}}}})
    while b"\\0" not in buf:
        buf += os.read(3, 65536)
    line, buf = buf.split(b"\\0", 1)
    msg = json.loads(line)
    log.write(json.dumps({{"method": msg["method"], "params": msg.get("params", {{}})}}) + "\\n")
    log.flush()
def act(op, sel, text):
    global focused
    if sel.endswith("["):
        return {{"bad": "not a valid selector"}}
    if sel not in dom:
        return {{"missing": True}}
    if op == "click":
        dom.update(clicks.get(sel, {{}}))
        for url, kind in reqs.get(sel, []):
            held(url, kind)
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
        elif msg["method"] == "Page.navigate":
            held(p["url"], "Document")
            if "missing" in p["url"]:
                res = {{"errorText": "net::ERR_FILE_NOT_FOUND"}}
        elif msg["method"] == "Input.insertText":
            dom[focused] += p["text"]
        elif msg["method"] == "Runtime.evaluate" and os.environ.get("STUB_MODE") == "odd":
            res = {{"exceptionDetails": None}}
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

    def env(self, dom=None, clicks=None, requests=None, **more):
        return dict({"FOREMAN_CHROME": self.stub, "STUB_LOG": self.log, "STUB_DOM": json.dumps(dom or {}),
                     "STUB_CLICK": json.dumps(clicks or {}), "STUB_REQUESTS": json.dumps(requests or {})}, **more)

    def write(self, text):
        path = os.path.join(self.repo, "journey.flow")
        with open(path, "w") as f:
            f.write(text)
        return path

    def flow(self, text, *args, env=None, **page):
        return self.fm("flow", self.write(text), "--timeout", "1", *args, env=dict(self.env(**page), **(env or {})),
                       check=False)

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
        self.assertEqual([c["requestId"] for c in self.calls("Fetch.continueRequest")], ["r1"])  # its own page

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
        r = self.flow("goto nothere.html\n")  # parse refuses a missing file before any browser starts
        self.assertEqual(r.returncode, 1)
        self.assertIn("nothere.html", r.stderr)
        with open(os.path.join(self.repo, "missing.html"), "w") as f:
            f.write("x")
        r = self.flow("goto missing.html\n")  # the stub fails it
        self.assertEqual(r.returncode, 1)
        self.assertIn("ERR_FILE_NOT_FOUND", r.stdout)

    def test_wait_has_its_own_cap_not_the_element_timeout(self):
        start = time.monotonic()
        r = self.fm("flow", self.write("goto page.html\nwait 700\n"), "--timeout", "0.1", env=self.env(), check=False)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertGreaterEqual(time.monotonic() - start, 0.7)

    def test_the_whole_journey_has_a_deadline(self):
        args = argparse.Namespace(file=self.write("goto page.html\n" + "wait 400\n" * 5), timeout=1.0,
                                  any_url=False, json=True)
        out, code, start = io.StringIO(), 0, time.monotonic()
        with mock.patch.dict(os.environ, self.env()), mock.patch.object(fmflow, "TOTAL_S", 1), \
                contextlib.redirect_stdout(out):
            try:
                fmflow.cmd_flow(args)
            except SystemExit as e:
                code = e.code
        data = json.loads(out.getvalue())
        self.assertEqual(code, 1)
        self.assertLess(time.monotonic() - start, 5)
        self.assertIn("ran past 1 s", data["steps"][-1]["error"])
        self.assertLess(data["failed"], 6)

    def test_with_no_browser_it_exits_2_and_says_so(self):
        empty = os.path.join(self.tmp, "empty")
        os.makedirs(empty)
        r = self.flow(SIGNUP, env={"FOREMAN_CHROME": "", "PATH": empty, "HOME": empty,
                                   "PLAYWRIGHT_BROWSERS_PATH": empty})
        self.assertEqual(r.returncode, 2)
        self.assertIn("no browser", r.stdout)
        self.assertIn("not a pass", r.stdout)
        self.assertIn("fm flow installs nothing", r.stdout)
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

    def test_an_odd_browser_answer_fails_the_step_by_name(self):
        r = self.flow("goto page.html\nexpect h1\n", env={"STUB_MODE": "odd"}, dom={"h1": "x"})
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("step 2 (line 2)", r.stdout)
        self.assertIn("answered oddly", r.stdout)
        self.assertNotIn("Traceback", r.stderr)


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

    def test_goto_opens_only_the_flows_folder_and_local_hosts(self):
        os.makedirs(os.path.join(self.repo, "sub"))
        outside = os.path.join(self.tmp, "secret.txt")
        with open(outside, "w") as f:
            f.write("secret")
        os.symlink(outside, os.path.join(self.repo, "link.html"))
        for url in ("https://example.com/", "http://localhost.evil.com/", "http://localhost@evil.com/",
                    "http://user@localhost/", "http://evil.com\\@localhost/", "http://local host/",
                    "http://127.0.0.1.evil.com/", "javascript:alert(1)", "data:text/html,x", "file://evil/x",
                    "chrome://settings", "/etc/passwd", "../secret.txt", "file:///etc/os-release",
                    "file://" + outside, "link.html", "sub", ".", "http://localhost:99999/"):
            r = self.flow(f"goto '{url}'\n")
            self.assertEqual(r.returncode, 1, url)
            self.assertIn("line 1", r.stderr, url)
            self.assertFalse(os.path.exists(self.log), url)  # refused before any browser starts
        for url in ("http://localhost:8000/x", "http://127.0.0.1/", "http://[::1]:3000/"):
            self.assertEqual(fmflow.target(url, self.repo, False), url)
        self.assertEqual(fmflow.target("HTTP://LocalHost:8000/a?q=1#f", self.repo, False),
                         "http://localhost:8000/a?q=1#f")  # rebuilt from its parts
        self.assertEqual(fmflow.target("file://" + self.page, self.repo, False), "file://" + self.page)
        self.assertEqual(fmflow.target("page.html?state=hover#x", self.repo, False),
                         "file://" + self.page + "?state=hover#x")  # T-1640: a state by query string
        for url in ("../secret.txt?x", "nothere.html?x", "?x", "#x", "..%2Fsecret.txt", "%2e%2e/page.html?x"):
            self.assertRaises(ValueError, fmflow.target, url, self.repo, False)
        os.makedirs(os.path.join(self.repo, "%2e%2e"))  # a folder really named so: its % reaches Chrome escaped
        with open(os.path.join(self.repo, "%2e%2e", "page.html"), "w") as f:
            f.write("x")
        self.assertTrue(fmflow.target("%2e%2e/page.html?x", self.repo, False).endswith("/%252e%252e/page.html?x"))
        self.assertEqual(fmflow.target("https://example.com/", self.repo, True), "https://example.com/")
        for url in ("javascript:alert(1)", "http://evil.com\\@localhost/", "/etc/passwd"):
            self.assertRaises(ValueError, fmflow.target, url, self.repo, True)

    def test_a_page_that_leaves_the_rule_fails_its_step_and_its_request_is_failed(self):
        r = self.flow('goto page.html\nclick "#out"\nexpect "#out"\n', dom={"#out": "x"},
                      requests={"#out": [["file:///etc/os-release", "Document"]]})
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("step 2 (line 2)", r.stdout)
        self.assertIn("went outside the allowed pages, to file:///etc/os-release", r.stdout)
        self.assertEqual(len(self.calls("Fetch.failRequest")), 1)
        [enable] = self.calls("Fetch.enable")
        self.assertEqual(enable["patterns"][0]["urlPattern"], "*")

    def test_an_outside_subresource_is_failed_and_named_but_the_step_holds(self):
        r = self.flow('goto page.html\nclick "#b"\n', dom={"#b": "x"},
                      requests={"#b": [["https://cdn.example.com/a.js", "Script"], ["http://localhost/b.css", "Stylesheet"]]})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("blocked https://cdn.example.com/a.js", r.stdout)
        self.assertEqual(len(self.calls("Fetch.failRequest")), 1)
        self.assertEqual(len(self.calls("Fetch.continueRequest")), 2)  # the page itself and localhost's css
        r = self.flow('goto page.html\nclick "#b"\n', "--any-url", dom={"#b": "x"},
                      requests={"#b": [["https://cdn.example.com/a.js", "Script"]]})
        self.assertNotIn("blocked", r.stdout)

    def test_the_vocabulary_arity_and_caps(self):
        bad = ["eval 'alert(1)'", "click", "click a b", "type a", "expect", "expect a b c", "wait", "wait -1",
               "wait 99999", "wait soon", "wait ²", 'type a "unclosed', "click " + "x" * (fmflow.MAX_ARG + 1),
               "goto page.html\n" * (fmflow.MAX_STEPS + 1), "", "# only a comment\n"]
        for text in bad:
            r = self.flow(text)
            self.assertEqual(r.returncode, 1, text[:40])
            self.assertIn("fm flow", r.stderr, text[:40])
        self.assertFalse(os.path.exists(self.log))
        r = self.flow("x" * (fmflow.MAX_BYTES + 1))
        self.assertIn("over", r.stderr)
        for t in ("0", "61", "x", "nan"):
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


class BrowserClose(StubCase):
    def test_close_doesnt_wait_forever_on_a_browser_it_cant_kill(self):
        with mock.patch.dict(os.environ, self.env()):
            b = fmshot.Browser(self.stub, fmshot.SIZE)
        pid = b.pid
        try:
            with mock.patch("os.killpg", side_effect=PermissionError), \
                    mock.patch("os.kill", side_effect=PermissionError), mock.patch.object(fmshot, "CLOSE_S", 0.3):
                start = time.monotonic()
                b.close()
                self.assertLess(time.monotonic() - start, 3)
        finally:
            os.killpg(pid, signal.SIGKILL)
            os.waitpid(pid, 0)


@unittest.skipUnless(headless_chrome(), "no headless Chromium here")
class InABrowser(ForemanTestCase):
    def flow(self, text, *args):
        path = os.path.join(self.repo, "j.flow")
        with open(path, "w") as f:
            f.write(text)
        return self.fm("flow", path, "--timeout", "1", *args, check=False)

    def test_a_real_journey_passes_and_a_missing_element_fails(self):
        self.fm("init")
        with open(os.path.join(self.repo, "form.html"), "w") as f:
            f.write('<input id="name" value="Ada"><button id="go" onclick="document.getElementById(\'out\').textContent'
                    ' = \'Hello, \' + document.getElementById(\'name\').value">Go</button><p id="out"></p>')
        text = 'goto form.html\ntype "#name" " Lovelace"\nclick "#go"\nexpect "#out" "Hello, Ada Lovelace"\n'
        r = self.flow(text)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        r = self.flow(text + 'expect "#gone"\n')
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("step 5 (line 5) expect #gone", r.stdout)

    def test_act_in_a_real_page(self):
        self.fm("init")
        with open(os.path.join(self.repo, "a.html"), "w") as f:
            f.write('<title>T</title><div id="hid" style="display:none">x</div>'
                    '<p data-x=\'"); document.title = "pwned"; ("\'>q</p>'
                    '<a id="away" href="file:///etc/os-release">away</a>'
                    '<a id="next" href="b.html">next</a>')
        with open(os.path.join(self.repo, "b.html"), "w") as f:
            f.write("<h1>Page B</h1>")
        cases = [('click "#hid"', "#hid is there but not shown"), ("expect 'a[['", "is not a valid selector"),
                 ('click "#away"', "went outside the allowed pages, to file:///etc/os-release")]
        for line, why in cases:
            r = self.flow(f"goto a.html\n{line}\n")
            self.assertEqual(r.returncode, 1, line)
            self.assertIn(why, r.stdout, line)
        evil = """'[data-x='"'"'"); document.title = "pwned"; ("'"'"']'"""  # shell-quoted: [data-x='"); ... ("']
        r = self.flow(f'goto a.html\nexpect {evil} q\nexpect title T\nclick "#next"\nexpect h1 "Page B"\n')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)  # matched as data; the title never changed


if __name__ == "__main__":
    unittest.main()
