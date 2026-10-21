"""T-1388: a coding CLI that fm code runs (FOREMAN_WORKER_OF set in its environment) only reads Foreman's state: every
command that changes it, grants above all, is refused; reads still work."""
import json
import unittest

from helpers import ForemanTestCase

WORKER = {"FOREMAN_WORKER_OF": "fm-code-T-0001"}


class WorkerOnlyReads(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.tid = json.loads(self.fm("task", "new", "a task", "--type", "FIX", "--tier", "S", "--json",
                                      "--ac", "done :: true", "--step", "do it").stdout)["id"]

    def test_grants_and_state_changes_are_refused(self):
        before = self.fm("task", "show", self.tid, "--json").stdout
        for argv in (["task", "set", self.tid, "--allow", "publish"], ["ask", self.tid, "publish", "--why", "x"],
                     ["standing", "off"], ["autonomy", "full"], ["task", "done", self.tid],
                     ["vetoes", "rm", "1"], ["capture", "do something else"], ["focus", self.tid],
                     # T-1388 review: a subcommand's own `cmd` argument once posed as an allowed verb; log appends
                     # ledger events (a forged check_run passes a gate); these flags write from a read command
                     ["task", "evidence", self.tid, "state", "exit 0"], ["log", "check_run", "{}"],
                     ["queue", "--replan"], ["recall", "--lessons", "--retire", "L-1", "--why", "x"],
                     ["map", "--capture"]):
            with self.subTest(argv=argv):
                r = self.fm(*argv, env=WORKER, check=False)
                self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
                self.assertIn("worker", r.stderr)
        self.assertEqual(self.fm("task", "show", self.tid, "--json").stdout, before, "nothing changed")

    def test_reads_still_work(self):
        for argv in (["state"], ["status"], ["task", "show", self.tid], ["task", "list"], ["queue"], ["next"],
                     ["lib", "search", "pdf"], ["vetoes"], ["gates"]):
            with self.subTest(argv=argv):
                r = self.fm(*argv, env=WORKER, check=False)
                self.assertNotIn("worker of an fm code run", r.stderr, argv)


if __name__ == "__main__":
    unittest.main()
