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

    def test_a_real_veto_after_a_permission_clause_records(self):
        rec = self.c.add_veto(self.p, "stop asking me about releases, but never push to main")
        self.assertEqual(rec["words"], ["push", "main"])
