# Brainstorm — lens: capability map

- **Negative-select against synthetic self for paths the user never touches** — SECURITY — value 4 — effort M — risk low — category: guard learning
  Why: assumption: thymus replay uses only the user's command history, and AIRE-style promiscuous expression (the thymus shows detectors samples of tissues it never contains) tests tolerance for the rest. Prior art: none found. Better by: a child generates plausible benign commands for rarely used areas (deploy scripts, migrations), so a new rule is tested against self it has never seen. Novelty 4.
  Done when: a new rule that blocks a seeded benign command in an untouched area fails release, and the same rule passes once the synthetic sample is removed.

- **Desensitise a rule the user keeps overriding** — FEATURE — value 4 — effort M — risk med — category: false positives
  Why: the pack shows "track autoimmunity" and "notice allergies" but only deletion as the outcome. Prior art: allow-list growth in Claude Code and Codex, which is binary. Better by: allergy-style graded exposure steps a rule block → warn → log in doses, replaying the 124-case corpus at each step and halting if a labelled harm case flips. Novelty 4.
  Done when: a rule overridden 5 times drops one rung, a corpus harm case stays blocked at every rung, and the step is logged.

- **Close each harm as a healed wound with phases** — FEATURE — value 4 — effort M — risk low — category: incident lifecycle
  Why: the pack covers risk-budget step-down and lessons, but a harm has no object that is "open" until healed. Prior art: incident postmortem tools (none in coding harnesses). Better by: phases are contain, repair, remodel (regression test, rule or lesson, retire the stopgap), and the wound stays open until all artifacts exist. Novelty 3.
  Done when: `fm doctor` lists an open wound with its missing artifact, and the wound closes only after the test and the lesson are committed.

- **Sample allowed calls like M cells and audit them later** — SECURITY — value 3 — effort S — risk low — category: guard misses
  Why: assumption: the guard is only scored on blocks and replay, so its false negatives are unseen; the pack's "detect evasion after block" and interrupt-as-miss ideas cover only noisy cases. Prior art: none found. Better by: 1–2% of allowed calls get a post-hoc cheap-model review, giving a measured miss rate. Novelty 3.
  Done when: a seeded harmful-but-allowed call is caught by the sample within a day's run, and the miss rate appears in `fm doctor`.

- **Trained immunity: decaying per-repo threshold shift after an incident** — FEATURE — value 3 — effort S — risk low — category: innate layer
  Why: after harm the pack offers new rules or a global fever, but nothing the innate layer "remembers" without a new rule. Prior art: none found. Better by: a repo-local, time-decayed bias on existing rules (a destructive-verb warn becomes a block for N days) with no new artifact to curate. Novelty 4.
  Done when: after a seeded harm the same call is stricter, and it returns to baseline after the decay window in a faked-clock test.

- **Split lessons into plasma (always on) and memory (dormant, recalled on a signature)** — PERFORMANCE — value 3 — effort M — risk low — category: lean
  Why: the 387k context per reply and the unused-cards problem point to injection without a promotion test. Prior art: CLAUDE.md-style static memory. Better by: only lessons that earned repeated saves are injected, and the rest wake on a failure signature. Novelty 3.
  Done when: injected lesson chars fall with the same exam pass count, and a dormant lesson is recalled on its signature.

- **Raise an interferon state in neighbouring lanes** — FEATURE — value 3 — effort M — risk med — category: parallel lanes
  Why: assumption: parallel lanes share modules, and a failure signature in one gives the others no warning. Prior art: none found. Better by: lanes whose blast radius overlaps the failing module get a temporary stricter verify step, then clear. Novelty 3.
  Done when: a seeded failure in lane A adds the verify step in an overlapping lane B and not in a disjoint lane C.

- **Differentiate a stem reviewer into a lens reviewer only on a damage signal** — FEATURE — value 4 — effort M — risk med — category: review
  Why: the frontier shows multi-lens parallel review loved but in conflict with the one-pass token rule. Prior art: claudekit and ECC fan out always. Better by: one generalist pass, and a specialist lens (security, perf, concurrency) is spawned only where the diff or CI shows damage signals. Novelty 3.
  Done when: a clean diff costs one pass, and a diff touching auth spawns exactly the security lens.

- **Keep a germline guard that learners cannot edit** — SECURITY — value 4 — effort S — risk low — category: tamper resistance
  Why: assumption: many learners now propose rules (affinity maturation, vaccination), and the pack has no wall between shipped and learned rules. Prior art: managed-policy layers in Claude Code. Better by: learned (somatic) rules can add stricter checks but never loosen or delete a shipped rule, enforced by a test. Novelty 3.
  Done when: a learner patch that removes a shipped rule is rejected, and one that adds a stricter rule is accepted.

- **Wild: Mine a repo-specific neoantigen rule from its own recurring failures** — FEATURE — value 3 — effort L — risk med — category: personalised checks
  Why: wild; captured FIX tasks from CI red already record the repo's recurring failures. Prior art: none found. Better by: diffs shared by the failures but absent from green history yield a repo-only pre-commit check, vetted on the thymus replay. Novelty 4.
  Done when: three seeded failures with a common diff pattern produce a check that flags a fourth and stays silent on 20 green commits.

- **Wild: Reconstitute all learners from a clean seed and diff the result** — SECURITY — value 3 — effort M — risk med — category: poison recovery
  Why: wild; an earlier question asks which learner was never tested with poisoned input. Prior art: none found. Better by: one verb wipes every learned state, replays the append-only sources, and shows what changed. Novelty 4.
  Done when: after seeding a poisoned lesson, `fm reconstitute` removes it and prints the diff of recalled lessons.

- **Wild: Spin up a tertiary lymphoid hub on a chronic hotspot** — FEATURE — value 3 — effort L — risk med — category: local expertise
  Why: wild; lessons are recalled per file but chronic hotspots get no standing local reviewer. Prior art: none found. Better by: a file with repeated reopens gets a local checklist and reviewer prompt that dissolves after N clean closes. Novelty 4.
  Done when: a file with three seeded reopens gains a hub, and the hub disappears after five clean closes.

Next question: Which of these immune ideas has a labelled harm case in the 124-case corpus that would catch its failure, and which need new cases first?
Next question: When two immune layers disagree (fever vs desensitisation), which one wins, and is that tested?
