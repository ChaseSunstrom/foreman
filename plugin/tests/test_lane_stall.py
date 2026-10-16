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
    ENV = {"FM_STALL_MIN": "0.05"}  # 3 s

    def builder(self, live=True):
        tid = json.loads(self.fm("task", "new", "Built", "--type", "FEATURE", "--tier", "M", "--ac", "ok :: true",
                                 "--step", "s", "--interpretation", "x", "--approach", "x", "--json").stdout)["id"]
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

    def test_a_stopped_lane_keeps_its_own_label(self):
        tid = self.builder(live=False)
        time.sleep(4)
        out = self.fm("lane", "list", env=self.ENV).stdout
        self.assertNotIn("STALLED", out)
        self.assertIn(f"fm lane resume {tid}", self.fm("next", env=self.ENV).stdout)


if __name__ == "__main__":
    unittest.main()
