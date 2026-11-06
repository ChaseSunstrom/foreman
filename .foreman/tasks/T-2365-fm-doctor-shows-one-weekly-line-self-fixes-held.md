---
id: T-2365
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T14:01:20Z
updated: 2026-11-01T19:09:37Z
group: Mission 8 surfaces
base: 7ba4f75dc334cbe92eaeeca27d0ac28c8b4901f1
base_tree: 06d7a6b8252cb2411b6f13497b96786500b76f21
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-01T19:02:32Z
plan0_scope: []
verified: strong
---
# fm doctor shows one line for the last 7 days of self-fix trials: how many held and how many did not
## Raw request
> fm doctor shows one weekly line: self-fixes held vs did not hold (Mission 8 inbox, tier 2; reads brief T-2351's trial verdicts)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm doctor prints the week's self-fix trials as held against not held, and says none when there were none — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then the line from fmtrials' verdicts
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_doctor.SelfFixWeek` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: SelfFixWeek 0s) / FAILED (1 classes: test_doctor.SelfFixWeek) [ran] [tree b8504c067955] (2026-11-01T19:02:42Z)
- (step 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 102 tests in 4.4s (33 classes, 16 at a time; slowest: ViewsRepair 4s, LockProbe 3s, Timing 2s) / OK [ran] [tree 039c75422ac1] (2026-11-01T19:03:26Z)
- `python3 plugin/tests/run.py test_doctor.SelfFixWeek` → ✗ exit 1 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: SelfFixWeek 0s) / FAILED (1 classes: test_doctor.SelfFixWeek) (start tree + this task's tests) [ran] [tree 039c75422ac1] (2026-11-01T19:03:29Z)
- `python3 plugin/tests/run.py test_doctor.SelfFixWeek` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: SelfFixWeek 0s) / OK [ran] [tree 039c75422ac1] (2026-11-01T19:03:29Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 102 tests in 4.2s (33 classes, 16 at a time; slowest: ViewsRepair 4s, LockProbe 3s, Command 2s) / OK [ran] [tree 039c75422ac1] (2026-11-01T19:09:12Z)
- (audit edge) `self-review: the line reads only stored verdicts (no regrading), windows by at+by days within the last 7, skips malformed rows and non-self-fix trials; WARN only on a didn't-hold since its FIX is filed already` → no project, no trials, a garbage timestamp, a pending trial, an old one and a plain metric trial are each excluded or counted as the test pins [tree 039c75422ac1] (2026-11-01T19:09:12Z)
- (audit self) `self-review: the line reads only stored verdicts (no regrading), windows by at+by days within the last 7, skips malformed rows and non-self-fix trials; WARN only on a didn't-hold since its FIX is filed already` → no findings [tree 039c75422ac1] (2026-11-01T19:09:12Z)
## Log
- 2026-10-31T14:01:20Z created
- 2026-11-01T18:21:11Z planned from capture
- 2026-11-01T19:02:32Z focused
- 2026-11-01T19:02:32Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-01T19:03:37Z scope: fmdoctor check_self_fixes + wiring, test_doctor SelfFixWeek, MASTER, CHANGELOG
- 2026-11-01T19:09:35Z done
- 2026-11-01T19:09:37Z committed f3c59a14 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2351-review: T-2351 review (fm-reviewer, one pass): changes needed; fixed before close (new tests written with the fixes).
- T-2077 [RESEARCH L, blocked, 8 steps] Genesis gen 1: Missions 2-8, critiques, lineage, sweep, gen-2 Seed
- T-2124 [FEATURE M, done, 2 steps] Scout project probes: fm find + prove on the user's own project, at most 3 a day, proven only, refutation ledger, doctor faults to the …
- decision 2026-10-30: Doctor faults from user projects go to Foreman's own inbox as source scout, deduped by the self project's scout_keys
- similar past tasks were M: consider --tier M
- the similar finished task took 2 steps
## Plan gaps
- failed first: step 1 red test, then the line from fmtrials' verdicts
## Files touched
- plugin/tests/test_doctor.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
- MASTER.md
