# Brainstorm — lens: beautiful UI and motion

- **Draw the Exam as a meter-and-clock pair** — FEATURE — value 4 — effort M — risk low — category: Exam UI
  Why: the request carries "every brief's Exam names an outcome measure and a live-state reading", and the pack's ideas stop at the schema. No look is given to that pair. Show the outcome as a horizontal meter (target tick, today's value, parent-commit value ghosted) and the live reading as a clock face of its age, which turns from solid to hatched once it goes stale.
  Done when: a brief page rendered from a fixture with one fresh and one 9-day-old reading shows a solid meter for the first and a hatched one for the second, asserted in a DOM test.

- **Animate a dissent as a two-sided scale** — FEATURE — value 4 — effort M — risk low — category: Dissent
  Why: "dissents scored against outcomes" is a carried gap, and a score is a number nobody will read. A scale that tips toward the side the outcome favoured explains the verdict at a glance. Its fourth state, "outcome never observed", rests level and dimmed, not tipped.
  Done when: for dissents fixtured as upheld, overruled and unobserved, the DOM shows three distinct tilt classes, and the scale animates once on first view and not on re-render.

- **Underline the request cell by cell** — FEATURE — value 5 — effort M — risk med — category: Mission page
  Why: the question left open is "which cell do they open first, and does the grid order match it?". Render the user's request text with each clause underlined in the colour of its cell state (filled, empty, n/a, left out). Hovering a clause scrolls to its brief. That puts the grid in the user's own words, not an abstract matrix.
  Done when: a Mission fixture with five clauses renders five underlines, and each clause links to a brief anchor or to a "left out" slip.

- **Print the left-out receipt as a torn-edge slip** — FEATURE — value 4 — effort S — risk low — category: Receipt
  Why: "say what it left out" is the Mission's point, and a bare list reads as a footnote. A slip with a perforated edge pinned under the finish card makes the omission a first-class object. It shows each item with its reason and who can unblock it. It never reads "nothing" without a count.
  Done when: closing a fixture Mission renders a slip element with one row per left-out cell, and an empty list renders "0 left out of N cells considered".

- **Fill the grid with a coverage wash, not icons** — FEATURE — value 4 — effort M — risk low — category: Grid
  Why: the ideas so far list the grid with filled, empty and n/a cells. A wash gives filled cells a solid tint, empty cells a dark gap, n/a cells a dotted outline, and unverified cells a hatch. This keeps one verdict grammar, with "unproven" always hatched and never green. Add a shape per state so colour is never the only cue.
  Done when: a contrast test passes at 16-colour and NO_COLOR, with each of the four states distinguishable by pattern alone.

- **Animate a cell filling when its brief closes** — FEATURE — value 3 — effort S — risk low — category: Motion
  Why: motion should explain state change. When a brief closes, its cell fills over 300 ms from the edge nearest the brief card, then settles. Under reduced motion it swaps instantly with a one-frame outline.
  Done when: a state-change fixture emits exactly one fill transition per closed brief, and the `prefers-reduced-motion` run emits none.

- **Design the empty, stale and "can't read" states** — FEATURE — value 4 — effort M — risk low — category: States
  Why: the open question is what the Exam says when a snapshot cannot be taken. Give it its own kind tone: "Couldn't read this (service offline). Last good reading: 3 days ago." with the command to retry. Empty cells say what would fill them. None of them is red.
  Done when: each of the three states has a rendered fixture with its next command visible, and none uses the failure colour.

- **Pin one interpretation banner above every Mission** — FEATURE — value 4 — effort S — risk low — category: Mission page
  Why: the ideas so far include "record which scope width a request was taken at", but nothing shows it. A single banner reads "I took this as: X, at width Y; here is what that excludes." and carries a one-key widen with a price preview.
  Done when: every rendered Mission page has exactly one banner element holding a width label, and a Mission without one fails the page test.

- **Show a "since you looked" ribbon on the Mission page** — FEATURE — value 3 — effort S — risk low — category: Delta
  Why: the unattended Mission runs while the user is away, so the first view should say what changed in the grid. The ribbon reads "3 cells filled, 1 re-opened, 2 readings went stale", and clicking a count highlights those cells.
  Done when: with a stored last-seen epoch, the ribbon counts match a fixture diff and disappear after being viewed.

- **Scrub the Mission as a timeline of what was considered** — FEATURE — value 3 — effort L — risk med — category: Timeline
  Why: this makes the exhaustive-thinking process visible. The scrubber walks lenses, canaries, drops and fills in order, so the user can see why an idea was dropped. Each drop carries its "nearest existing thing" canary.
  Done when: dragging the scrubber to step k shows exactly the grid state recorded after event k, tested against a fixture of 12 events.

- **Wild: Render the grid as a night-sky map** — FEATURE — value 3 — effort M — risk low — category: Grid (wild)
  Why: wild. Empty cells are dark patches and filled cells are stars, brighter the more typed asks landed there. "What I haven't looked at" is then literally the dark. Keyboard users get a data-table twin.
  Done when: toggling sky view keeps the same cell ids as the table view, and a screen-reader test reads the same counts either way.

- **Wild: Dim the hard hat's lamp as unexamined cells shrink** — FEATURE — value 2 — effort S — risk low — category: Delight (wild)
  Why: wild. The logo hat in the pane header carries a small lamp whose brightness equals the share of cells examined. It is a quiet, honest ambient gauge, and it pulses only when a reading goes stale.
  Done when: the pane header lamp's brightness class changes with the coverage fixture value, and pulsing is limited to the stale case.

- **Wild: Tear the left-out slip off and keep it** — FEATURE — value 2 — effort M — risk low — category: Receipt (wild)
  Why: wild. Dragging the slip off the page drops it into a "kept" tray the user can revisit. Each kept slip is turned into a deferred task, and the next Mission's pack carries it as an aged seed.
  Done when: tearing a fixture slip creates one deferred task that appears in the next Mission's pack with its age.

- **Make Exam readings legible to a screen reader** — FEATURE — value 3 — effort S — risk low — category: Accessibility
  Why: a meter and a hatched clock mean nothing unspoken. Each carries one sentence such as "Outcome 62 of 80, reading 9 days old, stale", and the grid and scale carry a data-table twin.
  Done when: an accessibility test reads the sentence for each fixture state, and no meter lacks one.

Next question: which of these surfaces does the user actually open (web page, pane or the finish card), so motion effort goes to the one they see first?
Next question: when a reading is stale, does the user want it hatched and kind, or blocked, and who decides?
