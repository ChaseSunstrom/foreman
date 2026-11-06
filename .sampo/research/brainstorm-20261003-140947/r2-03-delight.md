# Brainstorm — lens: delight

- **Settle every panel with a one-beat "ink dry" animation** — FEATURE — value 4 — effort S — risk low — category: motion
  Why: the user asked "can you animate your messages better?" and noted that `$` in shell commands isn't animated like "Running". A reply already settles on ●. Extend that into one shared beat: border brightens, then eases to its resting colour when the turn ends. Every panel kind then finishes the same way.
  Done when: a mod test renders reply, command, edit and agent panels through a "settling" frame and a "settled" frame, and all four differ only in border colour.

- **Pair every diff hunk with a theme-tuned palette and a word-level highlight** — FEATURE — value 4 — effort M — risk low — category: diffs
  Why: the user said "the git diffs with the green/red are weird in contrast". Use muted row backgrounds and brighten only the changed words, so the panel palette stays intact and large edits don't glare.
  Done when: a golden-frame test of a one-line change shows only the changed tokens in the strong colour, with the contrast ratio asserted in the test.

- **Collapse finished tool rows into a one-line "did X in 4 steps" fold** — FEATURE — value 4 — effort M — risk med — category: chat-density
  Why: the user complained about "Update and whatever" tool-call rows and about things "not being shown". The idea "Fold tool rows into per-step groups" exists; this adds that a fold opens in place on a key and a failed row never folds.
  Done when: a finished step with 6 tool rows renders as 1 row, a step containing a failed row stays expanded, and the expand key restores the full rows in a test.

- **Make the dashboard and the in-chat panels share one theme token file** — CLEAN — value 3 — effort M — risk low — category: consistency
  Why: the user's repeated complaints that "AC and audits aren't matching", "buttons aren't panelled" and "everything still doesn't match foreman". Mismatches come from per-component styling. Assumption: kit.tsx currently holds some colours and spacing inline.
  Done when: a lint test fails if any rows/register/kit file uses a literal colour or border style outside the token file.

- **Show a "return card" on resume that fits one panel** — FEATURE — value 3 — effort S — risk low — category: continuity
  Why: after `--continue`, the user said "you weren't reprompted". The restart now works; the next step is a short panel stating what ran while away, what is waiting on them, and what the drive does next.
  Done when: a resume with open work and one waiting gate renders a card with exactly those three lines, in a test.

- **Name each parallel lane with a stable colour and glyph across the dashboard and chat** — FEATURE — value 3 — effort M — risk low — category: parallel
  Why: the user cares about parallel runs ("make sure parallel things don't cause context/speed/quality issues"). Interleaved lane output is hard to read without a visual key. Assumption: lane ids are available to the renderer.
  Done when: two lanes' rows carry different glyph and colour in the chat, and the dashboard lane list uses the same pair.

- **Wild: Play a "task closed" flourish that draws the receipt as a ticket stub** — FEATURE — value 2 — effort S — risk low — category: celebration
  Why: wild. Closing is the moment of delight. A 400 ms frame animation resolves into a stub showing the task id, criteria passed, audits, time and the commit hash, and it stays in the transcript as a keepsake.
  Done when: `fm task finish` emits a stub panel containing the id, the criteria count and the short commit hash, and the animation can be turned off with one setting.

- **Wild: Add a `fm postcard` that exports the session as a one-page HTML story** — FEATURE — value 3 — effort M — risk low — category: sharing
  Why: wild. The user keeps judging how Foreman looks. A static, offline-readable page built from the ledger (tasks, diffs, evidence, timeline) lets them show the work. Python stdlib only, no network.
  Done when: running it on a project with 3 closed tasks writes one HTML file with 3 task sections, and it contains no external URLs.

- **Wild: Make the panel border breathe slowly while the model is thinking** — FEATURE — value 2 — effort S — risk med — category: motion
  Why: wild. Thinking summaries can't be panelled (no render hook). A gentle pulse on the next panel's border or the band tells the user something is alive. Assumption: terminal redraw cost stays small at about 1 Hz.
  Done when: a thinking-state frame sequence alternates two border shades at no more than 1 Hz, and idle sessions draw no frames.

- **Add an "unexplained blank" detector that flags any visible region with no owning panel** — FIX — value 3 — effort M — risk low — category: render-QA
  Why: the user said "some stuff looks weird, not everything is shown" and "dashboard duplicated at the bottom of the chat". A frame-level check that every non-empty line belongs to exactly one panel, and that no section is rendered twice, would catch both classes.
  Done when: a test feeding a frame with a duplicated dashboard section and an unpanelled line fails with both reported by name.
