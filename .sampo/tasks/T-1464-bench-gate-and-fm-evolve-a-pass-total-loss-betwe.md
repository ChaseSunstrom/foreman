---
id: T-1464
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmbench.py, plugin/tests/test_bench.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T14:51:20Z
updated: 2026-10-22T15:27:09Z
base: 4677d37746a7cb9aee108d9d15c1775039644e4d
base_tree: e0f3042f973ebd1a76195ad86f69855313a729fe
plan0_at: 2026-10-22T15:01:00Z
plan0_scope: [plugin/lib/fmbench.py, plugin/tests/test_bench.py, CHANGELOG.md]
verified: strong
---
# Bench gate calls a 1–2 SE loss inconclusive and names its power
## Raw request
> Bench gate and fm evolve: a pass-total loss between 1 and 2 SE reads 'inconclusive: rerun the differing cases with more runs', not a pass (research bench-band-calibration: at 3 runs a real 2-pass loss in 10 cases is caught 49-65% at 2 SE, 77% with the zone; ~14% of unchanged runs would rerun); and the gate names its detection power when either side has under 5 runs
## Interpretation
Research bench-band-calibration: at 3 runs a real 2-pass loss in 10 cases passes the 2 SE gate about half the time. fmbench.gate treats any loss inside the band as noise (ok).
## Assumptions (confidence)
## Acceptance criteria
- [x] a loss between 1 and 2 SE is not proposed and names a rerun; under 1 SE passes; over 2 SE fails; few runs adds the power line — verify with `cd plugin/tests && python3 -m unittest test_bench.Bench.test_a_loss_between_one_and_two_se_is_inconclusive`
## Non-goals
## Approach (options → choice → why)
In gate(): a pass loss over 1 SE (pband/2) but within 2 SE → ok False with '? fewer passes, likely a loss: rerun <lost cases> with --runs 10 before proposing' (not proposed until rerun); a loss under 1 SE stays noise; a loss over 2 SE stays ✗. When either side's cases ran under 5 times, add one line: 'few runs (N): a real loss of about 2 passes is caught about half the time; --runs 10 for a firmer gate'. fm evolve's _better is unchanged (it already needs a gain beyond the band).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] inconclusive zone and power line in gate()
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- `cd plugin/tests && python3 -m unittest test_bench.Bench.test_a_loss_between_one_and_two_se_is_inconclusive` → ✗ exit 1 · Ran 1 test in 2.326s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 691cbbdf2688] (2026-10-22T15:23:10Z)
- `cd plugin/tests && python3 -m unittest test_bench.Bench.test_a_loss_between_one_and_two_se_is_inconclusive` → exit 0 · Ran 1 test in 2.339s / OK [ran] [tree 691cbbdf2688] (2026-10-22T15:23:10Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_bench.Bench.test_a_loss_between_one_and_two_se_is_inconclusive` → exit 0 · Ran 1 test in 1.813s / OK [ran] [tree 691cbbdf2688] (2026-10-22T15:23:21Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_bench.Bench.test_a_loss_between_one_and_two_se_is_inconclusive` → exit 0 · Ran 1 test in 2.302s / OK [ran] [tree 691cbbdf2688] (2026-10-22T15:23:24Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_bench.Bench.test_a_loss_between_one_and_two_se_is_inconclusive` → exit 0 · Ran 1 test in 2.324s / OK [ran] [tree c3809f0c4511] (2026-10-22T15:25:01Z)
- (audit intent) `builder (sonnet) test-first; red proved with fm task prove; merged; test_bench + test_evolve green; two existing fixtures adjusted (the noise case widened with an identical flip so it stays under 1 SE; the old-results case now asserts the rerun line), not weakened.` → the research's recommendation as built: 2 SE fail line kept, 1–2 SE inconclusive (not proposed), power line under 5 runs [tree c3809f0c4511] (2026-10-22T15:25:01Z)
- (audit edge) `builder (sonnet) test-first; red proved with fm task prove; merged; test_bench + test_evolve green; two existing fixtures adjusted (the noise case widened with an identical flip so it stays under 1 SE; the old-results case now asserts the rerun line), not weakened.` → a zero-variance band stays falsy, so clean 3/3 vs 0/3 takes the plain ✗ path as before; single runs keep their old line [tree c3809f0c4511] (2026-10-22T15:25:01Z)
- (audit self) `builder (sonnet) test-first; red proved with fm task prove; merged; test_bench + test_evolve green; two existing fixtures adjusted (the noise case widened with an identical flip so it stays under 1 SE; the old-results case now asserts the rerun line), not weakened.` → no findings [tree c3809f0c4511] (2026-10-22T15:25:01Z)
## Log
- 2026-10-22T14:51:20Z created
- 2026-10-22T15:00:41Z planned from capture
- 2026-10-22T15:00:47Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1464.builder.md
- 2026-10-22T15:00:59Z focused
- 2026-10-22T15:23:01Z merged worktree-agent-aa9bc912688ec3b6c (2 file(s))
- 2026-10-22T15:23:01Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa9bc912688ec3b6c
- 2026-10-22T15:23:02Z focused
- 2026-10-22T15:27:04Z done
- 2026-10-22T15:27:09Z committed fa212a67 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research bench-band-calibration: Question: fmbench.pass_band is 2 standard errors of the pass-total difference (observed rates). With 10 cases at
- decision 2026-10-22: Recommendation: keep 2 SE as the bench gate's fail line (3-5% false alarms); add an inconclusive verdict for a pass-total loss between 1 and 2 SE th…
- T-1439 [RESEARCH S, done, 2 steps] Calibrate the bench gate's noise band by simulation
- T-1260 [FEATURE M, done, 2 steps] fm bench's gate shows each delta with its noise band from repeated runs, and calls a change inside it noise, not a win or a loss — less…
- similar finished tasks took 2–2 steps
- likely tests for the scope: plugin/tests/test_bench.py
## Files touched
- plugin/tests/test_bench.py
- plugin/lib/fmbench.py
- CHANGELOG.md
