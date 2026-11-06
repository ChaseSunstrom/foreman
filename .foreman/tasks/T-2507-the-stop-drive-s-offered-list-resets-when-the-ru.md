---
id: T-2507
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-01T19:41:16Z
updated: 2026-11-01T20:17:43Z
base: 47fdcaa598a13c6949a88b1ce622054a6b2799ef
base_tree: 38656c327dc19cd3a1b79ed513c30db3e0ff991e
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-01T19:56:06Z
plan0_scope: []
verified: strong
---
# The Stop drive offers each queued task once per active task, not once per background set
## Raw request
> FIX: the Stop drive's offered list resets when the running background set changes (fmhooks _drive: d['offered'] = [] on a new wait), so a side task drafted during an earlier wait is offered again; keep the offers for the active task's whole run (reset on focus change), so each queued task is offered once per active task
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a change in the running background set doesn't re-offer a side task already offered for the same active task; a new active task resets the offers — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then keep offers keyed to the active task
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.Stop.test_a_new_background_set_does_not_offer_the_same_side_task_again` → ✗ exit 1 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: Stop 1s) / FAILED (1 classes: test_hooks.Stop) [ran] [tree c4bbaad4a7b5] (2026-11-01T19:57:06Z)
- (step 1) `python3 plugin/tests/run.py test_hooks test_drive_side test_loop` → exit 0 · Ran 274 tests in 44.5s (38 classes, 16 at a time; slowest: Stop 44s, NoTaskGate 27s, PreToolUse 22s) / OK [ran] [tree addf775a132f] (2026-11-01T20:03:57Z)
- `python3 plugin/tests/run.py test_hooks.Stop.test_a_new_background_set_does_not_offer_the_same_side_task_again` → ✗ exit 1 · Ran 1 tests in 2.2s (1 classes, 16 at a time; slowest: Stop 1s) / FAILED (1 classes: test_hooks.Stop) (start tree + this task's tests) [ran] [tree addf775a132f] (2026-11-01T20:04:02Z)
- `python3 plugin/tests/run.py test_hooks.Stop.test_a_new_background_set_does_not_offer_the_same_side_task_again` → exit 0 · Ran 1 tests in 1.6s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree addf775a132f] (2026-11-01T20:04:02Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 245 tests in 43.1s (31 classes, 16 at a time; slowest: Stop 43s, NoTaskGate 26s, PreToolUse 20s) / OK [ran] [tree 79afa843aa2e] (2026-11-01T20:10:22Z)
- (audit edge) `self-review: the reset now keys on the active task (offered_for), not on the running set, so a new background job doesn't re-offer and a new active task gets its own round; the T-0401 per-wait cap (OFFERS_MAX) still ends a round` → the first Stop after upgrade has no offered_for, so it resets once; same jobs with a new active task reset too (the test pins both) [tree 79afa843aa2e] (2026-11-01T20:10:22Z)
- (audit self) `self-review: the reset now keys on the active task (offered_for), not on the running set, so a new background job doesn't re-offer and a new active task gets its own round; the T-0401 per-wait cap (OFFERS_MAX) still ends a round` → no findings [tree 79afa843aa2e] (2026-11-01T20:10:22Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm ask: text in a file; a run of a documented command proves it (--yes-run) / · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a f [ran] [tree 79afa843aa2e] (2026-11-01T20:11:47Z)
## Log
- 2026-11-01T19:41:16Z created
- 2026-11-01T19:56:06Z planned from capture
- 2026-11-01T19:56:06Z focused
- 2026-11-01T19:56:06Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-01T20:04:02Z scope: fmhooks _drive offered_for, test_hooks Stop test, MASTER, CHANGELOG
- 2026-11-01T20:11:23Z done
- 2026-11-01T20:11:25Z committed 9530de63 (4 files)
- 2026-11-01T20:11:47Z guard authorization added: publish
- 2026-11-01T20:17:43Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1899 [FIX S, done, 3 steps] Drive side work skips a task that waits on any open task, not only on the active one: draf — lesson: A wait rule that checks only the activ…
- T-0401 [FIX M, done, 3 steps] Drive: while background work runs, name a concrete queued task to start (builder lane / plan / block), offer up to 3 in turn, then wait — J…
- T-2495 [FIX S, done, 2 steps] Under economy mode the Stop drive offers main-thread prep, never a builder lane — lesson: a drive message is a per-turn cost: when a mode f…
- decision 2026-10-29: Keep the drive offering a new side task each Stop even when one was ignored
- similar finished tasks took 2–3 steps
## Plan gaps
- failed first: step 1 red test, then keep offers keyed to the active task
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
