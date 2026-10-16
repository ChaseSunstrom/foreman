"""T-1086: the outbound ledger (WebFetch, WebSearch, mcp__, Bash curl) and fm run's opt-in sandbox."""
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
        self.assertEqual(self.bash("curl -s https://x.test/a"), ["x.test"])

    def test_fm_outbound_lists(self):
        for _ in range(2):
            self.hook("PostToolUseValidate", {"tool_name": "WebFetch", "tool_input": {"url": "https://docs.test/a"},
                                              "tool_response": "ok"})
        out = self.fm("outbound", self.tid).stdout
        self.assertIn("docs.test", out)
        self.assertIn("2", out)

    def bash(self, cmd):
        self.hook("PostToolUse", {"tool_name": "Bash", "tool_input": {"command": cmd},
                                  "tool_response": {"stdout": "", "stderr": ""}})
        return [e["data"]["target"] for e in self.events()]

    def web(self, tool, **ti):
        self.hook("PostToolUseValidate", {"tool_name": tool, "tool_input": ti, "tool_response": "ok"})
        return self.events()[-1]["data"]["target"]

    def test_bash_command_position(self):
        self.assertEqual(self.bash("cat ~/.ssh/config; curl-config --cflags"), [])
        self.assertEqual(self.bash("curl https://a.test/x; curl https://b.test/y"), ["a.test", "b.test"])

    def test_host_stops_at_query(self):
        self.assertEqual(self.web("WebFetch", url="https://api.x.com?sig=SECRET"), "api.x.com")
        self.assertEqual(self.web("WebFetch", url="api.y.com/p?sig=SECRET"), "api.y.com")
        self.assertEqual(self.bash("git push git@github.com:o/r.git main"), ["api.x.com", "api.y.com", "github.com"])

    def test_websearch_redacted_and_cut(self):
        t = self.web("WebSearch", query="token ghp_" + "a" * 36 + " " + "x" * 200)
        self.assertNotIn("ghp_a", t)
        self.assertLessEqual(len(t), 80)


class Sandbox(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")

    def cmd(self, avail=True, **kw):
        args = types.SimpleNamespace(**{"permission_mode": None, "sandbox": False, "no_sandbox": False, **kw})
        p = c.find_project(self.repo)
        with mock.patch.object(fmserve, "_sandbox_available", lambda: avail), \
                mock.patch.object(fmserve, "_prompt", lambda *a: "x"):
            return fmserve._claude_cmd(p, types.SimpleNamespace(tier="S"), args, {})

    def test_opt_in_only(self):
        self.assertNotIn("--settings", self.cmd())
        self.assertIn("--settings", self.cmd(sandbox=True))
        self.assertNotIn("--settings", self.cmd(False, sandbox=True))

    def test_project_setting_and_opt_out(self):
        self.fm("sandbox", "on")
        self.assertIn("--settings", self.cmd())
        self.assertNotIn("--settings", self.cmd(no_sandbox=True))
        self.fm("sandbox", "off")
        self.assertNotIn("--settings", self.cmd())

    def test_settings_allow_domains_and_writes(self):
        self.fm("sandbox", "allow", "x.test")
        cmd = self.cmd(sandbox=True)
        s = json.loads(cmd[cmd.index("--settings") + 1])["sandbox"]
        self.assertIn("x.test", s["network"]["allowedDomains"])
        self.assertIn(self.repo, s["filesystem"]["allowWrite"])

    def test_both_flags_rejected(self):
        p = self.fm("run", "--sandbox", "--no-sandbox", check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("sandbox", p.stderr + p.stdout)
