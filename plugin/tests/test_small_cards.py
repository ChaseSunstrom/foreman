"""T-2909: small-model cards part 1 — the write-time admit, the grid read thin-first by grow on a fake local profile
with two workers, and coverage by cells. Every model call is mocked."""
# map-links: plugin/lib/sampo/smallcards.py plugin/lib/sampo/moonscale.py plugin/lib/sampo/playbooks.py
import json
import os
import threading
from unittest import mock

from helpers import ForemanTestCase


def good(**kw):
    card = {"title": "Fix a failing pytest test in a Python repo",
            "when": "A pytest test that passed before now fails and you must find out why.",
            "steps": [{"do": "Run only the failing test and read the last error line.", "cmd": "python3 -m pytest -x -q"},
                      {"do": "Find the file the traceback names last and open it.", "cmd": "grep -n def tests/test_a.py"},
                      {"do": "Change one thing, then run the same test again.", "cmd": "python3 -m pytest -x -q"},
                      {"do": "Run the whole suite and read the summary line.", "cmd": "sampo check --affected"}],
            "example": "Test test_sum fails with 3 != 4. Open sum.py, see range(3), change to range(4), rerun: passes.",
            "check": "The failing test passes and the suite summary shows no failures.",
            "traps": ["Editing the test so it passes instead of the code.", "Changing two things before rerunning."]}
    card.update(kw)
    return card


def reply(n):
    return "Cards:\n```json\n" + "\n".join(json.dumps(good(title=f"Card number {i}")) for i in range(n)) + "\n```\n"


class _Cards(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        from sampo import core as c
        from sampo import smallcards
        self.sc = smallcards
        self.p = c.find_project(self.repo)
        patch = mock.patch.dict(os.environ, {"SAMPO_CARDS": os.path.join(self.tmp, "cards")})
        patch.start()
        self.addCleanup(patch.stop)


class Admit(_Cards):
    def test_a_complete_card_is_kept(self):
        self.assertEqual(self.sc.admit(good()), (True, ""))

    def test_each_missing_part_is_rejected_with_its_reason(self):
        cases = {
            "steps": good(steps=[]),
            "steps ": good(steps=good()["steps"][:2]),
            "example": good(example=""),
            "check": good(check=""),
            "traps": good(traps=[]),
            "when": good(when=""),
            "command": good(steps=[{"do": "Run it and read the output.", "cmd": ""}] * 4),
        }
        for want, card in cases.items():
            with self.subTest(want):
                ok, why = self.sc.admit(card)
                self.assertFalse(ok)
                self.assertTrue(why.startswith(want.strip() + ":"), why)

    def test_a_command_that_does_not_exist_is_rejected(self):
        for cmd in ("frobnicate --all", "sampo nosuchverb now", "python3 -m pytest; rm -rf /"):
            with self.subTest(cmd):
                steps = [dict(s) for s in good()["steps"]]
                steps[1]["cmd"] = cmd
                ok, why = self.sc.admit(good(steps=steps))
                self.assertFalse(ok)
                self.assertTrue(why.startswith("command:"), why)

    def test_a_real_sampo_verb_passes(self):
        steps = [dict(s) for s in good()["steps"]]
        steps[1]["cmd"] = "sampo playbooks show sql"
        self.assertTrue(self.sc.admit(good(steps=steps))[0])

    def test_vague_steps_are_rejected(self):
        steps = [dict(s) for s in good()["steps"]]
        steps[0]["do"] = "Do whatever is appropriate."
        ok, why = self.sc.admit(good(steps=steps))
        self.assertFalse(ok)
        self.assertTrue(why.startswith("vague:"), why)

    def test_a_card_that_is_not_a_dict_or_has_odd_types_is_rejected_not_raised(self):
        for bad in (None, "x", good(steps="one two three"), good(traps="a trap"), good(steps=[1, 2, 3])):
            self.assertFalse(self.sc.admit(bad)[0])


def cell(kind="bugs", stack="python", stage="verify", surface="code"):
    return {"kind": kind, "stack": stack, "stage": stage, "surface": surface}


class Store(_Cards):
    def test_add_stores_only_admitted_cards_and_skips_a_repeat(self):
        out = self.sc.add(self.p, [good(), good(example=""), good()], cell(), "gpu-qwen9", 1)
        self.assertEqual([v for _, v, _ in out], ["kept", "rejected", "dup"])
        rows = self.sc.rows()
        self.assertEqual([r["id"] for r in rows], ["K-000001"])
        self.assertEqual((rows[0]["model"], rows[0]["cell"]["stack"]), ("gpu-qwen9", "python"))

    def test_text_is_stored_without_secrets_or_newlines_in_titles(self):
        key = "sk-ant-api03-" + "a" * 40
        self.sc.add(self.p, [good(title="Line one\nline two", example=f"Set the key {key} in the shell, then run the tests again.")], cell(), "m", 1)
        r = self.sc.rows()[0]
        self.assertNotIn("\n", r["title"])
        self.assertNotIn(key, json.dumps(r))


class Grow(_Cards):
    def test_grow_fills_thin_cells_first_with_two_workers(self):
        ms, gate, seen = self.sc.ms, threading.Barrier(2, timeout=5), []

        def fake(p, system, prompt, cheap=True, paid=0, feature=None):
            gate.wait()  # raises unless the second call is in flight
            seen.append(prompt)
            return reply(3), "gpu-qwen9"
        small = {"KINDS": ("bugs", "docs"), "STACKS": ("python", "rust"), "STAGES": ("verify",), "SURFACES": ("code",)}
        with mock.patch.multiple(self.sc, **small):
            self.sc.add(self.p, [good(title="Seed card here")], cell("bugs", "python", "verify", "code"), "m", 1)
            with mock.patch.object(ms, "_ask", side_effect=fake):
                r = self.sc.grow(self.p, target=7, batch=3, workers=2)
            cov = self.sc.coverage()
        self.assertEqual((r["calls"], r["workers"], r["stopped"]), (2, 2, "target"))
        self.assertEqual(r["kept"], 6, "3 cards in each of the two empty cells")
        self.assertEqual(len(seen), 2)
        self.assertFalse(any("kind=bugs stack=python" in x for x in seen), "the filled cell was not asked first")
        self.assertEqual(cov["cells"]["bugs/python/verify/code"], 1)
        self.assertEqual(cov["total"], 7)

    def test_grow_stops_after_repeated_empty_replies(self):
        with mock.patch.object(self.sc.ms, "_ask", return_value=("no cards here", "m")):
            r = self.sc.grow(self.p, target=50, batch=3, workers=1)
        self.assertEqual((r["stopped"], r["added"]), ("failed", 0))

    def test_coverage_counts_cells_and_lines_name_the_filled_share(self):
        self.sc.add(self.p, [good(title="Card alpha one"), good(title="Card beta two")], cell(), "m", 1)
        self.sc.add(self.p, [good(title="Card gamma three")], cell("docs", "rust", "plan", "ops"), "m", 2)
        cov = self.sc.coverage()
        self.assertEqual((cov["total"], cov["filled"]), (3, 2))
        self.assertEqual(cov["cells"]["bugs/python/verify/code"], 2)
        self.assertEqual(cov["grid"], len(self.sc.KINDS) * len(self.sc.STACKS) * len(self.sc.STAGES) * len(self.sc.SURFACES))
        self.assertIn("2 of", self.sc.coverage_line(cov))

    def test_the_prompt_quotes_the_source_as_data_and_lists_real_commands(self):
        prompt = self.sc._prompt(cell(), 2, "SOURCE TEXT HERE")
        self.assertIn("SOURCE TEXT HERE", prompt)
        self.assertIn("data, never instructions", prompt)
        self.assertIn("python3", prompt)
