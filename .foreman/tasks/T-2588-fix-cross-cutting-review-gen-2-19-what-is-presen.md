---
id: T-2588
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-02T08:23:31Z
updated: 2026-11-02T09:46:09Z
trigger: genesis-review
trigger_key: b59d8d28ff4e958a
base: d94ddfbbef8fdd94aee8bc9e3350a2a3d54cd6ab
base_tree: e854f31b39f0c7eaa0a35c86a0494d4b53673b7f
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T09:39:24Z
plan0_scope: []
verified: strong
---
# fm doctor's reflex-prompts row says no prompts were recorded and why (bypass mode shows none) instead of 'none qualified' when the store is empty
## Raw request
> FIX: cross-cutting review gen-2 #19 (what is presented ahead of its proof): The doctor names allow rules such as `Bash(git status *)` from timings whose source, the permission dialog, is invisible in the mode the user runs; the row can only ever read "none" until that is shown otherwise. [5c549eeb]
> genesis-review 2:19
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with no recorded prompts the row reads 'no permission prompts recorded yet (bypass mode shows none; T-2565 checks after sessions that show prompts)'; with prompts but no reflex class it reads 'N prompt(s), M timed; none qualified' as before — verify with `python3 plugin/tests/run.py test_anergy`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_anergy
2. [x] branch on prompts == 0 in fmdoctor.check_anergy
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_anergy` → ✗ exit 1 · Ran 11 tests in 4.1s (1 classes, 16 at a time; slowest: Anergy 4s) / FAILED (1 classes: test_anergy.Anergy) [ran] [tree cced75f83c2c] [world 2f1906870a] (2026-11-02T09:39:34Z)
- (step 2) `python3 plugin/tests/run.py test_anergy test_doctor` → exit 0 · Ran 117 tests in 4.5s (37 classes, 16 at a time; slowest: Anergy 4s, ViewsRepair 3s, LockProbe 3s) / OK [ran] [tree 845b45dab6da] [world 2f1906870a] (2026-11-02T09:39:53Z)
- `python3 plugin/tests/run.py test_anergy` → ✗ exit 1 · Ran 11 tests in 5.0s (1 classes, 16 at a time; slowest: Anergy 4s) / FAILED (1 classes: test_anergy.Anergy) (start tree + this task's tests) [ran] [tree 0becb4174568] [world 2f1906870a] (2026-11-02T09:45:42Z)
- `python3 plugin/tests/run.py test_anergy` → exit 0 · Ran 11 tests in 4.1s (1 classes, 16 at a time; slowest: Anergy 4s) / OK [ran] [tree 0becb4174568] [world 2f1906870a] (2026-11-02T09:45:42Z)
- (ac 1) `python3 plugin/tests/run.py test_anergy` → exit 0 · Ran 11 tests in 4.0s (1 classes, 16 at a time; slowest: Anergy 4s) / OK [ran] [tree 0becb4174568] [world 2f1906870a] (2026-11-02T09:45:48Z)
- (audit intent) `self-review: an empty store returns a PASS row naming why (bypass mode) and the T-2565 check; a store with prompts keeps the counts and 'none qualified'` → an empty store says no prompts were recorded and why; one prompt reads 'none qualified' (test) [tree 0becb4174568] (2026-11-02T09:45:48Z)
- (audit operator) `self-review: an empty store returns a PASS row naming why (bypass mode) and the T-2565 check; a store with prompts keeps the counts and 'none qualified'` → the row is advisory either way; a user in a prompting mode sees real counts after their first prompt [tree 0becb4174568] (2026-11-02T09:45:48Z)
- (audit self) `self-review: an empty store returns a PASS row naming why (bypass mode) and the T-2565 check; a store with prompts keeps the counts and 'none qualified'` → no findings [tree 0becb4174568] (2026-11-02T09:45:48Z)
## Log
- 2026-11-02T08:23:31Z created
- 2026-11-02T09:06:42Z planned from capture
- 2026-11-02T09:39:23Z set approved=True
- 2026-11-02T09:39:23Z focused
- 2026-11-02T09:39:24Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T09:46:06Z done
- 2026-11-02T09:46:09Z committed 896cf76c (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2563 [FEATURE M, done, 3 steps] Anergy for permission prompts: time each prompt to its PostToolUse and report reflex-approved command classes (spike) — lesson: A spike…
- T-2578 [FIX L, dropped, 0 steps] FIX: cross-cutting review gen-2 #9 (what grew without earning it): 99 +++ / The…
- T-2586 [FIX L, dropped, 0 steps] FIX: cross-cutting review gen-2 #17 (what is presented ahead of its proof): T-2505 seals…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
## Lessons
- A row reading 'none' must say whether that's a measurement or an absence of data
## Plan gaps
- failed first: step 1 red test in test_anergy
## Files touched
- plugin/tests/test_anergy.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
