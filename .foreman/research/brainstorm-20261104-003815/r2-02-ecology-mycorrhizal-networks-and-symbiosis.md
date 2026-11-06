# Brainstorm — lens: ecology: mycorrhizal networks and symbiosis

- **Plant sentinel seeds in every bulk batch** — FEATURE — value 5 — effort M — risk low — category: moons funnel
  Why: the 10,000-candidate funnel leans on local models for bulk, and the user wants the bulk tier to be trustworthy. Earlier ideas rate models by cheater cut-off, but only after the fact. Here, 2–3% of each batch are planted candidates with known verdicts (a known duplicate, a known internal-only leak, a known dud), shuffled in unmarked.
  Done when: a batch run prints a per-model sentinel hit rate, and a batch whose rate falls below the set floor is rerun on the other model instead of passing.

- **Fuse converging lineages instead of deduping them** — FEATURE — value 4 — effort M — risk med — category: moons funnel
  Why: the exact and embedding dedupe drops one of two near-identical moons. Two independent lineages reaching the same idea is evidence, and a drop discards it. This idea adds hyphal fusion: the survivor keeps both parents' provenance and a `converged_from` count that feeds promotion.
  Done when: two seeded near-duplicates from different lineages come out as one candidate with both parents listed and a convergence count of 2.

- **Label lessons with tracers and follow them into diffs** — FEATURE — value 4 — effort M — risk low — category: lessons
  Why: T-0217 wants lesson confidence, and the open questions ask which injected lines a session never acts on. Each lesson carries a short unique phrase, and a scan of the resulting diffs, tests and commit messages finds which sessions carried it forward. This is pulse-chase labelling, and it measures what actually moved into work.
  Done when: `sampo lessons trace` lists each lesson with its downstream hit count over the last N closed tasks, and a lesson with zero hits is marked dormant.

- **Choose ecto or arbuscular integration depth per harness** — FEATURE — value 4 — effort L — risk med — category: harness integration
  Why: T-0335–T-0337 are blocked on Codex, Gemini and opencode hook gaps, and Sampo must not be Claude-specific. Ectomycorrhiza wraps the outside (an audit-only sidecar, no host edits). Arbuscular penetrates the host (hooks, a Stop gate). Each harness gets the deepest tier it can host, and `sampo doctor` shows which tier is live.
  Done when: on a harness with no Stop hook, `sampo doctor` reports the sidecar tier, and a transcript audit still flags a false done.

- **Graft imported skills with a callus window** — SECURITY — value 4 — effort M — risk low — category: supply chain
  Why: T-0791 lists injection and supply-chain defenses, and the pack mentions source plugins like the `rea` reverse-engineering plugin. Anything imported (a skill, a card, a hook) first runs in shadow: its output is logged but never injected, and the Ward reads its file opens. It is wired in only after N clean sessions plus a cold read.
  Done when: an imported skill is inert for its callus window, a planted exfiltration line in it is flagged, and it is promoted only by an explicit command.

- **Route spare local capacity to lanes near promotion** — PERFORMANCE — value 4 — effort M — risk med — category: scheduling
  Why: the pack records a ~3 minute model-switch cost and a rule to batch by resident model. Mother trees feed shaded seedlings from surplus, so idle local-model minutes could go to the candidate families closest to a stage threshold, such as one more embedding pass or one more cold read, instead of idling.
  Done when: a night run's receipt shows idle resident-model minutes, how many went to near-threshold families, and how many of those promoted.

- **Cluster the 10,000 into guilds by resource use** — PERFORMANCE — value 3 — effort M — risk low — category: moons funnel
  Why: semantic families already exist. Guilds would group candidates by what they consume (the same hook, file set, model or surface), so the shared scaffolding is built once and each guild builds as a batch.
  Done when: the funnel report lists guilds with a shared-dependency list, and one guild's builds reuse one scaffold in a test.

- **Weight lesson edges by co-recall before a pass** — FEATURE — value 3 — effort M — risk low — category: lessons
  Why: T-0217 gives each lesson a confidence. Edges between lessons that were recalled together before a first-time pass strengthen, and untraversed edges decay. Recall then returns a lesson's strongly linked neighbours too (Hebbian strengthening in the mycelium).
  Done when: after replaying 50 closed tasks, recall for a seed lesson returns its co-passing neighbours ahead of unrelated lessons.

- **Show the substrate in the web UI** — FEATURE — value 3 — effort M — risk low — category: ui
  Why: the user wants UI that explains state. One web view draws lessons, lanes and candidates as a thin-line network, with thickness for traffic and a fading colour for dormant edges, and each node opens its provenance. The existing "soil view" idea only shows files.
  Done when: the page renders the network from the ledgers, reduced motion is honoured, and a screenshot test shows a dormant edge drawn visibly thinner than an active one.

- **Instantiate a capability only where a root signal appears** — CLEAN — value 4 — effort L — risk med — category: lean
  Why: the pack's lean pressure (injected characters, 2.4 GB state, hooks) and the "auto-dormant" idea point the same way. In rhizobial nodulation the plant builds the nodule only when the soil signals a need. Here each verb's hook and injection stay off until a repeated failure signal for it appears, and are retired when the signal stops.
  Done when: a fresh repo's session start injects only the Ward plus a pointer, and a planted repeated failure turns on exactly one verb's injection.

- **Wild: Put a tiny endophyte model inside each session** — FEATURE — value 3 — effort L — risk med — category: local models — wild
  Why: the user wants decision models like Jev and Jeff used. A resident small model lives inside the lane's host session as a symbiont and watches tool-call shapes for drift from the goal capsule. It speaks only through a one-line flag, and it is local, so nothing is sent out.
  Done when: in a replay of a drifting session the endophyte flags the drift within K turns, with zero flags on a clean control replay.

- **Wild: Fix a mycorrhizal invoice for every model pair** — FEATURE — value 3 — effort M — risk low — category: moons funnel — wild
  Why: partner choice in real symbioses is reciprocal. Each (orchestrator, local model) pair gets a ledger of what each side gave the other. The local model gives drafts, the frontier gives corrections, and the corrections feed the next scaffold. A pair whose give-and-take stays lopsided is renegotiated, for example by switching the local model's role.
  Done when: `sampo louhi pairs` prints give and take per pair, and one lopsided pair is flagged with a suggested role change.

- **Wild: Pass lessons by spore between installs, offline** — SECURITY — value 3 — effort L — risk high — category: privacy — wild
  Why: privacy and local-first lens. A "spore" is a signed, size-capped, scrubbed file of failure shapes, never raw text, carried by the user (USB, a mail attachment). It enters through the graft quarantine above. Federation exists without any network path.
  Done when: exporting a spore on one install and importing it on another yields a quarantined lesson with provenance, and a planted secret in the source state is absent from the spore.

- **Wild: Let a dead lane's leftovers feed its successor** — FEATURE — value 3 — effort M — risk low — category: lanes — wild
  Why: the pack records killed sessions and resume costs. On death, a lane writes a compost file (failed approaches, files touched, the one surprise). The next lane on that task or a sibling receives it as a one-paragraph start card, and the file is deleted once it is consumed.
  Done when: killing a lane mid-task produces a compost file, the successor's first turn cites it, and no compost file remains afterward.

Next question: which of these cross-lane exchanges would leak across a trust boundary (a lane working in a private repo feeding lessons to a public one), and what is the smallest check that stops it?
Next question: if the funnel's bulk models were all wrong in the same direction, what independent signal not authored by those models would show it?
