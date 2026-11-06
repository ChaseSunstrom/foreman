# Brainstorm — lens: delight

- **Show the next ask as ghost text** — FEATURE — value 4 — effort M — risk med — category: prompt UX
  Why: the user's recurring asks (FEATURE!, FIX:, "again") are highly patterned; the pack's Anticipation gap is that predictions only live in files. assumption: foreman-ui can paint dim text in the prompt line.
  Done when: with a seeded asked-stream, the prompt shows a dimmed predicted request, Tab accepts it, and any other key clears it with a "dismissed" record.

- **Close every task with a doorway line** — FEATURE — value 4 — effort S — risk low — category: close-out
  Why: the "Ideas so far" has next-ask drafting but no moment where the user sees it; task close is when attention is highest. assumption: fm task finish prints a receipt.
  Done when: `fm task finish` prints one line ("Likely next: …, say `go` to draft it") drawn from fmforesight, or nothing if below the evidence floor.

- **Print "already built" before the ask is finished** — FEATURE — value 5 — effort M — risk low — category: capture
  Why: T-2546 and the dropped-as-built entries show the user repeatedly asking for things that exist (the guard-only arm, T-2534, was dropped as built). Delight is hearing "that's already here" in one second.
  Done when: typing a request that restates a MASTER.md clause shows the clause and task id within 1s in `fm capture`, and a test with the T-2534 wording fires it.

- **Flip the 58 cells into a "moments" flipbook** — FEATURE — value 3 — effort M — risk low — category: coverage UI
  Why: coverage.md is a grid nobody reads for pleasure; each filled cell can be the one moment the user would have been annoyed without it. assumption: cells can carry a one-line scene.
  Done when: the web UI page steps through filled Anticipation cells as cards (scene, file cited, "try it" command), arrow keys move, reduced-motion shows a static list.

- **Add a "told you so" receipt** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: foresight warnings that came true are the proof it earns its bytes (the lean steer wants measured substance). assumption: flags are logged with a signature.
  Done when: when a flagged problem later occurs, the next session start shows "Flagged 2 days ago: X. It happened." with the lead time, and misses show nothing.

- **Make dismissal teach, with a tiny "not today" shelf** — FEATURE — value 4 — effort S — risk low — category: restraint
  Why: the user pushes back on noise (steers on lean, pace, silence). A nudge dismissed twice must go quiet. 
  Done when: dismissing a flag mutes its signature after two dismissals, `fm foresight shelf` lists muted ones with a restore command, and a test covers both.

- **Show restraint as a pride line** — FEATURE — value 3 — effort S — risk low — category: status line
  Why: the pack stresses silence ratio and weight; seeing "quiet: 41 turns, 0 bytes" is a small delight that proves the lean steer.
  Done when: the status line (or `fm doctor`) shows a silence count for the session and it matches injected-byte logs.

- **Let "again" resolve to the right autonomous act** — FEATURE — value 4 — effort M — risk med — category: prompt UX
  Why: the user's words are terse ("again", "the second brief"); the pack's wild ideas include this. assumption: autonomous acts are logged with cause.
  Done when: typing `again` after a lane ran lists the 1–3 candidate acts with one-letter picks, and a pick re-runs it.

- **Wild: Hold a "guess my next ask" mini-game** — FEATURE — value 3 — effort M — risk low — category: calibration (wild)
  Why: assumption: scoring predictions needs the user's ground truth; a 10-second game gives labelled hits and a visible Brier score while being fun.
  Done when: the web UI shows three predicted asks, the user ticks the closest, and the pick lands in the prediction ledger and moves a hit-rate chart.

- **Wild: Open each session with the one thing you'll probably type first** — FEATURE — value 4 — effort S — risk med — category: session start (wild)
  Why: users who start work the same way daily (queue, ship, review) can skip typing; the dropped-as-built list shows the cost of mistakes at start.
  Done when: SessionStart shows one candidate first action only if its backtest hit rate is ≥ a stated floor, else nothing; `fm foresight why` explains it.

- **Wild: Tip the hard hat when trouble is coming** — FEATURE — value 3 — effort S — risk low — category: motion (wild)
  Why: the logo is a hard hat; a tiny tilt/animation in the web UI and a glyph in the status line makes a warning feel friendly instead of alarming.
  Done when: a pending foresight flag adds a one-frame tilt glyph to the status line and a CSS tip animation on the pane, with prefers-reduced-motion disabling the animation.

- **Give each forecast a one-line "because"** — FEATURE — value 4 — effort S — risk low — category: explanation
  Why: unexplained nudges read as noise; the user's steers demand grounding and no reused phrasing.
  Done when: every foresight output ends with "because: <ledger row or file>" and one that can't cite a source isn't shown.

- **Print a "things you'll probably ask next" list at task close, from co-change** — FEATURE — value 3 — effort M — risk med — category: close-out
  Why: sibling-edit follow-ups are the user's frequent pattern (T-2547 followed T-2546's grounding idea). assumption: git co-change is available.
  Done when: closing a task that touched file A lists up to 3 files that changed with A in ≥3 prior commits, and none when evidence is thin.

Next question: Which delight touches get used and which does the user switch off, and is there a way to learn this without asking?
Next question: Does anything the user sees today (status line, fm next, the pane) have room for a forecast line without raising the injected-bytes ratchet?
