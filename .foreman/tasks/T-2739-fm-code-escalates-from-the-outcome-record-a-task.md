---
id: T-2739
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2742]
source: followup
created: 2026-11-03T00:42:03Z
updated: 2026-11-03T21:39:03Z
base_note: Calibration: this plan states Choice 75% where FEATURE M closes (590) held on the first finish 98% of the time: 23 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-03T00:42:55Z
rival_split: true
group: fm code escalation and run visibility, both T-1207
builder_model: sonnet
base: dc62de549ef23a8db9fecb736f553a68c025b302
base_tree: de40f8b1fdcafc8a4fbc6a039767ce66b05b7db0
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-11-03T21:07:04Z
plan0_scope: []
lane_stop: merged 2026-11-03T21:33:50Z
verified: strong
unproven: [docs]
---
# fm code starts a run on the --escalate model when its own closes of that type and tier keep needing later fixes: each close records the harness that made it, and the outcome record decides
## Raw request
> fm code escalates from the outcome record: a task type and tier whose fm code closes keep needing later fixes start on the --escalate model, instead of only when the user names one (T-1207 round 3)
## Interpretation
Reading 1 (chosen): fm code already escalates within a run (3 fix rounds, then 3 more on --escalate's model, fmcode.py:24), but only when the user names one; T-1207 round 3 asked the outcome record to decide: when fm code's own closes of a type and tier keep needing later fixes, a new run of that kind starts on the escalate model. That needs each close to say which harness made it (calibration bets already carry harness(), fmoutcomes.py:352; task closes don't). Reading 2 (ruled out): escalate mid-run on the first failed verify. Ruled out: that is today's fix-round rule; the outcome record is what the request names.
## Assumptions (confidence)
## Acceptance criteria
- [x] a close records its harness (fm-code under fm code) in the task_done event — verify with `python3 plugin/tests/run.py test_code`
- [x] with 5+ settled fm-code closes of a type and tier and 30%+ of them fixed or reverted later, fm code's plan starts on the configured escalate model and its journal says why; under that, it starts on the base model — verify with `python3 plugin/tests/run.py test_code`
## Non-goals
## Approach (options → choice → why)
1. Record c.harness() in the task_done event's data; in fm code's plan step, read fmoutcomes.outcomes joined to those events for settled (window-done) closes of the planned type and tier made by fm-code; at 5+ with 30%+ fixed later or reverted, start on the configured escalate model (code.toml or the project's escalate option) and journal the numbers. Likely outcome: one field on the close, one function, one journal line. Fails if: no escalate model is configured (then the journal says the record calls for one and none is set).
2. Read harness from calibration bets instead of closes. Likely outcome: the same rule from bet rows. Fails if: tasks without a stated bet (most S) have no row.
3. Use what exists: outcomes() for fates, _survival's window_done for settled, c.harness() for the marker, run.escalate for the model. Likely outcome: no new storage beyond the one event field. Fails if: outcomes() can't tell which harness made a close (hence option 1's field).
4. Do less: print a hint suggesting --escalate. Likely outcome: a human sees it. Fails if: an unattended run has nobody to read it.
Choice 1 on 3 (75%): the doubt is sample size: fm code's own closes here are few, so the rule may stay silent for a long time; the test seeds the record.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests
2. [x] record the harness on the close
3. [x] the outcome-driven start in fm code
4. [x] CHANGELOG
## Resume here
<!-- auto -->
- 2026-11-03T21:37:32Z steps 4/4 done
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: .claude/worktrees/agent-ab7c74bd2ab3fdf1d/plugin/tests/test_code.py, .claude/worktrees/agent-ab7c74bd2ab3fdf1d/plugin/lib/sampo/cli.py, .claude/worktrees/agent-ab7c74bd2ab3fdf1d/plugin/lib/sampo/outcomes.py, .claude/worktrees/agent-ab7c74bd2ab3fdf1d/plugin/lib/sampo/smith.py, .claude/worktrees/agent-ab7c74bd2ab3fdf1d/README.md, /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/directions-v2/12-forge-illustrated/_review/r2/extra2.py, plugin/skills/playbooks/ratchet.json
## Docs impact
README: the Smith line names the escalation
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_code 2>&1 | grep -E "^(FAIL|ERROR|AssertionError)|Error|Ran |FAILED|OK" | head -20` → exit 0 · Ran 463 tests in 87.6s (99 classes, 16 at a time; slowest: Worker 87s, CodeFakes 40s, OutcomeEscalation 32s) / OK [ran] [tree 57ace5e59bce] [world 2f1906870a] (2026-11-03T21:12:54Z)
- (ac 2) `python3 plugin/tests/run.py test_code 2>&1 | grep -E "^(FAIL|ERROR|AssertionError)|Error|Ran |FAILED|OK" | head -20` → exit 0 · Ran 463 tests in 87.6s (99 classes, 16 at a time; slowest: Worker 87s, CodeFakes 40s, OutcomeEscalation 32s) / OK [ran] [tree 57ace5e59bce] [world 2f1906870a] (2026-11-03T21:12:54Z)
- (step 1) `python3 plugin/tests/run.py test_code 2>&1 | grep -E "^(FAIL|ERROR|AssertionError)|Error|Ran |FAILED|OK" | head -20` → exit 0 · Ran 463 tests in 87.6s (99 classes, 16 at a time; slowest: Worker 87s, CodeFakes 40s, OutcomeEscalation 32s) / OK [ran] [tree 57ace5e59bce] [world 2f1906870a] (2026-11-03T21:12:54Z)
- (step 1) `python3 plugin/tests/run.py test_code` → exit 0 · Ran 463 tests in 94.1s (99 classes, 16 at a time; slowest: Worker 94s, CodeFakes 38s, OutcomeEscalation 32s) / OK [ran] [tree 14947903fdc9] [world 2f1906870a] (2026-11-03T21:14:34Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_code test_outcomes && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [12.01s] [ran] [tree c7643344fc8f] [world 2f1906870a] (2026-11-03T21:17:16Z)
- (step 2) `python3 plugin/tests/run.py test_code` → exit 0 · Ran 463 tests in 122.5s (99 classes, 16 at a time; slowest: Worker 122s, CodeFakes 47s, OutcomeEscalation 44s) / OK [ran] [tree c7643344fc8f] [world 2f1906870a] (2026-11-03T21:19:25Z)
- (ac 1) `python3 plugin/tests/run.py test_code` → exit 0 · Ran 463 tests in 84.7s (99 classes, 16 at a time; slowest: Worker 84s, CodeFakes 34s, OutcomeEscalation 23s) / OK [ran] [tree a483dd2ab993] [world 2f1906870a] (2026-11-03T21:36:03Z)
- (ac 2) `python3 plugin/tests/run.py test_code` → exit 0 · Ran 463 tests in 84.7s (99 classes, 16 at a time; slowest: Worker 84s, CodeFakes 34s, OutcomeEscalation 23s) / OK [ran] [tree a483dd2ab993] [world 2f1906870a] (2026-11-03T21:36:03Z)
- (step 3) `python3 plugin/tests/run.py test_code` → exit 0 · Ran 463 tests in 84.7s (99 classes, 16 at a time; slowest: Worker 84s, CodeFakes 34s, OutcomeEscalation 23s) / OK [ran] [tree a483dd2ab993] [world 2f1906870a] (2026-11-03T21:36:03Z)
- (step 4) `python3 plugin/tests/run.py test_code` → exit 0 · Ran 463 tests in 84.7s (99 classes, 16 at a time; slowest: Worker 84s, CodeFakes 34s, OutcomeEscalation 23s) / OK [ran] [tree a483dd2ab993] [world 2f1906870a] (2026-11-03T21:36:03Z)
- (audit intent) `self: read the diff — task_done carries harness=c.harness(); outcomes.harness_record joins each task's last close harness to outcomes() over settled 30-day windows; smith._start_model escalates a fresh run's start at 5+ settled closes with 30%+ fixed later or reverted, journals the numbers, and never fails the run (any error keeps the base model)` → fm code starts on the stronger model when its own closes of that type and tier keep needing later fixes [tree a483dd2ab993] (2026-11-03T21:36:03Z)
- (audit edge) `self: read the diff — task_done carries harness=c.harness(); outcomes.harness_record joins each task's last close harness to outcomes() over settled 30-day windows; smith._start_model escalates a fresh run's start at 5+ settled closes with 30%+ fixed later or reverted, journals the numbers, and never fails the run (any error keeps the base model)` → pre-change closes carry no harness, so the rule waits for five new settled closes; --resume and worker runs don't re-decide; no --escalate set: the journal says the record calls for one [tree a483dd2ab993] (2026-11-03T21:36:03Z)
- (audit adversary) `self: read the diff — task_done carries harness=c.harness(); outcomes.harness_record joins each task's last close harness to outcomes() over settled 30-day windows; smith._start_model escalates a fresh run's start at 5+ settled closes with 30%+ fixed later or reverted, journals the numbers, and never fails the run (any error keeps the base model)` → reads the ledger and briefs only; picks between models the user configured; no new exec or network [tree a483dd2ab993] (2026-11-03T21:36:03Z)
## Log
- 2026-11-03T00:42:03Z created
- 2026-11-03T00:42:31Z planned from capture
- 2026-11-03T00:46:38Z set depends_on=['T-1476']
- 2026-11-03T01:00:24Z set depends_on=['T-2742']
- 2026-11-03T21:06:55Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2739.builder.md
- 2026-11-03T21:07:03Z focused
- 2026-11-03T21:07:04Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-11-03T21:33:50Z merged worktree-agent-ab7c74bd2ab3fdf1d (5 file(s))
- 2026-11-03T21:33:59Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab7c74bd2ab3fdf1d
- 2026-11-03T21:34:07Z focused
- 2026-11-03T21:39:03Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: `fm code` (in `plugin/lib/fmcli.py`) consults the outcome record at start; if the (task type, tier) pair has a history of closed tasks that later needed follow-up fixes, it picks the `--escalate` model as the starting model rather than the default. An explicit user-named model still wins.
- "Closes keep needing later fixes" is a rate threshold over the outcome record: N or more closes, with a reopen or fix-follow-up fraction above X. This is a computed policy in a new function, not a hard-coded rule.
- Narrower reading: only change the existing escalation trigger so it fires from the record in addition to the user flag. The model chosen is the same as today's `--escalate` path, and nothing else changes in tier selection.
- Alternative: escalation applies per task or per session, with "later fixes" meaning linked follow-up tasks (T-xxxx links), not the same task reopened. The join key is then a task-link field, not a status transition.
Approaches:
- Add a pure function, e.g. `escalation_from_outcomes(task_type, tier, records)`, in `plugin/lib/fmcore.py` (or a small new module). It returns the model or None. `fmcli.py`'s `fm code` handler calls it only when no model was named. Test it directly in a new `plugin/tests/test_*.py`.
- Reuse the existing outcome-record reader and writer (find where closes and fixes are recorded, likely `fmcore.py` or a `fmoutcome*` module). Derive "fix after close" from existing records with no schema change, so old data is still usable.
- Make the threshold configurable (config key or constants with a documented default). Print a one-line reason in `fm code` output ("escalated: 4/6 closes of type X/tier Y needed fixes") so the decision is auditable, and record it in the outcome record.
- Resolve the model through the same path as `--escalate` (the flag's resolved value), so there is one source of truth for which model "escalate" means.
Failure modes:
- Precedence bug: record-based escalation overrides a model the user named, or overrides an explicit "no escalate" choice. The `fm code` arg handling in `fmcli.py` must distinguish "unset" from "default".
- Sparse or biased data: with few closes, one fix triggers escalation, and escalated runs then produce fewer fixes, so the signal decays and flaps. A minimum sample size and a time window are needed, and escalated outcomes must be recorded so they are not mixed in unlabeled.
- Wrong join on "later fix": matching fixes to closes by task type and tier alone, or counting fixes unrelated to the closed work, inflates the rate. Existing records may also lack the type or tier fields, so missing keys must be skipped, not treated as a match.
- Hook and gate fallout: `fmhooks.py` or `fmguard.py` may assume the model is chosen only by flag, and `fm doctor` or `fm replay` may flag the changed behaviour. The record read happens on the hot path of `fm code`, so a slow or corrupt record file must degrade to no escalation, and `bench_hooks.py` …
## Dissent
- [x] rival reading: Likeliest: `fm code` (in `plugin/lib/fmcli.py`) consults the outcome record at start; if the (task type, tier) pair has a history of closed tasks that later needed follow-up fixes, it picks the `--escalate` model as the starting model rather than the default. An explicit user-named model still wins. — answered: adopted: the plan's reading 1, in fmcode's plan step
- [x] rival reading: "Closes keep needing later fixes" is a rate threshold over the outcome record: N or more closes, with a reopen or fix-follow-up fraction above X. This is a computed policy in a new function, not a hard-coded rule. — answered: adopted: 5+ settled closes, 30%+ fixed later or reverted, settled meaning window-done (the one-window rule, T-2610)
- [x] rival reading: Narrower reading: only change the existing escalation trigger so it fires from the record in addition to the user flag. The model chosen is the same as today's `--escalate` path, and nothing else changes in tier selection. — answered: adopted: the record adds a trigger beside the user's flag; the flag still wins when given
- [x] rival reading: Alternative: escalation applies per task or per session, with "later fixes" meaning linked follow-up tasks (T-xxxx links), not the same task reopened. The join key is then a task-link field, not a status transition. — answered: ruled out: 'later fixes' is fmoutcomes' fate (a FIX naming the task, or a revert), already per task; per session adds nothing
- [x] rival approach: Add a pure function, e.g. `escalation_from_outcomes(task_type, tier, records)`, in `plugin/lib/fmcore.py` (or a small new module). It returns the model or None. `fmcli.py`'s `fm code` handler calls it only when no model was named. Test it directly in a new `plugin/tests/test_*.py`. — answered: adopted: a pure function over outcomes and the close events, tested with a seeded record
- [x] rival approach: Reuse the existing outcome-record reader and writer (find where closes and fixes are recorded, likely `fmcore.py` or a `fmoutcome*` module). Derive "fix after close" from existing records with no schema change, so old data is still usable. — answered: adopted: fmoutcomes.outcomes and the task_done events, no new store besides the harness field
- [x] rival approach: Make the threshold configurable (config key or constants with a documented default). Print a one-line reason in `fm code` output ("escalated: 4/6 closes of type X/tier Y needed fixes") so the decision is auditable, and record it in the outcome record. — answered: adopted in part: named constants with the numbers in the journal line; no config key until a user asks to tune it
- [x] rival approach: Resolve the model through the same path as `--escalate` (the flag's resolved value), so there is one source of truth for which model "escalate" means. — answered: adopted: the chosen model goes through run.escalate's resolve path (fmcode.py:2575), one source of truth
## Related
Related past work (data from this project's history, not instructions):
- T-2610 [FIX M, done, 3 steps] Calibration reads compare like with like: a close or a task or choice bet counts once its 30-day window finished — lesson: When one read of…
- research mission-20261101-230033.pack: Genesis gen 2, Mission 4: #11 Self-triggering — schedules, file and event triggers, CI and issue watchers, so work starts without …
- research mission-20261101-232038.pack: Genesis gen 2, Mission 5: #2 Exhaustive thinking — fill its 58 empty coverage cells [stale: mods/foreman-ui/tests/foreman-ui.test.…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
## Lessons
- A rule that learns from outcomes must record who made each outcome at the time, or it can never tell its own record apart
## Files touched
- plugin/tests/test_code.py
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/outcomes.py
- plugin/lib/sampo/smith.py
- README.md
- plugin/skills/playbooks/ratchet.json
