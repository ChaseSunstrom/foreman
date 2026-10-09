"""T-0703 (Frontier 03, first slice): what a session costs comes from how much context every turn re-reads, so the
cost model is per session, and task boundaries compact by tokens, not only by a share of a 1M window."""
import datetime
import json
import os
import re

from helpers import ForemanTestCase
from test_hooks import HookCase, parse


def usage(n, r, w, i=0, o=500):
    ts = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=10 - n)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {"type": "assistant", "timestamp": ts, "sessionId": "sess-a",
            "message": {"id": f"m{n}", "role": "assistant", "content": [],
                        "usage": {"cache_read_input_tokens": r, "cache_creation_input_tokens": w,
                                  "input_tokens": i, "output_tokens": o}}}


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
