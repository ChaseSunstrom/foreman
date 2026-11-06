---
id: T-0896
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T16:45:27Z
updated: 2026-10-15T16:59:13Z
base: 468a790b089689f735e1aa87549f98db3d755fcb
base_tree: 577cdcc371a8328c8a500d31e435ccd8528b98b0
verified: strong
---
# A RESEARCH task can't close without a Decision section, and its decision lands in decision
## Raw request
> FEATURE: A RESEARCH task can't close without a Decision section, and its decision lands in decisions.md
> CONTEXT: round 6 #29. fmcli warns at close (T-0599) only
## Interpretation
Closing a RESEARCH task needs a Decision section (or 'none: <why>'); on close, a real decision is recorded in decisions.md with the task id, so research ends in a choice the project keeps. Replaces the close-time warning (T-0599).
## Assumptions (confidence)
## Acceptance criteria
- [x] a RESEARCH task without a Decision is refused; with one, decisions.md gets it — verify with `python3 plugin/tests/run.py test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_cli DecisionsResearchSelf, then the gate and the decisions.md row
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli test_night test_skills test_docs` → exit 0 · Ran 130 tests in 25.3s (37 classes, 16 at a time; slowest: TaskLifecycle 25s, StateViews 8s, Checks 5s) / OK [ran] [tree b384d49dc995] (2026-10-15T16:50:47Z)
- `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 89 tests in 21.8s (24 classes, 16 at a time; slowest: TaskLifecycle 21s, StateViews 10s, Checks 8s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree b384d49dc995] (2026-10-15T16:51:27Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 89 tests in 18.0s (24 classes, 16 at a time; slowest: TaskLifecycle 18s, StateViews 7s, Checks 4s) / OK [ran] [tree b384d49dc995] (2026-10-15T16:51:27Z)
- (step 1) `python3 plugin/tests/run.py test_cli test_knowledge test_night` → exit 0 · Ran 107 tests in 19.0s (35 classes, 16 at a time; slowest: TaskLifecycle 19s, StateViews 8s, Checks 5s) / OK [ran] [tree 22a2b2eaacbc] (2026-10-15T16:57:18Z)
- (ac 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 89 tests in 18.1s (24 classes, 16 at a time; slowest: TaskLifecycle 18s, StateViews 7s, Checks 5s) / OK [ran] [tree 22a2b2eaacbc] (2026-10-15T16:59:12Z)
- (audit self) `self review: RESEARCH done needs a Decision (or 'none: why'); a real one is written to decisions.md with the task id and title; the close warning it replaces and its test were updated; brainstorm skill step 8 says to set it` → no findings [tree 22a2b2eaacbc] (2026-10-15T16:59:12Z)
## Log
- 2026-10-15T16:45:27Z created
- 2026-10-15T16:45:31Z set tier=S
- 2026-10-15T16:49:12Z focused
- 2026-10-15T16:59:12Z done
- 2026-10-15T16:59:13Z committed 8367c00 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0674 [FEATURE M, done, 3 steps] Milestone: Features — Observability, replay and trust — lesson: Check where secrets enter before adding redaction: every write path her…
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- T-0672 [SECURITY L, done, 6 steps] Milestone: Features — Guard and safety — lesson: a safety claim shown to the user (restorable) must state its limits; a reviewer will …
- decision 2026-10-15: Round 6 slate: 6 builds from 49 grounded ideas (salvage on drop, research closes with a decision, fm spec from the user's examples, fm at, promise c…
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- plugin/skills/brainstorm/SKILL.md
- plugin/tests/test_knowledge.py
