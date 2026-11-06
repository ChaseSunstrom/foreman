---
id: T-0689
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:17Z
updated: 2026-10-09T20:23:55Z
batch: [T-0616, T-0617, T-0640, T-0641, T-0656, T-0657, T-0658]
base: ba9b36dd83ff3a00a97163bc0f10a69440d90500
base_tree: 7d62fb91f07538d72e7e7dd18c71969fb82a9e86
verified: strong
---
# Milestone: Intelligence — Learning from outcomes
## Raw request
> T-0616: FEATURE: Outcome ledger (I076, value 4/5, effort M, risk low)
>   first version: fm outcomes: join each done task with later events (reverts via git, reopened/follow-up tasks naming it, sentinel failures, fm smoke at +24h/+7d via fm night) and record fate; start with revert/follow-up detection from git and #T-ids.
>   what it is: Joins every decision and plan step to its eventual fate, with delayed checks.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 9 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0617: FEATURE: Lesson lifecycle (I077, value 4/5, effort M, risk low)
>   first version: Give lessons stable ids, log when a recalled lesson is shown in fm focus, and flag lessons never recalled or followed by repeat failures (fm recall note_failure sig); then bench-gated retire via fm evolve. Skip tournaments, interference tests, confounder adjustment.
>   what it is: Traces, tests, gates, minimises and retires lessons by measured benefit.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 10 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0640: FEATURE: Agent and pass yield (I080, value 3/5, effort S, risk low)
>   first version: Extend fm usage/digest with per-lens yield (findings confirmed vs false positives from recorded audits) and per-pass: second-read/oracle/brainstorm hits that changed the plan. Data already in ledger.
>   what it is: Tracks which passes, lenses and sub-agent outputs ever mattered.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 3 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0641: FEATURE: Reflection and track record (I081, value 3/5, effort S, risk low)
>   first version: Add a one-line 'would do differently' field to fm task finish (--lesson already exists, extend) and render a short track record (verified-first-time rate by type/tier) in fm digest and injected at fm focus for same type.
>   what it is: Writes what it would do differently and a track record page it reads before claiming confidence.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 3 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0656: FEATURE: Self-regression and eval hygiene (I078, value 3/5, effort M, risk low)
>   first version: First step: fm bench report listing cases that pass/fail identically across all plugin versions (non-discriminating) and propose dropping them; reuse bench result history. Skip island models and bounties.
>   what it is: Attributes Foreman's own regressions, retires weak evals and audits rules.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 7 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0657: FEATURE: Counterfactual and hindsight learning (I079, value 3/5, effort M, risk low)
>   first version: Cheapest step: fm tidy/next reopens blocked tasks when a task they depend on (#T-id) or a file named in the block reason changes (reuse decide --revisit triggers); wrong-turn registry from reverted commits feeds fm recall.
>   what it is: Replays what would have happened and relabels failed attempts.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 5 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0658: FEATURE: Process mining (I082, value 3/5, effort M, risk low)
>   first version: First step: fm friction extension that mines the ledger for stage-transition sequences and flags smooth-but-unverified tasks (few events, weak grade) and common give-up points (blocks after N failures). Skip learning curves until more data.
>   what it is: Discovers the workflow Foreman really follows, mines smooth and failed tasks, and learns learning curves and give-up points.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 5 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Do T-0616, T-0617, T-0640, T-0641, T-0656, T-0657, T-0658 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0689. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0616: Outcome ledger (I076, value 4/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_outcomes.py -k Outcomes`
- [x] T-0617: Lesson lifecycle (I077, value 4/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_outcomes.py -k Lessons`
- [x] T-0640: Agent and pass yield (I080, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_outcomes.py -k Yield`
- [x] T-0641: Reflection and track record (I081, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_outcomes.py -k TrackRecord`
- [x] T-0656: Self-regression and eval hygiene (I078, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_outcomes.py -k Hygiene`
- [x] T-0657: Counterfactual and hindsight learning (I079, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_outcomes.py -k Reopen`
- [x] T-0658: Process mining (I082, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_outcomes.py -k Mining`
## Non-goals
## Approach (options → choice → why)
Options: (a) one learning store (outcomes.jsonl written at close and by night jobs); (b) derive every fate on demand from what's already recorded (git log, briefs, ledger, events, bench results); (c) a model pass that reads histories. Choice: (b) — every signal is already on disk (reverts in git, follow-up FIX briefs naming the id, finish events with failed counts, audit results, lesson_shown events, bench result files), so nothing new to keep in sync and no model spend. Placement: fmoutcomes.py (new: reverts, outcomes, track record, fm outcomes); fmrecall (lesson ids/stats, fm recall --lessons, wrong-turn source); fmcost (lens and pass yield in usage --agents and digest, track record and would-do-differently in digest); fmbench (bench hygiene); fmtidy (reopen blocked on deps closed or a named file changed, auto with --apply); fmfriction (process mining sections). Complete version later: +24h/+7d smoke fates via fm night, bench-gated lesson retire, per-finding audit records.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0616: Outcome ledger (I076, value 4/5, effort M, risk low)
2. [x] T-0617: Lesson lifecycle (I077, value 4/5, effort M, risk low)
3. [x] T-0640: Agent and pass yield (I080, value 3/5, effort S, risk low)
4. [x] T-0641: Reflection and track record (I081, value 3/5, effort S, risk low)
5. [x] T-0656: Self-regression and eval hygiene (I078, value 3/5, effort M, risk low)
6. [x] T-0657: Counterfactual and hindsight learning (I079, value 3/5, effort M, risk low)
7. [x] T-0658: Process mining (I082, value 3/5, effort M, risk low)
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md (Unreleased: learning from outcomes), ~/.claude/foreman/MASTER.md (plugin/lib row: fmoutcomes, fmfriction mining)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_outcomes.py` → ✗ exit 1 · Ran 8 tests in 0.9s (7 classes, 16 at a time; slowest: Reopen 1s, Outcomes 1s, Lessons 1s) / FAILED (7 classes) [ran] [tree 55822412a0e2] (2026-10-09T20:17:00Z)
- (step 1) `python3 plugin/tests/run.py -p test_outcomes.py -k Outcomes` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: Outcomes 1s) / OK [ran] [tree 81cf374f0dcc] (2026-10-09T20:21:07Z)
- (step 2) `python3 plugin/tests/run.py -p test_outcomes.py -k Lessons` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Lessons 1s) / OK [ran] [tree 81cf374f0dcc] (2026-10-09T20:21:08Z)
- (step 3) `python3 plugin/tests/run.py -p test_outcomes.py -k Yield` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Yield 1s) / OK [ran] [tree 81cf374f0dcc] (2026-10-09T20:21:09Z)
- (step 4) `python3 plugin/tests/run.py -p test_outcomes.py -k TrackRecord` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: TrackRecord 1s) / OK [ran] [tree 81cf374f0dcc] (2026-10-09T20:21:10Z)
- (step 5) `python3 plugin/tests/run.py -p test_outcomes.py -k Hygiene` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Hygiene 0s) / OK [ran] [tree 81cf374f0dcc] (2026-10-09T20:21:10Z)
- (step 6) `python3 plugin/tests/run.py -p test_outcomes.py -k Reopen` → exit 0 · Ran 2 tests in 0.9s (1 classes, 16 at a time; slowest: Reopen 1s) / OK [ran] [tree 81cf374f0dcc] (2026-10-09T20:21:11Z)
- (step 7) `python3 plugin/tests/run.py -p test_outcomes.py -k Mining` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Mining 0s) / OK [ran] [tree 81cf374f0dcc] (2026-10-09T20:21:12Z)
- (step 6) `python3 plugin/tests/run.py -p test_outcomes.py -k Reopen` → exit 0 · Ran 2 tests in 1.9s (1 classes, 16 at a time; slowest: Reopen 2s) / OK [ran] [tree 3fa0ba7ad42b] (2026-10-09T20:21:54Z)
- (ac 1) `python3 plugin/tests/run.py -p test_outcomes.py -k Outcomes` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: Outcomes 1s) / OK [ran] [tree 3fa0ba7ad42b] (2026-10-09T20:23:54Z)
- (ac 2) `python3 plugin/tests/run.py -p test_outcomes.py -k Lessons` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Lessons 1s) / OK [ran] [tree 3fa0ba7ad42b] (2026-10-09T20:23:54Z)
- (ac 3) `python3 plugin/tests/run.py -p test_outcomes.py -k Yield` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Yield 1s) / OK [ran] [tree 3fa0ba7ad42b] (2026-10-09T20:23:54Z)
- (ac 4) `python3 plugin/tests/run.py -p test_outcomes.py -k TrackRecord` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: TrackRecord 1s) / OK [ran] [tree 3fa0ba7ad42b] (2026-10-09T20:23:54Z)
- (ac 5) `python3 plugin/tests/run.py -p test_outcomes.py -k Hygiene` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Hygiene 0s) / OK [ran] [tree 3fa0ba7ad42b] (2026-10-09T20:23:54Z)
- (ac 6) `python3 plugin/tests/run.py -p test_outcomes.py -k Reopen` → exit 0 · Ran 2 tests in 1.0s (1 classes, 16 at a time; slowest: Reopen 1s) / OK [ran] [tree 3fa0ba7ad42b] (2026-10-09T20:23:54Z)
- (ac 7) `python3 plugin/tests/run.py -p test_outcomes.py -k Mining` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Mining 0s) / OK [ran] [tree 3fa0ba7ad42b] (2026-10-09T20:23:54Z)
- `python3 plugin/tests/run.py` → exit 0 · Ran 1197 tests in 68.1s (373 classes, 16 at a time; slowest: Stop 43s, TaskLifecycle 28s, Bench 27s) / OK [ran] [tree 3fa0ba7ad42b] (2026-10-09T20:23:54Z)
- (audit intent) `main-thread review of the diff against each member's first version, plus live runs on this project's real history` → all seven first versions shipped as briefed; the deferred parts (smoke fates at +24h/+7d, bench-gated lesson retire, per-finding audit records) captured as T-0743 [tree 3fa0ba7ad42b] (2026-10-09T20:23:54Z)
- (audit edge) `main-thread review of the diff against each member's first version, plus live runs on this project's real history` → fixed: release and batch FIX tasks naming several ids were counted as follow-up fixes (42 → 13 on real data, spot-checked T-0719, T-0741, T-0164); results opening with no/none count as clean; paths in block reasons must resolve inside the project; tidy only reopens on a change after the block (1 s slack) [tree 3fa0ba7ad42b] (2026-10-09T20:23:54Z)
- (audit operator) `main-thread review of the diff against each member's first version, plus live runs on this project's real history` → fixed: tidy is rarely run (JARVIS never has), so fm next names retryable blocked tasks when the queue is empty; reports are on demand, nothing new is stored, and the lone hot-path addition is the idle branch of fm next [tree 3fa0ba7ad42b] (2026-10-09T20:23:54Z)
## Log
- 2026-10-09T15:40:17Z created
- 2026-10-09T20:15:49Z criterion 1 verify: `` → `python3 plugin/tests/run.py -p test_outcomes.py -k Outcomes`
- 2026-10-09T20:15:49Z criterion 2 verify: `` → `python3 plugin/tests/run.py -p test_outcomes.py -k Lessons`
- 2026-10-09T20:15:49Z criterion 3 verify: `` → `python3 plugin/tests/run.py -p test_outcomes.py -k Yield`
- 2026-10-09T20:15:49Z criterion 4 verify: `` → `python3 plugin/tests/run.py -p test_outcomes.py -k TrackRecord`
- 2026-10-09T20:15:49Z criterion 5 verify: `` → `python3 plugin/tests/run.py -p test_outcomes.py -k Hygiene`
- 2026-10-09T20:15:49Z criterion 6 verify: `` → `python3 plugin/tests/run.py -p test_outcomes.py -k Reopen`
- 2026-10-09T20:15:49Z criterion 7 verify: `` → `python3 plugin/tests/run.py -p test_outcomes.py -k Mining`
- 2026-10-09T20:15:51Z focused
- 2026-10-09T20:23:55Z done
- 2026-10-09T20:23:55Z committed ac4119a (12 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- T-0676 [FEATURE M, done, 7 steps] Milestone: Features — Performance and cost — lesson: A 'degrade when over pace' rule must name what is optional: side offers and self-i…
- T-0672 [SECURITY L, done, 6 steps] Milestone: Features — Guard and safety — lesson: a safety claim shown to the user (restorable) must state its limits; a reviewer will …
- decision 2026-10-04: Brainstorm loop recorded dry after round 8 (1 strong idea of 41: fm oracle, queued); T-0214 sentinel and T-0217 lesson confidence deferred — low gro…
## Would do differently
run each new report against this project's real history before writing its test, not after
## Lessons
- Outcome signals already sit in git, the briefs and the ledger; the work is the join, and the join's heuristic needs a spot-check on real data (release tasks named the ids they shipped and looked like fixes)
## Files touched
- plugin/tests/test_outcomes.py
- plugin/lib/fmoutcomes.py
- plugin/lib/fmcli.py
- plugin/lib/fmrecall.py
- plugin/lib/fmhooks.py
- plugin/lib/fmcost.py
- plugin/lib/fmbench.py
- plugin/lib/fmtidy.py
- plugin/lib/fmfriction.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcore.py
