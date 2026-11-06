---
id: T-3421
type: FEATURE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T09:57:38Z
updated: 2026-11-06T10:15:58Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a52fb904eaa0fceb9
lane_branch: worktree-agent-a52fb904eaa0fceb9
base: bde7afc07e1a546532ad97af95448441a0b9df0d
base_tree: 2d4ad93f64d5a5c0129271fa648fc6aa01d9471f
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T09:58:47Z
plan0_scope: []
builder_returned: 2026-11-06T10:15:58Z
---
# fm check --affected and sampo task evidence can sit idle up to 3600 s waiting for a CPU…
## Raw request
> FEATURE: fm check --affected and sampo task evidence can sit idle up to 3600 s waiting for a CPU slot when builders fill the pool, and hang guards read that as a timeout; print 'waiting for a test slot (N busy)' once, record the wait in the check_run event, and let the wait count against no timeout (T-3417 builder)
## Interpretation
Reading 1: notices on stderr plus recorded wait, as asked. Reading 2 (ruled out): pausing callers' outer timeouts; they live in other processes.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a full pool prints a waiting line and the wait is recorded — verify with `python3 plugin/tests/run.py test_slots.Slots`
## Non-goals
## Approach (options → choice → why)
1) use what exists: the slot loop in cpu_slot prints a notice, and cli check_run parses wait_s from the output; likely outcome: guards see output. 2) do less: notice only, no wait_s; fails if the wait stays unrecorded. 3) a status file the caller polls; fails if no caller reads it. Choice 1 (80%): smallest; the wait is already outside the class timeout and deadline (clock starts after cpu_slot); a caller's outer timeout cannot be paused, the notices keep its output alive.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests, then notices and wait_s
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_slots.Slots` → exit 0 · Ran 10 tests in 4.6s (1 jobs, 16 at a time; slowest: Slots 2s) / OK [ran] [tree 30a43af4a375] [world 2f1906870a] (2026-11-06T09:59:43Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_ci_annotations test_cli test_core test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_run test_slots test_verify_alias test_verify_unittest_form && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 778 tests in 197.5s (202 jobs, 16 at a time; slowest: PerTestJobs 147s, AffectedPairs 147s, CheckSkip 127s) / FAILED (1 classes: test_cli.AffectedPairs) [ran] [tree 30a43af4a375] [world 2f1906870a] (2026-11-06T10:03:10Z)
- (step 1) `python3 plugin/tests/run.py test_slots.Slots` → exit 0 · Ran 13 tests in 62.7s (1 jobs, 16 at a time; slowest: Slots 4s) / OK [ran] [tree 721a68da4036] [world 2f1906870a] (2026-11-06T10:15:50Z)
## Log
- 2026-11-06T09:57:38Z created
- 2026-11-06T09:58:33Z planned: it has criteria and steps
- 2026-11-06T09:58:46Z focused
- 2026-11-06T09:58:47Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-3252 [PERFORMANCE L, dropped, 4 steps] PERF: Sampo's work shouldn't eat the whole CPU, and should get faster. Measured…
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- decision 2026-11-06: No new builder lanes until T-3252's slot pool lands
- similar finished tasks took 3–4 steps
