---
id: T-1731
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmlanes.py, plugin/lib/fmbus.py, plugin/lib/fmcore.py, plugin/agents/fm-builder.md, plugin/tests/test_bookkeeping.py, plugin/tests/test_lanes.py, plugin/tests/test_cli.py, plugin/tests/test_bus.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-23T03:35:16Z
updated: 2026-10-23T04:45:33Z
batch: [T-1711, T-1712, T-1718, T-1729]
base: c4a9fba234a12173eef76e5cdcef1682b7c3918c
base_tree: ec2fd21daa4fc12e6e6bfc9a4426e3caf9db2e17
plan0_at: 2026-10-23T04:01:25Z
plan0_scope: [plugin/lib/fmcli.py, plugin/lib/fmlanes.py, plugin/lib/fmbus.py, plugin/lib/fmcore.py, plugin/agents/fm-builder.md, plugin/tests/test_bookkeeping.py, plugin/tests/test_lanes.py, plugin/tests/test_cli.py, plugin/tests/test_bus.py, CHANGELOG.md]
verified: strong
---
# Lane and close friction: finish --commit and shared files, CLEAN behaviour-lock in builder briefs, check --affected ski…
## Raw request
> T-1711: fm task finish --commit commits a shared file (CHANGELOG.md) whole, including another open task's lines, without a notice (fmcli.py:1231 _theirs, 1511 git add)
> T-1712: Builder briefs for CLEAN tasks don't say to record the behaviour lock (fm check --evidence ID --step 1) before the first edit, so CLEAN lanes fail the close gate (fmlanes.py:551-580, agents/fm-builder.md)
> T-1718: fm check --affected passes a test module it says it skipped (a red-first test of another lane, e.g. test_fmshot) to run.py, which then fails 'no test matches'
> T-1729: fm lease drop prints another session's lease line instead of confirming the caller's own drop (three builders reported it)
## Interpretation
Do T-1711, T-1712, T-1718, T-1729 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-1731. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1711: finish --commit on a shared file (CHANGELOG.md) that also holds another open task's uncommitted lines commits only this task's lines, or says which task's lines it took along — verify with `python3 plugin/tests/run.py test_bookkeeping.CommitOwnFiles`
- [x] T-1712: a builder brief for a CLEAN task says to record the behaviour lock (fm check --evidence ID --step 1) before the first edit — verify with `python3 plugin/tests/run.py test_lanes`
- [x] T-1718: fm check --affected never passes a module it reports as skipped to run.py — verify with `python3 plugin/tests/run.py test_cli.AffectedPairs`
- [x] T-1729: fm lease drop confirms what it dropped for the caller and lists no other session's lease as if it were the result — verify with `python3 plugin/tests/run.py test_bus.Lease`
## Non-goals
## Approach (options → choice → why)
Four small fixes, each test-first in the named test class. T-1711: options: stage only the hunks whose lines name the task (git apply --cached of a filtered diff) (chosen when the file is a union-merged log like CHANGELOG.md); refuse the commit (rejected: blocks closes); a notice only (fallback when hunks can't be split). T-1712: add the behaviour-lock line to fmlanes' brief for CLEAN and to agents/fm-builder.md. T-1718: --affected filters the module list after skipping, in the same place it prints the skip. T-1729: lease drop prints 'dropped: PATH' lines for the caller's leases and nothing else (other leases only with --all).
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1711: Fm task finish --commit commits a shared file (CHANGELOG.md) whole, including another open
2. [x] T-1712: Builder briefs for CLEAN tasks don't say to record the behaviour lock (fm check --evidence
3. [x] T-1718: Fm check --affected passes a test module it says it skipped (a red-first test of another l
4. [x] T-1729: Fm lease drop prints another session's lease line instead of confirming the caller's own d
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli -k test_a_skipped_red_first 2>&1 | tail -30` → exit 0 · Ran 112 tests in 36.9s (34 classes, 16 at a time; slowest: TaskLifecycle 37s, StateViews 15s, Checks 15s) / OK [ran] [tree 319efbe57f4c] (2026-10-23T04:08:06Z)
- (step 2) `python3 plugin/tests/run.py -k AffectedPairs.test_a_skipped_red_first 2>&1 | tail -30` → exit 0 · Ran 1 tests in 1.6s (1 classes, 16 at a time; slowest: AffectedPairs 1s) / OK [ran] [tree 319efbe57f4c] (2026-10-23T04:08:10Z)
- (step 1) `python3 plugin/tests/run.py test_bookkeeping.CommitOwnFiles` → exit 0 · Ran 3 tests in 3.1s (1 classes, 16 at a time; slowest: CommitOwnFiles 3s) / OK [ran] [tree 78bf65b5d502] (2026-10-23T04:12:11Z)
- (step 2) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 33 tests in 19.8s (5 classes, 16 at a time; slowest: Lanes 20s, BoardLanes 1s, SafeGitFailsClosed 0s) / OK [ran] [tree 78bf65b5d502] (2026-10-23T04:12:37Z)
- (step 3) `python3 plugin/tests/run.py test_cli.AffectedPairs` → exit 0 · Ran 2 tests in 2.9s (1 classes, 16 at a time; slowest: AffectedPairs 3s) / OK [ran] [tree 78bf65b5d502] (2026-10-23T04:12:40Z)
- (step 4) `python3 plugin/tests/run.py test_bus.Lease` → exit 0 · Ran 3 tests in 4.3s (1 classes, 16 at a time; slowest: Lease 4s) / OK [ran] [tree 78bf65b5d502] (2026-10-23T04:12:45Z)
- (ac 1) `python3 plugin/tests/run.py test_bookkeeping.CommitOwnFiles` → exit 0 · Ran 3 tests in 3.1s (1 classes, 16 at a time; slowest: CommitOwnFiles 3s) / OK [ran] [tree 4e3fde6c23f4] (2026-10-23T04:39:29Z)
- (ac 2) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 33 tests in 13.0s (5 classes, 16 at a time; slowest: Lanes 13s, BoardLanes 1s, SafeGitFailsClosed 0s) / OK [ran] [tree 4e3fde6c23f4] (2026-10-23T04:39:42Z)
- (ac 3) `python3 plugin/tests/run.py test_cli.AffectedPairs` → exit 0 · Ran 4 tests in 3.8s (1 classes, 16 at a time; slowest: AffectedPairs 4s) / OK [ran] [tree 4e3fde6c23f4] (2026-10-23T04:39:47Z)
- (ac 4) `python3 plugin/tests/run.py test_bus.Lease` → exit 0 · Ran 4 tests in 3.4s (1 classes, 16 at a time; slowest: Lease 3s) / OK [ran] [tree 4e3fde6c23f4] (2026-10-23T04:39:50Z)
- (ac 1) `python3 plugin/tests/run.py test_bookkeeping.CommitOwnFiles` → exit 0 · Ran 3 tests in 3.1s (1 classes, 16 at a time; slowest: CommitOwnFiles 3s) / OK [ran] [tree 4e3fde6c23f4] (2026-10-23T04:40:28Z)
- (ac 2) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 33 tests in 12.9s (5 classes, 16 at a time; slowest: Lanes 13s, BoardLanes 1s, SafeGitFailsClosed 0s) / OK [ran] [tree 4e3fde6c23f4] (2026-10-23T04:40:28Z)
- (ac 3) `python3 plugin/tests/run.py test_cli.AffectedPairs` → exit 0 · Ran 4 tests in 3.8s (1 classes, 16 at a time; slowest: AffectedPairs 4s) / OK [ran] [tree 4e3fde6c23f4] (2026-10-23T04:40:28Z)
- (ac 4) `python3 plugin/tests/run.py test_bus.Lease` → exit 0 · Ran 4 tests in 3.4s (1 classes, 16 at a time; slowest: Lease 3s) / OK [ran] [tree 4e3fde6c23f4] (2026-10-23T04:40:28Z)
- (audit intent) `fm-reviewer full pass (approve with nits); all five nits fixed test-first: red-first skips by exact path, not stem; the shared-file notice says 'was also edited by T-xxxx' and caps at 8; lease drop caps at 8 and names lane claims still held; an all-skipped --affected run says so and points at the full gates` → closes say whose edits ride along in a shared file; CLEAN builder briefs ask for the behaviour lock first; --affected never hands run.py a module it skipped; lease drop says only what it dropped [tree 4e3fde6c23f4] (2026-10-23T04:40:28Z)
- (audit edge) `fm-reviewer full pass (approve with nits); all five nits fixed test-first: red-first skips by exact path, not stem; the shared-file notice says 'was also edited by T-xxxx' and caps at 8; lease drop caps at 8 and names lane claims still held; an all-skipped --affected run says so and points at the full gates` → a same-name test under another runner still runs; the notice relies on 'touched' records, so shell edits by another task go unnamed [tree 4e3fde6c23f4] (2026-10-23T04:40:28Z)
- (audit operator) `fm-reviewer full pass (approve with nits); all five nits fixed test-first: red-first skips by exact path, not stem; the shared-file notice says 'was also edited by T-xxxx' and caps at 8; lease drop caps at 8 and names lane claims still held; an all-skipped --affected run says so and points at the full gates` → lease output keeps its JSON keys and the 'Dropped N lease(s).' line callers read [tree 4e3fde6c23f4] (2026-10-23T04:40:28Z)
- `python3 plugin/tests/run.py test_bookkeeping.CommitOwnFiles test_cli.AffectedPairs test_bus.Lease` → ✗ exit 1 · Ran 11 tests in 9.4s (3 classes, 16 at a time; slowest: AffectedPairs 8s, CommitOwnFiles 7s, Lease 7s) / FAILED (3 classes) (start tree + this task's tests) [ran] [tree 4e3fde6c23f4] (2026-10-23T04:42:34Z)
- `python3 plugin/tests/run.py test_bookkeeping.CommitOwnFiles test_cli.AffectedPairs test_bus.Lease` → exit 0 · Ran 11 tests in 7.8s (3 classes, 16 at a time; slowest: AffectedPairs 7s, CommitOwnFiles 7s, Lease 7s) / OK [ran] [tree 4e3fde6c23f4] (2026-10-23T04:42:34Z)
- (audit intent) `fm-reviewer full pass (approve with nits); all five nits fixed test-first: red-first skips by exact path, not stem; the shared-file notice says 'was also edited by T-xxxx' and caps at 8; lease drop caps at 8 and names lane claims still held; an all-skipped --affected run says so and points at the full gates` → closes say whose edits ride along in a shared file; CLEAN builder briefs ask for the behaviour lock first; --affected never hands run.py a module it skipped; lease drop says only what it dropped [tree 4e3fde6c23f4] (2026-10-23T04:42:40Z)
- (audit edge) `fm-reviewer full pass (approve with nits); all five nits fixed test-first: red-first skips by exact path, not stem; the shared-file notice says 'was also edited by T-xxxx' and caps at 8; lease drop caps at 8 and names lane claims still held; an all-skipped --affected run says so and points at the full gates` → a same-name test under another runner still runs; the notice relies on 'touched' records, so shell edits by another task go unnamed [tree 4e3fde6c23f4] (2026-10-23T04:42:40Z)
- (audit operator) `fm-reviewer full pass (approve with nits); all five nits fixed test-first: red-first skips by exact path, not stem; the shared-file notice says 'was also edited by T-xxxx' and caps at 8; lease drop caps at 8 and names lane claims still held; an all-skipped --affected run says so and points at the full gates` → lease output keeps its JSON keys and the 'Dropped N lease(s).' line callers read [tree 4e3fde6c23f4] (2026-10-23T04:42:40Z)
## Log
- 2026-10-23T03:35:16Z created
- 2026-10-23T03:35:49Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_bookkeeping.CommitOwnFiles`
- 2026-10-23T03:35:49Z criterion 1 text: T-1711: Fm task finish --commit commits a shared file (CHANGELOG.md) whole, including another open works → T-1711: finish --commit on a shared file (CHANGELOG.md) that also holds another open task's uncommitted lines commits only this task's lines, or says which task's lines it took along
- 2026-10-23T03:35:51Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_lanes`
- 2026-10-23T03:35:51Z criterion 2 text: T-1712: Builder briefs for CLEAN tasks don't say to record the behaviour lock (fm check --evidence works → T-1712: a builder brief for a CLEAN task says to record the behaviour lock (fm check --evidence ID --step 1) before the first edit
- 2026-10-23T03:35:53Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_cli.AffectedPairs`
- 2026-10-23T03:35:53Z criterion 3 text: T-1718: Fm check --affected passes a test module it says it skipped (a red-first test of another l works → T-1718: fm check --affected never passes a module it reports as skipped to run.py
- 2026-10-23T03:35:55Z criterion 4 verify: `` → `python3 plugin/tests/run.py test_bus.Lease`
- 2026-10-23T03:35:55Z criterion 4 text: T-1729: Fm lease drop prints another session's lease line instead of confirming the caller's own d works → T-1729: fm lease drop confirms what it dropped for the caller and lists no other session's lease as if it were the result
- 2026-10-23T03:35:58Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmlanes.py', 'plugin/lib/fmbus.py', 'plugin/lib/fmcore.py', 'plugin/agents/fm-builder.md', 'plugin/tests/test_bookkeeping.py', 'plugin/tests/test_lanes.py', 'plugin/tests/test_cli.py', 'plugin/tests/test_bus.py', 'CHANGELOG.md']
- 2026-10-23T04:01:15Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1731.builder.md
- 2026-10-23T04:01:25Z focused
- 2026-10-23T04:36:15Z merged worktree-agent-afd0cc30b74e15bc6 (8 file(s))
- 2026-10-23T04:36:16Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-afd0cc30b74e15bc6
- 2026-10-23T04:39:25Z focused
- 2026-10-23T04:39:58Z scope: merged lane files (fmcli.py, fmbus.py, fmlanes.py, tests, CHANGELOG.md)
- 2026-10-23T04:45:33Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- T-0729 [FIX S, done, 3 steps] Friction: lane rm unlocks a finished builder's worktree; no false re-ask note on capture
- research wave2-plan-af4fd23e40a859f90: === T-1028 [stale: plugin/lib/fmbus.py, plugin/lib/fmcli.py, plugin/lib/fmlanes.py changed since it was written]
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar finished tasks took 3–5 steps
- start here (files T-1117 touched): plugin/tests/test_close_gates.py, plugin/lib/fmcli.py, CHANGELOG.md, MASTER.md, README.md
- likely tests for the scope: plugin/tests/test_bus.py, plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_lanes.py
## Preflight
Changed in scope since this was planned (2026-10-23): CHANGELOG.md, plugin/lib/fmbus.py, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmlanes.py, plugin/tests/test_bookkeeping.py, plugin/tests/test_bus.py, plugin/tests/test_cli.py, plugin/tests…; re-ground the plan against them before editing
## Why not caught
none: each was friction seen in use (builders' reports), not a regression a test could have caught
## Lessons
- Skip a test by its path, never by its name
## Files touched
- plugin/tests/test_bookkeeping.py
- plugin/tests/test_lanes.py
- plugin/tests/test_cli.py
- plugin/tests/test_bus.py
- plugin/lib/fmcli.py
- plugin/lib/fmbus.py
- plugin/lib/fmlanes.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcodetui.py
- plugin/lib/fmdoctor.py
- plugin/tests/helpers.py
- plugin/tests/run.py
- plugin/tests/test_code.py
- plugin/tests/test_code_tui.py
- plugin/tests/test_docs.py
- plugin/tests/test_doctor.py
- plugin/tests/test_help.py
- plugin/tests/test_run.py
- plugin/tests/test_showpieces.py
- plugin/tests/test_site_hero.py
