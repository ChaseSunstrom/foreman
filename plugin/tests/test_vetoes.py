"""T-1323: "stop asking me / don't ask before X" grants X; only a real "never do X" records a veto."""
import os
import sys

from helpers import ForemanTestCase

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import fmcore  # noqa: E402


class RecordedVetoes(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.c = fmcore
        self.p = fmcore.find_project(self.repo)

    def test_permission_phrasings_record_no_veto(self):
        for said in ("stop asking me if you can release, I give full permission", "don't ask before pushing",
                     "dont' stop until complete, full auto", "don't stop now", "do not stop working",
                     "never wait for me", "stop checking with me", "don't bother confirming", "no need to ask",
                     "no need to ask me before you push"):
            self.assertIsNone(self.c.add_veto(self.p, said), said)
        self.assertEqual(self.c.vetoes(self.p), [])

    def test_real_vetoes_still_record(self):
        for said in ("never push to main", "don't release on Fridays", "stop deleting tests",
                     "do not touch the guard", "never checkout main"):
            self.assertIsNotNone(self.c.add_veto(self.p, said), said)
        self.assertEqual(len(self.c.vetoes(self.p)), 5)

    def test_each_veto_lists_the_command_that_retracts_exactly_it(self):  # T-1410
        import json
        import shlex
        self.c.add_veto(self.p, "never push to main")
        self.c.add_veto(self.p, "don't release on Fridays")
        listed = json.loads(self.fm("vetoes", "--json").stdout)
        self.assertEqual([v["retract"] for v in listed], ["fm vetoes rm 1", "fm vetoes rm 2"])
        text = self.fm("vetoes").stdout
        for v in listed:
            self.assertIn(v["retract"], text)
        self.fm(*shlex.split(listed[1]["retract"])[1:])  # the release veto's own command
        self.assertEqual([v["words"] for v in self.c.vetoes(self.p)], [listed[0]["words"]])

    def test_a_real_veto_after_a_permission_clause_records(self):
        rec = self.c.add_veto(self.p, "stop asking me about releases, but never push to main")
        self.assertEqual(rec["words"], ["push", "main"])
