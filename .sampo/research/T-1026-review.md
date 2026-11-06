## intent: changes needed

**MEDIUM** `mods/foreman-ui/hooks/register.tsx:1736-1742` — the Agents bars do not stay in one column when a stop button shows.
- summary: A row with a `■ stop` button puts a button (about 6-8 cells) after the bar, where other rows put the 12-cell status box (`STW`). The bar shifts right by about 4-6 cells.
- short_summary: Stop-button rows misalign the Agents time axis
- failure_scenario: A subagent quiet for 10 minutes or more (`stop` set) sits beside a running one. The two bars no longer share a time axis, so the quiet agent's start and end read wrongly. The column alignment is what this change set out to deliver.
- category: layout-misalignment
- verdict: PLAUSIBLE (I read the Box order and widths, and did not render it)
- fix: wrap the Button in `<Box flexShrink={0} width={STW} justifyContent="flex-end">`.
- reproducer: add a test with a quiet agent and a running agent, then compare the two `gantt-*` Raster x-positions.

**MEDIUM** `register.tsx:1500-1511` — the work-bar row overflows at the real dock width.
- summary: The bar is `workW` = floor(W*0.32) wide, plus every label as a `flexShrink={0}` box. The head column is the dock minus the 11-cell mascot.
- short_summary: Work-bar labels clip, blocked first
- failure_scenario: At 76 columns the head is about 63 cells. With the bar (23) and all five parts present, the row needs about 75 cells. `overflow="hidden"` silently cuts the last labels, and "blocked" comes last. The test uses a wider `bodyColumns: 70` and only checks that the nodes exist.
- category: silent-truncation
- verdict: PLAUSIBLE
- fix: size `workW` from the width left after the labels, or put `blocked` before `inbox`.

**LOW** `register.tsx:1181` — `v.history ?` is true for `[]`.
- summary: `_guarded(...) or []` (`fmwatch.py:674`) turns a `_history` exception into `[]`. The pane then shows an empty History, and `v.recent` is not used as a fallback.
- short_summary: Empty history blocks the `recent` fallback
- failure_scenario: Any malformed ledger event, such as a non-string `ts`, blanks the History pane silently.
- category: silent-failure
- verdict: CONFIRMED
- fix: test `v.history?.length`.

**LOW** `register.tsx:1272` and `register.tsx:1496-1498` — the `sessions` minimum (`min` 3) and the modes moved onto the title line. Neither is in the request or the changelog. The `min` of 5 for agents can starve the queue's approve rows on a short dock.

## adversary: ok
`audit` lens values are validated by `fmcli.py:529`. `allow` is a category list. Titles, decisions and surprises go through `c.plain`. I found no unsanitized sink.

## edge: ok
Only the `[]` case above.

## operator: ok
`marketplace.json` and `plugin.json` both say 0.13.0, and I found no other `0.12.0` outside the changelog. The README matches the code.

## maintainer: changes needed
**LOW** `mods/foreman-ui/types/index.d.ts:616` — `FmHistory` was inserted between the comment "A brainstorm while fm ideas runs…" and `FmBrainstorm`, so the comment now describes the wrong type. Move it.

**LOW** `plugin/tests/test_ui.py:709` — `assertLessEqual(len(h), 60)` passes with 3 events, so the 60-event cap is untested. Seed more than 60 events.

**LOW** `plugin/lib/fmwatch.py:105-133` — `_history` repeats `_recent`'s event-to-mark mapping (`fmwatch.py:77-102`). The two can drift. Have both use one table.

## Acceptance criteria
- Agents tree, time bar per node, History title, gradient dividers: met in code (`register.tsx:1380-1440`, `ruleCells`). The "pane still fills the dock" part is not verifiable here, because I am read-only and cannot run `claude plugin test .`.
- `fm ui --json` with up to 60 events and task titles: met (`_history`, `out[-n:]`). I could not run `test_ui`.

## Implicit decisions
- The "node graph" is a tree of bars, not free-form lines.
- The graph still appears only when there are agents, brainstorms or worktrees.
- `muted` is 0x9aa3b0.
- The status column is a fixed 12 cells.
- The root's bar shows the calls from the last 30 minutes.
- Blocked counts every blocked task.
- History is built from 5000 ledger events.

## Not checked
I ran no tests and rendered no pane. I did not check `claude plugin test .`, how a Button is sized, or `CHANGELOG.md` beyond its first lines.

Noticed: `gather()` (`fmwatch.py:74`) calls `_recent` with no `_guarded`, so one bad ledger line takes down the whole view.
