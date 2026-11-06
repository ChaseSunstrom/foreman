# Brainstorm — lens: reliability

- **Grade infra failures as "ungradable", never a loss** — FIX — value 5 — effort S — risk low — category: exam integrity
  Why: selection rests on "closes more scenarios than its parent"; a timeout, missing toolchain or OOM that scores as a fail silently lets a worse rewrite win or a better one lose. Pack shows 6 languages and many arms, so infra noise is certain. (Appears only as a one-liner earlier; this makes it a typed result.)
  Done when: a scenario killed by timeout/missing binary is recorded `ungradable` with a reason, excluded from both sides of selection, and a generation with >20% ungradable refuses to select.

- **Run an oracle-and-empty health check before every grading pass** — FEATURE — value 5 — effort S — risk low — category: exam integrity
  Why: exam has an oracle and an empty arm already; running them first catches a broken exam (oracle fails, or empty passes) before spending on child arms. Assumption: the check isn't currently automatic per pass.
  Done when: a deliberately broken scenario (oracle fails) aborts the pass with the scenario id before any model arm runs.

- **Ratchet selection: a rewrite cannot reopen what its parent closed** — FEATURE — value 4 — effort M — risk med — category: selection
  Why: "closes more" lets a child gain 3 and lose 2 and still win, hiding regressions. A per-scenario ratchet makes lineage monotone.
  Done when: a fixture child that closes +3 but regresses 1 previously-closed scenario is rejected with the regressed id named.

- **Run every child in its own process group with a lease file and a reaper** — FIX — value 4 — effort M — risk med — category: process safety
  Why: tower spawns tool-less children, session arms, lanes and detached publish; a crashed orchestrator leaves orphans burning quota (budget is hard-capped). Assumption: no reaper exists today.
  Done when: killing the orchestrator mid-generation leaves zero child processes after the next `fm genesis` open, and the reaper logs what it killed.

- **Validate every child's output against a schema, retry once on repair** — FIX — value 4 — effort S — risk low — category: child output
  Why: gen-0 writer, Seed, Mission and critique outputs are free text parsed by the tower; a truncated or off-format reply must not be stored as a generation doc.
  Done when: a malformed Seed reply triggers exactly one repair retry, then a typed `child-invalid` failure; nothing is written to the tower.

- **Make the exam runner hermetic** — FIX — value 4 — effort M — risk low — category: determinism
  Why: held-out comparisons between generations are only meaningful if reruns agree. Pinned clock, locale, seed, no network, per-scenario timeout.
  Done when: the same scenario run twice on the oracle yields byte-identical results, and a scenario that touches the network fails loudly.

- **Quarantine flaky scenarios before they decide a selection** — FEATURE — value 4 — effort M — risk low — category: exam integrity
  Why: a scenario that flips on identical input contributes noise equal to a real gain. Run the parent 3× on borderline selections and drop disagreeing scenarios.
  Done when: a planted flaky scenario is auto-quarantined with a note, and the selection verdict is computed without it.

- **Never land over the user's live edits** — SECURITY — value 5 — effort S — risk low — category: safety
  Why: Genesis ships to main on its own (`live on`, standing grant) and runs lanes; a dirty tree or concurrent session must block landing.
  Done when: with an uncommitted edit to a target file, publish defers and reports it; the edit is byte-intact afterwards.

- **Trip an auto-start breaker on Genesis's own failure rate** — FEATURE — value 4 — effort S — risk low — category: autonomy
  Why: auto-start from a dry queue repeats; three consecutive aborted or no-gain towers should stop it proposing and say why.
  Done when: after N failed towers, the next dry queue yields no proposal and `fm genesis status` names the breaker.

- **Inject a fake clock into the orchestrator** — CLEAN — value 3 — effort S — risk low — category: testability
  Why: cooldowns, usage-reset waits, debounce and dead-man timers can't otherwise be tested in the gate suite.
  Done when: a test advances a fake clock 24h and asserts the cooldown release and debounce flush with no sleeping.

- **Wild: Replay the whole tower from recorded model outputs** — FEATURE — value 4 — effort L — risk med — category: replay
  Why: wild. Record each child reply; `fm genesis replay` re-runs orchestration, selection and drift with zero model calls, so gate tests cover the real state machine.
  Done when: replaying a recorded 2-generation tower reproduces the same lineage file byte for byte at $0.

- **Wild: Chaos monkey on a fixture project** — FEATURE — value 3 — effort M — risk low — category: resilience
  Why: wild. Randomly kill the process, truncate a file or fail a child at each stage on a fixture; the tower must resume to the same end state.
  Done when: 20 seeded chaos runs all converge to the fixture's expected lineage or a typed halt, never a corrupted tower.

- **Wild: Nightly canary project that pages on regression** — FEATURE — value 3 — effort M — risk low — category: monitoring
  Why: wild. A small frozen project runs "make this great" nightly on the current Foreman; a drop in closed scenarios shows on the site page and next session.
  Done when: a deliberately weakened template makes the canary score fall and surface a warning within one run.

- **Pin the Foreman code version for the length of a generation** — FIX — value 3 — effort S — risk low — category: determinism
  Why: Foreman is edited by its own lanes while a tower runs; a mid-generation change to the exam or grader makes parent and child incomparable.
  Done when: each generation records the code commit, and a mismatch between parent and child grading commits forces a re-grade of the parent.

Next question: Which Genesis stages write outside the tower directory (site publish, lanes, task queue), and does each have an idempotency key so a retry cannot double-apply?
Next question: When the exam grader and the exam author disagree on a scenario's key, who is the tiebreaker and is that recorded anywhere?
