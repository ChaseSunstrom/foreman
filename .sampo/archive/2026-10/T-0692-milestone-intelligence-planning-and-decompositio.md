---
id: T-0692
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:18Z
updated: 2026-10-09T20:46:04Z
batch: [T-0645, T-0666]
base: 8173461b0a89ce7c4dd96f9aea476d6f13154943
base_tree: bacbcb1881ed926b96c0d84617a142b84bf528e5
verified: strong
---
# Milestone: Intelligence — Planning and decomposition (2)
## Raw request
> T-0645: FEATURE: Plan from history (I019, value 3/5, effort M, risk low)
>   first version: Record per-step outcomes at finish (steps added late, steps that failed) and have fm recall surface 'steps similar plans forgot' for the new brief. Falsifiable plan predictions graded at finish piggyback on it.
>   what it is: Reuses a pattern library, scores plans and templates against replayed outcomes and spots novel problem classes.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 7 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0666: FEATURE: Plan as a graph or compiled object (I014, value 3/5, effort L, risk med)
>   first version: First step: optional 'requires/produces' notes per step and an fm task step lint that flags steps whose postcondition already holds (cheap git/file check). Full living graph and timeline UI are wild; skip.
>   what it is: Treats the plan as a living graph with conditions, named passes and live prediction of file changes.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 12 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Do T-0645, T-0666 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0692. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0645: Plan from history (I019, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_planhistory.py -k History`
- [x] T-0666: Plan as a graph or compiled object (I014, value 3/5, effort L, risk med) works — verify with `python3 plugin/tests/run.py -p test_planhistory.py -k Contracts`
## Non-goals
## Approach (options → choice → why)
Options: (a) a plan-diff store written at every step change; (b) derive at close from the ledger — step_add events after the first focus are steps the plan forgot, steps whose evidence failed are steps that failed — and keep them in the brief as 'Plan gaps', which recall already indexes; (c) a model that compares plans. Choice: (b): no new store, recall surfaces 'steps similar plans added late' at focus from the hits it already found. Contracts: an optional '(produces: PATH, …)' / '(requires: PATH, …)' note in a step's text; fm focus lints undone steps whose produced paths already exist and required paths that neither exist nor come from an earlier step. Hints only. Later: falsifiable plan predictions, the living graph.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0645: Plan from history (I019, value 3/5, effort M, risk low)
2. [x] T-0666: Plan as a graph or compiled object (I014, value 3/5, effort L, risk med)
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md (Unreleased: planning 2), ~/.claude/foreman/plugin/skills/intake/references/planning.md (contracts and plan gaps)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_planhistory.py` → ✗ exit 1 · Ran 2 tests in 0.4s (2 classes, 16 at a time; slowest: History 0s, Contracts 0s) / FAILED (2 classes) [ran] [tree d2d431a1212b] (2026-10-09T20:43:55Z)
- (step 1) `python3 plugin/tests/run.py -p test_planhistory.py -k History` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: History 1s) / OK [ran] [tree 26e1e4d07868] (2026-10-09T20:44:32Z)
- (step 2) `python3 plugin/tests/run.py -p test_planhistory.py -k Contracts` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Contracts 0s) / OK [ran] [tree 26e1e4d07868] (2026-10-09T20:44:32Z)
- (ac 1) `python3 plugin/tests/run.py -p test_planhistory.py -k History` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: History 1s) / OK [ran] [tree 26e1e4d07868] (2026-10-09T20:46:03Z)
- (ac 2) `python3 plugin/tests/run.py -p test_planhistory.py -k Contracts` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Contracts 0s) / OK [ran] [tree 26e1e4d07868] (2026-10-09T20:46:03Z)
- `python3 plugin/tests/run.py` → exit 0 · Ran 1213 tests in 83.8s (386 classes, 16 at a time; slowest: Stop 41s, TaskLifecycle 27s, Bench 24s) / OK [ran] [tree 26e1e4d07868] (2026-10-09T20:46:03Z)
- (audit intent) `main-thread review of the diff against both first versions; recall render checked on the real project` → both first versions shipped (plan gaps from the ledger surfaced by recall; produces/requires lint at focus); falsifiable plan predictions and the living graph stay out, as the brief says [tree 26e1e4d07868] (2026-10-09T20:46:03Z)
- (audit edge) `main-thread review of the diff against both first versions; recall render checked on the real project` → steps added before the first focus are planning, not gaps; only the first run per step decides 'failed first'; a product is checked only on undone steps so a resumed task doesn't flag its own finished work; a requirement made by an earlier step isn't flagged (tested) [tree 26e1e4d07868] (2026-10-09T20:46:03Z)
## Log
- 2026-10-09T15:40:18Z created
- 2026-10-09T20:43:43Z criterion 1 verify: `` → `python3 plugin/tests/run.py -p test_planhistory.py -k History`
- 2026-10-09T20:43:43Z criterion 2 verify: `` → `python3 plugin/tests/run.py -p test_planhistory.py -k Contracts`
- 2026-10-09T20:43:43Z focused
- 2026-10-09T20:46:03Z done
- 2026-10-09T20:46:04Z committed 4186db6 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- T-0674 [FEATURE M, done, 3 steps] Milestone: Features — Observability, replay and trust — lesson: Check where secrets enter before adding redaction: every write path her…
- T-0672 [SECURITY L, done, 6 steps] Milestone: Features — Guard and safety — lesson: a safety claim shown to the user (restorable) must state its limits; a reviewer will …
- decision 2026-10-09: Self-approve T-0691 (planning milestone, L) after the second-plan review: all six objections answered in the brief (independent replan triggers, def…
## Lessons
- The ledger already orders plan events against the first focus; 'what the plan forgot' is just the step_add events after it
## Plan gaps
- failed first: step 1 T-0645: Plan from history (I019, value 3/5, effort M, risk low)
## Files touched
- plugin/tests/test_planhistory.py
- plugin/lib/fmcli.py
- plugin/lib/fmrecall.py
- CHANGELOG.md
- plugin/skills/intake/references/planning.md
