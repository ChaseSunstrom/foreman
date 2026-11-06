---
id: T-2331
type: FEATURE
tier: L
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T13:39:48Z
updated: 2026-11-06T03:54:40Z
---
# Mission 8 (self, #7 #9 #11 #12 #3): write gen-1/mission-self.md, build its open briefs, write its critique
## Raw request
> Mission 8 (self, #7 #9 #11 #12 #3): write gen-1/mission-self.md, build its open briefs, write its critique
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] the Mission file passes its cold read and is filed — verify with `test -f state/projects/foreman-4a056f/research/genesis/gen-1/mission-self.md`
- [ ] each open brief is built test-first and its tests pass — verify with `python3 plugin/tests/run.py test_recall test_triggers test_outcomes test_lanes`
- [ ] its critique passes its cold read and is filed — verify with `test -f state/projects/foreman-4a056f/research/genesis/gen-1/critique-self.md`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Write the Mission from its pack and brainstorm, grounded in what's built (T-2272, T-2276, T-2281, T-2290, T-2291); fm genesis put it until its cold read passes; #3 anticipation and #11's trigger table each get a full pass or go to gen 2 as their own Mission  <- CURRENT
2. [ ] Build each open brief test-first (red, then green), one commit each
3. [ ] Write its critique (closed vs planned, zero-token outside signals, coverage cells, not-yet, spike verdicts, what failed); fm genesis put it
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-31T13:39:48Z created
- 2026-10-31T13:40:31Z plan: main-thread L umbrella (fm lane refuses L); Mission file drafted by one agent and filed via fm genesis put; open briefs intaken as S/M tasks and built in fm lanes in parallel; merged in mission order; critique after its briefs merge. Approaches: (1) Mission file in main thread + S/M brief lanes [chosen], (2) one raw worktree agent per Mission [no lane tracking], (3) sequential Missions [ignores the steer]
- 2026-10-31T13:40:42Z set approved=True
- 2026-10-31T15:00:17Z blocked: step 1 (file the Mission) waits on the user's call on the cold-read rule (decision 2026-10-31: tower filing waits; the draft is in the scratchpad, one fm genesis put away); step 2's briefs build in fm lanes meanwhile and close on their own tasks
- 2026-11-06T03:54:40Z dropped: superseded: Rune ran gens 2-4 since (seeds and critiques filed); gen-1's narrative filing no longer changes anything (2026-11-06 blocked review)
## Follow-ups captured
## Build vs reuse
Reuses the tower (fm genesis put/step, cold read), fm mission + fm ideas for the brainstorm, fm intake for its briefs, fm lane brief/merge for building, and the modules its built briefs already extended; nothing new outside its briefs
## Draft: Mission file and critique (unfiled, 2026-11-01)
# Mission 8 — self (gen 1, #7 self-repair, #9 orchestration, #11 self-triggering, #12 lean, #3 anticipation): as built, and its critique

Umbrella: T-2331. Parent: gen-1/seed.md row 8 → gen-0.md §2 #3, #7, #9, #11, #12, §3 (gaps: signal → fix loop, tier 3; trigger table, tier 4; model router,
tier 3; lean ratchet, tier 3; prediction scored, tier 4). Written after its briefs were built (the tower filing waits
on the user's call on the cold-read rule). Numbers: exam runs s21-013 and s11-012 (2026-11-01, zero-token arms),
fm triggers, fm outcomes --predictions.

## Briefs (26 built)
| Gap | Briefs | State |
|---|---|---|
| Signal → fix (#7) | T-2272, T-2349 (Foreman's own failures enter it), T-2350 (a failing steer check becomes a fix), T-2351 (self-fixes are registered trials) | done |
| Trigger table and watchers (#11) | T-2276, T-2355 (one table routes every event, with budgets), T-2356 (CI, issue and file watchers on a zero-token tick), T-2357 (timers staged, installed only on the user's yes) | done |
| Router and lanes (#9) | T-2291, T-2353 (the cheapest model that holds), T-2354 (stopped lanes recover by cause) | done |
| Lean (#12) | T-2281, T-2358 (hook p95 and injected context), T-2359 (net growth fails the sweep), T-2352 (the self-change gate at merge) | done |
| Prediction (#3) | T-2290 (effort), T-2406 (next request, scored against a naive baseline), T-2407 (draft ahead), T-2408 (breakage warnings), T-2449 and T-2454 (the path guess fixed after the replay) | done |
| Exam and surfaces | T-2360 watch, T-2361 recur and correction, T-2362 lanes, T-2363 lean, T-2384 long-horizon faults, T-2409 forecast and breakage, T-2364 surfaces | done |
Inbox (tier 2, captured): T-2365.

## Exam (zero tokens)
s21-013: the triggers arm closes 9/9 watch, the lanes drill 9/9 lanes, the foresight arm 18/18 forecast and breakage;
recur, correction, lean, parts and trigger need the session arms (end-of-run exam). s11-012: forecast type 8/9 against
the naive baseline's 0/9; breakage flagged 9/9 before the fake clock reached it, 0 false alarms. The replay of this
user's own requests (376 held out): type 259 against 256; paths 0.116 against 0.115 after T-2449 and T-2454 (0.052
against 0.086 before: the guess skipped the last request, cut to 5 paths and counted files outside the repo).

## Outside signals
- fm triggers: recurring-failure fired 3 times and all 3 were dropped (precision 0.00); no trigger has a fix that held
  yet ("fixes held" 0 everywhere); 5 self-fix trials are due.
- The tick runs live from the Stop hook's sweep while a session is open: today it made one next-request prediction
  (05:09Z, after T-2447) and ran the breakage pass (no warnings). That prediction waits for the next request of the
  user's own to score it; everything filed since has been Foreman's own captures. With no session open nothing ticks:
  the night timers aren't staged or installed (T-2357's path needs the user's yes).
- The live row exposed a bug: a request's paths included a file touched outside the repo (a scratchpad path, written
  as ../../..), so the guess and draft-ahead keys carried it (fixed by T-2454).
- The self-change gate's own mutation set found it blind to a hook that waits under load and to an added verb; both
  fixed in T-2363.

## The overload rule (seed: #3 and #11 each need a full pass or go to gen 2 as their own Mission)
- #3: its zero-token held-out scenarios pass and the predictor beats its baseline on the user's own history, but live
  it has one unscored prediction and the session arms haven't run. Not a full pass: #3 goes to gen 2 as its own
  Mission, graded on a week of live predictions and warnings.
- #11: the table, the watchers and the watch kind pass, and the tick runs while sessions are open; it has never run on
  a schedule. Same verdict: gen 2 gets a #11 Mission whose first criterion is a week of scheduled ticks with their
  captures graded.

## What failed
- The signal → fix loop's recurring-failure captures were all dropped: the signatures it groups aren't ones a fix
  addresses (3 of 3).
- Self-running stops when the session does: every Mission 8 trigger rides a tick that only an open session's Stop
  hook starts until the timers are installed.

## What the next Seed should change
- Stage the night timers and put the install to the user first thing (fm night --stage, one yes), then grade a week of
  live ticks: predictions scored, warnings scored, watcher captures and their precision.
- Rework recurring-failure grouping against its 3 drops before it fires again.
- #3 and #11 as their own gen-2 Missions, per the seed's overload rule.
## Briefs (26 built)
| Gap | Briefs | State |
|---|---|---|
| Signal → fix (#7) | T-2272, T-2349 (Foreman's own failures enter it), T-2350 (a failing steer check becomes a fix), T-2351 (self-fixes are registered trials) | done |
| Trigger table and watchers (#11) | T-2276, T-2355 (one table routes every event, with budgets), T-2356 (CI, issue and file watchers on a zero-token tick), T-2357 (timers staged, installed only on the user's yes) | done |
| Router and lanes (#9) | T-2291, T-2353 (the cheapest model that holds), T-2354 (stopped lanes recover by cause) | done |
| Lean (#12) | T-2281, T-2358 (hook p95 and injected context), T-2359 (net growth fails the sweep), T-2352 (the self-change gate at merge) | done |
| Prediction (#3) | T-2290 (effort), T-2406 (next request, scored against a naive baseline), T-2407 (draft ahead), T-2408 (breakage warnings), T-2449 and T-2454 (the path guess fixed after the replay) | done |
| Exam and surfaces | T-2360 watch, T-2361 recur and correction, T-2362 lanes, T-2363 lean, T-2384 long-horizon faults, T-2409 forecast and breakage, T-2364 surfaces | done |
Inbox (tier 2, captured): T-2365.

## Exam (zero tokens)
s21-013: the triggers arm closes 9/9 watch, the lanes drill 9/9 lanes, the foresight arm 18/18 forecast and breakage;
recur, correction, lean, parts and trigger need the session arms (end-of-run exam). s11-012: forecast type 8/9 against
the naive baseline's 0/9; breakage flagged 9/9 before the fake clock reached it, 0 false alarms. The replay of this
user's own requests (376 held out): type 259 against 256; paths 0.116 against 0.115 after T-2449 and T-2454 (0.052
against 0.086 before: the guess skipped the last request, cut to 5 paths and counted files outside the repo).

## Outside signals
- fm triggers: recurring-failure fired 3 times and all 3 were dropped (precision 0.00); no trigger has a fix that held
  yet ("fixes held" 0 everywhere); 5 self-fix trials are due.
- The tick runs live from the Stop hook's sweep while a session is open: today it made one next-request prediction
  (05:09Z, after T-2447) and ran the breakage pass (no warnings). That prediction waits for the next request of the
  user's own to score it; everything filed since has been Foreman's own captures. With no session open nothing ticks:
  the night timers aren't staged or installed (T-2357's path needs the user's yes).
- The live row exposed a bug: a request's paths included a file touched outside the repo (a scratchpad path, written
  as ../../..), so the guess and draft-ahead keys carried it (fixed by T-2454).
- The self-change gate's own mutation set found it blind to a hook that waits under load and to an added verb; both
  fixed in T-2363.

## The overload rule (seed: #3 and #11 each need a full pass or go to gen 2 as their own Mission)
- #3: its zero-token held-out scenarios pass and the predictor beats its baseline on the user's own history, but live
  it has one unscored prediction and the session arms haven't run. Not a full pass: #3 goes to gen 2 as its own
  Mission, graded on a week of live predictions and warnings.
- #11: the table, the watchers and the watch kind pass, and the tick runs while sessions are open; it has never run on
  a schedule. Same verdict: gen 2 gets a #11 Mission whose first criterion is a week of scheduled ticks with their
  captures graded.

## What failed
- The signal → fix loop's recurring-failure captures were all dropped: the signatures it groups aren't ones a fix
  addresses (3 of 3).
- Self-running stops when the session does: every Mission 8 trigger rides a tick that only an open session's Stop
  hook starts until the timers are installed.

## What the next Seed should change
- Stage the night timers and put the install to the user first thing (fm night --stage, one yes), then grade a week of
  live ticks: predictions scored, warnings scored, watcher captures and their precision.
- Rework recurring-failure grouping against its 3 drops before it fires again.
- #3 and #11 as their own gen-2 Missions, per the seed's overload rule.
## Briefs (26 built)
| Gap | Briefs | State |
|---|---|---|
| Signal → fix (#7) | T-2272, T-2349 (Foreman's own failures enter it), T-2350 (a failing steer check becomes a fix), T-2351 (self-fixes are registered trials) | done |
| Trigger table and watchers (#11) | T-2276, T-2355 (one table routes every event, with budgets), T-2356 (CI, issue and file watchers on a zero-token tick), T-2357 (timers staged, installed only on the user's yes) | done |
| Router and lanes (#9) | T-2291, T-2353 (the cheapest model that holds), T-2354 (stopped lanes recover by cause) | done |
| Lean (#12) | T-2281, T-2358 (hook p95 and injected context), T-2359 (net growth fails the sweep), T-2352 (the self-change gate at merge) | done |
| Prediction (#3) | T-2290 (effort), T-2406 (next request, scored against a naive baseline), T-2407 (draft ahead), T-2408 (breakage warnings), T-2449 (the path guess fixed after the replay) | done |
| Exam and surfaces | T-2360 watch, T-2361 recur and correction, T-2362 lanes, T-2363 lean, T-2384 long-horizon faults, T-2409 forecast and breakage, T-2364 surfaces | done |
Inbox (tier 2, captured): T-2365.

## Exam (zero tokens)
s21-013: the triggers arm closes 9/9 watch, the lanes drill 9/9 lanes, the foresight arm 18/18 forecast and breakage;
recur, correction, lean, parts and trigger need the session arms (end-of-run exam). s11-012: forecast type 8/9 against
the naive baseline's 0/9; breakage flagged 9/9 before the fake clock reached it, 0 false alarms. The replay of this
user's own requests (376 held out): type 259 against 256; paths 0.088 against 0.086 after T-2449 (0.052 before).

## Outside signals
- fm triggers: recurring-failure fired 3 times and all 3 were dropped (precision 0.00); no trigger has a fix that held
  yet ("fixes held" 0 everywhere); 5 self-fix trials are due.
- The tick runs live from the Stop hook's sweep while a session is open: today it made one next-request prediction
  (05:09Z, after T-2447) and ran the breakage pass (no warnings). That prediction waits for the next request of the
  user's own to score it; everything filed since has been Foreman's own captures. With no session open nothing ticks:
  the night timers aren't staged or installed (T-2357's path needs the user's yes).
- The live row exposed a bug: a request's paths included a file touched outside the repo (a scratchpad path, written
  as ../../..), so the guess and draft-ahead keys carried it (fixed in T-2454).
- The self-change gate's own mutation set found it blind to a hook that waits under load and to an added verb; both
  fixed in T-2363.

## The overload rule (seed: #3 and #11 each need a full pass or go to gen 2 as their own Mission)
- #3: its zero-token held-out scenarios pass and the predictor beats its baseline on the user's own history, but live
  it has one unscored prediction and the session arms haven't run. Not a full pass: #3 goes to gen 2 as its own
  Mission, graded on a week of live predictions and warnings.
- #11: the table, the watchers and the watch kind pass, and the tick runs while sessions are open; it has never run on
  a schedule. Same verdict: gen 2 gets a #11 Mission whose first criterion is a week of scheduled ticks with their
  captures graded.

## What failed
- The signal → fix loop's recurring-failure captures were all dropped: the signatures it groups aren't ones a fix
  addresses (3 of 3).
- Self-running stops when the session does: every Mission 8 trigger rides a tick that only an open session's Stop
  hook starts until the timers are installed.

## What the next Seed should change
- Stage the night timers and put the install to the user first thing (fm night --stage, one yes), then grade a week of
  live ticks: predictions scored, warnings scored, watcher captures and their precision.
- Rework recurring-failure grouping against its 3 drops before it fires again.
- #3 and #11 as their own gen-2 Missions, per the seed's overload rule.
## Briefs (26 built)
| Gap | Briefs | State |
|---|---|---|
| Signal → fix (#7) | T-2272, T-2349 (Foreman's own failures enter it), T-2350 (a failing steer check becomes a fix), T-2351 (self-fixes are registered trials) | done |
| Trigger table and watchers (#11) | T-2276, T-2355 (one table routes every event, with budgets), T-2356 (CI, issue and file watchers on a zero-token tick), T-2357 (timers staged, installed only on the user's yes) | done |
| Router and lanes (#9) | T-2291, T-2353 (the cheapest model that holds), T-2354 (stopped lanes recover by cause) | done |
| Lean (#12) | T-2281, T-2358 (hook p95 and injected context), T-2359 (net growth fails the sweep), T-2352 (the self-change gate at merge) | done |
| Prediction (#3) | T-2290 (effort), T-2406 (next request, scored against a naive baseline), T-2407 (draft ahead), T-2408 (breakage warnings), T-2449 (the path guess fixed after the replay) | done |
| Exam and surfaces | T-2360 watch, T-2361 recur and correction, T-2362 lanes, T-2363 lean, T-2384 long-horizon faults, T-2409 forecast and breakage, T-2364 surfaces | done |
Inbox (tier 2, captured): T-2365.

## Exam (zero tokens)
s21-013: the triggers arm closes 9/9 watch, the lanes drill 9/9 lanes, the foresight arm 18/18 forecast and breakage;
recur, correction, lean, parts and trigger need the session arms (end-of-run exam). s11-012: forecast type 8/9 against
the naive baseline's 0/9; breakage flagged 9/9 before the fake clock reached it, 0 false alarms. The replay of this
user's own requests (376 held out): type 259 against 256; paths 0.088 against 0.086 after T-2449 (0.052 before).

## Outside signals
- fm triggers: recurring-failure fired 3 times and all 3 were dropped (precision 0.00); no trigger has a fix that held
  yet ("fixes held" 0 everywhere); 5 self-fix trials are due.
- No live next-request prediction has been scored: the tick isn't scheduled (the night timers wait to be staged and
  get the user's yes, T-2357), so the book only runs when fm night --tick is called.
- The self-change gate's own mutation set found it blind to a hook that waits under load and to an added verb; both
  fixed in T-2363.

## The overload rule (seed: #3 and #11 each need a full pass or go to gen 2 as their own Mission)
- #3: its zero-token held-out scenarios pass, and the predictor beats its baseline on the user's own history, but none
  of it has run live (no scheduled tick) and the session arms haven't run. Not a full pass: #3 goes to gen 2 as its own
  Mission, starting from the live tick.
- #11: the table, the watchers and the watch kind pass; it too has never run on a schedule. Same verdict: gen 2 gets a
  #11 Mission whose first criterion is a week of scheduled ticks with their captures graded.

## What failed
- The signal → fix loop's recurring-failure captures were all dropped: the signatures it groups aren't ones a fix
  addresses (3 of 3).
- Nothing self-running runs: every Mission 8 trigger depends on a tick no timer starts.

## What the next Seed should change
- Stage the night timers and put the install to the user first thing (fm night --stage, one yes), then grade a week of
  live ticks: predictions scored, warnings scored, watcher captures and their precision.
- Rework recurring-failure grouping against its 3 drops before it fires again.
- #3 and #11 as their own gen-2 Missions, per the seed's overload rule.
