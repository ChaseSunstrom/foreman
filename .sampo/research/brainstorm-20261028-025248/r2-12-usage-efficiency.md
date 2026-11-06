# Brainstorm — lens: usage efficiency

- **Route each brainstorm lens to the cheapest model that held its quality** — FEATURE — value 4 — effort M — risk med — category: model routing
  Why: `lens_rates` already records per-lens yield, but every lens runs on the same model. Assumption: the capability-map lens is mostly recall and a smaller model matches the strong one there.
  Done when: a round's per-lens cost table shows at least one lens on a cheaper model with accepted-idea rate within 10% of the strong model's.

- **Set reasoning effort per lens from its measured yield** — FEATURE — value 3 — effort S — risk low — category: thinking budget
  Why: assumption: list-style lenses (capability map, every device) gain little from deep thinking, while "approaches" and "agents of agents" do. The brainstorm pack doesn't set effort per lens.
  Done when: `fm cost` reports tokens per lens at two effort levels, and the cheaper level is picked automatically for list lenses without dropping accepted ideas.

- **Rerun only the lenses whose input sections changed** — PERFORMANCE — value 4 — effort M — risk low — category: incremental rounds
  Why: each round resends the whole pack and reruns every lens, though a round often changes only the user's words or the ideas-so-far list. The pack already has named sections, so each lens can declare which ones it reads.
  Done when: changing only "Recent commits" reruns zero lenses that don't read it, and `fm cost` shows the skipped spend.

- **Filter the user's words per lens by tag** — PERFORMANCE — value 4 — effort M — risk low — category: pack slicing
  Why: the pack contains "The user's own words" twice, and every lens gets the full block even when most entries are about CI or the usage burn. Tagging entries by lens lets each child see only the relevant ones.
  Done when: each lens's pack contains only entries tagged for it or tagged "all", and the total user-words size drops by at least half on this pack.

- **Give children a 1 KB map digest instead of the full repo map** — PERFORMANCE — value 4 — effort M — risk med — category: pack size
  Why: the map runs to 1,835 files, gates, layout and test links, and children have no tools, so they can't look anything up and mostly ignore most of it. Assumption: a short digest plus the evidence check keeps ideas grounded.
  Done when: the map section in each child's pack is under 1 KB, and the evidence check still passes on last round's ideas that cited files.

- **Build the brainstorm slate with a script, not a model** — CLEAN — value 4 — effort S — risk low — category: merge cost
  Why: merging six lenses' outputs and deduping titles can run as deterministic code, since every child already emits a value and an effort field per idea.
  Done when: merging six child outputs uses zero model tokens and reproduces the top 15 from the last round's model-merged slate.

- **Two-tier children: one-line ideas first, bodies for the top five** — PERFORMANCE — value 4 — effort M — risk low — category: output length
  Why: each child writes up to 15 full entries with Why and Done-when lines, but scoring only needs the top few in full. The parent can ask for bodies only after ranking one-line headlines.
  Done when: a round's child output tokens drop by at least 40%, and the top five ideas match those from full-body output on a replayed round.

- **Record cost per accepted idea on each round's scorecard** — FEATURE — value 3 — effort S — risk low — category: efficiency metric
  Why: a round reports ideas filed and spend per gate, but not what each accepted idea cost. That is the number that says whether a round was worth its budget.
  Done when: the round's output ends with dollars per accepted idea, equal to total lens cost divided by accepted ideas.

- **Compact only between lens batches, never mid-fan-out** — PERFORMANCE — value 3 — effort S — risk low — category: compaction timing
  Why: assumption: a compaction that lands between spawning children and joining them forces the parent to resend its context to each child. The 200k setting fires wherever it happens to fall.
  Done when: a test shows no compaction fires between a fan-out's spawn and join.

- **Wild: write all six lenses in one call so the pack is billed once** — FEATURE — value 3 — effort L — risk med — category: call batching
  Why (wild): six independent calls each pay for the full pack, while one call with six sections bills the shared input once. The trade-off is lost independence between lenses, so a cheap second pass could check for cross-lens copying.
  Done when: one call produces six lens sections, the input-token bill is under half of six separate calls, and the copy check flags no lens that repeats another's top idea.

- **Wild: let a child cite a ledger ID instead of rewriting a repeat** — FEATURE — value 3 — effort M — risk low — category: output dedupe
  Why (wild): children spend output tokens restating ideas already in the ledger, and the parent then discards them. A child that cites `L-0412` for a repeat, instead of retyping it, costs about ten tokens.
  Done when: a child that repeats a known idea emits an ID under 15 tokens, and the parent resolves every ID to its ledger entry.

- **Wild: stop each lens when its next idea costs more than its last accepted one** — PERFORMANCE — value 3 — effort M — risk med — category: marginal stopping
  Why (wild): the lens count and idea count are fixed, so late ideas often cost as much as early ones while earning less. Stopping on marginal cost per accepted idea spends the budget where it pays.
  Done when: on a replayed round, the stopping rule keeps every accepted idea from the full run and cuts spend by at least 25%.
