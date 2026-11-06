---
id: T-3383
type: FIX
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T06:41:41Z
updated: 2026-11-06T09:56:04Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a2f1e18efd3bd34d3
lane_branch: worktree-agent-a2f1e18efd3bd34d3
base: 19cf45dc02be51d02cca75532c0a953687420bda
base_tree: f7e92771539040aa709b2972758be9d5f52b3845
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-06T08:45:58Z
plan0_scope: []
builder_returned: 2026-11-06T09:56:04Z
---
# Sampo task evidence --run '<cmd> | tail' records the pipe's exit code, not the…
## Raw request
> FIX: sampo task evidence --run '<cmd> | tail' records the pipe's exit code, not the command's: refuse a top-level pipe in --run, or run it with pipefail and say so (T-3353 builder)
## Interpretation
Reading 1: run --run with pipefail. Reading 2 (ruled out): refuse top-level pipes, which would break legitimate pipes like grep|wc.
## Assumptions (confidence)
## Acceptance criteria
- [ ] false | cat records failure, true | cat success — verify with `python3 plugin/tests/run.py test_evidence_quality`
## Non-goals
## Approach (options → choice → why)
1) use what exists: core.run_command already shared, add -o pipefail; fails if: a command relies on a tolerated pipe failure 2) refuse pipes; fails if: legit pipes blocked 3) do less: document only; fails if: still records green. Choice 1 (90%): shared path, one line
## Risks and rollback
## Execution prompt
## Steps
1. [x] pipefail in run_command + test
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_evidence_quality` → exit 0 · Ran 20 tests in 56.9s (5 jobs, 16 at a time; slowest: Bench 4s, Inconclusive 1s, Assume 1s) / OK [ran] [tree 2cf307836d1e] [world 2f1906870a] (2026-11-06T08:48:41Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_core test_doctor test_evidence_quality test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [14.79s] [ran] [tree 2cf307836d1e] [world 2f1906870a] (2026-11-06T08:50:09Z)
- (step 1) `python3 plugin/tests/run.py test_evidence_quality` → exit 0 · Ran 21 tests in 9.2s (5 jobs, 16 at a time; slowest: Bench 7s, Assume 2s, Inconclusive 1s) / OK [ran] [tree 3098e6d97eaa] [world 2f1906870a] (2026-11-06T08:54:09Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_core test_doctor test_evidence_quality test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [13.97s] [ran] [tree 3098e6d97eaa] [world 2f1906870a] (2026-11-06T08:54:50Z)
- (ac 1) `python3 plugin/tests/run.py test_evidence_quality` → exit 0 · Ran 22 tests in 67.5s (5 jobs, 16 at a time; slowest: Bench 5s, Assume 1s, Inconclusive 1s) / OK [ran] [tree 12ec2871a74b] [world 2f1906870a] (2026-11-06T09:13:05Z)
- (ac 1) `python3 plugin/tests/run.py test_evidence_quality` → ✗ exit 1 · Ran 22 tests in 47.1s (5 jobs, 16 at a time; slowest: Bench 5s, Assume 1s, Inconclusive 1s) / FAILED (1 classes: test_evidence_quality.Pipefail) [ran] [tree 9de8269e2c64] [world 2f1906870a] (2026-11-06T09:13:58Z)
- (ac 1) `python3 plugin/tests/run.py test_evidence_quality` → exit 0 · Ran 22 tests in 103.0s (5 jobs, 16 at a time; slowest: Bench 7s, Assume 2s, Surprise 2s) / OK [ran] [tree 5b26dfd49424] [world 2f1906870a] (2026-11-06T09:15:46Z)
- (step 1) `python3 plugin/tests/run.py test_evidence_quality` → exit 0 · Ran 22 tests in 129.8s (13 jobs, 16 at a time; slowest: Inconclusive 2s, Bench.test_medians_before_and_after_are_recorded_and_finish_accepts_them 2s, Bench.test_a_command_resolving_into_the_tree_runs_ [ran] [tree 5b26dfd49424] [world 2f1906870a] (2026-11-06T09:17:58Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_core test_doctor test_evidence_quality test_hooks test_kalevala test_lane_twins test_lanes test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 1114 tests in 624.1s (445 jobs, 16 at a time; slowest: AffectedPairs.test_only_the_red_first_file_itself_is_left_out 99s, AffectedPairs.test_an_affected_run_with_evidence_records_it 45s, AffectedP [ran] [tree 5b26dfd49424] [world 2f1906870a] (2026-11-06T09:28:33Z)
- (step 1) `python3 plugin/tests/run.py test_hooks test_evidence_quality` → exit 0 · Ran 281 tests in 149.9s (209 jobs, 16 at a time; slowest: SessionStart.test_budget_holds_with_large_queue 7s, NoTaskGateMulti.test_at_stop_the_requests_with_evidence_close_when_every_python_start_take [ran] [tree deb65b21c0b6] [world 2f1906870a] (2026-11-06T09:51:38Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_core test_doctor test_evidence_quality test_hooks test_kalevala test_lane_twins test_lanes test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [26.02s] [ran] [tree deb65b21c0b6] [world 2f1906870a] (2026-11-06T09:55:52Z)
## Log
- 2026-11-06T06:41:41Z created
- 2026-11-06T08:45:46Z planned: it has criteria and steps
- 2026-11-06T08:45:58Z focused
- 2026-11-06T08:45:58Z predicted from its closes: 8 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0773 [FIX S, done, 2 steps] Evidence runs whose output reports failing tests count as failures even when a pipe hides the exit — lesson: evidence must read the run's o…
- T-2765 [FIX S, done, 2 steps] A piped fm check (or sampo check) without pipefail is refused with how to run it instead, rather than a note read after the fact: the exit …
- T-1759 [FIX S, done, 1 steps] A piped fm check reads green when the gates are red: say so on the Bash call
- decision 2026-11-02: [costly] T-2663's credential-name exemption reverted; the bare-name refusal stays fail-closed
- similar finished tasks took 1–2 steps
- start here (files T-0773 touched): plugin/tests/test_core.py, plugin/lib/fmcore.py
