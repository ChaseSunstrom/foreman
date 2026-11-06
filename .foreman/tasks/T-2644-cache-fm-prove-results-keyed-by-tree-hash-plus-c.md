---
id: T-2644
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_finish_reuse.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-11-02T19:21:26Z
updated: 2026-11-02T19:55:32Z
base: 70245f9d8eb66786e4cc73956fa513a765b85295
base_tree: 1c68dd523ead00def66881e8107b5841b84af925
plan0_at: 2026-11-02T19:51:41Z
plan0_scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_finish_reuse.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# fm task finish reuses a criterion's passing run when the same command already ran on this exact tree and world, instead of running it again (T-2625's close spent 165 s re-running what had just passed)
## Raw request
> PERF: Cache fm prove results keyed by tree hash plus command so unchanged trees skip the rerun (c11: Speed: caching, warm daemon, impacted tests; value 3, effort S, risk low)
> CONTEXT: from the 2 November brainstorm (research/brainstorm-20261102.md, 552 ideas grounded in 59 clusters); each line is a cluster Claude marked build; the user's ticks on the Foreman Idea Triage page re-order them.
## Interpretation
Reading 1 (chosen): the cost that repeats is at close: fm task finish runs every open criterion's verify command even when fm task evidence --run just recorded that exact command passing, stamped [ran] [tree X] [world W] on the same working tree and environment. Reuse that run instead; the gates' own fm check at finish is untouched. Reading 2 (ruled out): cache fm prove's finder runs by tree. Its runs are rare and already gated; the 165-second closes this session were criteria and gates.
## Assumptions (confidence)
## Acceptance criteria
- [x] a criterion whose exact command has a [ran] passing evidence line stamped with the current tree and world closes without a second run (the finish names it reused); a different tree, world, command or a failed later run runs it again — verify with `python3 plugin/tests/run.py test_finish_reuse`
- [x] the finish and close suites still pass — verify with `python3 plugin/tests/run.py test_finish_reuse test_close_gates test_cli test_core`
## Non-goals
## Approach (options → choice → why)
1) In task_finish, before running a criterion, look for the newest evidence line of that exact command: passing, [ran], [tree] equal to the current tree id and [world] equal to the current world hash, with no failed run of it after; if found, check the criterion as reused. Likely outcome: closes that follow fm task evidence --run skip the rerun. 2) Cache results in a separate store keyed by (command, tree, world). Fails if: it duplicates what the brief's evidence lines already record and drifts from them. 3) Skip reruns on time alone (last pass under N minutes). Fails if: an edit in between makes the pass stale. 4) Do less: only print that a rerun was redundant. Likely outcome: no time saved. 5) Use what exists: the [ran], [tree] and [world] marks fm already writes on every run (T-2398), and the tree id fm evidence uses. Likely outcome: no new store. Choice 1 built on 5 (85%).
## Risks and rollback
A flaky or time-dependent check could pass once and fail later on the same tree; the reuse only takes a pass with no failed run after it, and fm check's gates still run at close. Rollback: git revert.
Blast radius (fm graph blast): co-changes plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmhooks.py, README.md, plugin/lib/fmexam.py; past FIXes T-1056, T-1106, T-1117, T-1122, T-1124.
## Execution prompt
## Steps
1. [x] red test
2. [x] reuse in task_finish, keyed on (command, tree, world)
3. [x] docs: CHANGELOG, MASTER
## Resume here
## Docs impact
CHANGELOG (Unreleased entry); MASTER.md: a Close reuse bullet (map count bumped).
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_finish_reuse` → ✗ exit 1 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: FinishReuse 1s) / FAILED (1 classes: test_finish_reuse.FinishReuse) [ran] [tree b32757774bff] [world 2f1906870a] (2026-11-02T19:52:15Z)
- (step 1) `python3 plugin/tests/run.py test_finish_reuse` → ✗ exit 1 · Ran 3 tests in 1.9s (1 classes, 16 at a time; slowest: FinishReuse 2s) / FAILED (1 classes: test_finish_reuse.FinishReuse) [ran] [tree 8b1e82a4bf37] [world 2f1906870a] (2026-11-02T19:52:34Z)
- (step 2) `python3 plugin/tests/run.py test_finish_reuse test_close_gates test_cli test_core` → exit 0 · Ran 302 tests in 28.3s (74 classes, 16 at a time; slowest: TaskLifecycle 28s, CloseGates 23s, CaptureAndIntake 16s) / OK [ran] [tree 57c58c2e326d] [world 2f1906870a] (2026-11-02T19:53:44Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 103 tests in 8.3s (24 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree 5784b1bc5083] [world 2f1906870a] (2026-11-02T19:54:04Z)
- (ac 1) `python3 plugin/tests/run.py test_finish_reuse` → exit 0 · Ran 3 tests in 2.0s (1 classes, 16 at a time; slowest: FinishReuse 2s) / OK [ran] [tree 5784b1bc5083] [world 2f1906870a] (2026-11-02T19:54:28Z)
- (ac 2) `python3 plugin/tests/run.py test_finish_reuse test_close_gates test_cli test_core` → exit 0 · Ran 302 tests in 21.2s (74 classes, 16 at a time; slowest: TaskLifecycle 21s, CloseGates 16s, CaptureAndIntake 9s) / OK [ran] [tree 5784b1bc5083] [world 2f1906870a] (2026-11-02T19:54:28Z)
- (step 1) `python3 plugin/tests/run.py test_finish_reuse` → exit 0 · Ran 3 tests in 2.0s (1 classes, 16 at a time; slowest: FinishReuse 2s) / OK [ran] [tree 5784b1bc5083] [world 2f1906870a] (2026-11-02T19:54:28Z)
- (audit intent) `self (M PERF): the reuse is keyed on fm's own marks: (ran], the worktree tree id and the world hash, the newest line of the exact command; a later failed run, an edit, a lockfile change, a typed line or a different command all run it again (three tests); gates at close untouched` → closes stop paying twice for a check that just passed on the same files [tree 5784b1bc5083] (2026-11-02T19:54:28Z)
- (audit adversary) `self (M PERF): the reuse is keyed on fm's own marks: (ran], the worktree tree id and the world hash, the newest line of the exact command; a later failed run, an edit, a lockfile change, a typed line or a different command all run it again (three tests); gates at close untouched` → a typed evidence line can't carry (ran], (tree] or (world] (_unmarked strips them), so it can't be reused as a pass [tree 5784b1bc5083] (2026-11-02T19:54:28Z)
## Log
- 2026-11-02T19:21:26Z created
- 2026-11-02T19:51:39Z planned from capture
- 2026-11-02T19:51:40Z focused
- 2026-11-02T19:55:15Z done
- 2026-11-02T19:55:18Z committed 845127d3 (5 files)
- 2026-11-02T19:55:32Z correction: the --numbers line claimed criterion 2 was reused at this close; it was not (docs edited after its evidence run moved the tree); Measurements corrected
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2642 [FEATURE S, done, 3 steps] fm ship refuses to push when the tree it would push isn't the tree its tests ran on (an edit or checkout between the gates and the push…
- research brainstorm-20261102: 552 ideas in 59 clusters, each grounded in the code: 104 built, 197 new, 249 partial, 2 premise-false. 24 clusters marked build.
- T-2657 [FEATURE S, done, 3 steps] flakes.json counts each flaky test's fails and passes; fm doctor lists the three worst by fail rate with the command that flakes them —…
- decision 2026-10-20: [cites: research/brainstorm-20261020] Round 1 of the 2026-10-20 brainstorm builds T-1254 (cost per fully-correct session on the page), T-1255 (Claud…
- similar finished tasks took 3–3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_core.py
## Measurements
Correction (the number first recorded here was wrong): at this task's own close criterion 2 ran again (21 s), because the docs were edited after its evidence run, so the tree differed and the reuse rightly refused. Measured instead by test_finish_reuse: across an evidence run and a finish on an unchanged tree the command runs once, not twice (one run of 302 tests, about 21 to 29 s, saved per close that follows its evidence with no edit in between). The saving only applies when the evidence run is the last change before the close; a docs edit after it costs the rerun.
## Lessons
- Fresh evidence means the same files and the same world, not a fresh process: key reuse on the tree and world marks fm already stamps
## Plan gaps
- failed first: step 1 red test
## Files touched
- plugin/tests/test_finish_reuse.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
