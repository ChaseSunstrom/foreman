---
id: T-3353
type: CLEAN
tier: M
status: planned
priority: normal
scope: [plugin/rules/foreman.md, MASTER.md, docs/map/ops-1.md, plugin/agents/fm-builder.md, plugin/agents/fm-reviewer.md, plugin/lib/sampo/lanes.py, plugin/tests/test_lanes.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T05:33:56Z
updated: 2026-11-06T06:58:29Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a879c1c0c29cef328
lane_branch: worktree-agent-a879c1c0c29cef328
base: 63f19d902a1815ca2f5e9fb9433545a642c72f24
base_tree: 1b9837219c451629fdffd9906b71771442a157e6
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T06:25:15Z
plan0_scope: [plugin/rules/foreman.md, MASTER.md, docs/map/ops-1.md, plugin/agents/fm-builder.md, plugin/agents/fm-reviewer.md, plugin/lib/sampo/lanes.py, plugin/tests/test_lanes.py, CHANGELOG.md]
builder_returned: 2026-11-06T06:58:29Z
---
# Tonight's lessons into the prompts every session loads: the operating rules, MASTER.md and its ops map, and the builder and reviewer agent definitions plus the lane brief
## Raw request
> Tonight's lessons into the prompts every session loads: the operating rules, MASTER.md and its ops map, and the builder and reviewer agent definitions plus the lane brief
## Interpretation
Reading 1: add each lesson as a line in the prompt file its reader loads (builder, reviewer, orchestrator). Reading 2: build a new lessons mechanism; ruled out, nothing would load it.
## Assumptions (confidence)
## Acceptance criteria
- [ ] the builder contract (fm-builder.md and the lane brief, kept in step by test_lanes T-1151) says: a red affected check reruns only its failing classes alone and, if they pass alone and touch none of the lane's files, records that run and commits naming them; 'lock busy' (exit 3) means rerun the same command; never pipe a run through tail/grep when its exit code is the evidence; no PYTHON_CPU_COUNT prefix (the slot pool shares CPUs) — verify with `python3 plugin/tests/run.py test_lanes`
- [ ] the operating rules and MASTER.md say: every finished lane gets one review (/foreman:review, or one fm-reviewer) against the integration branch, not main; should-level findings go back to the same builder (SendMessage) before the merge; anything new shown to the user uses the current product name; every fixed list or limit gets asked whether it binds; the reviewer definition says to diff against the base the brief names — verify with `python3 plugin/tests/run.py test_docs test_rules`
- [ ] builder rules 1-9 in fm-builder.md and lane brief in step — verify with `python3 plugin/tests/run.py test_lanes`
## Non-goals
## Approach (options → choice → why)
1) a line each in files already loaded: likely outcome: reaches every reader, fails if lines drift. 2) a new lessons file: fails if nobody loads it. 3) memory only: fails, builders cannot see it. 4) do less: only the rules file; likely outcome: builders miss it. Choice 1 (80%): cheapest, rules file stays terse.
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [x] builder contract lines in fm-builder.md and the lane brief, test_lanes in step
2. [x] rules, MASTER and ops-1 lines for the lead, reviewer base line
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 185 tests in 328.1s (15 jobs, 16 at a time; slowest: Lanes 33s, LaneRecovery 30s, RaceEvidence 13s) / OK (ran] (tree fe25e6586a03] (world 2f1906870a] (2026-11-06T06:31:39Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · (no output) (ran] (tree 6f3a8a3177d7] (world 2f1906870a] (2026-11-06T06:55:44Z)
- (ac 3) `python3 plugin/tests/run.py test_lanes` → exit 0 · (no output) (ran] (tree 6f3a8a3177d7] (world 2f1906870a] (2026-11-06T06:55:44Z)
- (step 2) `python3 plugin/tests/run.py test_lanes` → exit 0 · (no output) (ran] (tree 6f3a8a3177d7] (world 2f1906870a] (2026-11-06T06:55:44Z)
## Log
- 2026-11-06T05:33:56Z created
- 2026-11-06T06:25:12Z focused
- 2026-11-06T06:25:15Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T06:33:17Z focused
- 2026-11-06T06:53:28Z focused
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-3222 [FEATURE L, done, 5 steps] Network and filesystem sandboxing as a Sampo feature: one sampo sandbox verb that turns… — lesson: running the whole suite inside the n…
- decision 2026-11-05: Recommendation: keep the notes as the cold read for these files; the fm*.py aliases point at plugin/lib/sampo, so a session reading them should open…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_agents.py, plugin/tests/test_ambient.py, plugin/tests/test_audit.py, plugin/tests/test_board_export.py, plugin/tests/test_bookkeeping.py, …
## Preflight
Changed in scope since this was planned (2026-11-06): CHANGELOG.md, MASTER.md, docs/map/ops-1.md, plugin/agents/fm-builder.md, plugin/agents/fm-reviewer.md, plugin/rules/foreman.md, plugin/tests/test_lanes.py; re-ground the plan against them before editing
