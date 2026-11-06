# Brainstorm — lens: ecology: succession and niches

- **Run the funnel as ecological succession** — FEATURE — value 5 — effort M — risk low — category: moons-at-scale
  Why: the pack's 10,000-candidate funnel is cheap-first, and the ecology lens maps that onto succession. Pioneer stage: local qwen3.8-27b mass-spawns candidates, kept by exact and shingle dedupe only. Shrub stage: embedding dedupe plus the "Today you can't / With this, you can" rule. Climax stage: cold wildness review. Each stage's survivors carry an "age" and the stage that admitted them. Assumption: the funnel log already records per-stage drops.
  Done when: `sampo moons succession` prints per-stage census (entered, survived, median age) from the funnel log, and the stage-1 to climax ratio is within a stated band.

- **Stop generating when the rarefaction curve flattens** — PERFORMANCE — value 5 — effort S — risk low — category: moons-at-scale
  Why: nothing in the pack says when 10,000 candidates is enough. Species-accumulation curves answer this: count new families per 100 candidates and halt the pioneer stage once discovery falls under a threshold, so local-model hours go to a different lens.
  Done when: a run on a recorded log stops before the cap, and the printed curve's last 5 points show new-family rate below the stated floor.

- **Sample the ecotones between filled grid cells** — FEATURE — value 4 — effort M — risk low — category: grid
  Why: edges between habitats hold the most species. Pair two adjacent filled coverage cells (e.g. Ward × web UI and lanes × phone) and ask the local model for a candidate that only exists at the seam. This is the combination step the standing rule on empty cells doesn't cover. Assumption: coverage.md cells are machine-readable.
  Done when: `sampo moons ecotone` emits N candidates each citing two parent cells, and the family tags show a family that no single-cell run produced.

- **Force character displacement between near-duplicate moons** — FEATURE — value 4 — effort M — risk med — category: dedupe
  Why: dedupe currently kills near-duplicates. Competitive exclusion suggests a better rule: when two candidates share a niche (cosine over threshold), the later one must re-target to a differing "Today you can't" line or die. This turns duplicates into spread.
  Done when: on a seeded pair, the funnel logs a displacement attempt and the survivor's embedding distance from its twin is above the niche radius.

- **Keep a seed bank of dormant moons with germination predicates** — FEATURE — value 5 — effort M — risk low — category: not-yet
  Why: the standing rule says failed spikes go to not-yet.md with their blocker and every Seed retries them. Make that mechanical: each dormant moon stores a machine-checkable blocker predicate (a verb exists, a model profile loads, a host version) and germinates by itself when it flips.
  Done when: flipping a stub predicate in a test moves exactly one moon from not-yet to the pioneer queue with a log line naming the predicate.

- **Burn the deferred backlog on purpose and count resprouters** — CLEAN — value 3 — effort M — risk med — category: backlog
  Why: about 35 deferred "Later from T-07xx/08xx" items sit open (T-0788 to T-0869). Fire ecology: archive a tranche to a tombstone, and only items a session or user re-asks for within a window resprout. Survivors are the real demand; the rest are not "killed", they are dormant per the no-kill rule.
  Done when: a dry-run burn lists the tranche, and an undo restores every item byte-for-byte.

- **Add a trophic energy pyramid across model tiers** — PERFORMANCE — value 4 — effort M — risk low — category: models
  Why: local models are bulk "producers", embeddings are "herbivores", frontier cold reviewers are "predators". Enforce a roughly 10:1 call ratio per tier and flag a run where predators eat producers' output uncurated, which is what a cheap-first funnel exists to prevent.
  Done when: the funnel report shows calls per tier and fails the run if the top tier exceeds its ratio.

- **Wild: Gate promotion on quorum sensing across independent lineages** — FEATURE — value 4 — effort M — risk low — category: moons-at-scale — wild
  Why: a moon is promoted only when K separate generator lineages (different model, temperature, seed lens) independently emit members of the same family, an "autoinducer" threshold. Lone-wolf ideas are ignored; convergent ones become climax candidates, free of any cold-reader cost. Assumption: families are stable enough to count across lineages.
  Done when: a synthetic run where 3 lineages hit one family promotes it and 1 lineage does not, logged with the lineage count.

- **Wild: Grow a mycorrhizal lesson network between repos and lanes** — FEATURE — value 4 — effort L — risk med — category: lessons — wild
  Why: lessons stay inside the repo and session that earned them, and T-0217 wants confidence on them. A hyphal layer would let a lesson that preceded first-time passes in one repo flow, redacted and tagged, to sibling repos on the same stack card, strengthening with use and withering unused.
  Done when: a lesson earned in repo A appears in repo B's recall for a matching stack card with its source stripped, and decays after a stated idle period.

- **Wild: Run a Red Queen arms race between generator and critic** — FEATURE — value 4 — effort L — risk med — category: moons-at-scale — wild
  Why: the user said the moons "aren't that wild". Feed the cold reviewer's kill reasons back to the local generator as negative few-shot each round while the critic's rubric tightens. Track the oscillation like predator-prey and keep the generation where wildness plateaus.
  Done when: over 5 rounds the mean wildness score of survivors rises and the log shows each round's kill-reason prompt.

- **Wild: Hold a nurse-log week where Sampo builds scaffolds for future tasks** — FEATURE — value 3 — effort M — risk med — category: niche construction — wild
  Why: niche construction means the organism changes its own habitat. Idle-time lanes would leave fixtures, helper scripts and test harnesses in the repo for later agents, and measure whether tasks touching them pass first-time more often. Assumption: first-time-pass is already tracked (T-0217 mentions it).
  Done when: a scaffolded path shows a measured first-time-pass delta against a matched unscaffolded path over a stated sample.

- **Compute a keystone score per verb from a simulated extinction** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: earlier ideas toggle capabilities one at a time. A food-web view replays recorded sessions with one verb removed, follows the downstream verbs that starve, and ranks verbs by cascade size, so the rare verb that holds everything up is found before anyone retires it.
  Done when: `sampo web keystone` ranks verbs by cascade, and a planted verb with known dependants ranks first.

- **Show the tower as a forest with age rings** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: the site already has a Moons section from the catalogue and an illustrated forge. Render each moon as a tree: ring per stage survived, canopy height for wildness, colour for family, with a succession playback of the funnel. Needs reduced-motion handling.
  Done when: the site page renders from catalogue data with no extra host, and a reduced-motion flag gives a static forest.

Next question: Which stage of the funnel loses the wildest candidates, and does the log let us tell a kill for being wild from a kill for being wrong?
Next question: If one local model went extinct (server swap costs about 3 minutes), would family diversity collapse, and does any measure show it?
