"""T-1069: racing builders. `fm lane race T` clones T's brief as its "b" side and writes a builder brief for each, so two
builders work it in their own worktrees under their own ids; --score compares them; pick merges the winner, drops
the other with a reason and removes both lanes."""
import json
import os
import subprocess

from helpers import ForemanTestCase

import fmcore as c


class Race(ForemanTestCase):
    def git(self, cwd, *args):
        return subprocess.run(["git", "-C", cwd, "-c", "user.email=t@t", "-c", "user.name=t", *args],
                              capture_output=True, text=True, check=True).stdout

    def task(self, tier="S"):
        return json.loads(self.fm("task", "new", "Make it win", "--type", "FEATURE", "--tier", tier, "--ac",
                                  "it wins :: test -f win.txt", "--step", "s", "--json").stdout)["id"]

    def builder(self, tid, side, win):
        """What a builder does: its own worktree, fm focus there, a committed change."""
        path = os.path.join(self.tmp, f"wt-{side}")
        self.git(self.repo, "worktree", "add", "-q", "-b", f"race-{side}", path, "HEAD")
        self.fm("focus", tid, cwd=path)
        with open(os.path.join(path, "win.txt" if win else "lose.txt"), "w") as f:
            f.write(side + "\n" * (1 if win else 40))
        self.git(path, "add", "-A")
        self.git(path, "commit", "-qm", f"{tid}: side {side}")
        return path

    def test_race_score_and_pick(self):
        self.fm("init")
        tid = self.task()
        d = json.loads(self.fm("lane", "race", tid, "--json").stdout)
        other = d["race"]
        self.assertNotEqual(other, tid)
        for t in (tid, other):
            self.assertTrue(os.path.exists(os.path.join(c.find_project(self.repo).dir, "audits", f"{t}.builder.md")))
        self.assertIn("different approach", c.find_brief(c.find_project(self.repo), other).section("Race"))
        a, b = self.builder(tid, "a", True), self.builder(other, "b", False)
        out = self.fm("lane", "race", tid, "--score").stdout
        self.assertIn("tests", out)
        self.assertIn("lines", out)
        self.assertRegex(out, rf"leader: {tid}\b")
        picked = self.fm("lane", "pick", tid).stdout
        self.assertTrue(os.path.exists(os.path.join(self.repo, "win.txt")), "the winner is merged")
        self.assertFalse(os.path.exists(os.path.join(self.repo, "lose.txt")), "the loser isn't")
        self.assertFalse(os.path.isdir(a) or os.path.isdir(b), "both lanes removed: " + picked)
        p = c.find_project(self.repo)
        self.assertEqual(c.find_brief(p, other).status, "dropped")
        self.assertIn("race_pick", [e.get("event") for e in c.ledger_tail(p, 30)])

    def test_the_b_side_can_win_and_takes_over_the_task(self):
        self.fm("init")
        tid = self.task()
        other = json.loads(self.fm("lane", "race", tid, "--json").stdout)["race"]
        self.builder(tid, "a", False)
        self.builder(other, "b", True)
        self.assertRegex(self.fm("lane", "race", tid, "--score").stdout, rf"leader: {other}\b")
        self.fm("lane", "pick", other)
        p = c.find_project(self.repo)
        self.assertEqual(c.find_brief(p, tid).status, "dropped")
        self.assertIn(other, c.find_brief(p, tid).section("Log"))

    def test_review_fixes_lines_snapshot_brief_and_no_half_start(self):
        self.fm("init")
        tid = self.task()
        other = json.loads(self.fm("lane", "race", tid, "--json").stdout)["race"]
        p = c.find_project(self.repo)
        brief_b = open(os.path.join(p.dir, "audits", f"{other}.builder.md")).read()
        self.assertIn("different approach", brief_b, "the b builder is told to take another approach")
        self.builder(tid, "a", True)
        self.builder(other, "b", False)
        self.fm("task", "ac", other, "add", "anything", "--verify", "true")  # a side can't move its own goalposts
        d = json.loads(self.fm("lane", "race", tid, "--score", "--json").stdout)
        sides = {s["id"]: s for s in d["sides"]}
        self.assertGreaterEqual(sides[other]["lines"], 40, "real line counts, not a silent 0")
        self.assertEqual((sides[other]["passed"], sides[other]["tests"]), (0, 1), "scored on the race's own checks")
        r = self.fm("lane", "pick", other, check=False)
        self.assertNotEqual(r.returncode, 0, "a side failing the race's checks can't win")
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "wt-b")))
        # no half-started race: with no builder slots free it is refused before anything is written
        self.fm("lane", "max", "1")
        third = self.task()
        r = self.fm("lane", "race", third, check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse(c.find_brief(p, third).meta.get("race"))
        self.assertEqual(len([b for b in c.load_briefs(p) if b.meta.get("race_of") == third]), 0)

    def test_l_tasks_and_second_races_are_refused(self):
        self.fm("init")
        big = self.task("L")
        r = self.fm("lane", "race", big, check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("S or M", r.stderr + r.stdout)
        tid = self.task()
        self.fm("lane", "race", tid)
        r = self.fm("lane", "race", tid, check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("already", r.stderr + r.stdout)
