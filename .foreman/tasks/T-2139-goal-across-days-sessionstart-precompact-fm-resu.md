---
id: T-2139
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2135]
source: user
created: 2026-10-30T10:37:52Z
updated: 2026-10-31T02:41:33Z
inferred_deps: [T-2137]
inferred_why: T-2137: carries the goal verdict across sessions
base: 1b06cdfe7d13a49674c268e56fbc1b0100f41416
base_tree: 4c0b26be16ff3d58ffb56e882391068b69a68a96
plan0_at: 2026-10-31T02:00:40Z
plan0_scope: []
verified: strong
---
# Goal across days: SessionStart, PreCompact, fm resume and fm run carry the goal line until its verdict is finished (Mission 4 brief 5)
## Raw request
> Goal across days: SessionStart, PreCompact, fm resume and fm run carry the goal line until its verdict is finished (Mission 4 brief 5)
## Interpretation
A goal outlives a session: SessionStart, the PreCompact checkpoint and fm resume print one goal line (the goal's text cut short, items done/total, the next item: the lowest-numbered item not done, with its first open task) while a goal stands and isn't finished; fm run, on an empty queue, takes the next item's first open task. One helper in fmmandate (goal_line) is the only source, so every surface prints the same line.
## Assumptions (confidence)
## Acceptance criteria
- [x] a goal set by a past session shows in SessionStart, the PreCompact checkpoint and fm resume with items done/total and the next item; fm run takes the next item's task on an empty queue — verify with `python3 plugin/tests/run.py test_goal test_hooks`
## Non-goals
## Approach (options → choice → why)
Options: (1) one goal_line(p) helper read by each surface (chosen: one source, cheap: meta + briefs, no checks run); (2) each surface formats its own (drifts); (3) a separate goal file (a second store). Choice 1. bench_hooks budget: goal_line must not run checks or git.
## Risks and rollback
## Execution prompt
## Steps
1. [x] goal line helper + SessionStart + PreCompact + fm resume, test-first
2. [x] fm run picks the next item's task; bench_hooks stays under budget
3. [x] docs
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_goal test_hooks 2>&1 | tail -15` → ✗ exit 1 · Ran 230 tests in 64.3s (32 classes, 16 at a time; slowest: Stop 62s, NoTaskGate 43s, PreToolUse 38s) / FAILED (3 classes) [ran] [tree 5b6b6d9c07a8] (2026-10-31T02:02:45Z)
- (step 1) `python3 plugin/tests/run.py test_goal test_mandate test_hooks test_scout 2>&1 | tail -25` → exit 0 · Ran 259 tests in 66.0s (38 classes, 16 at a time; slowest: Stop 65s, NoTaskGate 45s, PreToolUse 40s) / OK [ran] [tree 40a1bcbce61c] (2026-10-31T02:04:04Z)
- (step 2) `python3 plugin/tests/run.py test_goal test_mandate test_hooks test_scout test_close_gates 2>&1 | tail -6` → exit 0 · Ran 276 tests in 37.2s (39 classes, 16 at a time; slowest: Stop 37s, NoTaskGate 28s, PreToolUse 23s) / OK [ran] [tree a7beabbc3435] (2026-10-31T02:16:30Z)
- (step 3) `python3 plugin/tests/run.py test_goal test_mandate test_hooks test_scout test_close_gates 2>&1 | tail -12` → exit 0 · Ran 279 tests in 58.6s (39 classes, 16 at a time; slowest: Stop 58s, NoTaskGate 40s, PreToolUse 34s) / OK [ran] [tree 6f0fefd2bd9a] (2026-10-31T02:31:47Z)
- `python3 plugin/tests/run.py test_goal test_hooks` → ✗ exit 1 · Ran 234 tests in 35.6s (32 classes, 16 at a time; slowest: Stop 34s, NoTaskGate 24s, PreToolUse 19s) / FAILED (3 classes) (start tree + this task's tests) [ran] [tree 3603ca38f013] (2026-10-31T02:37:16Z)
- `python3 plugin/tests/run.py test_goal test_hooks` → exit 0 · Ran 234 tests in 34.6s (32 classes, 16 at a time; slowest: Stop 34s, NoTaskGate 24s, PreToolUse 19s) / OK [ran] [tree 3603ca38f013] (2026-10-31T02:37:16Z)
- (step 1) `python3 plugin/tests/run.py test_goal test_mandate test_hooks test_scout test_close_gates` → exit 0 · Ran 279 tests in 36.3s (39 classes, 16 at a time; slowest: Stop 36s, NoTaskGate 26s, PreToolUse 21s) / OK [ran] [tree 3603ca38f013] (2026-10-31T02:38:15Z)
- (step 2) `python3 plugin/tests/run.py test_goal test_mandate test_hooks test_scout test_close_gates` → exit 0 · Ran 279 tests in 36.3s (39 classes, 16 at a time; slowest: Stop 36s, NoTaskGate 26s, PreToolUse 21s) / OK [ran] [tree 3603ca38f013] (2026-10-31T02:38:51Z)
- (step 3) `python3 plugin/tests/run.py test_goal test_mandate test_hooks test_scout test_close_gates` → exit 0 · Ran 279 tests in 36.3s (39 classes, 16 at a time; slowest: Stop 36s, NoTaskGate 26s, PreToolUse 21s) / OK [ran] [tree 3603ca38f013] (2026-10-31T02:39:28Z)
- (ac 1) `python3 plugin/tests/run.py test_goal test_hooks` → exit 0 · Ran 234 tests in 34.6s (32 classes, 16 at a time; slowest: Stop 34s, NoTaskGate 24s, PreToolUse 19s) / OK [ran] [tree 3603ca38f013] (2026-10-31T02:40:36Z)
- (audit intent) `fm-reviewer five lenses on the branch: changes needed, fixed in 3def9ef2 and b986183e: fm run never adds a task its normal queue excludes (no captured or unplanned work; it only puts the goal's next item's tasks first), fm resume prints one fresh goal line, an item is done only with a done task and none open (one item_state helper shared with T-2137's verdict), goal reads are wrapped so a broken goal never hides the mandate, the goal text stays quoted as data; bench_hooks SessionStart p50 64 ms, PreCompact 36 ms (budget 150); test_goal test_mandate test_hooks test_scout test_close_gates 279 green; red-to-green proven` → a goal set by a past session shows in SessionStart, the PreCompact checkpoint and fm resume with items done/total and the next item; fm run takes that item's planned task first [tree 3603ca38f013] (2026-10-31T02:40:36Z)
- (audit adversary) `fm-reviewer five lenses on the branch: changes needed, fixed in 3def9ef2 and b986183e: fm run never adds a task its normal queue excludes (no captured or unplanned work; it only puts the goal's next item's tasks first), fm resume prints one fresh goal line, an item is done only with a done task and none open (one item_state helper shared with T-2137's verdict), goal reads are wrapped so a broken goal never hides the mandate, the goal text stays quoted as data; bench_hooks SessionStart p50 64 ms, PreCompact 36 ms (budget 150); test_goal test_mandate test_hooks test_scout test_close_gates 279 green; red-to-green proven` → fm run can't be steered onto an unplanned or user-held task by linking it to the goal; the goal text is quoted data [tree 3603ca38f013] (2026-10-31T02:40:36Z)
- (audit edge) `fm-reviewer five lenses on the branch: changes needed, fixed in 3def9ef2 and b986183e: fm run never adds a task its normal queue excludes (no captured or unplanned work; it only puts the goal's next item's tasks first), fm resume prints one fresh goal line, an item is done only with a done task and none open (one item_state helper shared with T-2137's verdict), goal reads are wrapped so a broken goal never hides the mandate, the goal text stays quoted as data; bench_hooks SessionStart p50 64 ms, PreCompact 36 ms (budget 150); test_goal test_mandate test_hooks test_scout test_close_gates 279 green; red-to-green proven` → a stale checkpoint line, dropped-only items, deleted tasks, a damaged goal record [tree 3603ca38f013] (2026-10-31T02:40:36Z)
- (audit operator) `fm-reviewer five lenses on the branch: changes needed, fixed in 3def9ef2 and b986183e: fm run never adds a task its normal queue excludes (no captured or unplanned work; it only puts the goal's next item's tasks first), fm resume prints one fresh goal line, an item is done only with a done task and none open (one item_state helper shared with T-2137's verdict), goal reads are wrapped so a broken goal never hides the mandate, the goal text stays quoted as data; bench_hooks SessionStart p50 64 ms, PreCompact 36 ms (budget 150); test_goal test_mandate test_hooks test_scout test_close_gates 279 green; red-to-green proven` → goal_line reads meta and briefs only; SessionStart p50 64 ms with it [tree 3603ca38f013] (2026-10-31T02:40:36Z)
- (audit maintainer) `fm-reviewer five lenses on the branch: changes needed, fixed in 3def9ef2 and b986183e: fm run never adds a task its normal queue excludes (no captured or unplanned work; it only puts the goal's next item's tasks first), fm resume prints one fresh goal line, an item is done only with a done task and none open (one item_state helper shared with T-2137's verdict), goal reads are wrapped so a broken goal never hides the mandate, the goal text stays quoted as data; bench_hooks SessionStart p50 64 ms, PreCompact 36 ms (budget 150); test_goal test_mandate test_hooks test_scout test_close_gates 279 green; red-to-green proven` → one goal_line and one item_state feed every surface and the verdict [tree 3603ca38f013] (2026-10-31T02:40:36Z)
## Log
- 2026-10-30T10:37:52Z created
- 2026-10-31T02:00:06Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2139.builder.md
- 2026-10-31T02:00:39Z focused
- 2026-10-31T02:36:00Z merged worktree-agent-a9bc2ea32a5fdacc8 (9 file(s))
- 2026-10-31T02:36:05Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9bc2ea32a5fdacc8
- 2026-10-31T02:36:05Z focused
- 2026-10-31T02:40:01Z scope: plugin/lib/fmmandate.py (progress, goal_line, item_state), plugin/lib/fmhooks.py (SessionStart), plugin/lib/fmcore.py (checkpoint), plugin/lib/fmcli.py (cmd_resume), plugin/lib/fmserve.py (_next_runnable), plugin/tests/test_goal.py, plugin/tests/test_hooks.py, MASTER.md, CHANGELOG.md
- 2026-10-31T02:41:33Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2137 [FEATURE M, active, 3 steps] fm goal verdict: finished vs stopped with the stop's cause, deterministic; a done claim on an unfinished goal blocks once at Stop (Mi…
- decision 2026-10-30: [revisit: when plugin/lib/fmmandate.py changes @468614546a50] Mission 4: the goal ledger grows fm mandate (one standing goal per project: text, clau…
- T-2095 [FEATURE M, done, 3 steps] fm genesis step: the tower's next action from its files, resumable after any kill — lesson: A resumable state machine over files has to…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
## Lessons
- A fallback that hands a worker a task must draw from the same filtered list as the main path, or it becomes a way around every filter
## Files touched
- plugin/lib/fmmandate.py
- plugin/tests/test_goal.py
- plugin/tests/test_hooks.py
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- plugin/lib/fmcli.py
- plugin/lib/fmserve.py
- MASTER.md
- bench.out
- CHANGELOG.md
- plugin/lib/fmgenesis.py
- plugin/skills/genesis/SKILL.md
- plugin/tests/test_genesis.py
