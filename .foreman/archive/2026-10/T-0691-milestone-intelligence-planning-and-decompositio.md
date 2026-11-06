---
id: T-0691
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:17Z
updated: 2026-10-09T20:41:05Z
batch: [T-0603, T-0604, T-0623, T-0624, T-0625, T-0626, T-0643, T-0644]
base: e6c839daf7df1d5fb30f41d1f7554ee3cafe9418
base_tree: 221d162b1bfcb025d390ef379db3e2128cf916cc
verified: strong
---
# Milestone: Intelligence — Planning and decomposition (1)
## Raw request
> T-0603: FEATURE: Replan on surprise (I011, value 4/5, effort M, risk low)
>   first version: When fm surprise or a failed assumption verify is logged on an active M/L task, fm next injects 'replan: re-read Steps/Execution prompt' once and logs a plan revision line in the brief.
>   what it is: Re-plans in rolling waves, at checkpoints and on steers, keeping a revision history.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 8 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0604: FEATURE: Stress-test the plan before running (I013, value 4/5, effort M, risk low)
>   first version: Extend fm second plan with selectable roles (pre-mortem, naive reader, plan court prosecutor/defender) as extra prompt variants for L plans; reuse the child_cmd and budget path. Skip personas with memory and throwaway-copy rehearsal.
>   what it is: Attacks the plan with pre-mortems, naive readers, tabletop runs, courts and fuzzing before any edit.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 20 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0623: FEATURE: Order steps by risk and information (I010, value 3/5, effort S, risk low)
>   first version: Add a rubric line to planning.md R2 and a brief Steps lint: spikes/unknowns/human-dependent steps first, reversible before irreversible. Pure instruction text, no code.
>   what it is: Puts the riskiest or most informative steps first and schedules slow or human-dependent ones early.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 8 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0624: FEATURE: Decomposition recipes and seams (I012, value 3/5, effort S, risk low)
>   first version: Add a decomposition-recipes reference (expand/migrate/contract, test ladder, walking skeleton, one observable per step) linked from planning.md; later lint step granularity. Skip the co-change seam cutter, already T-0445.
>   what it is: Splits work by named recipes, oracles, tests, cost of seams and commit-sized steps.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 15 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0625: FEATURE: Spike and skeleton first (I020, value 3/5, effort S, risk low)
>   first version: Add a walking-skeleton rule for FEATURE L (first step: thinnest end-to-end path with a failing acceptance test) and a throwaway-spike step type to planning.md. Skip empty-commit skeletons and simulators.
>   what it is: Builds a walking skeleton, throwaway spike or empty-commit skeleton before the real plan.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 6 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0626: FEATURE: Planned obligations and safe ends (I021, value 3/5, effort S, risk low)
>   first version: Planning rubric adds: every FIX has contain/cure/inoculate steps, every migration has a cleanup/rollback step; fm next warns at finish if rollback section empty on L.
>   what it is: Makes cleanup, rollback and breaking-change phases explicit plan items, and plans by the ending.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 3 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0643: FEATURE: Bind plans to assumptions (I015, value 3/5, effort M, risk low)
>   first version: Let steps cite assumption numbers; when an assumption goes [false], fm next names the steps that cite it for re-check. Known-unknowns ledger is the same list.
>   what it is: Ties steps to assumptions and beliefs so only dependent steps are invalidated when one breaks.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 6 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0644: FEATURE: Size and estimate plans (I016, value 3/5, effort M, risk low)
>   first version: Trip a re-frame note in fm next when on-task time passes 2x the typical median, and record planned scope vs real changed files at finish for a correction factor. Skip Monte Carlo and working-memory span.
>   what it is: Estimates steps, effort and footprint from measured history and Monte Carlo.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 11 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Do T-0603, T-0604, T-0623, T-0624, T-0625, T-0626, T-0643, T-0644 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0691. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0603: Replan on surprise (I011, value 4/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_replan.py -k Replan`
- [x] T-0604: Stress-test the plan before running (I013, value 4/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_replan.py -k Roles`
- [x] T-0623: Order steps by risk and information (I010, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_replan.py -k Order`
- [x] T-0624: Decomposition recipes and seams (I012, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_replan.py -k Recipes`
- [x] T-0625: Spike and skeleton first (I020, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_replan.py -k Skeleton`
- [x] T-0626: Planned obligations and safe ends (I021, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_replan.py -k Obligations`
- [x] T-0643: Bind plans to assumptions (I015, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_replan.py -k Bind`
- [x] T-0644: Size and estimate plans (I016, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_replan.py -k Estimate`
## Non-goals
## Approach (options → choice → why)
Options: (a) a plan engine that re-plans by itself; (b) hard gates (refuse execution until the plan passes lints); (c) nudges at the moments that matter — fm next names a pending replan, focus prints step-order lints, finish warns on missing obligations — plus rubric text, and a role switch on the existing second-plan child. Choice: (c): every member's first version is a nudge or text, and refusals would fight the model on heuristics (step-word lints are guesses). Replan: fm surprise or a false assumption on an active M/L task sets meta replan (with the steps citing the assumption as A<n>); fm next leads with it until fm task log ID "replan: …" clears it. Roles: fm second plan --role pre-mortem|naive|prosecutor|defender prepends a stance to the PLAN prompt, saved as 'Plan review: <role>'. Order: a focus-time lint flags a step that explores an unknown after one that's hard to undo. Recipes, skeleton, spike, obligations: planning.md and a new decomposition.md reference. Rollback: an L closing with an empty Risks and rollback warns. Estimate: fm next adds a re-frame note past 2x the type/tier median; task_done logs planned scope vs changed files, fm digest shows the ratio.
## Risks and rollback
Risk: a replan nudge that never clears would block fm next's other advice — cleared by fm task log 'replan: …', and only M/L active tasks get one. Risk: word-based step lints misfire — they're printed hints, never refusals. Rollback: revert the commit; the only new state is meta 'replan' on briefs, ignored by older versions.
## Execution prompt
## Steps
1. [x] T-0603: Replan on surprise (I011, value 4/5, effort M, risk low)
2. [x] T-0604: Stress-test the plan before running (I013, value 4/5, effort M, risk low)
3. [x] T-0623: Order steps by risk and information (I010, value 3/5, effort S, risk low)
4. [x] T-0624: Decomposition recipes and seams (I012, value 3/5, effort S, risk low)
5. [x] T-0625: Spike and skeleton first (I020, value 3/5, effort S, risk low)
6. [x] T-0626: Planned obligations and safe ends (I021, value 3/5, effort S, risk low)
7. [x] T-0643: Bind plans to assumptions (I015, value 3/5, effort M, risk low)
8. [x] T-0644: Size and estimate plans (I016, value 3/5, effort M, risk low)
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md (Unreleased: planning 1), ~/.claude/foreman/MASTER.md (fmsecond roles), ~/.claude/foreman/plugin/skills/intake/references/planning.md (Steps rubric), ~/.claude/foreman/plugin/skills/intake/references/decomposition.md (new)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_replan.py` → ✗ exit 1 · Ran 10 tests in 0.7s (8 classes, 16 at a time; slowest: Replan 1s, Order 1s, Bind 0s) / FAILED (8 classes) [ran] [tree 95cc15186381] (2026-10-09T20:34:49Z)
- (step 1) `python3 plugin/tests/run.py -p test_replan.py -k Replan` → exit 0 · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: Replan 1s) / OK [ran] [tree 7ecbcd440708] (2026-10-09T20:36:18Z)
- (step 2) `python3 plugin/tests/run.py -p test_replan.py -k Roles` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Roles 0s) / OK [ran] [tree 7ecbcd440708] (2026-10-09T20:36:18Z)
- (step 3) `python3 plugin/tests/run.py -p test_replan.py -k Order` → exit 0 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: Order 0s) / OK [ran] [tree 7ecbcd440708] (2026-10-09T20:36:19Z)
- (step 4) `python3 plugin/tests/run.py -p test_replan.py -k Recipes` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Recipes 0s) / OK [ran] [tree 7ecbcd440708] (2026-10-09T20:36:19Z)
- (step 5) `python3 plugin/tests/run.py -p test_replan.py -k Skeleton` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Skeleton 0s) / OK [ran] [tree 7ecbcd440708] (2026-10-09T20:36:20Z)
- (step 6) `python3 plugin/tests/run.py -p test_replan.py -k Obligations` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Obligations 0s) / OK [ran] [tree 7ecbcd440708] (2026-10-09T20:36:20Z)
- (step 7) `python3 plugin/tests/run.py -p test_replan.py -k Bind` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Bind 0s) / OK [ran] [tree 7ecbcd440708] (2026-10-09T20:36:21Z)
- (step 8) `python3 plugin/tests/run.py -p test_replan.py -k Estimate` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Estimate 0s) / OK [ran] [tree 7ecbcd440708] (2026-10-09T20:36:21Z)
- (step 1) `python3 plugin/tests/run.py -p test_replan.py -k Replan` → exit 0 · Ran 3 tests in 1.0s (1 classes, 16 at a time; slowest: Replan 1s) / OK [ran] [tree 15ab2e9b14a2] (2026-10-09T20:37:26Z)
- (step 3) `python3 plugin/tests/run.py -p test_replan.py -k Order` → exit 0 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: Order 0s) / OK [ran] [tree 15ab2e9b14a2] (2026-10-09T20:37:27Z)
- (step 8) `python3 plugin/tests/run.py -p test_replan.py -k Estimate` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Estimate 0s) / OK [ran] [tree 15ab2e9b14a2] (2026-10-09T20:37:27Z)
- (ac 1) `python3 plugin/tests/run.py -p test_replan.py -k Replan` → exit 0 · Ran 3 tests in 1.0s (1 classes, 16 at a time; slowest: Replan 1s) / OK [ran] [tree 7c6b10246d89] (2026-10-09T20:38:42Z)
- (ac 2) `python3 plugin/tests/run.py -p test_replan.py -k Roles` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Roles 0s) / OK [ran] [tree 7c6b10246d89] (2026-10-09T20:38:42Z)
- (ac 3) `python3 plugin/tests/run.py -p test_replan.py -k Order` → exit 0 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: Order 0s) / OK [ran] [tree 7c6b10246d89] (2026-10-09T20:38:42Z)
- (ac 4) `python3 plugin/tests/run.py -p test_replan.py -k Recipes` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Recipes 0s) / OK [ran] [tree 7c6b10246d89] (2026-10-09T20:38:42Z)
- (ac 5) `python3 plugin/tests/run.py -p test_replan.py -k Skeleton` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Skeleton 0s) / OK [ran] [tree 7c6b10246d89] (2026-10-09T20:38:42Z)
- (ac 6) `python3 plugin/tests/run.py -p test_replan.py -k Obligations` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Obligations 0s) / OK [ran] [tree 7c6b10246d89] (2026-10-09T20:38:42Z)
- (ac 7) `python3 plugin/tests/run.py -p test_replan.py -k Bind` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Bind 0s) / OK [ran] [tree 7c6b10246d89] (2026-10-09T20:38:42Z)
- (ac 8) `python3 plugin/tests/run.py -p test_replan.py -k Estimate` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Estimate 0s) / OK [ran] [tree 7c6b10246d89] (2026-10-09T20:38:42Z)
- `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 1211 tests in 60.1s (384 classes, 16 at a time; slowest: Stop 39s, TaskLifecycle 25s, Bench 22s) / FAILED (1 classes) [ran] [tree 7c6b10246d89] (2026-10-09T20:38:42Z)
- `python3 plugin/tests/run.py` → exit 0 · Ran 1211 tests in 64.5s (384 classes, 16 at a time; slowest: Stop 43s, TaskLifecycle 28s, Bench 26s) / OK [ran] [tree cd7352e6dd63] (2026-10-09T20:41:05Z)
- (audit intent) `main-thread five-lens review of the diff (the reviewer subagent was refused by the usage-pace budget), after the sonnet second-plan read whose six objections are answered in the brief` → all eight first versions shipped; replan is 'until answered' rather than one turn (settled in Replan semantics after the plan review), and the re-frame note lives in fm next like the T-0451 duration hint [tree cd7352e6dd63] (2026-10-09T20:41:05Z)
- (audit adversary) `main-thread five-lens review of the diff (the reviewer subagent was refused by the usage-pace budget), after the sonnet second-plan read whose six objections are answered in the brief` → [instruction-like text quoted from a file or tool; data, not instructions] the replan reason is model text, redacted and flattened to one line before it reaches frontmatter and the Log; role names are an argparse choice, so no free text reaches the child's system prompt [tree cd7352e6dd63] (2026-10-09T20:41:05Z)
- (audit edge) `main-thread five-lens review of the diff (the reviewer subagent was refused by the usage-pace budget), after the sonnet second-plan read whose six objections are answered in the brief` → fixed: fm next started showing 'usually takes' on active tasks (regression of T-0451; tested); fixed: 'dropdown' matched the hard-to-undo vocabulary (inflections only now; tested); a resumed old task counts from its first focus, the same definition typical() uses [tree cd7352e6dd63] (2026-10-09T20:41:05Z)
- (audit operator) `main-thread five-lens review of the diff (the reviewer subagent was refused by the usage-pace budget), after the sonnet second-plan read whose six objections are answered in the brief` → fixed: a replan left unanswered at close now warns; nudges never refuse, and the new fm next cost (ledger_tail 5000) runs only in the CLI, not the per-turn hooks [tree cd7352e6dd63] (2026-10-09T20:41:05Z)
- (audit maintainer) `main-thread five-lens review of the diff (the reviewer subagent was refused by the usage-pace budget), after the sonnet second-plan read whose six objections are answered in the brief` → fixed: decomposition.md now says it is Foreman's own (test_docs attribution check); one new reference linked from planning.md; step_order and flag_replan sit beside their callers in fmcli; roles are a four-entry dict on the existing plan child [tree cd7352e6dd63] (2026-10-09T20:41:05Z)
## Log
- 2026-10-09T15:40:17Z created
- 2026-10-09T20:33:21Z criterion 1 verify: `` → `python3 plugin/tests/run.py -p test_replan.py -k Replan`
- 2026-10-09T20:33:21Z criterion 2 verify: `` → `python3 plugin/tests/run.py -p test_replan.py -k Roles`
- 2026-10-09T20:33:22Z criterion 3 verify: `` → `python3 plugin/tests/run.py -p test_replan.py -k Order`
- 2026-10-09T20:33:22Z criterion 4 verify: `` → `python3 plugin/tests/run.py -p test_replan.py -k Recipes`
- 2026-10-09T20:33:22Z criterion 5 verify: `` → `python3 plugin/tests/run.py -p test_replan.py -k Skeleton`
- 2026-10-09T20:33:22Z criterion 6 verify: `` → `python3 plugin/tests/run.py -p test_replan.py -k Obligations`
- 2026-10-09T20:33:22Z criterion 7 verify: `` → `python3 plugin/tests/run.py -p test_replan.py -k Bind`
- 2026-10-09T20:33:23Z criterion 8 verify: `` → `python3 plugin/tests/run.py -p test_replan.py -k Estimate`
- 2026-10-09T20:34:10Z set approved=True
- 2026-10-09T20:34:13Z focused
- 2026-10-09T20:41:05Z done
- 2026-10-09T20:41:05Z committed 48a7aac (9 files)
## Follow-ups captured
## Build vs reuse
Reuses: fmsecond.plan and its child/budget path (roles are prompt prefixes), fmwatch.typical (durations), the brief Log/meta and fm task log (replan state), _close_warnings (rollback warning), the surprise and assumption commands (triggers). Nothing new to install; no new module.
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: Dependency between T-0603 and T-0643 is inverted. Replan's key behavior ("steps citing the assumption as A<n>") needs step-to-assumption citations, which T-0643 builds in step 7; step 1 either stubs it or can't be tested alone. Per-step `-k` runs would then pass against a stub or fail until s…
- HIGH: All eight tests live in one file (`test_replan.py`) and "write all failing tests first, together" is paired with "per step run only -k". The criteria are then only checked individually, and a shared helper or fixture change by one step can silently break another until the single close-time fu…
- MEDIUM: Several criteria don't prove the request. "works — verify with -k X" says nothing about what the tests assert. T-0623, 0624, 0625 are "pure instruction text", so tests would be string-presence checks on planning.md that pass without changing model behavior; T-0626's "warns at finish if roll…
- MEDIUM: Scope drifts from the raw requests. T-0644 asked for the note against "typical median" and recording planned scope vs real changed files; the plan adds an `fm digest` ratio display not requested. T-0604 asked for "selectable roles ... for L plans" reusing child_cmd and budget path; the plan…
- MEDIUM: Replan state edge cases are unspecified: what if a surprise is logged twice before clearing, on an S task, or after the task is done; does the "once" injection mean once ever or until cleared (the request says once, the approach says "until cleared")? A stuck nudge is the plan's own named r…
- LOW: The word-based order lint ("explores an unknown after one that's hard to undo") has no defined vocabulary, so it's untestable beyond a toy case and may be noisy on every focus. — Define a small fixed keyword list in the plan and test one positive and one negative case; keep it hint-only as sta…
Verdict: revise — the approach (nudges, not gates) is sound, but fix the 0603/0643 ordering, tighten what each test asserts, and settle the replan clearing semantics before writing tests.
## Dissent
- [x] HIGH: Dependency between T-0603 and T-0643 is inverted. Replan's key behavior ("steps citing the assumption as A<n>") needs step-to-assumption citations, which T-0643 builds in step 7; step 1 either stubs it or can't be tested alone. Per-step `-k` runs would then pass against a stub or fail until s… — answered: Replan and Bind have independent triggers (surprise vs false assumption) and tests; see Replan semantics
- [x] HIGH: All eight tests live in one file (`test_replan.py`) and "write all failing tests first, together" is paired with "per step run only -k". The criteria are then only checked individually, and a shared helper or fixture change by one step can silently break another until the single close-time fu… — answered: by design (T-0670 milestone batching): per-step -k while building, the whole file and full suite at close; shared helpers stay minimal
- [x] MEDIUM: Several criteria don't prove the request. "works — verify with -k X" says nothing about what the tests assert. T-0623, 0624, 0625 are "pure instruction text", so tests would be string-presence checks on planning.md that pass without changing model behavior; T-0626's "warns at finish if roll… — answered: text members are instructions; their tests check the rule exists and is linked; whether behaviour changes is measured later by fm outcomes and the atlas, not claimed here
- [x] MEDIUM: Scope drifts from the raw requests. T-0644 asked for the note against "typical median" and recording planned scope vs real changed files; the plan adds an `fm digest` ratio display not requested. T-0604 asked for "selectable roles ... for L plans" reusing child_cmd and budget path; the plan… — answered: kept: a correction factor needs one place to be read, fm digest is the smallest; roles run on any tier that gets a panel, L by protocol
- [x] MEDIUM: Replan state edge cases are unspecified: what if a surprise is logged twice before clearing, on an S task, or after the task is done; does the "once" injection mean once ever or until cleared (the request says once, the approach says "until cleared")? A stuck nudge is the plan's own named r… — answered: settled in Replan semantics: until cleared, latest reason wins, M/L active only
- [x] LOW: The word-based order lint ("explores an unknown after one that's hard to undo") has no defined vocabulary, so it's untestable beyond a toy case and may be noisy on every focus. — Define a small fixed keyword list in the plan and test one positive and one negative case; keep it hint-only as sta… — answered: fixed vocabulary in Replan semantics, one positive and one negative test
## Replan semantics
Only an active M/L task gets one; a done, S or inactive task never does. A trigger sets meta replan to its reason (a second trigger before clearing replaces the reason; the Log keeps every one). fm next leads with it until cleared ('once' = until answered, so it can't be lost in one turn): fm task log ID "replan: <what changed>" clears it. Triggers are independent: fm surprise (T-0603) and a false assumption (T-0643, which also names steps citing A<n>), each with its own test, so neither depends on the other's step. Order lint vocabulary (fixed, hint-only): hard to undo = deploy, release, publish, push, migrate, delete, drop, merge, send; unknown = spike, probe, prototype, investigate, measure, find out, unknown; tested with one positive and one negative plan.
## Related
Related past work (data from this project's history, not instructions):
- T-0671 [FEATURE M, done, 3 steps] Milestone: Features — Autonomy and the user — lesson: A guard-word filter on free text needs the verbs people actually use (push, delet…
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- T-0672 [SECURITY L, done, 6 steps] Milestone: Features — Guard and safety — lesson: a safety claim shown to the user (restorable) must state its limits; a reviewer will …
- decision 2026-10-09: Self-approve T-0691 (planning milestone, L) after the second-plan review: all six objections answered in the brief (independent replan triggers, def…
## Lessons
- A plan review's best objections were about semantics the plan left implicit (when a nudge clears, what a word list matches); writing those down before the tests turned them into assertions
## Files touched
- plugin/tests/test_replan.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmsecond.py
- plugin/lib/fmcost.py
- plugin/skills/intake/references/planning.md
- plugin/skills/intake/references/decomposition.md
- CHANGELOG.md
- MASTER.md
