# Brainstorm — lens: delight

- **Run a hello-proof on first use** — FEATURE — value 4 — effort S — risk low — category: onboarding
  Why: assumption: a newcomer meets proof as a gate before ever seeing it work. The pack's open items T-0862 and T-0863 (newcomer tour, first-hour ladder) are still deferred.
  Done when: `fm prove --hello` in a fresh repo checks one true claim about it (for example that the README's install command resolves) in under 5 seconds and prints the proof line, a red-canary line and an "unproven" example.

- **Circle the change on every shot** — FEATURE — value 4 — effort M — risk low — category: UI proof
  Why: `fm shot` ideas so far cover slider, flicker and flip-through, but none say where to look. Assumption: reviewers skim images.
  Done when: a shot diff writes a PNG with the changed regions outlined and a plain-words caption ("button moved 12px right"), plus a ghost-cursor trail when it came from `fm flow`.

- **Draw perf claims on a wobble bar** — FEATURE — value 4 — effort S — risk low — category: performance
  Why: the request asks that what can't be proven be labelled, and earlier ideas already ask for a noise floor and an "inconclusive" verdict. Neither shows the user that a "20% faster" claim sits inside the noise.
  Done when: a perf proof prints a one-line bar with the noise band shaded and the claimed delta marked; a delta inside the band renders as "can't tell" and fails a test that asserts the band width.

- **Let evidence zoom through three levels** — FEATURE — value 4 — effort M — risk low — category: legibility
  Why: assumption: users want a glance first and the full artifact only when they are suspicious. Many separate evidence ideas exist; none sets a common depth ladder.
  Done when: every proof line exposes glyph, one line and full artifact, and `fm proof ID --zoom N` prints each level.

- **Show the smallest wrong thing when a proof fails** — FIX — value 5 — effort M — risk low — category: failure UX
  Why: the pack's "does it do what the user meant" and failed-check work (T-2613 keeps each failed check's line and class) stop at classifying the failure. A red result is where delight is cheapest to lose.
  Done when: a red proof prints one highlighted offending line or region, the last-green delta, and a copy-ready repro command that reproduces the red when run.

- **Draw data changes as sparkline cards** — FEATURE — value 3 — effort M — risk low — category: data proof
  Why: row-polaroids and a balance-scale picture were proposed; neither shows a distribution. Assumption: null rate, row count and a numeric spread are what people actually eyeball.
  Done when: a data proof prints before/after sparklines for row count, null share and one numeric column in a terminal-safe form that also works under NO_COLOR.

- **Highlight verified claims in the margin of the docs** — FEATURE — value 4 — effort M — risk low — category: docs proof
  Why: docs-against-code checks exist as ideas; no one has made the result readable in place. The README makes many claims (numbers, flags, "passes").
  Done when: `fm docs --margin README.md` prints the file with each claim line marked proven, unproven or contradicted and a pointer to the code line that settles it.

- **Keep an IOU jar for unproven claims** — FEATURE — value 3 — effort S — risk low — category: unproven
  Why: the request says unproven must be labelled; ranked registers and cost-to-prove exist as ideas. The unfilled piece is making the debt feel paid off.
  Done when: each unproven claim gets an IOU line with an owner and a cheapest next step; paying one prints a short "IOU torn up" line and the jar count drops, covered by a test.

- **Say it back in one plain sentence** — FEATURE — value 4 — effort M — risk med — category: meant-check
  Why: example pairs and a meant-meter exist; a single observed-behaviour sentence the user answers with Enter or an edit does not. The hard part is that the sentence must come only from captured evidence.
  Done when: at finish the user sees "When you X, it now Y" built from recorded evidence, and Enter records it as the user's confirmation, while an edit is stored as a correction.

- **Print a contact sheet in the finish receipt** — FEATURE — value 3 — effort S — risk low — category: UI proof
  Why: finish receipts list claims, but a reviewer with five shots has to open five files. Assumption: one grid image gets looked at.
  Done when: a finish writes one PNG grid of all shots, each labelled with its claim id, and the receipt links to it.

- **Wild: Give each prover a trading card** — FEATURE — value 2 — effort S — risk low — category: playful
  Why: wild. Provers prune by unique catch in an earlier idea; a card per prover (catches, false alarms, last catch, runtime) makes the keep-or-cut decision something you want to browse.
  Done when: `fm provers --cards` prints one card per prover from real ledger numbers, and a prover with no catches shows "rookie".

- **Wild: Show a proof tide on the status line** — FEATURE — value 2 — effort S — risk low — category: ambient
  Why: wild. A live counter was proposed, but not the week's trend. A tide glyph that rises and falls with the share of fresh proofs shows decay without a number.
  Done when: the status line renders a rising, steady or falling glyph from the last 7 days of proof records, and a test fixes the three states.

- **Wild: Re-run a recorded flow months later as then/now** — FEATURE — value 3 — effort M — risk med — category: time capsule
  Why: wild. A captured flow is a free time capsule. This differs from flipping through commits: it replays a past proof's own recorded steps against today's build.
  Done when: `fm flow replay ID --then-now` shows the old and new captures side by side with a diff summary, or labels the flow "no longer replayable" with the reason.

Next question: Which of these delights does the user open and reuse in a week, judged from their own command history rather than Foreman's guess?
Next question: When a delight surface shows a proof, what stops it from looking more certain than the underlying evidence?
