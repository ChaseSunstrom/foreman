# Brainstorm — lens: beautiful UI and motion

- **Acknowledge every keypress within 100 ms** — PERFORMANCE — value 4 — effort S — risk low — category: pane feedback
  Why: the user asked that `g` pressed mid-run queue instead of making them wait or retype. Assumption: the pane currently waits on the journal read before it paints anything.
  Done when: in a pty test during an active run, pressing `g` paints a visible acknowledgement frame in under 100 ms, before the journal read returns.

- **Set one type scale and baseline grid for every surface** — CLEAN — value 4 — effort S — risk low — category: design tokens
  Why: the pack names four surfaces (web UI, pane, desk, mod) that each style text on their own. Assumption: sizes and line heights drift between them.
  Done when: one tokens file generates the web, pane and desk sizes, and a test fails on any font size outside the scale.

- **Use a fixed-metric code font with no ligatures in diffs** — FIX — value 3 — effort S — risk low — category: code typography
  Why: assumption: ligature substitution in some code fonts shifts diff gutter columns, so added and removed lines misalign.
  Done when: a snapshot of a fixture with ligature-prone pairs shows gutter columns aligned at the same x-positions in web and pane.

- **Dim every lane except the one that just moved** — FEATURE — value 3 — effort S — risk low — category: focus
  Why: the Activity lanes and Agents graph show concurrent work, and assumption: with two lanes active, the eye has no anchor for what changed.
  Done when: with two lanes active, the idle lane's opacity drops to the dim level and returns on its next event, checked by a DOM class test.

- **Stack the queue as a newspaper front page with the run that needs you as the lead story** — FEATURE — value 4 — effort M — risk low — category: layout hierarchy
  Why (wild): the web UI and pane lay out every task at equal weight, so the one item needing the user is buried. Turn the layout into a front page: lead story is the blocked or failed item, then running work, then a digest.
  Done when: with one needs-you task and five others, the lead card is that task at the top, verified by a snapshot test with two fixtures.

- **Make the phone layout thumb-first** — FEATURE — value 3 — effort M — risk low — category: mobile layout
  Why: the pack lists phones among surfaces it barely covers, and assumption: the web UI's action buttons sit at the top, out of thumb reach.
  Done when: at a 390 px width every needs-you action sits in the bottom 40% of the screen with 44 px minimum targets, checked by a screenshot test.

- **Make the History and Today charts zoom from day to hour to run** — FEATURE — value 3 — effort M — risk low — category: data viz
  Why: assumption: History and Today show one fixed granularity, so a bad hour is invisible in a week view.
  Done when: zooming from a day to a run changes granularity over the same data with no reload, checked by a headless render test.

- **Draw each closed task as a bookshelf spine whose thickness is its diff size** — FEATURE — value 2 — effort M — risk low — category: history view
  Why (wild): History is a list today, and a shelf of spines makes a month of work readable at a glance, with a fat spine as a big change.
  Done when: a fixture of three tasks with diffs of 10, 100 and 1000 lines renders spine widths in that order, verified by a render test.

- **Give the pane's stalled-run card a haptic-style pulse on phones, distinct from done** — FEATURE — value 2 — effort S — risk low — category: notifications
  Why (wild): assumption: a phone notification is the only way a stuck run reaches the user away from the desk, and it reads the same as a finished one.
  Done when: needs-you and done send different vibration patterns in a device-simulator test, and the patterns are documented in the same place.

- **Show a glyph cursor that walks to the file being edited** — FEATURE — value 2 — effort S — risk low — category: live feedback
  Why (wild): the pane shows edits in a list, and a small cursor that moves to each file while the model works gives a sense of presence without extra text.
  Done when: during an edit event, the cursor's target matches the edited file's row in a render test, and it hides when the run stops.

- **Dim the pane after a minute with no input and no events** — FEATURE — value 2 — effort S — risk low — category: screen comfort
  Why: assumption: a long-running pane stays fully bright all night, which is tiring and wastes battery on laptops.
  Done when: after 60 idle seconds the pane drops to the dim level, and the first key or event restores it within one frame.
