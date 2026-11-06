---
id: T-0900
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T16:45:27Z
updated: 2026-10-15T18:29:33Z
base: c83c73e0a33437f30c0c648ffb828f4886b3be5f
base_tree: f3b34eb3f3425feb53735270f14a93207345b891
verified: strong
---
# A close names the criteria nothing here could prove as a check-by-hand card
## Raw request
> FEATURE: fm task finish prints the criteria nothing could prove (typed, no command) as a check-by-hand card
> CONTEXT: round 6 #6
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a criterion with no verify of its own is listed to check by hand after done; one its own command proved isn't — verify with `python3 plugin/tests/run.py test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then the card in task done's output
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli test_demo` → exit 0 · Ran 95 tests in 17.9s (25 classes, 16 at a time; slowest: TaskLifecycle 18s, StateViews 7s, Checks 5s) / OK [ran] [tree a18b8335cbf7] (2026-10-15T18:26:50Z)
- `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 91 tests in 18.1s (24 classes, 16 at a time; slowest: TaskLifecycle 18s, StateViews 7s, Checks 4s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree a18b8335cbf7] (2026-10-15T18:27:27Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 91 tests in 18.0s (24 classes, 16 at a time; slowest: TaskLifecycle 18s, StateViews 6s, Checks 4s) / OK [ran] [tree a18b8335cbf7] (2026-10-15T18:27:27Z)
- (ac 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 91 tests in 17.7s (24 classes, 16 at a time; slowest: TaskLifecycle 18s, StateViews 6s, Checks 4s) / OK [ran] [tree a18b8335cbf7] (2026-10-15T18:29:32Z)
- (audit self) `self review: after done, every criterion not proved by its own command's fm-run evidence (no verify, or typed/generic only) is listed under 'Check by hand' and in JSON as check_by_hand; the verify suffix is stripped from the text` → no findings [tree a18b8335cbf7] (2026-10-15T18:29:32Z)
## Log
- 2026-10-15T16:45:27Z created
- 2026-10-15T16:45:31Z set tier=S
- 2026-10-15T18:25:38Z planned from capture
- 2026-10-15T18:25:38Z focused
- 2026-10-15T18:29:33Z done
- 2026-10-15T18:29:33Z committed 9374fab (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0777 [FEATURE M, done, 3 steps] Never idle without tmux: a plugin monitor streams this session's Foreman mail, and fm bus --wake prefers it over typing into tmux — les…
- T-0674 [FEATURE M, done, 3 steps] Milestone: Features — Observability, replay and trust — lesson: Check where secrets enter before adding redaction: every write path her…
- T-0870 [FEATURE M, done, 2 steps] fm demo: see Foreman work in a minute without model calls (a temp repo with a seeded bug: brief, guard block, red test, fix, evidence, …
- decision 2026-10-15: Round 6 slate: 6 builds from 49 grounded ideas (salvage on drop, research closes with a decision, fm spec from the user's examples, fm at, promise c…
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
