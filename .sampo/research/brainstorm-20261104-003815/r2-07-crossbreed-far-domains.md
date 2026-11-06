# Brainstorm — lens: crossbreed far domains

- **Breed moons by affinity maturation** — FEATURE — value 5 — effort M — risk low — category: funnel
  Why: assumption: the 10,000-candidate funnel mostly filters. Nothing in the pack improves a survivor. Immunology clones the best binders, hypermutates them with the local model, and re-scores them against the "antigen", here the user's wildness and value rubric.
  Done when: for 20 moons that reach the top tier, `sampo moons mature` makes 8 mutants each and at least one mutant per moon outscores its parent on the blind wild-rater; a run log shows parent and child scores.

- **Cull by negative selection against boring** — SECURITY? no, FEATURE — value 5 — effort M — risk low — category: funnel
  Why: the user said the moons "aren't that moon-y". Immune systems kill any T-cell that binds "self". Here "self" is every moon the user rejected or the cold rater scored wild ≤2. Generate detector embeddings from those and drop any new candidate that falls near one, at zero tokens.
  Done when: replaying the rejected set through the detectors drops ≥80% of them, while the user-accepted set loses ≤10%, both on held-out data.

- **Anchor wildness with a Mohs kit** — FEATURE — value 4 — effort S — risk low — category: rating
  Why: wildness scoring drifts by rater and model. Mineralogy fixes this with five reference minerals and scratch tests. Keep one frozen reference moon per wild level 1–5. The rater compares a candidate pairwise against the kit ("scratches level 3, not 4") instead of scoring in the abstract.
  Done when: two different raters give the same level to ≥85% of 100 candidates, up from the current agreement, which is recorded first.

- **Train a seismic early-warning surrogate** — PERFORMANCE — value 4 — effort M — risk med — category: funnel
  Why: P-waves arrive before the damaging S-waves. Cheap features (embedding, length, verb overlap) can predict the expensive cold-review score. Fit a small regressor on past cold-review verdicts and use it as a stage between dedupe and the local model.
  Done when: the surrogate reaches Spearman ≥0.5 on held-out cold-review scores and cuts local-model calls ≥30% with no loss of top-decile recall.

- **Alert on the difference, like a sky survey** — FEATURE — value 4 — effort M — risk low — category: novelty
  Why: astronomy surveys subtract the last image from the new one and alert only on new sources. Embed each generation's candidate field, subtract the stacked previous fields, and send only candidates in empty regions to the funnel. This also stops re-proposing ideas that were already dropped.
  Done when: on a replay of gen 3 against gen 4 candidates, ≥90% of known near-duplicates of old ideas are suppressed before any model call, and a planted novel idea survives.

- **Assay each moon's fineness** — FEATURE — value 3 — effort S — risk low — category: quality
  Why: the forge theme and the "Today you can't / With this, you can" rule. Assaying strips off the slag and weighs the metal. Count the share of a moon's text that is checkable claims, and stamp a karat (e.g. 18k) on it. Low-fineness moons go back to a rewrite lane before the cold read.
  Done when: `sampo moons assay` prints a fineness value for every candidate, and fineness correlates positively with cold-read pass rate on 200 past moons.

- **Cast the cladogram of ideas** — FEATURE — value 3 — effort M — risk low — category: provenance
  Why: linguists rebuild language trees from shared innovations. Cluster moons by shared distinctive phrasing and mechanism words, then separate inherited traits from convergent reinvention. A root with many descendants shows which lens or seed is productive. Reinvention across branches is a quorum signal.
  Done when: the tree for ≥500 moons renders as one file, and each lens and model gets a descendants-per-root figure.

- **Find index fossils for each generation's tics** — CLEAN — value 3 — effort S — risk low — category: quality
  Why: geologists date strata by marker fossils. Phrases that appear in 1 generation but not others ("mycorrhizal ledger", "wild:") are its slop fingerprint. Find them by comparing n-gram frequency across generations, then add them to the generator's ban list and the rater's penalty list.
  Done when: the next generation's fossil-phrase rate drops ≥50% against gen 4, measured by the same detector.

- **Sketch with MinHash across repos** — SECURITY — value 3 — effort M — risk low — category: privacy
  Why: the user runs Sampo on several repos and moons are deduped within one store. MinHash sketches (no text) of each candidate can be compared across repos or with a friend's install, so duplicates are found with nothing sent. This matches the local-first rule.
  Done when: the cross-repo dedupe finds a planted duplicate between two stores while the sketch file contains no recoverable sentence, checked by a grep for 5-word windows.

- **Anneal the wildness temperature** — FEATURE — value 3 — effort S — risk low — category: generation
  Why: assumption: all candidates use one prompt temperature. Annealing starts hot, accepts bad and strange ideas, and cools as the pool fills. Schedule generator temperature, the rubric's wildness floor and the dedupe threshold across the rounds of a run.
  Done when: a 3-round run logs a temperature per round, and the later rounds have a lower share of duplicates than a fixed-temperature control run.

- **Wild: Open booster packs of moons on the phone** — FEATURE — value 3 — effort M — risk low — category: devices
  Why: wild. Trading-card games train taste through packs. Five moons per pack with rarity set by wildness; the user keeps, burns or "trades" each, which gives preference pairs for the rater. A binder shows the collection by family.
  Done when: a phone-width page serves a pack, and 20 swipes write 20 labelled rows to the preference store.

- **Wild: Draw the 10,000 moons as a world map** — FEATURE — value 4 — effort L — risk med — category: ui
  Why: wild. Cartography at scale: embedding positions become continents (families), elevation is wildness, rivers are ancestry, and levels of detail appear as you zoom. Empty ocean marks unexplored niches; a click sends a generation lane there.
  Done when: the web UI renders 10,000 points at 30 fps with zoom, and clicking an ocean region files a brief naming it.

- **Wild: Sonify the funnel as ambient audio** — FEATURE — value 2 — effort M — risk low — category: devices
  Why: wild. Unattended nights are silent. A local synthesis turns stage throughput into a drone and kills into soft percussion. A top-tier hit is a single bell, and a stalled stage goes quiet. The user can tell the funnel's health with eyes closed.
  Done when: a command plays a 60 s rendering of a logged run, and a stalled stage is audibly distinct from a flowing one (verified by a spectrum check).

- **Wild: Tablebase for settled feasibility questions** — PERFORMANCE — value 3 — effort M — risk med — category: funnel
  Why: wild. Chess solves endgames once and looks them up. Questions like "does a hook event exist for X" or "does a verb already do Y" recur across thousands of moons. Store each answer keyed by normalised question plus repo hash, and invalidate it when the cited file changes.
  Done when: a 1,000-moon run answers ≥40% of feasibility questions from the table, and all of them match a fresh check on a sample of 50.

Next question: which of these crossbreeds survives the user's "wild" test once a blind rater scores their own output, not just the moons they generate?
Next question: when one far domain is borrowed, what is the exam that tells a real mechanism from a metaphor, and who writes it?
