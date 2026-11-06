# Brainstorm — lens: self-modification

- **Seed the leak list from the host's own identifiers** — FEATURE — value 5 — effort S — risk low — category: self-edit / vocabulary
  Why: the user pushed back on "jarvis" and on naming Claude as the orchestrator. The public-surface lint needs a forbidden-term list, and the host already knows the sensitive terms: hostname, `$USER`, profile names and endpoint hosts in config, and model IDs in settings. The lint would regenerate its list from those at each run instead of relying on hand-typed words.
  Done when: adding a new profile named `zzdemo` to a scratch config makes the lint fail on a page containing "zzdemo", with no edit to the lint's source.

- **Block self-edits that shrink verifier coverage** — SECURITY — value 4 — effort M — risk med — category: self-edit / safety
  Why: assumption: a verifier can pass more by checking less. Every verifier already emits the claim classes it checked; diff that set before and after any self-edit to verifier code, and fail the edit if the set shrank without a recorded `narrowed:` reason.
  Done when: a test edit that drops one claim class from the docs verifier fails the gate with the class named, and passes again with `narrowed: <reason>`.

- **Name the exam lines a self-edit should flip, before running it** — FEATURE — value 3 — effort M — risk low — category: self-edit / verification
  Why: assumption: edits that flip exam lines nobody predicted show the author didn't understand the blast radius. The editing lane writes `expect-flip:` lines at pickup; unexplained flips in either direction block landing.
  Done when: a self-edit that changes an unlisted exam line is refused with that line quoted.

- **Keep a frozen checker outside the self-edit reach** — SECURITY — value 4 — effort S — risk low — category: trust anchor
  Why: the 599 unproven "meaning" claims are judged by machinery Sampo can rewrite. A stdlib-only script (≤200 lines, hash recorded in `doctor`) re-checks a fixed corpus of planted right and wrong claims. Self-edits cannot touch it. A mismatch reports "the verifier drifted".
  Done when: `doctor` reds if the frozen script's hash changes, or if the live verifier's verdicts differ from the script's on the corpus.

- **Refuse unattended self-edits to files no test covers** — SECURITY — value 3 — effort S — risk low — category: self-edit / guard
  Why: the repo already has a tests→src map. A drive-initiated edit to a `plugin/lib` file with no covering test goes to a proposal branch instead of main, labelled "untested self-edit".
  Done when: a drive edit to an uncovered scratch module lands on the proposal branch, and the same edit to a covered module lands normally.

- **Mine repeated hand-fix shapes into lint rules** — FEATURE — value 4 — effort M — risk med — category: self-edit / lint
  Why: the history shows the same corrections recurring, such as wording renames (T-2768) and the drive-counting fixes (T-2873/2874/2901). Cluster FIX commits by diff shape (token substitution, added guard clause) and, at three or more, draft a lint or codemod with its own planted-defect test, shown as a proposal.
  Done when: replaying the last 200 commits yields at least one proposed rule whose test fails on the pre-fix code of its source commits.

- **Bisect a gauge regression to the self-edit that caused it** — FEATURE — value 3 — effort M — risk low — category: self-edit / recovery
  Why: assumption: when the unproven count rises, nobody knows which self-edit did it. Run the exam as the bisect predicate across Sampo's own commits and file a revert-or-fix task naming the commit.
  Done when: on a scratch repo with a planted regression, `sampo` names the planted commit in under N steps.

- **Run every auto-editor twice and demand a zero diff** — CLEAN — value 3 — effort S — risk low — category: self-edit / idempotence
  Why: the renamers, the number-templating and the doc-fill steps all rewrite Sampo's own files. A second run on their own output must change nothing, and a non-idempotent editor is the likely source of churn across the rename work (T-2748).
  Done when: the gate runs each editor on a copy twice and fails on a nonempty second diff.

- **Register generated artifacts with a regen check** — CLEAN — value 3 — effort S — risk low — category: self-edit / drift
  Why: shims, site data, the picker artifact and the genesis data are all written by Sampo. Each carries a header naming its generator command, and the gate regenerates it and diffs, so a hand edit is flagged instead of overwritten silently.
  Done when: editing a generated file by hand fails the gate with the generator command printed.

- **Nudge drive constants from the ledger, with a ratchet** — PERFORMANCE — value 3 — effort M — risk med — category: self-tuning
  Why: LONG_JOB_S and the tail window mis-counted agents three times. Let a bounded step (±20%, one constant per week) propose new values from the drive's own ledger, shadow-run them, and revert automatically if misses rise.
  Done when: a replay of the ledger with a planted too-small window shows the proposal enlarging it and the miss count dropping.

- **Capture the user's hand edits of Sampo-written prose as lint seeds** — FEATURE — value 4 — effort M — risk low — category: self-edit / learning
  Why: assumption: the user rewrites a phrase by hand rather than say why. A hand edit to a line Sampo wrote, such as "jarvis" becoming "the local model", is stored as a before/after pair. A pair repeated twice is proposed as a rule.
  Done when: two scratch hand edits with the same substitution produce one proposed lint rule that fires on a third instance.

- **Wild: replay Sampo's own reverted self-edits against the gate nightly** — FEATURE — value 4 — effort M — risk low — category: self-edit / gate test
  Why: reverted self-edits are known-bad changes already in the history. Re-apply each to a scratch clone nightly. Any the ship gate would now let through is a hole, filed with the commit.
  Done when: the nightly run reports a catch rate over all reverted self-edits, and a deliberately weakened gate lowers it.

- **Wild: cap the share of effort Sampo spends on itself** — FEATURE — value 3 — effort S — risk low — category: self-edit / budget
  Why: round 1 was told to finish everything before anything new, and Sampo's own tower work can crowd out the user's repos. A visible "Sampo on Sampo" percentage of dollars and tasks, with a user-set ceiling, pauses self-edits above it.
  Done when: the finish card shows the percentage, and setting the ceiling to 0 stops drive-picked self-edit tasks.

- **Wild: backfill the unproven curve by running today's checker over past commits** — FEATURE — value 3 — effort L — risk med — category: self-edit / measurement
  Why: a verifier change looks like a real improvement on the gauge. Run the current checker on every 10th commit in a scratch worktree, so the chart is plotted in one consistent instrument.
  Done when: the Genesis site shows a proven-over-time line built from a single checker version, and a verifier change leaves the line's past values unchanged.

Next question: Which of Sampo's self-edits could the user not currently tell apart from their own, and does a provenance trailer on every commit change what they review?
Next question: When a self-edit improves one gauge by lowering another's coverage, which gauge does the user actually look at first?
