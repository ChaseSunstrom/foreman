# Brainstorm — lens: bold bets

- **Characterize before you change** — FEATURE — value 4 — effort M — risk low — category: edge cases
  Why: gen-0 #2 asks for edge cases and blast radius, but the pack shows no step that records what the code does today. Several recent FIX tasks (T-2525, T-2540) were about unstated premises.
  Done when: for a task touching function F, `fm task plan` writes a snapshot test of F's current outputs on enumerated edge inputs, and a change that alters an unlisted output fails it.

- **Pick the edge-case atlas from the diff** — FEATURE — value 4 — effort M — risk low — category: edge cases
  Why: assumption: edge cases are currently listed from the model's memory. Stack cards (1219, 5 used) could carry short per-language and per-domain lists (empty input, encoding, time zones, idempotency, partial failure), chosen from the diff's signals.
  Done when: a plan touching a datetime parser shows the time-zone and DST entries, each marked covered, n/a with a reason, or probed. The gate refuses a plan with none of them addressed.

- **Cluster the open queue by root cause before planning any item** — FEATURE — value 4 — effort M — risk low — category: queue thinking
  Why: the open list has 28 "Later from T-07xx/08xx" bundles and many deferred items. Exhaustive thinking at queue level should find that five tasks share one cause.
  Done when: `fm next` flags tasks that share a file set or failure signature, offers one merged deliberation, and a test shows two seeded duplicates collapse into one plan.

- **Disambiguate by example, not by question** — FEATURE — value 4 — effort M — risk low — category: readings
  Why: the user's recurring steers are about letter defeating intent (T-2341, T-2525). When the readings disagree, show one concrete input/output pair per reading so the user answers with a single pick.
  Done when: an ambiguous fixture request produces a card with 2–3 example pairs, and the chosen pair is saved as a test.

- **Keep a deliberation graph that later tasks reuse** — FEATURE — value 4 — effort L — risk med — category: memory
  Why: assumption: readings, approaches, failure modes and probes are prose in each plan and are re-derived next time. Store them as a typed graph with branches keyed to file hashes, so a pruned branch stays pruned until its files change.
  Done when: a second task on the same module starts with the first task's rejected approaches and their reasons, and editing a file listed in a branch marks it stale.

- **Add a "trap" exam kind where the obvious fix is wrong** — FEATURE — value 4 — effort M — risk med — category: exam
  Why: the standing rules want weakness-finding from signals Foreman didn't author, and exam scenarios from a tool-less child. A child that never sees the code writes tasks whose first-instinct fix fails a hidden check, which tests #2 directly. Adding it is a `fm genesis grow` exam kind.
  Done when: `fm exam` has a trap kind with at least 6 child-authored held-out scenarios, and the scorecard reports how often foreman and plain take the first-instinct fix.

- **Run assumption probes before the plan is accepted** — FEATURE — value 3 — effort S — risk low — category: premises
  Why: assumption: plans assert flags, versions and paths without running anything. Each Assumption line gets a one-line probe, and the plan gate shows the result.
  Done when: a plan claiming `tool --flag` exists is blocked or annotated when the probe fails.

- **Model-check the task state machine by bounded exhaustive search** — FEATURE — value 3 — effort L — risk med — category: reliability
  Why: assumption: recent fixes (T-2540, T-2526, T-2534) are all odd task-state interleavings found one at a time. Enumerating every sequence of up to N verbs on a fake store finds the rest.
  Done when: a test enumerates all verb sequences up to length 5 and fails on any illegal state or lost write. It catches a seeded bug.

- **Spend deliberation tokens where expected regret is highest** — FEATURE — value 3 — effort M — risk med — category: depth
  Why: the brief says "scale depth to risk", but the pack shows only tier labels doing it. Allocate a per-day thinking budget across the queue by blast radius times irreversibility times past reopen rate.
  Done when: two tasks of the same tier but different blast radius get different recorded depth, and `fm doctor` prints the allocation.

- **Wild: a Decision Garden in the web UI** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: wild. The web UI is the only surface and the deliberation lives as text. Draw readings and approaches as a tree where branches visibly wilt as probes kill them, with a "prune this" button for the user.
  Done when: a finished task's page shows its options as a tree with each branch's kill reason, and a user prune is written back as a steer.

- **Wild: an eval bar for every task** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. Plot the task's confidence over time like a chess engine's eval bar, with each probe or surprise as a labelled swing. It uses the bet ledger Foreman already keeps.
  Done when: a closed task page shows a confidence line with at least its plan, first test and finish points, each linking to its evidence.

- **Wild: a blind edge-case author scored by what later broke** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: wild. A tool-less child sees only the task title and writes the edge-case list before the builder starts. Later reopens and fix-after-done commits score which list would have caught the bug, so the atlas learns from outcomes Foreman didn't author.
  Done when: the ledger shows, per task, the child's recall of the bugs found within 30 days, and the atlas ranks entries by it.

Next question: Which of the 58 empty cells name a session path that actually calls exhaustive thinking, and which are empty only because nothing triggers the step on that surface?
Next question: When a deliberation changes nothing (the first plan wins every probe), what does it cost, and is that rate low enough to justify the depth?
