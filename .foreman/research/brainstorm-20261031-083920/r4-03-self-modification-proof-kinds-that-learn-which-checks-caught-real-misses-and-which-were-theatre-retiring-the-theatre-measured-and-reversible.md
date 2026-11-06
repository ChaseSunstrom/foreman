# Brainstorm — lens: self-modification: proof kinds that learn which checks caught real misses and which were theatre, retiring the theatre, measured and reversible

- **Mine ground truth from fix-after-done commits** — FEATURE — value 5 — effort M — risk low — category: proof learning
  Why: the catch ledger ideas need labels, and real reopens are rare. Git already records them: later commits naming a closed T-id, reverts, and "Fixes T-NNNN" trailers. Assumption: commit trailers or messages carry task ids reliably.
  Done when: `fm proof labels` lists closed tasks with a later fix or revert, each with the proof kinds that blessed it, and a test repo with 3 planted fix-after-done pairs yields exactly those 3.

- **Retire only on a statistical bound, not a streak** — FIX — value 4 — effort S — risk low — category: retirement rule
  Why: "N consecutive no-signal runs" retires a rarely-firing kind that simply hasn't met its bad case yet. Assumption: kinds fire at very different rates. Use a rule-of-three upper bound on catch rate over *applicable* runs.
  Done when: a kind with 5 runs and 0 catches is never retired, one with 300 runs and 0 catches is, and a test shows the same streak length giving different outcomes at different run counts.

- **Classify each proof failure's resolution: code fixed or check weakened** — FEATURE — value 5 — effort M — risk med — category: theatre detection
  Why: a failure that the builder cleared by editing the check or the verify command is not a catch, and counts as a loosened gate. Today a "catch" and a retreat look the same. Assumption: the diff between the failing run and the next green run is available.
  Done when: a fixture where a failing assertion is deleted is scored "weakened" and not credited to the kind, and `fm proof ledger` shows the split per kind.

- **Make every policy change a task that carries its own replay evidence** — FEATURE — value 4 — effort M — risk low — category: self-application
  Why: the retirer is itself an unproven change. Require each retire, revive or reorder to ship through `fm ship` with a before/after run over replayed closed tasks. Assumption: replay of closed tasks is cheap enough to run per change.
  Done when: a policy edit with no replay record is refused by `fm doctor`, and a test shows the record naming tasks replayed and verdict diffs.

- **Bisect policy history when reopens rise** — FEATURE — value 4 — effort M — risk low — category: reversibility
  Why: when the reopen or unproven rate climbs, the cause may be one retirement from weeks ago. Policy changes are versioned, so a bisect can replay the history under each policy snapshot.
  Done when: given a synthetic history where one retirement raises misses, `fm proof bisect` names that change and offers a one-command revert.

- **Order verify steps by catch-per-second, fail-fast** — PERFORMANCE — value 3 — effort S — risk low — category: proof speed
  Why: order does not change the verdict but does change time to a red. Cheap, high-catch checks should run first. Assumption: per-kind timings and catch counts are in the ledger.
  Done when: on a fixture with a slow no-catch check ahead of a fast catching one, a failing run's time to first red drops, and the order is shown in `fm prove --plan`.

- **Collapse kinds that always agree into one** — CLEAN — value 3 — effort M — risk med — category: redundancy
  Why: uselessness isn't the only waste. Two kinds that pass and fail together on every replayed task double the cost for one signal. Assumption: enough shared history exists to compute agreement.
  Done when: `fm proof overlap` prints a kind-by-kind agreement matrix and flags pairs agreeing on at least 95% of 30+ shared runs, with the cheaper one kept.

- **Run kinds as randomized experiments with an interval** — FEATURE — value 4 — effort M — risk med — category: measurement
  Why: shadow mode and silent samples exist, but a fixed rule can't tell "no catches" from "no exposure". Randomly hold out some tasks per kind so catch rate has a confidence interval.
  Done when: `fm proof ledger` shows each kind's catch rate with a CI and its holdout share, and a test confirms assignment is seeded and reproducible.

- **Wild: Breed stricter mutants of each check overnight** — FEATURE — value 3 — effort L — risk med — category: evolution
  Why: wild. A nightly lane tries variants of a theatre check (tighter threshold, extra assertion) against the planted-fault set and proposes the one that catches more at similar cost.
  Done when: for a seeded weak check, the lane files a task proposing a variant that catches a planted fault the original missed.

- **Wild: Séance the retired** — FEATURE — value 3 — effort M — risk low — category: second opinion
  Why: wild. Before retirement is final, a cold different-house model blind-judges the kind's last 50 runs and says which it would have objected to. A gap flags a kind that may be silent for reasons the ledger can't see.
  Done when: retirement of a fixture kind is held when the cold judge objects to 5 or more runs the kind passed, and the held reason quotes them.

- **Wild: Retirement insurance that revives on a hit** — SECURITY — value 4 — effort M — risk low — category: tripwire
  Why: wild. Each retirement records the files and claims the kind covered. A later fix commit touching them auto-revives the kind in shadow mode and files a task naming the retirement.
  Done when: in a fixture, a fix commit touching a retired kind's covered path flips the kind to shadow and files exactly one task.

- **Wild: A/B two whole proof policies over repo history** — FEATURE — value 3 — effort L — risk med — category: policy diff
  Why: wild. Replay the same closed tasks under the current and a candidate policy, and show verdict diffs: what the new one would have missed or caught.
  Done when: `fm proof ab OLD NEW` prints per-task verdict differences, and on a fixture with one retirement it lists the one task whose verdict flips.

- **Explain a kind's standing in one command** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: the user's job is to veto or overrule, which needs the evidence. Show the three best catches, three misses, cost, trust state, and the undo command.
  Done when: `fm proof why KIND` prints those fields, each quoting a task id, and a test checks a kind with no history says so plainly.

Next question: What does the user do after Foreman retires or revives a kind, and does any trace of that reaction (an override, a revive, a later reopen) feed back into the ledger as a label?
Next question: Which proof kinds guard things whose failures are rare but catastrophic, so a catch-rate rule must never touch them?
