# Brainstorm — lens: brainstorming and ideation methods

- **Route each problem to a named ideation method** — FEATURE — value 5 — effort M — risk low — category: brainstorming
  Why: lenses in `fm ideas` are fixed per run, and today's lens list is the only variety. A catalogue of techniques (inversion, SCAMPER, constraint removal, TRIZ contradictions, analogy, first principles, abstraction ladder) as small prompt cards would let intake pick two or three that fit the task type. After finish, log which method produced the surviving option.
  Done when: `fm ideas --method list` shows at least 8 methods, a FIX and a FEATURE brief pick different ones, and the ledger records method→outcome.

- **Fill a morphological box before listing approaches** — FEATURE — value 5 — effort M — risk low — category: planning
  Why: the brief demands "3+ options for M/L", which tends to give three variants of one idea. Instead, name the independent design dimensions (trigger, where state lives, who acts, sync vs async, build vs reuse), enumerate combinations, prune the infeasible ones, and pick options from distant cells.
  Done when: an M/L brief carries a dimension table and each option cites its cell, and a test fails if two options share all cells.

- **Gate option sets on measured distinctness** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: assumption: options often paraphrase each other. Reject a set when pairwise token or feature overlap is high, and force one "do less", one "reuse an existing fm command" and one "invert the problem" slot.
  Done when: a brief with two near-identical options is refused by `fm task brief` with the pair named, and passes once they are differentiated.

- **Add a blind first round to `fm ideas`** — FEATURE — value 5 — effort S — risk low — category: anchoring
  Why: recursive rounds see prior ideas, which anchors them. The 835-idea pile shows heavy convergence on the same themes (the edit-time sentinel and the dream queue each appear several times). Run round 0 per lens with the pack only, then diff it against the existing pile and report what the blind round found that the pile lacked.
  Done when: `fm ideas --blind` outputs a "new vs already-seen" split with a count, using a fixed fixture pile.

- **Stop brainstorming when novelty saturates** — FEATURE — value 4 — effort M — risk low — category: brainstorming
  Why: the pile has many near-duplicates and the user said "I like almost all of those", so volume is no longer the bottleneck. Compute a novelty rate per round (clusters not already in the pile) and halt or switch lens when it falls below a threshold, instead of running a fixed number of rounds.
  Done when: a replayed 3-round run on a saturated fixture stops after round 2 and prints the novelty rate per round.

- **Rank ideas by pairwise tournament, not scores** — FEATURE — value 4 — effort M — risk med — category: convergence
  Why: the brainstorm skill scores each idea, and the open queue shows C0xx items almost all tied at "value 4/5, effort M". Scores that cluster can't order a queue. Run head-to-head comparisons weighted by the user's keeps and skips (the punch list has skip marks), and get a stable total order.
  Done when: running twice on the same input gives the same top 10, and a skipped-idea fixture drops its neighbours' ranks.

- **Tune lens budgets from which ideas the user keeps** — FEATURE — value 4 — effort M — risk low — category: self-improvement
  Why: the punch list records kept and skipped ideas per lens, but every lens gets equal effort. Weight lens rounds by acceptance rate and decay the weights so unfashionable lenses still get occasional runs.
  Done when: `fm ideas --plan` prints per-lens budgets derived from history, and a fixture where one lens is never accepted shows its share shrinking.

- **Climb the abstraction ladder at intake** — FEATURE — value 4 — effort S — risk low — category: understanding
  Why: intake expands a request into a brief but treats the request as given. Add a "why / how" ladder of two steps up and two down (e.g. "login timeout" → "slow-network resilience" → "every request has a retry budget") and let the brief choose its altitude on purpose. This differs from the XY check, which only flags a mismatch.
  Done when: an L brief includes a ladder of at least 3 levels and a line justifying the chosen level.

- **Replay a plan under forced constraints** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: "do less" appears only as an option. Systematically re-plan under squeezes (half the files, no new command, no new dependency, one hour) and show which steps survive every squeeze. Survivors are the core, so build them first and let the rest wait.
  Done when: `fm plan squeeze T-xxxx` lists the steps that survive at least 3 of 4 constraints, and the drive orders them first.

- **Keep a pattern library that plans can cite** — FEATURE — value 3 — effort M — risk low — category: analogy
  Why: recall finds look-alike tasks inside the project, but cross-domain structure (saga, outbox, circuit breaker, lease, tombstone) comes from the model's memory ad hoc. A short list of named patterns with the problem shape that triggers each lets the plan say "this is a lease problem", and bench can score whether the citation helped.
  Done when: 15 patterns exist, intake cites at most 2 per L brief, and a fixture brief with a claimed pattern fails if the trigger shape is absent.

- **Wild: Fire oblique provocations from the project's own history** — FEATURE — value 3 — effort S — risk low — category: wild
  Why: wild. Like Oblique Strategies, pick a random old reverted commit, dropped request or dead-end note and ask each brainstormer "what would this suggest here?". Forced association from Foreman's own past surfaces ideas that pure lens thinking cannot.
  Done when: `fm ideas --provoke 3` shows three seeded provocations in the pack and the output marks which ideas cite one.

- **Wild: Cross-breed top ideas automatically** — FEATURE — value 4 — effort M — risk med — category: wild
  Why: wild. Rounds are told to combine ideas but nothing does so systematically. Take the top 20 from different categories, build a compatibility matrix, have a child write a one-paragraph fusion for each promising pair, and keep it only if it scores above both parents in the tournament.
  Done when: `fm ideas --cross` outputs fusions with both parent ids, and a fusion that loses to a parent is dropped with the reason.

- **Wild: Let a "devil's idea" argue for the opposite product** — FEATURE — value 3 — effort S — risk low — category: wild
  Why: wild. For each epic, one agent must write the best case for not building it, or for building the opposite (fewer commands, no memory). If the case survives the tournament, the epic is flagged. This pushes against the user's pile of "like almost all of those", which no current lens does.
  Done when: each epic in the roadmap has a counter-brief, and one fixture counter-brief wins and moves its epic to "reconsider".
