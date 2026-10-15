"""T-0825 (round 2): `fm … | head` and readers that quit early: a read-only verb whose stdout closes, with no stdin,
ends quietly instead of printing a BrokenPipeError traceback."""
import os
import subprocess
import sys

from helpers import FM, ForemanTestCase

VERBS = [["status"], ["queue"], ["next"], ["digest"], ["ui", "--json"], ["state"], ["research", "list"], ["log"]]


class ClosedPipe(ForemanTestCase):
    def test_read_only_verbs_end_quietly_when_the_reader_quits(self):
        self.fm("init")
        for i in range(30):  # enough output that a write lands after the reader is gone
            self.fm("capture", f"Idea number {i} with a long enough title to fill the pipe quickly")
        for verb in VERBS:
            with self.subTest(verb=verb):
                p = subprocess.Popen([sys.executable, FM, *verb], cwd=self.repo, stdin=subprocess.DEVNULL,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     env=dict(os.environ, FOREMAN_HOME=self.home))
                p.stdout.close()  # the reader quits before fm writes
                err = p.stderr.read().decode(errors="replace")
                p.wait(60)
                self.assertNotIn("Traceback", err)
                self.assertNotIn("BrokenPipeError", err)
