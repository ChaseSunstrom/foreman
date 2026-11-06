# Brainstorm — lens: deepen: verification

- **Build a proof-strength ledger that fuses mutation, coverage and red-first into one score** — FEATURE — value 5 — effort L — risk med — category: verification
  Why: the list holds many separate probes (mutate the proof, reject empty verifies, measure diff coverage by evidence, red-first, strength ladder). The T-0342 incident shows a verify that ran no tests passed silently. One score per criterion (did it fail before, does it fail under mutation, did it execute diff lines) turns these into a single gate.
  Done when: `fm task done` on a task with a vacuous `-k` verify prints a per-criterion score below the threshold and refuses; a real red→green criterion scores at or above it.

- **Replay the verifier against the pre-fix commit automatically** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: assumption: FIX briefs have a recorded base commit. Checking each verify out against the parent commit in a temp worktree proves it can fail, with no mutation tooling. It is the cheapest "gate that can't fail" detector, and the other probes can build on it.
  Done when: a FIX whose verify also passes on the base commit is refused with that commit's hash shown.

- **Maintain a claim graph linking every sentence of a done summary to its evidence** — FEATURE — value 4 — effort L — risk med — category: verification
  Why: assumption: summaries today are free text. Parse each claim ("login times out no more", "no other callers") into a node, attach the evidence event that supports it, and flag unsupported claims. Context-blind checkers (already listed) can then verify node by node instead of reading a blob.
  Done when: a done summary containing a claim with no linked evidence is flagged by name, and `fm tour` shows claim→evidence links.

- **Run a verification canary: plant known bugs and check the gates catch them** — FEATURE — value 5 — effort L — risk med — category: verification
  Why: `fm sentinel` re-runs old checks, but nothing measures gate sensitivity. Periodically (via `fm night`) inject seeded faults from a library mined from past FIX tasks into a scratch worktree and record the catch rate. A falling rate is a project-level health signal.
  Done when: `fm doctor` reports a catch-rate figure per project, and a deliberately neutered gate lowers it.

- **Learn a per-project verification policy from escapes** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: the repo has lessons with confidence (T-0217) and `fm surprise`. When a bug is reported against a task already marked done ("There's new bug feedback", T-0317), record it as an escape and link it to the weak proof. Escapes then raise the required evidence tier for similar future tasks.
  Done when: after an escape is logged against a task, a new task touching the same files requires a higher gate tier, shown in `fm gates`.

- **Verify by independent re-derivation: a second agent solves the spec without seeing the diff, then the two are compared behaviourally** — FEATURE — value 4 — effort L — risk med — category: verification
  Why: builds on `fm oracle` (examples from the spec alone) and differential testing. Run the oracle's examples against the implementation, then have the independent solution disagree on inputs found by fuzzing. Disagreements become either bugs or spec ambiguities.
  Done when: for a task, `fm oracle --diff` outputs a list of inputs where the two implementations differ, or states there were none across N inputs.

- **Treat the guard as a verified artifact: formal-ish differential fuzzing against real bash with property invariants** — SECURITY — value 4 — effort M — risk low — category: verification
  Why: the guard keeps being fixed one case at a time (bash -lc, symlink rm, python -c, T-0275). A grammar-based generator of shell lines, compared with real bash on a sandbox, finds the next hole before JARVIS does. The 5000-command replay only covers what already happened.
  Done when: a fuzz run of N generated commands reports zero cases where the guard allows a write outside the sandbox that real bash performed, with a seed to reproduce any finding.

- **Prove step evidence belongs to the step with causal tracing** — FEATURE — value 3 — effort M — risk med — category: verification
  Why: T-0406 made evidence move the current step, which means evidence is now trusted for progress. Tag each evidence run with the file hashes at the time, and invalidate evidence when its inputs change afterward.
  Done when: editing a tested file after step evidence was recorded marks that step "stale" in the band and blocks done until re-proved.

- **Wild: Run a verification tournament where agents bid on how to break the change, and paid-out bugs fund the budget** — FEATURE — value 4 — effort L — risk high — category: verification
  Why: wild. Several red-team agents (for example property-based, boundary, concurrency, hostile-input) each submit one failing test. Score by distinct real failures. Agents that find nothing in several rounds get a smaller budget next time, so effort follows yield.
  Done when: a tournament run on a seeded-bug diff produces at least one failing test attributed to a named agent, and the budget file reflects the allocation.

- **Wild: Verify against a digital twin of the user, replaying their own session habits on the product** — FEATURE — value 4 — effort L — risk high — category: verification
  Why: wild. `fm smoke` checks the product "the way its user uses it", but with generic flows. Derive journeys from the user's real traces (the transcripts and `fm usage`), such as slow wifi in the login-timeout example, and replay them with network and device throttling profiles.
  Done when: `fm smoke --twin` runs journeys derived from recorded sessions under a throttled profile and reports per-journey pass/fail.

- **Wild: Time-travel bisect for every regression the sentinel finds** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: wild. When `fm sentinel` finds a previously passed check now failing, auto-bisect across Foreman-recorded commits (each task commit is already atomic) in a worktree, and file a FIX brief naming the culprit task and its lessons.
  Done when: a seeded regression produces a queued FIX task citing the offending task ID without user input.

- **Assert cross-task invariants: decisions and vetoes become executable checks** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: `fm decide` and `fm vetoes` store rules as prose, checked on commands and edits only. Compile decisions like "subagents are never capped by a token count" into greps or tests, and run them at done so old choices cannot silently be undone.
  Done when: a decision with an attached check fails `fm task done` for a diff that violates it, naming the decision ID.

- **Make evidence tamper-evident with a hash-chained ledger and a signed done receipt** — SECURITY — value 3 — effort M — risk low — category: verification
  Why: the ledger is the source of truth for "verified with recorded evidence", yet an agent with edit access could rewrite it. Chain event hashes and emit a receipt that `fm pr` and `fm sync` include, so reviewers can check the proof wasn't edited after the fact.
  Done when: editing an old ledger event makes `fm doctor` report a chain break at that event.

- **Score verification debt per area and steer the queue toward it** — FEATURE — value 3 — effort M — risk low — category: verification
  Why: combine hot files from `fm map`, escapes, and weak-proof scores into a map of under-verified areas. The drive offers "harden X" tasks when it would otherwise idle (the JARVIS idling complaint).
  Done when: `fm next` on an empty queue proposes a hardening task naming the lowest-scoring area with its score.
