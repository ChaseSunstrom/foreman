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

    def prompt(self, text="back"):
        out = self.hook("UserPromptSubmit", {"prompt": text, "session_id": "s-away"}).stdout
        return (json.loads(out).get("hookSpecificOutput") or {}).get("additionalContext", "") if out.strip() else ""

    def test_the_away_line_rides_on_a_prompt(self):
        # T-2008: back after a silence mid-session (no new session start): the first prompt carries the summary
        self.gap()
        ctx = self.prompt()
        self.assertEqual(ctx.count("Away: 10 h since you last spoke"), 1, ctx)
        self.assertIn("T-0003", ctx)
        self.assertNotIn("Away:", self.prompt("and then"), "only the prompt that ends the silence")

    def test_a_short_gap_adds_nothing_on_a_prompt(self):
        self.seed([(0.2, "prompt", None, {"text": "go"}), (0.1, "task_done", "T-0003", {})])
        self.assertNotIn("Away:", self.prompt())

    def start(self, source):
        return json.loads(self.hook("SessionStart", {"source": source}, env={"CLAUDE_ENV_FILE": self.env_file}).stdout
                          )["hookSpecificOutput"]["additionalContext"]

    def test_a_new_sessions_first_prompt_leaves_the_line_to_its_start(self):
        self.gap()
        self.seed([(0, "session_start", None, {"source": "startup"})])
        self.assertNotIn("Away:", self.prompt(), "the session start already said it")

    def test_a_prompt_past_the_tail_reports_only_its_own_silence(self):
        import fmaway
        self.seed([(30, "prompt", None, {}), (20, "prompt", None, {}), (19, "task_done", "T-0001", {}),
                   (1, "prompt", None, {}), (0.5, "task_done", "T-0003", {}), (0.4, "task_done", "T-0004", {}),
                   (0, "prompt", None, {})])
        self.assertEqual(fmaway.returned(self.p, n=3), "", "the 19 h silence ended an hour before this prompt")
        self.seed([(-1, "task_done", "T-0005", {}), (-1, "task_done", "T-0006", {}), (-3, "prompt", None, {})])
        self.assertIn("Away: 3 h since you last spoke", fmaway.returned(self.p, n=3))

    def test_a_compact_or_clear_start_after_a_gap_has_no_away_line(self):
        self.gap()
        for source in ("compact", "clear"):
            self.assertNotIn("Away:", self.start(source))

    def test_a_git_revert_after_the_gap_is_listed_under_reverted(self):
        import subprocess
        self.gap()
        subprocess.run(["git", "-C", self.repo, "commit", "-q", "--allow-empty", "-m", 'Revert "add thing (T-0009)"',
                        "-m", "This reverts commit abc123."], check=True)  # like git revert's: a body-less one is skipped by reverts()
        text = self.fm("away").stdout
        self.assertIn("T-0009", text)
        self.assertIn("Reverted:", text)

    def test_the_session_line_names_the_newest_ids(self):
        self.seed([(10, "prompt", None, {"text": "go"})] + [(9 - i * 0.1, "task_done", f"T-{i:04d}", {}) for i in range(1, 10)])
        ctx = self.start("startup")
        self.assertIn("T-0009", ctx)
        self.assertNotIn("T-0001", ctx)
