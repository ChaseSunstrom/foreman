# Critique — Mission 5, thinking (gen 1, #2 and #8)

Tasks: T-2269, T-2335, T-2277, T-2336, T-2271, T-2339, T-2340, T-2341, T-2337, T-2338, T-2342, T-2343, T-2344 (all done). Mission: gen-1/mission-thinking.md. Numbers: exam run s21-013 (2026-11-01,
zero-token arms), fm outcomes --judgment and fm outcomes --predictions (2026-11-01).

## Closed vs planned
- Every planned gap has its briefs closed (see the Mission's table); none is closed in the exam's sense yet: #2 and #8's
  kinds grade what an answer reads and decides, which only the foreman and plain arms do, at the end-of-run exam.

## Outside signals
- Calibration ledger: 51 bets pending, 0 of the 20 it needs scored, so no bar has moved (research 70, race 55). #8's
  core claim, that stated confidence matches outcomes, is unproven a day in.
- Effort predictions (T-2290, Mission 8, a #8 signal): 63% hit over 93 scored, against 60% for the naive baseline (fm outcomes --predictions).
- Coverage: #2 has 6 cells filled; #8 has 2, the thinnest capability on the grid.

## What failed
- T-2277's blast-radius line fired on 0 of 33 M/L briefs (none had scope paths); T-2336 fixed it. A gate that never
  fires looked like a gate that passes.
- The door gate refused T-2357 at focus: "writes nothing outside state" read as destructive because `_NEGATE` misses
  "nothing" (captured T-2444, open).
- The calibration ledger scores bets only as signals arrive, so a day of work moves nothing; #8 can't be judged yet.

## What the next Seed should change
- Give the calibration ledger a fast signal: score a bet at its task's close (criteria green, reverted or not), not
  only on later outcomes, and show the bars moving on the scorecard.
- Fill #8's surfaces (2 cells): confidence and doors on fm code, MCP and the pane, as #2's are.
- Fix T-2444 and replay the door gate over past steps for other negations it misreads.
