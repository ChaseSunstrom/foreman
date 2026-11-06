---
id: T-1674
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmwatch.py, plugin/tests/test_ui.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T21:09:34Z
updated: 2026-10-23T03:51:29Z
group: pane safety and width
base: e30400bd12dc571f3c235d2843f7c93fd2634c53
base_tree: 040218261ea233ecd3f2ecfe9b02a2de94ef0b1b
plan0_at: 2026-10-23T03:41:20Z
plan0_scope: [plugin/lib/fmwatch.py, plugin/tests/test_ui.py, CHANGELOG.md]
verified: strong
---
# Foreman-ui pane: a task title or step text holding an escape sequence makes Claude Code re
## Raw request
> foreman-ui pane: a task title or step text holding an escape sequence makes Claude Code refuse the whole pane (a text child holds a control character); clean() the fm ui --json view in hooks/register.tsx, or strip upstream in fm ui
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm ui --json holds no control, format or separator characters in any string, whatever a task title or step holds (newlines kept) — verify with `python3 plugin/tests/run.py test_ui.UiView`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: a title with ESC, OSC, BEL and U+202E
2. [x] clean every string of view() but the watch paths
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- `python3 plugin/tests/run.py test_ui.UiView` → ✗ exit 1 · Ran 16 tests in 89.5s (1 classes, 16 at a time; slowest: UiView 85s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 33d608a1f9ca] (2026-10-23T03:44:07Z)
- `python3 plugin/tests/run.py test_ui.UiView` → ✗ exit 1 · Ran 16 tests in 60.4s (1 classes, 16 at a time; slowest: UiView 57s) / FAILED (1 classes) [ran] [tree 33d608a1f9ca] (2026-10-23T03:44:07Z)
- `python3 plugin/tests/run.py test_ui.UiView` → ✗ exit 1 · Ran 16 tests in 18.6s (1 classes, 16 at a time; slowest: UiView 17s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree c8f8e1b894ee] (2026-10-23T03:46:02Z)
- `python3 plugin/tests/run.py test_ui.UiView` → ✗ exit 1 · Ran 16 tests in 14.4s (1 classes, 16 at a time; slowest: UiView 14s) / FAILED (1 classes) [ran] [tree c8f8e1b894ee] (2026-10-23T03:46:02Z)
- `python3 plugin/tests/run.py test_ui.UiView` → ✗ exit 1 · Ran 16 tests in 34.2s (1 classes, 16 at a time; slowest: UiView 33s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 3949bb3fa4a2] (2026-10-23T03:47:30Z)
- `python3 plugin/tests/run.py test_ui.UiView` → ✗ exit 1 · Ran 16 tests in 16.6s (1 classes, 16 at a time; slowest: UiView 16s) / FAILED (1 classes) [ran] [tree 3949bb3fa4a2] (2026-10-23T03:47:30Z)
- `python3 plugin/tests/run.py test_ui.UiView` → ✗ exit 1 · Ran 17 tests in 16.3s (1 classes, 16 at a time; slowest: UiView 15s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree ac8d9f2031d6] (2026-10-23T03:49:41Z)
- `python3 plugin/tests/run.py test_ui.UiView` → exit 0 · Ran 17 tests in 19.5s (1 classes, 16 at a time; slowest: UiView 19s) / OK [ran] [tree ac8d9f2031d6] (2026-10-23T03:49:41Z)
- (step 1) `python3 plugin/tests/run.py test_ui.UiView` → exit 0 · Ran 17 tests in 17.8s (1 classes, 16 at a time; slowest: UiView 17s) / OK [ran] [tree 72e28a5a5734] (2026-10-23T03:50:05Z)
- (step 2) `python3 plugin/tests/run.py test_ui test_ui_signals test_ui_replay` → exit 0 · Ran 41 tests in 15.3s (12 classes, 16 at a time; slowest: UiView 15s, UiSkills 1s, Run 1s) / OK [ran] [tree 72e28a5a5734] (2026-10-23T03:50:21Z)
- (ac 1) `python3 plugin/tests/run.py test_ui.UiView` → exit 0 · Ran 17 tests in 15.3s (1 classes, 16 at a time; slowest: UiView 15s) / OK [ran] [tree 72e28a5a5734] (2026-10-23T03:50:37Z)
- (ac 1) `python3 plugin/tests/run.py test_ui.UiView` → exit 0 · Ran 17 tests in 15.8s (1 classes, 16 at a time; slowest: UiView 16s) / OK [ran] [tree 72e28a5a5734] (2026-10-23T03:50:59Z)
- (audit adversary) `self: one cleaner on view()'s return, the one place every surface (the foreman-ui mod, fm ui --follow) reads; paths a surface stats or writes (watch, trust_file, root) kept raw; newlines kept; escape sequences removed whole, then plain_lines. Found the reported title/step case already plain()ed upstream (Brief.title, steps), so the net covers the rest: ledger lines, signals, decisions, research asks` → a hand-edited or synced brief, a ledger event or any other string can no longer put a control or bidi character into a pane text child [tree 72e28a5a5734] (2026-10-23T03:50:59Z)
- (audit edge) `self: one cleaner on view()'s return, the one place every surface (the foreman-ui mod, fm ui --follow) reads; paths a surface stats or writes (watch, trust_file, root) kept raw; newlines kept; escape sequences removed whole, then plain_lines. Found the reported title/step case already plain()ed upstream (Brief.title, steps), so the net covers the rest: ledger lines, signals, decisions, research asks` → non-strings (numbers, None, booleans) pass untouched; nested lists and dicts are walked [tree 72e28a5a5734] (2026-10-23T03:50:59Z)
- (audit self) `self: one cleaner on view()'s return, the one place every surface (the foreman-ui mod, fm ui --follow) reads; paths a surface stats or writes (watch, trust_file, root) kept raw; newlines kept; escape sequences removed whole, then plain_lines. Found the reported title/step case already plain()ed upstream (Brief.title, steps), so the net covers the rest: ledger lines, signals, decisions, research asks` → no findings [tree 72e28a5a5734] (2026-10-23T03:50:59Z)
## Log
- 2026-10-22T21:09:34Z created
- 2026-10-23T03:34:20Z set scope=['plugin/lib/fmwatch.py', 'plugin/tests/test_ui.py', 'CHANGELOG.md']
- 2026-10-23T03:41:19Z focused
- 2026-10-23T03:51:28Z done
- 2026-10-23T03:51:29Z committed 6c426be0 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- research T-1534-review: Verdict:** changes needed (one MEDIUM, easy to fix). The data-not-code question comes out clean.
- T-0144 [SECURITY L, done, 3 steps] Guard: leave out only real top-level fm --run arguments from the interpreter claude-check (a fake --run in a heredoc or -c body hid co…
- decision 2026-10-21: Accept foreman-ui's supply entry after T-1434 named its hooks module
- similar past tasks were L: consider --tier L
- similar finished tasks took 3–5 steps
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md; re-ground the plan against them before editing
## Why not caught
the view's contract test used plain titles only; nothing walked every string of the view
## Lessons
- Clean a view model once at its boundary, not field by field
## Files touched
- plugin/tests/test_ui.py
- plugin/lib/fmwatch.py
- CHANGELOG.md
