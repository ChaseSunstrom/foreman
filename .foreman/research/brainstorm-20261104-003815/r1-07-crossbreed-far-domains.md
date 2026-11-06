# Brainstorm — lens: crossbreed far domains

- **Cap the cheap stage with a predator-prey controller** — PERFORMANCE — value 4 — effort M — risk low — category: moons funnel
  Why: Moons at scale runs 10,000 candidates through a cheap-first funnel, and the local models can emit far faster than the expensive cold reviewers can read. Assumption: the funnel has no feedback from the expensive stage's backlog.
  Done when: in a 10k simulated run, the expensive-stage queue never exceeds a set length, and the cheap-stage emission rate rises and falls with it, as logged in the funnel log.

- **Promote by quorum, not by one judge** — FEATURE — value 5 — effort M — risk med — category: moons funnel
  Why: the user said the moons "aren't even that moon-y", and one judge's taste is the likely cause. Each independent cheap signal adds to a threshold: embedding distance from prior art, a small-model jury from two families, and a shingle-novelty check. A candidate moves up only when at least 3 signals agree and 2 model families are among them.
  Done when: `sampo genesis moonshot` prints, per promoted candidate, which signals voted. Over a held-out batch, the share of promoted candidates the cold reviewer scores wildness ≥4 beats a single-judge baseline.

- **Replace the ideas-so-far wall with a census of occupied and empty niches** — FIX — value 5 — effort M — risk low — category: brainstorm packs
  Why: this pack carries thousands of one-line ideas with heavy repeats, which costs tokens and nudges lenses to echo. Cluster them by embedding and give each lens a species count per cluster, 2 exemplars per cluster, and the vacant regions.
  Done when: a generated pack is under a set character budget, and the duplicate rate of a brainstorm run on it falls against the same run on the full list.

- **Stop a lens when its rarefaction curve flattens** — PERFORMANCE — value 4 — effort S — risk low — category: moons funnel
  Why: new-cluster-per-sample is the ecological measure of diminishing returns. It would also cover the deferred idea of dropping lenses that go dry (T-0829).
  Done when: a lens run ends early with a "curve flat at N" line, and the clusters it found match a full run within a set tolerance.

- **Score keystone moons per family** — FEATURE — value 4 — effort M — risk low — category: moons funnel
  Why: families exist but have no way to choose where the costly wildness review goes. Rank each family member by how many descendants and neighbours depend on it, and spend the cold review on the keystone first.
  Done when: for each of 5 sampled families, the keystone is listed with its dependants, and the reviewer's score on it predicts the family's mean score better than a random member does.

- **Burn the dominant cluster when diversity collapses** — FEATURE — value 4 — effort M — risk med — category: moons funnel (wild)
  Why: 10k bulk candidates from one local model will drift into one monoculture. Track a Simpson diversity index on the pool. Below a floor, set aside the biggest cluster (kept, not deleted) and let seed-bank items from `not-yet.md` germinate in the opened space.
  Done when: after a simulated monoculture, the index recovers above the floor within one cycle, and the set-aside cluster is restorable by an undo verb.

- **Detect Batesian mimic moons** — SECURITY — value 4 — effort M — risk med — category: wildness gate
  Why: the rater scores wildness 1-5, and bulk local models learn to write sci-fi vocabulary around mundane substance. Flag candidates whose wild-word density is high but whose embedding sits close to existing features or tweaks.
  Done when: on a planted set of 20 mimics among real moons, at least 90% are flagged, and the flag is shown beside the wildness score.

- **Breed hybrids from far-apart parent pairs** — FEATURE — value 5 — effort M — risk low — category: moon generation (wild)
  Why: the user wants wild and bulk is cheap. Pick pairs of candidates from different grid cells or ecology and non-ecology domains that are far apart in embedding space, and have a local model write the hybrid. Keep it only if it is far from both parents.
  Done when: 1,000 hybrids are generated in one local run, and the share that pass the funnel and reach wildness ≥4 is reported against single-parent mutation.

- **Speciate moons on isolated islands** — FEATURE — value 3 — effort L — risk med — category: moon generation (wild)
  Why: run one moon through several local profiles, each with its own constraints, for a few rounds. Then reunite the lines and look for hybrid vigour. Assumption: the 27B and 35B models differ enough to diverge.
  Done when: one moon yields at least 3 lineages with measured pairwise distance, and the best reunited hybrid outscores its ancestor in a blind review.

- **Let wild moons build their own grid cells** — FEATURE — value 4 — effort M — risk med — category: coverage grid
  Why: the rule says a moonshot fits no coverage cell. Niche construction means such a moon may open a new row or column through `sampo genesis grow`. The new axis is kept only after 2 later candidates occupy it.
  Done when: a moon with no cell proposes an axis with evidence, and the axis is kept or retired automatically on the 2-occupant rule.

- **Grow foraging probes along the best moon's neighbourhood** — FEATURE — value 3 — effort M — risk low — category: moon generation (wild)
  Why: idle GPU time can extend outward from a top-scoring moon in small steps, like fungal hyphae, and retract from dead ends. Branches that fail the cheap funnel for 3 steps in a row die.
  Done when: a one-night run logs a tree of probes with pruned tips, and at least one branch reaches the expensive stage.

- **Feed a lessons flow by need, not by copy** — FEATURE — value 3 — effort M — risk low — category: small-model cards
  Why: a small model gets a card only when its own failure signature matches the card's trigger, like the mother-tree nursing of seedlings. This keeps cards short (the small-model-cards work is open) and gives each card a measured sink.
  Done when: a local Smith run injects only matching cards, and its card characters per task fall against the all-cards arm with no loss in pass rate.

- **Build a coral reef of accepted moons** — FEATURE — value 3 — effort M — risk low — category: delight (wild)
  Why: each accepted moon deposits a layer on a growing structure on the site, with its spec, a first test and a render. Growth rings show generations, and a reader can see the wildest layers at the top.
  Done when: the Genesis page shows one reef with a layer per accepted moon, every layer opens to its spec, and the reef rebuilds from the catalogue alone.

- **Add a decomposer lane for dead candidates** — CLEAN — value 3 — effort S — risk low — category: moons funnel
  Why: 10k candidates will leave a heap of rejected ones. A lane digests each rejected family into a short reason and a tag, which feed the burn rule above and the mimic detector, before the bodies are archived by tier.
  Done when: every rejected family has a one-line reason and tag, and the candidate store's active size falls below a set limit.

Next question: Which funnel stage is the scarce one in practice: local-model throughput, cold-reviewer cost, or the user's attention on the final slate?
Next question: When the local model switch costs ~3 minutes, does the candidate generator batch by resident model, and is its output diverse enough across the 27B and 35B to be worth two lineages?
