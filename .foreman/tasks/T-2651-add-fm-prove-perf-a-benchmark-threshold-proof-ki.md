---
id: T-2651
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_bench_under.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-02T19:21:26Z
updated: 2026-11-02T20:12:14Z
builder_model: sonnet
base: 3e7509ccdbbd7c34791d14240ca1931c46cdcb39
base_tree: f6885b29c742653001a789bc1c6e5f91904c3f02
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T20:00:32Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_bench_under.py, CHANGELOG.md]
lane_stop: merged 2026-11-02T20:10:26Z
verified: strong
---
# fm task evidence --bench CMD --under MS: a benchmark that is a pass/fail proof, failing when the median is over the threshold (today --bench records medians but never fails)
## Raw request
> FEATURE: Add fm prove --perf: a benchmark threshold proof kind (c18: Proof kinds and verification; value 3, effort M, risk med)
> CONTEXT: from the 2 November brainstorm (research/brainstorm-20261102.md, 552 ideas grounded in 59 clusters); each line is a cluster Claude marked build; the user's ticks on the Foreman Idea Triage page re-order them.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a bench whose median is over --under MS records a failed run (exit 1, the median and the bar), one under it a pass; --under without --bench is a usage error — verify with `python3 plugin/tests/run.py test_bench_under`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] --under on fm task evidence and _bench
3. [x] CHANGELOG
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_bench_under 2>&1 | tail -15` → ✗ exit 1 · Ran 12 tests in 16.5s (1 classes, 16 at a time; slowest: BenchUnder 14s) / FAILED (1 classes: test_bench_under.BenchUnder) [ran] [tree de1829417460] [world 2f1906870a] (2026-11-02T20:01:06Z)
- (ac 1) `python3 plugin/tests/run.py test_bench_under 2>&1 | tail -15` → exit 0 · Ran 12 tests in 15.6s (1 classes, 16 at a time; slowest: BenchUnder 15s) / OK [ran] [tree 57c254444890] [world 2f1906870a] (2026-11-02T20:01:33Z)
- (step 1) `python3 plugin/tests/run.py test_bench_under 2>&1 | tail -15` → exit 0 · Ran 12 tests in 15.6s (1 classes, 16 at a time; slowest: BenchUnder 15s) / OK [ran] [tree 57c254444890] [world 2f1906870a] (2026-11-02T20:01:33Z)
- (step 2) `python3 plugin/tests/run.py test_bench_under` → exit 0 · Ran 12 tests in 14.6s (1 classes, 16 at a time; slowest: BenchUnder 14s) / OK [ran] [tree 57c254444890] [world 2f1906870a] (2026-11-02T20:01:50Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_bench_under test_board_verbs test_cli test_guard_cases test_paused test_robustness test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [20.78s] [ran] [tree 57c254444890] [world 2f1906870a] (2026-11-02T20:02:52Z)
- (ac 1) `python3 plugin/tests/run.py test_bench_under 2>&1 | grep -E "^(FAIL|ERROR|AssertionError)" | head -5` → ✗ exit 1 · FAILED (failures=1) / FAILED (1 classes: test_bench_under.BenchUnder) [ran] [tree 87a84700f3de] [world 2f1906870a] (2026-11-02T20:10:47Z)
- (step 2) `python3 plugin/tests/run.py test_bench_under test_evidence_quality` → exit 0 · Ran 23 tests in 6.4s (5 classes, 16 at a time; slowest: Bench 6s, BenchUnder 3s, Assume 2s) / OK [ran] [tree 497d54e26342] [world 2f1906870a] (2026-11-02T20:11:25Z)
- (step 3) `grep -q 'is now a pass/fail proof' CHANGELOG.md` → exit 0 · (no output) [ran] [tree 497d54e26342] [world 2f1906870a] (2026-11-02T20:11:26Z)
- (ac 1) `python3 plugin/tests/run.py test_bench_under` → exit 0 · Ran 4 tests in 5.1s (1 classes, 16 at a time; slowest: BenchUnder 5s) / OK [ran] [tree 497d54e26342] [world 2f1906870a] (2026-11-02T20:11:33Z)
- (audit edge) `self: read the builder diff; --under validates nan/inf/0 and needs --bench; only the current tree's median decides; found and fixed in review that a failed bench lacked the ✗ exit mark (red test showed its step checked off), and stopped the test re-running Bench's 9 inherited tests` → a failing bench command now leaves its step open and is re-run at finish (tested); --under 0 and --under without --bench are usage errors (tested) [tree 497d54e26342] (2026-11-02T20:11:33Z)
- (audit self) `self: read the builder diff; --under validates nan/inf/0 and needs --bench; only the current tree's median decides; found and fixed in review that a failed bench lacked the ✗ exit mark (red test showed its step checked off), and stopped the test re-running Bench's 9 inherited tests` → no findings [tree 497d54e26342] (2026-11-02T20:11:33Z)
## Log
- 2026-11-02T19:21:26Z created
- 2026-11-02T20:00:13Z planned from capture
- 2026-11-02T20:00:18Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2651.builder.md
- 2026-11-02T20:00:31Z focused
- 2026-11-02T20:00:32Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T20:10:26Z merged worktree-agent-a77fb917d4ac70ee1 (2 file(s))
- 2026-11-02T20:10:27Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a77fb917d4ac70ee1
- 2026-11-02T20:10:27Z focused
- 2026-11-02T20:12:12Z done
- 2026-11-02T20:12:14Z committed 647ec357 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2638 [FEATURE M, dropped, 0 steps] fm prove --coverage: report which changed hunks the proof command actually executed…
- T-2637 [FEATURE M, dropped, 0 steps] fm outcomes: per proof kind, how often a proven task was later reverted or corrected…
- T-2655 [FEATURE S, active, 3 steps] The drive's end-of-run receipt adds yield per dollar (tasks closed per dollar, dollars per task) beside spend and tokens, and prints …
- decision 2026-11-02: brainstorm-20261102 slate: all 552 ideas grounded into 59 clusters (104 built, 249 partial, 197 new, 2 premise-false); the 24 clusters marked build …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py
## Lessons
- A result string that bypasses c.run_result must carry its '✗ exit N' mark itself: the step and finish gates read only that mark
## Files touched
- plugin/tests/test_bench_under.py
- plugin/lib/fmcli.py
- CHANGELOG.md
