# Brainstorm — lens: approaches

**Answering a left-over question first:** the user model is a learner that has already eaten poisoned input. Mistaken captures from T-2547's test and test writes into the real state dir both reached it. Idea 3 targets that.

- **Gate guard signatures on an execution-context motif** — FIX — value 4 — effort M — risk low — category: guard
  Why: the dropped "breakage ahead" and brief-guard path false positives show regexes firing on text that merely mentions a command. This borrows the CRISPR PAM, where a spacer cuts only next to a motif. A rule fires only in command position, never in prose, paths or briefs.
  Done when: a corpus of mirrored pairs (the same string in command position vs in a brief or comment) blocks only the former, and the 124 replay cases are unchanged.
  Prior art: shell tokenizers (already proposed); none found for motif-gating.
  Better by: no full parser, and each rule carries its own context requirement.
  Novelty: 3

- **Guard the guardee, not the attacker** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: plant NLR immunity watches the host proteins pathogens must alter, not the pathogen. A manifest of about 15 invariants (hook config, guard rules, test assertions, CI yaml, lockfile) is hash-checked after every tool call, whatever command changed it. Assumption: the existing hook-bypass tripwire covers only hooks.
  Done when: editing any manifest item through a route the guard doesn't recognise still raises a revert-and-freeze within one call.
  Prior art: AIDE/Tripwire for hosts; none found in agent harnesses.
  Better by: it catches novel evasion routes, because it keys on the effect rather than the command.
  Novelty: 3

- **Sense data in the wrong compartment** — FIX — value 4 — effort M — risk low — category: integrity
  Why: cGAS-STING fires on DNA in the wrong place, whatever its sequence. A compartment map says which record types may live where (state dir, ledgers, repo, child packs). A nightly scan flags test-origin or other-repo records in real ledgers. This is the evidence above: two mistaken captures in the user's asks, and tests that wrote real state.
  Done when: a planted test-origin capture in the real ledger is flagged the next tick and quarantined.
  Prior art: data-loss-prevention tools; none found for agent ledgers.
  Better by: it checks location, not content, so it needs no list of bad strings.
  Novelty: 3

- **Convert harm into verification spend** — FEATURE — value 3 — effort M — risk med — category: risk budget
  Why: emergency myelopoiesis shifts marrow output to defenders. Today harm only steps autonomy down. Instead it reallocates the next N tasks' budget toward cold reads and exam arms, then decays.
  Done when: after a recorded harm, the next three tasks show a higher verifier share, and it returns to baseline on schedule.
  Prior art: none found.
  Better by: it buys evidence, where today's mechanism only withholds trust.
  Novelty: 4

- **Starve the taint** — SECURITY — value 4 — effort M — risk med — category: capability
  Why: nutritional immunity sequesters iron the moment bacteria appear. On the first read of untrusted text (issue, CI log, web page), the session loses credentials and network for the rest of that lane. The pack shows 81% security worry and a sandbox escape-hatch complaint.
  Done when: a lane that fetched hostile text cannot read env secrets or open sockets, and a test proves it.
  Prior art: dual-LLM and CaMeL-style taint research; static sandboxes.
  Better by: the restriction is dynamic and triggered by observed taint, not set at launch.
  Novelty: 3

- **Live with it: a disease-tolerance ledger** — FEATURE — value 3 — effort S — risk low — category: reliability
  Why: hosts survive some infections by limiting damage, not clearing the cause. For failures that can't be fixed (a flaky upstream, a host bug), the ledger holds a damage cap, a fence and a review date. Flaky reruns only retry.
  Done when: each ledger row has a cap that a test exercises, and a lapsed review date surfaces in `fm doctor`.
  Prior art: circuit breakers.
  Better by: it is explicit, dated and tied to a bet.
  Novelty: 3

- **Clot with a dissolving timer** — FEATURE — value 3 — effort S — risk low — category: ship
  Why: haemostasis plugs a breach in seconds and dissolves on repair. When CI goes red on main, one lock blocks ship and self-started merges, and clears on verified green or a TTL. Assumption: ship isn't already blocked on red.
  Done when: a red main blocks `fm ship` within one tick, and a green run releases it unaided.
  Prior art: merge queues.
  Better by: the plug is automatic and expires itself.
  Novelty: 2

- **Splenic squeeze** — CLEAN — value 3 — effort S — risk low — category: state (wild)
  Why: assumption: aged red cells are cleared by squeezing through narrow slits, and the rigid ones fail. Nightly, a scratch clone gets a rename or move, and lessons, triggers and cell citations that break are flagged as brittle. The pack shows 1214 unused cards and stale-map complaints.
  Done when: a lesson anchored to a moved file is flagged without anyone naming it.
  Prior art: link checkers.
  Better by: it deforms the tree instead of only checking existence.
  Novelty: 4

- **Audit enhancing antibodies** — FEATURE — value 3 — effort M — risk low — category: lessons (wild)
  Why: in dengue, old antibodies worsen a different strain. Compare outcomes for tasks where a lesson was recalled against matched tasks where it wasn't, and flag lessons that raise harm on lookalikes (a retry lesson on a non-idempotent op). Ablation duels and the bet ledger supply the data.
  Done when: a seeded harmful lesson is flagged against its matched controls.
  Prior art: none found.
  Better by: it finds lessons that do harm, not just stale ones.
  Novelty: 4

- **Donor reviewer, intolerant of local habit** — FEATURE — value 3 — effort M — risk med — category: review (wild)
  Why: in graft-versus-leukaemia, donor cells attack what the host tolerates. Once a generation, a reviewer given only the diff and the public README flags what the repo and the tower have grown used to, such as unused verbs or odd conventions.
  Done when: it flags at least one planted tolerated oddity in a fixture repo.
  Prior art: fresh-eyes reviews.
  Better by: it is deliberately blind to local convention.
  Novelty: 3

Next question: which of Foreman's stores has no record of where each entry came from?
Next question: when a learned artifact misleads, what outcome signal shows it was the artifact rather than the model?
