---
id: T-3378
type: FIX
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T06:21:40Z
updated: 2026-11-06T09:27:18Z
lane: ~/.claude/foreman/.claude/worktrees/agent-afc590f8120a32622
lane_branch: worktree-agent-afc590f8120a32622
base: 3d1fb1b45301fd28e7778307c206b18fb6b25aa6
base_tree: f27a253dae101a7012916cf55e935e8195b9407a
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-06T08:56:19Z
plan0_scope: []
builder_returned: 2026-11-06T09:27:18Z
---
# Bash-sourced touched events carry data.at (file mtime) but last_change uses the event…
## Raw request
> FIX: Bash-sourced touched events carry data.at (file mtime) but last_change uses the event ts, so a Bash edit seen after a hook delay is timed late (T-3317 review)
## Interpretation
Reading 1: last_change/first_touch should date a touched event by data.at when plausible. Reading 2 (ruled out): change the hook to log ts=mtime; that rewrites history and the ledger ts is the append order.
## Assumptions (confidence)
## Acceptance criteria
- [ ] A touched event with at earlier than ts dates the change at at; one without at (or with a future at) keeps ts — verify with `python3 plugin/tests/run.py test_core.Ledger.test_last_change_dates_a_bash_edit_at_its_mtime`
## Non-goals
## Approach (options → choice → why)
1) Do less: patch last_change only; fails if first_touch keeps the same late-ts mistake. 2) Use what exists: a shared helper touch_time beside last_change, used by both timing readers; likely outcome: one place to fix. 3) Rewrite ts at the hook; fails because the ledger ts is append order and history would change. Choice 2 (85%): covers both readers.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test, then touch_time helper used by last_change and first_touch
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_core.Ledger` → exit 0 · Ran 4 tests in 84.0s (1 jobs, 16 at a time; slowest: Ledger 0s) / OK [ran] [tree 2ab4ab9cc827] [world 2f1906870a] (2026-11-06T08:57:57Z)
- `sampo check --affected (affected tests only): plugin/lib/sampo/louhi.py plugin/tests/test_exam.py && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 126 · bash: line 1: plugin/lib/sampo/louhi.py: Permission denied [ran] [tree 2ab4ab9cc827] [world 2f1906870a] (2026-11-06T08:58:04Z)
- (step 1) `python3 plugin/tests/run.py test_core.Ledger` → exit 0 · Ran 5 tests in 36.3s (1 jobs, 16 at a time; slowest: Ledger 0s) / OK [ran] [tree fa1e9397cb69] [world 2f1906870a] (2026-11-06T09:22:14Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_core test_doctor test_hooks test_left_out test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [17.38s] [ran] [tree fa1e9397cb69] [world 2f1906870a] (2026-11-06T09:27:13Z)
## Log
- 2026-11-06T06:21:40Z created
- 2026-11-06T08:56:04Z planned: it has criteria and steps
- 2026-11-06T08:56:18Z focused
- 2026-11-06T08:56:19Z predicted from its closes: 8 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0164 [FIX S, done, 3 steps] A Bash touch is timed by the file's mtime, so a scope reason logged in the same command covers it — lesson: An async hook's own clock is th…
- T-3317 [FIX S, active, 2 steps] Edits outside the repo don't stale a task's audits
- research wave1-plan-a306a171bb6861f90: === T-1044 [stale: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmcost.py changed since it was written]
- decision 2026-11-05: T-3082 merges with night wired and drive left for a follow-up
- the similar finished task took 3 steps
- start here (files T-0164 touched): plugin/tests/test_bash_touch.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py, CHANGELOG.md
