---
id: T-0695
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:18Z
updated: 2026-10-09T21:01:47Z
batch: [T-0596, T-0610, T-0632, T-0633, T-0649, T-0650]
base: 1bf6d2e074f0f2d944eac0816cea30631f0bd8d2
base_tree: f0785475f6f850ba16638b008f4edb8ec057c0f6
verified: strong
---
# Milestone: Intelligence — Steps and execution craft
## Raw request
> T-0596: FEATURE: Gate steps on observables (I043, value 4/5, effort S, risk low)
>   first version: Add optional 'expect:' text on a step (step text '... :: cmd') recorded at plan time; fm task evidence compares the run output to it and logs a match/miss. First step: reuse the AC '::' parser for steps.
>   what it is: Declares a prediction, observable or done-snippet before each step and checks it after.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 8 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0610: FEATURE: Check the step against the plan (I044, value 4/5, effort M, risk low)
>   first version: fm audit prep adds per-step section: diff files vs step text and scope; a second-read prompt asks whether each hunk serves a step. Build on fm second and audit prep.
>   what it is: Verifies each step by a different method and compares the diff to the step and the brief.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 4 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0632: FEATURE: Step ledgers and handoffs (I046, value 3/5, effort S, risk low)
>   first version: Hook-level repeat detector: a third identical failing evidence cmd on a step logs 'tried' and nudges (T-0440 does this for refusals); add tried list to Resume here.
>   what it is: Records what was tried, why the order, and a handoff stub per step.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 4 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0633: FEATURE: Overlap and script the work (I048, value 3/5, effort S, risk low)
>   first version: fm task start preflight: git clean, deps import, gate baseline cached, scope files exist; reports before step 1. Fold with BASELINE.
>   what it is: Runs verification in the background, scripts repetition and prepares before step one.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 4 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0649: FEATURE: Checkpoint, undo and resume (I045, value 3/5, effort M, risk med)
>   first version: On resume, re-run the last green step's evidence command and report drift; skip per-step commits (git-write risk, lanes cover isolation).
>   what it is: Gives each step a cheap undo and a clean baseline, and reconciles half-done work on resume.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 6 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0650: FEATURE: Keep steps in scope (I047, value 3/5, effort M, risk low)
>   first version: fm check/finish scan the added diff lines for debug scaffolding (print, console.log, TODO-debug, breakpoint) in files the task touched; first step is a regex lint on added lines.
>   what it is: Attributes hunks to steps, flags foreign rewrites, skipped steps and scaffolding, and time-boxes exploration.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 10 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Do T-0596, T-0610, T-0632, T-0633, T-0649, T-0650 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0695. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0596: Gate steps on observables (I043, value 4/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_execution.py -k Expect`
- [x] T-0610: Check the step against the plan (I044, value 4/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_execution.py -k PlanCheck`
- [x] T-0632: Step ledgers and handoffs (I046, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_execution.py -k Tried`
- [x] T-0633: Overlap and script the work (I048, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_execution.py -k Preflight`
- [x] T-0649: Checkpoint, undo and resume (I045, value 3/5, effort M, risk med) works — verify with `python3 plugin/tests/run.py -p test_execution.py -k ResumeCheck`
- [x] T-0650: Keep steps in scope (I047, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_execution.py -k Scaffold`
## Non-goals
## Approach (options → choice → why)
Options: (a) a step runner that executes the plan; (b) checks at the moments steps already pass through — fm task evidence (expectations, repeat detection), fm focus (preflight), fm resume (re-run the last green check), fm audit prep (files vs steps), the close (debug scaffolding in added lines); (c) model judges per step. Choice: (b), all model-free, each extends one existing command. Expect: a step's '(expect: TEXT)' note is compared with the run's output; a miss is logged in the evidence line and warned, not failed. Repeats: a third identical failing command on a step nudges and is logged as tried; resume lists what was tried. Preflight at first focus: scope paths that don't exist, uncommitted files outside the scope, and whether gates ran green on this tree. Resume re-runs the last green step check (2 min cap; --no-check skips). Audit prep adds Files vs steps. Close warns on breakpoint(), pdb, debugger;, console.log in JS/TS, and DEBUG prints in added lines.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0596: Gate steps on observables (I043, value 4/5, effort S, risk low)
2. [x] T-0610: Check the step against the plan (I044, value 4/5, effort M, risk low)
3. [x] T-0632: Step ledgers and handoffs (I046, value 3/5, effort S, risk low)
4. [x] T-0633: Overlap and script the work (I048, value 3/5, effort S, risk low)
5. [x] T-0649: Checkpoint, undo and resume (I045, value 3/5, effort M, risk med)
6. [x] T-0650: Keep steps in scope (I047, value 3/5, effort M, risk low)
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md (Unreleased: execution craft), ~/.claude/foreman/plugin/skills/intake/references/execute.md (preflight, tried, files vs steps, scaffolding), ~/.claude/foreman/plugin/skills/intake/references/planning.md (expect), ~/.claude/foreman/plugin/skills/resume/SKILL.md (drift check), ~/.claude/foreman/plugin/skills/reflect/SKILL.md (--no-check)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_execution.py` → ✗ exit 1 · Ran 6 tests in 0.5s (6 classes, 16 at a time; slowest: Tried 0s, ResumeCheck 0s, PlanCheck 0s) / FAILED (6 classes) [ran] [tree f0e62e0584fb] (2026-10-09T20:58:51Z)
- (step 1) `python3 plugin/tests/run.py -p test_execution.py -k Expect` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Expect 0s) / OK [ran] [tree 4f39b47277da] (2026-10-09T21:00:24Z)
- (step 2) `python3 plugin/tests/run.py -p test_execution.py -k PlanCheck` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: PlanCheck 0s) / OK [ran] [tree 4f39b47277da] (2026-10-09T21:00:25Z)
- (step 3) `python3 plugin/tests/run.py -p test_execution.py -k Tried` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Tried 0s) / OK [ran] [tree 4f39b47277da] (2026-10-09T21:00:25Z)
- (step 4) `python3 plugin/tests/run.py -p test_execution.py -k Preflight` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Preflight 0s) / OK [ran] [tree 4f39b47277da] (2026-10-09T21:00:26Z)
- (step 5) `python3 plugin/tests/run.py -p test_execution.py -k ResumeCheck` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: ResumeCheck 0s) / OK [ran] [tree 4f39b47277da] (2026-10-09T21:00:27Z)
- (step 6) `python3 plugin/tests/run.py -p test_execution.py -k Scaffold` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Scaffold 0s) / OK [ran] [tree 4f39b47277da] (2026-10-09T21:00:27Z)
- (ac 1) `python3 plugin/tests/run.py -p test_execution.py -k Expect` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Expect 0s) / OK [ran] [tree 4f39b47277da] (2026-10-09T21:01:46Z)
- (ac 2) `python3 plugin/tests/run.py -p test_execution.py -k PlanCheck` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: PlanCheck 0s) / OK [ran] [tree 4f39b47277da] (2026-10-09T21:01:46Z)
- (ac 3) `python3 plugin/tests/run.py -p test_execution.py -k Tried` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Tried 0s) / OK [ran] [tree 4f39b47277da] (2026-10-09T21:01:46Z)
- (ac 4) `python3 plugin/tests/run.py -p test_execution.py -k Preflight` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Preflight 0s) / OK [ran] [tree 4f39b47277da] (2026-10-09T21:01:46Z)
- (ac 5) `python3 plugin/tests/run.py -p test_execution.py -k ResumeCheck` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: ResumeCheck 0s) / OK [ran] [tree 4f39b47277da] (2026-10-09T21:01:46Z)
- (ac 6) `python3 plugin/tests/run.py -p test_execution.py -k Scaffold` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Scaffold 0s) / OK [ran] [tree 4f39b47277da] (2026-10-09T21:01:46Z)
- `python3 plugin/tests/run.py` → exit 0 · Ran 1231 tests in 67.9s (402 classes, 16 at a time; slowest: Stop 41s, TaskLifecycle 26s, Bench 23s) / OK [ran] [tree 4f39b47277da] (2026-10-09T21:01:46Z)
- (audit intent) `main-thread review of the diff against the six first versions; checked that only the explicit resume skill runs fm resume (reflect now passes --no-check)` → all six first versions shipped on the commands steps already pass through; per-step commits skipped as the brief says; the second-read part of T-0610 is the reviewer instruction in the brief, not a new child [tree 4f39b47277da] (2026-10-09T21:01:46Z)
- (audit edge) `main-thread review of the diff against the six first versions; checked that only the explicit resume skill runs fm resume (reflect now passes --no-check)` → fixed: the reflect skill read the ledger through fm resume, which now runs a check, so it passes --no-check; an expectation miss warns but never fails a passing run; repeats count only identical commands on the same step; JS console.log is skipped in test paths and plain Python prints aren't flagged (tested) [tree 4f39b47277da] (2026-10-09T21:01:46Z)
- (audit operator) `main-thread review of the diff against the six first versions; checked that only the explicit resume skill runs fm resume (reflect now passes --no-check)` → fm resume's re-run is capped at 2 minutes and skippable; preflight runs only at a task's first focus; the scaffolding scan is one git diff -U0 over the task's own files [tree 4f39b47277da] (2026-10-09T21:01:46Z)
## Log
- 2026-10-09T15:40:18Z created
- 2026-10-09T20:58:33Z criterion 1 verify: `` → `python3 plugin/tests/run.py -p test_execution.py -k Expect`
- 2026-10-09T20:58:33Z criterion 2 verify: `` → `python3 plugin/tests/run.py -p test_execution.py -k PlanCheck`
- 2026-10-09T20:58:33Z criterion 3 verify: `` → `python3 plugin/tests/run.py -p test_execution.py -k Tried`
- 2026-10-09T20:58:33Z criterion 4 verify: `` → `python3 plugin/tests/run.py -p test_execution.py -k Preflight`
- 2026-10-09T20:58:33Z criterion 5 verify: `` → `python3 plugin/tests/run.py -p test_execution.py -k ResumeCheck`
- 2026-10-09T20:58:33Z criterion 6 verify: `` → `python3 plugin/tests/run.py -p test_execution.py -k Scaffold`
- 2026-10-09T20:58:33Z focused
- 2026-10-09T21:01:46Z done
- 2026-10-09T21:01:47Z committed 4b7cea3 (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0672 [SECURITY L, done, 6 steps] Milestone: Features — Guard and safety — lesson: a safety claim shown to the user (restorable) must state its limits; a reviewer will …
- T-0676 [FEATURE M, done, 7 steps] Milestone: Features — Performance and cost — lesson: A 'degrade when over pace' rule must name what is optional: side offers and self-i…
- T-0674 [FEATURE M, done, 3 steps] Milestone: Features — Observability, replay and trust — lesson: Check where secrets enter before adding redaction: every write path her…
- decision 2026-10-09: Self-approve T-0691 (planning milestone, L) after the second-plan review: all six objections answered in the brief (independent replan triggers, def…
## Lessons
- When a read-only command starts doing work (resume now re-runs a check), find every caller that used it to read: a skill reading the ledger through it would have paid for a test run
## Plan gaps
- failed first: step 1 T-0596: Gate steps on observables (I043, value 4/5, effort S, risk low)
## Files touched
- plugin/tests/test_execution.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- plugin/skills/intake/references/execute.md
- plugin/skills/intake/references/planning.md
- plugin/skills/reflect/SKILL.md
- plugin/skills/resume/SKILL.md
