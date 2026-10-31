"""T-1156: a live builder lane with no file change, commit or ledger event for FM_STALL_MIN minutes is stalled: fm lane
list marks it and fm next names it. A fresh edit, or a stopped builder, is not stalled."""
import json
import os
import subprocess
import time
import unittest

from helpers import ForemanTestCase

import fmbus
import fmcore as c


class LaneStall(ForemanTestCase):
    ENV = {"FM_STALL_MIN": "0.05", "FM_STALL_CACHE_S": "0"}  # 3 s

    def builder(self, live=True):
        tid = json.loads(self.fm("task", "new", "Built", "--type", "FEATURE", "--tier", "M", "--ac", "ok :: true",
                                 "--step", "s", "--interpretation", "x", "--approach", "1) a 2) b 3) c Choice 1: a", "--json").stdout)["id"]
        self.path = json.loads(self.fm("lane", "new", tid, "--json").stdout)["path"]
        p = c.find_project(self.repo)
        b = c.find_brief(p, tid)
        b.meta["builder"] = c.now()
        b.meta["builder_proc"] = (f"{fmbus.host_id()}|{os.getpid()}|{fmbus._proc(os.getpid())[1]}" if live
                                  else f"{fmbus.host_id()}|999999999|1")
        c.save_brief(p, b)
        self.wip = os.path.join(self.path, "wip.py")
        with open(self.wip, "w") as f:
            f.write("x = 1\n")
        return tid

    def lane_row(self):
        rows = json.loads(self.fm("lane", "list", "--json", env=self.ENV).stdout)["lanes"]
        return next(r for r in rows if r["path"] == os.path.realpath(self.path))

    def test_a_live_lane_with_nothing_new_is_stalled_and_a_fresh_edit_clears_it(self):
        tid = self.builder()
        old = time.time() - 3600
        for root, _, names in os.walk(self.path):
            if ".git" not in root.split(os.sep):
                for n in names:
                    os.utime(os.path.join(root, n), (old, old))
        time.sleep(4)
        self.assertIsNotNone(self.lane_row().get("stalled_min"))
        self.assertIn("STALLED", self.fm("lane", "list", env=self.ENV).stdout)
        nxt = self.fm("next", env=self.ENV).stdout
        self.assertIn(tid, nxt[nxt.index("stalled"):])
        os.utime(self.wip)  # a fresh edit
        self.assertIsNone(self.lane_row().get("stalled_min"))

    def test_a_returned_builder_with_commits_and_a_clean_worktree_is_not_stalled(self):
        self.builder()
        subprocess.run(["git", "-C", self.path, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.path, "commit", "-qm", "work"], check=True)
        time.sleep(4)
        row = self.lane_row()
        self.assertIn("stalled_min", row)
        self.assertIsNone(row["stalled_min"])
        self.assertNotIn("stalled", self.fm("next", env=self.ENV).stdout)

    def test_a_merged_lane_is_not_stalled(self):
        tid = self.builder()
        c.log_event(c.find_project(self.repo), "lane_merge", task=tid)
        time.sleep(0.1)
        self.assertIsNone(self.lane_row()["stalled_min"])

    def test_the_result_is_cached_and_a_bad_threshold_means_the_default(self):
        import fmlanes
        self.builder()
        p = c.find_project(self.repo)
        os.environ["FM_STALL_MIN"] = "0"
        self.addCleanup(os.environ.pop, "FM_STALL_MIN", None)
        self.assertEqual(fmlanes.stalled(p), {})  # 0 is the default 15 min, not "always"
        os.environ["FM_STALL_MIN"] = "0.0001"
        time.sleep(1)
        self.assertEqual(fmlanes.stalled(p), {}, "cached: the 60 s old answer stands")
        os.environ["FM_STALL_CACHE_S"] = "0"
        self.addCleanup(os.environ.pop, "FM_STALL_CACHE_S", None)
        self.assertEqual(len(fmlanes.stalled(p)), 1)

    def test_a_stopped_lane_keeps_its_own_label(self):
        tid = self.builder(live=False)
        time.sleep(4)
        out = self.fm("lane", "list", env=self.ENV).stdout
        self.assertNotIn("STALLED", out)
        self.assertIn(f"fm lane resume {tid}", self.fm("next", env=self.ENV).stdout)


if __name__ == "__main__":
    unittest.main()
