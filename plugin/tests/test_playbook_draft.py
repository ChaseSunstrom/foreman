"""T-1523: playbooks drafted from this repo's own work: draft ID turns a done task into a playbook draft; mine lists
files changed together; counter lists what failed here; show puts the steps the active task's failed runs point at
first."""
import json
import os
import subprocess
import unittest

from helpers import ForemanTestCase
from test_playbook_machinery import put


class FromThisRepo(ForemanTestCase):
    """T-1523: draft ID turns a done task into a playbook draft; mine lists files changed together; counter lists what
    failed here; show puts the steps the active task's failed runs point at first."""
    def setUp(self):
        super().setUp()
        self.lib = os.path.join(self.tmp, "lib")
        put(self.lib, "references/perf/cache.md", "# Cache\n\nUse when it is slow.\n\n## The procedure\n\n"
            "1. Profile the parser warmup.\n2. Check the cache invalidation keys.\n3. Measure again.\n")
        self.fm("init")

    def run_fm(self, *words):
        return self.fm("playbooks", *words, check=False, env={"FOREMAN_PLAYBOOKS": self.lib})

    def commit(self, msg, **files):
        for rel, text in files.items():
            put(self.repo, rel, text)
        subprocess.run(["git", "-C", self.repo, "add", "--", *files], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", msg], check=True)

    def task(self, title, *steps):
        return json.loads(self.fm("task", "new", title, "--type", "FIX", "--tier", "S", "--ac", "fast :: true",
                                  *[x for s in steps for x in ("--step", s)], "--json").stdout)["id"]

    def test_draft_turns_a_done_task_into_a_procedure(self):
        tid = self.task("Cache the parser", "measure the warmup", "add the cache")
        self.assertNotEqual(self.run_fm("draft", tid).returncode, 0, "not done: nothing is proved yet")
        self.fm("focus", tid)
        self.fm("task", "evidence", tid, "--step", "1", "--run", "true")
        self.fm("task", "step", tid, "done", "1")
        self.fm("task", "step", tid, "done", "2", "--evidence", "x", "ok")
        self.fm("task", "ac", tid, "check", "1", "--evidence", "x", "ok")
        self.fm("task", "audit", tid, "self", "x", "ok")
        self.fm("task", "set", tid, "--section", "Regression test", "--text", "none: fixture")
        self.fm("task", "set", tid, "--section", "Lessons", "--text", "- Measure before you cache")
        self.fm("task", "done", tid)
        text = self.run_fm("draft", tid).stdout
        self.assertIn("Use when: a fix task like", text)
        self.assertIn("1. measure the warmup — proved by `true`.", text)
        self.assertIn("2. add the cache\n", text, "typed evidence proves nothing")
        self.assertIn("## Pitfalls\n\n- Measure before you cache", text)

    def test_mine_lists_the_files_changed_together(self):
        for k in range(5):
            self.commit(f"change {k}", **{"app.py": f"x = {k}\n", "CHANGELOG.md": f"- {k}\n"})
        self.commit("alone", **{"app.py": "x = 9\n", "other.py": "y = 1\n"})
        got = json.loads(self.run_fm("mine", "--json").stdout)["recipes"]
        app = next(x for x in got if x["file"] == "app.py")
        self.assertEqual((app["commits"], app["with"]), (6, [["CHANGELOG.md", 0.83]]))
        self.assertIn("app.py (6 commits): also CHANGELOG.md 83%", self.run_fm("mine").stdout)

    def test_counter_lists_reverts_and_blocked_tasks(self):
        self.commit("retry the flaky upload", **{"up.py": "retry = 3\n"})
        subprocess.run(["git", "-C", self.repo, "revert", "--no-edit", "HEAD"], check=True, capture_output=True)
        tid = self.task("Mock the vendor API", "try it")
        self.fm("task", "block", tid, "the vendor API has no sandbox")
        text = self.run_fm("counter").stdout
        self.assertIn("✗ retry the flaky upload (reverted: reverted by", text)
        self.assertIn(f"✗ {tid} Mock the vendor API (blocked: the vendor API has no sandbox)", text)

    def test_show_puts_the_failing_steps_first(self):
        self.assertNotIn("Look here first", self.run_fm("show", "cache").stdout)
        tid = self.task("Speed up the parser", "find it")
        self.fm("focus", tid)
        self.fm("task", "evidence", tid, "--step", "1", "--run", "echo stale cache invalidation; false", check=False)
        got = json.loads(self.run_fm("show", "cache", "--json").stdout)
        self.assertEqual([(x["n"], x["words"]) for x in got["look_first"]], [(2, ["cache", "invalidation"])])
        self.assertTrue(got["text"].startswith("Look here first"), got["text"][:200])

    def test_score_marks_the_steps_a_run_followed(self):  # T-1525
        tid = self.task("Speed up start", "profile the parser warmup", "add the cache")
        got = json.loads(self.run_fm("score", "cache", "--task", tid, "--json").stdout)
        self.assertEqual([(x["n"], x["followed"]) for x in got["steps"]], [(1, True), (2, False), (3, False)])
        self.assertIn(f"{tid} followed 1 of 3 steps", self.run_fm("score", "cache", "--task", tid).stdout)
        self.assertNotEqual(self.run_fm("score", "cache").returncode, 0, "which task's run")

    def test_kata_lists_practice_briefs_and_scores_an_answer(self):  # T-1525
        listed = json.loads(self.fm("playbooks", "kata", "verify/tdd-workflow", "--json").stdout)["katas"]
        self.assertGreaterEqual(len(listed), 3)
        put(self.tmp, "answer.md", "I'd write a failing test first, then fix it.\n")
        got = json.loads(self.fm("playbooks", "kata", "verify/tdd-workflow", "--answer",
                                 os.path.join(self.tmp, "answer.md"), "--json").stdout)["katas"]
        self.assertTrue(got[0]["pass"])
        self.assertFalse(all(x["pass"] for x in got))
        self.assertNotEqual(self.run_fm("kata", "cache").returncode, 0, "no held-out briefs for it")

    def test_lesson_reads_a_diff_with_its_tasks_lessons(self):  # T-1525
        tid = self.task("Cache the parser", "do it")
        self.fm("task", "set", tid, "--section", "Lessons", "--text", "- Measure before you cache")
        self.commit(f"cache the parser ({tid})", **{"src/app.py": "cache = {}\n"})
        got = json.loads(self.run_fm("lesson", "--json").stdout)
        self.assertEqual(got["commits"][0][1], f"cache the parser ({tid})")
        self.assertEqual(got["folders"], [["src", ["app.py"]]])
        self.assertIn("review/python", got["checklists"])
        text = self.run_fm("lesson", "HEAD").stdout
        self.assertIn(f"{tid} Cache the parser: Measure before you cache", text)
        self.assertNotEqual(self.run_fm("lesson", "--", "-x").returncode, 0, "a range never reads as an option")


if __name__ == "__main__":
    unittest.main()
