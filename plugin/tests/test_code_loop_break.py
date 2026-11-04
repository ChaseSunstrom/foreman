"""T-2966: the third identical action in a step goes once to the planner (else escalate) profile, else the actor gets a
note naming the repetition; a journal event records each break; a run with no repeats sends nothing extra."""
import json

from test_code import CLOSE, FIX, M_PLAN, CodeCase, call, journal_text, plan

READ = call("read", path="calc.py")


def breaks(case):
    return [json.loads(l) for l in journal_text(case).splitlines() if '"loop_break"' in l]


class LoopBreak(CodeCase):
    def stuck(self, flag):
        fix = call("edit", file="calc.py", old="a - b", new="a + b")
        pl = flag == "--planner"  # escalate isn't asked the plan or the close notes: the actor is
        big = self.serve("anthropic", *([plan(M_PLAN), fix, CLOSE] if pl else [fix]), name="big")
        small = self.serve("anthropic", *([] if pl else [plan(M_PLAN)]), READ, READ, READ, call("done", summary="x"),
                           *([] if pl else [CLOSE]), name="small")
        return self.code("fix add", "--model", "small", flag, "big", check=False), big, small

    def test_the_third_repeat_goes_once_to_the_planner_and_the_actor_carries_on(self):
        self.check_break("--planner")

    def test_escalate_takes_it_when_no_planner_is_set(self):
        self.check_break("--escalate")

    def check_break(self, flag):
        r, big, small = self.stuck(flag)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        pl = flag == "--planner"
        self.assertEqual(len(small.seen), 4 if pl else 6, "three reads, then the actor carries on")
        self.assertEqual(len(big.seen), 3 if pl else 1, "plan+handoff+close, or the handoff only")
        self.assertIn("same action", big.said(1 if pl else 0))
        self.assertIn("same action", small.said(3 if pl else 4), "the actor is told what the stronger model did")
        self.assertEqual([b["action"] for b in breaks(self)], ["read"])

    def test_with_neither_profile_the_actor_gets_a_note(self):
        small = self.serve("anthropic", plan(M_PLAN), READ, READ, READ, *FIX, CLOSE, name="small")
        r = self.code("fix add", "--model", "small")
        self.assertEqual(len(small.seen), 7, r.stdout)
        self.assertIn("same action", small.said(4))
        self.assertNotIn("same action", small.said(3))
        self.assertEqual(len(breaks(self)), 1)

    def test_a_run_with_no_repeats_sends_nothing_extra(self):
        small = self.serve("anthropic", plan(M_PLAN), READ, *FIX, name="small")
        big = self.serve("anthropic", plan(M_PLAN), CLOSE, name="big")
        self.code("fix add", "--model", "small", "--planner", "big")
        self.assertEqual(len(big.seen), 2, "only the plan and the close notes")
        self.assertEqual(breaks(self), [])
