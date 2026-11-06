# Brainstorm — lens: approaches

- **Derive proof obligations from the diff, not from the agent's claims** — FEATURE — value 4 — effort M — risk low — category: obligations
  Why: assumption: the existing ideas all start from a claim ("type every claim", "route every claim"), so an agent that under-claims escapes them. A static hunk classifier (templates and CSS → UI, SQL and migrations → data, `*.md` → docs, `*.tf` and units → infra, hot-path files → perf) lists what must be proven or labelled unproven. Trade-off: coarse, but it needs no model and can't be talked out of a category.
  Done when: a diff touching a migration and a template prints a data obligation and a UI obligation with no claim text supplied, and `fm task finish` refuses to omit either.

- **Unmask luck-passes by re-running proofs under perturbation** — FEATURE — value 4 — effort M — risk low — category: proof strength
  Why: the pack covers flaky verdicts and tick-only perturbation, but not "passes only because TZ, locale, `PYTHONHASHSEED`, test order or the clock happened to align" for ordinary task proofs. Run each proof twice more under shuffled settings; a verdict that flips is labelled luck-pass, not proven. Trade-off: about 3x proof time, so run it only on L tasks or overnight.
  Done when: a planted proof that depends on `TZ=UTC` is labelled luck-pass, and a hermetic proof stays proven.

- **Turn each unproven label into a dispatchable proof ticket** — FEATURE — value 4 — effort M — risk low — category: unproven
  Why: unproven claims currently end as text. A ticket is a self-contained file (claim, exact command, the environment it needs, the output shape that counts as pass). A CI job, a second machine or a person runs it and returns a result file, which Foreman ingests as a proof record. Trade-off: this adds an ingest format, but it reuses the `proof.sh` and "ingest other tools' verdicts" ideas instead of building provers.
  Done when: a ticket run on another checkout returns a result file, and `fm` flips that claim from unproven to proven with the host recorded.

- **Label each proof one-shot or standing, and say where the standing ones run** — FEATURE — value 3 — effort S — risk low — category: durability
  Why: assumption: "proven" today means "passed once". A claim backed by a repo test or CI job will be re-caught, while a one-off `fm shot` check won't. Map each proof to the repo's own test and CI config to find which kind it is. Trade-off: the mapping is heuristic, so it errs toward "one-shot".
  Done when: the finish receipt shows "standing (CI job X)" or "one-shot, nothing will re-catch this" beside each proven claim.

- **Ship the labelling layer alone as the do-less baseline** — FEATURE — value 4 — effort S — risk low — category: minimal
  Why: the request's last sentence is "whatever can't be proven gets labelled". This approach builds no new provers. It classifies each sentence of the final message by whether a logged command supports it, and prints Proven or Unproven with the reason. Trade-off: it is the cheapest approach and catches only unsupported claims, not weak proofs, so it is the control arm for every richer approach.
  Done when: a final message that says "UI verified" with no screenshot or flow in the tool log is flagged unproven.

- **Run `fm flow` over a pairwise covering array of flags, env and locale** — FEATURE — value 3 — effort M — risk med — category: UI matrix
  Why: the pack proposes state, browser and hostile-environment matrices, but a full product of options explodes. A pairwise covering array (PICT-style) hits every two-way combination in about 10 runs. Trade-off: it misses three-way bugs, so a `--full` switch is needed.
  Done when: five boolean flags produce a fixed set of runs of 8 or fewer, and a planted bug that needs flags A and B together is caught.

- **Treat disagreement between two independent provers as the output** — FEATURE — value 3 — effort S — risk low — category: proof strength
  Why: assumption: a DOM assertion that passes while the screenshot diff fails, or a doc example that runs while the prose contradicts it, shows more than either result alone. Report every disagreeing pair at the top of the receipt. Trade-off: it only works where two provers exist for the same claim.
  Done when: a planted change where the text is right but the colour is wrong prints a "provers disagree" line naming both.

- **Allocate proof effort by expected loss** — FEATURE — value 3 — effort M — risk med — category: budget
  Why: assumption: every claim currently gets the same effort. Score blast radius, reversibility and the prover's historical miss rate (from the reopen ledger). Spend deep provers only above a threshold, and print the score. Trade-off: it needs data, so use fixed weights until 30 closed tasks exist.
  Done when: a docs typo fix gets only the lint pass and a migration gets a rehearsal on a scratch clone, each with its score shown.

- **Rank unproven claims by how much other work rests on them** — FEATURE — value 3 — effort S — risk low — category: unproven
  Why: a claim-level dependency graph (the UI flow rests on the API, which rests on the migration) turns the flat unproven list into "this one is load-bearing". It extends "pass unproven status down" from tasks to claims. Trade-off: edges must be declared or inferred from file overlap, which is noisy.
  Done when: the unproven register's first line names the claim with the most dependants, with the count.

- **Build twice and diff the artifact hashes** — FEATURE — value 2 — effort S — risk low — category: infra
  Why: assumption: "release artifacts match the tag" is covered, but not whether two clean builds from one tag match. A mismatch shows hidden nondeterminism that makes every later proof harder to trust. Trade-off: slow for big builds, so make it opt-in.
  Done when: a build embedding a timestamp is reported non-reproducible with the differing file named.

- **Give proof artifacts a retention class and delete them on schedule** — SECURITY — value 2 — effort S — risk low — category: artifact hygiene
  Why: scrubbing exists, but screenshots, traces and captures accumulate outside the repo indefinitely (see the question on files that persist outside the repo). Tag each artifact receipt-only, 30-day or keep, and let the nightly tick purge it. Trade-off: replaying an old proof may lose its evidence, which the receipt must say.
  Done when: a 31-day-old trace is deleted, its receipt remains, and `fm doctor` names the purge.

- **Wild: measure ambiguity by paraphrase twins** — FEATURE — value 4 — effort M — risk low — category: meant
  Why: wild. For "does it do what the user meant", a tool-less child writes example input/output pairs from three paraphrases of the user's sentence. The pairs are then cross-checked, and disagreement becomes a numeric ambiguity score that shows before building. Trade-off: it costs three cheap children and measures ambiguity, not correctness.
  Done when: a deliberately two-reading ask scores above a clear one, and the split inputs are listed.

- **Wild: let a jury of small local vision models vote on "does this screen match the sentence"** — FEATURE — value 2 — effort L — risk high — category: local judge
  Why: wild; assumption: a local-first user may accept a free, private witness. Five local models vote, the disagreement is logged, and the result is capped at "weak witness" and never counts as proven. Trade-off: it is noisy, but it works offline and sends nothing out.
  Done when: with the network blocked, a screenshot and a sentence yield votes tagged weak, and the finish still lists the claim unproven.

- **Wild: stage a three-turn debate when two proofs disagree, with an evidence-only judge** — FEATURE — value 3 — effort M — risk med — category: adversarial
  Why: wild. One child defends the claim and one attacks it, each allowed to cite only stored artifacts. A third child sees only the transcript and the artifacts, rules, and the transcript is stored. Trade-off: three model calls for the rare disputed case, and the rule that artifacts only count if they exist limits invention.
  Done when: a debate that cites a nonexistent artifact is discounted, and the ruling lists the artifact ids it relied on.

Next question: Which proof kind has the lowest observed miss rate on past reopened tasks, and does the ledger record the kind used on each finish well enough to tell?
Next question: Where does a user-run manual check (a click-through, an `ls`) leave a trace Foreman could settle against, other than Foreman's own logs?
