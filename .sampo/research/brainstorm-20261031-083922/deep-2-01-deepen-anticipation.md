# Brainstorm — lens: deepen: anticipation

- **Build a prediction book with a scoreboard** — FEATURE — value 5 — effort M — risk low — category: anticipation
  Why: T-2290 scores effort predictions only. "Score the predicted next request" and "prediction book" are separate ideas; one ledger (kind, predicted, actual, baseline, hit) lets them share scoring.
  Done when: `fm predictions` lists every prediction kind with hit rate and the naive baseline's rate beside it, from stored rows.

- **Mute predictors that lose to the baseline** — FEATURE — value 5 — effort S — risk low — category: anticipation
  Why: The steers demand signals Foreman didn't author. A predictor under "most recent repeat" after N scored rows should stop drafting and surfacing.
  Done when: A test feeds a predictor 20 misses against a baseline; it is muted, and `fm doctor` names it and the unmute command.

- **Draft the predicted request as a plan-only lane** — FEATURE — value 4 — effort M — risk med — category: speculation
  Why: The Mission 8 text says it "drafts it on spec in a lane". Limiting the draft to a plan plus failing tests keeps cost small and nothing can land unasked.
  Done when: A predicted request makes a lane holding a plan and red tests, with no push and no merge, labelled "speculative" in `fm lanes`.

- **Adopt a speculative draft when the real ask overlaps it** — FEATURE — value 4 — effort M — risk med — category: speculation
  Why: A draft is wasted when the ask differs slightly. At intake, compare the ask's scope paths and words to open drafts; above a threshold, offer to adopt one with the diff shown.
  Done when: A test ask overlapping a draft by ≥60% of scope paths gets the draft attached to its task; one under 20% leaves it untouched.

- **Learn from plan edits after acceptance** — FEATURE — value 4 — effort M — risk low — category: user model
  Why: An earlier question asks which plan edit is most common after acceptance. The edits are the signal; add the repeated one (for example, a missing Risks line) to the draft before acceptance.
  Done when: After 3 identical post-accept edits, the next plan carries that edit pre-applied and marked "learned", and the user's reversal is recorded.

- **Predict the correction before delivery** — FEATURE — value 4 — effort M — risk med — category: user model
  Why: Corrections are recorded as steers and "asked" rows. Before `fm task finish`, check the diff against past correction patterns, such as a test file naming or the 6,400-char rules budget (the ship-red example), and flag the likely one.
  Done when: Replaying a closed task's diff against corrections recorded before it flags the one the user later made.

- **Predict the next un-parked task** — FEATURE — value 3 — effort S — risk low — category: ranking
  Why: The open work is mostly deferred or blocked. Rank them by what the user's recent words, touched paths and unblockers point at, and put the top one into the `fm next` footer.
  Done when: Scored against actual un-park events, top-3 hit rate appears in `fm predictions`; an unblocker like libappindicator being installed moves T-0325 up.

- **Predict follow-up edits to a just-closed task** — FEATURE — value 3 — effort M — risk low — category: foresight
  Why: Fix chains are visible in the pack (T-2283, then a dropped duplicate of the same baseline red; T-2298 absorbing a sibling). Co-change history with `fm graph blast` can name the likely second touch.
  Done when: At close, Foreman lists up to 2 files likely to change within a week, and the hit rate is scored on later commits.

- **Pre-warm the repo before the habitual start** — PERFORMANCE — value 3 — effort S — risk low — category: foresight
  Why: The lean steers say hooks stay fast. Learn the user's usual start hour from session-start events and run the zero-token work (`fm find`, doctor cache, map) just before it.
  Done when: First `fm doctor` after a habitual start is a cache hit, with warm-up time on record and an off switch.

- **Time-box every prediction and give it a mute switch** — CLEAN — value 3 — effort S — risk low — category: safety
  Why: The lean and guard steers hold for new loops. Each prediction row carries a TTL, a token cap and a per-kind `fm predict off KIND`, and expired drafts' lanes are removed.
  Done when: A draft past TTL has no lane left, and a muted kind creates nothing in a test.

- **Wild: Ghost-user lane that runs the predicted ask blind** — FEATURE — value 4 — effort L — risk med — category: speculation
  Why: wild. A throwaway child attempts the predicted request with no hints and records its first question, which is a gap in the plan, intake or docs. It could answer the open question on what to do while the user waits.
  Done when: A ghost run writes "first question" and its answer is in the task's Assumptions before the user types the ask.

- **Wild: Overnight dry-run of tomorrow's first task** — FEATURE — value 3 — effort L — risk med — category: speculation
  Why: wild. Run the predicted first task in a throwaway worktree with the tests only, so the morning brief says "this will probably be red because X". Fits the existing Mission 8 trigger table.
  Done when: The morning brief carries a pre-mortem line for the top prediction, scored later against the real first-task outcome.

- **Wild: Let the user bet against the book** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: wild. `fm predictions bet` lets the user pick yes or no on a prediction. A disagreement is a free labelled example, a second signal beyond what Foreman wrote.
  Done when: A bet is recorded, scored at resolution, and the user's calibration versus Foreman's is shown.

- **Wild: Review the user's hand-made commits in the background** — FEATURE — value 3 — effort M — risk low — category: foresight
  Why: wild. Commits the user makes outside tasks are unreviewed by the gates. A cold read by a different model flags missing tests or budget breaches and queues a FIX.
  Done when: A hand-made commit gets a note within a minute, and a planted missing-test commit yields a queued FIX.

Next question: Which prediction kinds would the user actually accept being wrong about, and what wrong-draft cost, in tokens or interruption, would make them turn the whole thing off?
Next question: Are there signals of the user's intent outside Foreman, such as their editor, issue tracker or CI, that predict the next ask better than Foreman's own history?
