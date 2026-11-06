---
id: T-2147
type: FIX
tier: M
status: done
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-10-30T10:52:15Z
updated: 2026-10-30T11:00:38Z
baseline: true
base: 70cdbe016946b76a15d16755ab4dfd38e75bf60d
base_tree: b71153f54940e943009d2693b59f6a3b768301dc
plan0_at: 2026-10-30T10:53:00Z
plan0_scope: []
verified: strong
---
# Baseline red: `python3 plugin/tests/run.py` fails…
## Raw request
> Baseline red: `python3 plugin/tests/run.py` fails test_docs.MasterShape.test_master_sections_are_grouped_folded_and_keep_every_note. Captured by fm check: the gates are red, so fix this before new work (it may not be this task's doing).
## Interpretation
T-2138 added a 17th note under Evidence, gates and verification; the map table still said 16.
## Assumptions (confidence)
## Acceptance criteria
- [x] the docs tests pass — verify with `python3 plugin/tests/run.py test_docs`
## Non-goals
## Approach (options → choice → why)
Bump the map table count to 17 (the test counts the notes). Only option worth having.
## Risks and rollback
## Execution prompt
## Steps
1. [x] bump the map count
## Resume here
## Docs impact
MASTER.md map table count (the fix itself).
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 80 tests in 8.3s (21 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree b71153f54940] (2026-10-30T10:53:12Z)
- (ac 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 80 tests in 8.2s (21 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree b71153f54940] (2026-10-30T10:53:31Z)
- (audit intent) `self: one-number diff in MASTER's map table; counted the section's notes (17) against the row` → the row now matches the note count test_docs counts [tree b71153f54940] (2026-10-30T10:53:31Z)
- (audit edge) `self: one-number diff in MASTER's map table; counted the section's notes (17) against the row` → no other map row changed; full docs suite green [tree b71153f54940] (2026-10-30T10:53:31Z)
## Log
- 2026-10-30T10:52:15Z created
- 2026-10-30T10:52:59Z planned: it has criteria and steps
- 2026-10-30T10:53:00Z focused
- 2026-10-30T10:53:16Z scope: MASTER.md map row only
- 2026-10-30T10:53:34Z done
- 2026-10-30T10:57:52Z guard authorization added: publish
- 2026-10-30T11:00:38Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2085 [FIX M, dropped, 0 steps] Baseline red: `python3 plugin/tests/run.py` fails…
- T-2021 [FIX M, dropped, 0 steps] Baseline red: `python3 plugin/tests/run.py` fails…
- T-1597 [FIX S, done, 1 steps] Baseline red: test_hooks.NoTaskGate stop-close and test_ideas parallel-lens tests failed under load — lesson: Under heavy machine load the …
- decision 2026-10-20: Slate, round 1: T-1254 cost per fully-correct session on the Benchmarks page; T-1255 the Claude Code version in every bench result; T-1256 piped tes…
- the similar finished task took 1 steps
## Regression test
none: test_docs.MasterShape is the test that went red; it now passes
## Why not caught
T-2138 ran only test_hooks while iterating; the docs count lives in test_docs, which only the full gate runs
## Lessons
- a new MASTER note bumps its group's map-table count; run test_docs after any MASTER edit
