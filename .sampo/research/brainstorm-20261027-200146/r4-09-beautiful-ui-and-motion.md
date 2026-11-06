# Brainstorm — lens: beautiful UI and motion

- **Keep scroll still while a run appends** — FIX — value 4 — effort S — risk low — category: scroll anchoring
  Why: the live tree and Activity lanes repaint as the run writes, which can move the row a reader is looking at. assumption: the pane and web UI don't anchor scroll position to the visible row.
  Done when: with a fixture run appending 200 lines, the visible row's offset from the viewport top stays within 1 px across 50 appends.

- **Reflow the stage rail by container width, not viewport** — FIX — value 4 — effort S — risk low — category: responsive layout
  Why: the pane docks beside the terminal, so its width is not the window width. assumption: the stage rail reads the viewport breakpoint and clips when the pane is narrow.
  Done when: at pane widths of 40, 60 and 90 columns, every stage label is visible or truncated with an ellipsis, and none overflows.

- **Check every colour pair against WCAG AA in the build** — FIX — value 4 — effort S — risk low — category: contrast
  Why: colours are defined per surface, and a pair that drops below 4.5:1 would only show up as a visual bug. assumption: no contrast check runs today.
  Done when: the build fails if any text/background pair in the shared palette is below 4.5:1, and a deliberately low-contrast test colour makes it fail.

- **Use tabular figures for every time and token count** — CLEAN — value 3 — effort S — risk low — category: typography
  Why: timings and token counts change width as they tick, so proportional digits shift columns during a run. assumption: the pane and web UI use proportional numerals for live counters.
  Done when: every live numeric element carries the tabular-nums setting, and a counter ticking from 9 to 10 leaves the column edge unchanged.

- **Give each task a 12-cell gate sparkline in the list** — FEATURE — value 3 — effort S — risk low — category: task list
  Why: each task's gate history (pass, fail, rerun) is in the journal but only shows as text in `fm status`. assumption: a user scanning the queue wants to see which tasks flapped before opening one.
  Done when: a task with the journal sequence pass, fail, pass renders as three distinct cell states, and the same task renders identically on the web UI and the pane.

- **Morph a running card into its History row on close** — FEATURE — value 3 — effort M — risk low — category: motion
  Why: a task moves from Activity to History at close, and the jump is currently an unexplained swap. This is motion that explains a state change, which the existing "every motion has a reason" idea asks for. assumption: users track a task by its position across the two lists.
  Done when: a FLIP test shows the card's transform reaches the History row's rect within 300 ms, and with reduced motion the card lands with no transform.

- **Show the stage rail's key hints on focus, not hover** — FEATURE — value 3 — effort S — risk low — category: discoverability
  Why: the pane is keyboard-first, and hover tips do nothing in a terminal or on touch. assumption: a new user doesn't learn the keys until they are shown them where they are.
  Done when: tabbing onto any stage control displays its key within 100 ms, and the tip clears on blur.

- **Inline the critical CSS and draw the stage rail before the scripts load** — PERFORMANCE — value 3 — effort S — risk low — category: first paint
  Why: the web UI waits on its bundle before the rail appears. assumption: first paint is delayed by the script, not the network.
  Done when: first contentful paint for the rail, measured on a throttled profile, lands before the script finishes loading.

- **Print the close receipt on one page with a real print stylesheet** — FEATURE — value 2 — effort S — risk low — category: print
  Why: the receipt is the artifact users keep, and it has no print rules, so a browser print breaks it across pages. assumption: some users print receipts for their records.
  Done when: printing a receipt to PDF yields one A4 page with no clipped rows and no navigation chrome.

- **Wild: let an idle web UI play the last closed receipts as a slow kiosk loop** — FEATURE — value 2 — effort M — risk low — category: ambient display
  Why: the desk and the web UI both sit idle for long stretches, and a quiet loop of real results would make the idle surface worth looking at. wild: nobody asked for a screensaver.
  Done when: after 10 minutes with no input the loop starts, any key stops it within 100 ms, and the loop shows only receipts already closed.

- **Wild: shift the palette with local dawn and dusk, with no location access** — FEATURE — value 2 — effort S — risk low — category: theme
  Why: the terminal theme is fixed, so the UI looks the same at 6 a.m. and at midnight. wild: a clock-driven palette is a small surprise that costs no data. Use the system clock only, never a location.
  Done when: with the clock set to 06:00 and 22:00, the palette tokens differ, and the palette reads no location or network source.

- **Wild: leave a faint afterimage of a pass that fades over a minute** — FEATURE — value 2 — effort S — risk low — category: feedback
  Why: a passing gate ends silently, and a short afterimage in the pane would mark the moment without a sound or a prompt. wild: a glow that lingers like a camera flash is unusual for a CLI.
  Done when: a pass sets the afterimage, its opacity reaches zero within 60 s, and with reduced motion it appears as a static border that clears on the next keypress.
