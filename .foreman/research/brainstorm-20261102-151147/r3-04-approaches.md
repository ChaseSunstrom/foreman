# Brainstorm — lens: approaches

- **Grade grounding by acceptance sampling, not "spot checks"** — FEATURE — value 4 — effort M — risk low — category: grounding
  Why: the pack records a grounding pass where 3 of 4 slate items were already built or mis-stated, and Mission 6 asks for spot checks on each claim. Treat each brief's claims as a lot, stratified by claim class (built, effort, file exists, external host). Sample per class and stop only when the upper bound on that class's error rate is under a set figure. The error rate per class also shows which claim kinds to check first.
  Done when: `fm ground --sample` prints a per-class sample size, a measured error rate and an upper bound, and a fixture with 20% planted false "already built" claims is rejected.

- **Mine the model's own wishes from transcripts** — FEATURE — value 4 — effort S — risk low — category: demand source
  Why: assumption: session logs hold sentences like "there's no way to", "I can't", "workaround" and "Foreman doesn't". The pack's demand sources are the user's words and Foreman's own ledgers, and nothing reads what the agent says it lacked.
  Done when: `fm friction --agent-voice` lists the top 10 phrases by count from the last 30 days of logs, each with a session pointer, and files unmatched ones as capture items.

- **Re-run a lens only over what changed since its last run** — PERFORMANCE — value 4 — effort M — risk low — category: brainstorm cost
  Why: the pack shows 525 ideas and a map taken at an older HEAD, so every brainstorm re-pays for settled ground. Key each lens's last run to a hash of the files under its area. The next run packs only the changed areas plus a 30-line digest of the rest.
  Done when: after a one-file edit the brainstorm pack shrinks to under 30% of the full size and names the area it kept.

- **Chain backward from each DONE-WHEN clause to its falsifiers** — FEATURE — value 4 — effort M — risk low — category: exhaustive thinking
  Why: gen-0's DONE-WHEN is the one finite list the tower must satisfy, and the brainstorm so far only generates forward. For each clause a child lists how it could be false while every current gauge stays green. Those cases are filed as probes.
  Done when: every DONE-WHEN clause has at least one listed falsifier, each with a runnable probe or an explicit "no probe possible" reason.

- **Rank ideas by scorer disagreement, not mean score** — FEATURE — value 3 — effort M — risk med — category: ranking
  Why: assumption: ideas that three differently-configured scorers rate the same are the safe middle. The hidden gems and hidden harms sit where they split, and that is where the user's judgement is needed. The existing cold-read tiers compare verdicts only for pass/fail, not for value.
  Done when: a slate prints a "split" column and the top 5 by split are listed separately from the top 5 by mean.

- **Set-cover the catalogue to a build kernel** — CLEAN — value 3 — effort M — risk low — category: catalogue
  Why: the catalogue is 500+ ideas with heavy overlap, and the pack already notes "Collapse the catalogue into a subsumption tree" without a selection rule. Greedy set-cover over the coverage grid cells picks the smallest idea set that fills every cell. Dominated ideas are archived with the id of the idea that dominates them.
  Done when: `fm catalogue --kernel` prints the kernel size and every archived idea carries a dominator id, with all grid cells still covered.

- **Zero-token candidate generator: operators × the verb table** — FEATURE — value 3 — effort S — risk low — category: generation
  Why: gen-0's rule is that a free arm beats a session arm where it can. Apply fixed operators (merge, split, invert, delegate, schedule, undo, explain) to each row of the verb table to emit candidate lines. Models then only judge, which saves tokens and gives repeatable coverage.
  Done when: running it twice yields identical output, and at least 20 candidates survive a dedupe against the catalogue.

- **Constraint roulette lens (wild)** — FEATURE — value 3 — effort S — risk low — category: lens
  Why: assumption: children converge on additive verbs. Give each child one drawn constraint (no new file, no model call, offline, under 10 lines, no new verb) so its ideas take a different shape.
  Done when: a brainstorm run logs each child's constraint, and the share of ideas that add a verb falls below the unconstrained baseline.

- **Hybrids that must shrink the catalogue (wild)** — FEATURE — value 3 — effort S — risk low — category: combination
  Why: this round asks for combinations worth more together. Pair ideas from the two farthest clusters by a deterministic rule. A hybrid is accepted only if it replaces at least two existing briefs, so crossover subtracts as well as adds.
  Done when: `fm ideas --cross` prints pairs and hybrids, and each accepted hybrid names the two or more briefs it supersedes.

- **Life-event deck: forty things that happen to the owner (wild)** — FEATURE — value 3 — effort M — risk low — category: scenarios
  Why: every slate so far assumes one user in steady state. Cards such as "a second developer joins", "the repo goes public", "laptop stolen", "new model ID replaces the pinned one" or "license audit" each ask what Foreman does on day one. Gaps found become briefs, and cards are redrawn each generation.
  Done when: the deck lives in a file, a child answers each card from MASTER.md alone, and unanswerable cards are listed as gaps.

- **Hardest-buyer FAQ as a doc-gap detector** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: the README claims "discipline layer for coding agents", and the likeliest objection is "why not plain Claude Code?". A tool-less child writes the 20 hardest sceptic questions. Any question MASTER.md cannot answer is a gap, either a missing doc or a missing capability.
  Done when: each question is marked answered (with a MASTER.md line) or unanswered, and the unanswered ones are filed.

- **Tell a dry lens from a failed child before scoring it** — FIX — value 3 — effort S — risk low — category: measurement
  Why: the pack's recurring gap is gauges that read green while broken, and lens dry-rates feed lens scaling (T-0829). A child that times out looks the same as a lens with nothing new to say.
  Done when: a lens ledger row carries `ok`, `empty` or `failed`, and a planted timeout is recorded as `failed`, not counted in the dry rate.

- **Fertility-weighted lens budget from idea lineage** — PERFORMANCE — value 2 — effort M — risk med — category: allocation
  Why: assumption: the pack already says round-2 ideas should cite what they extend. Track parent→child ideas and give the next round's budget to lineages that produced accepted work.
  Done when: a round plan shows each lens's budget and the accepted-descendant count that set it.

Next question: which claim classes in briefs have the highest measured false rate today, and is that already recorded anywhere that a sampler could read?
Next question: what does the user do with a slate in the first 60 seconds, and could a lens predict that behaviour better than it predicts value?
