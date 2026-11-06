# Brainstorm — lens: bold bets

- **Run the moon catalogue as a niche-partitioned population** — FEATURE — value 5 — effort L — risk med — category: moons at scale
  Why: the pack asks for 10,000 candidates over a grid with families. Assumption: today ranking is flat, so one popular family can crowd out the rest.
  Done when: a funnel run over 10,000 seeds prints per-cell occupancy, and no family holds more than 15% of the survivors.

- **Run a controlled burn on dominant families** — FEATURE — value 4 — effort M — risk low — category: moon diversity
  Why: assumption: cheap-first funnels keep rewarding the most common idea shape. Burning the top family each round lets rare "understory" moons get through.
  Done when: after a burn, the Simpson diversity index of the shortlist rises, and the burned family's best entry is recorded as culled with a reason.

- **Cascade user verdicts down the trophic funnel** — FEATURE — value 5 — effort M — risk med — category: moons at scale
  Why: the user pushed back that the moons "aren't that wild". The funnel levels are embeddings, local model, Sonnet and the user. A rejection or a "wilder" at the top should reweight the layers below it.
  Done when: one rejected moon lowers the prior of its family and its 20 nearest candidates, and the cascade is logged with before and after scores.

- **Recombine moons across distant families** — FEATURE — value 4 — effort M — risk med — category: ideation — wild
  Why: assumption: ideas inside one family converge. A local model crosses two moons from far-apart grid cells, and the offspring gets a novelty bonus for the distance between its parents.
  Done when: a nightly run emits 200 offspring, each recording its two parent ids, and at least 5 reach the Sonnet read.

- **Treat independent reinvention as a quorum signal** — FEATURE — value 4 — effort M — risk low — category: ranking
  Why: assumption: at 10k candidates, a cluster of near-identical ideas from different model families is stronger evidence than any single score. Quorum sensing in ecology is the same trigger by density.
  Done when: clusters with 3 or more model families advance one funnel stage regardless of their individual scores, and the ledger shows the family count.

- **Trial moons in a synthetic terrarium of planted-fault repos** — FEATURE — value 5 — effort L — risk med — category: validation — wild
  Why: wild means a sealed world of generated tiny repos, with faults planted by a tool-less child that has never seen Sampo. The local model runs a moon's mechanism there overnight, and survival is the fitness. This gives a signal Sampo did not author, which the steers ask for.
  Done when: 50 moons get a survive or die score from 20 terrarium repos each, and the score is shown beside the cold-read verdict.

- **Send hyphal alarms between lanes** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: plants warn neighbours through fungal networks. Evidence: lanes repeatedly rediscover the same hazards (the worktree state resolution bugs, the drive's false waits). One lane's hazard note goes to sibling lanes within one turn.
  Done when: a hazard recorded by lane A (for example, a flaky test path) appears in lane B's next brief, and B skips the hazard without rediscovering it.

- **Send pioneer lanes ahead of the expensive ones** — FEATURE — value 4 — effort M — risk low — category: unattended work
  Why: succession starts with cheap pioneers. A local-model lane first writes the fixtures, maps and failing-test skeletons for a task, and the stronger agent arrives onto prepared ground.
  Done when: tasks with a pioneer pass show fewer orientation reads than matched tasks without one, measured in `fm outcomes`.

- **Compute a keystone index from the verb interaction graph** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: the open question asks which capability the user would miss first. Build the graph of verbs from hook, session and ledger co-use, then rank by downstream cascade size.
  Done when: `sampo doctor` prints the top 5 keystone verbs, and removing one in a scratch lane breaks more dependents than removing a random verb.

- **Give not-yet moons a seed bank with germination cues** — FEATURE — value 4 — effort S — risk low — category: genesis
  Why: the steer says a failed moon goes to not-yet.md with its blocker and is retried when a capability unblocks it. Make this mechanical: each entry stores a predicate, and a local model checks every newly landed capability against all cues.
  Done when: landing a capability that matches a stored cue files a retry task naming the moon and the cue.

- **Run the generator and the critic as predator and prey** — PERFORMANCE — value 3 — effort M — risk med — category: moon quality
  Why: assumption: the cold reviewer is too harsh or too lenient depending on the batch, and the user saw low wildness slip through. A feedback controller on the wildness-pass rate keeps both populations alive.
  Done when: over 5 rounds the share of moons rated wild 4 or above stays within a stated band, with the controller's adjustments logged.

- **Record a niche ledger for what each capability changes in the repo** — FEATURE — value 3 — effort M — risk med — category: lean
  Why: niche construction means a capability reshapes the environment it lives in, for example by adding conventions or removing a failure class. A capability whose niche has gone becomes a retirement candidate with evidence.
  Done when: each capability lists the repo facts it changed, and the ledger flags one whose target failure class has not appeared in 30 days.

- **Add a phenology calendar of the user's work seasons** — FEATURE — value 3 — effort M — risk low — category: anticipation — wild
  Why: wild means learning release weeks, bursts and quiet stretches from ledger timing. Heavy brainstorms and moon runs get scheduled in the lulls, and ship gates are pre-warmed before bursts.
  Done when: a morning card names the predicted season, and a replay on 90 days of history places at least 70% of heavy days in the right season.

- **Show a lichen index as one bioindicator of repo health** — FEATURE — value 3 — effort S — risk low — category: observability — wild
  Why: lichens signal air quality at a glance. Combine flaky-test count, doc drift, unproven-claim count and state growth into one glyph, so the user sees stress before any single gauge trips.
  Done when: the pane shows one glyph whose colour changes when any of its four inputs crosses its threshold, and the glyph links to the input that moved.

Next question: Which moon survived every cheap funnel stage but would make the user say "that's not wild", and what did all of its ancestors share?
Next question: If the 10k candidates were generated twice by different local models, how many survivors overlap, and does that overlap measure real novelty or shared model bias?
