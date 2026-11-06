# Brainstorm — lens: beautiful UI and motion

- **Render the goal as one living "contents ledger" board** — FEATURE — value 5 — effort M — risk low — category: goal UI
  Why: the pack's goal ledger, contents list, and progress denominator are spread across pane lines, the Stop hook, and the site, with no single visual object. Genesis already has a tower graph page (site/genesis), so a goal can reuse its design language. Rows are grouped by stage (planned, building, proven, reopened), and each shows its provenance tag and evidence glyph.
  Done when: a goal's page renders every contents row with a state glyph and provenance, and a test that changes a row's state in the ledger shows it moving to the new column.

- **Animate a row's state change with a short settle** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: assumption: state changes (planned → proven) are silent text swaps today. A 200 ms slide and fade explains what just changed and lets the user see a reopen as a visible step backward.
  Done when: toggling a row's state fires one transition, and `prefers-reduced-motion` turns it into an instant swap, checked in a browser test.

- **Draw a finish-line meter with an honest denominator** — FEATURE — value 4 — effort S — risk low — category: progress
  Why: the earlier "Make the progress denominator honest" idea has no visual form. Draw a bar with a solid fill for proven rows, hatched for done-but-unverified, and a ghost segment for rows added after sealing, so scope growth is visible rather than hidden.
  Done when: adding a row after sealing widens the bar's ghost segment, and its aria-valuenow and aria-valuetext match the numbers.

- **Show done vs stopped as two distinct end states** — FEATURE — value 4 — effort S — risk low — category: state design
  Why: the pack's core ask is knowing when it's actually done rather than merely stopped, and a typed verdict needs a look nobody can mistake. Done is a closed ring with a check, stopped a half-ring with its cause (usage limit, killed, gave up), and unknown renders as stopped. Each state differs in shape and wording as well as colour, so it survives colour blindness and monochrome terminals.
  Done when: a snapshot test renders all three states and shows distinct glyph, label, and contrast of at least 4.5:1 in both themes.

- **Design the empty, loading, and error states of the goal page** — FEATURE — value 3 — effort S — risk low — category: states
  Why: assumption: site/genesis shows a blank until its JSON loads. States needed: no goal yet (one line and the `fm` command to start), a plan being drafted (skeleton rows), a ledger that can't be read (the fail-closed message with the file path).
  Done when: three fixtures (empty, partial, corrupt ledger) each render a designed state with no console errors.

- **Print a one-screen goal card with a fixed layout for the terminal** — FEATURE — value 4 — effort M — risk low — category: terminal UI
  Why: the pack lists re-injecting a goal card every session under a hook byte budget, but its look is unspecified. Use a fixed-width box with the meter, next action, the stop cause of the last session, and the top open row. Same glyphs as the pane and site, with an ASCII fallback under NO_COLOR.
  Done when: the card stays under its byte cap in a golden test, and renders identically after stripping ANSI.

- **Show a baton-pass animation in the pane** — FEATURE — value 2 — effort M — risk low — category: motion
  Why: the pack has foreman-ui's pane and the baton idea. When a new session picks up a goal, a marker travels from the prior leg's last step to the next action, so the user sees which leg ended where.
  Done when: a resume event shows the marker moving once; a reduced-motion setting shows only the end position.

- **Wild: Play a goal back as a timelapse of the contents board** — FEATURE — value 3 — effort L — risk low — category: delight
  Why: wild. The ledger is an append-only event log, so replaying it at 60x on the site can show rows appear, turn green, and reopen, with the scope-growth ghost segment swelling. A scrubber is included, which makes the replay linkable and shareable as a postcard.
  Done when: the page replays a fixture ledger deterministically from events and a scrubber position maps to the same frame on reload.

- **Wild: Draw a "distance to finished" map as a trail** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. A winding path from start to flag, with a pin per leg, camps where sessions stopped (labelled with cause), and detours where a reopen forced a step back. A glance tells a multi-day story better than a list.
  Done when: a fixture goal with 3 legs and 1 reopen renders 3 camps and 1 detour, and every camp has a text alternative.

- **Wild: Stamp a "looks done?" seal that wobbles until the auditor agrees** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. A stamp that sits slightly crooked and pulses in amber while the cold auditor or the 14-day warranty is pending, then snaps straight and turns solid on confirmation. It encodes "done is provisional" without a word of explanation.
  Done when: the seal's state follows the ledger across the pending, confirmed, and reopened fixtures, and the pending state has a text label as well.

- **Give the goal page a diff view between plan versions** — FEATURE — value 3 — effort M — risk low — category: goal UI
  Why: the pack's ideas include plan diffs at resume and scope growth shown to the user, but no view exists. A two-column view marks added, removed, and reordered rows, and tags each with its cause (user steer, lesson, miss).
  Done when: two sealed fixture versions render with added, removed, and moved rows distinguished by both icon and colour.

- **Unify glyphs and colours in one token file for terminal, pane, and site** — CLEAN — value 3 — effort M — risk low — category: design system
  Why: the pack shows the genesis page was rebuilt to match style.css tokens, and the pane has its own palette problems (T-1217, background #262626). One token file generates the CSS variables, the ANSI map, and the pane theme, so a state never looks different across surfaces.
  Done when: a test compares the token file against the site, pane, and terminal outputs and fails when one drifts.

- **Run an accessibility check on every goal surface as a gate** — FEATURE — value 3 — effort M — risk low — category: accessibility
  Why: assumption: no gate covers contrast, keyboard order, or reduced motion on the goal page. Add one check to `fm doctor` that runs axe over the fixtures and fails on serious violations.
  Done when: `fm doctor` reports the page's accessibility check and exits non-zero when a fixture has a contrast failure.

Next question: Which of these surfaces does the user actually look at during a multi-day goal (pane, terminal card, site), so the first to be designed is the one they open daily?
Next question: What does a goal with 80+ contents rows look like, and does the board group, collapse, or summarize before it becomes unreadable?
