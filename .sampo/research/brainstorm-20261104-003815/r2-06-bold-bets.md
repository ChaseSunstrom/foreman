# Brainstorm — lens: bold bets

- **Estimate the unfound ideas by mark-recapture** — FEATURE — value 4 — effort S — risk low — category: moons at scale
  Why: wild. Many brainstormers and lenses run over the same pack, and the pack only reports rarefaction and a "diversity index". Lincoln-Petersen on the overlap between two independent lenses (or two local models) gives N̂, the total number of distinct ideas in a cell. That turns "stop when the curve flattens" into "stop at 90% of N̂" and tells you how many are still unfound.
  Done when: `sampo genesis moonshot census` prints N̂ with a confidence interval per cell, and on a planted pool of 200 known ideas it lands within ±15%.

- **Transect-sample the killed candidates to measure funnel recall** — FEATURE — value 5 — effort M — risk low — category: funnel
  Why: the cheap-first funnel (exact dedupe, embedding, shingle) kills most of the 10,000, but the pack only ledgers each stage's unique kills, never what it wrongly killed. Pull a random 1% stratified by stage and family and give it a cold Sonnet read. That gives each cheap stage a false-kill rate with an interval, and a stage above 5% is retuned.
  Done when: a funnel report lists, per stage, kills sampled, rescues found and a false-kill % with an interval, and a stage over threshold fails `fm genesis check`.

- **Model family capacity with island biogeography** — FEATURE — value 3 — effort M — risk low — category: moons at scale
  Why: wild. Each coverage cell is an island whose "mainland" is gen-0 capabilities. Distance (embedding) sets the immigration rate of new candidates, and cell size sets the extinction rate. The MacArthur-Wilson equilibrium predicts how many families a cell can hold, and a cell far under it has a real gap while one over it has saturated. Assumption: cell sizes and distances are computable from the existing grid.
  Done when: the grid view shows predicted versus observed family counts per cell, and the 20 largest residuals feed the next Seed.

- **Detect an approaching stall by critical slowing down** — FEATURE — value 4 — effort M — risk med — category: drive reliability
  Why: the pack shows repeated drive failures (phantom waits, a running set that is miscounted, restarts that re-push). In tipping systems, rising lag-1 autocorrelation and variance precede the collapse. Compute both over rolling windows of tick latency, retry rate and wait-set churn. Warn before the drive holds or the funnel jams, not after.
  Done when: replaying the T-2873, T-2900 and T-2901 incident logs raises the warning at least one tick before the stall in at least 2 of 3 cases, and a quiet week raises none.

- **Trace contagion of templated phrasing through candidates** — FIX — value 4 — effort S — risk low — category: moons at scale
  Why: the steer says a templated cell isn't counted, and 10,000 local-model outputs will copy each other's stock phrases. Treat a phrase as a pathogen with R0 = how many later candidates adopt it. A phrase over R0 1 is quarantined: it is stripped from the generator's few-shot context and every carrier is flagged.
  Done when: on a seeded batch with one planted catchphrase, the tool names the phrase, lists its carriers and drops the repeat rate below 2% in the next batch.

- **Probe for existing capability from its traces, like eDNA** — FEATURE — value 5 — effort M — risk low — category: dedupe
  Why: "Today you can't / With this, you can" dedupes by text, but a capability that already exists leaves traces in code: verbs, hook names, test names, doc anchors, ledger keys. Fingerprint those traces with zero tokens and score every candidate against them. This catches "already built" and "premise already met" without a model, and many of the pack's dropped items were exactly that.
  Done when: of 100 past dropped-as-built items, at least 80 are flagged by the probe alone, and fewer than 5 of 100 genuinely new candidates are falsely flagged.

- **Wild: allocate tasks by response thresholds, ant-style** — FEATURE — value 3 — effort L — risk med — category: lanes
  Why: wild. Each queue item emits a stimulus that grows with its age and its blocked dependents. Each lane or model has a personal threshold, and an idle agent takes work whose stimulus exceeds it. There is no central scheduler. Specialisation emerges because a successful lane's threshold drops for that task kind. Assumption: lanes can read the queue state cheaply.
  Done when: in a simulated 3-lane, 40-task run, makespan is within 10% of the current scheduler with no central assignment, and each lane's task-kind mix visibly specialises.

- **Wild: leave decaying pheromone on verbs and files that led to a first-time pass** — FEATURE — value 3 — effort M — risk med — category: recall
  Why: the pack has trails of Reads and lesson confidence, but nothing that evaporates. Reinforce a path (file, verb, card) on a first-time pass, let it decay with a half-life, and let `fm next` and map slicing prefer strong trails. Stale advice then dies on its own.
  Done when: on replayed closed tasks, trail-weighted file suggestions beat unweighted ones on top-3 hit rate, and an unused trail drops below the noise floor after its half-life.

- **Plan each night around its limiting resource (Liebig's minimum)** — FEATURE — value 4 — effort M — risk low — category: unattended
  Why: the pack has many resource items (GPU residency, the 3-minute model switch, frontier quota, disk, the user's morning attention) but no rule that says which one binds tonight. Estimate each resource's supply against the queue's demand, name the scarcest, and shape the plan around it. Spare resources fund exploration.
  Done when: the sealed night plan names its limiting resource, and over 7 nights the stated limiter matches the resource that actually ran out first at least 5 times.

- **Wild: hold the gate steady with a Daisyworld ceremony homeostat** — FEATURE — value 4 — effort L — risk high — category: self-regulation
  Why: wild. Ceremony tuning is set by hand today (T-1266 is deferred). Two opposed populations of nudges, "tighten" and "relax", grow or shrink with recent outcomes. False-done rate raises the tighten population, and cost and re-ask rate raise the relax one. Strictness settles at an equilibrium with no explicit tuner, and tightening only is allowed unattended, in line with the ratchet steer.
  Done when: in a replay with injected false dones, strictness rises within 5 tasks and then returns to the baseline band, and an unattended loosen is refused.

- **Run a common-garden experiment to separate capability from model** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: the free-versus-session and bare-model comparisons confound a capability's lift with the model and repo it ran on. Reciprocally transplant: run each capability on the same scenarios across models and repos, and fit genotype × environment. A lift that vanishes on stronger models is flagged as retiring. Assumption: the local profiles give enough model spread.
  Done when: the scorecard shows a capability × model grid with variance split between the two factors, and at least one capability is flagged "environment-dependent".

- **Wild: tag each capability with its Holling adaptive-cycle phase** — FEATURE — value 3 — effort S — risk low — category: lifecycle
  Why: wild. Phases are growth, conservation (rigid, heavy, brittle), release and reorganisation. Classify from commit churn, injected characters, use counts and outcome lift. A capability in conservation with falling lift is a candidate for controlled release, and one in reorganisation gets room. The pack has sunsets and tripwires but no phase view.
  Done when: `fm doctor` lists each capability's phase with its evidence, and a capability stuck in conservation for two generations opens a review task.

- **Wild: breed moons by reciprocal crossing with a sterility check** — FEATURE — value 3 — effort M — risk med — category: moons at scale
  Why: wild. Crossing distant parents is already listed, but nothing checks that the offspring is viable. Test each hybrid for sterility: if it cannot state a distinct "Today you can't / With this, you can" line unlike both parents, it is dropped. A viable hybrid whose line passes goes on to the usual cold read. Local models make this free at 10,000 scale.
  Done when: a batch of 500 crosses yields a measured viable fraction, and every survivor's line has similarity below the dedupe threshold to both parents.

Next question: which funnel stage's false-kill rate, once sampled, would change which of the 10,000 the user finally sees?
Next question: what single signal from the user's real sessions would let the ecology metrics (census, capacity, phase) be checked against what they actually valued?
