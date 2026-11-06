# Brainstorm — lens: ecology: succession and niches

- **Chart each moon's fundamental vs realized niche** — FEATURE — value 4 — effort M — risk low — category: moons grid
  Why: assumption: the grid shows filled/empty cells, but a moon's cell is where it was *tried*. Record the full vector where it could work (surface × stage × actor × model tier × cost) beside where an exam showed it working. The gap is the cheapest list of next experiments.
  Done when: `sampo genesis moonshot niche M-id` prints both sets, and a test with a moon filed on one surface but claiming three lists the two untried cells.

- **Treat the per-turn character budget as a contested resource** — PERFORMANCE — value 4 — effort M — risk med — category: injection budget
  Why: the pack shows many capabilities fighting for session-start and per-turn characters (the double SessionStart, 2,733 chars, 48–76 per turn). Gause's law says two capabilities in the same niche can't both survive. Give each capability a declared character niche, find overlaps, and let the one with the better held-out delta keep the slot.
  Done when: `sampo doctor` lists capability pairs whose injected lines target the same behaviour, and a planted duplicate pair is flagged.

- **Quarantine every new skill, plugin or MCP like ballast water** — SECURITY — value 4 — effort M — risk low — category: supply chain
  Why: the open items T-0791 (injection and supply-chain defenses) and T-0869 (rival-plugin imports) show foreign code is coming. A newcomer gets a small plot (no hook slot, read-only, Ward-wrapped) and earns a wider niche only after N clean sessions.
  Done when: an imported plugin's hooks stay unregistered until its plot-age and block-count thresholds pass, and a planted noisy plugin never leaves the plot.

- **Predict device colonization with an island-biogeography model** — FEATURE — value 3 — effort M — risk low — category: devices
  Why: devices are thin and the pack lists only web UI, CLI and the Smith TUI. Treat phone, watch, tray and car as islands: size is the surface's capability, distance is how much plumbing it shares with the nearest filled surface. Rank which moons should land first and ship a minimal colonist (a single status line or notification) per island.
  Done when: a table gives each (moon, device) a colonization score, and one top-ranked pair is built as a one-card notification.

- **Print a dichotomous key for the docs** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: MASTER.md is too large to Read, and "how do I X" is a recurring gap. Generate a yes/no taxonomic key from each verb's niche vector ("Does it change files? → …") that ends at one verb and one shard.
  Done when: a tool-less child using only the key reaches the right verb on 8 of 10 held-out "how do I" questions.

- **Map each data class's dispersal kernel** — SECURITY — value 4 — effort M — risk low — category: privacy
  Why: the standing rule says nothing leaves without a setting, but no single view shows where each kind of byte (steers, transcripts, briefs, repo text) can travel. Per data class, list the vectors (child process, local endpoint, embedding call, published site data) and the farthest distance reached.
  Done when: `sampo doctor privacy` prints a class × distance table, and routing a steer through a non-local profile turns the row red.

- **Draw the moon catalogue as a niche map** — FEATURE — value 3 — effort M — risk low — category: ui
  Why: the tower and site lead with moons, but a list hides overlap. Plot moons by niche coordinates with overlap shading, so removing one visibly opens a gap and crowded clusters stand out. Animate a moon's stage change as a ring growing.
  Done when: the web UI renders the map from the catalogue, supports reduced motion, and a no-JS fallback is a ranked list.

- **Switch the funnel between r- and K-regimes** — PERFORMANCE — value 4 — effort M — risk med — category: funnel
  Why: the funnel is cheap-first over 10,000 candidates, and a model switch costs ~3 minutes. Run the early stages as r-selection (many cheap candidates on the fast MoE, batched by resident model) and the late stages as K-selection (few candidates, deep reads on the 27B). Measure the regime from the novelty yield and move stage proportions with it.
  Done when: a run logs its regime per stage and uses one model swap per regime, and the dedupe-survivor yield per resident minute beats the single-regime baseline.

- **Wild: Replay primary succession on a stripped install** — FEATURE — value 4 — effort L — risk med — category: capability ranking
  Why: assumption: "which capability would you notice first?" is an open question. Clone the state, remove every capability, replay a week of real tasks, and let each capability re-enable only when its absence causes a measured failure. The order of return is the true pioneer-to-climax ladder.
  Done when: a scratch run outputs an ordered list of capabilities with the failure that triggered each, and the first three match no one's prior guess or are explained.

- **Wild: Hold a mast generation** — FEATURE — value 3 — effort M — risk med — category: moons
  Why: the cold reviewer is a bottleneck with finite budget. Every N generations, fire all lenses at one frontier question at once and flood the funnel with thousands of candidates, so the reviewer's limits can't reject them all (predator satiation). The following generation is a fallow one that only prunes.
  Done when: a mast run files over 5× the normal candidate count, and the cold-read tier reports both its survival rate and its cost per survivor.

- **Wild: Route lane work by stigmergy** — FEATURE — value 3 — effort L — risk high — category: lanes
  Why: the open items T-0792 (lanes and fleet) and the many lease and takeover ideas suggest hard locks are brittle. Replace some of them with decaying scent marks on files and tasks: a successful lane reinforces a path, a failed one weakens it, and marks evaporate on a timer. New lanes follow the strongest unclaimed trail.
  Done when: a simulated fleet of 4 lanes on a conflicting task set has fewer merge conflicts than the lease baseline, and marks decay to zero within the configured half-life.

- **Wild: Advance the proven grid as a fairy-ring front** — FEATURE — value 4 — effort M — risk low — category: moons grid
  Why: with 10,000 candidates, global ranking is expensive. Expand outward from cells with proven moons into their neighbours only. Fruit (publish to the site) only where an exam passes, and leave the interior dormant.
  Done when: each generation's candidates all sit adjacent to a proven cell, and the funnel spends measurably fewer tokens per kept moon than the global run.

- **Gate the push on a hook-slot census by family** — SECURITY — value 3 — effort S — risk low — category: Ward integrity
  Why: assumption: families of moons may each register hooks. Count hook registrations per family at ship and fail when one family holds more than its share of per-event latency, so no family becomes a monoculture on the guard path.
  Done when: the ship gate prints a family × event table, and a test family with a planted extra hook fails it.

Next question: what do the user's real sessions show about which moons they look at twice, and can that become the "fitness" signal in the niche map?
Next question: which of the ecological metaphors in the ideas so far changed a decision, and which only renamed an existing list?
