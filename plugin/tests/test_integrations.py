"""Integrations: a task's run as a Perfetto (Chrome trace JSON) or OTLP JSON trace from the ledger, fm glance's one
JSON line for shells and status bars, and fm lsp: a stdio LSP stub publishing a brief's proof gaps."""
import json
import os
import re
import subprocess
import sys
import time
from unittest import mock

from helpers import FM, LIB, ForemanTestCase

import fmcore as c

first = lambda text: json.JSONDecoder().raw_decode(text)[0]  # noqa: E731 — --focus prints its own lines after the JSON


class Trace(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)
        self.tid = first(self.fm("task", "new", "Fix login", "--type", "FIX", "--tier", "S", "--ac", "ok :: true",
                                 "--step", "red test", "--step", "fix", "--focus", "--json").stdout)["id"]
        t0 = time.time() + 5

        def at(k, event, task=self.tid, data=None, session="sess-a"):
            with mock.patch.object(c, "now", return_value=c.iso(t0 + k)):
                c.log_event(self.p, event, task=task, data=data, session=session)
        at(5, "evidence", data={"step": 1, "cmd": "pytest -k login"})
        at(20, "check_run", data={"results": [{"cmd": "python3 -m unittest t", "exit": 0, "s": 4.0},
                                              {"cmd": "ruff check .", "exit": 1, "s": 2.5}]})
        # ts is cut to the second: a run straight after can claim to start before the last one ended
        at(21, "check_run", data={"results": [{"cmd": "make lint", "exit": 0, "s": 3.0}]})
        at(25, "capture", task="T-0099", data={"text": "someone else's"})
        at(30, "evidence", data={"step": 2, "cmd": "pytest"}, session="sess-b")
        # an older Foreman's unredacted line: the export redacts it again
        with open(os.path.join(self.p.dir, "ledger.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": c.iso(t0 + 40), "session_id": "sess-b", "project": self.p.slug, "task": self.tid,
                                "event": "note", "data": {"cmd": "curl -H 'Authorization: Bearer abc123secretvalue'"}})
                    + "\n")

    def test_a_run_exports_as_valid_perfetto_json(self):
        out = self.fm("timeline",self.tid)
        doc = json.loads(out.stdout)
        evs = doc["traceEvents"]
        self.assertTrue(evs)
        for e in evs:
            self.assertIn(e["ph"], ("X", "i", "M"), e)
            self.assertIsInstance(e["name"], str)
            self.assertIsInstance(e["pid"], int)
            self.assertIsInstance(e["tid"], int)
            if e["ph"] != "M":
                self.assertIsInstance(e["ts"], int)
                self.assertGreater(e["ts"], 0)
            if e["ph"] == "X":
                self.assertGreaterEqual(e["dur"], 0)
            if e["ph"] == "i":
                self.assertIn(e["s"], ("t", "p", "g"))
        spans = {e["name"]: e for e in evs if e["ph"] == "X"}
        task = next(e for n, e in spans.items() if n.startswith(self.tid))
        self.assertIn("Fix login", task["name"])
        for n in ("step 1", "step 2"):
            self.assertIn(n, spans)
            self.assertGreaterEqual(spans[n]["ts"], task["ts"])
            self.assertLessEqual(spans[n]["ts"] + spans[n]["dur"], task["ts"] + task["dur"])
        ruff, unit = spans["ruff check ."], spans["python3 -m unittest t"]
        self.assertEqual(ruff["dur"], 2_500_000)
        self.assertEqual(ruff["args"]["exit"], 1)
        self.assertEqual(unit["ts"] + unit["dur"], ruff["ts"], "a run's checks laid end to end, the last at its event")
        lint = spans["make lint"]
        self.assertEqual((lint["ts"], lint["dur"], lint["args"]["s"]), (ruff["ts"] + ruff["dur"], 1_000_000, 3.0))
        for t in {e["tid"] for e in evs}:  # Perfetto drops slices on a thread that overlap without nesting
            stack = []
            for x in sorted((e for e in evs if e["ph"] == "X" and e["tid"] == t), key=lambda e: (e["ts"], -e["dur"])):
                while stack and x["ts"] >= stack[-1]:
                    stack.pop()
                self.assertTrue(not stack or x["ts"] + x["dur"] <= stack[-1], (x, stack))
                stack.append(x["ts"] + x["dur"])
        threads = {e["args"]["name"] for e in evs if e["ph"] == "M" and e["name"] == "thread_name"}
        self.assertTrue({"sess-a", "sess-b"} <= threads, threads)
        self.assertNotIn("someone else's", out.stdout)
        self.assertNotIn("abc123secretvalue", out.stdout)
        self.assertIn("[REDACTED]", out.stdout)
        self.assertNotIn("T-0099", out.stdout)

    def test_the_active_task_is_the_default_and_out_writes_a_file(self):
        dest = os.path.join(self.tmp, "run.json")
        self.fm("timeline","--out", dest)
        with open(dest, encoding="utf-8") as f:
            self.assertTrue(any(e["name"].startswith(self.tid) for e in json.load(f)["traceEvents"]))

    def test_otlp_json_nests_steps_and_checks_under_the_task_span(self):
        doc = json.loads(self.fm("timeline",self.tid, "--otlp").stdout)
        rs = doc["resourceSpans"][0]
        keys = {a["key"]: a["value"] for a in rs["resource"]["attributes"]}
        self.assertEqual(keys["service.name"], {"stringValue": "foreman"})
        spans = rs["scopeSpans"][0]["spans"]
        root = [s for s in spans if not s.get("parentSpanId")]
        self.assertEqual(len(root), 1)
        root = root[0]
        self.assertRegex(root["traceId"], r"^[0-9a-f]{32}$")
        for s in spans:
            self.assertRegex(s["spanId"], r"^[0-9a-f]{16}$")
            self.assertEqual(s["traceId"], root["traceId"])
            self.assertLessEqual(int(s["startTimeUnixNano"]), int(s["endTimeUnixNano"]))
            if s is not root:
                self.assertEqual(s["parentSpanId"], root["spanId"])
        self.assertEqual(len({s["spanId"] for s in spans}), len(spans))
        failed = next(s for s in spans if s["name"] == "ruff check .")
        self.assertEqual(failed["status"]["code"], 2)
        self.assertIn("evidence", {e["name"] for e in root["events"]})
        self.assertEqual(doc, json.loads(self.fm("timeline",self.tid, "--otlp").stdout), "the same run, the same ids")

    def test_a_sensitive_project_exports_timings_without_words(self):
        self.fm("sensitive", "on")
        out = self.fm("timeline",self.tid).stdout
        evs = json.loads(out)["traceEvents"]
        self.assertTrue(any(e["ph"] == "X" and e["name"] == "check" for e in evs))
        for word in ("pytest", "ruff", "Fix login", "REDACTED"):
            self.assertNotIn(word, out)

    def test_a_task_with_no_events_is_an_error(self):
        p = self.fm("timeline","T-0999", check=False)
        self.assertEqual(p.returncode, 1)
        self.assertIn("T-0999", p.stderr)


class Glance(ForemanTestCase):
    def test_one_json_line_with_bar_fields(self):
        self.fm("init")
        tid = first(self.fm("task", "new", "Fix the login", "--type", "FIX", "--tier", "S", "--ac", "ok :: true",
                            "--step", "a", "--focus", "--json").stdout)["id"]
        out = self.fm("glance").stdout
        self.assertEqual(len(out.splitlines()), 1, out)
        self.assertTrue(out.isascii(), "no raw separator a reader could split on")
        d = json.loads(out)
        self.assertEqual(d["v"], 1)
        self.assertEqual(d["task"], tid)
        self.assertEqual(d["step"], "1/1")
        self.assertIn(tid, d["text"])
        self.assertEqual(d["class"], "active")
        self.assertIn("login", d["tooltip"])
        for k in ("queue", "inbox", "blocked"):
            self.assertIsInstance(d[k], int)

    def test_outside_a_project_one_line_and_nothing_created(self):
        before = sorted(os.listdir(self.home))
        p = self.fm("glance", cwd=self.tmp)
        self.assertEqual(len(p.stdout.splitlines()), 1)
        self.assertEqual(json.loads(p.stdout)["project"], None)
        self.assertEqual(json.loads(p.stdout)["class"], "none")
        self.assertIsNone(c.find_project(self.tmp))
        self.assertEqual(sorted(os.listdir(self.home)), before)


def frame(msg):
    body = json.dumps(msg).encode()
    return b"Content-Length: %d\r\n\r\n" % len(body) + body


def frames(raw):
    out = []
    while raw.strip():
        head, _, rest = raw.partition(b"\r\n\r\n")
        n = int(re.search(rb"Content-Length: (\d+)", head).group(1))
        out.append(json.loads(rest[:n]))
        raw = rest[n:]
    return out


BRIEF = """---
id: T-0001
title: x
---
# T-0001: x

## Acceptance criteria
- [ ] it works — verify with `true`
- [ ] no check here

## Steps
1. [x] write tests
2. [ ] build it  <- CURRENT

## Verification evidence
- (ac 1) `true` → exit 0 [ran] (2026-10-22T00:00:00Z)
"""


class Lsp(ForemanTestCase):
    URI = "file:///tmp/T-0001.md"

    def lsp(self, *msgs, home=None):
        env = dict(os.environ, FOREMAN_HOME=home or self.home)
        env.pop("CLAUDE_CODE_SESSION_ID", None)
        raw = b"".join(m if isinstance(m, bytes) else frame(m) for m in msgs)
        p = subprocess.run([sys.executable, FM, "lsp"], input=raw, env=env,
                           capture_output=True, timeout=30, cwd=self.tmp)
        return p, frames(p.stdout)

    def test_answers_initialize_and_publishes_proof_gaps(self):
        open_ = {"jsonrpc": "2.0", "method": "textDocument/didOpen",
                 "params": {"textDocument": {"uri": self.URI, "languageId": "markdown", "version": 1, "text": BRIEF}}}
        p, out = self.lsp({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
                          {"jsonrpc": "2.0", "method": "initialized", "params": {}}, open_,
                          {"jsonrpc": "2.0", "id": 2, "method": "shutdown"}, {"jsonrpc": "2.0", "method": "exit"})
        self.assertEqual(p.returncode, 0, p.stderr[-500:])
        init = next(m for m in out if m.get("id") == 1)
        self.assertIn("textDocumentSync", init["result"]["capabilities"])
        self.assertEqual(init["result"]["serverInfo"]["name"], "foreman")
        pub = next(m for m in out if m.get("method") == "textDocument/publishDiagnostics")
        self.assertEqual(pub["params"]["uri"], self.URI)
        lines = BRIEF.split("\n")
        by_line = {d["range"]["start"]["line"]: d for d in pub["params"]["diagnostics"]}
        self.assertEqual(sorted(by_line), sorted(lines.index(x) for x in ("- [ ] no check here", "1. [x] write tests",
                                                                           "2. [ ] build it  <- CURRENT")))
        self.assertIn("verify", by_line[lines.index("- [ ] no check here")]["message"])
        self.assertEqual(by_line[lines.index("1. [x] write tests")]["severity"], 2)
        self.assertEqual(by_line[lines.index("2. [ ] build it  <- CURRENT")]["severity"], 3)
        for d in pub["params"]["diagnostics"]:
            self.assertEqual(d["source"], "foreman")
        self.assertIsNone(next(m for m in out if m.get("id") == 2)["result"])

    def test_bad_input_gets_errors_and_closing_clears(self):
        deep = b"[" * 100000 + b"]" * 100000
        p, out = self.lsp(b"Content-Length: %d\r\n\r\n" % len(deep) + deep, b"Content-Length: 3\r\n\r\n{x}",
                          b"X-No-Length: 1\r\n\r\n",
                          {"jsonrpc": "2.0", "id": 7, "method": "no/such"},
                          {"jsonrpc": "2.0", "method": "textDocument/didOpen",
                           "params": {"textDocument": {"uri": self.URI, "version": 1, "text": "not a brief"}}},
                          {"jsonrpc": "2.0", "method": "textDocument/didClose", "params": {"textDocument": {"uri": self.URI}}})
        self.assertEqual(p.returncode, 1, "the input ended without a shutdown")
        self.assertEqual([m["error"]["code"] for m in out[:3]], [-32700] * 3, p.stderr[-300:])
        self.assertEqual(next(m for m in out if m.get("id") == 7)["error"]["code"], -32601)
        pubs = [m["params"]["diagnostics"] for m in out if m.get("method") == "textDocument/publishDiagnostics"]
        self.assertEqual(pubs, [[], []])

    def test_reads_no_network_and_writes_no_state(self):
        home = os.path.join(self.tmp, "empty-home")
        os.makedirs(home)
        p, out = self.lsp({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
                          {"jsonrpc": "2.0", "id": 2, "method": "shutdown"}, {"jsonrpc": "2.0", "method": "exit"},
                          home=home)
        self.assertEqual(p.returncode, 0, p.stderr[-500:])
        self.assertEqual(os.listdir(home), [])
        with open(os.path.join(LIB, "fmintegrations.py"), encoding="utf-8") as f:
            src = f.read()
        self.assertNotRegex(src, r"(?m)^\s*(import|from)\s+(socket|http|socketserver|urllib)\b")
