---
id: T-1439
type: RESEARCH
tier: S
status: done
priority: normal
scope: [plugin/lib/fmbench.py]
depends_on: []
source: discovered
created: 2026-10-21T21:29:13Z
updated: 2026-10-22T14:51:35Z
base: a4455a05c3690df97f03b929727fb2c682bdbc7a
base_tree: 67da385a2aba9254c316312827edd61dea029bdc
plan0_at: 2026-10-22T14:51:16Z
plan0_scope: [plugin/lib/fmbench.py]
verified: strong
---
# Calibrate the bench gate's noise band by simulation
## Raw request
> bench gate at 3 runs is lenient: across 10 cases at ~2/3 a loss of about 2 passes reads as noise; the band's calibration isn't tested (T-1260 builder)
## Interpretation
pass_band is 2 SE of the pass-total difference. With 10 cases at p≈2/3 and 3 runs each it is ≈2.4 passes, so a real loss of 2 passes reads as noise. Measure, don't guess: false-alarm rate when nothing changed and detection rate for real losses, at 3/5/10 runs, for the current rule and alternatives.
## Assumptions (confidence)
## Acceptance criteria
- [x] a research note with the false-alarm and detection table for each rule and a recommendation — verify with `fm research list | grep -q bench-band-calibration`
## Non-goals
## Approach (options → choice → why)
A stdlib Monte Carlo in the scratchpad (binomial draws per case, 10k trials) over p in {0.5, 2/3, 0.9}, runs {3,5,10}, true loss {0,1,2,3} passes; compare 2 SE two-sided, 1.64 SE one-sided, and an 'inconclusive → rerun the differing cases' middle zone (1–2 SE). Record the table in research; capture the change it argues for.
## Risks and rollback
## Execution prompt
## Steps
1. [x] simulate
2. [x] record findings and capture the follow-up
## Resume here
## Docs impact
research bench-band-calibration
## Verification evidence
- (step 1) `python3 -I /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/bandsim.py` → exit 0 · 0.90    10    2 |     0.95        0.98                 0.04 / 0.90    10    3 |     1.00        1.00                 0.00 [ran] [tree 67da385a2aba] (2026-10-22T14:51:19Z)
- (step 2) `fm research list | grep -q bench-band-calibration` → exit 0 · (no output) [ran] [tree 67da385a2aba] (2026-10-22T14:51:21Z)
- (ac 1) `fm research list | grep -q bench-band-calibration` → exit 0 · (no output) [ran] [tree 67da385a2aba] (2026-10-22T14:51:26Z)
- (audit intent) `self: stdlib Monte Carlo (seed 1439, 4,000 trials/cell) over p {0.5, 2/3, 0.9}, runs {3,5,10}, loss {0..3}; band computed from observed rates as fmbench.pass_band does. Findings and recommendation in research bench-band-calibration; follow-up captured T-1464.` → confirms the capture: at 3 runs a 2-pass loss passes as noise ~half the time; false alarms stay 3-5% [tree 67da385a2aba] (2026-10-22T14:51:26Z)
- (audit edge) `self: stdlib Monte Carlo (seed 1439, 4,000 trials/cell) over p {0.5, 2/3, 0.9}, runs {3,5,10}, loss {0..3}; band computed from observed rates as fmbench.pass_band does. Findings and recommendation in research bench-band-calibration; follow-up captured T-1464.` → uniform per-case drop is one loss model; a loss concentrated in 2 cases has the same expected total, slightly different variance [tree 67da385a2aba] (2026-10-22T14:51:26Z)
- (audit self) `self: stdlib Monte Carlo (seed 1439, 4,000 trials/cell) over p {0.5, 2/3, 0.9}, runs {3,5,10}, loss {0..3}; band computed from observed rates as fmbench.pass_band does. Findings and recommendation in research bench-band-calibration; follow-up captured T-1464.` → no findings [tree 67da385a2aba] (2026-10-22T14:51:26Z)
- (audit intent) `self: stdlib Monte Carlo (seed 1439, 4,000 trials/cell) over p {0.5, 2/3, 0.9}, runs {3,5,10}, loss {0..3}; band computed from observed rates as fmbench.pass_band does. Findings and recommendation in research bench-band-calibration; follow-up captured T-1464.` → confirms the capture: at 3 runs a 2-pass loss passes as noise ~half the time; false alarms stay 3-5% [tree 67da385a2aba] (2026-10-22T14:51:34Z)
- (audit edge) `self: stdlib Monte Carlo (seed 1439, 4,000 trials/cell) over p {0.5, 2/3, 0.9}, runs {3,5,10}, loss {0..3}; band computed from observed rates as fmbench.pass_band does. Findings and recommendation in research bench-band-calibration; follow-up captured T-1464.` → uniform per-case drop is one loss model; a loss concentrated in 2 cases has the same expected total, slightly different variance [tree 67da385a2aba] (2026-10-22T14:51:34Z)
- (audit self) `self: stdlib Monte Carlo (seed 1439, 4,000 trials/cell) over p {0.5, 2/3, 0.9}, runs {3,5,10}, loss {0..3}; band computed from observed rates as fmbench.pass_band does. Findings and recommendation in research bench-band-calibration; follow-up captured T-1464.` → no findings [tree 67da385a2aba] (2026-10-22T14:51:34Z)
## Log
- 2026-10-21T21:29:13Z created
- 2026-10-22T14:50:12Z planned from capture
- 2026-10-22T14:51:15Z focused
- 2026-10-22T14:51:35Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1435 [FIX S, done, 1 steps] fm evolve keeps a candidate only for a win outside the bench noise band, and a result's pass rate is read within 0..1 — lesson: When extrac…
- T-1260 [FEATURE M, done, 2 steps] fm bench's gate shows each delta with its noise band from repeated runs, and calls a change inside it noise, not a win or a loss — less…
- research T-1242-review: Verdict: changes needed.** The acceptance criterion's published result is missing, and per-request passes aren't reported. [stale: plugin/lib/fmb…
- decision 2026-10-15: Recommendation: close the gaps where a small model has to guess a command (done: T-0969, T-0985, T-0986, T-0987); no separate small-model mode or MC…
- likely tests for the scope: plugin/tests/test_bench.py
## Preflight
Changed in scope since this was planned (2026-10-21): plugin/lib/fmbench.py; re-ground the plan against them before editing
## Decision
Recommendation: keep 2 SE as the bench gate's fail line (3-5% false alarms); add an inconclusive verdict for a pass-total loss between 1 and 2 SE that gate and evolve treat as 'rerun the differing cases with more runs', not a pass (T-1464); 1.64 SE rejected (+4 pts false alarms for +10 pts detection). Would change if: suites grow past ~30 cases (the band narrows relative to a 2-pass loss) or runs default to 10 (83-95% detection at 2 SE alone).
