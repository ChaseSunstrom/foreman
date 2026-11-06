# Brainstorm — lens: delight

- **Open every Mission on a one-sentence "what I took you to mean"** — FEATURE — value 5 — effort S — risk low — category: legibility
  Why: the request "#2 Exhaustive thinking" is jargon; the user's habit of narrowing scope ("scoped to the volatile-path audit", "ledger conservation is left out") shows interpretation is where Missions go wrong. Earlier ideas covered an interpretation banner but not its voice: write it as a single plain sentence quoting the user's own words, with the width taken.
  Done when: every file under gen-4/mission-*.md starts with a line `Taken as:` of ≤ 30 words that quotes at least one phrase from the request, checked by `fm genesis check`.

- **Print a "Left out" slip as a torn-edge receipt at Mission close** — FEATURE — value 4 — effort S — risk low — category: closure
  Why: the request is "says what it left out"; assumption: a visible, tidy artifact makes the claim feel real. One slip per Mission, at most five lines, each with the unlock command.
  Done when: closing a Mission prints a boxed slip whose line count equals the Mission file's Left-out entries, capped at 5 with "+N more" and the flag that shows them.

- **Fill a grid cell with a small ripple when its brief closes** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: the web UI shows state as numbers; motion that maps to a ledger edge explains progress. Respect reduced-motion; no ripple when the page loads already filled.
  Done when: a test closes a brief and the web page's cell gains `data-just-filled` for 1.2 s, and not under `prefers-reduced-motion`.

- **Show each dissent as a two-pan scale that tips when the outcome lands** — FEATURE — value 3 — effort M — risk low — category: dissent
  Why: dissents scored against outcomes are a carried gap; a pending dissent should look level, and tip toward whoever was right at the 14-day close-survival reading.
  Done when: the web card renders three states (level/pending, tipped-dissent, tipped-majority) from the existing survival record, with an unmeasured state that stays level and says why.

- **Greet an all-clear with one calm line** — FEATURE — value 3 — effort S — risk low — category: tone
  Why: `fm doctor` and `fm genesis check` print long lists; a user scanning for trouble enjoys one line when nothing is wrong. Assumption: red-only output is not yet default.
  Done when: `fm doctor --calm` prints exactly one line and exit 0 on a green state, and the full list on any red.

- **Quote the user's own sentence beside each canary hit** — FEATURE — value 4 — effort M — risk low — category: grounding
  Why: "already built" drops recur (many dropped items); showing the nearest existing thing beside the user's phrase makes the near-miss recognizable rather than just rejected.
  Done when: a grounded "not built" claim prints up to three nearest existing things, each with path:line, and the user phrase it matched on.

- **Name a settled dissent in the feed with a one-line result** — FEATURE — value 3 — effort S — risk low — category: feed
  Why: scored dissents are invisible unless someone reads the ledger; a "Dissent on T-2690 was right: the close was reverted on day 6" line gives the habit a payoff.
  Done when: settling a dissent appends one feed line with task id, verdict, and days elapsed, and none for unmeasured ones.

- **Mark unreadable Exam readings with "can't read: why" instead of a blank** — FIX — value 4 — effort S — risk low — category: empty states
  Why: carried gap asks every Exam to name a live-state reading; offline or missing state must not look like a pass or an empty cell.
  Done when: an Exam whose command exits nonzero or times out renders `unmeasured — <reason code>` with the age of the last good reading, in CLI and web.

- **Wild: Tear-off slip you can keep** — FEATURE — value 3 — effort M — risk low — category: keepsake
  Why: wild. Export a Mission's Left-out slip as a one-page printable SVG sized like a receipt, with the date, the interpretation sentence, and a QR to the Mission page.
  Done when: `fm genesis slip gen-4/1` writes a valid SVG under 20 KB that renders the sentence and every left-out line.

- **Wild: Night-sky map of the request** — FEATURE — value 3 — effort L — risk low — category: visualization
  Why: wild. Render the grid as a dark field where each filled cell is a lit star, brightness by canary evidence strength, and empty cells stay dark but labelled, so the dark areas are literally what was left out.
  Done when: the web grid view renders from the same data as the table and the count of dark nodes equals the empty-cell count shown in the CLI.

- **Wild: Blind-spot pop quiz at Mission close** — FEATURE — value 3 — effort M — risk low — category: play
  Why: wild. Before showing the Left-out slip, ask the user to guess one hole in five seconds; their guess becomes a free signal for which cells the user thinks about, scored against the slip afterwards.
  Done when: closing a Mission with `--quiz` records the guess, and the slip marks a hit, near-miss or miss; skipping costs nothing and is never asked twice in a day.

- **Chime once when a long unattended Mission lands with a first** — FEATURE — value 2 — effort S — risk low — category: sound
  Why: unattended Missions finish while the user is elsewhere; a single terminal bell plus a one-line "first of its kind" badge is a small, shareable moment. Assumption: bell is off by default and quiet hours are honoured.
  Done when: a Mission closing with a new capability rings the bell once only if `chime=on`, with a test asserting zero bells when off.

- **Hatched "unproven" as the shared look for every not-measured cell** — FEATURE — value 4 — effort M — risk low — category: design language
  Why: Exam readings, dissents and live states each have a third state (unmeasured, pending, can't read); one hatch pattern plus a shape glyph, never colour alone, makes them one language across CLI, pane and web.
  Done when: one component renders all three non-pass states with a shape glyph, passing a contrast check and a NO_COLOR snapshot test.

Next question: When the user opens a Mission page, which single line do they read first, and could the page be reordered by logging that locally rather than guessing?

Next question: Which of the delight touches (slip, ripple, chime) does the user actually keep on after a week, given their record of dropping decorative items?
