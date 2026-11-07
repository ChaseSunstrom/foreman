---
id: T-3558
type: PERFORMANCE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T00:43:44Z
updated: 2026-11-07T04:24:26Z
lane: ~/.claude/foreman.lanes/T-3558
lane_branch: foreman/T-3558
base: 746ca71b53870cb530fb6a5b61ddf2324ec5760c
base_tree: 624d8cb4b78f002d60e7ad2565e20ee8f6a18b24
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T02:39:07Z
plan0_scope: []
lane_stop: merged 2026-11-07T04:14:53Z
lane_verified: 020346f6dd8d82f6614b6c5fc59884a8991a8bde
---
# Sampo focus holds the project lock 1.8-7.3 s (sampled from /proc/locks while 8 lanes…
## Raw request
> PERF: sampo focus holds the project lock 1.8-7.3 s (sampled from /proc/locks while 8 lanes focused): under it run git branch/worktree snapshots, a full load_briefs, recall, outcomes.predict on a first focus, and regen_views, whose state_dict spends 0.4 of 0.57 s in rune.health reading the ledger; take the git and recall work before the lock (T-2342 did doors) and cache or skip rune.health in regen (found in T-3535)
## Interpretation
Reading 1 (chosen): focus and every cli.mutate (task set/ac/step/evidence) hold the shared project lock across slow work (git snapshots, recall, outcomes.predict, regen_views re-reading every brief); move that work out of the lock, keeping only the brief/meta/ledger read-modify-write under it, never losing a concurrent write. Folds in T-3556 (regen out of the lock). Reading 2 (ruled out): make the slow work itself faster (rune.health cache, a brief index): T-3565 and T-3573 do that; the hold would still grow with the briefs.
## Assumptions (confidence)
## Acceptance criteria
- [ ] A concurrent edit made while focus does its slow pre-lock work survives, and focus holds the project lock only for the brief's read-modify-write — verify with `nice -n 10 python3 plugin/tests/run.py test_focus_lock`
- [ ] mutate and focus regenerate STATE.md and the status files after releasing the project lock, the sync mirror still exports under it — verify with `nice -n 10 python3 plugin/tests/run.py test_focus_lock`
## Non-goals
## Approach (options → choice → why)
1) do less: only move regen_views out of mutate's lock (T-3556 alone). likely outcome: task edits drop to ~0.05 s, focus still holds git snapshots and recall 2-7 s. 2) use what exists: T-2342's pattern (doors read before the lock in cmd_focus) and lock(p.dir/<name>) sub-locks (train) — extended to the git, recall and predict work and a views lock. likely outcome: the same as 3, which builds on it. 3) two phases: focus computes git, recall and predict from an unlocked peek, then under the lock re-reads the brief, re-checks and applies (recomputing only an input that moved); mutate and focus regenerate views after the lock under a views lock (compute and write as one step, so the last regen saw every save), the sync mirror export stays under the project lock (T-3556: sync off's removal relies on it). likely outcome: focus hold ~0.3 s, edits ~0.05 s. 4) a background view daemon that coalesces regens. fails if: its lifecycle (start, crash, stale pid) costs more than it saves. Choice 3 (80%), built from 2's patterns: smallest diff that frees the lock for hooks and keeps every invariant.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: concurrent edit during focus survives; regen runs outside the project lock; views still regenerate
2. [x] Focus: git, recall and predict work before the lock, re-read and apply under it; mutate and focus regen after the lock under a views lock (mirror export stays locked)
3. [x] Measure lock hold for focus, evidence and task set before/after; run the related suites
## Resume here
## Docs impact
none: internal lock scope (cli.mutate, cmd_focus, core.regen_views/export_mirror); no documented behaviour or command changes.
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_focus_lock` → red as expected (exit 1) · Ran 3 tests in 23.9s (1 jobs, 16 at a time; slowest: FocusLock 7s) / FAILED (1 classes: test_focus_lock.FocusLock) [ran] [tree bd0a56f3de35] [world 2f1906870a] (2026-11-07T02:46:00Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_focus_lock` → exit 0 · Ran 3 tests in 66.8s (1 jobs, 16 at a time; slowest: FocusLock 2s) / OK [ran] [tree b4a14ec4159e] [world 2f1906870a] (2026-11-07T02:53:56Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_focus_lock test_sync` → exit 0 · Ran 40 tests in 9.6s (38 jobs, 16 at a time; slowest: FocusLock 2s, Sync.test_explicit_off_is_respected_and_checkpoints_ignore_the_mirror 2s, Sync.test_a_failed_commit_puts_it_back_and_only_export_ret [ran] [tree b2a8b3d17491] [world 2f1906870a] (2026-11-07T02:59:05Z)
## Log
- 2026-11-07T00:43:44Z created
- 2026-11-07T02:38:30Z planned: it has criteria and steps
- 2026-11-07T02:38:37Z lane: ~/.claude/foreman.lanes/T-3558 on foreman/T-3558
- 2026-11-07T02:39:06Z focused
- 2026-11-07T02:39:07Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T04:14:53Z merged foreman/T-3558 in merge train
- 2026-11-07T04:24:26Z verified: the full suite is green on 020346f6d, which contains 020346f6d
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- decision 2026-11-06: Sync is off until its export is cheap: every state write re-exported all ~3,300 briefs under the project lock (sync.export inside regen_views), so c…
## Measurements
Project-lock hold (time inside c.lock(p.dir), median; a bench test on a --shared clone of this repo with the real 2,371 briefs, ledger and closes copied in; load ~27-40 on 16 cores): focus (first) 2.185 s → 0.044 s (max 2.676 → 0.053); focus (switch/again) 1.317 s → 0.043 s (max 1.593 → 0.053); task evidence 0.224 s → 0.004 s (max 0.365 → 0.005); task set 0.165 s → 0.004 s (max 0.333 → 0.008). Wall: focus first 4.73 → 3.07 s, evidence 0.33 → 0.14 s (one shared worktree snapshot per focus instead of one per paused task plus one for the base).
