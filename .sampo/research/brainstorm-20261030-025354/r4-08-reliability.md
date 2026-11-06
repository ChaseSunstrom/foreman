# Brainstorm — lens: reliability

- **Gate releases on verdict churn** — FEATURE — value 4 — effort M — risk low — category: determinism
  Why: the exam outcome is one run (s0-001), so one noisy score can drive selection. Assumption: hunter output varies run to run.
  Done when: `fm find --twice` runs the pipeline twice on one commit with caches off and prints the verdict-set diff, and the exam gate fails if churn on `none` repos exceeds a stored ceiling.

- **Score the exam as a k-run interval** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: the pack asks what k repeats cost and when selection may trust a delta. A single run can't separate a better arm from luck.
  Done when: `fm exam` reports mean and interval over k runs and the selector refuses to promote a rewrite whose delta lies inside the interval.

- **Plant a decoy key and audit every arm** — SECURITY — value 4 — effort S — risk low — category: exam integrity
  Why: the exam's hidden keys must be unreachable from the finder arms, and a leak would inflate the score undetected. Assumption: arms run with filesystem access.
  Done when: a decoy key file sits in the keys dir and the exam fails any arm whose file-access trace touched it, with a test proving the failure fires.

- **Snapshot-revert non-git projects** — FEATURE — value 4 — effort M — risk med — category: portability
  Why: "any project" is the mission, but lanes and reverts assume git. Assumption: some target repos have none; this child's own working directory is not a repo.
  Done when: `fm find` on a plain directory takes a tar snapshot and a rejected fix restores the tree byte-identical (hash-checked).

- **Stamp every artifact with tree identity** — FIX — value 3 — effort S — risk low — category: wrong-target safety
  Why: assumption: a resumed or misdirected run can apply a finding to the wrong directory or a moved tree.
  Done when: a finding carries path and HEAD or tree hash, and a lane refuses to start when they don't match, with a test using a swapped directory.

- **Key every cache by probe, model and tree** — FIX — value 4 — effort M — risk low — category: stale verdicts
  Why: the ideas list includes "skip repos already cleared", an inspected-ground ledger and dismissal fingerprints. Each can serve a stale "clean" after the prompt or model changes.
  Done when: changing the probe version or model snapshot id invalidates all three caches, and exam mode asserts zero cache hits.

- **Replay hunter transcripts as cassettes** — CLEAN — value 4 — effort M — risk low — category: testability
  Why: the pipeline's staging, ranking and resume logic can't be tested deterministically while the model is live; the cost line stays at $0 in CI.
  Done when: CI replays recorded hunter transcripts through find→prove→rank offline and compares the output to a golden file.

- **Migrate the findings ledger by schema version** — FIX — value 3 — effort S — risk low — category: durability
  Why: assumption: probe and fingerprint formats will change, and old ledgers would then mis-dedupe or crash.
  Done when: a test loads ledgers from the last three schema versions and the migrated output validates under `fm find check`.

- **Run proofs under the repo's pinned runtime** — FIX — value 4 — effort M — risk med — category: wrong-reason reds
  Why: a red caused by the wrong interpreter or node version is a wrong-reason failure that looks like a bug, across the exam's six languages.
  Done when: the proof reads `.tool-versions`, `.nvmrc`, `rust-toolchain` or equivalent, and a fixture with a mismatched default runtime yields "cannot run here" rather than a finding.

- **Add decoy-comment fixtures** — FEATURE — value 3 — effort S — risk low — category: false positives
  Why: the `none` kind needs hunters that ignore misleading cues such as `# BUG:`, `TODO fix` and a suspicious-looking but correct branch. Assumption: today's fixtures contain none.
  Done when: the exam adds clean repos seeded with decoy comments and any filing on them counts as a hard failure.

- **Wild: Twin each repo with renamed identifiers** — FEATURE — value 4 — effort M — risk med — category: contamination
  Why: assumption: public repos may be memorised, so a score on them may not transfer to the never-seen repos Mission 3 is graded on. A mechanical rename preserves behaviour.
  Done when: the exam runs each repo plus its renamed twin and flags any arm whose twin score drops beyond the interval.

- **Wild: Have the hunter predict the red before running** — FEATURE — value 3 — effort S — risk low — category: hallucination check
  Why: assumption: a hunter that cannot say which assertion will fail, and with what message, is guessing.
  Done when: the finding records a predicted failing line and message, and a mismatch with the actual output demotes the finding and logs it per probe.

- **Wild: Run a soak tank of toy hostile repos** — FEATURE — value 3 — effort L — risk low — category: MTBF
  Why: assumption: an idle laptop can run the pipeline continuously over rotating tiny repos, giving a daily "hours between wrong filings" figure instead of occasional exam snapshots.
  Done when: `fm doctor` shows the soak's last-7-day mean time between wrong filings and fails below a floor.

Next question: Which pipeline failures can only be seen across many nights (drift in the model, the toolchains, the exam) and what long-run monitor would catch them before the user does?
Next question: When the hunter's verdict, the proof and the cold refuter disagree, which one does the system trust by default, and where is that decided?
