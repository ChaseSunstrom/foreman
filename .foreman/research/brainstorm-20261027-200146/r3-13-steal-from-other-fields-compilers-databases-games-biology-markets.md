# Brainstorm — lens: steal from other fields (compilers, databases, games, biology, markets)

- **Trip a circuit breaker on a failing model runner** — FIX — value 4 — effort S — risk low — category: resilience
  Why: The pack shows runs stalling and failing over (the stalled-run card, T-0337 blocked on Gemini's done-gate), and `fm run` waits out usage limits, but nothing stops it from calling a runner that has failed several times in a row. Assumption: repeated failures are not rare.
  Done when: After 3 consecutive failures, the next run skips that runner without calling it and prints one line saying why; a single probe runs after a cooldown and closes the breaker on success.

- **Cut off dependent checks when an output hash doesn't change** — PERFORMANCE — value 4 — effort M — risk low — category: build graph
  Why: The pack lists `fm check --affected`, `--evidence` and the full gate as separate reruns, and an earlier idea memoizes by file hash. Early cutoff (as in Shake and Bazel) goes further: a changed input whose output is identical stops the rerun from spreading to dependents. Assumption: many edits are comment-only or formatting-only.
  Done when: A comment-only edit reruns zero dependent checks, and the verdict line names each check that was cut off and why.

- **Halt the queue when burn spikes, like a trading halt** — FEATURE — value 4 — effort S — risk low — category: usage guard
  Why: The user said Foreman should have caught its own usage burn without being told ("foreman should've figured it out itself"). Nothing in the pack halts on a sudden rate change, only on totals.
  Done when: When the burn rate over 10 minutes exceeds 3× the trailing hour, the queue pauses with one line naming the cause, and one command resumes it.

- **Add hysteresis to the usage governor** — FIX — value 3 — effort S — risk low — category: governor
  Why: The governor picks model and context from a threshold (compact at 200k, builders on Sonnet). Assumption: a burn figure that hovers near the threshold will flip the choice back and forth, as a thermostat without a deadband does.
  Done when: A burn signal oscillating within ±5% of the threshold causes at most one switch per 30 minutes, checked by a test that replays a synthetic series.

- **Rank the backlog by value per effort with price-time priority** — FEATURE — value 3 — effort S — risk low — category: backlog ranking
  Why: Every backlog item already carries value 1–5 and effort S/M/L, and there are over 40 open or deferred items, but the order is picked by hand. Borrowed from exchange order books: higher value and smaller effort first, ties by age.
  Done when: `fm next` returns the same top item on two runs over an unchanged backlog and prints the tie-break it used.

- **Group-commit hook events into one write** — PERFORMANCE — value 3 — effort S — risk low — category: hook latency
  Why: The hook bench has a 300 ms p95 budget, and one run measured p95 at 272 ms on a quiet box against the 300 ms budget. Assumption: each hook event is written and synced alone. Database group commit amortizes one sync over a batch.
  Done when: `bench_hooks --runs 20` shows lower p95 on the same machine, and a test that kills the process mid-batch loses no event that was acknowledged.

- **Give each lane a stride-scheduled share of the gate** — FEATURE — value 3 — effort M — risk med — category: lane fairness
  Why: The gate lock is machine-wide, and the pack shows builders waiting behind one another. The auction idea allocates by expected value but gives no fairness bound. Proportional-share scheduling (stride, as in early OS schedulers) gives a guaranteed ratio.
  Done when: Two lanes with weights 2:1 receive 2:1 of 60 simulated gate slots in a test.

- **Keep `fm status` as a materialized view, updated per event** — PERFORMANCE — value 3 — effort M — risk low — category: status reads
  Why: `fm status` and the Today charts appear to recompute from the journal on every read. Assumption: that cost grows with history. Incremental view maintenance from databases updates the summary per event instead.
  Done when: `fm status` on a 10,000-event journal answers in under 50 ms and matches a full recompute in a test.

- **Compact journals in levels, as an LSM tree does** — CLEAN — value 3 — effort M — risk med — category: journal storage
  Why: The repo holds about 1,800 files and every run appends. Assumption: journals grow without bound. Level-based compaction keeps recent events hot and folds older ones into summaries.
  Done when: Compacting a 100,000-event journal shrinks it, and `fm why` on every run prints the same output before and after.

- **Share failure fingerprints across installs, opt-in only** — FEATURE — value 3 — effort L — risk high — category: shared immunity
  Wild: Immune memory across hosts. Each install sends a hash of a failing check's signature, with no source text, and gets back the fix other installs accepted.
  Why: Assumption: many failures repeat across projects. The local-first rule in the pack means nothing leaves the machine without an explicit setting.
  Done when: With the setting off, a test records zero network calls; with it on, the sent payload contains only the hash and the check name, and a known fingerprint returns a suggested fix.

- **Store each proof with parity so a damaged journal can be rebuilt** — FEATURE — value 2 — effort M — risk low — category: durability
  Wild: Erasure coding for evidence. Each proof is split into shards with parity, borrowed from storage systems.
  Why: Assumption: proof files are the only record of what was checked, so losing one loses the receipt.
  Done when: Deleting one of four shards still lets `fm why` reconstruct the proof, and the output says it was rebuilt.

- **Render the pane's predicted state, then reconcile on the journal** — FEATURE — value 3 — effort M — risk low — category: pane responsiveness
  Wild: Rollback netcode from multiplayer games. The pane shows the expected next state at once, then rolls back and redraws if the journal disagrees.
  Why: Assumption: the pane lags the journal during active runs, which is why the pack asks for live countdowns and motion that reflects state.
  Done when: A key press changes the pane within one frame, and a forced mismatch redraws the pane from the journal with no stale state left in a snapshot test.
