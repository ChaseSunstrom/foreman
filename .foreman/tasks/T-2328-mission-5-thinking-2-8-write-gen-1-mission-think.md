---
id: T-2328
type: FEATURE
tier: L
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T13:39:37Z
updated: 2026-11-06T03:54:35Z
---
# Mission 5 (thinking, #2 #8): write gen-1/mission-thinking.md, build its open briefs, write its critique
## Raw request
> Mission 5 (thinking, #2 #8): write gen-1/mission-thinking.md, build its open briefs, write its critique
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] the Mission file passes its cold read and is filed — verify with `test -f state/projects/foreman-4a056f/research/genesis/gen-1/mission-thinking.md`
- [ ] each open brief is built test-first and its tests pass — verify with `python3 plugin/tests/run.py test_reasoning test_core`
- [ ] its critique passes its cold read and is filed — verify with `test -f state/projects/foreman-4a056f/research/genesis/gen-1/critique-thinking.md`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Write the Mission from its pack and brainstorm, grounded in what's built (T-2269, T-2271, T-2277); fm genesis put it until its cold read passes  <- CURRENT
2. [ ] Build each open brief test-first (red, then green), one commit each
3. [ ] Write its critique (closed vs planned, zero-token outside signals, coverage cells, not-yet, spike verdicts, what failed); fm genesis put it
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-31T13:39:37Z created
- 2026-10-31T13:40:31Z plan: main-thread L umbrella (fm lane refuses L); Mission file drafted by one agent and filed via fm genesis put; open briefs intaken as S/M tasks and built in fm lanes in parallel; merged in mission order; critique after its briefs merge. Approaches: (1) Mission file in main thread + S/M brief lanes [chosen], (2) one raw worktree agent per Mission [no lane tracking], (3) sequential Missions [ignores the steer]
- 2026-10-31T13:40:41Z set approved=True
- 2026-10-31T15:00:16Z blocked: step 1 (file the Mission) waits on the user's call on the cold-read rule (decision 2026-10-31: tower filing waits; the draft is in the scratchpad, one fm genesis put away); step 2's briefs build in fm lanes meanwhile and close on their own tasks
- 2026-11-06T03:54:35Z dropped: superseded: Rune ran gens 2-4 since (seeds and critiques filed); gen-1's narrative filing no longer changes anything (2026-11-06 blocked review)
## Follow-ups captured
## Build vs reuse
Reuses the tower (fm genesis put/step, cold read), fm mission + fm ideas for the brainstorm, fm intake for its briefs, fm lane brief/merge for building, and the modules its built briefs already extended; nothing new outside its briefs
## Draft: Mission file and critique (unfiled, 2026-11-01)
# Mission 5 — thinking (gen 1, #2 exhaustive thinking, #8 calibrated judgment): as built, and its critique

Umbrella: T-2328. Parent: gen-1/seed.md row 5 → gen-0.md §2 #2 and #8, §3 (gaps: readings/approaches gate by tier, tier 3; auto race by evidence,
tier 4; unsure → research trigger, tier 3). Written after its briefs were built: the tower filing waits on the user's
call on the cold-read rule (decision 2026-10-31), so this records what was planned in the briefs and what closed.
Numbers: exam run s21-013 (2026-11-01, zero-token arms) and fm calibration.

## Briefs (13 built, all tier 3-4)
| Gap | Briefs | State |
|---|---|---|
| Readings and approaches gated by tier | T-2269 (M/L Approach: 3+ options and a choice), T-2335 (readings and each option's outcome), T-2277 + T-2336 (blast radius in the plan) | done |
| Race by evidence | T-2271 (the stuck ladder races the runner-up), T-2339 (race at plan time), T-2340 (L plans race their design as spikes), T-2341 (a cold rival reads the request) | done |
| Unsure → research, judgment at doors | T-2337 (calibration ledger: each stated confidence a write-once bet), T-2338 (confidence routes the next step), T-2342 (stop only at an irreversible, ambiguous step) | done |
| Exam and surfaces | T-2343 (race, fork, door, unsure kinds, child-authored), T-2344 (fm code, MCP, AGENTS, site, pane) | done |
Inbox (tier 2, captured): T-2345 to T-2348, T-2403. T-2402 (a second model's key on one-way doors) waits on a grant.

## Exam
#2 kinds: ambiguous, exists, race; #8 kinds: ambiguous, clean, fork, door, unsure, each 9 a kind with 3 held out and an
outside author. s21-013: the oracle closes all 63 scenarios, empty closes only the 9 clean ones, and the finders find
fork's planted defects (9/9) but fix nothing, so they close none. No zero-token arm can do these kinds' work (they grade
what an answer reads and decides); the foreman and plain arms run them at the end-of-run exam.

## Outside signals
- Calibration ledger: 45 bets pending, 0 of the 20 it needs scored, so no bar has moved (research 70, race 55). #8's
  core claim, that stated confidence matches outcomes, is unproven a day in.
- Effort predictions (T-2290, Mission 8, a #8 signal): 67% within 2x over 79 closes, against 64% for the naive median.
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
## Briefs (13 built, all tier 3-4)
| Gap | Briefs | State |
|---|---|---|
| Readings and approaches gated by tier | T-2269 (M/L Approach: 3+ options and a choice), T-2335 (readings and each option's outcome), T-2277 + T-2336 (blast radius in the plan) | done |
| Race by evidence | T-2271 (the stuck ladder races the runner-up), T-2339 (race at plan time), T-2340 (L plans race their design as spikes), T-2341 (a cold rival reads the request) | done |
| Unsure → research, judgment at doors | T-2337 (calibration ledger: each stated confidence a write-once bet), T-2338 (confidence routes the next step), T-2342 (stop only at an irreversible, ambiguous step) | done |
| Exam and surfaces | T-2343 (race, fork, door, unsure kinds, child-authored), T-2344 (fm code, MCP, AGENTS, site, pane) | done |
Inbox (tier 2, captured): T-2345 to T-2348, T-2403. T-2402 (a second model's key on one-way doors) waits on a grant.

## Exam
#2 kinds: ambiguous, exists, race; #8 kinds: ambiguous, clean, fork, door, unsure, each 9 a kind with 3 held out and an
outside author. s21-013: the oracle closes all 63 scenarios, empty closes only the 9 clean ones, and the finders find
fork's planted defects (9/9) but fix nothing, so they close none. No zero-token arm can do these kinds' work (they grade
what an answer reads and decides); the foreman and plain arms run them at the end-of-run exam.

## Outside signals
- Calibration ledger: 45 bets pending, 0 of the 20 it needs scored, so no bar has moved (research 70, race 55). #8's
  core claim, that stated confidence matches outcomes, is unproven a day in.
- Effort predictions (T-2290, Mission 8, a #8 signal): 67% within 2x over 79 closes, against 64% for the naive median.
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
