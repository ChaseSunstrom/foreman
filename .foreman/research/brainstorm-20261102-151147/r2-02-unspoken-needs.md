# Brainstorm — lens: unspoken needs

Round 2, through the "unspoken needs" lens. Most obvious gaps are already in the list, so these go after the need behind the user's repeated corrections: the same kind of drop, steers that interact, and rules cut off mid-clause. The pack gives evidence for most; the rest are marked as assumptions.

- **Run a built-check keyed to the drop class before any slate** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: the dropped list is mostly "mostly built" or "value 2 after re-grounding" (guard --dry-run, tidy --verbs, the doctor rows), and T-2659 exists because of it. Each drop reason implies a specific check: grep the verb's help strings, look for the reader, look for the existing gauge. Today one generic grounding pass handles all of them.
  Done when: replaying the five recent drops through the per-class checks flags at least 4 of them before they reach a slate.

- **Show claimed value beside grounded value on every slate line** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: the user keeps re-grounding value downward by hand ("value 3" becoming "value 2"). A claimed → grounded column makes inflated claims visible and gives lenses a score for how much they overclaim.
  Done when: each slate line prints `claimed 3 → grounded 2` or `unchanged`, and a test fails if the grounded value is missing.

- **Render steers whole when relevant and cut by relevance, not length** — FIX — value 4 — effort S — risk low — category: context packs
  Why: the pack cuts standing rules mid-clause with "…" (the long-horizon tier, the cold-read rule, the lean-substance rule). A tool-less child reads half a constraint and can't ask for the rest.
  Done when: for a given lens, every steer whose words overlap the request or the lens is printed untruncated, and a test asserts no pack line ends in "…" for those steers.

- **Run a steer interaction matrix in simulation** — FEATURE — value 4 — effort M — risk med — category: standing rules
  Why: several steers now act on the same drive: pace off, round-first holds, wait out real limits, never stop for budget, and the new `--stall-usd`. Conflict detection is static. The user's actual need is "do these combine into what I meant?", which needs a fake-clock, fake-spend drive run under each combination.
  Done when: a test drives a fake queue through all 2^4 settings of pace/round-first/stall/limit-pause and asserts the intended stop or continue outcome. A planted contradictory pair fails it.

- **Preview a new steer against history before it is stored** — FEATURE — value 3 — effort M — risk low — category: standing rules
  Why: assumption: steers are issued quickly and tersely, and each becomes a permanent rule plus an automatic check. The converse of "replay with one steer removed": `fm decide --preview` lists which closed tasks and decisions the new rule would have changed or blocked.
  Done when: previewing a known steer prints at least one past task it would have affected, and previewing a no-op steer prints "affects nothing".

- **Detect repeat-correction language and trigger a sibling sweep and a pause** — FEATURE — value 4 — effort M — risk med — category: user signal
  Why: the missed-asks list is a run of corrections of the same class (grounding, counting, "already built"). Phrases like "again", "I already said" and "same as before" are free, user-authored signals Foreman doesn't use. It could sweep for sibling cases and drop autonomy for the next task.
  Done when: a replay of recorded user messages flags at least 80% of the labelled repeat-corrections, and each flagged one files a sibling-sweep capture.

- **Number every idea so round-2 ideas cite what they extend** — FEATURE — value 3 — effort S — risk low — category: brainstorm
  Why: the "ideas so far" list is thousands of untitled lines. The round-2 brief asks for combinations, but nothing records which idea a combination builds on, so duplication and combination can't be measured.
  Done when: each idea carries a stable id, and a round-2 idea with an `extends:` field resolving to a real id is counted as a combination in the report.

- **Stop on estimated unseen idea mass, not on round count** — PERFORMANCE — value 3 — effort M — risk low — category: brainstorm cost
  Why: assumption: cost grows with each round while novelty falls (this pack's thin categories are already fully populated). Estimate the unseen share from the cluster counts, which the 525-idea catalogue already has.
  Done when: a replay of rounds 1–2 of a past brainstorm gives a stop signal no later than the round where fewer than 20% of new ideas survived grounding.

- **List the questions Foreman suppressed because of "never block on the user"** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: the user ordered Foreman to pick and record rather than ask. The unspoken need is knowing which unasked questions would have changed the outcome. The costly-decision record holds the choices but not the suppressed forks, ranked by how expensive a wrong guess is.
  Done when: the Genesis report has a "questions I did not ask" section, ranked, each linked to its `fm decide` record.

- **(wild) Hunt for loopholes in each steer's wording** — SECURITY — value 3 — effort M — risk low — category: standing rules
  Why: assumption: terse steers get read literally by sub-agents. A tool-less adversary child is rewarded for finding an action that obeys the words and defeats the intent. Each find becomes a clarified clause or a check.
  Done when: the first run on the current steers yields at least one loophole, and a fixed steer's check blocks the planted example.

- **(wild) Seal a prediction of the user's next steer and score it** — FEATURE — value 2 — effort S — risk low — category: user model
  Why: assumption: the user's last 30 steers have patterns. Before each generation, a tool-less child writes the next steer from the ledger and the dropped list. The comparison measures how well Foreman understands them, and a miss is a missed-ask lead.
  Done when: the sealed prediction is stored with a hash before the generation starts, and the report scores it against the steers that actually arrive.

- **(wild) Rehearse a week of silence** — FEATURE — value 3 — effort L — risk med — category: unattended
  Why: the user's rules assume long unattended runs with real limits waited out. A scripted fake user says nothing for a simulated week on a fixture repo. The check is that spend stays under the stall cap and held items stay held. The final report must list every dead end that needed the user.
  Done when: the run ends with zero unreviewed pushes beyond the grant and a ranked list of what is waiting on the user.

Next question: Which of the user's recurring corrections have a repeat rate that Foreman has never measured, and what is the cheapest outside signal that would show it?
Next question: When two of the user's steers conflict in practice rather than on paper, which one has Foreman actually obeyed so far, and does anyone know?
