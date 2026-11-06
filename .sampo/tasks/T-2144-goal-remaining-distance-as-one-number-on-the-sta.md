---
id: T-2144
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T10:40:19Z
updated: 2026-10-31T07:02:31Z
inferred_deps: [T-2135]
inferred_why: T-2135: remaining distance counts the ledger's items
base: ad6fc381f06624e866f40c54251ca2b280535dc4
base_tree: 6db54b1165f6254003977d15a0000636dad30974
plan0_at: 2026-10-31T06:54:29Z
plan0_scope: []
verified: strong
---
# Goal remaining distance as one number on the statusline and terminal title (Mission 4…
## Raw request
> Goal remaining distance as one number on the statusline and terminal title (Mission 4 inbox)
## Interpretation
Mission 4's goal ledger (T-2135/T-2139) prints its line in the session context, checkpoints and fm status, but the two glanceable surfaces, the statusline (state.line) and the terminal title (fmhooks.py:249, from badge_text), don't show how far the standing goal is from done, so a person watching a long unattended run can't see it at a glance.
## Assumptions (confidence)
## Acceptance criteria
- [x] while a goal with items stands, state.line ends with 'goal D/N' and the terminal title carries it; with no goal, or a goal that can't be read, both are as today; the statusline script reads no briefs — verify with `python3 plugin/tests/run.py test_goal test_hooks`
## Non-goals
## Approach (options → choice → why)
1) compute goal D/N once where the views are regenerated (regen_views → state_line and badge_text get it from the status data, from fmmandate.progress on the briefs already loaded), so the polled surfaces read a file as today: state.line gains 'goal 3/7' and the title 'foreman · T-0123 … · goal 3/7' while a goal with items stands; 2) compute it inside the statusline script — rejected: a polled surface must not load briefs; 3) a separate goal.line file — rejected: one more file every surface must learn. Choice 1.
## Risks and rollback
A broken goal must never break the views: progress errors give no goal part. Rollback: the part is additive.
## Execution prompt
## Steps
1. [x] red tests: goal D/N in state.line and the title; no goal unchanged; a broken goal unchanged
2. [x] goal count in the status data at regen; state_line and badge_text
3. [x] docs: give MASTER and CHANGELOG lines in the report
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_goal test_hooks` → exit 0 · Ran 247 tests in 38.1s (35 classes, 16 at a time; slowest: Stop 38s, NoTaskGate 27s, PreToolUse 22s) / OK [ran] [tree 10a07cfb031d] (2026-10-31T06:56:35Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_core test_goal && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [16.18s] [ran] [tree 10a07cfb031d] (2026-10-31T06:56:56Z)
- `python3 plugin/tests/run.py test_goal test_hooks test_core` → ✗ exit 1 · Ran 342 tests in 37.6s (57 classes, 16 at a time; slowest: Stop 36s, NoTaskGate 26s, PreToolUse 21s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 7a98e8aa90d1] (2026-10-31T06:59:32Z)
- `python3 plugin/tests/run.py test_goal test_hooks test_core` → exit 0 · Ran 342 tests in 35.6s (57 classes, 16 at a time; slowest: Stop 35s, NoTaskGate 25s, PreToolUse 20s) / OK [ran] [tree 7a98e8aa90d1] (2026-10-31T06:59:32Z)
- (step 1) `python3 plugin/tests/run.py test_goal test_hooks test_core` → exit 0 · Ran 342 tests in 35.6s (57 classes, 16 at a time; slowest: Stop 35s, NoTaskGate 25s, PreToolUse 20s) / OK [ran] [tree 7a98e8aa90d1] (2026-10-31T07:00:07Z)
- (step 2) `python3 plugin/tests/run.py test_goal test_hooks test_core` → exit 0 · Ran 342 tests in 35.7s (57 classes, 16 at a time; slowest: Stop 35s, NoTaskGate 25s, PreToolUse 20s) / OK [ran] [tree 7a98e8aa90d1] (2026-10-31T07:00:43Z)
- (step 3) `python3 plugin/tests/run.py test_goal test_hooks test_core` → exit 0 · Ran 342 tests in 35.6s (57 classes, 16 at a time; slowest: Stop 35s, NoTaskGate 25s, PreToolUse 20s) / OK [ran] [tree 7a98e8aa90d1] (2026-10-31T07:01:19Z)
- (ac 1) `python3 plugin/tests/run.py test_goal test_hooks` → exit 0 · Ran 247 tests in 35.4s (35 classes, 16 at a time; slowest: Stop 35s, NoTaskGate 24s, PreToolUse 19s) / OK [ran] [tree fdeae8e9a9b2] (2026-10-31T07:02:07Z)
- (audit intent) `self-review of the diff: the count is computed at view regen from briefs already loaded; any goal error leaves the line as today; the statusline script and hooks load no briefs` → a person watching an unattended run sees the goal's distance at a glance (test_goal red-to-green) [tree fdeae8e9a9b2] (2026-10-31T07:02:07Z)
- (audit edge) `self-review of the diff: the count is computed at view regen from briefs already loaded; any goal error leaves the line as today; the statusline script and hooks load no briefs` → no goal or a goal without items: unchanged; the title's 80-char cut can drop the suffix on a very long line (noted) [tree fdeae8e9a9b2] (2026-10-31T07:02:07Z)
## Log
- 2026-10-30T10:40:19Z created
- 2026-10-31T06:54:11Z set tier=M
- 2026-10-31T06:54:12Z planned: it has criteria and steps
- 2026-10-31T06:54:13Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2144.builder.md
- 2026-10-31T06:54:28Z focused
- 2026-10-31T06:58:06Z merged worktree-agent-a722fd07d662deba0 (2 file(s))
- 2026-10-31T06:58:06Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a722fd07d662deba0
- 2026-10-31T06:58:17Z focused
- 2026-10-31T07:01:30Z scope: plugin/lib/fmcore.py (_goal_count, state_line, badge_text), plugin/tests/test_goal.py, MASTER.md, CHANGELOG.md
- 2026-10-31T07:02:29Z done
- 2026-10-31T07:02:31Z committed eb5a0858 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2172 [FEATURE S, done, 2 steps] fm exam's surfaces: the exam scorecard isn't an MCP tool (so Desktop can't read it) and… — lesson: Put a new piece of state on the one …
- T-2136 [FEATURE M, done, 3 steps] fm goal plan: a grounded contents list from the user's words, the repo's surfaces and the finish standard; misses learn (Mission 4 brie…
- decision 2026-10-31: [revisited: Mission 4: the goal ledger grows fm mandate] Mission 4 as built: the goal ledger lives on fm mandate's record (one standing goal: text, …
- T-2139 [FEATURE M, done, 3 steps] Goal across days: SessionStart, PreCompact, fm resume and fm run carry the goal line until its verdict is finished (Mission 4 brief 5) …
## Lessons
- Put a polled surface's new number where the file is already written, not where it's read
## Files touched
- plugin/tests/test_goal.py
- plugin/lib/fmcore.py
- CHANGELOG.md
- MASTER.md
