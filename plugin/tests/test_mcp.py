"""fm mcp (T-0245): Foreman's memory and state as read-only MCP tools over stdio (JSON-RPC 2.0, one message a line)."""
import json
import os
import subprocess
import sys

from helpers import FM, ForemanTestCase


class _Mcp(ForemanTestCase):
    def talk(self, *messages, raw=()):
        lines = [m if isinstance(m, str) else json.dumps(m) for m in messages] + list(raw)
        p = subprocess.run([sys.executable, FM, "mcp"], input="\n".join(lines) + "\n", capture_output=True, text=True,
                           cwd=self.repo, timeout=60, env=dict(os.environ, FOREMAN_HOME=self.home))
        return [json.loads(x) for x in p.stdout.splitlines() if x.strip()], p

    @staticmethod
    def call(i, tool, **arguments):
        return {"jsonrpc": "2.0", "id": i, "method": "tools/call", "params": {"name": tool, "arguments": arguments}}


class RoundTrip(_Mcp):
    def test_initialize_list_and_call(self):
        self.fm("init")
        tid = json.loads(self.fm("capture", "Parse dates in the importer", "--json").stdout)["id"]
        out, _ = self.talk(
            {"jsonrpc": "2.0", "id": 1, "method": "initialize",
             "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "t", "version": "1"}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            self.call(3, "state"),
            self.call(4, "task_show", id=tid))
        by = {m["id"]: m for m in out}
        self.assertEqual(len(out), 4)  # the notification gets no answer
        self.assertEqual(by[1]["result"]["serverInfo"]["name"], "foreman")
        self.assertIn("tools", by[1]["result"]["capabilities"])
        names = {t["name"] for t in by[2]["result"]["tools"]}
        self.assertEqual(names, {"state", "next", "recall", "research_list", "research_read", "task_show", "checks"})
        for t in by[2]["result"]["tools"]:
            self.assertEqual(t["inputSchema"]["type"], "object")
        self.assertIn("Parse dates in the importer", by[3]["result"]["content"][0]["text"])
        self.assertFalse(by[3]["result"]["isError"])
        self.assertIn(tid, by[4]["result"]["content"][0]["text"])


class Edges(_Mcp):
    def test_bad_input_is_an_error_and_the_server_keeps_going(self):
        self.fm("init")
        out, _ = self.talk(self.call(1, "rm_everything"),
                           self.call(2, "research_read", name="../../etc/passwd"),
                           {"jsonrpc": "2.0", "id": 3, "method": "no/such"},
                           self.call(5, "task_show", id="T-1; rm -rf /"),
                           self.call(6, "next"),
                           {"jsonrpc": "2.0", "id": 7, "method": "initialize"},
                           raw=["{not json"])
        by = {m.get("id"): m for m in out}
        self.assertTrue(by[1]["result"]["isError"])
        self.assertTrue(by[2]["result"]["isError"])
        self.assertEqual(by[3]["error"]["code"], -32601)
        self.assertTrue(by[5]["result"]["isError"])
        self.assertFalse(by[6]["result"]["isError"])  # still serving after all of that
        self.assertEqual(by[None]["error"]["code"], -32700)  # the malformed line
        self.assertTrue(by[7]["result"]["protocolVersion"])  # a client that names none gets ours

    def test_a_sensitive_project_serves_nothing(self):
        self.fm("init")
        self.fm("sensitive", "on")
        out, _ = self.talk({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}, self.call(2, "state"))
        by = {m["id"]: m for m in out}
        self.assertEqual(by[1]["result"]["tools"], [])
        self.assertTrue(by[2]["result"]["isError"])
        self.assertIn("sensitive", by[2]["result"]["content"][0]["text"])


class Review(_Mcp):
    """T-0245 review: no options through a query, bounded lines, no symlinked notes, and the last check results."""

    def test_the_reviews_cases(self):
        import fmcore as c
        self.fm("init")
        p = c.find_project(self.repo)
        os.makedirs(os.path.join(p.dir, "research"), exist_ok=True)
        outside = os.path.join(self.tmp, "secret.md")
        with open(outside, "w") as f:
            f.write("outside the project")
        os.symlink(outside, os.path.join(p.dir, "research", "linked.md"))
        self.fm("log", "check_run", json.dumps({"results": [{"cmd": "python3 -m pytest -q", "exit": 1, "s": 2.5}]}))
        out, _ = self.talk(self.call(1, "recall", query="--corrections"),
                           self.call(2, "recall", query="-n 5"),
                           self.call(3, "research_read", name="linked"),
                           self.call(4, "checks"),
                           "x" * 1_100_000,
                           self.call(6, "state"))
        by = {m.get("id"): m for m in out}
        for i in (1, 2, 3):
            self.assertTrue(by[i]["result"]["isError"], i)
        self.assertIn("python3 -m pytest -q", by[4]["result"]["content"][0]["text"])
        self.assertIn("✗", by[4]["result"]["content"][0]["text"])
        self.assertEqual(by[None]["error"]["code"], -32600)  # the oversized line, refused
        self.assertFalse(by[6]["result"]["isError"])  # and the next request still served
