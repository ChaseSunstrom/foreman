# Brainstorm — lens: steal from other fields

- **Score every lane with an early-warning number** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: hospitals use the NEWS score, which folds several weak vitals into one number with graded responses. The pack has single tripwires (Stop-hook cap, tier escalation, quarantine after three failures) but no composite. Assumption: the ledger already has retries, edits per file, test flaps, and tokens against forecast.
  Done when: a replayed ledger of a thrashing lane crosses score 5 and triggers a fresh-eyes diagnosing agent, and crosses 7 and triggers a pre-committed turnaround (salvage and stop). A healthy lane stays under 2.

- **Run drug-safety signal detection on rules and hints** — FEATURE — value 5 — effort S — risk low — category: self-improvement
  Why: the pack scores hints by hit rate, but pharmacovigilance asks whether the harm co-occurs more than baseline. For each rule or hint, build a 2×2 table of fired versus a user correction or interrupt within 3 turns, then compute the proportional reporting ratio (PRR). The user's repeated "still cluttered" complaints suggest some injected rules cause harm silently.
  Done when: `fm learn signals` lists rules with PRR ≥ 2 and n ≥ 5 from a fixture ledger, and a planted harmful rule ranks first.

- **Mine conserved quantities from history and flag diffs that break them** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: this is Noether-style invariants, as in Daikon. Walk git history for quantities that never changed, such as test count never decreasing, the public CLI verb set, or hook latency under the budget. Flag a diff that breaks a long-held invariant. Gate failures like the PATH and claude-lockout ones were invariants nobody had written down. Assumption: false positives are tolerable if the flag is advisory.
  Done when: on this repo, `fm invariants` proposes at least 3 held invariants. A fixture diff that deletes a test is flagged with the commit span that supports the invariant.

- **Pull an Andon cord that halts merges fleet-wide** — FEATURE — value 4 — effort S — risk low — category: fleet
  Why: Toyota lets any worker stop the whole line. Foreman has per-task quarantine, but a reviewer or lane that finds a systemic fault (a red gate on main, a bad hint) cannot freeze other lanes' merges. Assumption: merges pass through one `fm` code path that can check a marker.
  Done when: `fm andon pull "why"` makes other lanes' close and merge refuse with the reason. It clears only through `fm andon clear` with a recorded cause, and the pane shows the line stopped.

- **Cold back-translation of every plan** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: translators check fidelity by translating back without seeing the source. The pack asks Foreman to warn when a plan is bigger than the request implies. A Haiku child that sees only the plan and writes the request it would have come from, scored against the verbatim capture, catches misreads before any edit.
  Done when: a fixture where the plan solves the wrong problem scores below threshold and blocks the plan stage. A faithful plan passes, and the cost is one Haiku call per plan.

- **Annotate each session like a chess game with an eval bar** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: the pack has per-step splits and a work bar, but no signed judgement on how each move changed the position. Compute an eval from criteria green/total, test delta, and scope drift. Mark each step ! or ?, show the bar in the pane, and have the close-out list the blunders with step ids. Assumption: the three inputs are in the ledger now.
  Done when: a fixture session where step 3 turns a passing test red gets "?" on step 3. The pane shows the bar dropping and rising, and `fm learn` can read the ? steps.

- **Plan hold points and witness points** — FEATURE — value 4 — effort S — risk low — category: autonomy
  Why: construction inspection plans mark hold points (work stops until inspected) and witness points (notify, proceed unless objected). The pack has deadline-default asks and earned autonomy, but no per-step taxonomy. Planning marks each step none, witness, or hold.
  Done when: a hold step blocks the next step's edits via PreToolUse until the user answers. A witness step posts a notification and proceeds after its window, and both appear on the stage rail.

- **Detect the P-wave before the user interrupts** — FEATURE — value 4 — effort M — risk med — category: prediction
  Why: seismographs catch the small early wave before the damaging one. Sequence-mine the 5 tool events before each Esc or correction (already logged) and find precursors, such as the third repeated failing edit or a read of a generated file. Flag them live with a one-line nudge. Assumption: enough interrupts exist to mine, since the user has steered often.
  Done when: offline mining over the ledger produces ≥1 precursor pattern with lift ≥ 2. Replaying a session containing it fires the nudge before the interrupt step.

- **Make the user's challenge flag buy a full re-verification** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: sports review lets a coach spend a limited challenge. `fm challenge T-xxxx` or one key in the pane triggers an independent re-verification, run by a fresh agent with no access to the builder's claims. Overturn and uphold rates per claim type calibrate how much "done" is trusted.
  Done when: a challenged fixture task with a faked claim is overturned and recorded. The scoreboard shows upheld versus overturned counts by claim type.

- **Wild: leave decaying scent marks on files for later agents** — FEATURE — value 4 — effort M — risk low — category: coordination
  Why: ants coordinate through evaporating pheromone trails instead of messages. A PostToolUse sidecar records per-path marks (bit me, generated file, flaky, hot) with a 2-day half-life. A PreToolUse Read or Edit injects one line from the strongest mark. This is persistent and per-file, unlike the planned overlap prediction. Assumption: one line per edit stays inside the token budget.
  Done when: after a lane records "generated, don't hand-edit" on a file, the next lane's first Edit of it shows the line. After two days the mark has halved and then disappears.

- **Wild: issue TCAS-style resolution advisories to colliding lanes** — FEATURE — value 3 — effort M — risk med — category: concurrency
  Why: aircraft collision avoidance gives the two planes complementary instructions in real time, not just a pre-flight plan. When PreToolUse sees a live lane about to edit a file another lane edited in the last N minutes, it applies a deterministic tie-break through the lease. One lane proceeds and the other gets "yield: rebase on lane X first". Planned overlap prediction cannot cover files that only become hot mid-run.
  Done when: two fixture lanes editing the same file produce exactly one yield advisory, and the yielding lane resumes after the other closes without a conflict.

- **Wild: grow the brain's family tree** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: biologists draw lineages. Every hint, rule, and card variant becomes a node that records its parent and mutation (merged, split, retired, re-promoted), coloured by PRR and hit rate. The pane's idle screen can show the branches that thrive and the dead lines. Assumption: the provenance ledger already stores parent ids.
  Done when: `fm learn tree` prints an ASCII phylogeny from a fixture store, with retired lines marked and survivors showing their lift.

- **Show a pit-wall ETA with a probability for the queue** — FEATURE — value 3 — effort S — risk low — category: forecasting
  Why: F1 strategy teams run Monte Carlo over race outcomes. Sample each queued task's duration from similar closed tasks and report "P50 6:40pm, 80% chance done by 8pm" in the pane and in `fm night`. This builds on the planned per-task forecast and the "land a verified state at return time" wild idea. Assumption: ≥20 closed tasks exist per tier.
  Done when: `fm next --eta` prints P50 and P90 for the queue, and a backtest on closed history has P90 coverage between 85% and 95%.
