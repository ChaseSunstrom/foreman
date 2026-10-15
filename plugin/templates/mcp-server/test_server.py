"""Drives server.py over stdio as a client would: initialize, tools/list, a good call, rejected injections.
Made by Foreman's `fm mcp new`; run: python3 test_server.py. Make the good call assert your command's real output."""
import json
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import server  # noqa: E402


def talk(*messages):
    lines = "".join(json.dumps(m) + "\n" for m in messages)
    p = subprocess.run([sys.executable, os.path.join(HERE, "server.py")], input=lines, capture_output=True, text=True,
                       timeout=server.TIMEOUT * len(messages) + 30)
    return {m.get("id"): m for m in map(json.loads, p.stdout.splitlines())}


def call(i, **arguments):
    if server.SUBS:
        arguments.setdefault("sub", server.SUBS[0])
    return {"jsonrpc": "2.0", "id": i, "method": "tools/call", "params": {"name": server.NAME, "arguments": arguments}}


class Server(unittest.TestCase):
    def test_initialize_list_call_and_refusals(self):
        by = talk({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}},
                  {"jsonrpc": "2.0", "method": "notifications/initialized"},
                  {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
                  call(3),
                  call(4, args=["--help"]),
                  call(5, args=["a\x00b"]),
                  call(6, args=["x" * (server.MAX_ARG + 1)]),
                  call(7, args="; rm -rf /"))
        self.assertEqual(by[1]["result"]["serverInfo"]["name"], server.NAME)
        self.assertEqual([t["name"] for t in by[2]["result"]["tools"]], [server.NAME])
        self.assertEqual(by[3]["result"]["content"][0]["type"], "text")  # the good call answered
        for i in (4, 5, 6, 7):
            self.assertTrue(by[i]["result"]["isError"], i)
            self.assertRegex(by[i]["result"]["content"][0]["text"], r"^(refused argument|args:)")


if __name__ == "__main__":
    unittest.main()
