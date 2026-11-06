---
id: T-2513
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py]
depends_on: []
source: discovered
created: 2026-11-01T22:21:17Z
updated: 2026-11-01T23:06:26Z
base: 51450637af73810e156c0ff15f5ad27053c4c778
base_tree: 49eb7c429fd3ffb4e701c307dcac67efe01c462f
predict_minutes: 7
predict_attempts: 1
plan0_at: 2026-11-01T22:39:26Z
plan0_scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py]
verified: strong
---
# The Stop drive offers each queued side task once per session, not once per active task
## Raw request
> Stop drive re-offers a side task already drafted this session: offered resets when the active task changes (T-2507), so T-2498 and T-2512 were offered again after T-2511 → T-2367; remember drafted side tasks per session, not per active task
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] after the active task changes, a side task offered under the earlier one isn't offered again in the same session; an unoffered one still is — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test beside T-2507's: offer X under task A, finish A and focus B, a new background set: the offer is Y, never X
2. [x] fmhooks._drive: on an active-task change carry the offered ids into a session-long list and keep them out of _side_work; OFFERS_MAX still counts per active task
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.Stop.test_a_new_background_set_does_not_offer_the_same_side_task_again test_hooks.Stop.test_a_side_task_planned_since_its_offer_is_offered_once_more_for_its_draft` → exit 0 · Ran 2 tests in 2.9s (1 classes, 16 at a time; slowest: Stop 3s) / OK [ran] [tree 9506e372eeca] (2026-11-01T22:42:16Z)
- (step 2) `python3 plugin/tests/run.py test_hooks test_drive_side` → exit 0 · Ran 254 tests in 46.6s (34 classes, 16 at a time; slowest: Stop 46s, NoTaskGate 28s, PreToolUse 22s) / OK [ran] [tree 9506e372eeca] (2026-11-01T22:43:03Z)
- `python3 plugin/tests/run.py test_hooks.Stop.test_a_new_background_set_does_not_offer_the_same_side_task_again test_hooks.Stop.test_a_side_task_planned_since_its_offer_is_offered_once_more_for_its_draft` → ✗ exit 1 · Ran 2 tests in 3.9s (1 classes, 16 at a time; slowest: Stop 3s) / FAILED (1 classes: test_hooks.Stop) (start tree + this task's tests) [ran] [tree 9506e372eeca] (2026-11-01T22:43:11Z)
- `python3 plugin/tests/run.py test_hooks.Stop.test_a_new_background_set_does_not_offer_the_same_side_task_again test_hooks.Stop.test_a_side_task_planned_since_its_offer_is_offered_once_more_for_its_draft` → exit 0 · Ran 2 tests in 2.9s (1 classes, 16 at a time; slowest: Stop 3s) / OK [ran] [tree 9506e372eeca] (2026-11-01T22:43:11Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 246 tests in 45.0s (31 classes, 16 at a time; slowest: Stop 45s, NoTaskGate 26s, PreToolUse 21s) / OK [ran] [tree 1b20ca6813c8] (2026-11-01T22:50:40Z)
- (audit edge) `self-review: offered still counts per active task for OFFERS_MAX; made holds id:status for the session (the drive file is per session), and skip adds only ids whose current status was already offered, so a task that moved from captured to planned is offered once more; status comes from briefs on both the record and the check, so they agree` → same stage under a new active task is skipped; a stage change is offered; a task offered under A and active later is excluded by _side_work anyway [tree 1b20ca6813c8] (2026-11-01T22:50:40Z)
- (audit self) `self-review: offered still counts per active task for OFFERS_MAX; made holds id:status for the session (the drive file is per session), and skip adds only ids whose current status was already offered, so a task that moved from captured to planned is offered once more; status comes from briefs on both the record and the check, so they agree` → no findings [tree 1b20ca6813c8] (2026-11-01T22:50:40Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm ask: text in a file; a run of a documented command proves it (--yes-run) / · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a f [ran] [tree 8174bc759256] (2026-11-01T23:00:12Z)
## Log
- 2026-11-01T22:21:17Z created
- 2026-11-01T22:21:37Z planned from capture
- 2026-11-01T22:22:07Z steer: key the session memory on id:status, so a captured task's plan and its later draft are separate stages; T-2507's test's last assertion flips (it encoded the re-offer)
- 2026-11-01T22:39:24Z focused
- 2026-11-01T22:39:26Z predicted from its closes: 7 min, 1 attempt(s)
- 2026-11-01T22:43:11Z scope: CHANGELOG.md entry
- 2026-11-01T22:51:43Z done
- 2026-11-01T22:51:45Z committed 543a8bb8 (3 files)
- 2026-11-01T23:00:12Z guard authorization added: publish
- 2026-11-01T23:06:26Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2507 [FIX S, done, 1 steps] The Stop drive offers each queued task once per active task, not once per background set
- T-1899 [FIX S, done, 3 steps] Drive side work skips a task that waits on any open task, not only on the active one: draf — lesson: A wait rule that checks only the activ…
- T-2374 [FEATURE M, done, 4 steps] Install-grant queue (Mission 6, #5): fm ask --later queues a user-only grant that never expires, with the miss, the alternatives and th…
- decision 2026-10-30: T-2105: Genesis offers itself through fm scout (probe_genesis, once ever, ≥10 done tasks, no tower, nothing queued) as a confirm task, not a new fm …
- similar finished tasks took 1–4 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_hooks.py
## Why not caught
T-2507's test asserted the re-offer under a new active task as the intended behavior; only this session's log showed it re-drafting finished work (T-2498 offered for a draft under T-2511 and again under T-2367).
## Lessons
- Remember what a session already did by what it was asked (task plus stage), not by which task was active when it was asked
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
