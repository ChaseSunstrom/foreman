# Critique — Mission 8, self (gen 1, #3, #7, #9, #11 and #12)

Tasks: T-2272, T-2349, T-2350, T-2351, T-2276, T-2355, T-2356, T-2357, T-2291, T-2353, T-2354, T-2281, T-2358, T-2359, T-2352, T-2290, T-2406, T-2407, T-2408, T-2449, T-2454, T-2360, T-2361, T-2362, T-2363, T-2384, T-2409, T-2364 (all done). Mission: gen-1/mission-self.md.

## Closed vs planned
- Every planned gap has its briefs closed (see the Mission's table); none is closed in the exam's sense until the
  end-of-run exam's session arms grade it.

## Outside signals
- The user's own requests are the one outside signal: the replay line in the Mission's Exam section, and the
  live next-request prediction below, which waits for a request of the user's to score it.

## Signals from Foreman's own tooling and its live tick
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
