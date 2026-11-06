# Brainstorm — lens: 2030 worked back

- **Key every output by its trigger event** — FIX — value 4 — effort S — risk low — category: reliability
  Why: assumption: catch-up on resume, retries and drive restarts re-fire events. The pack covers deduping inputs (CI signatures, subject keys) but not outputs, so a re-fire could open a second branch, PR or comment.
  Done when: firing the same event twice, including after a killed run, yields one branch/commit trailer/comment, and the second run adopts the first's output. A test asserts this.

- **Arm new triggers only inside a fleet error budget** — FEATURE — value 5 — effort M — risk low — category: unattended safety
  Why: the request names "drive stops appeared (0 to 0.1)" and "failed tool calls up by half". The pack has per-session failure budgets but no night-wide budget that blocks adding more automation while the existing automation is unhealthy.
  Done when: with the trailing-7-night stop rate or failed-call rate over budget, `sampo trigger arm` refuses and names the number. An exam fixture shows it re-allowing once the rate recovers.

- **Audit trigger referents weekly for rot** — CLEAN — value 4 — effort S — risk low — category: durability
  Why: assumption: over four years, paths, branches, model profiles, endpoints and repos vanish. The Foreman→Sampo rename already shows names moving. Dry-resolve every noun in the triggers file (path, profile, remote, verb) and report dead ones in the morning card.
  Done when: renaming a watched path in a scratch repo makes the next audit name the trigger and the missing referent, and the trigger parks itself.

- **Decay autonomy with time since the user last looked** — SECURITY — value 4 — effort M — risk med — category: trust
  Why: the pack has leases and a dead-man switch on the morning card, but both are on/off. A trust half-life steps each trigger down its autonomy rung (push → branch → draft → observe) as days pass without a check-in, and restores it with one key. It is a gradient between "armed" and "paused".
  Done when: a simulated clock jump of 3, 7 and 14 days shows each trigger's rung drop on schedule, and a check-in restores them.

- **Allocate the night's tokens by measured yield per cost** — PERFORMANCE — value 4 — effort M — risk low — category: scheduling
  Why: the user wants "overnight progress unattended" and unlimited local volume. The pack has fair splits per repo and cheapest-executor bidding, but no signal for which trigger kinds actually closed work last month. Add an exploration floor so new triggers still get a chance.
  Done when: `sampo trigger budget` prints each trigger's tasks-closed-and-surviving per unit cost. A replayed month shifts allocation toward the high-yield triggers while every trigger keeps at least its floor.

- **Lint trigger sets for conflicts** — FIX — value 3 — effort S — risk low — category: correctness
  Why: assumption: file, CI and schedule triggers will multiply, and two can target the same files or issue with opposite aims (a formatter against a refactor lane). Goals are linted against each other but triggers are not.
  Done when: two fixture triggers with overlapping globs and opposing intents fail `sampo trigger lint` with both ids named.

- **Export a causal trace in a standard shape** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: assumption: by 2030 other tools will read traces. The pack plans a "why did this start?" ledger, but only in Sampo's own format. Emit event → trigger → task → commit spans as OpenTelemetry-style JSON lines alongside it.
  Done when: a fired trigger's chain validates against the trace schema, and the same ids appear in the ledger and the file.

- **Seal the trigger ledger into monthly rollups** — CLEAN — value 3 — effort M — risk med — category: state
  Why: the pack's state is already 2.4 GB, and every fire/skip reason adds to it. Keep per-month counts by reason plus the last N full rows, and make the rollup enough to recompute the yield and rot metrics above.
  Done when: rolling up a fixture year shrinks it by at least 10x, and yield and silence reports computed from the rollup match the ones from raw rows.

- **Wild: record run tapes so future models can rerun them** — FEATURE — value 4 — effort L — risk med — category: time-travel
  Why: wild. Store each triggered run's redacted brief, model id, tool-response digests and verdict. A later `sampo tape rerun --model X` reruns only the failed or stopped runs on a stronger model and prints what newly passes. The user gets a dated "frontier moved" report built from their own work, not a public benchmark.
  Done when: rerunning a tape from a fixture night on a stub model produces a per-run pass/fail diff against the original verdict.

- **Wild: keep a graveyard of retired triggers** — FEATURE — value 3 — effort S — risk low — category: memory
  Why: wild. Retired or parked triggers go into a searchable graveyard with the reason they died (ignored, looped, cost, rot). Arming a new trigger first shows its three nearest graveyard neighbours, so the same dead idea isn't reinvented every generation.
  Done when: arming a trigger that resembles a parked one prints that entry's cause of death and requires a one-line justification.

- **Wild: fire triggers on capability crossings, not clocks** — FEATURE — value 4 — effort M — risk low — category: local models
  Why: wild. The user wants local models used "without limit". Let a trigger wait on a predicate such as "the local endpoint first passes ≥X% on the held-out bench for task kind K". Then the deep-audit or backlog-grooming lane starts the day the hardware earns it. The model bench and fingerprinting already exist; this wires them to the trigger intake.
  Done when: a fixture bench result crossing the threshold fires the dormant trigger exactly once, and a drop below it re-parks it.

Next question: Which of Mission 6's own triggers, if left running untouched for six months, would the user have to rescue by hand, and does any ledger show that rescue coming?
Next question: When a trigger's output is correct but arrives in a form the user must re-type to use (a card, a branch, a comment), where does that last-metre friction get measured?
