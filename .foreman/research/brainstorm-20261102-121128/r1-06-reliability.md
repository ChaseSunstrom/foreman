# Brainstorm — lens: reliability

**Answers to earlier questions, from the reliability lens**
- Ledger readers: any reader that counts, ranks or computes a rate (Brier, base rate, survival) would give a wrong number, not an error, if a record class vanished. Idea 1 tests this.
- Unrunnable UI checks must record "unproven" as its own state, never a skipped pass. Idea 2.
- Overrides need a separate record that says "override, not proof". Idea 6.

---

- **Delete-a-record-class drill** — FEATURE — value 5 — effort M — risk low — category: ledger integrity
  Why: assumption: readers like outcomes, calibration and bet settlement silently produce plausible numbers on partial data, as the "compare like with like" fixes (T-2610) suggest.
  Done when: `fm doctor --ledger-drill` copies each ledger to a scratch dir, drops one record class at a time, and fails for any reader whose output changes without a warning.

- **Make "unproven" a first-class receipt state** — FIX — value 5 — effort S — risk low — category: proof
  Why: the pack asks how a UI check without a display is told apart from a pass. The web UI and foreman-ui checks are headless-prone.
  Done when: a finish run with no display records `unproven: no display`, `fm task finish` prints it distinctly from "proven", and a test asserts it can't count as a pass.

- **Record overrides as overrides** — FEATURE — value 4 — effort S — risk low — category: proof
  Why: the pack asks who records that a hand override isn't proof.
  Done when: `fm task prove --override "reason"` writes a row marked `override`, which `fm outcomes` and the receipt list separately and never count as held.

- **Track reversed "proven" labels** — FEATURE — value 5 — effort M — risk low — category: proof / calibration
  Why: the pack asks which proven labels were later reversed, and what share had no run record.
  Done when: `fm outcomes --reversals` lists tasks whose proof was later contradicted (reopened, reverted, CI red), with the share lacking a run record, and fm doctor shows the rate.

- **Cross-check self-written gauges against outside signals** — FEATURE — value 4 — effort M — risk med — category: ops trust
  Why: the pack asks which gauges Foreman trusts only because it wrote them. Timer liveness already reads systemd (T-2542).
  Done when: doctor compares bet settlement with git/CI outcomes and the canary state with a fresh independent run. It WARNs when the two disagree, in a test that plants the mismatch.

- **Restore drill for a replaced host** — FEATURE — value 4 — effort M — risk low — category: recovery
  Why: the pack asks what must be rebuilt by hand after a wipe. Install pieces such as timers, the mod and the memory dir are all outside the repo.
  Done when: `fm restore --drill` rebuilds from the repo plus a state backup in a temp HOME and prints a checklist of everything that needed manual steps. A clean run prints an empty list.

- **Hook circuit breaker: fail open on slow, fail closed on guard** — PERFORMANCE — value 4 — effort M — risk med — category: hooks
  Why: T-2605 caught a waiting hook only by a bench, and a library import failure already needed a fallback.
  Done when: a hook over its latency budget is skipped for the rest of the session with a logged note, the guard still blocks (a test with a sleeping hook shows both).

- **Flake quarantine with rates** — CLEAN — value 3 — effort S — risk low — category: tests
  Why: the LeanKind flake (T-2605) showed that one flaky gate can turn a self-change red.
  Done when: the suite records per-test pass rates, and a failing test with prior flake history is re-run N times before going red, with the verdict naming the history.

- **Version-skew check across installed parts** — FIX — value 3 — effort S — risk low — category: install
  Why: T-0418 (the installed foreman-ui is behind 0.6.1) is the kind of skew nothing flags.
  Done when: `fm doctor` WARNs when the CLI, plugin, mod and desktop app versions disagree, and a fixture test covers it.

- **Torn-write fuzz for ledgers** — FIX — value 4 — effort M — risk low — category: ledger integrity
  Why: assumption: ledger writes are append-based, and a crash mid-write (the night tick, a killed session) could leave a half row.
  Done when: a test kills the writer at random byte offsets, and each reader skips or repairs the torn row and names it.

- **Chaos run (wild)** — FEATURE — value 4 — effort L — risk med — category: fault injection
  Why: wild; the planted-faults tier (forced compaction, killed session, usage-limit pause) exists only for the long-horizon exam.
  Done when: `fm chaos` injects faults into a scratch drive (full disk, clock jump, killed child, missing `claude`) and reports which ones lost work or left a stuck lock.

- **Reproduce a sample of proofs cold (wild)** — FEATURE — value 5 — effort L — risk med — category: proof
  Why: wild; the standing steers prefer signals Foreman didn't author.
  Done when: nightly, a random sample of past "proven" commands is re-run on a clean checkout of the task's commit, and a mismatch lands in the inbox with both outputs.

- **Flight recorder for hook decisions (wild)** — FEATURE — value 3 — effort M — risk low — category: debuggability
  Why: wild; after a crash or a surprising block, nothing shows the last N guard and hook decisions in order.
  Done when: `fm replay --last 50` prints the most recent hook events with inputs, verdicts and timings, kept in a bounded ring file.

- **Log the user's own verification commands (wild)** — FEATURE — value 3 — effort S — risk low — category: unspoken checks
  Why: the pack asks what the user types by hand to check verdicts, without reading shell history. A `fm v <cmd>` wrapper logs only commands run through it, and nothing is read unless the user opts in.
  Done when: `fm v pytest -k x` runs the command, logs it as a user check, and `fm outcomes` shows which verdicts the user re-checked and whether they agreed.

Next question: Which Foreman failure would the user only discover days later, because every reader of that state still prints a confident answer?
Next question: What is the smallest outside-the-repo state (timers, mod, tokens, memory) whose loss would leave `fm doctor` green?
