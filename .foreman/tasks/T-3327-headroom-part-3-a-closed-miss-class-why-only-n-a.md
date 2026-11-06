---
id: T-3327
type: FEATURE
tier: S
status: active
priority: normal
scope: [plugin/lib/sampo/selfaware.py, plugin/tests/test_self_aware.py]
depends_on: []
source: followup
created: 2026-11-06T04:31:26Z
updated: 2026-11-06T06:29:42Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a34ecabef7e98306f
lane_branch: worktree-agent-a34ecabef7e98306f
base: 0e503eeeeb87000325d02673ba119e35ff08b7e8
base_tree: 5c2bb7b2f14ef72b4659b9d747b61d1c44bc9aca
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T05:52:19Z
plan0_scope: [plugin/lib/sampo/selfaware.py, plugin/tests/test_self_aware.py]
builder_returned: 2026-11-06T06:29:42Z
---
# Headroom part 3: a 'closed' miss class: 'why only N' and 'more than this' steers are logged as closed-set misses
## Raw request
> Headroom part 3: a 'closed' miss class: 'why only N' and 'more than this' steers are logged as closed-set misses
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] selfaware.CLASSES has 'closed'; the user's message 'there's only 26 tower ideas, but how come there's not more than that?' is classed closed; existing classes unchanged — verify with `python3 plugin/tests/run.py test_self_aware`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] test with the user's own message, red  <- CURRENT
2. [x] add the class and its pattern
## Resume here
## Docs impact
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_self_aware` → ✗ exit 1 · Ran 4 tests in 32.4s (2 jobs, 16 at a time; slowest: Ledger 1s, Classify 0s) / FAILED (1 classes: test_self_aware.Ledger) (ran] (tree a7fd89fc020b] (world 2f1906870a] (2026-11-06T05:53:13Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_models test_rename_scan test_self_aware && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 220 tests in 53.1s (63 jobs, 16 at a time; slowest: ViewsRepair 13s, RenameScan 11s, Bench 6s) / FAILED (2 classes: test_left_out.LeftOut, test_self_aware.Ledger) (ran] (tree a7fd89fc020b] (world 2f1906870a] (2026-11-06T05:54:11Z)
- (step 2) `python3 plugin/tests/run.py test_self_aware` → exit 0 · Ran 5 tests in 122.2s (2 jobs, 16 at a time; slowest: Ledger 3s, Classify 1s) / OK (ran] (tree 875ae1acfb11] (world 2f1906870a] (2026-11-06T05:58:32Z)
- (step 2) `python3 plugin/tests/run.py test_self_aware` → exit 0 · Ran 5 tests in 272.8s (2 jobs, 16 at a time; slowest: Ledger 1s, Classify 0s) / OK (ran] (tree 326d6e98126f] (world 2f1906870a] (2026-11-06T06:24:09Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_models test_rename_scan test_self_aware && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 221 tests in 298.2s (72 jobs, 16 at a time; slowest: RenameScan.test_no_fm_only_command_regex 5s, ViewsRepair 5s, LockProbe 3s) / FAILED (1 classes: test_left_out.LeftOut) (ran] (tree 326d6e98126f] (world 2f1906870a] (2026-11-06T06:29:16Z)
## Log
- 2026-11-06T04:31:26Z created
- 2026-11-06T05:52:17Z focused
- 2026-11-06T05:52:19Z predicted from its closes: 2 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3316 [FEATURE M, planned, 3 steps] Headroom part 1: census of a project's fixed sets and caps, plus caps raised by hand (T-3316)
- T-3328 [FEATURE M, planned, 3 steps] Headroom part 4: orphans and proposals: work that fits no member of a set, a local-model 'what does a complete version lack' pass on…
- T-2774 [CLEAN M, done, 3 steps] Rune's anticipation gaps are consumed, not dropped: the next generation's predict action lists the last generation's missed steers, and s…
- decision 2026-10-31: Mission 6 (tools, #5) approach A: wire the parts Foreman has into one loop on the active task (T-2270's hook notices the miss; fm which, fm lib and …
- similar past tasks were M: consider --tier M
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
