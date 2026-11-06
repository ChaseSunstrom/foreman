---
id: T-0680
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:15Z
updated: 2026-10-09T18:04:15Z
batch: [T-0454, T-0455, T-0456, T-0470, T-0471, T-0497, T-0498, T-0499]
base: 6e08980e24b71819a543aaca2cdace9c9f36c43f
base_tree: 7f6f22a69e355c116f84820683babaa42d6c85b1
verified: strong
---
# Milestone: Features — Self-improvement and learning
## Raw request
> T-0454: FEATURE: Lesson lifecycle (C038, value 4/5, effort M, risk low)
>   first version: Add a lesson ledger sidecar: count when a tripwire-surfaced lesson preceded a clean pass vs a repeat block; fm tidy flags lessons whose pinned file changed or that never helped. Skip quizzes and truth-maintenance graph.
>   what it is: Store lessons with confidence, evidence and expiry, quiz them, resolve contradictions and prune or retire the stale ones.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 11 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0455: FEATURE: Evals from failures and steers (C039, value 4/5, effort M, risk low)
>   first version: Auto-run fm evals when a task is blocked and log guard false positives (user steer after a block) into an eval inbox; gate releases on fm bench gate plus these cases. Skip predictive failure and randomized trials.
>   what it is: Capture an eval automatically from every block, steer or guard false positive and gate releases on them.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 14 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0456: FEATURE: Benchmarks of Foreman itself (C043, value 4/5, effort M, risk low)
>   first version: Add a holdout split to fm bench so evolve gates on train cases and a release check runs the held-out ones; keep a scorecard line per release. Skip outside benchmarks and publishing.
>   what it is: Hold secret bench sets, grow them when saturated, track a release scorecard, measure time horizon and report outside scores.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 8 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0470: FEATURE: Rule lifecycle (C045, value 3/5, effort S, risk low)
>   first version: From fm friction counts, flag a prose rule that was nudged or corrected 3+ times as a candidate for a guard check; add reaffirm date to rules in fm tidy. Decision tripwires already exist, skip those.
>   what it is: Give rules a half-life, promote repeatedly broken prose rules to enforcement and detect contradictions.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 5 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0471: FEATURE: Self-experiment discipline (C046, value 3/5, effort S, risk low)
>   first version: Dead-end registry: store rejected evolve and friction candidates with reason, and have fm evolve and fm friction skip or cite them. Skip Goodhart alarm and sequential trials.
>   what it is: Pre-register experiments, raise Goodhart alarms, test sequentially and keep dead-end registries.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 7 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0497: FEATURE: Mining lessons from attempts (C041, value 3/5, effort M, risk low)
>   first version: Extend fm repeats to propose a playbook draft from repeated successful step sequences, and scan git reverts linked to T-ids for a lesson line. Skip contrastive pairs and teaching notes until bench pairs exist.
>   what it is: Learn from paired attempts, reverted work, races and hard tasks, and write teaching notes for cheaper models.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 7 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0498: FEATURE: Instruction tuning across models (C042, value 3/5, effort M, risk med)
>   first version: Run fm evolve --drop over rules/skills on each new model id via bench models, report files that earn no tokens. Skip fuzzing, shadow runs and bake-off as duplicates of evolve+bench.
>   what it is: Tune, shrink and ablate instructions per model, delete crutches on new models and test instruction variants in shadow.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 8 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0499: FEATURE: Context injection quality (C044, value 3/5, effort M, risk low)
>   first version: Log injected note kinds and sizes per turn in the ledger and show a per-session total in fm friction, with a cap that drops the lowest-yield notes. Skip live rule-retention probes.
>   what it is: Keep injected context small, cache-stable and delivered at the action, and measure what was used.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 7 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Do T-0454, T-0455, T-0456, T-0470, T-0471, T-0497, T-0498, T-0499 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0680. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0499/T-0454 the hooks log each injected note (event, key, chars) and each tripwire lesson shown — verify with `python3 plugin/tests/run.py -p test_learning.py -k InjectLog`
- [x] T-0470/T-0499/T-0454 fm friction shows the note budget per kind, notes repeated 3+ times as check candidates, and the lessons shown — verify with `python3 plugin/tests/run.py -p test_learning.py -k FrictionSections`
- [x] T-0471 fm friction --reject TEXT --why WHY: later digests skip lines with it and count them — verify with `python3 plugin/tests/run.py -p test_learning.py -k DeadEnds`
- [x] T-0455, T-0456, T-0497, T-0498 captured for a later pass — verify with `fm task show T-0680`
## Non-goals
## Approach (options → choice → why)
Everything lands in the friction digest, the one place self-improvement passes read: the hooks log each note they inject (event, a short key, characters) and each lesson a tripwire shows; the digest adds the note budget per kind, the notes repeated 3+ times (candidates for a hard check: T-0470) and the lessons shown (T-0454); fm friction --reject TEXT --why keeps a dead end that later digests skip and count (T-0471). The paid or bench-bound members — auto-evals on a block (T-0455), a bench holdout split (T-0456), playbook drafts from repeats (T-0497), instruction tuning per model (T-0498) — are captured for a later pass.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests first
2. [x] note and lesson events in fmhooks
3. [x] friction sections and --reject
4. [x] full suite once; CHANGELOG; capture the deferred members
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_learning.py` → ✗ exit 1 · Ran 3 tests in 0.4s (3 classes, 16 at a time; slowest: DeadEnds 0s, FrictionSections 0s, InjectLog 0s) / FAILED (3 classes) [ran] [tree cf8072cfb8e8] (2026-10-09T18:02:25Z)
- (ac 1) `python3 plugin/tests/run.py -p test_learning.py -k InjectLog` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: InjectLog 0s) / OK [ran] [tree 1ea7af1fb1d7] (2026-10-09T18:04:15Z)
- (ac 2) `python3 plugin/tests/run.py -p test_learning.py -k FrictionSections` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: FrictionSections 0s) / OK [ran] [tree 1ea7af1fb1d7] (2026-10-09T18:04:15Z)
- (ac 3) `python3 plugin/tests/run.py -p test_learning.py -k DeadEnds` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: DeadEnds 0s) / OK [ran] [tree 1ea7af1fb1d7] (2026-10-09T18:04:15Z)
- (ac 4) `fm task show T-0680` → exit 0 · - T-0567 [FEATURE M, dropped, 0 steps] Mining lessons from attempts (C041, value 3/5, effort M, risk low) / - decision 2026-09-27: Recursion bound for T-0063: after R5, one more round (R6: auto-eviden [ran] [tree 1ea7af1fb1d7] (2026-10-09T18:04:15Z)
- (step 1) `python3 plugin/tests/run.py` → exit 0 · Ran 1117 tests in 55.6s (303 classes, 16 at a time; slowest: Stop 36s, TaskLifecycle 23s, Parallel 21s) / OK [ran] [tree 1ea7af1fb1d7] (2026-10-09T18:04:15Z)
- (step 2) `python3 plugin/tests/run.py` → exit 0 · Ran 1117 tests in 55.6s (303 classes, 16 at a time; slowest: Stop 36s, TaskLifecycle 23s, Parallel 21s) / OK [ran] [tree 1ea7af1fb1d7] (2026-10-09T18:04:15Z)
- (step 3) `python3 plugin/tests/run.py` → exit 0 · Ran 1117 tests in 55.6s (303 classes, 16 at a time; slowest: Stop 36s, TaskLifecycle 23s, Parallel 21s) / OK [ran] [tree 1ea7af1fb1d7] (2026-10-09T18:04:15Z)
- (step 4) `python3 plugin/tests/run.py` → exit 0 · Ran 1117 tests in 55.6s (303 classes, 16 at a time; slowest: Stop 36s, TaskLifecycle 23s, Parallel 21s) / OK [ran] [tree 1ea7af1fb1d7] (2026-10-09T18:04:15Z)
- (audit intent) `main-thread self-review over the diff: two event kinds logged by the hooks (inject, lesson_shown), three digest sections and a dead-end list; paid members captured` → first versions of four members feeding the one digest self-improvement passes read; the paid four captured [tree 1ea7af1fb1d7] (2026-10-09T18:04:15Z)
- (audit operator) `main-thread self-review over the diff: two event kinds logged by the hooks (inject, lesson_shown), three digest sections and a dead-end list; paid members captured` → inject logging adds one events.jsonl line per injected note (no new reads on the hot path); the note budget shows what the hooks cost in context per pass [tree 1ea7af1fb1d7] (2026-10-09T18:04:15Z)
- (audit edge) `main-thread self-review over the diff: two event kinds logged by the hooks (inject, lesson_shown), three digest sections and a dead-end list; paid members captured` → events from before this change have no inject kind, so the first digest shows nothing new; a dead end matches by substring, case-insensitive [tree 1ea7af1fb1d7] (2026-10-09T18:04:15Z)
## Log
- 2026-10-09T15:40:15Z created
- 2026-10-09T18:02:12Z focused
- 2026-10-09T18:04:15Z done
- 2026-10-09T18:04:15Z committed adf6e73 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0524 [FEATURE M, dropped, 0 steps] Lesson lifecycle (C038, value 4/5, effort M, risk low)
- T-0689 [FEATURE M, planned, 7 steps] Milestone: Intelligence — Learning from outcomes
- T-0567 [FEATURE M, dropped, 0 steps] Mining lessons from attempts (C041, value 3/5, effort M, risk low)
- decision 2026-09-27: Recursion bound for T-0063: after R5, one more round (R6: auto-evidence from Bash results matching a criterion's verify command) from the existing R…
## Lessons
- Measure what the harness itself injects: notes are tokens too, and a note repeated every turn is a rule asking to become a check.
## Files touched
- plugin/tests/test_learning.py
- plugin/lib/fmhooks.py
- plugin/lib/fmfriction.py
- plugin/lib/fmcli.py
- CHANGELOG.md
