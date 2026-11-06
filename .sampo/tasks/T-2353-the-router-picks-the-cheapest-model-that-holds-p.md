---
id: T-2353
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmlanes.py, plugin/lib/fmserve.py, plugin/lib/fmcli.py, plugin/lib/fmlong.py, plugin/tests/test_lanes.py, plugin/tests/test_serve.py, MASTER.md]
depends_on: []
source: user
created: 2026-10-31T14:00:58Z
updated: 2026-10-31T18:41:20Z
builder_model: sonnet
base: b1492842a3690b6bc565dcec36eb91361fb83385
base_tree: 8528302c62d9a43e48be85ce2041e7518b1cf90e
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T17:35:09Z
plan0_scope: [plugin/lib/fmlanes.py, plugin/lib/fmserve.py]
lane_stop: merged 2026-10-31T18:29:13Z
verified: strong
---
# The router picks the cheapest model that holds: probing down a tier, and fm run uses it too (Mission 8, #9)
## Raw request
> The router picks the cheapest model that holds: probing down a tier, and fm run uses it too (Mission 8, #9)
## Interpretation
Reading 1: T-2291's route learns downward as well as upward: it probes one model cheaper on a labelled sample of lanes and promotes the cheaper model when its rework rate holds, and fm run with no --models uses the same route (gap map #9 cheapest model that can do each part). Reading 2: only fix fm run's default to the cheapest model and leave lanes on today's escalate-on-rework. Ruled out: that leaves S lanes that would hold on haiku paying sonnet forever, the very cost named.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lane brief's route considers haiku, sonnet and opus: with the pick's rework 0.1 or less over 5+ lanes of a tier, every 5th lane of that tier is a probe one model down, labelled on the brief; 5+ probes reworking within 0.1 of the dearer model make the cheaper one the pick; a probe reworked or red after merge puts the next lane back up — verify with `python3 plugin/tests/run.py test_lanes`
- [x] Every promotion of a cheaper model, and every revert, is written as an fm decide row and recorded as provisional (shown on fm lane brief's line) until the end-of-run long-horizon tier confirms it; one revert step (a flag on fm lane brief, no new verb) restores the dearer picks made since a given date — verify with `python3 plugin/tests/run.py test_lanes`
- [x] fm run with no --models and none kept routes each session's model by the same per-tier rule and prints it; --models still wins — verify with `python3 plugin/tests/run.py test_serve`
## Non-goals
## Approach (options → choice → why)
1) Probe-down route: models rank haiku < sonnet < opus; where the pick's rework rate over 5+ lanes of a tier is 0.1 or less, every 5th lane is a labelled probe one model down; the cheaper model becomes the pick when its 5+ probes rework within 0.1 of the dearer one; a reworked or red-after-merge probe sends the next lane back up; each promotion is provisional until the end-of-run long-horizon tier confirms it, with one revert step; fm run with no --models uses the route. Fails if: probes are too few to separate models, so 5+ probes and the 0.1 band gate every promotion. 2) Use what exists: T-2291's route as it is, extended only so fm run reads its pick. Likely outcome: no downward learning, so every S lane stays on sonnet. 3) Do less: a fixed model table by tier. Fails if: it never learns and goes stale with each model release. 4) A bandit over task features. Fails if: 20-lane histories are too thin for it to beat the rework-rate rule. Choice 1 (80%): it is the smallest rule that can find a cheaper model that holds and can be undone.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmcli.py, plugin/tests/test_lanes.py, plugin/tests/test_builder.py, MASTER.md; past FIXes T-0968, T-1127, T-1136, T-1196, T-1685.
## Execution prompt
## Steps
1. [x] red tests: probe every 5th lane; promotion after 5 good probes; demotion on one bad probe; fm run default
2. [x] probe-down route in fmlanes; fm run's default from it
3. [x] docs: MASTER router line, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T17:40:31Z step 1/3: red tests: probe every 5th lane; promotion after 5 good probes; demotion on one bad probe; fm run default
- git: worktree-agent-a855e1119292d21ce; 3 uncommitted: plugin/lib/fmlanes.py, plugin/tests/test_lanes.py, plugin/tests/test_serve.py
- touched since last checkpoint: plugin/tests/test_lanes.py, plugin/tests/test_serve.py, plugin/lib/fmlanes.py
## Docs impact
CHANGELOG.md, MASTER.md (builder)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes` → ✗ exit 1 · Ran 135 tests in 31.9s (12 classes, 16 at a time; slowest: LaneRecovery 31s, Lanes 29s, RaceEvidence 24s) / FAILED (2 classes: test_lanes.ProbeDown, test_lanes.ProbeProvisional) [ran] [tree 1e4fe011e634] (2026-10-31T17:40:22Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -30` → ✗ exit 1 · Ran 135 tests in 29.2s (12 classes, 16 at a time; slowest: LaneRecovery 29s, Lanes 26s, RaceEvidence 18s) / FAILED (1 classes: test_lanes.ProbeProvisional) [ran] [tree b319e9b7317d] (2026-10-31T17:44:24Z)
- (ac 2) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -30` → ✗ exit 1 · Ran 135 tests in 29.2s (12 classes, 16 at a time; slowest: LaneRecovery 29s, Lanes 26s, RaceEvidence 18s) / FAILED (1 classes: test_lanes.ProbeProvisional) [ran] [tree b319e9b7317d] (2026-10-31T17:44:24Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -30` → exit 0 · Ran 135 tests in 45.1s (12 classes, 16 at a time; slowest: Lanes 45s, LaneRecovery 43s, RaceEvidence 33s) / OK [ran] [tree d82912072de2] (2026-10-31T17:45:28Z)
- (ac 2) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -30` → exit 0 · Ran 135 tests in 45.1s (12 classes, 16 at a time; slowest: Lanes 45s, LaneRecovery 43s, RaceEvidence 33s) / OK [ran] [tree d82912072de2] (2026-10-31T17:45:28Z)
- (ac 3) `python3 plugin/tests/run.py test_serve 2>&1 | tail -30` → exit 0 · Ran 36 tests in 23.7s (7 classes, 16 at a time; slowest: Run 23s, RunRoute 12s, Serve 4s) / OK [ran] [tree 1b7a0b1a9ded] (2026-10-31T17:46:19Z)
- (step 2) `python3 plugin/tests/run.py test_lanes test_serve test_outcomes` → exit 0 · Ran 223 tests in 42.0s (32 classes, 16 at a time; slowest: LaneRecovery 42s, Lanes 41s, Survival 33s) / OK [ran] [tree 1b7a0b1a9ded] (2026-10-31T17:47:04Z)
- (step 3) `grep -c T-2353 MASTER.md` → exit 0 · 1 [ran] [tree 02c9855b477f] (2026-10-31T17:47:09Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_builder test_cli test_docs test_guard_cases test_lanes test_long test_parallel test_paused test_robustness test_serve test_unattended test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.83s] [ran] [tree 02c9855b477f] (2026-10-31T17:48:12Z)
- (step 1) `python3 plugin/tests/run.py test_lanes test_serve test_outcomes test_long` → exit 0 · Ran 267 tests in 35.3s (39 classes, 16 at a time; slowest: Long 35s, LaneRecovery 24s, Lanes 19s) / OK [ran] [tree 797c16baf5f0] (2026-10-31T18:38:59Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 135 tests in 25.4s (12 classes, 16 at a time; slowest: LaneRecovery 25s, Lanes 21s, RaceEvidence 13s) / OK [ran] [tree 46012385ddd3] (2026-10-31T18:39:47Z)
- (ac 2) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 135 tests in 25.4s (12 classes, 16 at a time; slowest: LaneRecovery 25s, Lanes 21s, RaceEvidence 13s) / OK [ran] [tree 46012385ddd3] (2026-10-31T18:39:47Z)
- (ac 3) `python3 plugin/tests/run.py test_serve` → exit 0 · Ran 36 tests in 20.3s (7 classes, 16 at a time; slowest: Run 20s, RunRoute 11s, Serve 4s) / OK [ran] [tree 46012385ddd3] (2026-10-31T18:39:47Z)
- (audit intent) `coordinator review in the main thread (pace gate held subagents): intent, adversary, edge, operator; approve, one gap captured (T-2434)` → probes one model down on a stable fifth of lanes; promotion provisional with a decide row; fm run routes the same way [tree 46012385ddd3] (2026-10-31T18:39:47Z)
- (audit edge) `coordinator review in the main thread (pace gate held subagents): intent, adversary, edge, operator; approve, one gap captured (T-2434)` → one reworked probe at n=5 blocks promotion; a revert pauses probing 20 lanes; corrupt route.json reads as the base rule [tree 46012385ddd3] (2026-10-31T18:39:47Z)
- (audit operator) `coordinator review in the main thread (pace gate held subagents): intent, adversary, edge, operator; approve, one gap captured (T-2434)` → transitions under the lock write one decide row per change [tree 46012385ddd3] (2026-10-31T18:39:47Z)
## Log
- 2026-10-31T14:00:58Z created
- 2026-10-31T16:07:00Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2353.builder.md
- 2026-10-31T16:07:01Z builder slot freed
- 2026-10-31T16:10:57Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2353.builder.md
- 2026-10-31T16:10:58Z builder slot freed
- 2026-10-31T16:50:49Z ground: T-2291's route is fmlanes.model_route(p, tier) (sonnet unless sonnet's rework over the last 20 lane-built closes of the tier is 0.3+ above opus's, 5+ each); rework = fmoutcomes fate reverted/fixed later, survival lost, or a baseline red naming it; builder_model is on each brief. fm run's per-tier models: fmserve.py:688 (--models, else the kept --save choice, else Claude Code's default). Probes: every 5th lane of a tier one model down when the pick's rework <= 0.1 over 5+; promotion after 5+ probes within 0.1; provisional until the end-of-run long tier.
- 2026-10-31T16:59:44Z plan (second-plan review, all taken): (1) provisional state lives in the project's route.json (per tier: pick, since, provisional, evidence); fm lane brief's line shows '(provisional since D)'; a step hooks fm exam long's run summary: a long run whose goals in that tier pass at least as often as the last run before the promotion confirms it, otherwise it reverts (fm decide row either way). (2) statistics pinned: one-sided, cheaper's probe rework rate <= the pick's rate + 0.1, n >= 5 probes; at n=5 that means no reworked probe unless the pick itself reworks; the window is the last 10 probes. (3) probe selection: a stable hash of the task id mod 5 == 0, not arrival order, so lane size doesn't line up with probes. (4) a reworked or red-after-merge probe (fmoutcomes fate reverted/fixed later, survival lost, a baseline red naming it) sends the next lane back up and restarts the probe streak; history is kept. (5) red tests split by criterion (ProbeDown, ProbeProvisional, RunRoute) and cover --models precedence, no kept choice, per-session routing and the printed line. (6) off switch: fm lane brief --revert-route DATE restores the dearer picks made since DATE and pauses probing for the next 20 lanes of each tier.
- 2026-10-31T17:34:57Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2353.builder.md
- 2026-10-31T17:35:08Z focused
- 2026-10-31T17:35:09Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T17:38:35Z set scope=['plugin/lib/fmlanes.py', 'plugin/lib/fmserve.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmlong.py', 'plugin/tests/test_lanes.py', 'plugin/tests/test_serve.py', 'MASTER.md']
- 2026-10-31T18:29:13Z merged worktree-agent-a855e1119292d21ce (7 file(s))
- 2026-10-31T18:38:10Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a855e1119292d21ce
- 2026-10-31T18:38:10Z focused
- 2026-10-31T18:38:59Z scope: files outside the globs came from the lane merge and the changelog line
- 2026-10-31T18:41:20Z done
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: Criterion 2 requires the "end-of-run long-horizon tier confirms" a provisional promotion, but no step builds or hooks into that confirmation, and the plan doesn't say what the tier emits or how a promotion becomes un-provisional (or reverts if it fails). The provisional state, the `fm decide`…
- HIGH: The statistics are underspecified and likely unsound. "Rework within 0.1 of the dearer model" over only 5 probes has a granularity of 0.2 per event, so a single rework swings the rate by more than the band. Whether "within" is one-sided (cheaper ≤ dearer + 0.1) or two-sided is not stated, nor…
- MEDIUM: Probe selection is "every 5th lane of that tier," which is deterministic, so probes can systematically hit the same kind of lane (e.g. always the biggest or smallest). The comparison then confounds model with lane difficulty. The text also says "labelled sample of lanes" without defining sa…
- MEDIUM: Ambiguity in the demotion rule. "A probe reworked or red after merge puts the next lane back up" is a one-lane reaction, but the probe counter and the cheaper-model stats must still persist. It's unclear whether the failed probe resets the 5-probe count, and "red after merge" needs a signal…
- MEDIUM: Step 1's test list covers only 4 cases (probe cadence, promotion, demotion, fm run default) and omits `--models` precedence, "none kept" (what does "kept" mean for fm run?), per-session routing, and the printed output, all of which are in criterion 3. — Extend the red tests to cover `--mode…
- LOW: Verification of criteria 1 and 2 points to the same `test_lanes` suite, so a pass doesn't distinguish them, and a rollback story for the router itself (disabling probing entirely) isn't offered beyond the date-based revert. — Split tests by criterion name, and consider an off switch so probing…
Verdict: revise — criterion 2 (provisional state, decide rows, long-horizon confirmation, revert flag) has no implementing step, and the promotion statistics at n=5 need to be pinned down before the red tests can b…
## Dissent
- [ ] HIGH: Criterion 2 requires the "end-of-run long-horizon tier confirms" a provisional promotion, but no step builds or hooks into that confirmation, and the plan doesn't say what the tier emits or how a promotion becomes un-provisional (or reverts if it fails). The provisional state, the `fm decide`…
- [ ] HIGH: The statistics are underspecified and likely unsound. "Rework within 0.1 of the dearer model" over only 5 probes has a granularity of 0.2 per event, so a single rework swings the rate by more than the band. Whether "within" is one-sided (cheaper ≤ dearer + 0.1) or two-sided is not stated, nor…
- [ ] MEDIUM: Probe selection is "every 5th lane of that tier," which is deterministic, so probes can systematically hit the same kind of lane (e.g. always the biggest or smallest). The comparison then confounds model with lane difficulty. The text also says "labelled sample of lanes" without defining sa…
- [ ] MEDIUM: Ambiguity in the demotion rule. "A probe reworked or red after merge puts the next lane back up" is a one-lane reaction, but the probe counter and the cheaper-model stats must still persist. It's unclear whether the failed probe resets the 5-probe count, and "red after merge" needs a signal…
- [ ] MEDIUM: Step 1's test list covers only 4 cases (probe cadence, promotion, demotion, fm run default) and omits `--models` precedence, "none kept" (what does "kept" mean for fm run?), per-session routing, and the printed output, all of which are in criterion 3. — Extend the red tests to cover `--mode…
- [ ] LOW: Verification of criteria 1 and 2 points to the same `test_lanes` suite, so a pass doesn't distinguish them, and a rollback story for the router itself (disabling probing entirely) isn't offered beyond the date-based revert. — Split tests by criterion name, and consider an off switch so probing…
## Related
Related past work (data from this project's history, not instructions):
- T-2291 [FEATURE M, done, 3 steps] History-based model router (Mission 8, #9): fm lane brief picks the builder model from how past lanes' tasks held up per tier and model…
- T-2355 [FEATURE M, planned, 3 steps] One trigger table routes every event to inbox, queue, lane or mute, with budgets, learned from outcomes (Mission 8, #11)
- T-0373 [FEATURE M, done, 2 steps] Model routing: subagents on the cheapest model that can do the job; builder lanes on Sonnet for S tasks — lesson: Most of the routing a…
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (seventh): STANDING INTENT] [check: pending T-2191] The user's standing intent (on top of every earlier steer, u…
- similar finished tasks took 2–3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_lanes.py, plugin/tests/test_serve.py
## Preflight
Changed in scope since this was planned (2026-10-31): MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmlanes.py, plugin/lib/fmlong.py, plugin/lib/fmserve.py, plugin/tests/test_lanes.py, plugin/tests/test_serve.py; re-ground the plan against them before editing
## Lessons
- A confirmation step must key on an id both sides share: long-exam goals are scenario ids, not task ids
## Plan gaps
- failed first: step 1 red tests: probe every 5th lane; promotion after 5 good probes; demotion on one bad probe; fm run d…
## Files touched
- plugin/tests/test_lanes.py
- plugin/tests/test_serve.py
- plugin/lib/fmlanes.py
- plugin/lib/fmcli.py
- plugin/lib/fmlong.py
- plugin/lib/fmserve.py
- MASTER.md
- CHANGELOG.md
