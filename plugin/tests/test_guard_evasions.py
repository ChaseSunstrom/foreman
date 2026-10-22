"""The guard evasion corpus holds (T-1263).

guard_evasions.jsonl and guard_gaps.jsonl are gen_evasions.py's output. These tests hold the current guard to every
label in the corpus, hold every listed gap to still being a gap, and fail if regenerating would change either file —
so a guard change (a fix or a regression) forces a reviewed regeneration, and a fixed gap has to move into the corpus.
Run: cd plugin/tests && python3 -m unittest test_guard_evasions"""
import os
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
for p in (os.path.join(os.path.dirname(HERE), "lib"), os.path.join(HERE, "fixtures")):
    if p not in sys.path:
        sys.path.insert(0, p)

import fmreplay  # noqa: E402
import gen_evasions  # noqa: E402

FIX = os.path.join(HERE, "fixtures")
CORPUS = os.path.join(FIX, "guard_evasions.jsonl")
GAPS = os.path.join(FIX, "guard_gaps.jsonl")


@unittest.skipIf(gen_evasions.home_in_a_repo(), "the home folder is inside a git tree: the guard judges it a project")
class GuardEvasions(unittest.TestCase):
    def _cases(self, path):
        cases, broken = fmreplay.load_cases(path)
        self.assertEqual(broken, 0, f"a line of {os.path.basename(path)} is not a case")
        return cases

    def test_the_committed_files_are_the_generators_current_output(self):
        # regenerating must not change the committed bytes: a guard change breaks this until someone regenerates
        corpus_text, gaps_text = gen_evasions.build()
        with open(CORPUS, encoding="utf-8") as f:
            self.assertEqual(f.read(), corpus_text, "guard_evasions.jsonl is stale: python3 fixtures/gen_evasions.py")
        with open(GAPS, encoding="utf-8") as f:
            self.assertEqual(f.read(), gaps_text, "guard_gaps.jsonl is stale: python3 fixtures/gen_evasions.py")

    def test_the_guard_holds_every_corpus_label(self):
        cases = self._cases(CORPUS)
        self.assertGreater(len(cases), 0, "no evasion corpus")
        # T-1291: pin the temp folder as the real corpus test does, so a different TMPDIR cannot make a case drift
        with mock.patch.object(tempfile, "tempdir", "/var/tmp"):
            self.assertEqual(fmreplay.drift(cases), [], "the guard disagrees with a labelled evasion")
            self.assertEqual(tempfile.tempdir, "/var/tmp", "verdicts must restore tempfile's folder")

    def test_every_listed_gap_is_still_a_gap(self):
        gaps = self._cases(GAPS)
        self.assertGreater(len(gaps), 0, "no gaps listed")
        with mock.patch.object(tempfile, "tempdir", "/var/tmp"):
            drifted = fmreplay.drift(gaps)
        # every gap must still be one the guard gets wrong; a fix drops it from drift -> this fails until it moves to
        # the corpus. The recorded `got` must be what the guard actually returns now.
        self.assertEqual(len(drifted), len(gaps), "a listed gap no longer drifts: regenerate and move it to the corpus")
        by_id = {g["id"]: g for g in gaps}
        for d in drifted:
            self.assertEqual(d["got"], by_id[d["id"]]["got"], f"stored got is stale for {d['cmd']!r}")
        # a gap is a dangerous command let through or, outside a project (the corpus runs from home), an everyday one
        # refused once obfuscated: the guard can't see which tree a hidden rm or git writes to, so it says no
        self.assertTrue(all(g["got"] != g["should"] for g in gaps))
        known = ("-rf build/", "checkout -b fix/login")
        self.assertEqual([g["cmd"] for g in gaps if g["should"] == "allow" and not any(k in g["cmd"] for k in known)],
                         [], "a new over-broad refusal")


if __name__ == "__main__":
    unittest.main()
