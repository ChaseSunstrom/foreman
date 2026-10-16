"""T-1086: the outbound ledger (WebFetch, WebSearch, mcp__, Bash curl) and fm run's sandbox default."""
import json
import types
from unittest import mock

from helpers import ForemanTestCase

import fmcore as c
import fmserve


class Outbound(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.tid = json.loads(self.fm("task", "new", "Fetch docs", "--type", "FIX", "--tier", "S", "--json").stdout)["id"]
        self.fm("task", "step", self.tid, "add", "go")
        self.fm("task", "ac", self.tid, "add", "works", "--verify", "true")
        self.fm("focus", self.tid)

    def events(self):
        p = c.find_project(self.repo)
        return c.ledger_events(p, ["outbound"])

    def test_webfetch_logs_host(self):
        self.hook("PostToolUseValidate", {"tool_name": "WebFetch", "tool_input": {"url": "https://docs.test/a?k=1"},
                                          "tool_response": "ok"})
        e = self.events()[-1]
        self.assertEqual((e["task"], e["data"]["tool"], e["data"]["target"]), (self.tid, "WebFetch", "docs.test"))

    def test_bash_curl_logs_host(self):
        self.hook("PostToolUse", {"tool_name": "Bash", "tool_input": {"command": "curl -s https://x.test/a"},
                                  "tool_response": {"stdout": "", "stderr": ""}})
        self.assertEqual(self.events()[-1]["data"]["target"], "x.test")

    def test_fm_outbound_lists(self):
        for _ in range(2):
            self.hook("PostToolUseValidate", {"tool_name": "WebFetch", "tool_input": {"url": "https://docs.test/a"},
                                              "tool_response": "ok"})
        out = self.fm("outbound", self.tid).stdout
        self.assertIn("docs.test", out)
        self.assertIn("2", out)


class Sandbox(ForemanTestCase):
    def cmd(self, avail, no_sandbox=False):
        args = types.SimpleNamespace(permission_mode=None, sandbox=False, no_sandbox=no_sandbox)
        with mock.patch.object(fmserve, "_sandbox_available", lambda: avail), \
                mock.patch.object(fmserve, "_prompt", lambda *a: "x"):
            return fmserve._claude_cmd(types.SimpleNamespace(root=self.repo, dir=self.tmp), types.SimpleNamespace(tier="S"),
                                       args, {})

    def test_default_on_when_available(self):
        self.assertIn("--settings", self.cmd(True))
        self.assertNotIn("--settings", self.cmd(False))

    def test_no_sandbox_opts_out(self):
        self.assertNotIn("--settings", self.cmd(True, no_sandbox=True))
