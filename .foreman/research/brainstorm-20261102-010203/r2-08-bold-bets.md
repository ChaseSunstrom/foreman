# Brainstorm — lens: bold bets

- **Patrol for missing self** (NK cells) — FEATURE — value 5 — effort M — risk low — category: provenance
  Why: assumption: unlisted. Every Foreman act stamps a provenance mark (task, lane, hook); a night patrol flags changes without one. The pack's stamping ideas (trailers, origin tags) only add marks; none alarm on a missing one.
  Prior art: none found; harnesses detect known-bad, not unmarked. Better by: catches novel harm with no rule written. Novelty: 5.
  Done when: a planted edit with no provenance stamp is named by the night tick, and a stamped edit is not.

- **Opsonize risky artifacts** (tag so others attend) — FEATURE — value 4 — effort M — risk low — category: attention
  Why: assumption: cold-reader and ship-gate effort is spread evenly. A cheap detector never blocks; it tags a file or commit, and downstream stages (cold reader, CI watch, ship) spend more on tagged ones.
  Prior art: risk-scored review in some CI tools, not tag-and-route across harness stages. Better by: guard noise stays low while scrutiny follows the signal. Novelty: 3.
  Done when: a tagged file gets an extra cold-read line in the packet and an untagged one does not.

- **Let rules die unless renewed** (apoptosis with survival signals) — CLEAN — value 4 — effort M — risk med — category: lean
  Why: the pack has many "sunset clock" and "shelve unused" ideas, but each rule's survival is by schedule. Here a lesson, trigger or steer persists only while correct firings renew it; lapse is a soft archive.
  Prior art: TTL caches; none renew on correctness. Better by: deletion driven by evidence of use. Novelty: 3.
  Done when: a rule with no renewing firing in N days is archived and restorable in one command.

- **Require sustained signal before learning** (kinetic proofreading) — FEATURE — value 4 — effort S — risk low — category: learners
  Why: anergy ideas ask for two signals; this asks the same signature to persist across K separate steps or commits, so one-off blips never update a learner.
  Prior art: debounce in alerting. Better by: applies to learners, not only alarms. Novelty: 3.
  Done when: a signature seen in one step changes no learner, and the same one over K steps does.

- **Audit original antigenic sin** (imprinting) — FIX — value 4 — effort M — risk low — category: lessons
  Why: assumption: lessons recalled per file can anchor on the first incident and misguide variants. Compare outcomes with a lesson recalled against withheld, and flag lessons that did worse.
  Prior art: none found. Better by: finds harmful memory, not only unused memory. Novelty: 4.
  Done when: `fm doctor` lists lessons whose recalled-arm outcomes trail the withheld arm.

- **Declare immune-privileged zones** — FIX — value 3 — effort S — risk med — category: guard
  Why: the dropped false-positive path hits come from guard tests and fixtures holding dangerous strings. A zone list mutes detectors inside it; any action leaving the zone is judged at full strength.
  Prior art: scanner ignore files, with no escape rule. Better by: the exit is the guarded boundary. Novelty: 3.
  Done when: `rm -rf /` in a fixture path passes and the same string in `src` blocks.

- **Pair reviewers by uncorrelated misses** (MHC diversity) — FEATURE — value 4 — effort M — risk low — category: review
  Why: multi-lens review is proposed elsewhere in the frontier notes. This picks the pair whose past misses overlap least on the ledger.
  Prior art: parallel reviewers (claudekit); none select by measured error correlation. Better by: more catches per token. Novelty: 4.
  Done when: reviewer choice logs a correlation figure and beats a random pair on a replay.

- **Strip camouflage for the cold reader** (checkpoint evasion) — SECURITY — value 4 — effort M — risk low — category: review
  Why: assumption: diffs can hide a semantic change in formatting churn, or carry builder reassurance. Normalise cosmetic hunks and drop self-description before the read.
  Prior art: whitespace-ignore diffs. Better by: also removes persuasion. Novelty: 3.
  Done when: a planted logic change inside a reformat is flagged by the blind reader.

- **Combine guard rules from segments** (V(D)J) — FEATURE — value 3 — effort L — risk med — category: guard
  Why: replay corpus has 124 cases. Generate candidates as verb × target × context, keep those that bind blocks without hitting benign history, then ask the user.
  Prior art: none found. Better by: reaches novel verbs mutation cannot. Novelty: 4.
  Done when: a held-out unsafe command is caught by a generated rule with zero benign hits.

- **Suppress superantigen events** — FIX — value 3 — effort S — risk low — category: alarms
  Why: assumption: one degenerate input can fire many detectors. If one event fires more than K, file one incident and mute the rest.
  Prior art: alert grouping. Better by: tied to detector count per event. Novelty: 2.
  Done when: a synthetic event firing ten detectors yields one note.

- **Dose the guard in scratch** (hygiene hypothesis) — SECURITY — value 4 — effort M — risk high — category: calibration — wild
  Why: assumption: guard precision is only known from user reactions. In a snapshotted scratch worktree, sample-allow a block and see whether harm followed.
  Prior art: none found. Better by: measures counterfactual harm. Novelty: 5.
  Done when: a scratch block-allow is logged with harm or no-harm outcome and rolled back.

- **Nominate matured rules upstream** (somatic to germline) — FEATURE — value 3 — effort M — risk med — category: sharing — wild
  Why: assumption: local rules never improve the shipped guard. Opt-in only, a mature rule becomes a patch draft with replay evidence; nothing is sent automatically.
  Prior art: shared rule packs, none with local-first evidence. Better by: keeps data on the owner's disk. Novelty: 4.
  Done when: a nominated rule renders as a local patch file and nothing leaves the machine.

- **Broadcast hazards between live lanes** (paracrine signals) — FEATURE — value 4 — effort M — risk med — category: lanes — wild
  Why: assumption: lanes learn hazards only via the tower. A lane writes a short typed signal; other lanes' next hook injects it.
  Prior art: none found. Better by: seconds, not a rebuild. Novelty: 5.
  Done when: lane B's next tool call shows the hazard lane A wrote.

Next question: which of Foreman's detectors have never been shown a benign look-alike of their target?
Next question: what leaves a trace on disk today that no stage checks for a provenance mark?
