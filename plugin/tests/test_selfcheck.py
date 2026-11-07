"""T-3127: self-checks name what the user would otherwise point out, with its numbers, in every state (sampo next and
the drive), and go quiet once it's resolved. 2026-11-06's questions are the fixtures: landed work unshipped for hours,
a retired .foreman/ tracked beside .sampo/, the user's asks not landed."""
import datetime
import json
import os
import subprocess
import time

from helpers import ForemanTestCase

from sampo import core as c
from sampo import selfcheck

first = lambda text: json.JSONDecoder().raw_decode(text)[0]  # noqa: E731


def ago(hours):
    t = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=hours)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


class SelfCheck(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def git(self, *a, env=None):
        return subprocess.run(["git", "-C", self.repo, *a], check=True, capture_output=True, text=True,
                              env=env).stdout.strip()

    def land(self, name, hours):
        with open(os.path.join(self.repo, name), "w") as f:
            f.write(name)
        env = {**os.environ, "GIT_AUTHOR_DATE": ago(hours), "GIT_COMMITTER_DATE": ago(hours)}
        self.git("add", "-A")
        self.git("commit", "-qm", name, env=env)

    def test_landed_work_unshipped_for_hours_is_counted_and_aged(self):
        self.land("a.txt", 30)
        self.assertIsNone(selfcheck.unshipped(self.p, [], time.time()), "a project that never shipped says nothing")
        self.git("update-ref", "refs/foreman/shipped", "HEAD")
        self.land("b.txt", 5)
        self.land("c.txt", 1)
        self.assertEqual(selfcheck.unshipped(self.p, [], time.time()),
                         "2 landed commit(s) unshipped, the oldest 5 h → sampo ship")
        self.git("update-ref", "refs/foreman/shipped", "HEAD")
        self.assertIsNone(selfcheck.unshipped(self.p, [], time.time()), "shipped: quiet")

    def test_a_ship_ref_off_this_history_says_nothing(self):
        # review: after a rebase or re-pick the range would count commits main already has
        self.land("a.txt", 30)
        self.git("update-ref", "refs/foreman/shipped", "HEAD")
        self.git("checkout", "-q", "--orphan", "other")
        self.land("b.txt", 5)
        self.assertIsNone(selfcheck.unshipped(self.p, [], time.time()))

    def test_fresh_work_is_not_yet_unshipped(self):
        self.land("a.txt", 30)
        self.git("update-ref", "refs/foreman/shipped", "HEAD")
        self.land("b.txt", 0.5)
        self.assertIsNone(selfcheck.unshipped(self.p, [], time.time()))

    def test_a_retired_mirror_tracked_beside_the_new_one_is_named(self):
        old, new = c.MIRRORS[1], c.MIRROR
        os.makedirs(os.path.join(self.repo, old, "tasks"))
        os.makedirs(os.path.join(self.repo, new), exist_ok=True)
        with open(os.path.join(self.repo, old, "tasks", "T-0001.md"), "w") as f:
            f.write("# x\n")
        self.git("add", "-f", old)
        self.git("commit", "-qm", "old mirror back")
        self.assertIn(f"the retired {old}/ is tracked beside {new}/ → sampo sync export",
                      selfcheck.old_mirror(self.p, [], time.time()))
        self.git("rm", "-rq", old)
        self.git("commit", "-qm", "gone")
        self.assertIsNone(selfcheck.old_mirror(self.p, [], time.time()))

    def test_untracked_files_in_the_main_checkout_are_named(self):
        # T-3548: an untracked scripts/ sat in the main checkout all day; every close missed the train's pass
        self.assertIsNone(selfcheck.untracked(self.p, [], time.time()), "a clean checkout says nothing")
        for rel in ("scripts/a.py", "scripts/b.py", "notes.txt", "build.log", f"{c.MIRROR}/tasks/T-0099.md"):
            os.makedirs(os.path.dirname(os.path.join(self.repo, rel)), exist_ok=True)
            with open(os.path.join(self.repo, rel), "w") as f:
                f.write("x\n")
        with open(os.path.join(self.repo, ".git", "info", "exclude"), "a") as f:
            f.write("*.log\n")  # ignored: never part of the code tree
        self.assertIsNone(selfcheck.untracked(self.p, [], time.time()), "files made just now are work in progress")
        old = time.time() - 2 * 3600
        for rel in ("scripts/a.py", "scripts/b.py", "notes.txt", "build.log", f"{c.MIRROR}/tasks/T-0099.md"):
            os.utime(os.path.join(self.repo, rel), (old, old))
        with open(os.path.join(self.repo, "fresh.py"), "w") as f:
            f.write("x\n")  # still being written: not counted
        hit = selfcheck.untracked(self.p, [], time.time())
        self.assertTrue(hit.startswith("3 untracked file(s) in the main checkout (scripts/ (2), notes.txt)"), hit)
        self.assertIn("commit, .gitignore or remove them", hit)
        lane = os.path.join(self.tmp, "lane")
        self.git("commit", "-q", "--allow-empty", "-m", "base")
        self.git("worktree", "add", "-q", lane)
        self.assertEqual(selfcheck.untracked(c.find_project(lane), [], time.time()), hit, "a lane reads the main checkout")
        for rel in ("scripts/a.py", "scripts/b.py", "notes.txt"):
            os.remove(os.path.join(self.repo, rel))
        self.assertIsNone(selfcheck.untracked(self.p, [], time.time()))

    def ask(self, words, hours, **kw):
        tid = first(self.fm("capture", words, "--json", *kw.get("args", ())).stdout)["id"]
        b = c.find_brief(self.p, tid)
        b.meta["created"] = ago(hours)
        c.save_brief(self.p, b)
        return tid

    def test_the_users_asks_not_landed_are_counted_oldest_first(self):
        old = self.ask("remake the rune page as kalevala", 20)
        newer = self.ask("re-record the readme demo video", 6)
        self.ask("a request from an hour ago", 1)  # too fresh to ask about
        self.ask("an ask from last week", 24 * 8)  # past the window
        self.ask("a bug found while working", 10, args=("--source", "discovered"))  # not the user's
        self.ask("(noticed by an agent while landing) a stale lock", 10)  # Sampo's own note, user-sourced by default
        hit = selfcheck.asks_waiting(self.p, c.load_briefs(self.p), time.time())
        self.assertTrue(hit.startswith("2 of the user's asks from the last 3 days aren't landed; oldest: "
                                       f"{old} (20 h, captured); {newer} (6 h, captured)"), hit)
        for tid in (old, newer):
            self.fm("task", "drop", tid, "done elsewhere")
        self.assertIsNone(selfcheck.asks_waiting(self.p, c.load_briefs(self.p), time.time()))

    def test_a_pile_of_waiting_lanes_is_named_with_its_landing_rate(self):
        # T-3478: "why is this stuff taking so long just to push?": 50+ lanes waited at ~15 min each, never said
        from unittest import mock
        from sampo import lanes as slanes
        waiting = [f"T-00{n:02d}" for n in range(10, 16)]
        with mock.patch.object(slanes, "awaiting_merge", return_value=waiting):
            self.assertIn("6 finished lanes wait and none landed in the last 2 h",
                          selfcheck.landing_rate(self.p, [], time.time()))
            for tid in ("T-0001", "T-0002", "T-0003"):
                c.log_event(self.p, "lane_merge", task=tid, data={"train": ["T-0001", "T-0002", "T-0003"]})
            self.assertIn("6 finished lanes wait; 3 landed in the last 2 h (~40 min each), so the pile clears in ~4 h",
                          selfcheck.landing_rate(self.p, [], time.time()))
        with mock.patch.object(slanes, "awaiting_merge", return_value=waiting[:4]):
            self.assertIsNone(selfcheck.landing_rate(self.p, [], time.time()), "a short pile says nothing")

    def test_lines_are_cached_and_reach_sampo_next(self):
        self.ask("remake the rune page as kalevala", 20)
        now = time.time()
        first_lines = selfcheck.lines(self.p, now=now)
        self.assertEqual(len(first_lines), 1)
        self.ask("re-record the readme demo video", 6)
        self.assertEqual(selfcheck.lines(self.p, now=now + 10), first_lines, "cached for a hook's every Stop")
        self.assertIn("2 of the user's asks", selfcheck.lines(self.p, now=now + selfcheck.CACHE_S + 1)[0])
        os.remove(os.path.join(self.p.dir, "selfcheck.json"))
        self.assertIn("self-check: 2 of the user's asks", self.fm("next").stdout)
        note = self.hook("UserPromptSubmit", {"prompt": "hi", "session_id": "sess-1"}).stdout
        self.assertNotIn("self-check:", note, "the prompt note's 400 characters stay for the task and its next step")
