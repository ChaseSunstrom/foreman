"""T-0112: a taste profile from what the user kept, dropped, steered and corrected: fm taste shows it with its evidence,
and a brainstorm pack carries the same lines so ideas lean toward what they accept."""
import json
import os
import sys
import unittest

from helpers import ForemanTestCase

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))


class Taste(ForemanTestCase):
    def test_kept_dropped_and_steered_work_make_the_profile_and_reach_the_pack(self):
        import fmcore as c
        import fmideas
        self.fm("init")
        self.fm("capture", "Animated band", "--type", "FEATURE", "--tier", "M")
        self.fm("capture", "Telemetry upload", "--type", "FEATURE", "--tier", "M")
        self.fm("task", "drop", "T-0002", "no network calls, keep it local")
        self.fm("task", "new", "Quiet output", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "a",
                "--focus")
        self.fm("task", "log", "T-0003", "steer: spell out codes, no jargon")
        self.fm("task", "finish", "T-0003", "--run", "true", "--audit", "self check")
        out = self.fm("taste").stdout
        for needle in ("no network calls, keep it local", "spell out codes, no jargon", "Quiet output"):
            self.assertIn(needle, out)
        data = json.loads(self.fm("taste", "--json").stdout)
        self.assertTrue(data["dropped"] and data["steered"] and data["kept"])
        pack = fmideas.user_voice(c.find_project(self.repo))
        self.assertIn("dropped: Telemetry upload — no network calls, keep it local", pack)
        self.assertIn("steered: spell out codes, no jargon", pack)


if __name__ == "__main__":
    unittest.main()
