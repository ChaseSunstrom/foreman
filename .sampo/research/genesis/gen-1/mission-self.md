# Mission 8 — self (gen 1, #7 self-repair, #9 orchestration, #11 self-triggering, #12 lean, #3 anticipation): as built

Task: T-2272, T-2349, T-2350, T-2351, T-2276, T-2355, T-2356, T-2357, T-2291, T-2353, T-2354, T-2281, T-2358, T-2359, T-2352, T-2290, T-2406, T-2407, T-2408, T-2449, T-2454, T-2360, T-2361, T-2362, T-2363, T-2384, T-2409, T-2364 (the briefs below, done).

Umbrella: T-2331. Parent: gen-1/seed.md row 8 → gen-0.md §2 #3, #7, #9, #11, #12, §3 (gaps: signal → fix loop, tier 3; trigger table, tier 4; model router,
tier 3; lean ratchet, tier 3; prediction scored, tier 4). Written after its briefs were built, while tower filing waited on the user's call on the cold-read rule (decided
2026-11-01). Numbers: exam runs s21-013 and s11-012 (2026-11-01, zero-token arms),
fm triggers, fm outcomes --predictions.

## Briefs (28 built)
State is each brief's own; in the exam, recur, correction, lean, parts and trigger close only at the end-of-run
exam's session arms.

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
user's own requests (376 held out): type 259 against the naive 256 on both runs; paths 0.088 against 0.086 on
s21-013 (after T-2449: the guess had skipped the last request and cut to 5 paths) and 0.052 against 0.086 on s11-012
(before it). T-2454 (paths outside the repo) landed after both runs; the next run measures it.
