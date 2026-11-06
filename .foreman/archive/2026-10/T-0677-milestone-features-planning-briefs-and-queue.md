---
id: T-0677
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:14Z
updated: 2026-10-09T17:51:18Z
batch: [T-0450, T-0451, T-0452, T-0488, T-0489, T-0490, T-0491]
base: 1225d0a0f9ea34662c61d1c87311706931438b12
base_tree: 2157e336a63cec509d2b237f57fcb9c5ee6f98b4
verified: strong
---
# Milestone: Features — Planning, briefs and queue
## Raw request
> T-0450: FEATURE: Queue grooming and lifecycle (C048, value 4/5, effort M, risk low)
>   first version: First version: deferrals carry a revisit date/condition and fm next/tidy resurface expired ones; add fm task revert ID that lists dependents (fm relate) before undoing. Skip objectives layer and lifecycle table.
>   what it is: Groom the queue, expire deferrals, stack and park tasks and unify inbox, queue and tasks into one lifecycle.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 13 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0451: FEATURE: Estimates, pace and time budgets (C051, value 4/5, effort M, risk low)
>   first version: First version: fm next / plan shows predicted cost and minutes from finished tasks of the same type and tier (fm cost data), and fm run orders the queue to fit the remaining budget. Skip demo-date backwards planning.
>   what it is: Predict cost and duration of tasks, plan the day against pace and work backwards from dates.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 6 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0452: FEATURE: Triggers and standing orders (C055, value 4/5, effort M, risk med)
>   first version: First version: a standing-orders file (cron-like or file/CI/git-change condition -> captured brief or fm command) evaluated by fm night and drive; spend capped by fm budget. Skip event-push infrastructure.
>   what it is: Run standing orders on schedules or external conditions and wake sessions on events.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 5 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0488: FEATURE: Scope and intent drift (C050, value 3/5, effort M, risk low)
>   first version: Derive tier from the diff at done (files, lines, core paths) and flag a mismatch with the declared tier; reuse the existing scope check. Skip the effort ledger.
>   what it is: Detect drift between brief, diff and vetoes, derive tier from the diff and keep sessions on intent.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 4 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0489: FEATURE: Decisions, assumptions and promises (C052, value 3/5, effort M, risk low)
>   first version: First version: fm task assume gets a re-check command; sentinel/night reruns them and reopens or inboxes the task when one fails. Skip regret review, spaced repetition, release/rollback briefs, sunset contracts.
>   what it is: Keep tripwires, revisit triggers, assumption registers and promise ledgers that reopen work when they stop holding.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 6 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0490: FEATURE: Plan-time rigour (C053, value 3/5, effort M, risk low)
>   first version: First version: for FEATURE L plans require a short build-vs-reuse line (existing fm command or module found by recall) and one pre-mortem line from fm second plan; add SPIKE as a discarded-lane task. Skip council, rubber-duck, demo transcripts.
>   what it is: Require build-vs-reuse records, pre-mortems, spike tasks, demo transcripts and previews before building.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 13 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0491: FEATURE: Living handbook and docs (C054, value 3/5, effort M, risk low)
>   first version: First version: fm docs also checks MASTER.md module/command table against lib/*.py and fm help and offers the diff. Cold-start test already exists as bench stranger; skip editor why-lines (fm why exists).
>   what it is: Keep a self-writing handbook, MASTER.md and docs that track reality and pass a cold-start test.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 4 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Do T-0450, T-0451, T-0452, T-0488, T-0489, T-0490, T-0491 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0677. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0450 a deferral can carry --until DATE and fm next names it once that date passes — verify with `python3 plugin/tests/run.py -p test_planning.py -k DeferRevisit`
- [x] T-0451 fm next says how long this type/tier usually takes here — verify with `python3 plugin/tests/run.py -p test_planning.py -k UsualMinutes`
- [x] T-0452 fm orders add --every PERIOD|--on-change PATH TEXT, list, rm, run: due orders become captured tasks, once per period or change; fm night runs them — verify with `python3 plugin/tests/run.py -p test_planning.py -k StandingOrders`
- [x] T-0488 fm task done warns when the diff is a size bigger than the planned tier — verify with `python3 plugin/tests/run.py -p test_planning.py -k TierDrift`
- [x] T-0489 fm task assume add --check CMD; fm sentinel re-runs the checks of finished tasks and captures a task for one that broke — verify with `python3 plugin/tests/run.py -p test_planning.py -k AssumptionCheck`
- [x] T-0490 a FEATURE L is approved only with a Build vs reuse section — verify with `python3 plugin/tests/run.py -p test_planning.py -k PlanRigour`
- [x] T-0491 fm doctor's self-docs check names lib modules MASTER.md doesn't — verify with `python3 plugin/tests/run.py -p test_planning.py -k SelfDocsModules`
## Non-goals
## Approach (options → choice → why)
Smallest first version per member, reusing what exists: fmwatch.typical for minutes, the sentinel for re-checks, _close_warnings for drift, check_self_docs for modules, the approved= gate for L plans; a new fmorders module (one JSON file in the project dir) for standing orders. Deferred: fm task revert with dependents, budget-fit ordering, SPIKE type (captured).
## Risks and rollback
## Execution prompt
## Steps
1. [x] all seven failing classes first
2. [x] defer --until and fm next (fmcli, fmcore._next_for)
3. [x] usual minutes in fm next
4. [x] fm orders (new fmorders module), fm night runs it
5. [x] tier drift warning at done (_close_warnings)
6. [x] assume --check and the sentinel
7. [x] build-vs-reuse gate on approval; doctor missing modules; MASTER names fmcost/fmdocs/fmreplay/fmorders
8. [x] full suite once; CHANGELOG
## Resume here
## Docs impact
CHANGELOG entry; MASTER.md module table and CLI line; intake skill (Build vs reuse before approving a FEATURE L)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_planning.py` → ✗ exit 1 · Ran 0 tests in 0.0s (0 classes, 16 at a time; slowest: ) / NO TESTS RAN [ran] [tree 2157e336a63c] (2026-10-09T17:44:34Z)
- (step 1) `python3 plugin/tests/run.py -p test_planning.py` → ✗ exit 1 · Ran 7 tests in 0.9s (7 classes, 16 at a time; slowest: AssumptionCheck 1s, TierDrift 1s, UsualMinutes 1s) / FAILED (7 classes) [ran] [tree 50b98ec076d8] (2026-10-09T17:44:52Z)
- (step 7) `python3 plugin/tests/run.py -p test_planning.py -k DeferRevisit` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: DeferRevisit 0s) / OK [ran] [tree 5aece4339dd9] (2026-10-09T17:47:34Z)
- (step 7) `python3 plugin/tests/run.py -p test_planning.py -k UsualMinutes` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: UsualMinutes 1s) / OK [ran] [tree 5aece4339dd9] (2026-10-09T17:47:35Z)
- (step 7) `python3 plugin/tests/run.py -p test_planning.py -k StandingOrders` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: StandingOrders 0s) / OK [ran] [tree 5aece4339dd9] (2026-10-09T17:47:35Z)
- (step 7) `python3 plugin/tests/run.py -p test_planning.py -k TierDrift` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: TierDrift 0s) / OK [ran] [tree 5aece4339dd9] (2026-10-09T17:47:36Z)
- (step 7) `python3 plugin/tests/run.py -p test_planning.py -k AssumptionCheck` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: AssumptionCheck 1s) / OK [ran] [tree 5aece4339dd9] (2026-10-09T17:47:37Z)
- (step 7) `python3 plugin/tests/run.py -p test_planning.py -k PlanRigour` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: PlanRigour 0s) / OK [ran] [tree 5aece4339dd9] (2026-10-09T17:47:37Z)
- (step 7) `python3 plugin/tests/run.py -p test_planning.py -k SelfDocsModules` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: SelfDocsModules 0s) / OK [ran] [tree 5aece4339dd9] (2026-10-09T17:47:38Z)
- (ac 1) `python3 plugin/tests/run.py -p test_planning.py -k DeferRevisit` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: DeferRevisit 0s) / OK [ran] [tree 5aece4339dd9] (2026-10-09T17:48:44Z)
- (ac 2) `python3 plugin/tests/run.py -p test_planning.py -k UsualMinutes` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: UsualMinutes 1s) / OK [ran] [tree 5aece4339dd9] (2026-10-09T17:48:44Z)
- (ac 3) `python3 plugin/tests/run.py -p test_planning.py -k StandingOrders` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: StandingOrders 0s) / OK [ran] [tree 5aece4339dd9] (2026-10-09T17:48:44Z)
- (ac 4) `python3 plugin/tests/run.py -p test_planning.py -k TierDrift` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: TierDrift 0s) / OK [ran] [tree 5aece4339dd9] (2026-10-09T17:48:44Z)
- (ac 5) `python3 plugin/tests/run.py -p test_planning.py -k AssumptionCheck` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: AssumptionCheck 1s) / OK [ran] [tree 5aece4339dd9] (2026-10-09T17:48:44Z)
- (ac 6) `python3 plugin/tests/run.py -p test_planning.py -k PlanRigour` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: PlanRigour 0s) / OK [ran] [tree 5aece4339dd9] (2026-10-09T17:48:44Z)
- (ac 7) `python3 plugin/tests/run.py -p test_planning.py -k SelfDocsModules` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: SelfDocsModules 0s) / OK [ran] [tree 5aece4339dd9] (2026-10-09T17:48:44Z)
- (step 1) `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 1094 tests in 55.0s (293 classes, 16 at a time; slowest: Stop 41s, TaskLifecycle 27s, Bench 25s) / FAILED (4 classes) [ran] [tree 5aece4339dd9] (2026-10-09T17:48:44Z)
- (step 2) `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 1094 tests in 55.0s (293 classes, 16 at a time; slowest: Stop 41s, TaskLifecycle 27s, Bench 25s) / FAILED (4 classes) [ran] [tree 5aece4339dd9] (2026-10-09T17:48:44Z)
- (step 3) `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 1094 tests in 55.0s (293 classes, 16 at a time; slowest: Stop 41s, TaskLifecycle 27s, Bench 25s) / FAILED (4 classes) [ran] [tree 5aece4339dd9] (2026-10-09T17:48:44Z)
- (step 4) `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 1094 tests in 55.0s (293 classes, 16 at a time; slowest: Stop 41s, TaskLifecycle 27s, Bench 25s) / FAILED (4 classes) [ran] [tree 5aece4339dd9] (2026-10-09T17:48:44Z)
- (step 5) `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 1094 tests in 55.0s (293 classes, 16 at a time; slowest: Stop 41s, TaskLifecycle 27s, Bench 25s) / FAILED (4 classes) [ran] [tree 5aece4339dd9] (2026-10-09T17:48:44Z)
- (step 6) `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 1094 tests in 55.0s (293 classes, 16 at a time; slowest: Stop 41s, TaskLifecycle 27s, Bench 25s) / FAILED (4 classes) [ran] [tree 5aece4339dd9] (2026-10-09T17:48:44Z)
- (step 8) `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 1094 tests in 55.0s (293 classes, 16 at a time; slowest: Stop 41s, TaskLifecycle 27s, Bench 25s) / FAILED (4 classes) [ran] [tree 5aece4339dd9] (2026-10-09T17:48:44Z)
- (step 1) `python3 plugin/tests/run.py` → exit 0 · Ran 1105 tests in 53.2s (293 classes, 16 at a time; slowest: Stop 42s, TaskLifecycle 27s, Bench 25s) / OK [ran] [tree 3fe6b8e69d47] (2026-10-09T17:51:17Z)
- (step 2) `python3 plugin/tests/run.py` → exit 0 · Ran 1105 tests in 53.2s (293 classes, 16 at a time; slowest: Stop 42s, TaskLifecycle 27s, Bench 25s) / OK [ran] [tree 3fe6b8e69d47] (2026-10-09T17:51:17Z)
- (step 3) `python3 plugin/tests/run.py` → exit 0 · Ran 1105 tests in 53.2s (293 classes, 16 at a time; slowest: Stop 42s, TaskLifecycle 27s, Bench 25s) / OK [ran] [tree 3fe6b8e69d47] (2026-10-09T17:51:17Z)
- (step 4) `python3 plugin/tests/run.py` → exit 0 · Ran 1105 tests in 53.2s (293 classes, 16 at a time; slowest: Stop 42s, TaskLifecycle 27s, Bench 25s) / OK [ran] [tree 3fe6b8e69d47] (2026-10-09T17:51:17Z)
- (step 5) `python3 plugin/tests/run.py` → exit 0 · Ran 1105 tests in 53.2s (293 classes, 16 at a time; slowest: Stop 42s, TaskLifecycle 27s, Bench 25s) / OK [ran] [tree 3fe6b8e69d47] (2026-10-09T17:51:17Z)
- (step 6) `python3 plugin/tests/run.py` → exit 0 · Ran 1105 tests in 53.2s (293 classes, 16 at a time; slowest: Stop 42s, TaskLifecycle 27s, Bench 25s) / OK [ran] [tree 3fe6b8e69d47] (2026-10-09T17:51:17Z)
- (step 8) `python3 plugin/tests/run.py` → exit 0 · Ran 1105 tests in 53.2s (293 classes, 16 at a time; slowest: Stop 42s, TaskLifecycle 27s, Bench 25s) / OK [ran] [tree 3fe6b8e69d47] (2026-10-09T17:51:17Z)
- (audit intent) `main-thread self-review over the diff (subagents wait on pace): each member's smallest first version, reusing typical(), the sentinel, _close_warnings, check_self_docs and the approved= gate; the full suite caught three older tests approving an L feature and the help tier for fm orders` → seven members' first versions per the brainstorm; revert, budget-fit ordering and SPIKE captured as T-0732 [tree 3fe6b8e69d47] (2026-10-09T17:51:17Z)
- (audit adversary) `main-thread self-review over the diff (subagents wait on pace): each member's smallest first version, reusing typical(), the sentinel, _close_warnings, check_self_docs and the approved= gate; the full suite caught three older tests approving an L feature and the help tier for fm orders` → standing orders only capture tasks (redacted text, no command runs); assumption checks run through the sentinel's side-effect filter like its criteria re-runs; the L approval gate can't be skipped by setting approved with an empty section [tree 3fe6b8e69d47] (2026-10-09T17:51:17Z)
- (audit edge) `main-thread self-review over the diff (subagents wait on pace): each member's smallest first version, reusing typical(), the sentinel, _close_warnings, check_self_docs and the approved= gate; the full suite caught three older tests approving an L feature and the help tier for fm orders` → an unreadable orders.json is no orders; a missing watched file has its own signature so it fires when it appears; tier drift is a warning only and skips repos without git or a task base; the minutes note is fm next only (the hooks don't pay for a 5000-line ledger read) [tree 3fe6b8e69d47] (2026-10-09T17:51:17Z)
- (audit maintainer) `main-thread self-review over the diff (subagents wait on pace): each member's smallest first version, reusing typical(), the sentinel, _close_warnings, check_self_docs and the approved= gate; the full suite caught three older tests approving an L feature and the help tier for fm orders` → one new module (fmorders) and MASTER.md now names every lib module, enforced by fm doctor [tree 3fe6b8e69d47] (2026-10-09T17:51:17Z)
## Log
- 2026-10-09T15:40:14Z created
- 2026-10-09T17:44:34Z focused
- 2026-10-09T17:51:17Z done
- 2026-10-09T17:51:18Z committed 10eb787 (10 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0520 [FEATURE M, dropped, 0 steps] Queue grooming and lifecycle (C048, value 4/5, effort M, risk low)
- T-0559 [FEATURE M, dropped, 0 steps] Decisions, assumptions and promises (C052, value 3/5, effort M, risk low)
- T-0560 [FEATURE M, dropped, 0 steps] Plan-time rigour (C053, value 3/5, effort M, risk low)
- decision 2026-10-09: [costly] Build all 70 'build' capabilities from the Foreman brainstorm in value-for-effort rounds (security first); the user's ticks on the punch li…
## Lessons
- Seven small first versions fit one milestone when each reuses an existing mechanism; the new code is the glue, not new machinery.
## Files touched
- plugin/tests/test_planning.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmorders.py
- plugin/lib/fmnight.py
- plugin/lib/fmdoctor.py
- MASTER.md
- CHANGELOG.md
- plugin/tests/test_cli.py
- plugin/skills/intake/SKILL.md
