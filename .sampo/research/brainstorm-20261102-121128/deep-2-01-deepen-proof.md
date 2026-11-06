# Brainstorm — lens: deepen: proof

- **Make the proof state a four-valued lattice** — FEATURE — value 5 — effort M — risk low — category: proof
  Why: the list has "unproven", "could not run" and override-as-override as separate ideas; one ordered type (proven-by-run, proven-by-reread, could-not-run, overridden, unproven) lets every reader (receipt, site claims check, exam, `fm doctor`) share one join rule. Overrides and "could not run" can never join upward to "proven".
  Done when: a test feeds every state pair to the join function and none of the lower-ranked pairs (overridden, could-not-run, unproven) yields "proven"; the receipt prints the state with its reason.

- **Reverse-audit past "proven" labels** — FEATURE — value 5 — effort M — risk low — category: proof
  Why: the pack asks which past proven labels were later reversed and what share had no run record. Answer it with a verb that walks closed tasks, finds those followed by a revert, reopen or fix commit naming the same files, and reports a reversal rate split by proof kind and by whether a run record existed.
  Done when: `fm prove --audit` prints a reversal rate per proof kind and lists tasks proven with no run record.

- **Rank proof kinds by their measured reversal rate** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: this builds on the audit above. Each proof kind earns a weight from how often its "proven" survived. Receipts show the weight and `fm next` asks for the strongest kind the task allows. Assumption: enough closed tasks exist per kind to estimate.
  Done when: a receipt shows "proof weight 0.xx (n=…)" per kind, and a kind with fewer than 10 samples prints "too few to weigh".

- **Add mutation proof: break the fix, watch the test fail** — FEATURE — value 5 — effort M — risk med — category: proof
  Why: `fm task prove` already shows the test failing without the change. Extend it to mutate the landed lines (flip conditions, drop calls) and require that at least one test fails per mutated hunk. This catches tests that pass whatever the code does, and it feeds diff coverage.
  Done when: a task whose test passes under every mutation of its diff gets "weak proof" on the receipt, with the surviving mutations listed.

- **Quarantine proofs by independent author** — FEATURE — value 4 — effort M — risk med — category: proof
  Why: steers say weakness-finding must use signals Foreman didn't author. A proof written by the same session that wrote the fix scores lower than one written blind by a tool-less child from the task text only (the "write the acceptance test blind" idea). The receipt shows who wrote the check.
  Done when: a blind-written check runs against the fix, and its pass or fail appears on the receipt separately from the session's own tests.

- **Log the user's hand-checks as proof evidence** — FEATURE — value 4 — effort M — risk med — category: proof
  Why: the pack asks what the user types to check Foreman's verdicts. Offer an `fm check-by-hand NAME -- cmd` wrapper (and a prompt line in the finish receipt: "run this to see for yourself") that records the user's own run. A user-run check outranks an agent-run one, and the user doesn't have to dig through shell history.
  Done when: running the wrapper adds a "user-run" row to the task's proof, and the receipt ranks it above agent-run rows.

- **Spot-check proofs cold on a schedule** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: `fm night` already ticks. Re-run a random sample of old proofs at their own commit in a clean worktree, and record drift (flaky, environment-dependent, or now failing). This turns "proven" into a claim with a re-check date and hits the "ops gauges Foreman only trusts because it wrote them" question.
  Done when: the nightly tick re-runs 3 old proofs, and `fm doctor` names any that no longer reproduce.

- **Tie every MASTER.md clause to a proof row** — FEATURE — value 4 — effort L — risk low — category: proof
  Why: the sweep already compares public claims with exam lines. Extending this to clause-level mapping (clause → test or exam line) gives a coverage figure for the whole spec, and clauses with no proof show up as red. Assumption: clauses are parseable at semicolons, as `fmrecall.covered` already does.
  Done when: `fm genesis sweep` prints the percentage of MASTER.md clauses with a mapped check and lists the unmapped ones.

- **Make the receipt a signed, hash-chained bundle** — SECURITY — value 3 — effort M — risk low — category: proof
  Why: if the ledger writer is the only witness, an edited record is invisible. Chain each proof record to the previous one by hash, with the command, exit code, output digest and tree hash. A reader detects a missing or edited record, which answers the first open question (a reader that gives a wrong answer when a record class is missing).
  Done when: deleting or editing any proof row makes `fm doctor` report a chain break at that row.

- **Replay a past commit overnight, Foreman vs plain (wild)** — FEATURE — value 5 — effort L — risk med — category: proof
  Why: wild. Combines the long-horizon tier with the user's own repos: pick a real commit from the user's history, roll back, give the following change as the goal, and run both arms on idle usage ($200 budget, 0% used). The morning digest shows the diff of outcomes with each arm's proof states.
  Done when: one morning digest shows a replayed commit with both arms' pass, cost and proof state.

- **Run a proof court: an adversary tries to refute each "proven" (wild)** — FEATURE — value 4 — effort L — risk med — category: proof
  Why: wild. A tool-less child on a different model reads only the task text, the diff and the proof output, and must name one input or case the proof doesn't cover. Foreman then runs that case. A refutation downgrades the label and is stored as an exam scenario, so the exam gets scenarios Foreman didn't author.
  Done when: for a sample task, the refuter's case runs and the result (held or refuted) is on the receipt.

- **Hand out a proof "warranty" that expires (wild)** — FEATURE — value 3 — effort M — risk low — category: proof
  Why: wild. A proof is stamped with the commit, the dependency lockfile hash and the date. When any of them moves under the touched files, the label flips to "stale" in `fm next` and the nightly tick re-runs it. The user sees a decaying trust figure rather than a permanent checkmark.
  Done when: changing a dependency pin that a closed task's proof touches turns that task's label to "stale" on the next tick.

- **Prove the headless case: UI checks that say why they didn't run** — FIX — value 4 — effort S — risk low — category: proof
  Why: the pack asks how a receipt says "unproven" when no display or browser exists. Detect the missing display or browser up front, record "could not run: no display" and refuse to let the task close as proven without a user override that is itself recorded as an override.
  Done when: closing a UI task in a headless shell yields "could not run: no display" on the receipt and `fm task finish` refuses a "proven" label.

- **Restore drill: prove the proofs survive a wiped host** — FEATURE — value 3 — effort M — risk low — category: proof
  Why: the pack asks what must be rebuilt by hand on a new host. A `fm restore --drill` clones the repo and ledgers into a temp dir, rebuilds state and re-runs a sample of proofs, then lists what didn't come back (timers, grants, hand-set config).
  Done when: the drill prints a pass or fail per ledger and per timer, and names each item needing manual setup.

Next question: Which proof states does the user actually read (receipt, `fm doctor`, site, digest), and which would they act on if it turned red?
Next question: What proof exists for Foreman's own self-change gate, and who checks the checker when its bench is the only witness?
