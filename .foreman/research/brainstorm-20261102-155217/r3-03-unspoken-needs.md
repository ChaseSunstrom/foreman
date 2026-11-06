# Brainstorm — lens: unspoken needs

- **Collapse the catalogue into a "what I'd actually do Monday" list of five** — FEATURE — value 5 — effort M — risk low — category: triage
  Why: the user keeps filing and then dropping brainstorm items (c16, c17, c21 dropped after re-grounding); 525 ideas plus a very long "ideas so far" list, and ~30 "Later from" deferred tasks, suggest the unspoken need is fewer, decided items, not more. assumption: the user wants selection pressure, not generation.
  Done when: `fm next --monday` prints at most 5 items, each with the user's own prior words that justify it, and a test shows it never lists a dropped or deferred-as-duplicate item.

- **Show which side wins when the user's hand and Foreman's hand both change something** — FEATURE — value 4 — effort M — risk med — category: trust
  Why: the pack's open question ("which side does each reader trust?") and the dropped task_done item (removing ledger lines breaks the hash chain) show hand edits are an unmodelled path. assumption: the user edits queue/ledger files directly at times.
  Done when: a test hand-edits a task file, the ledger and the tree, and `fm doctor` names each divergence and which side every reader used.

- **Print a "while you were away" card with money, closes, stops and one reason** — FEATURE — value 5 — effort S — risk low — category: unattended
  Why: steers say never stop for budget, wait out limits, run unattended; the user's unspoken need is knowing in ten seconds what happened overnight without reading ledgers. Receipts exist but are per-run (T-2669 stall receipt).
  Done when: session start after an unattended `fm run` prints ≤8 lines including dollars spent, tasks closed, stop reason and the one thing needing the user, verified by a fixture ledger.

- **Flag when a new ask contradicts a standing steer before work starts** — FEATURE — value 4 — effort M — risk med — category: steers
  Why: 40+ steers accumulate; the user corrects the same classes repeatedly (T-2583 criterion contradicting its own example; "steered" items). assumption: the user forgets older steers.
  Done when: filing a task whose text violates a fixture steer prints the steer, its date and a keep/override choice, and the override is recorded.

- **Ask what "simplify" means once, then store it as a measurable preference** — FEATURE — value 3 — effort S — risk low — category: preferences
  Why: the earlier open question; the user's drops lean toward deleting and subtracting while Genesis keeps growing. assumption: the answer is one of fewer verbs, shorter output, fewer decisions.
  Done when: `fm decide` holds a simplify-meaning record and `fm lean` reports against that dimension.

- **Mark each blocked task with the single user action that frees it, ranked by count freed** — FEATURE — value 4 — effort S — risk low — category: blocked work
  Why: T-0325, T-0335/36/37, T-0352, T-0418 are blocked for months on pacman installs, other CLIs and a version update only the user can do. assumption: the user would act if shown one list.
  Done when: `fm blocked` lists actions with the number of tasks each unblocks, and the top entry matches a fixture.

- **Test the first minute after a silent fail-open** — FIX — value 4 — effort M — risk med — category: safety
  Why: an earlier question left unanswered; the user runs bypass mode and relies on the guard, so an invisible off-state is the worst surprise.
  Done when: a test breaks the guard import, starts a session, and asserts a visible degraded line appears in the first output.

- **Pre-answer "did it do what I meant" with their own sentence beside the evidence** — FEATURE — value 3 — effort M — risk low — category: proof
  Why: the many proof-ideas in the pack never place the user's verbatim words beside the result; the unspoken need is checking intent, not tests passing. assumption.
  Done when: the finish card quotes the originating ask and lists proof lines mapped to its clauses.

- **Estimate review minutes a day's work asks of the user** — FEATURE — value 3 — effort S — risk low — category: attention
  Why: heavy autonomy has moved the bottleneck to the user's review; nothing in the pack measures it.
  Done when: the finish card prints "~N min to review" computed from diff size and unproven count, with a fixture test.

- **(wild) Seal tomorrow's three likely asks at day close and show only the hits** — FEATURE — value 3 — effort M — risk low — category: anticipation
  Why: current Mission 7 is anticipation; sealed predictions give a score without ever bothering the user. wild
  Done when: next morning `fm anticipate score` prints hits/misses against a recency baseline.

- **(wild) A "things I decided for you" monthly ledger with a one-key veto** — FEATURE — value 3 — effort M — risk med — category: autonomy
  Why: the rule "never block on the user; record with fm decide --kind costly" piles up silent decisions the user never sees until the final report. wild
  Done when: `fm decide --month` lists decisions with a veto command that re-opens the affected task.

- **(wild) Replay the user's last week of asks and predict only the gaps** — FEATURE — value 2 — effort L — risk low — category: anticipation
  Why: a way to measure whether Foreman understands their rhythm without live risk. wild
  Done when: a script reports the share of the week's asks that a predictor from the prior weeks covered.

- **Keep the catalogue's use evidence next to each entry** — CLEAN — value 3 — effort M — risk low — category: measurement
  Why: the open question about what fraction of the 525 ideas has measured user-felt value.
  Done when: each catalogue row shows asked/dropped/shipped counts, and a report prints the measured fraction.

Next question: which of the user's drops were reversed later, and what does that say about when re-grounding is wrong?
Next question: what does the user do in the five minutes after a Foreman push to main?
