# Brainstorm — lens: 2030 worked back

- **Audit the cheap stage's false kills by sampling** — FEATURE — value 5 — effort M — risk low — category: moonscale
  Why: Standing rule says no idea is killed for ambition, but the funnel's exact, embedding and local-model stages cut cheapest-first. Nothing estimates how many good moons they drop. In 2030 the funnel will be 100x larger and judged by models nobody here has met.
  Done when: each funnel run draws 1% of every stage's kills at random, judges them at full cost, and prints a false-kill rate per stage. A planted known-good moon is caught at the expected rate.

- **Plant duplicates to measure dedupe recall at 10,000** — FIX — value 4 — effort S — risk low — category: moonscale
  Why: The char-shingle fallback is recorded but never scored. At scale, silent dedupe misses flood the grid with reworded moons.
  Done when: a harness injects 200 paraphrased copies of stored moons, and the scorecard reports recall for the embedding path and the fallback path, failing below a stated floor.

- **Replay the funnel at 2030 prices** — PERFORMANCE — value 4 — effort M — risk low — category: moonscale
  Why: Today's funnel order (cheap first) assumes frontier tokens are costly. Re-running the cost split with local tokens at 1/100 and the candidate count at 10^6 shows which stages become pointless and which become the bottleneck, whether the dedupe's memory use or the human review step. Assumption: the cost curves are a parameter table.
  Done when: `sampo moons plan --era 2030` prints per-stage time, memory and dollars at 10^6 candidates, and names the first stage that breaks.

- **Partition the candidate store by generation with a manifest** — CLEAN — value 3 — effort M — risk med — category: store
  Why: A single `candidates.jsonl` plus an append-only funnel log is fine at 10^4. At 10^6 each read of it costs seconds, and a torn write damages every generation at once.
  Done when: a 1M-row synthetic store loads a single generation in under 200 ms, and a torn tail in one shard leaves the others readable.

- **Migrate embeddings lazily through a dual index** — FEATURE — value 3 — effort M — risk med — category: moonscale
  Why: Embedders will change before 2030, and the pack lists three pinned candidates (qwen3-embedding, bge-m3, nomic). Dedupe must not silently compare vectors from two models.
  Done when: switching the embedder serves reads from the old index while new rows are re-embedded in the background, and a count shows when the cutover completes with zero mixed-model comparisons.

- **Gate stage 3 on a falsifiable 2030 headline** — FEATURE — value 4 — effort S — risk low — category: moonshot quality
  Why: Moons were criticised as "not wild", and the pack already holds a wildness score. A dated headline that a cold child can try to refute, because it needs a measurable future state, filters out rewordings of today's features. Assumption: this is distinct from the listed "backcast to a 2030 sentence" in that it blocks promotion.
  Done when: a moon without a headline naming a checkable 2030 state cannot advance, and a cold child's refutation attempt is stored with the verdict.

- **Keep a rejection corpus with judge rationale for later re-judging** — FEATURE — value 4 — effort M — risk low — category: moonscale
  Why: A 2030 judge will be stronger than any model Sampo has now. Storing each kill with its stage, the model id and the confidence lets a later model re-adjudicate only the low-confidence kills, cheaply.
  Done when: a new model id triggers a re-judge of kills under a confidence threshold, and the report lists any flips.

- **Wild: Fit climate envelopes to moon families** — FEATURE — value 4 — effort L — risk med — category: forecasting
  Why: Ecology lens: a species' range is modelled from climate variables. Here the variables are the host's release cadence, local-model quality and embedder price, and the output is which families stay viable through 2030 and which get absorbed by the host.
  Done when: each family carries an envelope with a viability horizon, and a held-out backtest on 2025 to 2026 host releases predicts at least one real absorption.

- **Wild: Read a sediment core of the funnel** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: Palaeoecology reconstructs past communities from stacked pollen layers. A web UI strip shows each generation's family mix as a layer, so a 2030 maintainer can see which niches were empty in 2026 and when diversity collapsed.
  Done when: the page renders one layer per generation from the funnel log, and clicking a layer lists its families and survivors.

- **Wild: Bury a germination vault of failed spikes with wake predicates** — FEATURE — value 4 — effort M — risk low — category: not-yet
  Why: The not-yet.md rule already requires blockers. This makes each blocker a machine-checkable predicate, such as "an embedder under 1 GB exists" or "the host ships subagent hooks", checked on each new model id or release.
  Done when: flipping a stubbed predicate re-queues its spike, and the report names the blocker that lifted.

- **Wild: Run a 2030 apprentice exam on the funnel itself** — FEATURE — value 3 — effort M — risk med — category: moonshot quality
  Why: A tool-less child gets only the store's schema and a README and must file three valid moons. If it can't, the write rules aren't legible to a stranger agent.
  Done when: the child's moons pass the write-time checks without help, and its failures are listed as doc fixes.

- **Set a review budget of three moons per morning** — FEATURE — value 3 — effort S — risk low — category: moonscale
  Why: At 10^4 to 10^6 candidates, human attention is the scarce resource. Capping the slate at three moons scoring wild 4 or more, each with its evidence and dissent, fits the user's complaint ("not that wild") and their rule against interruptions.
  Done when: the morning card never lists more than three moons, each with a wild score of at least 4.

Next question: Which funnel stage's verdicts has the user ever overridden by hand, and does the false-kill audit agree with that record?
Next question: What would the smallest 2030 host (one that ships native goals, memory and subagents) leave of the moons catalogue?
