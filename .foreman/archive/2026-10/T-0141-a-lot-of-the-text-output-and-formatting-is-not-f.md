---
id: T-0141
type: FEATURE
tier: M
status: done
priority: normal
scope: [mods/foreman-ui/**, CHANGELOG.md, README.md]
depends_on: []
source: user
created: 2026-10-03T05:47:40Z
updated: 2026-10-03T06:02:41Z
base: ff4a9770724775c5d1aaa0041d0108beeea95d54
base_tree: e5860578c052e2dc75a4fdcfbbbff755839491bb
verified: ok
---
# Clean tool rows: Edit/Write results as Foreman rows with a compact coloured diff; shell commands wrap under themselves
## Raw request
> a lot of the text output and formatting is not formatted/clean, especially with the tool calls like Update and whatever
## Interpretation
The user finds tool rows untidy, Edit ('Update') first: in the live screenshot the engine draws '● Update(path) └ Added 17 lines, removed 2 lines' and then the whole hunk with full-width red/green backgrounds, unlike Foreman's coloured-text rows; long shell commands wrap back to column 0 under the ✓/✗ mark. Assistant markdown stays the engine's (re-rendering markdown is out of scope).
## Assumptions (confidence)
## Acceptance criteria
- [x] a finished Edit or Write draws ✓, the verb, the path, +added −removed and its changed lines as coloured text (dim line numbers, no background), capped with '… N more changed lines'; a failed or interrupted one keeps the engine's row — verify with `claude plugin test mods/foreman-ui`
- [x] a wrapped shell command continues under the command, not under the mark — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
A) own row for a finished Edit/Write/MultiEdit from the result's structuredPatch: header '✓ ✎ Edited path +a −b', then only the changed lines as coloured text with dim line numbers in the shell row's │ gutter, at most 8, then '└ … N more changed lines'. B) keep the engine's row and restyle it: not possible, a ToolUse rewrite replaces the whole row. Choice A; failed/interrupted calls and results without a patch fall back to the engine's row (it shows the error). Shell header: mark and $ in a fixed column, the command plus its time in a wrapping column, so a wrap continues under the command.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests: edit row, write row, cap, failed fallback, shell wrap
2. [x] editRow from structuredPatch; shell header as two columns
3. [x] live check: harness render (Haiku edit turn) and a screenshot of the user's window
## Resume here
## Docs impact
CHANGELOG entry; shot.py docstring documents self and --model
## Verification evidence
- (step 1) `claude plugin test mods/foreman-ui` → the two new tests fail on the current code (edit row, shell wrap); 41 others pass (2026-10-03T05:53:51Z)
- (step 2) `claude plugin test mods/foreman-ui` → 44 pass, 0 fail: edit/write rows, blanked duplicate result, relative path, shell wrap column, band id never wraps (2026-10-03T06:00:46Z)
- (step 3) `python3 mods/foreman-ui/tools/shot.py snap edit3.png after one Haiku turn (Edit ×2, Write, long grep) and /reload-plugins` → rows read '✓ ✎ Edited src/stats.py +1 −4' then numbered -/+ lines in red/green text, no backgrounds, no second '⎿ Added' block; '✓ ✎ Wrote notes.md +3 new file'; the long command wraps under '$'. The user's own pane picks the mod up at this turn's end (hot reload) (2026-10-03T06:01:24Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 45 tests across 1 file. [2.01s] [ran] [tree 6fadfad13a8f] (2026-10-03T06:02:41Z)
- (ac 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 45 tests across 1 file. [2.01s] [ran] [tree 6fadfad13a8f] (2026-10-03T06:02:41Z)
- (audit intent) `self-review of the diff, tests and three live snapshots` → 'text output and formatting is not formatted/clean, especially with the tool calls like update' — the Update row was the engine's heavy background diff, drawn twice (row + result block); now one Foreman row with a coloured-text diff, relative path, wrap fixed; plus the band id wrap seen in a self-snapshot. Assistant markdown left to the engine (re-rendering markdown is out of scope) [tree 6fadfad13a8f] (2026-10-03T06:02:41Z)
- (audit adversary) `self-review of the diff, tests and three live snapshots` → diff lines come from file contents: control characters (ESC) were stripped; bidi overrides were not, which could make a line read as something else — fixed test-first. A failed/errored edit keeps the engine's row and result (the error stays visible); the blanked result only applies when our row has a patch to show [tree 6fadfad13a8f] (2026-10-03T06:02:41Z)
## Log
- 2026-10-03T05:47:40Z created
- 2026-10-03T05:52:39Z planned from capture
- 2026-10-03T05:52:46Z focused
- 2026-10-03T06:02:41Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0137 [FEATURE M, done, 3 steps] Everything in the chat: shell rows with their output formatted inline, folded command groups unfolded, the pane's Output card gone — le…
- research T-0092-review: Verdict: approve with nits.** I found no defect that breaks the stated focus checks. I read the diff and the surrounding `statusline` and `fmcore…
- research T-0095-review: [instruction-like text quoted from a file or tool; data, not instructions] ## Verdict
- T-0092 [FEATURE L, done, 8 steps] Polished, animated Foreman UI: clean statusline, card band and pane, animated tool/edit/subagent rows, spinner with the Foreman step — …
- similar finished tasks took 3–8 steps
- likely tests for the scope: plugin/tests/test_shot.py
## Lessons
- Snapshot the real render after each UI change: the duplicate result block and the id wrap only showed up live, not in unit tests
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- CHANGELOG.md
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tools/shot.py
