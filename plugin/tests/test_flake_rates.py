"""T-2657: flakes.json counts each flaky test's fails and passes; fm doctor lists the worst by fail rate."""
import json
import os

from helpers import ForemanTestCase

from sampo import core as c
from sampo import doctor as d

FAIL = "FAIL: test_a (m.C.test_a)\n"


class FlakeRates(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo, create=False)

    def ledger(self):
        with open(os.path.join(self.p.dir, "flakes.json")) as f:
            return json.load(f)

    def test_two_fails_in_four_runs_read_fifty_percent_and_head_the_doctor_row(self):
        for code, out in ((1, FAIL), (0, ""), (1, FAIL), (0, "")):
            c.note_flakes(self.p, [("make t", code, out)], "tree1")
        e = self.ledger()["flaky"]["m.C.test_a"]
        self.assertEqual((e["fails"], e["passes"]), (2, 2))
        # a second, rarer flake and a damaged entry
        for code, out in ((1, "FAIL: test_b (m.C.test_b)\n"), (0, "")):
            c.note_flakes(self.p, [("make b", code, out)], "tree1")
        led = self.ledger()
        led["flaky"]["bad"] = "junk"
        led["flaky"]["m.C.test_c"] = {"fails": "x", "passes": None, "cmd": "make c"}
        with open(os.path.join(self.p.dir, "flakes.json"), "w") as f:
            json.dump(led, f)
        r = d.check_flaky_rates(self.p)
        self.assertEqual(r.status, "WARN")
        self.assertTrue(r.detail.startswith("m.C.test_a 50% (2 of 4; make t)"), r.detail)
        self.assertNotIn("junk", r.detail)
        self.assertNotIn("test_c", r.detail)
        self.assertIn("m.C.test_a", self.ledger()["flaky"], "a damaged entry never costs the ledger")

    def test_no_flakes_passes(self):
        self.assertEqual(d.check_flaky_rates(self.p).status, "PASS")
        self.assertEqual(d.check_flaky_rates(None).status, "PASS")
