# Bench gate noise band: calibration (T-1439)

Question: fmbench.pass_band is 2 standard errors of the pass-total difference (observed rates). With 10 cases at
p≈2/3 and 3 runs it is ≈2.4 passes, so a real 2-pass loss can read as noise. How often does each rule catch a loss,
and how often does it cry wolf?

Method: stdlib Monte Carlo (scratchpad bandsim.py, seed 1439, 4,000 trials per cell). A and B each run 10 cases r
times; B's per-case pass chance is p − loss/10 (a uniform drop totalling `loss` passes). The band uses observed rates,
as the code does. Rules: fail below −2 SE (today), fail below −1.64 SE (one-sided 95%), and an "inconclusive"
middle zone between −2 and −1 SE.

| p | runs | loss | fail @2 SE | fail @1.64 SE | inconclusive (1–2 SE) |
|---|---|---|---|---|---|
| 0.50 | 3 | 0 | 0.05 | 0.09 | 0.14 |
| 0.50 | 3 | 2 | 0.50 | 0.60 | 0.28 |
| 0.67 | 3 | 0 | 0.05 | 0.08 | 0.15 |
| 0.67 | 3 | 1 | 0.21 | 0.29 | 0.27 |
| 0.67 | 3 | 2 | 0.49 | 0.60 | 0.28 |
| 0.67 | 3 | 3 | 0.78 | 0.85 | 0.15 |
| 0.67 | 5 | 0 | 0.04 | 0.08 | 0.13 |
| 0.67 | 5 | 2 | 0.61 | 0.71 | 0.26 |
| 0.67 | 10 | 0 | 0.03 | 0.06 | 0.14 |
| 0.67 | 10 | 2 | 0.83 | 0.91 | 0.14 |
| 0.90 | 3 | 0 | 0.05 | 0.10 | 0.18 |
| 0.90 | 3 | 2 | 0.65 | 0.74 | 0.23 |
| 0.90 | 10 | 2 | 0.95 | 0.98 | 0.04 |

(Full 36-row table: scratchpad bandsim.out.)

Findings:
- The 2 SE band is well calibrated for false alarms (3–5% when nothing changed) but weak at 3 runs: a real 2-pass
  loss in 10 cases is caught about half the time (49–65%).
- Switching to 1.64 SE buys ~10 points of detection for ~4 points more false alarms: not worth a gate that blocks.
- An "inconclusive" outcome for −2..−1 SE catches most of the rest: at 3 runs a 2-pass loss is flagged or
  inconclusive 77% of the time (p=2/3), at 10 runs 97%; the price is a rerun on ~14% of unchanged runs.
- More runs is the real lever: 10 runs catch a 2-pass loss 83–95% at the same 3% false-alarm rate.

Recommendation: keep 2 SE as the fail line; add an inconclusive verdict for a loss between 1 and 2 SE that gate and
evolve treat as "not proven better, rerun the differing cases with more runs" rather than a pass; and when either
side has under 5 runs, say so in the gate's output with the detection power it has.
