---
id: T-2284
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T06:32:06Z
updated: 2026-10-31T13:31:16Z
base: 46fda1f770694d7f0800b67e7d237696f995186b
base_tree: 4331170111542b5481547c395c671180666b5df5
plan0_at: 2026-10-31T06:35:13Z
plan0_scope: []
verified: strong
---
# Measured perf proof (Mission 7, #6): fm task evidence ID --bench "<cmd>" times the command on the task's start tree and on the current tree, and records the medians as the Measurements, run not typed
## Raw request
> Measured perf proof (Mission 7, #6): fm task evidence ID --bench "<cmd>" times the command on the task's start tree and on the current tree, and records the medians as the Measurements, run not typed
## Interpretation
Gap map #6: 'perf baseline gate'. A PERFORMANCE task closes on typed numbers (fm task finish --numbers, T-1956), so a speedup is a claim nobody ran, and fm proof (T-2273) now counts such closes as unproven. The proof is a measurement of both sides by Foreman itself.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task evidence ID --step N --bench CMD [--repeat K] runs CMD K times (default 5) in a throwaway worktree at the task's base and K times in the current tree, records '<cmd>: <base median> → <now median> (K runs each)' as run evidence and in Measurements, and a PERFORMANCE task's finish accepts it in place of typed --numbers; it refuses without a base commit, and a run that fails on either side records the failure — verify with `python3 plugin/tests/run.py test_evidence_quality test_cli`
## Non-goals
## Approach (options → choice → why)
1) --bench on fm task evidence: a throwaway git worktree at the task's base commit (as fm task prove does), CMD run K times there and K times in the current tree under the evidence runner's timeout, medians recorded as run evidence and written to Measurements; finish's PERF gate accepts a bench line as the numbers. 2) a separate fm bench verb — rejected: the proof belongs on the task's evidence. 3) compare against the last commit — rejected: the task's base is the right before. Choice 1.
## Risks and rollback
Timing noise: medians of K, and the line says K; a run under 50 ms is flagged as too fast to compare. CMD runs repo code like any --run (same consent rules: the user's own tree).
## Execution prompt
## Steps
1. [x] red tests: a seeded slow→fast script records before→after medians; a failing side recorded; no base refused; PERF finish accepts it
2. [x] the --bench path in fm task evidence (worktree at base, timing, cleanup)
3. [x] docs: give MASTER and CHANGELOG lines in the report
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_evidence_quality` → exit 0 · Ran 14 tests in 3.3s (4 classes, 16 at a time; slowest: Bench 3s, Assume 2s, Inconclusive 2s) / OK [ran] [tree d3ba05c5fb7e] (2026-10-31T06:36:56Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_evidence_quality test_guard_cases test_paused && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [12.42s] [ran] [tree d3ba05c5fb7e] (2026-10-31T06:37:53Z)
- `python3 plugin/tests/run.py test_evidence_quality test_cli` → ✗ exit 1 · Ran 155 tests in 20.3s (46 classes, 16 at a time; slowest: TaskLifecycle 19s, StateViews 8s, CaptureAndIntake 7s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree fd93500f670f] (2026-10-31T06:43:45Z)
- `python3 plugin/tests/run.py test_evidence_quality test_cli` → exit 0 · Ran 155 tests in 19.5s (46 classes, 16 at a time; slowest: TaskLifecycle 19s, StateViews 8s, CaptureAndIntake 7s) / OK [ran] [tree fd93500f670f] (2026-10-31T06:43:45Z)
- (step 1) `python3 plugin/tests/run.py test_evidence_quality test_cli` → exit 0 · Ran 155 tests in 19.5s (46 classes, 16 at a time; slowest: TaskLifecycle 19s, StateViews 8s, CaptureAndIntake 7s) / OK [ran] [tree fd93500f670f] (2026-10-31T06:44:05Z)
- (step 2) `python3 plugin/tests/run.py test_evidence_quality test_cli` → exit 0 · Ran 155 tests in 19.5s (46 classes, 16 at a time; slowest: TaskLifecycle 19s, StateViews 8s, CaptureAndIntake 7s) / OK [ran] [tree fd93500f670f] (2026-10-31T06:44:24Z)
- (step 3) `python3 plugin/tests/run.py test_evidence_quality test_cli` → exit 0 · Ran 155 tests in 19.5s (46 classes, 16 at a time; slowest: TaskLifecycle 19s, StateViews 8s, CaptureAndIntake 7s) / OK [ran] [tree fd93500f670f] (2026-10-31T06:44:44Z)
- (ac 1) `python3 plugin/tests/run.py test_evidence_quality test_cli` → exit 0 · Ran 155 tests in 19.6s (46 classes, 16 at a time; slowest: TaskLifecycle 19s, StateViews 8s, CaptureAndIntake 8s) / OK [ran] [tree e721d00cc394] (2026-10-31T06:47:36Z)
- (audit intent) `self-review of the diff: one --timeout deadline covers all 2K runs; the base worktree is removed in finally; output redacted by run_command; refusals for --bench with --run, typed, inconclusive, expect-fail` → a PERFORMANCE close can rest on a measurement Foreman made of both sides instead of typed numbers (test_evidence_quality red-to-green) [tree e721d00cc394] (2026-10-31T06:47:36Z)
- (audit adversary) `self-review of the diff: one --timeout deadline covers all 2K runs; the base worktree is removed in finally; output redacted by run_command; refusals for --bench with --run, typed, inconclusive, expect-fail` → CMD runs like any --run, in the user's own tree and a throwaway worktree of it; no new consent path [tree e721d00cc394] (2026-10-31T06:47:36Z)
- (audit edge) `self-review of the diff: one --timeout deadline covers all 2K runs; the base worktree is removed in finally; output redacted by run_command; refusals for --bench with --run, typed, inconclusive, expect-fail` → no base commit refused; a failing side is recorded as the failure and the other side skipped; untracked deps missing on the base side show as a failure, not hidden [tree e721d00cc394] (2026-10-31T06:47:36Z)
## Log
- 2026-10-31T06:32:06Z created
- 2026-10-31T06:34:57Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2284.builder.md
- 2026-10-31T06:35:12Z focused
- 2026-10-31T06:41:13Z merged worktree-agent-ab10957598a59af51 (2 file(s))
- 2026-10-31T06:47:16Z scope: plugin/lib/fmcli.py (_bench, evidence --bench), plugin/tests/test_evidence_quality.py, MASTER.md, CHANGELOG.md
- 2026-10-31T06:48:29Z done
- 2026-10-31T06:48:32Z committed c824fc38 (1 file)
- 2026-10-31T13:31:16Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab10957598a59af51
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2273 [FEATURE M, done, 3 steps] Unproven rollup (Mission 7, #6): done tasks whose criteria rest on typed or inconclusive evidence, or UI changes with no visual check, …
- playbook Profiling (fm playbooks show perf/profiling)
- research mission-20261030-025317: Request: Mission 3, Genesis gen 1: #1 Initiative — Foreman finds work nobody asked for in any project (scout probes for the project, bu…
- decision 2026-10-31: While the Genesis tower waits on T-2221 (Mission 3's critique; the cold-read rule change is the user's steer-2 call, T-2246), build the gap map's Mi…
- the similar finished task took 3 steps
## Lessons
- A measured claim needs both sides run by the same harness under one deadline, or the before is a memory
## Files touched
- plugin/tests/test_evidence_quality.py
- .fm-scratch/e.json
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmfind.py
- plugin/lib/ladder_rules/javascript/eval-call.scm
- plugin/lib/ladder_rules/javascript/loose-null-compare.scm
- plugin/lib/ladder_rules/python/bare-except.scm
- plugin/lib/ladder_rules/python/mutable-default.scm
- plugin/tests/test_find.py
