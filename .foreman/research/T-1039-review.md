## intent: changes needed

**HIGH** `mods/foreman-ui/hooks/rows.tsx:578-579, 594-595, 619-621`. The time bars are not in one aligned column.
- file: mods/foreman-ui/hooks/rows.tsx
- line: 594
- summary: Each row's bar is right-anchored, but the cell to its right has a different width on each row kind, so the bars start at different x positions.
- short_summary: tree time bars sit at different x per row kind
- failure_scenario: The call rows end in a fixed `width={7}` time cell (579). The root row ends in an unsized `facts` text, "3 calls · 1 agent" or "starting" (595). Agent rows end in an unsized "2 calls · 12s" (620). The bar is `flexShrink={0}` and sits after the `flexGrow` target box, so its left edge is the row width minus the right cell, minus the gap, minus `gw`. A root with 17 characters of facts and a call row with 7 therefore put their bars 10 columns apart. This is the first thing the user asked for ("each node's time bar in one column").
- category: layout-misalignment
- verdict: CONFIRMED (by reading the layout; I did not run it)
- fix: Give every row's last cell the same fixed width. For example, put the root and agent facts in a `width={N}` box (N around 16) and make the call time cell the same N. Alternatively, put the bar after a fixed-width label column instead of before a variable one.

**MEDIUM** `mods/foreman-ui/hooks/register.tsx:828-831`. The Spinner line is blanked on a condition that does not say the tree is drawn, and it drops information the tree does not carry.
- file: mods/foreman-ui/hooks/register.tsx
- line: 828
- summary: The spinner is replaced by an empty Box whenever `feed` has an entry, even if no tree is on screen. It also drops the elapsed time and the engine's message.
- short_summary: spinner blanked even when no tree is drawn
- failure_scenario: The tree is drawn only when AbovePrompt gets past `hasSurvey` (924) and, with the pane closed, past `treeRows >= 3` (1081). Take a tall approvals/plans card (`cardRows` large) so that `treeRows` is under 3. The tree is not drawn, and a non-empty `feed` still blanks the spinner, so the user sees no working indicator at all. Separately, the comment says the root shows the time, but `liveTree`'s root (rows.tsx:589-597) has no elapsed time. The old spinner's `elapsed(ms)` and `e.props.message` (for example a retry or compacting message, line 836) are lost.
- category: lost-feedback
- verdict: CONFIRMED
- fix: Compute "tree is drawn" once and share it. Blank the spinner only when it is true. For example, set a module flag in AbovePrompt, or reuse the `treeLive` and `treeRows` logic. Add `elapsed(now - turnStartedAt)` to the root row. Keep the spinner when `e.props.message` is set.

**LOW** `mods/foreman-ui/tests/foreman-ui.test.tsx:1699-1713`. The test covers only part of the criteria.
- It asserts that a child count is at least 6, not that the last child is blank.
- It asserts that two `tree-bar-*` keys exist, not that they share a column. That is why the misalignment above passes.
- It has no case where the spinner must still show.
- Fix: assert the last child's text is blank. Add a layout or position check for the bars, if the harness exposes one.

## Acceptance criteria
- **One height all turn, blank row under it:** met by the code. `treeTall` resets at turn start (register.tsx:68), only grows (962), and a gap `Text` is added (967). The test checks only a child count.
- **Each node has a time bar in one aligned column:** partly met. Every node has a bar, but the column is not aligned (HIGH finding).
- **Spinner line not drawn while the tree is:** partly met. It is also suppressed when the tree is not drawn (MEDIUM finding).
- **`claude plugin test .`:** not run (read-only).

## Implicit decisions
- Bar width is 22% of the body width, clamped to 8-30 columns. The axis is at least 60 s, rounded up to whole minutes.
- The minimum sticky height is 5 rows plus 1 gap row.
- `treeTall` is module-level state, reset at turn start rather than at session start.
- The root no longer shows the `sectionHead` rule and comet. It is a plain row.
- The version is bumped to 0.15.1, and the README and CHANGELOG are updated. marketplace.json is in sync with plugin.json, so the pre-audit item is dismissed.
- The CHANGELOG size item is dismissed. The change adds one line.

## Not checked
I did not run the tests or render the band at real widths. I did not check the desktop surface, where `bar` returns null.

**Noticed:** `register.tsx:68` resets `treeTall` only in turn.start. `feed.length = 0` at line 537 (new session) does not reset it, which is harmless but inconsistent.
