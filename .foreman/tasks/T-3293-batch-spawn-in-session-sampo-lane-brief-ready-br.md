---
id: T-3293
type: FEATURE
tier: S
status: active
priority: normal
scope: [plugin/lib/sampo/lanes.py, plugin/tests/test_lanes.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T02:40:04Z
updated: 2026-11-06T04:40:12Z
builder: 2026-11-06T02:40:41Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
lane: ~/.claude/foreman/.claude/worktrees/agent-a8a682a549377d9dd
lane_branch: worktree-agent-a8a682a549377d9dd
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
base_tree: 9eb33fa93e768f0136959dc9b365e08cdaa741eb
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T02:43:02Z
plan0_scope: [plugin/lib/sampo/lanes.py, plugin/tests/test_lanes.py, CHANGELOG.md]
builder_returned: 2026-11-06T04:40:12Z
---
# Batch spawn, in session: sampo lane brief --ready briefs every lane-ready task in one call and prints one block of launch lines
## Raw request
> Batch spawn, in session: sampo lane brief --ready briefs every lane-ready task in one call and prints one block of launch lines
## Interpretation
Reading 1 (chosen): the user asked (2026-11-06) 'why dont you implement a way to batch spawn agents' while the lead was briefing 20+ lanes one sampo lane brief call and one planner at a time. In-session, the lead's cost per lane is a brief command plus an Agent call; the Agent calls already go out in parallel in one message, so the missing piece is briefing every ready task in one command and handing back all launch lines at once. Reading 2 (ruled out): Sampo itself spawns the in-session subagents. Ruled out because only the model can call the Agent tool; Sampo can only prepare the batch (headless spawning is T-3294).
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo lane brief --ready briefs every planned S/M task with closed deps, no open lane and nothing waiting on the user, up to the free builder slots (or --limit N), and prints each task's launch line in one block; tasks it skips are listed with the reason — verify with `python3 plugin/tests/run.py test_lanes`
- [ ] --ready --json returns the briefs and launch lines as a list the lead can turn into parallel Agent calls — verify with `python3 plugin/tests/run.py test_lanes`
## Non-goals
## Approach (options → choice → why)
1. brief --ready loops the existing one-task brief over every ready task and prints one block. Likely outcome: small, reuses every gate the single brief has.
2. A new verb sampo lanes plan. Likely outcome: same logic under a new name; fails if it drifts from brief's gates.
3. Do less: document a shell loop over sampo lane brief. Likely outcome: works, but the lead re-derives the ready list each time.

Choice 1 (88%): one flag on the verb that already holds the rules. Captured: none.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing test: three planned tasks, --ready briefs all three, a fourth with an open dep is skipped with its reason  <- CURRENT
2. [x] brief --ready in lanes.cmd_lane, reusing the one-task brief path
## Resume here
<!-- auto -->
- 2026-11-06T04:32:46Z step 1/2: failing test: three planned tasks, --ready briefs all three, a fourth with an open dep is skipped with its reason
- git: worktree-agent-a8a682a549377d9dd; 2 uncommitted: plugin/lib/sampo/lanes.py, plugin/tests/test_lanes.py
- touched since last checkpoint: plugin/tests/test_lanes.py, plugin/lib/sampo/lanes.py
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_brief_ready test_lanes` → ✗ exit 1 · Ran 1 tests in 8.7s (1 jobs, 16 at a time; slowest: Lanes 6s) / FAILED (1 classes: test_lanes.Lanes) [ran] [tree fcf6d788ded2] [world 2f1906870a] (2026-11-06T02:53:12Z)
- (step 2) `python3 plugin/tests/run.py -k test_brief_ready test_lanes` → exit 0 · Ran 2 tests in 18.6s (2 jobs, 16 at a time; slowest: Lanes.test_brief_ready_honours_limit_never_briefs_twice_and_refuses_misuse 15s, Lanes.test_brief_ready_briefs_every_ready_task_and_skips_the_rest 1 [ran] [tree bee7aa418211] [world 2f1906870a] (2026-11-06T02:58:09Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_doctor test_kalevala test_lane_twins test_lanes test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [153.85s] [ran] [tree bee7aa418211] [world 2f1906870a] (2026-11-06T03:07:39Z)
- (step 2) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py -k test_brief_ready test_lanes` → exit 0 · Ran 2 tests in 30.0s (2 jobs, 2 at a time; slowest: Lanes.test_brief_ready_briefs_every_ready_task_and_skips_the_rest 21s, Lanes.test_brief_ready_honours_limit_never_briefs_twice_and_refuses_misuse 16 [ran] [tree bee7aa418211] [world 2f1906870a] (2026-11-06T03:54:08Z)
## Log
- 2026-11-06T02:40:04Z created
- 2026-11-06T02:40:29Z set scope=['plugin/lib/sampo/lanes.py', 'plugin/tests/test_lanes.py', 'CHANGELOG.md']
- 2026-11-06T02:40:41Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3293.builder.md
- 2026-11-06T02:42:57Z focused
- 2026-11-06T02:43:02Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T02:53:43Z scope widened: plugin/lib/sampo/cli.py gets the --ready and --limit flags of the brief verb (the parser is the only place a flag can live); the rest stays in lanes.py and test_lanes.py
- 2026-11-06T04:34:33Z steer: coordinator item 6 asks for the cli.py max help fix (1-6 stale); cli.py is in scope for that line only
- 2026-11-06T04:34:42Z steer: coordinator item 6 also asks for the --ready pointer in skills/intake/references/delegate.md (step 1)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3294 [FEATURE M, planned, 2 steps] Batch spawn, headless: sampo run --parallel N is a rolling pool up to lane max, not batches of 3 with fully disjoint scopes
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- T-2808 [CLEAN M, done, 3 steps] Agents, plugin and marketplace descriptions, install.sh's messages and the last skill, command and README lines say Sampo (T-2742 step 5)…
- decision 2026-10-31: [costly] Tower filing waits for the user's call on the cold-read rule: Missions 5-8's files and the Mission 3-4 critiques stay unfiled after 4-12 pu…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_lane_twins.py, plugin/tests/test_lanes.py
