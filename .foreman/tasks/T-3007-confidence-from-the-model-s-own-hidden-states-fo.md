---
id: T-3007
type: RESEARCH
tier: M
status: blocked
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T19:26:31Z
updated: 2026-11-05T04:44:09Z
---
# Confidence from a local model's hidden states: a linear probe on one layer's activations at each Smith turn predicts whether the turn's check will pass, measured on held-out exam scenarios
## Raw request
> Confidence from the model's own hidden states: for each open-weight local model (Qwen3.5 4B/9B, Gemma 4 12B via their HF weights on /models/hf), record one layer's activations at each Smith turn on exam scenarios, label turns by whether the step held (tests, verify, later revert), train a linear probe per model, and serve its calibrated score to the reasoning layer's budget (think more, check, or stop) in place of self-reported confidence; measured by calibration (Brier, AUC) on held-out scenarios against the model's stated confidence (T-3005)
## Interpretation
Reading 1 (chosen): for the open-weight models whose HF weights sit under /models/hf (Qwen3.5 4B and 9B, Gemma 4 12B), replay recorded Smith turns through transformers, record one middle layer's last-token activation per turn, label each turn by its check's outcome (labels from outcomes only), fit a logistic probe per model, and report held-out AUC by scenario family against the model's stated confidence; if a probe beats it by 0.05+ AUC, wire it as the deliberate-turn trigger T-3006's state arm reads. Reading 2: ask the model for its confidence; rejected, stated confidence is what T-3006 already reads and it is poorly calibrated.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a probe per model is fit on recorded Smith turns labelled only by their checks' outcomes, and its held-out AUC (by scenario family, never a turn's own scenario) beside the stated confidence's is in research — verify with `test -f ~/.claude/foreman/state/projects/foreman-4a056f/research/T-3007-hidden-state-probe.md`
- [ ] a decision row: the probe is wired as T-3006's deliberate-turn trigger only if it beats stated confidence by 0.05 AUC held out; otherwise recorded as not yet — verify with `grep -q T-3007 ~/.claude/foreman/state/projects/foreman-4a056f/decisions.md`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: the exam's Smith journals for turns and outcomes, the GPU and HF weights already on /models/hf, scikit-learn if installed else a numpy logistic fit; likely outcome: an AUC table per model, one decision. 2. Do less: probe one model; fails if: a single model's result can't say the method generalises. 3. Fine-tune a confidence head; fails if: it needs far more labelled turns than the journals hold. Choice 1 (65%)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] export turns and outcomes from the exam journals  <- CURRENT
2. [ ] activations per model on the GPU (one model at a time, the GPU share rule)
3. [ ] the probes, the held-out table, the decision
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-04T19:26:31Z created
- 2026-11-05T04:44:08Z planned from capture
- 2026-11-05T04:44:09Z set approved=True
- 2026-11-05T04:44:09Z blocked: approved; needs the GPU free of the moons embedder and Jeff; after T-3010
## Follow-ups captured
