"""T-0703 (Frontier 03, first slice): what a session costs comes from how much context every turn re-reads, so the
cost model is per session, and task boundaries compact by tokens, not only by a share of a 1M window."""
import datetime
import json
import os
import re

from helpers import ForemanTestCase
from test_hooks import HookCase, parse


def usage(n, r, w, i=0, o=500, ago=None, one_hour=False):
    ago = 10 - n if ago is None else ago
    ts = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=ago)).strftime("%Y-%m-%dT%H:%M:%SZ")
    u = {"cache_read_input_tokens": r, "cache_creation_input_tokens": w, "input_tokens": i, "output_tokens": o}
    if one_hour:  # how Claude Code logs a 1 h cache write
        u["cache_creation"] = {"ephemeral_1h_input_tokens": w, "ephemeral_5m_input_tokens": 0}
    return {"type": "assistant", "timestamp": ts, "sessionId": "sess-a",
            "message": {"id": f"m{n}", "role": "assistant", "content": [], "usage": u}}


class SessionCost(ForemanTestCase):
    def test_each_session_shows_its_context_per_turn_split_and_busts(self):
        self.fm("init")
        cfg = os.path.join(self.tmp, "cfg")
        folder = os.path.join(cfg, "projects", re.sub(r"[^A-Za-z0-9]", "-", os.path.realpath(self.repo)))
        os.makedirs(folder)
        rows = ((0, 40000), (40000, 2000), (42000, 1000), (1000, 60000))  # the last re-writes the context: a bust
        with open(os.path.join(folder, "sess-a.jsonl"), "w") as f:
            for n, (r, w) in enumerate(rows):
                f.write(json.dumps(usage(n, r, w)) + "\n")
        env = {"CLAUDE_CONFIG_DIR": cfg}
        out = self.fm("cost", "--sessions", env=env).stdout
        self.assertIn("sess-a", out)
        self.assertIn("4 turns", out)
        self.assertIn("1 bust", out)
        self.assertRegex(out, r"cache read \d+%")
        data = json.loads(self.fm("cost", "--sessions", "--json", env=env).stdout)
        s = data["sessions"][0]
        self.assertEqual((s["turns"], s["busts"]), (4, 1))
        self.assertEqual(s["avg_context"], (40000 + 42000 + 43000 + 61000) // 4)
        self.assertFalse(s["over"])
        self.assertNotIn("over 200k", out)

    def test_one_hour_cache_writes_cost_2x_and_keep_the_cache_an_hour(self):
        # T-1820: on the 1 h cache a write costs 2× base input, not 1.25×, and a 10-min gap is not an expiry
        import fmcost
        self.assertEqual(fmcost.weighted({"cache_creation_input_tokens": 100, "output_tokens": 2,
                                          "cache_creation": {"ephemeral_1h_input_tokens": 60}}), 40 * 1.25 + 60 * 2 + 10)
        self.fm("init")
        cfg = os.path.join(self.tmp, "cfg")
        folder = os.path.join(cfg, "projects", re.sub(r"[^A-Za-z0-9]", "-", os.path.realpath(self.repo)))
        os.makedirs(folder)
        rows = ((90, 0, 40000), (89, 40000, 2000), (79, 1000, 45000), (5, 1000, 46000))  # re-writes after 10, 74 min
        with open(os.path.join(folder, "sess-a.jsonl"), "w") as f:
            for n, (ago, r, w) in enumerate(rows):
                f.write(json.dumps(usage(n, r, w, ago=ago, one_hour=True)) + "\n")
        env = {"CLAUDE_CONFIG_DIR": cfg}
        s = json.loads(self.fm("cost", "--sessions", "--json", env=env).stdout)["sessions"][0]
        self.assertEqual(s["bust_causes"], {"context edit": 1, "ttl": 1})  # warm at 10 min; expired at 74
        self.assertEqual(s["input_equivalent"], 133000 * 2 + 42000 // 10 + 2000 * 5)
        self.assertEqual(s["bust_cost"], round(91000 * (2 - 0.1)))  # re-written instead of read
        self.assertIn("2 busts (1 context edit, 1 ttl) ≈ 173k lost", self.fm("cost", "--sessions", env=env).stdout)

    def test_a_session_averaging_over_200k_a_reply_is_flagged(self):
        # T-1797: the T-1796 regression check: with the 200k compact window no session should average past it
        self.fm("init")
        cfg = os.path.join(self.tmp, "cfg")
        folder = os.path.join(cfg, "projects", re.sub(r"[^A-Za-z0-9]", "-", os.path.realpath(self.repo)))
        os.makedirs(folder)
        with open(os.path.join(folder, "sess-a.jsonl"), "w") as f:
            for n in range(3):
                f.write(json.dumps(usage(n, 380000, 1000)) + "\n")
        env = {"CLAUDE_CONFIG_DIR": cfg}
        out = self.fm("cost", "--sessions", env=env).stdout
        self.assertIn("over 200k", out)
        self.assertIn("fm install-user", out)
        self.assertIn("1 session(s) average over 200k a reply", out)  # past the top 15 rows too
        self.assertTrue(json.loads(self.fm("cost", "--sessions", "--json", env=env).stdout)["sessions"][0]["over"])

    def test_subagent_replies_stay_out_of_their_parents_average(self):
        # a subagent transcript carries its parent's sessionId; its own context isn't the parent's per-turn figure
        self.fm("init")
        cfg = os.path.join(self.tmp, "cfg")
        folder = os.path.join(cfg, "projects", re.sub(r"[^A-Za-z0-9]", "-", os.path.realpath(self.repo)))
        os.makedirs(os.path.join(folder, "sess-a", "subagents"))
        with open(os.path.join(folder, "sess-a.jsonl"), "w") as f:
            f.write(json.dumps(usage(0, 40000, 1000)) + "\n")
        with open(os.path.join(folder, "sess-a", "subagents", "agent-1.jsonl"), "w") as f:
            for n in range(1, 4):
                f.write(json.dumps(usage(n, 380000, 1000)) + "\n")
        s = json.loads(self.fm("cost", "--sessions", "--json", env={"CLAUDE_CONFIG_DIR": cfg}).stdout)["sessions"][0]
        self.assertEqual((s["turns"], s["avg_context"], s["over"]), (1, 41000, False))


class BoundaryTokens(HookCase):
    def stop(self, msg):
        return self.hook("Stop", {"stop_hook_active": False, "last_assistant_message": msg, "session_id": "sess-1"})

    def test_a_task_boundary_past_200k_tokens_is_noted_on_a_1m_window(self):
        self.fm("init")
        self.task(focus=False)
        sessions = os.path.join(self.home, "state", "sessions")
        os.makedirs(sessions, exist_ok=True)
        with open(os.path.join(sessions, "sess-1.json"), "w") as f:
            json.dump({"context_pct": 25, "context_size": 1000000}, f)  # 250k tokens, a quarter of the window
        reason = parse(self.stop("Finished the previous task."))["reason"]
        self.assertIn("250k tokens", reason)
