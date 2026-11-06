# Brainstorm — lens: beautiful UI and motion

- **Render one Exam card as a meter-and-clock pair** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: Gen-4 Mission 1 requires every brief's Exam to name an outcome measure and a live-state reading; today they are prose, so the user can't see at a glance whether a reading is fresh or what it measured. Ideas so far cover the contract but not its look.
  Done when: a brief's web card shows the outcome value as a gauge and the live reading's age as a clock beside it, and a golden-screenshot test pins both for fresh, stale and "can't read" readings.

- **Design a four-state verdict glyph used everywhere** — FEATURE — value 5 — effort M — risk low — category: design language
  Why: Receipts, Exam readings, grid cells and dissents each show pass/fail differently (the pane paints #262626 oddly, T-1217). Many ideas ask for "unproven" and "overridden" states without one shared mark. Assumption: shape-plus-colour, hatched for unproven.
  Done when: one component renders proven, unproven, overridden and unread from a state table, and a test fails if any web view or CLI line uses a different mark.

- **Show the request grid as a coverage wash** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: The grid of surfaces/actors by failure modes is the core of exhaustive thinking, yet a table of filled/empty/n-a cells reads as a spreadsheet. A tint by fill and age shows the dark spots at once. Assumption: the user opens the sting cell first.
  Done when: the Mission page renders the grid with a tint per cell (filled, empty, n/a, stale), keyboard-navigable, with a data-table twin for screen readers, and a snapshot test covers all four tints.

- **Animate a cell filling when its brief closes** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: Motion should explain state. A close is the one event that changes a cell, and today it just changes text. Assumption: motion fires only on a real ledger change, never on a timer.
  Done when: closing a brief makes its cell animate once from empty to filled on the next page load, and with reduced-motion set it changes with no animation (tested).

- **Draw a dissent as a two-sided scale that tips on the outcome** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: Carried gap "dissents scored against outcomes". Objection vs outcome is the dissent's whole meaning, yet it would be a number in a column. A scale that tips toward the side the outcome supported, and stays level with "outcome never observed", makes it readable.
  Done when: each dissent renders level, tipped-to-dissenter or tipped-to-builder, with a text label; a test renders all three plus "never observed".

- **Pin a one-line interpretation banner above every Mission** — FEATURE — value 4 — effort S — risk low — category: copy and layout
  Why: Users keep correcting scope (several steers, many drops); stating how the request was read, and the width taken, lets them object in one glance before work starts. Assumption: the banner is built from existing Mission fields.
  Done when: every Mission page starts with a banner holding the interpretation and the scope width, and a test fails if the banner is missing or over 140 characters.

- **Design empty, stale and "can't read" states for every Exam view** — FEATURE — value 4 — effort M — risk low — category: states
  Why: The open question of an offline snapshot (service down) needs a visible answer: "unmeasured, carried forward from 3 days ago" is a state, not an error. Today an unreadable reading would likely show blank or a trace.
  Done when: each of empty, loading, stale and unreadable has a designed render with a reason line and the next command, covered by golden screenshots.

- **Render the left-out receipt as a torn-edge slip** — FEATURE — value 4 — effort S — risk low — category: delight
  Why: "Say what it left out" is the Mission's headline; a distinct, shareable slip with a perforated edge makes the omission as visible as the result. Capped at five lines, ranked.
  Done when: finishing a Mission shows the slip as the last element of the page and the CLI, five lines at most, with "N more" and the flag that shows them; test pins the cap.

- **Add a "since you looked" ribbon to the pane and Mission page** — FEATURE — value 4 — effort M — risk low — category: motion and state
  Why: The user returns after unattended runs; ideas ask for a while-you-were-away card, but a ribbon fixed at the top of each surface that lists cells changed, readings gone stale and decisions awaiting them is the visible form. Assumption: "looked" is the last page render recorded locally.
  Done when: reload after a ledger change shows a ribbon with the counts, clicking a count scrolls to the first changed item, and it clears after being seen.

- **Gate the web UI on a contrast, colour-depth and reduced-motion check** — FIX — value 4 — effort M — risk low — category: accessibility
  Why: T-1217 shows a docked pane background mismatch got through; no test catches colour regressions. Assumption: the checks run on both web and 16-colour terminal themes.
  Done when: a test fails if any theme token pair drops under 4.5:1 contrast, if a verdict relies on colour alone, or if any animation ignores `prefers-reduced-motion`.

- **Wild: Render the grid as a night-sky map where empty cells are dark** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. A request's coverage as stars: filled cells glow, left-out ones are dim patches you can click to promote to a task. Shows what's missing before anything is read.
  Done when: a toggle on the grid page switches to the sky view, with the same cells, clickable, and a screen-reader table twin.

- **Wild: Give the hard hat a lamp that dims as unexamined cells shrink** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. The logo is the product's face; letting its lamp brighten as the number of left-out cells falls gives a glanceable "how exhaustive was that" signal in the pane header and tray.
  Done when: the header icon's brightness maps to the share of cells examined, labelled with that number, and is static under reduced motion.

- **Wild: Scrub a Mission as a timeline of what was considered** — FEATURE — value 3 — effort L — risk med — category: motion
  Why: wild. A slider replays lenses proposing, canaries firing, ideas dropped as "already built" and cells filling, so the user can see how a result was reached and where a dissent was overruled.
  Done when: dragging the slider on a closed Mission shows the page's state at that point from ledger timestamps only, and a test replays two Missions deterministically.

Next question: Which Mission-page element does the user open first, and does anything record it locally so layout can follow it?
Next question: Does the pane's docked-background problem (T-1217) come from Claude Code's own paint or from foreman-ui, so a token sheet can actually fix it?
