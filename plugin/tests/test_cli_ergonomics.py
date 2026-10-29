"""T-1957, T-1962: fm CLI gaps hit in use: task new --json --focus, fm gates ID, fm task finish --numbers, step edit/rm."""
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
        r = self.fm("focus", tid)
        self.assertIn(f"(fm gates {tid})", r.stdout, "T-1961: focus names the id fm gates takes")
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

    def test_step_edit_and_rm_renumber(self):
        # T-1959: a batch's copied member steps took a whole Steps rewrite by hand
        tid = self.perf_task()
        for t in ("two", "three", "four"):
            self.fm("task", "step", tid, "add", t)
        self.fm("task", "step", tid, "edit", "2", "TWO")
        self.fm("task", "step", tid, "rm", "3")
        steps = [(s.n, s.text) for s in c.find_brief(c.find_project(self.repo), tid).steps()]
        self.assertEqual(steps, [(1, "speed it up"), (2, "TWO"), (3, "four")])
        r = self.fm("task", "step", tid, "rm", "9", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.fm("task", "evidence", tid, "--step", "3", "--run", "true")
        r = self.fm("task", "step", tid, "rm", "2", check=False)  # evidence is keyed by step number: renumbering would move it
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("evidence", r.stdout + r.stderr)
