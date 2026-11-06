---
id: T-3291
type: FEATURE
tier: M
status: planned
priority: normal
scope: [plugin/lib/sampo/kickoff.py, plugin/tests/test_kickoff.py, plugin/lib/sampo/cli.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T02:35:36Z
updated: 2026-11-06T02:36:25Z
builder: 2026-11-06T02:36:25Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
---
# Moon C-000930: 'sampo kickoff ID' dry-runs a task's plan before the first edit: files per step, covering tests, gates, and colliding open lanes on one screen
## Raw request
> Moon C-000930: 'sampo kickoff ID' dry-runs a task's plan before the first edit: files per step, covering tests, gates, and colliding open lanes on one screen
## Interpretation
Reading 1 (chosen): before a task's first edit, one command predicts its path from the brief alone: per step the files and symbols it will touch (scope globs plus paths and def/class names in the step text), the tests map.tests_for links to them, the gates cli.gates names for its type and tier, and the other open tasks or lanes whose scope or steps overlap. Partial: cli.affected (cli.py:5620) maps changed files to tests only after edits, cli.gates (cli.py:3813) prints gates without files, cli._others (cli.py:1778) finds collisions only after edits were touched; T-3278 gatemap, T-3268 lane preview and T-3276 objections are in lanes, unmerged. This composes them per task and never reimplements them. Reading 2 (ruled out): simulating the edit by running code or tests in a sandbox, because it costs CPU (T-3252) and cannot know an edit not yet written.
## Assumptions (confidence)
## Acceptance criteria
- [ ] kickoff.touch(p,b) lists per step the existing files its scope globs and its step text name (paths and def/class symbols grepped in them) — verify with `python3 plugin/tests/run.py test_kickoff`
- [ ] kickoff.collide(p,b) names open tasks (other id, any lane) whose scope or step text overlaps this task's files or symbols, and the tests via map.tests_for plus the gates via cli.gates are included in the report; gatemap.predict and lanes preview are used when importable and skipped silently when not — verify with `python3 plugin/tests/run.py test_kickoff`
- [ ] sampo kickoff ID [--json] prints under 20 lines (steps, tests, gates, collisions, one verdict line) and edits nothing; CHANGELOG has an entry — verify with `python3 plugin/tests/run.py test_kickoff`
## Non-goals
## Approach (options → choice → why)
1. New kickoff.py: pure functions touch, collide, report over the brief, map and open briefs; soft-import gatemap.predict and the lane preview when present; one lazy verb. Likely outcome: one screen before the first edit, one new file, almost no collision with other lanes.
2. Extend cli.cmd_gates to print files and collisions. Likely outcome: small, but cli.py is shared by every lane and gates stays task-agnostic.
3. Run affected tests against a scratch worktree copy of the plan. fails if: there is no edit yet to test and the run loads the CPU on every kickoff.
4. Do less: only list scope-overlapping open tasks. Likely outcome: catches collisions but gives no tests or gates.

Choice 1 (86%): cheap, grounded in existing maps, the soft imports let it land before T-3278/3268/3276 merge. Captured: none.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Write failing test_kickoff: temp project, two tasks with overlapping scope, assert touch/collide/report  <- CURRENT
2. [ ] Implement kickoff.py (touch, collide, report) reusing map.tests_for, cli.gates, core.load_briefs
3. [ ] Register lazy verb 'kickoff' in cli.py (one add() line plus argument), CHANGELOG entry
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T02:35:36Z created
- 2026-11-06T02:35:54Z set scope=['plugin/lib/sampo/kickoff.py', 'plugin/tests/test_kickoff.py', 'plugin/lib/sampo/cli.py', 'CHANGELOG.md']
- 2026-11-06T02:36:25Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3291.builder.md
## Follow-ups captured
