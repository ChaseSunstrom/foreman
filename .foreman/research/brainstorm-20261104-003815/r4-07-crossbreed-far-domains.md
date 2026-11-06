# Brainstorm — lens: crossbreed far domains

- **Rank candidates by compression distance to the kill corpus** — PERFORMANCE — value 4 — effort S — risk low — category: funnel
  Why: the pack has an exact-then-embedding dedupe and a shingle fallback, but nothing is free of model calls at 10,000. Cross information theory with taxonomy: train a zstd dictionary on killed and accepted moons, and send candidates that compress to under a threshold against it to the "likely duplicate or templated" lane. Assumption: the shingle fallback is slower than zstd at that scale.
  Done when: on a planted set of 200 near-duplicates in 10,000, the stage catches at least 90% with zero model calls, and the false-kill rate is logged from a 100-item audit sample.

- **Subtract a blank-control score from every judge call** — FEATURE — value 5 — effort M — risk med — category: funnel accuracy
  Why: a Dicke radiometer switches between the sky and a reference load to cancel instrument drift. Each cold or local judge scores the candidate and also a content-stripped twin with the same shape (headings, "Today you can't / With this, you can" line, length). The verdict is the difference. Evidence: the standing rules fear templated cells and the user says moons "aren't that wild", which suggests judges reward style. Assumption: a stripped twin can be made cheaply.
  Done when: planted fluent-but-empty moons score above planted terse-but-wild ones on the raw judge and below them on the differential, on a held-out set.

- **Cap lane count below the merge percolation threshold** — PERFORMANCE — value 4 — effort M — risk low — category: lanes
  Why: parallel Missions and lanes exist, and merge conflicts appear at some density. In percolation theory, a giant connected component appears suddenly once edge density passes a threshold. Build the file-overlap graph of the briefs and cut the dispatch width where the largest component would cover more than half the briefs. Assumption: brief file lists exist at filing.
  Done when: on 20 replayed Mission batches, the cap predicts which batches had merge conflicts, and the dispatcher batches the rest in waves.

- **Trace lane contacts and quarantine only the exposed** — SECURITY — value 4 — effort M — risk low — category: injection defense
  Why: the pack covers injection defenses and fencing, but a poisoned read today is a whole-run problem. Borrow epidemiology's contact tracing: log which lane read which external text hash (web, issue, imported skill, local-model output) and which lanes then touched the artifacts it wrote. On a flagged hash, hold the descendant artifacts and the lanes that read them, and leave the rest running.
  Done when: planting a flagged hash in one of 6 lanes holds exactly its read-descendants and no others, and the other lanes finish.

- **Require a costly signal before a moon reaches the morning card** — FEATURE — value 4 — effort M — risk med — category: moon quality
  Why: in the handicap principle (peacock tail), only a trait that is expensive to fake counts as honest. A moon surfaces to the user only with a signal a templated idea can't fake: a sandboxed 60-second demo, a failing-then-passing Exam on a planted repo, or a runnable counterexample to the nearest existing feature. It is a quality gate, not a price. Evidence: the user's "I want wild" complaint and the ban on templated cells.
  Done when: of 50 moons surfaced, every one links a demo that runs in the sandbox, and a planted ideas-only moon never reaches the card.

- **Kill whole families from one cheap kill** — PERFORMANCE — value 4 — effort S — risk med — category: funnel
  Why: the sieve of Eratosthenes crosses out all multiples of a prime in one pass. Families exist in the funnel, so one stage-1 kill with a reason class (for example "internal-only", "needs a host feature") propagates to family members that share the reason feature, and skips their scoring. Each propagated kill is audited by a sampled rescue check, so nothing is removed unrecorded. Assumption: reasons are stored as classes.
  Done when: the funnel log shows propagated kills with their source id, and the sampled audit shows under 5% would have survived.

- **Mark every Sampo-run executable with a methylation tag** — SECURITY — value 3 — effort M — risk low — category: Ward
  Why: bacteria use restriction-modification: self DNA carries a methyl mark and foreign DNA without it gets cut. The Ward would flag a hook, lane script or generated command that lives in the state or hook path and lacks a hash tag recorded by Sampo's own writer, whether it was dropped by a plugin, an imported skill or a local model. This catches what a command-shape rule can't, a planted script run by a harmless-looking command. Assumption: the writers can be funnelled through one helper.
  Done when: a planted untagged script in the hook path triggers a Ward notice on its first run, and Sampo's own generated scripts never do.

- **Keep a refugium of the last-good hook set** — PERFORMANCE — value 3 — effort M — risk low — category: hook latency
  Why: ecological refugia let a population survive a disturbance. Hooks are a bench-gated hot path, and a bad self-edit or a slow parallel run damages every session. Keep the previous hook bundle installed beside the live one, and flip to it when the p95 over the last N events exceeds the budget or an exception rate trips. Assumption: the plugin can hold two hook entry paths without double-firing.
  Done when: injecting a 300 ms delay into the live bundle flips to the refugium within 10 events, and exactly one hook fires per event.

- **Agree a pidgin between the orchestrator and local models** — FEATURE — value 3 — effort M — risk med — category: local models
  Why: contact languages grow when two groups need cheap, reliable exchange. Distil the 200 most-used message shapes (verbs, status words, clause slots) into a fixed vocabulary, pinned by cards and a constrained grammar, for orchestrator↔local traffic. Evidence: the pack has small-model cards and grammar-constrained briefs as ideas but no shared protocol. Assumption: message shapes are logged.
  Done when: local-model malformed-output rate on a held-out set drops against free text, and tokens per exchange fall by a logged amount.

- **Wild: turn the funnel's kill log into a tree-ring and read droughts** — FEATURE — value 3 — effort S — risk low — category: diagnostics
  Why: wild. Dendrochronology reads climate from ring widths. Plot kills per stage per generation as rings; a wide dull ring means a stage ran on a degenerate model or prompt. Combine with the hash-chained log idea so a ring can't be rewritten.
  Done when: the site shows the funnel as rings, and a planted bad-prompt run shows up as an anomalous ring that `sampo` flags.

- **Wild: grow moons on a mycelial "wood wide" bus between lanes' failed spikes** — FEATURE — value 3 — effort L — risk med — category: moon synthesis
  Why: wild. When a spike fails, a decomposer lane extracts the surviving fragment (the working parser, the passing test, the unblocked approach) and posts it to a shared fragment pool tagged by cell. Other lanes pull fragments by cell-match before starting. This is the "no idea killed" rule made mechanical. Assumption: fragments can be cut at function level.
  Done when: a second spike on a different moon reuses a posted fragment and records its source.

- **Wild: run a nightly "immune challenge" using a feeder model that attacks the funnel itself** — SECURITY — value 4 — effort M — risk med — category: red team
  Why: wild. Vaccination exposes the system to harmless pathogens. The uncensored local model writes candidates built to game each judge (flattery, injected "score 5" lines, templated cells), the funnel scores them, and any winner becomes a permanent negative exemplar. Evidence: the uncensored variant is available locally, and the judge-injection decoys idea exists but isn't fed back as training.
  Done when: a planted gaming candidate is caught by the next night's run, and the exemplar count and catch rate trend upward in the log.

- **Mark moon families by climate-zone and refuse out-of-zone claims** — CLEAN — value 2 — effort S — risk low — category: catalogue
  Why: species ranges depend on temperature and rainfall, and moons depend on model capability, hardware and host. Tag each family with its zone (local-only, needs frontier, needs host feature X) so claims like "works on any model" are checked against the tag.
  Done when: `fm genesis check` fails a moon whose text claims a zone its tag excludes.

Next question: Which of these cheap funnel stages (compression, blank control, family propagation) actually kills what a human later rejects, measured against the user's own accept and reject history rather than Foreman's cold reads?
Next question: What would a security reviewer reach for first on the state and hook path that no ecological or immune metaphor has yet suggested?
