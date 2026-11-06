---
id: T-1430
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T20:43:47Z
updated: 2026-10-21T22:32:12Z
base: 22147f53fcc570cbd2bba69c6d2fd735b97d83b3
base_tree: a98c38c174af9595021bc9ccc378866649833580
plan0_at: 2026-10-21T22:28:27Z
plan0_scope: []
verified: strong
---
# The app-opens TUI test checks the screen it rebuilds from the stream, not raw bytes a cell-diff redraw can split
## Raw request
> test_code_tui Command.test_fm_code_alone_on_a_terminal_opens_the_app reads raw bytes, but the screen redraws only changed cells, so a project name sharing a letter with 'Foreman projects' leaves a gap (2 of 6 runs); assert on the rebuilt screen instead (T-1301 builder)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_fm_code_alone_on_a_terminal_opens_the_app asserts on a screen rebuilt from the pty stream (cursor moves and text), so a project name sharing letters with 'Foreman projects' can't hide it; it passes 5 runs in a row — verify with `python3 plugin/tests/run.py test_code_tui.Command`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] a small _screen(stream, rows, cols) in test_code_tui that applies CSI cursor positioning, erase-display and text to a grid; until() waits on the rebuilt screen; 5 runs
## Resume here
## Docs impact
none: test-only
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 102 tests in 18.4s (15 classes, 16 at a time; slowest: Command 18s, Fuzz 14s, Events 6s) / OK [ran] [tree eba25dff074b] (2026-10-21T22:31:24Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui.Command` → exit 0 · Ran 11 tests in 16.7s (1 classes, 16 at a time; slowest: Command 16s) / OK [ran] [tree eba25dff074b] (2026-10-21T22:31:42Z)
- (audit intent) `self: screen() applies CSI cursor positioning, erase-display and printed characters (wide ones fill two cells) to a 34x120 grid, the size the test sets; until() now waits on the rebuilt screen; the assertions read text, so a skipped unchanged cell can't hide a word` → the app-opens test passed 5 of 5 (test_code_tui.Command) [tree eba25dff074b] (2026-10-21T22:31:42Z)
- (audit edge) `self: screen() applies CSI cursor positioning, erase-display and printed characters (wide ones fill two cells) to a 34x120 grid, the size the test sets; until() now waits on the rebuilt screen; the assertions read text, so a skipped unchanged cell can't hide a word` → escapes other than H and 2J are ignored (SGR, cursor show/hide, alternate screen), which is all the renderer emits besides text [tree eba25dff074b] (2026-10-21T22:31:42Z)
- (audit self) `self: screen() applies CSI cursor positioning, erase-display and printed characters (wide ones fill two cells) to a 34x120 grid, the size the test sets; until() now waits on the rebuilt screen; the assertions read text, so a skipped unchanged cell can't hide a word` → no findings [tree eba25dff074b] (2026-10-21T22:31:42Z)
## Log
- 2026-10-21T20:43:47Z created
- 2026-10-21T22:28:25Z planned from capture
- 2026-10-21T22:28:26Z focused
- 2026-10-21T22:32:09Z done
- 2026-10-21T22:32:12Z committed 8e10d221 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1300-review: Verdict: changes needed.** I read the code but couldn't run anything, because this session had no Bash tool. Nothing below was executed, and the …
- research T-1330-review: Verdict:** changes needed. I read the diff and the working-tree code. I ran no tests, because I had no way to run commands. [stale: plugin/lib/fm…
- T-0702 [FEATURE M, dropped, 3 steps] Frontier 02 — Context firewall and cheap reader
- decision 2026-10-21: T-1330 approved by self-critique (full autonomy): the app is views inside fm code tui's existing App; --task works a planned brief with a per-task l…
## Regression test
none: the old raw-byte check failed 2 of 6 runs by chance (a project name sharing a cell with 'Foreman projects'); the screen-model version passed 5 of 5 here
## Why not caught
the raw check passed whenever the random project name didn't overlap the title
## Lessons
- Assert on what a cell-diff renderer shows, never its raw bytes
## Files touched
- plugin/tests/test_code_tui.py
