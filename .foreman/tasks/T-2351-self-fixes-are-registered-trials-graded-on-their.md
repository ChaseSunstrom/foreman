---
id: T-2351
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmtrials.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py]
depends_on: []
source: user
created: 2026-10-31T14:00:56Z
updated: 2026-10-31T17:34:30Z
builder_model: sonnet
base: 3deb3dc7acf515c62b16c3a45fd8378c1171f572
base_tree: 9f274d89c499db3950218a1a816d1d6e741c2b84
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T17:23:58Z
plan0_scope: [plugin/lib/fmtrials.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py]
verified: strong
---
# Self-fixes are registered trials, graded on their own key and acted on (Mission 8, #7)
## Raw request
> Self-fixes are registered trials, graded on their own key and acted on (Mission 8, #7)
## Interpretation
Reading 1: gen-0 #7 'trials default + actioned' means every task a trigger filed (recurring failure, did-not-hold, CI red, steer check, capability miss, baseline red) registers a trial at finish, keyed on the trigger's own key, and the digest grades whether that key recurred. Today fmtrials registers only for fm rule add and fm evolve --moves and grades on ledger event rates, so none of these closes with a measure of whether its cause stayed gone. Reading 2: widen fmtrials' existing ledger-rate grade to trigger-filed tasks and stop there. Rejected as the plan: a rate over all ledger events moves with unrelated traffic, so it cannot say a specific signature stayed gone.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task finish on a task a trigger filed registers a trial keyed on its trigger's key, due in 14 days; a user-filed task registers none — verify with `python3 plugin/tests/run.py test_trials`
- [x] A due trial whose key recurred captures one FIX 'Self-fix T-X didn't hold' with the before and after counts and the branch to revert locally; a key with no recurrence is held; a key never seen before the fix is unmeasured, never held — verify with `python3 plugin/tests/run.py test_trials`
- [x] fm trial and the digest list self-fix trials with their verdicts; a held trial counts toward its trigger in fm triggers only once fm outcomes also shows the task held at 30 days (no revert, re-fix or user correction), a signal Foreman did not author — verify with `python3 plugin/tests/run.py test_trials test_triggers`
## Non-goals
## Approach (options → choice → why)
1) Keyed trial: fm task finish on a task whose brief carries the trigger field written at filing registers a trial keyed on the normalised signature stored on the brief, id derived from the task id; due 14 days after the merge to the main tree; the digest grades it held (no recurrence), didn't hold (one FIX with the counts, naming the merge commit and task id when the branch is gone) or unmeasured (the key had no events in the 30 days before the fix's focus, archives included, so never 'held' on no data); held at 30 days is no revert, re-fix or user correction touching the task's files, read from fmoutcomes survival only after day 30. Fails if: the key drifts (signature normalisation changes, a CI job is renamed), which the brief-stored key and the unmeasured label absorb. 2) Use what exists: grade by fmtrials' current ledger event rates, extended to these tasks. Likely outcome: a quiet week reads as held and a busy one as failed, whatever the cause did. 3) Do less: register the trial but only record it, with no digest grade and no FIX. Fails if: nothing is ever actioned, which is the gap this brief closes. 4) Auto-revert a self-fix that didn't hold. Breaks 'local and reversible': an unattended revert on main; the FIX names the branch for a local revert candidate instead. Review points kept from the logged plan review: a step and test for the 30-day held read; re-finishing or re-running the digest never duplicates the trial or resets its due date; older tasks without the trigger field are not trials. Choice 1 (80%): the key's own recurrences are the honest metric, and each review point is a test.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, MASTER.md, plugin/tests/test_cli.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py; past FIXes T-0875, T-0880, T-0908, T-0926, T-0928.
## Execution prompt
## Steps
1. [x] red tests: registration at finish; held, didn't hold, unmeasured; the FIX once; triggers count
2. [x] keyed trials in fmtrials, registration in task finish, the digest grade
3. [x] docs: MASTER, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T17:28:40Z step 3/3: docs: MASTER, CHANGELOG
- git: foreman/build; 6 uncommitted: plugin/lib/fmcli.py, plugin/lib/fmeco.py, plugin/lib/fmtrials.py, plugin/lib/fmtriggers.py, plugin/tests/test_trials.py, plugin/tests/test_triggers.py
- touched since last checkpoint: plugin/tests/test_triggers.py, plugin/lib/fmeco.py, plugin/lib/fmtrials.py, plugin/lib/fmcli.py, plugin/tests/test_trials.py, plugin/lib/fmtriggers.py
## Docs impact
MASTER.md (fmtrials line), CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_trials test_triggers` → ✗ exit 1 · Ran 23 tests in 10.1s (4 classes, 16 at a time; slowest: Trials 10s, Triggers 2s, SelfFixTrials 1s) / FAILED (2 classes: test_trials.SelfFixTrials, test_triggers.TriggerHeldFixes) [ran] [tree 007325d2a2af] (2026-10-31T17:24:31Z)
- (step 2) `python3 plugin/tests/run.py test_trials test_triggers test_recall test_cost` → exit 0 · Ran 77 tests in 15.1s (21 classes, 16 at a time; slowest: Recall 15s, TaskCostCap 8s, Trials 7s) / OK [ran] [tree d5c382f5c290] (2026-10-31T17:27:28Z)
- `python3 plugin/tests/run.py test_trials -k SelfFix` → ✗ exit 1 · Ran 6 tests in 2.4s (1 classes, 16 at a time; slowest: SelfFixTrials 1s) / FAILED (1 classes: test_trials.SelfFixTrials) (start tree + this task's tests) [ran] [tree d5c382f5c290] (2026-10-31T17:27:33Z)
- `python3 plugin/tests/run.py test_trials -k SelfFix` → exit 0 · Ran 6 tests in 1.4s (1 classes, 16 at a time; slowest: SelfFixTrials 1s) / OK [ran] [tree d5c382f5c290] (2026-10-31T17:27:33Z)
- (step 2) `python3 plugin/tests/run.py test_trials test_triggers test_recall test_cost test_foresight` → exit 0 · Ran 93 tests in 13.8s (24 classes, 16 at a time; slowest: Recall 14s, TaskCostCap 7s, Trials 6s) / OK [ran] [tree 523e15fca72d] (2026-10-31T17:33:16Z)
- (step 3) `grep -q T-2351 MASTER.md CHANGELOG.md` → exit 0 · (no output) [ran] [tree 523e15fca72d] (2026-10-31T17:33:16Z)
- (ac 1) `python3 plugin/tests/run.py test_trials` → exit 0 · Ran 14 tests in 6.0s (2 classes, 16 at a time; slowest: Trials 6s, SelfFixTrials 1s) / OK [ran] [tree 523e15fca72d] (2026-10-31T17:33:37Z)
- (ac 2) `python3 plugin/tests/run.py test_trials` → exit 0 · Ran 14 tests in 6.0s (2 classes, 16 at a time; slowest: Trials 6s, SelfFixTrials 1s) / OK [ran] [tree 523e15fca72d] (2026-10-31T17:33:37Z)
- (ac 3) `python3 plugin/tests/run.py test_trials test_triggers` → exit 0 · Ran 26 tests in 6.0s (4 classes, 16 at a time; slowest: Trials 6s, Triggers 1s, SelfFixTrials 1s) / OK [ran] [tree 523e15fca72d] (2026-10-31T17:33:37Z)
- (step 1) `python3 plugin/tests/run.py test_trials test_triggers` → exit 0 · Ran 26 tests in 6.0s (4 classes, 16 at a time; slowest: Trials 6s, Triggers 1s, SelfFixTrials 1s) / OK [ran] [tree 523e15fca72d] (2026-10-31T17:33:37Z)
- (audit intent) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 1 HIGH, 6 MEDIUM, 1 LOW fixed with tests` → signal-filed tasks become trials on their own key at done; held, didn't hold, unmeasured; fixes held only with outcomes survival [tree 523e15fca72d] (2026-10-31T17:33:37Z)
- (audit adversary) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 1 HIGH, 6 MEDIUM, 1 LOW fixed with tests` → the trial's own FIX can't trial itself; listings that repeat each poll aren't recurrences [tree 523e15fca72d] (2026-10-31T17:33:37Z)
- (audit edge) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 1 HIGH, 6 MEDIUM, 1 LOW fixed with tests` → CI keeps one key across runs; keyless captures key on the full first line; a key seen only at filing is unmeasured [tree 523e15fca72d] (2026-10-31T17:33:37Z)
- (audit operator) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 1 HIGH, 6 MEDIUM, 1 LOW fixed with tests` → the digest grades once and stores the verdict; fm trial and fm triggers only read [tree 523e15fca72d] (2026-10-31T17:33:37Z)
## Log
- 2026-10-31T14:00:56Z created
- 2026-10-31T15:07:11Z plan review (fm second, 2026-10-31) to apply when built: (1) add a step and a test for criterion 3: 'held at 30 days' = no revert, re-fix or user correction touching the task's files within 30 days of its close (fmoutcomes survival), read only after day 30; (2) the before-count is the key's events in the 30 days before the fix's focus, read from the ledger archives too; a key first seen after the fix is 'unmeasured'; (3) the after window starts at the merge to the main tree, and the key is the normalised signature the trigger filed it with, stored on the brief at filing; (4) the trial is keyed by task id: re-finishing or re-running the digest never duplicates it or resets its due date; (5) a trigger-filed task is one whose brief carries the trigger field written at filing (older tasks without it are not trials); (6) the FIX names the merge commit and task id when the branch is gone
- 2026-10-31T16:06:54Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2351.builder.md
- 2026-10-31T16:06:55Z builder slot freed
- 2026-10-31T16:10:54Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2351.builder.md
- 2026-10-31T16:10:55Z builder slot freed
- 2026-10-31T17:21:25Z plan (second-plan review, taken): (1) states: registered → due (day 14 after merge: recurrence check graded 'holding') → settled (day 30: fmoutcomes survival 'held' or 'lost'); the trigger count only uses settled trials; (2) anchor: the merge into the main tree (lane_merge event or the finish commit on main); a task finished without a merge registers at its finish commit; reverted before day 14 = settled lost; never merged = not registered; (3) 'unmeasured' = no events of the key in the 30 days before the fix task's first focus event (ledger, archives included via c.ledger_events since=); (4) trigger key: the brief's trigger field, validated against fmtriggers' names; empty/malformed = user-filed; several = one trial per key; (5) idempotency: trial id = task id + key; the FIX-once marker is a trial_fix_filed ledger event checked before filing; test re-finish and digest reruns.
- 2026-10-31T17:23:55Z focused
- 2026-10-31T17:23:58Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T17:27:28Z scope: fmeco.capture_once logs trigger_seen and stores trigger/trigger_key on the brief (the sighting stream the grade reads); fmtriggers shows fixes held; tests in test_trials and test_triggers
- 2026-10-31T17:28:40Z paused: focus moved to T-2340
- 2026-10-31T17:31:42Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-31T17:31:42Z focused
- 2026-10-31T17:33:24Z scope: fmeco (sightings, trial_key), fmci and fmforesight (CI trial keys), fmtriggers (fixes held column), tests in test_trials/test_triggers
- 2026-10-31T17:34:26Z done
- 2026-10-31T17:34:30Z committed 24113316 (11 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The "held at 30 days" check (fmoutcomes survival) conflicts with the 14-day trial due date and has no defined state. Between day 14 and day 30 a trial is graded "held" by recurrence, yet the trigger count must wait for day 30. Step 1 doesn't list tests for that interim state, or for what happ…
- HIGH: The "merge to the main tree" anchor for the due date is undefined for tasks that are never merged, are merged late, or are reverted before day 14. The plan doesn't say when the trial registers, or whether it registers at all, if finish happens without a merge. A trial anchored to finish rathe…
- HIGH: "Unmeasured" is defined as no events in the 30 days before the fix's focus, but the fix's focus is not defined. A key whose only events are very old, or that exist only in archives, may be misclassified. This is the guard against false "held" results, so it must be exact. — Define the baselin…
- MEDIUM: Trigger-filed versus user-filed rests on the brief's trigger field. Briefs that carry the field but a malformed or empty key, tasks whose trigger was edited after filing, and tasks with several triggers are all unspecified. A bad key would yield "unmeasured" forever and make the trial look …
- MEDIUM: Idempotency is stated as a review point, but no step or test names how it is enforced across finish, re-finish and digest re-runs. Deriving the id from the task id handles registration. The FIX "once" requirement needs a persisted marker, and without one a digest re-run after a crash betwee…
- LOW: The FIX tells the user to revert a branch locally. It names the merge commit when the branch is gone, but the plan does not say how a recurrence is judged to come from the fix rather than from a new cause with the same signature. The FIX wording "didn't hold" may overstate. — Phrase the FIX as…
Verdict: revise — the approach is sound, but the merge anchor, the day-14 and day-30 states and the baseline window are undefined, and each of those can cause a false "held". Pin them down and add a test for each b…
## Dissent
- [ ] HIGH: Acceptance criterion 3 requires `fm outcomes` to show the task held at 30 days, but the trial is due at 14 days and the plan has no step for the 30-day outcome check, no definition of how "held at 30 days" is computed (no revert, re-fix, or user correction), and no test for it. The "signal Fo…
- [ ] HIGH: The "unmeasured" rule depends on knowing the before-count of the key, but the plan does not say where the before-count comes from or the window used. If the ledger has rotated or truncated, or if the key was only introduced by this fix's own tracking, "never seen" and "seen but pruned" are in…
- [ ] MEDIUM: The recurrence definition is ambiguous. The "after" window starts at finish, but a recurrence from a branch not yet merged, or an event already in flight at finish time, may be counted as the fix failing. The trigger key may also be unstable (signature normalization changes, CI job renamed)…
- [ ] MEDIUM: Idempotency is only partly covered. "The FIX once" is a step, but it is unclear how re-running the digest, re-finishing a task, or reopening and re-finishing creates duplicates of the trial or the FIX. A re-finish could also reset the 14-day due date. — Make the trial id deterministic (task…
- [ ] MEDIUM: How `fm task finish` knows a task was trigger-filed is not stated. If it relies on a field set at filing, older tasks lack it and user-filed tasks that mimic trigger labels could be misclassified. Different triggers (CI job, rule, missing tool) also have differently shaped keys. — Specify t…
- [ ] LOW: The FIX names "the branch to revert locally", but the plan doesn't say what happens if the branch was deleted or squash-merged, or if the task had no branch. — Fall back to the merge commit or task id in the FIX text, and test the no-branch case.
- [ ] HIGH: The "held at 30 days" check (fmoutcomes survival) conflicts with the 14-day trial due date and has no defined state. Between day 14 and day 30 a trial is graded "held" by recurrence, yet the trigger count must wait for day 30. Step 1 doesn't list tests for that interim state, or for what happ…
- [ ] HIGH: The "merge to the main tree" anchor for the due date is undefined for tasks that are never merged, are merged late, or are reverted before day 14. The plan doesn't say when the trial registers, or whether it registers at all, if finish happens without a merge. A trial anchored to finish rathe…
- [ ] HIGH: "Unmeasured" is defined as no events in the 30 days before the fix's focus, but the fix's focus is not defined. A key whose only events are very old, or that exist only in archives, may be misclassified. This is the guard against false "held" results, so it must be exact. — Define the baselin…
- [ ] MEDIUM: Trigger-filed versus user-filed rests on the brief's trigger field. Briefs that carry the field but a malformed or empty key, tasks whose trigger was edited after filing, and tasks with several triggers are all unspecified. A bad key would yield "unmeasured" forever and make the trial look …
- [ ] MEDIUM: Idempotency is stated as a review point, but no step or test names how it is enforced across finish, re-finish and digest re-runs. Deriving the id from the task id handles registration. The FIX "once" requirement needs a persisted marker, and without one a digest re-run after a crash betwee…
- [ ] LOW: The FIX tells the user to revert a branch locally. It names the merge commit when the branch is gone, but the plan does not say how a recurrence is judged to come from the fix rather than from a new cause with the same signature. The FIX wording "didn't hold" may overstate. — Phrase the FIX as…
## Related
Related past work (data from this project's history, not instructions):
- T-1059 [FEATURE M, done, 3 steps] Every self-change is a pre-registered trial: fm evolve and rule/fix/card changes record th — lesson: A report that runs every day must …
- research T-2337-review: Changes needed.** Two acceptance criteria are not met: no bar check runs at finish, and Foreman's own evidence can still move a bar. I read the c…
- T-2077 [RESEARCH L, blocked, 8 steps] Genesis gen 1: Missions 2-8, critiques, lineage, sweep, gen-2 Seed
- decision 2026-10-31: While the Genesis tower waits on T-2221 (Mission 3's critique; the cold-read rule change is the user's steer-2 call, T-2246), build the gap map's Mi…
- the similar finished task took 3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_cost.py, plugin/tests/test_trials.py
## Preflight
Changed in scope since this was planned (2026-10-31): plugin/lib/fmcli.py, plugin/lib/fmcost.py, plugin/lib/fmtrials.py; re-ground the plan against them before editing
## Lessons
- A trial key must name the failure, not the firing: a run URL or a sha changes every time, so nothing could ever recur
## Plan gaps
- failed first: step 1 red tests: registration at finish; held, didn't hold, unmeasured; the FIX once; triggers count
## Files touched
- plugin/tests/test_trials.py
- plugin/tests/test_triggers.py
- plugin/lib/fmeco.py
- plugin/lib/fmtrials.py
- plugin/lib/fmcli.py
- plugin/lib/fmtriggers.py
- plugin/lib/fmci.py
- plugin/lib/fmcost.py
- plugin/lib/fmforesight.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcore.py
- plugin/lib/fmlanes.py
- plugin/tests/test_lanes.py
- plugin/tests/test_reasoning.py
