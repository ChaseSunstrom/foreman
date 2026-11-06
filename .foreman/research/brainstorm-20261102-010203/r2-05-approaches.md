# Brainstorm — lens: approaches

- **Detect missing-self, not bad-self (NK cells)** — FEATURE — value 4 — effort M — risk low — category: detection
  Why: every guard idea so far looks for bad shapes; in the pack, only the tower's origin stamps and builder-claimed marks come near the opposite test, which is to flag what lacks the expected marker. Marker examples are a task id trailer, a trigger tag or a probe on a row. Lane-made commits, files and plan rows carry none of these when they go off-process.
  Prior art: none found in coding harnesses; SLSA-style attestation is the closest. Better by: it catches novel failures with no signature, and it fits one checker over existing stamps. Novelty: 4.
  Done when: a planted commit with no task trailer, made inside a lane, shows up in `fm doctor` as "unstamped".

- **Challenge-test a risky call in a scratch copy (skin-prick test)** — FEATURE — value 5 — effort M — risk med — category: approvals
  Why: users report 15+ prompts per session; the allow list matches prefixes while the sandbox flags structure. Instead of asking, the guard runs a tiny dose of the command in a throwaway copy and measures damage (files deleted, paths touched, network). A harmless result earns an allow.
  Prior art: dry-run flags exist per tool; no harness does automatic empirical trial. Better by: the evidence is what the command did, not its text. Novelty: 5.
  Done when: a `rm` on a scratch-only path is allowed without a prompt after a trial run, and a trial that touches the real tree is blocked with the measured diff.

- **Create immune-privileged zones** — FEATURE — value 4 — effort M — risk med — category: prompt fatigue
  Why: inflammation is suppressed in the eye and brain because the immune response would do more harm than the invader. Night worktrees and scratch trees could get a relaxed alarm tier but a hard containment boundary, which cuts prompts where harm is bounded.
  Prior art: bypass modes exist, but none ties relaxation to a proven boundary. Better by: relaxation applies only where a boundary test passes. Novelty: 4.
  Done when: a lane in `night/<date>` runs 20 sandbox-safe calls with zero prompts, and a write outside the worktree is still denied.

- **Register commensals and alarm on overgrowth** — FEATURE — value 4 — effort S — risk low — category: tolerance
  Why: flaky reruns and the dropped false-alarm ledger show known-benign oddities are tolerated ad hoc. One registry would hold each tolerated oddity with its cause, an expiry and a count. The signal is overgrowth: a tolerated flake rate that climbs is dysbiosis, not noise.
  Prior art: flake quarantine lists; none treat tolerance as a living population. Better by: it separates "ignore" from "ignore until it grows". Novelty: 4.
  Done when: a tolerated test whose failure rate doubles in 7 days raises one named alarm.

- **Type grafts before accepting imported skills, cards and MCP tools (transplant matching)** — SECURITY — value 4 — effort M — risk low — category: supply chain
  Why: the pack shows MCP description pinning and install cooldown ideas, and a stack library of 1214 cards. Foreman imports foreign text and tools with no match test against its own conventions.
  Prior art: lockfiles and signature checks. Better by: it scores fit against the project's self (naming, verbs, hook budget), rejects mismatches, and runs a shadow window first. Novelty: 4.
  Done when: an imported card that adds an injection block over budget is rejected with the reason.

- **Test lessons against variants (original antigenic sin)** — FIX — value 3 — effort M — risk low — category: memory
  Why: lessons recalled per file are keyed to the first-seen failure. A lesson shaped by one incident can bias later answers wrongly on a variant. Replay each lesson against mutated variants of its incident, and flag lessons that fire wrongly.
  Prior art: none found. Better by: it measures overfit in memory, which nothing does now. Novelty: 4.
  Done when: a lesson planted with a too-narrow key is flagged "imprinted" in the nightly report.

- **Sample the tissue with a roving patrol** — FEATURE — value 3 — effort S — risk low — category: unattended
  Why: all detectors are triggered by events. A nightly lane would pick three random old files or diffs, and a cold reader checks them for rot nobody triggered.
  Prior art: scheduled linters. Better by: random sampling finds unknown unknowns; the miss rate is a gauge. Novelty: 3.
  Done when: a planted stale premise in a random file is found within two weeks.

- **Measure fibrosis: chronic over-containment** — CLEAN — value 3 — effort S — risk low — category: guard health
  Why: repeated containment of one path hardens into scar that blocks healthy work. Count paths where guard blocks or quarantine exceed a threshold with no harm event, and propose relaxing.
  Prior art: none found. Better by: the guard gets a cost gauge to match its benefit gauge. Novelty: 3.
  Done when: a path with 10 blocks and 0 harm outcomes is listed with a relax proposal.

- **Run a booster on waning rules** — FEATURE — value 3 — effort S — risk low — category: replay
  Why: the corpus has 124 labelled cases; a rule's last test date is not shown. Re-exercise rules whose last verified-fire is oldest.
  Prior art: spaced repetition for people. Better by: it targets waning, not just failure. Novelty: 3.
  Done when: `fm replay` lists rules by days since last real fire.

- **Wild: Evolve a camouflaged tumour** — FEATURE — value 4 — effort L — risk med — category: red team
  Why: assumption: wild. A red-team lane hides a bug from the cold reader each night; survivors become training cases for the reader. Tumours escape by self-labelling as safe, so builder-claimed "tests pass" is the target.
  Prior art: adversarial evals in labs, none unattended in a harness. Better by: the reviewer is co-evolved against live evasion. Novelty: 5.
  Done when: the reader's catch rate on a fixed set of planted camouflaged bugs rises over 7 nights.

- **Wild: Keep sentinel animals** — FEATURE — value 3 — effort M — risk low — category: release
  Why: assumption: wild. A cheap-model session runs each Foreman release against a scripted trap task before the user's session, so harm lands on the sentinel first.
  Prior art: canary releases. Better by: the canary is a weak model that falls into traps first. Novelty: 3.
  Done when: a planted regression in a release is caught by the sentinel before a user session starts.

- **Wild: Tissue-type the user's own repos** — FEATURE — value 3 — effort L — risk high — category: transfer
  Why: assumption: wild. Share only the shape of learned rules, with no content, across the user's own machines or repos; a new repo gets them only if its self-profile matches. Nothing leaves their hardware.
  Prior art: none found. Better by: transfer is gated by match, not copied blind. Novelty: 4.
  Done when: a rule moves between two matching repos and is refused by a mismatching one.

Next question: which of these detectors can be scored against a planted ground truth before it is allowed to speak?
Next question: what does the user override most by hand, and is that an allergy or a real gap?
