# Brainstorm — lens: delight

- **Craft the abstain, not just the vote** — FEATURE — value 5 — effort M — risk med — category: ui delight
  Why: earlier question asks which moment feels most like craft; the pack’s decider needs abstain/fallback and a web UI, so abstain can be the designed moment, not a grey failure.
  Done when: an abstain row shows a faint ghost answer, one-word reason, and a cooling ember; screen reader announces “abstained”.

- **Show confidence as ink, not bars** — FEATURE — value 4 — effort S — risk low — category: ui motion
  Why: assumption: a decider’s confidence is more readable as a continuous ink stroke whose opacity and weight encode certainty, matching the forge/astrolabe look.
  Done when: changing a mocked confidence from 0.3 to 0.9 visibly thickens and darkens the verdict line without changing its text.

- **Dim an overturned verdict with a 3-word apology** — FEATURE — value 4 — effort S — risk low — category: ui state
  Why: the pack makes user undo the only label; delight should show the model accepting the correction visibly.
  Done when: undoing a decider-supported close dims that verdict and stores/prints a 3-word reason such as “too quick, wrong file”.

- **Give new decider builds a proving badge** — FEATURE — value 4 — effort M — risk med — category: model delight
  Why: generic models must prove themselves across projects; a visible probation state makes adoption feel earned.
  Done when: a fresh model or project shows “proving” until it beats the zero-model arm on a held-out slice.

- **Print a one-line model birthday at retrain** — FEATURE — value 3 — effort S — risk low — category: model card
  Why: the request asks how the model is trained and measured; a birthday line makes provenance feel personal.
  Done when: after retrain, `sampo status` prints “born from N closes, held out K projects, abstain floor P%”.

- **Sign each verdict with a model-build rune** — FEATURE — value 3 — effort S — risk low — category: provenance delight
  Why: pinning weights by content hash is already implied; a tiny signature lets users see which build decided.
  Done when: two builds with different artifact hashes render different small glyphs, and hovering reveals the hash and bench.

- **Let a low-confidence note wait as “one more thing”** — FEATURE — value 4 — effort M — risk med — category: ui calm
  Why: the user hates mid-run interruption; a delayed, optional note respects that while preserving delight.
  Done when: a decider note below a confidence threshold appears once after 10 seconds, labelled “one more thing”, and can be muted by class.

- **Offer a 10-second replay from any verdict** — FEATURE — value 4 — effort M — risk med — category: ui evidence
  Why: a decider is only delightful if its reasons can be felt quickly, not read in a log.
  Done when: pressing one key on any verdict row plays a 10-second scroll of the top three briefs, commands, or ledger lines that drove it.

- **Send distinct phone haptic clinks for vote, abstain, veto** — FEATURE — value 4 — effort M — risk med — category: device delight
  Why: devices are thin; a haptic pattern can make model decisions feel like forge metal before the phone is even looked at.
  Done when: a phone test fires three notifications with distinct two-second haptic patterns and a setting to disable them.

- **Show one ember glyph on watch or lock screen** — FEATURE — value 3 — effort S — risk low — category: device delight
  Why: the pack lists web UI only; a glanceable device surface needs no words.
  Done when: a mock watch or lock screen shows one glyph: bright vote, cool abstain, dark quiet, and tapping opens a one-line reason.

- **Answer “what did the decider stop?” by voice in five seconds** — FEATURE — value 3 — effort M — risk med — category: device voice
  Why: a car or hands-free moment needs a delightfully short answer, not a dashboard.
  Done when: asking the voice query returns a five-second answer with a count and one example, and falls back to silence if none.

- **Store “I’ll remember this” on user undo** — FEATURE — value 4 — effort M — risk med — category: training delight
  Why: the pack’s regret/undo label idea becomes a visible ritual; the user should feel the correction is learned.
  Done when: an undo creates a visible receipt, and the next model card cites the undo id as a training row.

- **Let the decider’s mood be a forge ember** — FEATURE — value 4 — effort M — risk med — category: ui delight
  Why: wild: the decider’s health (abstain rate, veto rate, drift) can be shown as a small living ember instead of a status table.
  Done when: changing mock ledger metrics from calm to alert changes the ember’s color and temperature, with an accessible text label.

- **Export a taste rune that changes only when taste changes** — FEATURE — value 4 — effort M — risk med — category: delight export
  Why: wild: the user’s accept/reject history could become a tiny shareable rune, not a dashboard, with stability as the delight.
  Done when: exporting the same taste metrics produces the same SVG rune, and crossing a taste threshold changes it.

- **Play a tiny “phew” when an abstain later proves right** — FEATURE — value 3 — effort S — risk low — category: delight feedback
  Why: wild: a decider should celebrate its restraint, not only its action, without becoming noisy.
  Done when: when a previously abstained decision is confirmed as correct by a later held close, the UI plays one short sound and marks the abstain “held”.

Next question: Which single decider event deserves motion before any other, so delight does not become noise?
Next question: What is the smallest device surface where an abstain should be felt before it is read?
