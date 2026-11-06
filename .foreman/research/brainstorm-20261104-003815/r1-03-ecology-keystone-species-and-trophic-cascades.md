# Brainstorm — lens: ecology: keystone species and trophic cascades

- **Rank the work queue by keystone score** — FEATURE — value 4 — effort S — risk low — category: queue
  Why: the 3 blocked harness items (T-0335, T-0336, T-0337) and several blocked UI items look like one dependency cluster, but `fm next` orders by age or size, not by what each item unblocks.
  Done when: `fm next --why` prints each open item's count of transitive dependents, and a test with a planted hub item shows it ranked first.

- **Map the cascade when one capability is switched off** — FEATURE — value 5 — effort L — risk med — category: measurement
  Why: the pack's "live without me" drill removes one capability and reads its own metric only. Keystone loss shows up downstream in the capabilities that fed on its output. Assumption: the ledgers can attribute downstream outcomes.
  Done when: `sampo keystone run` disables each capability in turn in a lane, then writes a directed graph of which other capabilities' outcome rates moved, ranked by how many it moved.

- **Report a trophic pyramid for the 10,000-candidate funnel** — FEATURE — value 4 — effort S — risk low — category: moons
  Why: the cheap-first funnel has bulk local generators at the base, then dedupe and embedding filters, then cold reviewers. Nothing says whether the levels stay in proportion.
  Done when: the funnel report prints candidates, cost and wall time per level and flags an inverted pyramid, such as top-level reviews exceeding the base.

- **Gate stage promotion on a diversity index** — FEATURE — value 4 — effort S — risk low — category: moons
  Why: the user pushed back that the moons "aren't that wild". A funnel that selects on a single score tends to leave a monoculture of similar survivors.
  Done when: promotion refuses a stage if the Shannon index over families and grid cells falls below a threshold or one family exceeds a set share, with the reason printed.

- **Credit ecosystem-engineer moons through a lineage ledger** — FEATURE — value 4 — effort M — risk low — category: moons
  Why: niche construction. A moon that adds a capability changes what later moons are possible. Moons are currently judged on novelty and value alone.
  Done when: each shipped moon carries a count of later candidates or tasks whose Done-when cites its verb, and `fm genesis moonshot` sorts by it.

- **Seed moons with a pioneer-to-climax ladder** — FEATURE — value 4 — effort M — risk med — category: moons
  Why: succession. Cheap pioneer candidates "condition the soil" by turning their survivors into context for the next, more ambitious stage, rather than every stage seeing the same pack. Assumption: staged context changes output diversity.
  Done when: an A/B over one grid compares laddered and flat runs, and the report shows the laddered climax stage's wildness scores and their spread.

- **Pool lane findings in a shared mycorrhizal ledger** — FEATURE — value 4 — effort M — risk med — category: lanes
  Why: failed spikes go to not-yet.md with a blocker, and sibling lanes tackling a related task cannot see them. Parallel Missions 5-8 already run in lanes.
  Done when: a lane that starts a task touching a not-yet blocker's files gets that blocker injected as a one-line pointer, verified by a test with two planted lanes.

- **Promote candidate families by quorum** — FEATURE — value 3 — effort S — risk low — category: moons
  Why: quorum sensing. A near-duplicate family should advance only when enough independent model families converge on it. A single model repeating itself does not count.
  Done when: a family is promoted only with at least N distinct model-family votes, and a test where one model writes 50 variants shows it stays dormant.

- **Track mutualist and parasitic model pairings** — FEATURE — value 3 — effort M — risk low — category: models
  Why: symbiosis. The model bench measures models separately, but local-plus-orchestrator pairs can help or hurt each other. Assumption: the arms can be paired per task.
  Done when: a table labels each pair mutualist, commensal or parasitic from tokens saved against failure rate on held-out tasks.

- **Wild: Run a prescribed burn on the tower** — FEATURE — value 3 — effort M — risk med — category: hygiene
  Why: the pack has many "prune" ideas but no regrowth test. Periodically archive the lowest-ranked 20% of unread tower files to a trash in a scratch clone, then watch whether any session or exam ever asks for them. Wild.
  Done when: the burn report lists archived files, a restore-request count after 14 days, and flags regrowth demand.

- **Wild: Feed dropped ideas to a decomposer lane** — FEATURE — value 4 — effort M — risk low — category: moons
  Why: not-yet.md holds dead ideas with blockers. A decomposer would break each into reusable parts, such as a measure, a probe or a UI idea, and release them as nutrients to the next seed. Wild.
  Done when: each not-yet entry gets a parts list, and the next seed cites at least one part whose source idea was never retried whole.

- **Wild: Keep indicator-species canaries for environmental stress** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: coral bleaching. A tiny suite of the most fragile checks, such as the double SessionStart, the 3-minute llama-swap switch and resume cost, should flip first when the host, model or Arch updates. The main gates fail only after the damage. Wild.
  Done when: the canary suite runs in under 10 seconds at session start, and a simulated host-version change trips it before any gate in `fm doctor`.

- **Wild: Reintroduce an apex predator into the funnel** — FEATURE — value 4 — effort M — risk med — category: moons
  Why: trophic cascade. A deliberately harsh "wolf" reviewer culls mid-wild candidates, which may free the funnel to keep stranger ones that the dedupe herd would otherwise crowd out. Wild.
  Done when: an A/B with and without the wolf shows the culled count and the wildness score of the top survivors, with the result recorded either way.

Next question: which capability's removal does the user already compensate for by hand, and does any ledger record that compensation?
Next question: at 10,000 candidates, what is the carrying capacity of the local endpoint per night, and what should be culled when it is exceeded?
