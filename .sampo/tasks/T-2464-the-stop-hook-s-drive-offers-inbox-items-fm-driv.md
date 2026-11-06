---
id: T-2464
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-01T09:18:36Z
updated: 2026-11-01T09:34:39Z
base: 60f0bc698baaf47180a67cbbd156ec74c2b94009
base_tree: 1fdc556cffb9d0e8d323bfa812c7ae958e666cff
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-01T09:18:37Z
plan0_scope: []
verified: strong
---
# The Stop hook's drive offers inbox items fm drive --round-first holds (its inbox pick and its planning list skip _round_held)
## Raw request
> The Stop hook's drive offers inbox items fm drive --round-first holds (its inbox pick and its planning list skip _round_held)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the full-autonomy drive names no round-held inbox item — verify with `python3 plugin/tests/run.py test_hooks test_core`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then add the round-held ids to _drive's blocked set
## Resume here
## Docs impact
none: internal hook behaviour MASTER already describes under fm drive --round-first
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_full_autonomy_drive_skips_inbox_items_the_round_holds test_hooks` → ✗ exit 1 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: Stop 1s) / FAILED (1 classes: test_hooks.Stop) [ran] [tree 508a5cad33d4] (2026-11-01T09:18:46Z)
- (step 1) `python3 plugin/tests/run.py test_hooks test_core` → exit 0 · Ran 375 tests in 44.6s (57 classes, 16 at a time; slowest: Stop 44s, NoTaskGate 30s, PreToolUse 24s) / OK [ran] [tree 1ea9f5f6b8f3] (2026-11-01T09:19:42Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks test_core` → exit 0 · Ran 375 tests in 52.5s (57 classes, 16 at a time; slowest: Stop 52s, NoTaskGate 37s, PreToolUse 32s) / OK [ran] [tree 1ea9f5f6b8f3] (2026-11-01T09:20:42Z)
- `python3 plugin/tests/run.py -k test_full_autonomy_drive_skips_inbox_items_the_round_holds test_hooks` → ✗ exit 1 · Ran 1 tests in 1.7s (1 classes, 16 at a time; slowest: Stop 0s) / FAILED (1 classes: test_hooks.Stop) (start tree + this task's tests) [ran] [tree 1ea9f5f6b8f3] (2026-11-01T09:27:48Z)
- `python3 plugin/tests/run.py -k test_full_autonomy_drive_skips_inbox_items_the_round_holds test_hooks` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Stop 0s) / OK [ran] [tree 1ea9f5f6b8f3] (2026-11-01T09:27:48Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks test_core` → exit 0 · Ran 375 tests in 41.3s (57 classes, 16 at a time; slowest: Stop 41s, NoTaskGate 26s, PreToolUse 21s) / OK [ran] [tree 1ea9f5f6b8f3] (2026-11-01T09:28:35Z)
- (audit intent) `main-thread lens pass over the 3-line diff and its test` → the Stop hook's inbox pick and planning list skip what _round_held holds [tree 1ea9f5f6b8f3] (2026-11-01T09:28:35Z)
- (audit edge) `main-thread lens pass over the 3-line diff and its test` → round-first off gives an empty set; urgent or depended-on captures are never held [tree 1ea9f5f6b8f3] (2026-11-01T09:28:35Z)
- (audit operator) `main-thread lens pass over the 3-line diff and its test` → held items are no longer named each Stop; hook bench green [tree 1ea9f5f6b8f3] (2026-11-01T09:28:35Z)
- (audit self) `main-thread lens pass over the 3-line diff and its test` → no findings [tree 1ea9f5f6b8f3] (2026-11-01T09:28:35Z)
## Log
- 2026-11-01T09:18:36Z created
- 2026-11-01T09:18:36Z focused
- 2026-11-01T09:18:37Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-01T09:19:49Z scope: plugin/lib/fmhooks.py (_drive) and plugin/tests/test_hooks.py only
- 2026-11-01T09:29:31Z done
- 2026-11-01T09:29:34Z committed 4f7b9504 (2 files)
- 2026-11-01T09:29:40Z guard authorization added: publish
- 2026-11-01T09:34:39Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2459 [FIX S, done, 2 steps] Round first covers the drive's side-work offers too: while background work runs, the Stop hook offered T-2365 (filed by Foreman) despite fm…
- T-1866 [FEATURE M, done, 7 steps] Backlog swipe everywhere: app view, terminal loop, pick explores, prefer --reset — lesson: A loop that applies one verdict at a time mu…
- T-2317 [FIX S, done, 1 steps] A batch host held by a builder lane keeps its members out of the main inbox — lesson: A filter that looks things up by id must look in the …
- decision 2026-11-01: [revisited: T-2450 (the secrets finder reads a date as a credential)] [cites: user steer 2026-10-31: finish round 1 completely, in order; no new mai…
## Lessons
- A hold must be honoured wherever work is offered: grep every place that names inbox items
## Plan gaps
- failed first: step 1 red test, then add the round-held ids to _drive's blocked set
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
