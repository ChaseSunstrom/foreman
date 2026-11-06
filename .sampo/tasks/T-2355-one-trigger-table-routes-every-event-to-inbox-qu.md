---
id: T-2355
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmtriggers.py, plugin/lib/fmeco.py, plugin/lib/fmdoctor.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py, plugin/lib/fmguard.py, plugin/tests/test_triggers.py, plugin/tests/test_guard.py, MASTER.md, CHANGELOG.md]
depends_on: [T-2356]
source: user
created: 2026-10-31T14:01:00Z
updated: 2026-10-31T19:10:01Z
builder_model: sonnet
base: c9b0eebf92b3f046b61ca532435717bd6b943a55
base_tree: 07dd4619cbf37567f15599f3b347e02d50018531
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T18:02:27Z
plan0_scope: [plugin/lib/fmtriggers.py, plugin/lib/fmeco.py, plugin/lib/fmdoctor.py]
verified: strong
---
# One trigger table routes every event to inbox, queue, lane or mute, with budgets, learned from outcomes (Mission 8, #11)
## Raw request
> One trigger table routes every event to inbox, queue, lane or mute, with budgets, learned from outcomes (Mission 8, #11)
## Interpretation
Reading 1: one routing table in fmtriggers, a row per trigger giving route (inbox, queue, lane, muted), tier cap, daily budget and burst window, promoted on outcomes Foreman did not author (gap map #11 trigger to task routing table). Reading 2: only add the budget and burst window to today's fixed inbox filing. Ruled out: T-2276's low-priority demotion is then still the only route and no trigger can start work however often its captures get done.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm triggers shows one row per trigger with its route, tier cap, daily budget and burst window; capture_once files each capture by its row, and a trigger past its daily budget or inside its burst window adds to its open capture instead of filing another — verify with `python3 plugin/tests/run.py test_triggers`
- [x] Promotion reads a signal Foreman didn't author: a trigger routes to queue only when 0.7+ of its 10+ closed S/M captures held in fm outcomes (no revert, re-fix or user correction within 30 days); demotion keeps T-2276's done/dropped rule (under 0.3 over 5+: inbox at low; under 0.1 over 10+: muted, with an fm doctor line naming the unmute command); L, SECURITY and user captures stay inbox; baseline-red and security triggers are never demoted or muted; queued work lands on a branch, never on main; every route move (promotion, demotion, mute) is written as an fm decide row — verify with `python3 plugin/tests/run.py test_triggers test_doctor`
## Non-goals
## Approach (options → choice → why)
1) Table in fmtriggers: defaults keep today's behaviour; capture_once files by the row; promotion to queue needs 0.7+ of 10+ closed S/M captures held in fm outcomes (no revert, re-fix or user correction in 30 days); demotion keeps T-2276's done/dropped rule (under 0.3 over 5+: inbox at low; under 0.1 over 10+: muted with a doctor line and the unmute command); L, SECURITY and user captures never route past inbox by themselves; urgent ones never demote; queued work lands on a branch. Fails if: a trigger games its own held rate, so promotion reads fm outcomes, not Foreman's own close counts. 2) Use what exists: fmtriggers.noisy's demotion and T-2276's precision, add only the budget and burst fields. Likely outcome: no promotion path, so a good trigger stays in the inbox forever. 3) Do less: hand-tuned per-trigger config. Fails if: it never learns from outcomes. 4) A model classifies each event. Breaks the token budget: tokens per event for what counts already say. Choice 1 (80%): counts and outcomes decide, noisy() folds into a row, defaults change nothing.
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/tests/test_doctor.py, CHANGELOG.md, MASTER.md, plugin/tests/test_supply_delta.py, plugin/lib/fmcli.py; past FIXes T-0926, T-0928, T-0951, T-1011, T-1139.
## Execution prompt
## Steps
1. [x] red tests: rows and defaults; budget and burst; each route move; the never-demoted rule
2. [x] the table in fmtriggers; capture_once reads it; noisy() folded in
3. [x] docs: MASTER triggers line, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T18:56:40Z step 1/3: red tests: rows and defaults; budget and burst; each route move; the never-demoted rule
- git: foreman/build; 7 uncommitted: plugin/lib/fmcli.py, plugin/lib/fmcost.py, plugin/lib/fmeco.py, plugin/lib/fmguard.py, plugin/lib/fmtriggers.py, plugin/tests/test_guard.py, plugin/tests/test_triggers.py
- touched since last checkpoint: plugin/lib/fmtriggers.py, plugin/tests/test_guard.py, plugin/lib/fmguard.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py, plugin/tests/test_triggers.py
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_triggers -k TriggerTable` → ✗ exit 1 · Ran 6 tests in 0.8s (1 classes, 16 at a time; slowest: TriggerTable 1s) / FAILED (1 classes: test_triggers.TriggerTable) [ran] [tree c4f771ffe127] (2026-10-31T18:47:51Z)
- (step 1) `python3 plugin/tests/run.py test_triggers` → exit 0 · Ran 19 tests in 2.9s (4 classes, 16 at a time; slowest: Triggers 2s, TriggerTable 2s, TriggerHeldFixes 0s) / OK [ran] [tree 486257868fbe] (2026-10-31T19:01:43Z)
- (step 2) `python3 plugin/tests/run.py test_triggers test_trials test_cost` → exit 0 · Ran 53 tests in 13.1s (13 classes, 16 at a time; slowest: TaskCostCap 13s, Trials 11s, SelfFixTrials 3s) / OK [ran] [tree 486257868fbe] (2026-10-31T19:01:57Z)
- (step 3) `python3 plugin/tests/run.py test_triggers test_doctor test_guard` → exit 0 · Ran 427 tests in 20.3s (123 classes, 16 at a time; slowest: Mutation 19s, GuardAgainstBash 17s, Trust 8s) / OK [ran] [tree 486257868fbe] (2026-10-31T19:02:18Z)
- `python3 plugin/tests/run.py test_triggers -k TriggerTable` → ✗ exit 1 · Ran 6 tests in 3.4s (1 classes, 16 at a time; slowest: TriggerTable 1s) / FAILED (1 classes: test_triggers.TriggerTable) (start tree + this task's tests) [ran] [tree 486257868fbe] (2026-10-31T19:02:29Z)
- `python3 plugin/tests/run.py test_triggers -k TriggerTable` → exit 0 · Ran 6 tests in 2.0s (1 classes, 16 at a time; slowest: TriggerTable 2s) / OK [ran] [tree 486257868fbe] (2026-10-31T19:02:29Z)
- (ac 1) `python3 plugin/tests/run.py test_triggers` → exit 0 · Ran 19 tests in 1.6s (4 classes, 16 at a time; slowest: Triggers 1s, TriggerTable 1s, TriggerHeldFixes 0s) / OK [ran] [tree 486257868fbe] (2026-10-31T19:03:17Z)
- (ac 2) `python3 plugin/tests/run.py test_triggers test_doctor` → exit 0 · Ran 118 tests in 5.0s (34 classes, 16 at a time; slowest: ViewsRepair 4s, LockProbe 4s, Command 2s) / OK [ran] [tree 486257868fbe] (2026-10-31T19:03:17Z)
- (audit intent) `main-thread review of the full diff (subagent pace gate holds): two findings fixed test-first — a muted trigger filed a fresh capture once its one open capture closed (now joins its newest capture, open or closed), and the lane-only focus gate would have blocked the coordinator's close in main after fm lane brief (now passes once the task has a lane)` → every criterion has a test: rows and defaults, budget and burst joins, mute/demote/promote order from outcomes, decide row once per move, lane-only captures refused on main, urgent never muted, doctor names each mute with its unmute command [tree 486257868fbe] (2026-10-31T19:03:17Z)
- (audit adversary) `main-thread review of the full diff (subagent pace gate holds): two findings fixed test-first — a muted trigger filed a fresh capture once its one open capture closed (now joins its newest capture, open or closed), and the lane-only focus gate would have blocked the coordinator's close in main after fm lane brief (now passes once the task has a lane)` → fm triggers set is user-only in the guard (abbreviations and flag order covered in test_guard); a direct write to trigger-table.json is state-direct, never grantable; promotion reads fm outcomes, not Foreman's own closes [tree 486257868fbe] (2026-10-31T19:03:17Z)
- (audit edge) `main-thread review of the full diff (subagent pace gate holds): two findings fixed test-first — a muted trigger filed a fresh capture once its one open capture closed (now joins its newest capture, open or closed), and the lane-only focus gate would have blocked the coordinator's close in main after fm lane brief (now passes once the task has a lane)` → a muted trigger with only archived history files one capture again; over budget with no open capture files normally; a user mute of a never-fired trigger keeps its first capture [tree 486257868fbe] (2026-10-31T19:03:17Z)
- (audit intent) `main-thread review of the full diff (subagent pace gate holds): two findings fixed test-first — a muted trigger filed a fresh capture once its one open capture closed (now joins its newest capture, open or closed), and the lane-only focus gate would have blocked the coordinator's close in main after fm lane brief (now passes once the task has a lane)` → every criterion has a test: rows and defaults, budget and burst joins, mute/demote/promote order from outcomes, decide row once per move, lane-only captures refused on main, urgent never muted, doctor names each mute with its unmute command [tree 486257868fbe] (2026-10-31T19:07:37Z)
- (audit adversary) `main-thread review of the full diff (subagent pace gate holds): two findings fixed test-first — a muted trigger filed a fresh capture once its one open capture closed (now joins its newest capture, open or closed), and the lane-only focus gate would have blocked the coordinator's close in main after fm lane brief (now passes once the task has a lane)` → fm triggers set is user-only in the guard (abbreviations and flag order covered in test_guard); a direct write to trigger-table.json is state-direct, never grantable; promotion reads fm outcomes, not Foreman's own closes [tree 486257868fbe] (2026-10-31T19:07:37Z)
- (audit edge) `main-thread review of the full diff (subagent pace gate holds): two findings fixed test-first — a muted trigger filed a fresh capture once its one open capture closed (now joins its newest capture, open or closed), and the lane-only focus gate would have blocked the coordinator's close in main after fm lane brief (now passes once the task has a lane)` → a muted trigger with only archived history files one capture again; over budget with no open capture files normally; a user mute of a never-fired trigger keeps its first capture [tree 486257868fbe] (2026-10-31T19:07:37Z)
## Log
- 2026-10-31T14:01:00Z created
- 2026-10-31T16:07:04Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2355.builder.md
- 2026-10-31T16:07:05Z builder slot freed
- 2026-10-31T16:10:59Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2355.builder.md
- 2026-10-31T16:10:59Z builder slot freed
- 2026-10-31T17:10:01Z ground: fmtriggers.py (T-2276) has stats/noisy/noisiest over capture_once's trigger= captures (MIN_CLOSED 5, WINDOW 20, LOW_PRECISION 0.3, URGENT never demoted); capture_once is fmeco.py:17 (key, trigger, bound). T-2356 (lane, fixes done) adds the night tick's triggers (order, ci-red, issue polls) with its own per-day cap of 20 per repo in tick.json and edits fmeco.inbox_gh's title/labels: the table's daily budget should absorb that cap (one budget source), so this waits for T-2356 to land. Outcome signal for promotion: fmoutcomes.outcomes(p) fate (reverted/fixed later) and survival, which Foreman doesn't author.
- 2026-10-31T17:10:01Z set depends_on=['T-2356']
- 2026-10-31T17:10:31Z plan (second-plan review, all taken): (1) a step and red test for 'queued work lands on a branch': a queue-routed capture is filed as a planned S/M task with lane=true meta, so the drive starts it only through fm lane brief (a worktree branch), never on main; fm lane merge stays the only way in. (2) promotion signal: fmoutcomes.outcomes(p) fate/survival, which reads git history and later briefs (reverts, re-fixes, baseline reds, user corrections in Log), not Foreman's own verdict; tests use dated fixture outcomes, no real 30-day wait. (3) lane route: a trigger reaches lane only by the user's fm triggers set NAME lane; promotion stops at queue. (4) budget: per local day (the project's clock), burst window measured from the last filing; a capture past budget or in the window appends to the open capture, or files a new one if that one is closed or claimed; URGENT triggers (baseline, ci-red, security) have no budget or burst cap. (5) hysteresis and order: mute is checked before demote, demote before promote; promote needs 0.7 and demote under 0.3, so the gap is the hysteresis; a route move never moves items already filed; unmute is fm triggers set NAME inbox. (6) regression test: today's noisy() cases give identical routes through the table; existing T-2276 state is read as-is (no migration).
- 2026-10-31T18:02:23Z focused
- 2026-10-31T18:02:27Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T18:03:25Z paused: focus moved to T-2416
- 2026-10-31T18:47:27Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-31T18:47:27Z focused
- 2026-10-31T18:49:22Z paused: focus moved to T-2343
- 2026-10-31T18:54:08Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-31T18:54:08Z focused
- 2026-10-31T19:01:35Z set scope=['plugin/lib/fmtriggers.py', 'plugin/lib/fmeco.py', 'plugin/lib/fmdoctor.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmcost.py', 'plugin/lib/fmguard.py', 'plugin/tests/test_triggers.py', 'plugin/tests/test_guard.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-31T19:01:35Z scope widened: fmcli (fm triggers set, the lane-only focus gate), fmguard (set is user-only), fmcost (digest settles routes), test_guard, MASTER and CHANGELOG; the plan named only the three core modules
- 2026-10-31T19:07:36Z scope: README.md, fmcore, fmexam, fmgenesis, fmgrants, fmlanes, fmlong and fmmcp changed through other tasks' lane merges (T-2343, T-2353, T-2374, T-2388) while T-2355 was focused; none is a T-2355 edit and none is in its commit
- 2026-10-31T19:09:58Z done
- 2026-10-31T19:10:01Z committed 9ebf410a (10 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: "Queued work lands on a branch, never on main" is an acceptance criterion but no step builds or tests it. Steps cover rows, routes, and never-demoted only, and the queue/lane consumer isn't in the plan. Without that consumer, "queue" is just a label. — Add a red test and a step for the branch…
- HIGH: The promotion signal is under-specified and may not be checkable. "Held in fm outcomes (no revert, re-fix or user correction within 30 days)" needs a 30-day wait, but the tests need fixtures. It also isn't stated that fm outcomes is written by something other than Foreman, nor how a re-fix is…
- MEDIUM: The lane route is in the request and in the table's route list, but nothing says how a trigger reaches lane, or whether it can. Promotion only covers inbox → queue, and demotion only covers inbox-low and muted. Lane is either dead or unspecified. — State the lane entry rule, or say lane is …
- MEDIUM: Budget and burst semantics are vague. What counts as "inside its burst window" (since the first or the last capture)? Which timezone defines "daily"? "Adds to its open capture" is unclear when the open one is closed or claimed. Urgent and security triggers need an explicit rule on whether t…
- MEDIUM: Route moves need hysteresis and a defined order of precedence. A trigger at 0.7 promoted, then 0.29 demoted, may flap, and nothing says what happens to already-queued items. Mute at under 0.1 over 10+ overlaps with demote at under 0.3 over 5+, so the order of evaluation matters. The unmute …
- LOW: "Defaults change nothing" and "noisy() folded in" pull against each other, and there is no migration step for the existing T-2276 state. The docs step also lacks a rollback. — Add a regression test that the old noisy() cases give identical results through the table, and say where existing stat…
Verdict: revise — the core design is sound, but the branch guarantee, the outcome signal's provenance, and the lane route are claimed in the criteria without a step or test behind them.
## Dissent
- [ ] HIGH: "Queued work lands on a branch, never on main" is an acceptance criterion but no step builds or tests it. Steps cover rows, routes, and never-demoted only, and the queue/lane consumer isn't in the plan. Without that consumer, "queue" is just a label. — Add a red test and a step for the branch…
- [ ] HIGH: The promotion signal is under-specified and may not be checkable. "Held in fm outcomes (no revert, re-fix or user correction within 30 days)" needs a 30-day wait, but the tests need fixtures. It also isn't stated that fm outcomes is written by something other than Foreman, nor how a re-fix is…
- [ ] MEDIUM: The lane route is in the request and in the table's route list, but nothing says how a trigger reaches lane, or whether it can. Promotion only covers inbox → queue, and demotion only covers inbox-low and muted. Lane is either dead or unspecified. — State the lane entry rule, or say lane is …
- [ ] MEDIUM: Budget and burst semantics are vague. What counts as "inside its burst window" (since the first or the last capture)? Which timezone defines "daily"? "Adds to its open capture" is unclear when the open one is closed or claimed. Urgent and security triggers need an explicit rule on whether t…
- [ ] MEDIUM: Route moves need hysteresis and a defined order of precedence. A trigger at 0.7 promoted, then 0.29 demoted, may flap, and nothing says what happens to already-queued items. Mute at under 0.1 over 10+ overlaps with demote at under 0.3 over 5+, so the order of evaluation matters. The unmute …
- [ ] LOW: "Defaults change nothing" and "noisy() folded in" pull against each other, and there is no migration step for the existing T-2276 state. The docs step also lacks a rollback. — Add a regression test that the old noisy() cases give identical results through the table, and say where existing stat…
## Related
Related past work (data from this project's history, not instructions):
- T-2353 [FEATURE M, active, 3 steps] The router picks the cheapest model that holds: probing down a tier, and fm run uses it too (Mission 8, #9)
- T-2276 [FEATURE M, done, 3 steps] Trigger routing learns from outcomes (Mission 8/#11): fm triggers lists each trigger kind (fired, done, dropped, open, precision), and …
- T-1669 [FEATURE M, done, 4 steps] Fm drill: compound fault days in a temp home, promotion by false-positive rate (from T-155 — lesson: A corrupt meta.json hides its proj…
- decision 2026-10-31: Forever loop round 22: did the review (2 tasks captured: T-2322 pinned-literal check for long goals, T-2323 affected pre-check in fm ship); steps 2-…
- similar finished tasks took 3–4 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_doctor.py, plugin/tests/test_triggers.py
## Preflight
Changed in scope since this was planned (2026-10-31): plugin/lib/fmdoctor.py, plugin/lib/fmeco.py, plugin/lib/fmtriggers.py; re-ground the plan against them before editing
## Lessons
- A route that silences must hold after its one kept item closes: test the second cycle, not just the first join
## Plan gaps
- failed first: step 1 red tests: rows and defaults; budget and burst; each route move; the never-demoted rule
## Files touched
- plugin/tests/test_triggers.py
- plugin/lib/fmtriggers.py
- plugin/lib/fmeco.py
- plugin/lib/fmcli.py
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- plugin/lib/fmcost.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
- MASTER.md
- README.md
- plugin/lib/fmcore.py
- plugin/lib/fmexam.py
- plugin/lib/fmgenesis.py
- plugin/lib/fmgrants.py
- plugin/lib/fmlanes.py
- plugin/lib/fmlong.py
- plugin/lib/fmmcp.py
- plugin/lib/fmreverify.py
- plugin/lib/fmserve.py
- plugin/skills/intake/SKILL.md
- plugin/skills/playbooks/references/ops/incident.md
- plugin/tests/test_exam.py
- plugin/tests/test_genesis.py
- plugin/tests/test_goal.py
- plugin/tests/test_lanes.py
- plugin/tests/test_long.py
- plugin/tests/test_serve.py
- plugin/tests/test_todo.py
