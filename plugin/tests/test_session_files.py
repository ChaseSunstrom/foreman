"""T-1097: the sessions folder also holds side files (sid.outlined-<agent>.json, a list): readers of session snapshots
must skip them. fm ui crashed on one and the band and the pane went blank."""
import json
import os
import time
import unittest

from helpers import ForemanTestCase

import fmcore as c


class SideFiles(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        d = os.path.join(c.state_dir(), "sessions")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "sess-1.json"), "w") as f:
            json.dump({"session_id": "sess-1", "project": None, "ts": c.now()}, f)
        time.sleep(0.05)
        with open(os.path.join(d, "sess-1.outlined-a1.json"), "w") as f:  # the newest file, and a list
            json.dump(["plugin/lib/fmcore.py"], f)

    def test_fm_ui_reads_past_a_side_file(self):
        v = self.fm_json("ui")
        self.assertEqual(v.get("v"), 1)
        self.assertTrue(v.get("project"))

    def test_the_fleet_skips_a_side_file(self):
        import fmbus
        self.assertTrue(all(isinstance(s, dict) for s in fmbus.live()))


if __name__ == "__main__":
    unittest.main()
