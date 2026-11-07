---
id: T-3378
type: FIX
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/core.py, plugin/lib/sampo/hooks.py, plugin/tests/test_core.py]
depends_on: []
source: discovered
created: 2026-11-06T06:21:40Z
updated: 2026-11-06T21:59:37Z
base: 81de6117ebb5eb92339e29c572d44667cd4faca5
base_tree: 4292d2cb372e7e78d517e0b86024e6a8727f7921
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-06T08:56:19Z
plan0_scope: []
builder_returned: 2026-11-06T09:27:18Z
lane_stop: merged 2026-11-06T18:26:22Z
verified: strong
---
# Bash-sourced touched events carry data.at (file mtime) but last_change uses the event…
## Raw request
> FIX: Bash-sourced touched events carry data.at (file mtime) but last_change uses the event ts, so a Bash edit seen after a hook delay is timed late (T-3317 review)
## Interpretation
Reading 1: last_change/first_touch should date a touched event by data.at when plausible. Reading 2 (ruled out): change the hook to log ts=mtime; that rewrites history and the ledger ts is the append order.
## Assumptions (confidence)
## Acceptance criteria
- [x] A touched event with at earlier than ts dates the change at at; one without at (or with a future at) keeps ts — verify with `python3 plugin/tests/run.py test_core.Ledger.test_last_change_dates_a_bash_edit_at_its_mtime`
## Non-goals
## Approach (options → choice → why)
1) Do less: patch last_change only; fails if first_touch keeps the same late-ts mistake. 2) Use what exists: a shared helper touch_time beside last_change, used by both timing readers; likely outcome: one place to fix. 3) Rewrite ts at the hook; fails because the ledger ts is append order and history would change. Choice 2 (85%): covers both readers.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test, then touch_time helper used by last_change and first_touch
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_core.Ledger` → exit 0 · Ran 4 tests in 84.0s (1 jobs, 16 at a time; slowest: Ledger 0s) / OK [ran] [tree 2ab4ab9cc827] [world 2f1906870a] (2026-11-06T08:57:57Z)
- `sampo check --affected (affected tests only): plugin/lib/sampo/louhi.py plugin/tests/test_exam.py && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 126 · bash: line 1: plugin/lib/sampo/louhi.py: Permission denied [ran] [tree 2ab4ab9cc827] [world 2f1906870a] (2026-11-06T08:58:04Z)
- (step 1) `python3 plugin/tests/run.py test_core.Ledger` → exit 0 · Ran 5 tests in 36.3s (1 jobs, 16 at a time; slowest: Ledger 0s) / OK [ran] [tree fa1e9397cb69] [world 2f1906870a] (2026-11-06T09:22:14Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_core test_doctor test_hooks test_left_out test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [17.38s] [ran] [tree fa1e9397cb69] [world 2f1906870a] (2026-11-06T09:27:13Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree c0181b0bf521] (2026-11-06T18:34:05Z)
- `python3 plugin/tests/run.py test_core` → ✗ exit 1 · Ran 150 tests in 4.7s (30 jobs, 16 at a time; slowest: ConfidenceRoutes 3s, Migrate 2s, WritesAndLocks 2s) / FAILED (1 classes: test_core.Ledger) (start tree + this task's tests) [ran] [tree c0181b0bf521] [world 2f1906870a] (2026-11-06T18:34:16Z)
- `python3 plugin/tests/run.py test_core` → exit 0 · Ran 150 tests in 3.4s (30 jobs, 16 at a time; slowest: ConfidenceRoutes 3s, Migrate 2s, WritesAndLocks 2s) / OK [ran] [tree c0181b0bf521] [world 2f1906870a] (2026-11-06T18:34:16Z)
- (ac 1) `python3 plugin/tests/run.py test_core.Ledger.test_last_change_dates_a_bash_edit_at_its_mtime` → exit 0 · Ran 1 tests in 0.4s (1 jobs, 16 at a time; slowest: Ledger 0s) / OK [ran] [tree c0181b0bf521] [world 2f1906870a] (2026-11-06T18:34:19Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree c0181b0bf521] (2026-11-06T18:34:19Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree c0181b0bf521] (2026-11-06T18:34:19Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree c0181b0bf521] (2026-11-06T18:34:19Z)
## Log
- 2026-11-06T06:21:40Z created
- 2026-11-06T08:56:04Z planned: it has criteria and steps
- 2026-11-06T08:56:18Z focused
- 2026-11-06T08:56:19Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-06T18:26:22Z merged worktree-agent-afc590f8120a32622 in merge train
- 2026-11-06T18:34:05Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/core.py', 'plugin/lib/sampo/hooks.py', 'plugin/tests/test_core.py']
- 2026-11-06T18:34:05Z scope: widened at merge to the reviewed lane's own diff (d74cca4ef), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T18:35:03Z done
- 2026-11-06T18:35:06Z committed 16d73c11b (1 file)
- 2026-11-06T21:59:37Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-afc590f8120a32622; dropped: its task is closed; the lane was left behind after the merge
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0164 [FIX S, done, 3 steps] A Bash touch is timed by the file's mtime, so a scope reason logged in the same command covers it — lesson: An async hook's own clock is th…
- T-3317 [FIX S, active, 2 steps] Edits outside the repo don't stale a task's audits
- research wave1-plan-a306a171bb6861f90: === T-1044 [stale: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmcost.py changed since it was written]
- decision 2026-11-05: T-3082 merges with night wired and drive left for a follow-up
- the similar finished task took 3 steps
- start here (files T-0164 touched): plugin/tests/test_bash_touch.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py, CHANGELOG.md
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Files touched
- plugin/tests/test_core.py
- plugin/lib/sampo/core.py
- .fm-scratch/e.json
- plugin/lib/sampo/hooks.py
- CHANGELOG.md
