"""T-1957: fm CLI gaps hit in use: task new --json --focus, fm gates ID, fm task finish --numbers."""
import json

from helpers import ForemanTestCase

import fmcore as c


class CliErgonomics(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")

    def perf_task(self, focus=False):
        r = self.fm("task", "new", "faster", "--type", "PERFORMANCE", "--tier", "S", "--ac", "fast :: true",
                    "--step", "speed it up", *(["--focus"] if focus else []), "--json")
        return json.loads(r.stdout)["id"]

    def test_json_focus_prints_one_json_document(self):
        # T-1954: fm focus's text followed the JSON on stdout, so piping it into jq failed
        tid = self.perf_task(focus=True)
        self.assertEqual(c.active_brief(c.load_briefs(c.find_project(self.repo))).id, tid)

    def test_gates_takes_a_task_id(self):
        # T-1955: fm focus says "Done needs: … (fm gates)", and fm gates T-… was a usage error
        tid = self.perf_task()
        r = self.fm("gates", tid)
        self.assertIn("(PERFORMANCE S)", r.stdout)
        self.assertIn("numbers", r.stdout)
        r = self.fm("gates", "BOGUS", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("BOGUS", r.stderr)

    def test_finish_numbers_fills_measurements(self):
        # T-1956: a PERFORMANCE close took a separate fm task set for its numbers
        tid = self.perf_task(focus=True)
        r = self.fm("task", "finish", tid, "--run", "true", "--audit", "read it", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("--numbers", r.stdout + r.stderr)
        self.fm("task", "finish", tid, "--run", "true", "--audit", "read it", "--numbers", "runs: 2 → 1 (counted)")
        b = c.find_brief(c.find_project(self.repo), tid)
        self.assertEqual(b.status, "done")
        self.assertIn("runs: 2 → 1", b.section("Measurements"))
