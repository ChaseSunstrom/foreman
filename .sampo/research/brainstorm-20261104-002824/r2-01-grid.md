# Brainstorm — lens: grid

- **Refuse to ship commits born from a prediction** — SECURITY — value 4 — effort S — risk low — category: anticipation × unattended × unsafe
  Why: drafts run in lanes while the user sleeps, and `fm ship` spends a push grant. Nothing in the pack stops a lane working a *predicted* brief from landing it under that grant (assumption: drafts get no marker today). Mark each draft's commits with a `Predicted-by:` trailer, and have `fm ship` refuse any trailer the user hasn't adopted.
  Done when: a scratch commit with the trailer is refused by `fm ship`, and passes once `fm adopt T-id` has run.

- **Re-grade the queue when the user changes the bar** — FEATURE — value 5 — effort M — risk med — category: anticipation × user × wrong
  Why: the user pushed back that the moons "aren't that wild; I want wild". Candidates already queued under the old bar stayed in the queue. A pushback of the form "not X enough" should become a scored rubric line and re-rank every unshipped draft and candidate, demoting the failures.
  Done when: replaying the 2026-11-03 wildness steer demotes at least one stored moon candidate and prints which rubric line did it.

- **Withdraw a warning when its cause goes away** — FIX — value 4 — effort S — risk low — category: anticipation × user × wrong (stale)
  Why: the drive false-wait bugs (T-2873, T-2900, T-2901) are the pattern. A flag raised on yesterday's state stays on screen after the state has changed. Give every pre-warning a `still-true:` zero-token predicate and retire the flag with a one-line "no longer true" when it fails.
  Done when: a flag whose predicate flips disappears from `fm next` and the pane within one tick, and a ledger row records the withdrawal.

- **Carry a one-line repro on every flagged problem** — FEATURE — value 4 — effort S — risk low — category: anticipation × agent × unclear
  Why: an agent that reads "this will break" can't tell whether it's true. A read-only command that shows the problem today lets the agent or the user check it in one step. This pairs with the carried gap that every Exam reads live state.
  Done when: filing a pre-warning without a command that exits non-zero on a planted fault fails.

- **Leave disputed draft fields blank** — FEATURE — value 4 — effort M — risk med — category: local models × agent × wrong
  Why: standing steer: a 27B scaffolded to frontier results. Sample the draft three times and keep only the fields all samples agree on. Disputed fields (Done-when numbers, file lists) are blanked and marked `?`, so a wrong guess can't pass as spec.
  Done when: on 10 past briefs, the kept fields are at least as accurate as single-sample fields, with the blank rate reported.

- **Sweep the site, README and scenes for banned terms from steers** — FIX — value 3 — effort S — risk low — category: site × agent × wrong
  Why: the user said never show "jarvis" and never name Claude as the orchestrator, then had to say it. Steers store `decide --check` rules already. Compile naming steers into a banned-term list and run it over site/, README, design/ and animations.
  Done when: planting "jarvis" in `site/index.html` turns the sweep red, naming the steer and the line.

- **Size the anticipation card to the model's context window** — PERFORMANCE — value 3 — effort S — risk low — category: Smith TUI × local model × slow
  Why: assumption: cards are one size. Small Ollama models and the 27B run with limited context, and a fixed card eats it. Budget the card per profile and spill the rest behind `fm why`.
  Done when: on a 4k-context profile the injected card stays under its budget, with an overflow pointer.

- **Back off the local model server when the user needs it** — FEATURE — value 3 — effort M — risk med — category: machines × unattended × unsafe
  Why: the llama-swap endpoint costs about 3 minutes per model switch and has no `/running`. Overnight work competes with the user's own morning use. Probe latency on the endpoint and pause speculative drafts when it climbs. Don't touch the loaded model without consent.
  Done when: a simulated slow endpoint pauses drafting within one tick and resumes after it recovers.

- **Wild: Draft the user's rejection before the draft** — FEATURE — value 4 — effort M — risk med — category: anticipation × user × wrong (wild)
  Why: wild. The user's pushbacks are recorded in their own words. For each draft, a tool-less child writes the most likely pushback from those. If it quotes a past pushback verbatim, the draft is killed or reworded before the user sees it.
  Done when: replayed against the 4 recorded pushbacks, at least 2 would have been caught pre-draft.

- **Wild: Keep only what a hasty and a stern persona both accept** — FEATURE — value 3 — effort M — risk med — category: local models × user × wrong (wild)
  Why: wild. Two small-model personas, one who skims and one who nitpicks, both read the draft. Only drafts both accept reach the morning card.
  Done when: the two-persona accept set beats the single-reader set on precision against the user's actual adopts.

- **Wild: Put a "predicted, not asked" watermark on everything speculative** — FEATURE — value 3 — effort S — risk low — category: web UI × user × unclear (wild)
  Why: wild. Pane rows, web cards, branch names and commits of speculative work all share one hatched look and one word, so the user can tell a prediction from their own asks at a glance. This overlaps the hatched "unproven" look in the pack but distinguishes origin.
  Done when: a lint finds no speculative surface without the mark.

- **Show a draft's provenance in one sentence in the web UI** — FEATURE — value 3 — effort S — risk low — category: web UI × user × unclear
  Why: the user can't judge a draft without knowing why it exists. State "because X closed and Y followed last 4 times" next to the card.
  Done when: every draft card has a reason that cites a ledger id.

Cells left empty: Desktop tray × any (blocked on libappindicator, T-0325); phone and watch × any (no surface exists yet, and earlier rounds cover them); site × unattended × slow (publish cadence is already covered).

Next question: which anticipation outputs does the user act on without opening the card, and can that be measured without logging more than file touches?
Next question: when a pushback changes the quality bar (as the moons one did), which stored artifacts were built under the old bar, and does anything find them?
