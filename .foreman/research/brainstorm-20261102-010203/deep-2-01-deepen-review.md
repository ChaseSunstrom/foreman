# Brainstorm — lens: deepen: review

- **Compile a presentation dossier the cold reader must cite** — FEATURE — value 4 — effort M — risk med — category: review
  Why: assumption: the card, hapten split, and suspect tags in the list are one pipeline. Per lane, a card holds the digest, three check lines, a mechanical-bulk summary, and the tagged hunks. The reader's verdict is void unless each finding cites a card line or a raw hunk. Prior art: none found for citation-bound review. Better by: a reader that cannot cite cannot hallucinate. Novelty 4.
  Done when: a verdict with an uncited finding is rejected, and a test shows a card-only verdict passes.

- **Delete reviewer lenses that flag self before release** — FEATURE — value 5 — effort M — risk low — category: review
  Why: thymic negative selection. Run each new lens or prompt variant over the 124 labelled replay cases and the user's accepted history. Any lens that blocks known-good work above a threshold is never released. This answers the poisoned-learner question. Prior art: eval gating of prompts, but not applied per reviewer against accepted self. Better by: it is automatic and uses Foreman's own corpus. Novelty 3.
  Done when: a seeded over-strict lens is refused with the self cases it flagged named.

- **Demand a second signal before a finding blocks** — FEATURE — value 5 — effort M — risk med — category: review
  Why: anergy. A lone reviewer finding is logged as anergic and does not block. It blocks only with a costimulus: a failing test, a guard hit, an uncorrelated second reviewer, or a CI red. The pack shows 66% frustrated by near-misses and 3 dropped false alarms. Prior art: none found; consensus voting exists. Better by: the costimulus must come from a different signal class, not a repeat vote. Novelty 4.
  Done when: a single-source finding is recorded as anergic, and the same finding with a failing test blocks.

- **Mature reviewers by CI-confirmed hits** — FEATURE — value 4 — effort L — risk med — category: review
  Why: affinity maturation. Reviewer prompt variants that predicted later CI reds or reverts multiply, and the others fade. Ablation duels are the selection arena, and the calibration ledger is the affinity score. Prior art: prompt-optimisation tools, with no live ground truth. Better by: selection comes from real shipped outcomes. Novelty 4.
  Done when: after a recorded run, the lens weights shift toward the variant with higher confirmed-hit rate, shown in `fm doctor`.

- **Fingerprint recurring findings for a cheap memory response** — PERFORMANCE — value 4 — effort M — risk low — category: review
  Why: memory cells. Hash the shape of each confirmed finding (file kind, pattern, fix). A matching diff gets a zero-token pre-check before any reviewer runs, which also trims token cost. Prior art: lint rules, and lessons recalled per file. Better by: the rule is auto-minted from confirmed findings and fires on shape, not on file path. Novelty 3.
  Done when: a repeated defect shape is flagged with no model call and the prior task is cited.

- **Regulate review storms with a suppressor** — FEATURE — value 3 — effort S — risk low — category: review
  Why: T-regs against cytokine storms. When findings per diff, fix-churn, or reviewer count exceed the norm, a suppressor merges duplicates and caps blockers. It also records "reviewers harmed throughput" as a harm signal. Prior art: none found. Better by: it treats overreaction as damage. Novelty 3.
  Done when: a diff with 30 duplicate findings yields at most the capped, deduped set, with the suppression logged.

- **Track autoimmune rate per Foreman detector** — FIX — value 5 — effort S — risk low — category: review
  Why: the user dropped three "Breakage ahead" alarms as false. Compute false-alarm rate for every detector (breakage-ahead, cold reader, guard, lean ratchet) from drops. A detector above its tolerance is demoted, as noisy triggers already are. Prior art: trigger precision exists for triggers only. Better by: it extends demotion to gates. Novelty 2.
  Done when: `fm doctor` lists per-detector false-alarm rate and a seeded noisy detector is demoted.

- **Mint a candidate detector from every CI-red FIX** — FEATURE — value 5 — effort L — risk med — category: review
  Why: antibody from autopsy. A captured FIX task drafts a guard or check rule. It must catch its own failing diff, and negative selection must show it flags none of the labelled good cases. Then it is offered for approval. Prior art: none found for auto-minted rules with a self-test gate. Better by: the harness learns from its own failures. Novelty 5.
  Done when: a fixture CI-red task yields a rule that replays red on its diff and green on the corpus.

- **Wild: Raise a system fever on harm clusters** — FEATURE — value 3 — effort M — risk med — category: review
  Why: wild. Rising harm sets a temperature that mandates a cold read on every lane, slows merges, and adds one lens, instead of per-task surges. It breaks after N clean ships, which are also logged. Prior art: none found. Better by: one global dial that visibly cools. Novelty 4.
  Done when: the third harm in a window sets the state, and the state clears after N clean ships.

- **Wild: Drain every lane's card into a lymph node** — FEATURE — value 4 — effort M — risk low — category: review
  Why: wild. One read-only node compares the dossiers across parallel lanes and flags the same antigen in two lanes, or contradictory fixes, before either merges. Prior art: merge-conflict detection, which is textual only. Better by: it catches semantic collisions. Novelty 4.
  Done when: two fixture lanes making incompatible assumptions are flagged before merge.

- **Wild: Vaccinate with planted harmless defects** — FEATURE — value 4 — effort M — risk low — category: review
  Why: wild. Occasionally seed a labelled defect into a shadow copy of a diff and log whether the cold reader catches it. Reviewer sensitivity is then measured, not assumed. Prior art: mutation testing aims at tests, not at reviewers. Better by: it reports a per-reviewer detection rate. Novelty 4.
  Done when: the ledger shows detection rate per reviewer from at least 10 seeded cases, with no seed reaching the real tree.

- **Wild: Herd immunity across projects, locally** — FEATURE — value 3 — effort M — risk med — category: review
  Why: wild; assumption: the user runs several repos and harnesses. Finding fingerprints (no code) are shared between projects on the same machine, so a lesson in one repo pre-checks the others. Nothing leaves the host. Prior art: shared team memory is called out as missing in the pack. Better by: it is local and fingerprint-only. Novelty 4.
  Done when: a fingerprint minted in repo A flags a matching diff in repo B, and nothing is written outside the home directory.

Next question: Which Foreman gate has the highest false-alarm rate in the user's own drops, and would the user rather lose that gate or retrain it?
Next question: When two review signals disagree, which one has historically been right, according to the calibration ledger?
