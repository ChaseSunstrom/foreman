---
id: T-3128
type: FEATURE
tier: S
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/hooks.py, plugin/lib/sampo/selfaware.py, plugin/tests/test_self_aware.py]
depends_on: []
source: user
created: 2026-11-05T03:20:45Z
updated: 2026-11-06T16:29:48Z
inferred_deps: [T-3123]
inferred_why: T-3123: named in its request
group: self-awareness and miss ledger
base: 10e7eac9ae066dec7ff1430294a92f943b6b5a0b
base_tree: 2953a27bc6b485332d522d1007643ec8de083fcc
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T12:46:59Z
plan0_scope: []
builder_returned: 2026-11-06T13:18:07Z
lane_stop: merged 2026-11-06T14:41:20Z
verified: strong
lane_verified: 791a5b6e839e087c496a4a41ad826581d4a4fd71
---
# Self-awareness part 3: at each task boundary, the predicted next asks no open task covers become captures, and a predicted capture the user later asks for counts as a catch (T-3123)
## Raw request
> Self-awareness part 3: at each task boundary, the predicted next asks no open task covers become captures, and a predicted capture the user later asks for counts as a catch (T-3123)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] at a task boundary the predictor's top three next asks that no open task's title or criteria cover are captured with source 'predicted'; when a later user message matches a predicted capture, it is marked caught and sampo misses counts catches beside misses — verify with `python3 plugin/tests/run.py test_self_aware`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests with a fake predictor
2. [x] the boundary capture and the catch match
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_self_aware.Boundary` → ✗ exit 1 · Ran 3 tests in 46.3s (1 jobs, 16 at a time; slowest: Boundary 1s) / FAILED (1 classes: test_self_aware.Boundary) [ran] [tree 75ae25e66550] [world 2f1906870a] (2026-11-06T12:48:56Z)
- (step 2) `python3 plugin/tests/run.py test_self_aware` → exit 0 · Ran 7 tests in 80.6s (3 jobs, 16 at a time; slowest: Boundary 0s, Ledger 0s, Classify 0s) / OK [ran] [tree bebd6b995ed4] [world 2f1906870a] (2026-11-06T12:52:06Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_core test_doctor test_hooks test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_self_aware test_verify_alias test_verify_unittest_form && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 942 tests in 95.0s (310 jobs, 16 at a time; slowest: TaskLifecycle 17s, Approvals 14s, UserPromptSubmit 11s) / FAILED (1 classes: test_left_out.LeftOut) [ran] [tree bebd6b995ed4] [world 2f1906870a] (2026-11-06T12:53:51Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_core test_doctor test_hooks test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_self_aware test_verify_alias test_verify_unittest_form && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [17.96s] [ran] [tree 6ac8d72a6f42] [world 2f1906870a] (2026-11-06T12:57:35Z)
- (step 2) `python3 plugin/tests/run.py test_self_aware` → ✗ exit 1 · Ran 9 tests in 125.6s (3 jobs, 16 at a time; slowest: Boundary 1s, Ledger 0s, Classify 0s) / FAILED (1 classes: test_self_aware.Boundary) [ran] [tree b409cab308ff] [world 2f1906870a] (2026-11-06T13:15:45Z)
- (step 2) `python3 plugin/tests/run.py test_self_aware` → exit 0 · Ran 9 tests in 66.3s (3 jobs, 16 at a time; slowest: Boundary 1s, Ledger 0s, Classify 0s) / OK [ran] [tree 537a79c51864] [world 2f1906870a] (2026-11-06T13:17:13Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 71bfd8dec220] (2026-11-06T14:41:24Z)
- (ac 1) `python3 plugin/tests/run.py test_self_aware` → exit 0 · Ran 9 tests in 107.6s (3 jobs, 16 at a time; slowest: Boundary 1s, Ledger 0s, Classify 0s) / OK [ran] [tree 71bfd8dec220] [world 2f1906870a] (2026-11-06T14:43:23Z)
- (step 1) `python3 plugin/tests/run.py test_self_aware.Boundary` → exit 0 · Ran 5 tests in 3.9s (1 jobs, 16 at a time; slowest: Boundary 1s) / OK [ran] [tree 71bfd8dec220] [world 2f1906870a] (2026-11-06T14:43:23Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 71bfd8dec220] (2026-11-06T14:43:23Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 71bfd8dec220] (2026-11-06T14:43:23Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 71bfd8dec220] (2026-11-06T14:43:23Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 71bfd8dec220] (2026-11-06T14:43:23Z)
## Log
- 2026-11-05T03:20:45Z created
- 2026-11-05T03:20:51Z set approved=True
- 2026-11-05T03:20:51Z blocked: approved; waits for a builder slot
- 2026-11-06T03:53:38Z unblocked
- 2026-11-06T12:46:58Z focused
- 2026-11-06T12:46:59Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T14:41:20Z merged worktree-agent-a28f05c61b88a3ee0 (5 file(s))
- 2026-11-06T14:41:21Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a28f05c61b88a3ee0
- 2026-11-06T14:41:21Z focused
- 2026-11-06T14:41:23Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/core.py', 'plugin/lib/sampo/hooks.py', 'plugin/lib/sampo/selfaware.py', 'plugin/tests/test_self_aware.py']
- 2026-11-06T14:41:23Z scope: widened at merge to the reviewed lane's own diff (791a5b6e8), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T14:47:23Z done
- 2026-11-06T14:47:27Z committed 566a10869 (1 file)
- 2026-11-06T16:29:48Z verified: the full suite is green on 1078ed22d, which contains 791a5b6e8
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3123 [FEATURE L, blocked, 3 steps] Self-awareness: Sampo notices what the user would otherwise point out: a miss ledger from the user's pointing-out messages, turn-end…
- T-2774 [CLEAN M, done, 3 steps] Rune's anticipation gaps are consumed, not dropped: the next generation's predict action lists the last generation's missed steers, and s…
- T-3316 [FEATURE M, active, 3 steps] Headroom part 1: census of a project's fixed sets and caps, plus caps raised by hand (T-3316)
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- similar past tasks were M: consider --tier M
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Plan gaps
- failed first: step 1 failing tests with a fake predictor
## Files touched
- plugin/tests/test_self_aware.py
- plugin/lib/sampo/selfaware.py
- plugin/lib/sampo/hooks.py
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/core.py
- CHANGELOG.md
