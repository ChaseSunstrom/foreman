"""T-1401: an unattended fm code run and fm release --push refuse when the newest guard corpus replay (fm replay --cases)
is red or older than 7 days, naming the check, its date and the refresh command; an attended run only warns, and
--stale-ok REASON runs anyway with the waiver on the ledger. The replay itself never runs: its ledger record is stubbed."""
import os
import time

from helpers import read_text, stub_corpus_replay

import fmcore as c
import fmreplay
from test_code import CodeCase, call, plan
from test_release import ReleaseCase, sh


def day(days):
    return c.iso(time.time() - days * 86400)[:10]


class SafetyGate(CodeCase):
    replayed = False

    def fixed(self, *flags, env=None, check=True):
        self.serve("openai", plan(), call("edit", file="calc.py", old="a - b", new="a + b"), call("done", summary="ok"))
        return self.code("make calc.add add", "--model", "fake", *flags, env=env, check=check)

    def assert_refused(self, r, *words):
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        for w in ("guard corpus replay", "fm replay --cases", *words):
            self.assertIn(w, r.stderr)
        self.assertIn("return a - b", self.calc())
        self.assertFalse(c.load_briefs(c.find_project(self.repo)), "refused before any task")

    def test_the_rule(self):
        p = c.find_project(self.repo, create=True)
        self.assertIn("no result on record", fmreplay.safety_gate(p))
        stub_corpus_replay(self.repo, days=8)
        self.assertRegex(fmreplay.safety_gate(p), rf"passed on {day(8)}, 8 days ago.*older than 7")
        stub_corpus_replay(self.repo, drifted=2)
        self.assertRegex(fmreplay.safety_gate(p), rf"failed on {day(0)}: 2 drifted")
        stub_corpus_replay(self.repo, cases=0)
        self.assertIn("0 cases", fmreplay.safety_gate(p), "an empty corpus proves nothing")
        stub_corpus_replay(self.repo)
        self.assertIsNone(fmreplay.safety_gate(p))

    def test_red_replay_refuses_an_unattended_run(self):
        stub_corpus_replay(self.repo, drifted=1)
        self.assert_refused(self.fixed(check=False), "failed on " + day(0))

    def test_stale_green_replay_refuses_an_unattended_run(self):
        stub_corpus_replay(self.repo, days=8)
        self.assert_refused(self.fixed(check=False), "passed on " + day(8))

    def test_fresh_green_replay_lets_it_run(self):
        stub_corpus_replay(self.repo, days=8)
        stub_corpus_replay(self.repo)
        r = self.fixed()
        self.assertIn("return a + b", self.calc())
        self.assertNotIn("guard corpus replay", r.stdout + r.stderr)

    def test_an_attended_run_only_warns(self):
        stub_corpus_replay(self.repo, drifted=1)
        r = self.fixed(env={"FOREMAN_CODE_ATTENDED": "1"})
        self.assertIn("return a + b", self.calc())
        self.assertIn("guard corpus replay", r.stdout + r.stderr)

    def test_waiver_is_logged(self):
        stub_corpus_replay(self.repo, days=8)
        self.fixed("--stale-ok", "replay box is down, checked by hand")
        self.assertIn("return a + b", self.calc())
        led = read_text(os.path.join(c.find_project(self.repo).dir, "ledger.jsonl"))
        self.assertIn('"safety_waiver"', led)
        self.assertIn("replay box is down, checked by hand", led)
        r = self.code("x", "--model", "fake", "--stale-ok", "  ", check=False)
        self.assertNotEqual(r.returncode, 0, "a blank reason is no waiver")

    def test_the_replay_records_its_result(self):
        cases = os.environ["FOREMAN_GUARD_CASES"]
        with open(cases, "w") as f:
            f.write('{"id": "a", "cmd": "ls", "cwd": "", "should": "allow", "why": "t"}\n')
        p = c.find_project(self.repo, create=True)
        self.fm("replay", "--cases", env={"FOREMAN_GUARD_CASES": cases})
        [e] = c.ledger_events(p, kinds=["guard_corpus"])
        self.assertEqual(e["data"], {"cases": 1, "drifted": 0, "broken": 0})
        self.assertIsNone(fmreplay.safety_gate(p))


class ReleaseGate(ReleaseCase):
    replayed = False

    def push(self, *flags):
        self.origin()
        self.tid(grant=True)
        return self.rel("9.9.9", "--push", *flags, check=False)

    def test_red_replay_refuses_the_push_before_any_change(self):
        stub_corpus_replay(self.repo, drifted=3)
        r = self.push()
        self.assertNotEqual(r.returncode, 0)
        for w in ("guard corpus replay", "fm replay --cases", "failed on " + day(0)):
            self.assertIn(w, r.stderr)
        self.assertEqual(self.subject(), "Foreman 1.0.0")
        self.assertEqual(sh(self.repo, "status", "--porcelain"), "")

    def test_stale_replay_refuses_the_push(self):
        stub_corpus_replay(self.repo, days=8)
        r = self.push()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("passed on " + day(8), r.stderr)

    def test_fresh_green_replay_lets_it_push(self):
        stub_corpus_replay(self.repo)
        r = self.push()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("pushed Foreman 9.9.9", r.stdout)

    def test_waiver_pushes_and_is_logged(self):
        stub_corpus_replay(self.repo, drifted=1)
        r = self.push("--stale-ok", "release hotfix, corpus fixed next")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        led = read_text(os.path.join(c.find_project(self.repo).dir, "ledger.jsonl"))
        self.assertIn('"safety_waiver"', led)
        self.assertIn("release hotfix, corpus fixed next", led)
