# Brainstorm — lens: 2030 worked back

- **Bind every completion word to a run** — FEATURE — value 5 — effort M — risk med — category: meaning
  Why: the largest unproven class is meaning (599), and finish text says "fixed" or "all passing" without naming a run. Assumption: the Stop hook can read the final message.
  Done when: a finish message containing "fixed", "works" or "all" with no cited ledger run id is held, and a planted unbacked claim is caught in a test.

- **Make an executable glossary of the user's nouns** — FEATURE — value 4 — effort M — risk low — category: meaning
  Why: example assertions use terms such as "active" or "stale" that no check defines. Assumption: terms recur across specs.
  Done when: a criterion naming an undefined glossary term is labelled unproven with that term, and defining it with a query makes the criterion runnable.

- **Score a spec's checkability before planning** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: spec examples become criteria at plan time, but some specs contain no checkable sentence. A zero-token score would say so before a plan is built.
  Done when: intake prints "k of n sentences checkable" with the unchecked ones highlighted, and a prose-only spec scores 0.

- **Derive metamorphic checks from spec words** — FEATURE — value 4 — effort M — risk med — category: criteria
  Why: examples cover points, but "idempotent", "order doesn't matter" and "at most N" are relations. Assumption: a small word-to-relation table covers the common cases.
  Done when: a spec saying "idempotent" produces a run-twice-and-compare criterion that fails on a planted non-idempotent function.

- **Diff refactors against real recorded inputs** — FEATURE — value 4 — effort M — risk med — category: differential proof
  Why: unit tests are the only proof of "behaviour unchanged". Hook and ledger inputs from real sessions are an unused corpus.
  Done when: a task tagged refactor replays the recorded inputs through the old and new trees, and a planted behaviour change shows as a diff.

- **Show behaviour forks for the user to pick** — FEATURE — value 4 — effort M — risk low — category: meaning
  Why: the user's pushbacks ("I want wild", "not jarvis") were meaning misses that a concrete output would have exposed.
  Done when: for an ambiguous noun, intake shows two concrete outputs for one input, one keypress picks, and the pick is stored as a criterion.

- **Offer proof tiers with their blind spots** — FEATURE — value 3 — effort S — risk low — category: proof menu
  Why: "unproven" is binary today. A cheap, medium and deep tier would each print what that tier cannot catch.
  Done when: planning lists three tiers with cost and a "cannot catch:" line, and the chosen tier is on the close receipt.

- **Retire verdicts when their judge is retired** — SECURITY — value 4 — effort M — risk low — category: model churn
  Why: public text must name models by role, and roles re-resolve to new models. A verdict from a model that no longer fills the role should not read as current.
  Done when: changing the model behind a role marks old judge-based verdicts "judge retired, re-judge pending" and lists them.

- **Set re-check cadence from measured claim half-life** — PERFORMANCE — value 3 — effort M — risk low — category: freshness
  Why: 421 docs claims are unchecked, and re-running all of them is costly. Assumption: some classes, such as host-behaviour claims, go stale much faster.
  Done when: `fm` prints a per-class survival rate and schedules re-checks by it, and a test shows the fast-decaying class is re-checked first.

- **Show unproven claims as editor diagnostics** — FEATURE — value 3 — effort M — risk low — category: developer experience
  Why: T-0788 defers LSP, and a doc line's proof status is invisible where the user edits.
  Done when: opening a doc with an unproven claim shows an info diagnostic on that line with its reason.

- **Wild: Publish a claims file for other agents** — FEATURE — value 3 — effort S — risk low — category: surfaces — wild
  Why: by 2030 other agents will read the site before adopting a tool. The site would serve `/.well-known/sampo-claims.json` listing each public claim, its proof status and run link, with roles only and no vendor or machine names.
  Done when: the file validates against the vocabulary lint and every site number appears in it with a status.

- **Wild: Let a reader file a counterexample** — FEATURE — value 3 — effort M — risk med — category: community proof — wild
  Why: the "show me" panel proposed so far is one-way. Assumption: a local-first button that writes a task file is enough, with no hosted service.
  Done when: a counterexample pasted against a claim becomes a task whose criterion is that example, and the claim shows "contested".

- **Wild: Run the criteria block through a deliberately weak orchestrator** — FEATURE — value 4 — effort M — risk low — category: orchestrator-neutral — wild
  Why: the steer says any agent must work. If the weakest local model cannot follow a criteria block, the block is too clever for the agents of 2030.
  Done when: each generated block is run through a small local model on a fixture, and a block it fails to execute is flagged.

- **Publish the false-close rate with an interval** — FEATURE — value 4 — effort M — risk med — category: measurement
  Why: "proven" claims need a measured base rate that Sampo did not author. Assumption: 14-day reopen and revert signals are enough.
  Done when: `fm outcomes` prints a rate with a confidence interval and its sample size, and a sample under 10 prints "too few".

Next question: Which of the 599 meaning-class items would a glossary or a behaviour-fork pick have settled, and does a sampled count show it?
Next question: When two orchestrators run the same criteria block and disagree, which one's reading is recorded as the evidence?
