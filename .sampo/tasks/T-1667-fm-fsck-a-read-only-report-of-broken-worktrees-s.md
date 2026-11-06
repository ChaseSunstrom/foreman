---
id: T-1667
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/lib/fmdoctor.py, plugin/tests/test_reliability_tools.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-22T20:59:12Z
updated: 2026-10-22T21:53:22Z
base: dff8d3d9c9b523f0a59ec7a19bd7826ced699796
base_tree: f9a8d9db66a419edc07b7418125deecd82c5c616
plan0_at: 2026-10-22T21:30:50Z
plan0_scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/lib/fmdoctor.py, plugin/tests/test_reliability_tools.py, CHANGELOG.md]
verified: strong
---
# fm fsck: a read-only report of broken worktrees, stale locks and torn journals, --fix for the safe repairs
## Raw request
> fm fsck: a read-only report of broken worktrees, stale locks and torn journals, --fix for the safe repairs
## Interpretation
fm fsck [--fix] [--json] is a deeper check of Foreman's own state than fm doctor: lane worktrees whose directory or branch is gone (broken), lock files whose holder process is dead (stale), and journal or ledger files whose last line is torn (no newline, or not JSON). It is read-only by default; --fix removes only stale locks. It never touches another project's worktrees. fm doctor reports fsck's one-line summary, so /foreman:doctor covers it from Claude Code.
## Assumptions (confidence)
## Acceptance criteria
- [x] fsck reports a planted broken worktree, stale lock and torn journal, and --fix repairs only the lock — verify with `python3 plugin/tests/run.py test_reliability_tools.Fsck`
## Non-goals
## Approach (options → choice → why)
Options: fold every check into fm doctor (doctor grows slow and mixed); repair silently at startup (hides damage); a separate read-only verb that doctor summarises. Choice: the separate verb: doctor stays the one health entry and fsck the deep scan. --fix is limited to stale locks, because a broken worktree or a torn ledger needs a person's judgement (the ledger is hash-chained).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test with a temp home
2. [x] three checks
3. [x] --fix limited to stale locks
## Resume here
## Docs impact
~/.claude/foreman/MASTER.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_reliability_tools.Fsck 2>&1 | tail -15` → ✗ exit 1 · Ran 6 tests in 3.2s (1 classes, 16 at a time; slowest: Fsck 2s) / FAILED (1 classes) [ran] [tree 876578bcfbe8] (2026-10-22T21:35:43Z)
- (step 1) `python3 plugin/tests/run.py test_reliability_tools.Fsck` → ✗ exit 1 · Ran 6 tests in 1.7s (1 classes, 16 at a time; slowest: Fsck 2s) / FAILED (1 classes) [ran] [tree 876578bcfbe8] (2026-10-22T21:35:47Z)
- (ac 1) `python3 plugin/tests/run.py test_reliability_tools.Fsck 2>&1 | tail -30` → exit 0 · Ran 6 tests in 1.8s (1 classes, 16 at a time; slowest: Fsck 2s) / OK [ran] [tree aceddd3d00fa] (2026-10-22T21:37:00Z)
- (step 2) `python3 plugin/tests/run.py test_reliability_tools.Fsck` → exit 0 · Ran 6 tests in 1.8s (1 classes, 16 at a time; slowest: Fsck 2s) / OK [ran] [tree 53ec73de9ad7] (2026-10-22T21:37:30Z)
- (step 3) `python3 plugin/tests/run.py -k test_fix_removes_only_the_stale_lock -k test_a_closed_task_and_a_young_or_odd_lock_are_not_findings -p test_reliability_tools.py` → exit 0 · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: Fsck 1s) / OK [ran] [tree 53ec73de9ad7] (2026-10-22T21:37:31Z)
- (ac 1) `python3 plugin/tests/run.py test_reliability_tools.Fsck 2>&1 | grep -E "^(FAIL|ERROR|Ran|OK|FAILED)|Error:" | head -30` → ✗ exit 1 · Ran 12 tests in 7.1s (1 classes, 16 at a time; slowest: Fsck 7s) / FAILED (1 classes) [ran] [tree 9c064e00f9ea] (2026-10-22T21:45:37Z)
- (step 3) `python3 plugin/tests/run.py test_reliability_tools.Fsck` → ✗ exit 1 · Ran 12 tests in 10.6s (1 classes, 16 at a time; slowest: Fsck 10s) / FAILED (1 classes) [ran] [tree 9c064e00f9ea] (2026-10-22T21:45:51Z)
- (ac 1) `python3 plugin/tests/run.py test_reliability_tools.Fsck 2>&1 | grep -E "^(FAIL|ERROR|Ran|OK|FAILED)|Error:" | head -30` → ✗ exit 1 · Ran 12 tests in 4.1s (1 classes, 16 at a time; slowest: Fsck 4s) / FAILED (1 classes) [ran] [tree df52c23e0178] (2026-10-22T21:47:58Z)
- (ac 1) `python3 plugin/tests/run.py test_reliability_tools.Fsck 2>&1 | grep -E "^(FAIL|ERROR|Ran|OK|FAILED)|Error:" | head -30` → exit 0 · Ran 12 tests in 4.2s (1 classes, 16 at a time; slowest: Fsck 4s) / OK [ran] [tree 57d9e7863216] (2026-10-22T21:48:06Z)
- (step 3) `python3 plugin/tests/run.py test_reliability_tools.Fsck` → exit 0 · Ran 12 tests in 6.3s (1 classes, 16 at a time; slowest: Fsck 6s) / OK [ran] [tree 4ca4f3868d6e] (2026-10-22T21:48:35Z)
- (ac 1) `python3 plugin/tests/run.py test_reliability_tools.Fsck` → exit 0 · Ran 12 tests in 6.0s (1 classes, 16 at a time; slowest: Fsck 6s) / OK [ran] [tree 8f8e570cf973] (2026-10-22T21:52:24Z)
- (step 3) `python3 plugin/tests/run.py test_reliability_tools test_doctor && fm fsck` → exit 0 · OK / fm fsck: OK: no broken lanes, stale locks or torn journals [ran] [tree 8f8e570cf973] (2026-10-22T21:52:34Z)
- (audit adversary) `--fix removes only *.pid locks at least an hour old with a dead holder, and refuses outside the host PID namespace (fixed inode check); symlinks, FIFOs and other files left alone` → fixed with tests [tree 8f8e570cf973] (2026-10-22T21:52:35Z)
- (audit edge) `pruned worktree records reported broken; deep JSON caught; unreadable files reported; a torn line re-read once` → tested [tree 8f8e570cf973] (2026-10-22T21:52:36Z)
- (audit operator) `fm fsck on the real state, read-only` → OK in 0.2 s; fm doctor shows its count and --fix removes stale locks [tree 8f8e570cf973] (2026-10-22T21:52:36Z)
- (audit maintainer) `project slug on every line; lane rm hint only for the current project` → clean [tree 8f8e570cf973] (2026-10-22T21:52:37Z)
- (audit intent) `criterion: reports a broken worktree, stale lock and torn journal; --fix repairs only the lock` → met (12 tests) [tree 8f8e570cf973] (2026-10-22T21:52:37Z)
- (ac 1) `python3 plugin/tests/run.py test_reliability_tools.Fsck` → exit 0 · Ran 12 tests in 5.3s (1 classes, 16 at a time; slowest: Fsck 5s) / OK [ran] [tree 8f8e570cf973] (2026-10-22T21:52:50Z)
- (audit adversary) `one fm-reviewer five-lens pass; all findings fixed test-first; criterion green after the merge` → --fix bounded to old dead-holder pid files, refused outside the host PID namespace [tree 8f8e570cf973] (2026-10-22T21:52:50Z)
- (audit edge) `one fm-reviewer five-lens pass; all findings fixed test-first; criterion green after the merge` → pruned worktree records, deep JSON, unreadable files [tree 8f8e570cf973] (2026-10-22T21:52:50Z)
- (audit intent) `one fm-reviewer five-lens pass; all findings fixed test-first; criterion green after the merge` → met (12 tests) [tree 8f8e570cf973] (2026-10-22T21:52:50Z)
## Log
- 2026-10-22T20:59:12Z created
- 2026-10-22T20:59:13Z set scope=['plugin/lib/fmcore.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmdoctor.py', 'plugin/tests/test_reliability_tools.py', 'CHANGELOG.md']
- 2026-10-22T20:59:14Z split from T-1552 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:30:04Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_reliability_tools.Fsck`
- 2026-10-22T21:30:27Z criterion 1 text: fsck reports a planted broken worktree, stale lock and torn journal, and --fix repairs only the lock — verify with python3 plugin/tests/run.py test_reliability_tools.Fsck → fsck reports a planted broken worktree, stale lock and torn journal, and --fix repairs only the lock
- 2026-10-22T21:30:32Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1667.builder.md
- 2026-10-22T21:30:50Z focused
- 2026-10-22T21:37:20Z scope: MASTER.md widened: doctor's self-docs check needs the new fm fsck verb named there; the main thread asked for one short addition
- 2026-10-22T21:52:06Z merged worktree-agent-addfdef0f36ca424a (5 file(s))
- 2026-10-22T21:52:06Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-addfdef0f36ca424a
- 2026-10-22T21:52:08Z focused
- 2026-10-22T21:52:38Z scope: MASTER.md bullet after Crash hygiene (self-docs); fmcli registers the verb
- 2026-10-22T21:53:22Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1405 [FIX M, done, 4 steps] Crash hygiene: stack dumps for hung verbs, safe stale index.lock removal, a lock probe in doctor — lesson: A safety rule written as 'unknow…
- research T-1405-review: Verdict:** approve with nits. I found no CRITICAL or HIGH defect. I read the code and tests in the worktree and ran nothing, because the tools I …
- research wave2-plan-af4fd23e40a859f90: === T-1028 [stale: plugin/lib/fmbus.py, plugin/lib/fmcli.py, plugin/lib/fmlanes.py changed since it was written]
- decision 2026-10-22: T-1405: an unreadable /proc process of ours keeps a stale index.lock only when it is a git; any other unreadable process doesn't block (31 of this h…
- the similar finished task took 4 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_doctor.py
## Why not caught
tests used a same-namespace dead pid
## Lessons
- A dead-pid check is only true in the PID namespace the pid was written in; a repair tool must refuse to judge from inside a sandbox, and require age as well
## Plan gaps
- failed first: step 1 failing test with a temp home
## Files touched
- plugin/tests/test_reliability_tools.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmcli.py
- MASTER.md
- CHANGELOG.md
