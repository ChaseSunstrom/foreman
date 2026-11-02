"""T-2641: a removed verb or flag prints its tombstone (what replaced it, the task that removed it), not a bare argparse error."""
import json
import os

from helpers import ForemanTestCase


class Tombstones(ForemanTestCase):
    def events(self):
        import fmcore as c
        try:
            with open(os.path.join(c.state_dir(), "events.jsonl")) as f:
                return [json.loads(x) for x in f if x.strip()]
        except OSError:
            return []

    def test_a_removed_flag_names_its_replacement_and_the_task_that_removed_it(self):
        self.fm("init")
        p = self.fm("night", "--print-timer", check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("T-2475", p.stderr)
        self.assertIn("fm night --stage", p.stderr)
        self.assertNotIn("did you mean", p.stderr)
        self.assertFalse([e for e in self.events() if e.get("word") == "--print-timer"])  # a known removal isn't a vote

    def test_an_unknown_flag_without_a_tombstone_keeps_the_argparse_message_and_the_event(self):
        self.fm("init")
        p = self.fm("night", "--no-such-flag", check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn("unrecognized arguments", p.stderr)
        self.assertTrue([e for e in self.events() if e.get("word") == "--no-such-flag"])
