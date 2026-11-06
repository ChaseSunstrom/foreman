---
id: T-2290
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T07:14:46Z
updated: 2026-10-31T07:33:47Z
base: 6994c7c3aa24b796b87cd8a2e3cba120c07bd4ec
base_tree: 7ab63397637fa6ea63f9cc0ea4dbd4732dc66985
plan0_at: 2026-10-31T07:15:08Z
plan0_scope: []
verified: strong
---
# Foreman predicts and scores (Mission 8, #8/#3): at focus it records its own prediction of active minutes and attempts from closed tasks of the same tier and type, scores it at close, shows per-tier calibration, and notes a task running past 3x its prediction
## Raw request
> Foreman predicts and scores (Mission 8, #8/#3): at focus it records its own prediction of active minutes and attempts from closed tasks of the same tier and type, scores it at close, shows per-tier calibration, and notes a task running past 3x its prediction
## Interpretation
Gap map #8 (calibration feeds thresholds) and #3 (scored predictions): predict_minutes/predict_attempts exist (T-1061) and record_close compares them, but the ledger holds zero predictions because only a session typing fm task set records one, so nothing is ever scored: a capability no session path reaches (steer 3).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm focus records predict_minutes and predict_attempts from the median of the last 30 closed tasks of the same tier and type (none under 5 samples), unless already set; the close records predicted vs actual (fmoutcomes); fm outcomes --calibration prints per tier the median actual/predicted ratio and count; fm next adds one note when a task's active minutes pass 3x its prediction — verify with `python3 plugin/tests/run.py test_outcomes test_cli`
## Non-goals
## Approach (options → choice → why)
1) Foreman predicts at focus from its own history: the median active minutes and attempts of the last 30 closed tasks of the same tier and type (skipped under 5 samples, never overwriting a typed prediction), stored like T-1061's; the close already scores it; fm outcomes --calibration shows per-tier median actual/predicted and n; fm next notes once when active minutes pass 3x the prediction (re-plan, split or ask for fresh eyes). 2) ask the session to predict — rejected: zero recorded so far shows it won't. 3) a model estimate — rejected: tokens per focus, and the history is the better prior. Choice 1.
## Risks and rollback
Focus latency: the prediction reads closed outcomes; it must use the outcomes store (not every brief) and stay fast. Rollback: predictions are metadata; the note is advisory.
## Execution prompt
## Steps
1. [x] red tests: prediction from seeded closes; none under 5; scored at close; calibration table; the 3x note once
2. [x] prediction at focus, the calibration view, the fm next note
3. [x] docs lines in the report
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_outcomes test_cli 2>&1 | tail -25` → ✗ exit 1 · Ran 161 tests in 32.0s (52 classes, 16 at a time; slowest: TaskLifecycle 30s, Survival 22s, StateViews 12s) / FAILED (1 classes) [ran] [tree 5992a49358d3] (2026-10-31T07:17:08Z)
- (step 1) `python3 plugin/tests/run.py test_outcomes test_cli` → exit 0 · Ran 161 tests in 46.7s (52 classes, 16 at a time; slowest: TaskLifecycle 46s, Survival 37s, StateViews 16s) / OK [ran] [tree b0536f599a19] (2026-10-31T07:18:50Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_core test_guard_cases test_outcomes test_paused test_planning && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [21.79s] [ran] [tree b0536f599a19] (2026-10-31T07:20:03Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_guard_cases test_outcomes test_paused test_planning && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [40.79s] [ran] [tree 05d71cebd011] (2026-10-31T07:24:05Z)
- `cd plugin/tests && python3 -m unittest -q test_outcomes` → ✗ exit 1 · Ran 22 tests in 28.356s / FAILED (failures=2, errors=5) (start tree + this task's tests) [ran] [tree e1ef079446e8] (2026-10-31T07:31:03Z)
- `cd plugin/tests && python3 -m unittest -q test_outcomes` → exit 0 · Ran 22 tests in 28.097s / OK [ran] [tree e1ef079446e8] (2026-10-31T07:31:03Z)
- (step 1) `python3 plugin/tests/run.py test_outcomes test_cli` → exit 0 · Ran 164 tests in 20.7s (53 classes, 16 at a time; slowest: TaskLifecycle 20s, Survival 14s, ModelRouter 9s) / OK [ran] [tree e1ef079446e8] (2026-10-31T07:31:24Z)
- (step 2) `python3 plugin/tests/run.py test_outcomes test_cli` → exit 0 · Ran 164 tests in 20.5s (53 classes, 16 at a time; slowest: TaskLifecycle 20s, Survival 14s, ModelRouter 9s) / OK [ran] [tree e1ef079446e8] (2026-10-31T07:31:45Z)
- (step 3) `python3 plugin/tests/run.py test_outcomes test_cli` → exit 0 · Ran 164 tests in 20.6s (53 classes, 16 at a time; slowest: TaskLifecycle 20s, Survival 14s, ModelRouter 9s) / OK [ran] [tree e1ef079446e8] (2026-10-31T07:32:06Z)
- (ac 1) `python3 plugin/tests/run.py test_outcomes test_cli` → exit 0 · Ran 164 tests in 20.5s (53 classes, 16 at a time; slowest: TaskLifecycle 20s, Survival 14s, StateViews 9s) / OK [ran] [tree e1ef079446e8] (2026-10-31T07:32:27Z)
- (audit intent) `self-review plus one follow-up: backfill on first use (this project yields 0 rows: old closes logged no minutes, so predictions start after 5 new closes per tier and type), and the overrun note shown once per task` → steer 3: predictions now come from a real session path (focus), so calibration has data (test_outcomes red-to-green) [tree e1ef079446e8] (2026-10-31T07:32:27Z)
- (audit edge) `self-review plus one follow-up: backfill on first use (this project yields 0 rows: old closes logged no minutes, so predictions start after 5 new closes per tier and type), and the overrun note shown once per task` → under 5 samples no prediction; a typed prediction is never overwritten; the note lives in fm next only so hooks can't spend it [tree e1ef079446e8] (2026-10-31T07:32:27Z)
- (audit operator) `self-review plus one follow-up: backfill on first use (this project yields 0 rows: old closes logged no minutes, so predictions start after 5 new closes per tier and type), and the overrun note shown once per task` → predict reads closes.jsonl only (~1 ms on 500 rows), never all briefs [tree e1ef079446e8] (2026-10-31T07:32:27Z)
## Log
- 2026-10-31T07:14:46Z created
- 2026-10-31T07:14:55Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2290.builder.md
- 2026-10-31T07:15:08Z focused
- 2026-10-31T07:25:45Z merged worktree-agent-ab59b84de6906aec4 (3 file(s))
- 2026-10-31T07:27:30Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab59b84de6906aec4
- 2026-10-31T07:30:06Z focused
- 2026-10-31T07:32:06Z scope: plugin/lib/fmoutcomes.py (closes.jsonl, predict, calibration_report, overrun_note, _backfill), plugin/lib/fmcli.py (focus prediction, cmd_next note, outcomes --calibration), plugin/tests/test_outcomes.py, MASTER.md, CHANGELOG.md
- 2026-10-31T07:33:47Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1061 [FEATURE M, done, 2 steps] Calibration ledger: a plan predicts its size (files touched, minutes, attempts); the close — lesson: A self-regulating gate needs one r…
- research draft-mission-genesis-gen1: Task: T-2093 (brief 1, fm genesis check), T-2095 (brief 2, fm genesis step), T-2099 (brief 3, fm genesis draft/spec), T-2102 (brief …
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
- decision 2026-10-30: [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] Long-horizon tier is the deciding end-of-run score for every ca…
## Lessons
- A capability with zero recorded uses in the ledger is a capability no session reaches: check the ledger before building on it
## Files touched
- plugin/tests/test_outcomes.py
- plugin/lib/fmoutcomes.py
- .fm-scratch/e.json
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- .fm-scratch/perf.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmbudget.py
- plugin/lib/fmexam.py
- plugin/lib/fmlanes.py
- plugin/lib/fmlong.py
- plugin/tests/test_builder.py
- plugin/tests/test_exam.py
- plugin/tests/test_lanes.py
- plugin/tests/test_long.py
