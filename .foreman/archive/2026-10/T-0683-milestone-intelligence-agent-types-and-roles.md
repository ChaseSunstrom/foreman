---
id: T-0683
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:16Z
updated: 2026-10-09T19:41:13Z
batch: [T-0608, T-0629, T-0646, T-0647, T-0648]
base: a81dfda80a5cabd36c825d0e69ca225e112e4df3
base_tree: dae7b9b59e59693390261ce5835cc3e2a4526485
verified: strong
---
# Milestone: Intelligence — Agent types and roles
## Raw request
> T-0608: FEATURE: New specialist agents (I030, value 4/5, effort M, risk low)
>   first version: Add fm-reproducer (FIX: writes failing test/repro before any fix; feeds fm task prove) and an fm-profiler lens for PERF; skip the rest (historian is fm why/recall, closer/remediator overlap fm second). New agent files need user's plugin yes.
>   what it is: Adds roles such as interrogator, historian, integrator, reproducer, profiler, designer and release captain.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 15 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0629: FEATURE: What agents hand back (I031, value 3/5, effort S, risk low)
>   first version: Add a 'Noticed:' line to each agent's return format (agents/*.md) and have fm research add --from-agent extract it into fm capture --source discovered; skip interviews and values cards.
>   what it is: Has every agent return a typed noticed field, interview on exit, and log grievances.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 8 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0646: FEATURE: Roles as data with benches (I029, value 3/5, effort M, risk low)
>   first version: First step: fm bench case-type that runs one role (reviewer) on seeded diffs with known planted bugs and scores catch rate; reuse fm evolve to mutate that agent file.
>   what it is: Defines each agent role as data, benches it, and compiles it per harness.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 8 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0647: FEATURE: Overseeing agents (I032, value 3/5, effort M, risk low)
>   first version: Per-agent-type scorecard in fm usage: spawns, tokens, findings confirmed vs false positive (from fm task audit results) and builder lanes merged vs discarded. Skip ombudsman, spokespersons, chronicler.
>   what it is: Tracks role drift, delegation ROI and per-agent scorecards, and lets an ombudsman watch.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 8 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0648: FEATURE: Lane control in flight (I033, value 3/5, effort M, risk med)
>   first version: First step: builders write an 'andon' note file in the lane that fm lane list and fm next surface to the main thread (stop-and-ask with declared assumptions). Skip ghost owners and prediction duels.
>   what it is: Lets any lane raise an andon or point of order and proceed on declared assumptions.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 5 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Do T-0608, T-0629, T-0646, T-0647, T-0648 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0683. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0608: New specialist agents (I030, value 4/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_roles.py -k Reproducer`
- [x] T-0629: What agents hand back (I031, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_roles.py -k Noticed`
- [x] T-0646: Roles as data with benches (I029, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_roles.py -k SeedReview`
- [x] T-0647: Overseeing agents (I032, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_roles.py -k Scorecard`
- [x] T-0648: Lane control in flight (I033, value 3/5, effort M, risk med) works — verify with `python3 plugin/tests/run.py -p test_roles.py -k Andon`
## Non-goals
## Approach (options → choice → why)
First versions, model-free to build and test (stub claude): T-0608 a fm-reproducer agent (FIX: writes the failing test or repro first, hands back the command for fm task prove) and a performance lens line in fm-reviewer; T-0629 a 'Noticed:' line in every agent's return format, and fm research add --from-agent turns each into fm capture --source discovered; T-0646 fm bench seed-review: seeded one-line bugs in a scratch copy as review cases with their known location, scored by whether the reviewer's findings name the file and line (±3); T-0647 fm usage --agents: per agent type spawns, tokens, findings confirmed vs rejected and lanes merged vs removed, from the budget ledger and the ledger; T-0648 an ANDON.md a builder writes in its lane (stop-and-ask with declared assumptions), surfaced by fm lane list and fm next. Options weighed: new roles as prompts only (no hand-back), or a separate scorecard tool — reuse fm usage and fm lane list instead.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0608: New specialist agents (I030, value 4/5, effort M, risk low)
2. [x] T-0629: What agents hand back (I031, value 3/5, effort S, risk low)
3. [x] T-0646: Roles as data with benches (I029, value 3/5, effort M, risk low)
4. [x] T-0647: Overseeing agents (I032, value 3/5, effort M, risk low)
5. [x] T-0648: Lane control in flight (I033, value 3/5, effort M, risk med)
## Resume here
## Docs impact
CHANGELOG; MASTER.md agents row
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_roles.py` → ✗ exit 1 · Ran 5 tests in 0.3s (5 classes, 16 at a time; slowest: Andon 0s, SeedReview 0s, Scorecard 0s) / FAILED (5 classes) [ran] [tree e651ee09b0d3] (2026-10-09T19:36:21Z)
- (step 1) `python3 plugin/tests/run.py -p test_roles.py -k Reproducer` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Reproducer 0s) / OK [ran] [tree e91ced033e97] (2026-10-09T19:37:02Z)
- (step 2) `python3 plugin/tests/run.py -p test_roles.py -k Noticed` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Noticed 0s) / OK [ran] [tree e91ced033e97] (2026-10-09T19:37:02Z)
- (step 3) `python3 plugin/tests/run.py -p test_roles.py -k SeedReview` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: SeedReview 0s) / OK [ran] [tree aa9973bb7675] (2026-10-09T19:38:11Z)
- (step 4) `python3 plugin/tests/run.py -p test_roles.py -k Scorecard` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Scorecard 0s) / OK [ran] [tree aa9973bb7675] (2026-10-09T19:38:11Z)
- (step 5) `python3 plugin/tests/run.py -p test_roles.py -k Andon` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Andon 0s) / OK [ran] [tree aa9973bb7675] (2026-10-09T19:38:12Z)
- (ac 1) `python3 plugin/tests/run.py -p test_roles.py -k Reproducer` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Reproducer 0s) / OK [ran] [tree cbb8faf0c5d2] (2026-10-09T19:41:11Z)
- (ac 2) `python3 plugin/tests/run.py -p test_roles.py -k Noticed` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Noticed 0s) / OK [ran] [tree cbb8faf0c5d2] (2026-10-09T19:41:11Z)
- (ac 3) `python3 plugin/tests/run.py -p test_roles.py -k SeedReview` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: SeedReview 1s) / OK [ran] [tree cbb8faf0c5d2] (2026-10-09T19:41:11Z)
- (ac 4) `python3 plugin/tests/run.py -p test_roles.py -k Scorecard` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Scorecard 0s) / OK [ran] [tree cbb8faf0c5d2] (2026-10-09T19:41:11Z)
- (ac 5) `python3 plugin/tests/run.py -p test_roles.py -k Andon` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Andon 1s) / OK [ran] [tree cbb8faf0c5d2] (2026-10-09T19:41:11Z)
- (audit intent) `self review of the five members against their first-version notes; full suite` → each member's first version shipped as its note asked (reproducer + performance lens, Noticed hand-back into captures, seeded-bug reviewer bench, per-agent scorecard, andon), model-free to build and test [tree cbb8faf0c5d2] (2026-10-09T19:41:11Z)
- (audit adversary) `self review of the five members against their first-version notes; full suite` → the reproducer edits, so it is worktree-bound like the builder (the guard confines any lane session) and in both editing-agent allowlists; noticed lines are redacted and capped before they become captures; seed-review never writes the repo, it shows the reviewer a diff; an andon is read as text, never followed [tree cbb8faf0c5d2] (2026-10-09T19:41:11Z)
- (audit edge) `self review of the five members against their first-version notes; full suite` → 'Noticed: none' and duplicates capture nothing; a lane whose folder is gone shows no andon; seed-review with no return lines refuses; scorecard sums only subagent features [tree cbb8faf0c5d2] (2026-10-09T19:41:11Z)
## Log
- 2026-10-09T15:40:16Z created
- 2026-10-09T19:33:48Z criterion 1 verify: `` → `python3 plugin/tests/run.py -p test_roles.py -k Reproducer`
- 2026-10-09T19:33:49Z criterion 2 verify: `` → `python3 plugin/tests/run.py -p test_roles.py -k Noticed`
- 2026-10-09T19:33:49Z criterion 3 verify: `` → `python3 plugin/tests/run.py -p test_roles.py -k SeedReview`
- 2026-10-09T19:33:49Z criterion 4 verify: `` → `python3 plugin/tests/run.py -p test_roles.py -k Scorecard`
- 2026-10-09T19:33:49Z criterion 5 verify: `` → `python3 plugin/tests/run.py -p test_roles.py -k Andon`
- 2026-10-09T19:33:49Z focused
- 2026-10-09T19:41:12Z done
- 2026-10-09T19:41:13Z committed 0fb22ea (16 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-intelligence-20261009: 768 ideas from 15 lenses over 4 rounds plus 3 deepened categories, in 106 capabilities; every idea under exactly one capabilit…
- T-0689 [FEATURE M, planned, 7 steps] Milestone: Intelligence — Learning from outcomes
- T-0677 [FEATURE M, done, 8 steps] Milestone: Features — Planning, briefs and queue — lesson: Seven small first versions fit one milestone when each reuses an existing me…
- decision 2026-09-27: Recursion bound for T-0063: after R5, one more round (R6: auto-evidence from Bash results matching a criterion's verify command) from the existing R…
- the similar finished task took 8 steps
## Lessons
- A new editing agent inherits the builder's whole envelope (worktree, branch-only commits, allowlists in doctor and tests), or it is a hole in the read-only rule
## Files touched
- plugin/tests/test_roles.py
- plugin/agents/fm-reproducer.md
- plugin/agents/fm-builder.md
- plugin/agents/fm-debugger.md
- plugin/agents/fm-recon.md
- plugin/agents/fm-reviewer.md
- plugin/agents/fm-scout.md
- plugin/lib/fmcli.py
- plugin/lib/fmbench.py
- plugin/lib/fmcost.py
- plugin/lib/fmcore.py
- plugin/lib/fmlanes.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmdoctor.py
- plugin/tests/test_docs.py
- .claude-plugin/marketplace.json
- plugin/.claude-plugin/plugin.json
