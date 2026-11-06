---
id: T-1157
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T10:45:53Z
updated: 2026-10-16T11:07:46Z
base: efeb4cd28e1cff7c75a37e0bd1e2447f64153039
base_tree: 95e989653c1409df14203e3fe1b637889c5c96f8
plan0_at: 2026-10-16T10:48:13Z
plan0_scope: []
verified: strong
---
# Add `fm todo`, the list of what only the user can do (pending asks, blocked-on-user tasks,
## Raw request
> FEATURE: Add `fm todo`, the list of what only the user can do (pending asks, blocked-on-user tasks, costly or outward decisions), each with its command, dropping entries when resolved.
> DONE-WHEN: a test with one pending ask and one user-only block prints both with their commands, and after the ask is granted `fm todo` no longer lists it
## Interpretation
One list of what only the user can do right now, so a final report or a returning user sees it in one place: pending fm asks (category and why), tasks blocked on something only the user can grant, decisions recorded as costly or outward that await review, and plugin installs/updates needing their yes. Each line says what to type (a slash command or the prompt they will see). An entry disappears once resolved.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm todo prints a pending ask and a user-only block, each with what to type; after the ask is granted it is gone; with nothing pending it says so in one line — verify with `python3 plugin/tests/run.py test_todo`
## Non-goals
## Approach (options → choice → why)
Options: (a) a new fm todo verb assembling asks.json (fmcli.py ~2726), blocked briefs, fm decide --review records and plugin grant asks; (b) a section in fm status; (c) only the final-report template. Choice: (a); why: the drive's final report and the user can both call it, and it stays testable. Register next to the ask registration in fmcli (tier Everyday or Finding your way).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (test_todo.py): pending ask listed then gone after grant; blocked-on-user task listed; outward decision listed; empty case one line; --json
2. [x] fm todo, reading the existing stores only (no new state)
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_todo` → ✗ exit 1 · Ran 4 tests in 3.9s (1 classes, 16 at a time; slowest: Todo 4s) / FAILED (1 classes) [ran] [tree 8fa34d5d2e35] (2026-10-16T10:48:50Z)
- (step 2) `python3 plugin/tests/run.py test_todo` → exit 0 · Ran 4 tests in 5.1s (1 classes, 16 at a time; slowest: Todo 5s) / OK [ran] [tree 56f6bee9b426] (2026-10-16T10:49:16Z)
- (ac 1) `python3 plugin/tests/run.py test_todo` → exit 0 · Ran 8 tests in 7.5s (1 classes, 16 at a time; slowest: Todo 7s) / OK [ran] [tree 148506ee07cb] (2026-10-16T11:03:29Z)
- `python3 plugin/tests/run.py test_todo test_help` → exit 0 · Ran 13 tests in 8.4s (3 classes, 16 at a time; slowest: Todo 8s, Help 2s, PromptApprovals 2s) / OK [ran] [tree 148506ee07cb] (2026-10-16T11:03:29Z)
- (audit intent) `reviewer: one fm-reviewer pass found 5 issues (reversal marker never written, decisions never clear, expired asks said reply yes, unanswered decide asks missing, user-word regex); builder fixed all test-first; smoke-ran fm todo on this repo` → one place for what only the user can do, each with its command; resolved items vanish [tree 148506ee07cb] (2026-10-16T11:03:29Z)
- (audit adversary) `reviewer: one fm-reviewer pass found 5 issues (reversal marker never written, decisions never clear, expired asks said reply yes, unanswered decide asks missing, user-word regex); builder fixed all test-first; smoke-ran fm todo on this repo` → read-only over existing stores; block reasons are the project's own text, printed not executed [tree 148506ee07cb] (2026-10-16T11:03:29Z)
- (audit edge) `reviewer: one fm-reviewer pass found 5 issues (reversal marker never written, decisions never clear, expired asks said reply yes, unanswered decide asks missing, user-word regex); builder fixed all test-first; smoke-ran fm todo on this repo` → expired ask says ask again; token limit no longer matches; reversed decisions drop; >20 entries collapse to a count [tree 148506ee07cb] (2026-10-16T11:03:29Z)
- (audit operator) `reviewer: one fm-reviewer pass found 5 issues (reversal marker never written, decisions never clear, expired asks said reply yes, unanswered decide asks missing, user-word regex); builder fixed all test-first; smoke-ran fm todo on this repo` → on this repo it lists the 4 user-only blocks and the open outward decision with what to type [tree 148506ee07cb] (2026-10-16T11:03:29Z)
- (audit maintainer) `reviewer: one fm-reviewer pass found 5 issues (reversal marker never written, decisions never clear, expired asks said reply yes, unanswered decide asks missing, user-word regex); builder fixed all test-first; smoke-ran fm todo on this repo` → reuses c._decision_rows/_settled and unanswered_asks rather than new parsers [tree 148506ee07cb] (2026-10-16T11:03:29Z)
## Log
- 2026-10-16T10:45:53Z created
- 2026-10-16T10:47:51Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1157.builder.md
- 2026-10-16T10:48:12Z focused
- 2026-10-16T11:02:55Z merged worktree-agent-aa1e016c97ccd3972 (2 file(s))
- 2026-10-16T11:02:57Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa1e016c97ccd3972
- 2026-10-16T11:02:58Z focused
- 2026-10-16T11:03:12Z scope: MASTER.md and CHANGELOG.md lines
- 2026-10-16T11:07:45Z done
- 2026-10-16T11:07:46Z committed 515ab34 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1155 [FEATURE M, active, 2 steps] Show a return-after-gap summary (`fm away`, also once at session start) of what closed, bl
- research t0036-adversary-recheck: All four call sites correctly updated to the 5-tuple. This confirms the pin plumbs through `_ask_prompt` (dialog) and `_grant_prompted`…
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- decision 2026-10-06: [costly] fm ask grants stay Claude-Code-only on Codex/Gemini/opencode until T-0336 verifies live whether their prompt hooks fire for agent-written s…
- similar past tasks were L: consider --tier L
## Lessons
- a list of things to resolve needs every source to have a resolved state; decisions had none, so a time window stands in
## Plan gaps
- failed first: step 1 Failing tests (test_todo.py): pending ask listed then gone after grant; blocked-on-user task listed…
## Files touched
- plugin/tests/test_todo.py
- plugin/lib/fmcli.py
- MASTER.md
- CHANGELOG.md
