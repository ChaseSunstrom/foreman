"""T-1155: fm away, the return-after-gap summary: what closed, blocked, was asked or was reverted since the user last
spoke, and one line of it at session start after a long gap only."""
import json
import os
import time

from helpers import ForemanTestCase

import fmcore as c


class Away(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)
        self.env_file = os.path.join(self.tmp, "claude_env")
        open(self.env_file, "w").close()

    def seed(self, rows):
        """rows: (hours ago, event, task, data); written raw, oldest first."""
        with open(os.path.join(self.p.dir, "ledger.jsonl"), "a", encoding="utf-8") as f:
            for h, ev, task, data in rows:
                f.write(json.dumps({"ts": c.iso(time.time() - h * 3600), "event": ev, "task": task, "data": data or {}}) + "\n")

    def gap(self):
        self.seed([(30, "task_done", "T-0001", {}), (30, "task_block", "T-0002", {"reason": "old reason"}),
                   (29, "rollback", None, {"snapshot": "old-snap"}),
                   (10, "prompt", None, {"text": "go"}),
                   (8, "task_done", "T-0003", {}), (7, "task_block", "T-0004", {"reason": "needs the key"}),
                   (6, "ask_queued", "T-0004", {"n": 1, "q": "which db?", "default": "sqlite"}),
                   (5, "rollback", None, {"snapshot": "snap-new"}),
                   (4, "ask_queued", "T-0005", {"n": 2, "q": "answered one?", "default": "yes"})])
        meta = c.read_meta(self.p)
        meta["ask_digest"] = {"asks": [{"n": 1, "q": "which db?", "default": "sqlite"}], "deadline": "2099-01-01T00:00:00Z"}
        c.write_meta(self.p, meta)

    def test_lists_what_happened_after_the_gap_and_nothing_before(self):
        self.gap()
        text = self.fm("away").stdout
        for want in ("T-0003", "T-0004", "needs the key", "which db?", "snap-new"):
            self.assertIn(want, text)
        for gone in ("T-0001", "T-0002", "old reason", "old-snap", "answered one?"):
            self.assertNotIn(gone, text)

    def test_session_start_after_a_long_gap_carries_one_away_line(self):
        self.gap()
        ctx = json.loads(self.hook("SessionStart", {"source": "startup"}, env={"CLAUDE_ENV_FILE": self.env_file}).stdout
                         )["hookSpecificOutput"]["additionalContext"]
        self.assertEqual(ctx.count("Away:"), 1)
        self.assertIn("T-0003", ctx)

    def test_a_short_gap_has_no_away_line(self):
        self.seed([(0.2, "prompt", None, {"text": "go"}), (0.1, "task_done", "T-0003", {})])
        ctx = json.loads(self.hook("SessionStart", {"source": "startup"}, env={"CLAUDE_ENV_FILE": self.env_file}).stdout
                         )["hookSpecificOutput"]["additionalContext"]
        self.assertNotIn("Away:", ctx)
