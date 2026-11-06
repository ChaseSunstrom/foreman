# Brainstorm — lens: deepen: lean

- **Fold lean into one weighed footprint score** — FEATURE — value 4 — effort M — risk med — category: lean
  Why: the list holds ~30 separate lean ideas (BOM, trim, ceiling forecast, detach test, waiver) and T-2503 only has a "pending" row. One number per capability (context tokens injected, hook ms, ledger bytes, files in the user's repo) makes them combine instead of compete.
  Done when: `fm doctor` prints a footprint total with a per-capability breakdown, and adding a hook that injects 500 tokens raises the printed total by about 500.

- **Make every lean row expire into a decision** — FEATURE — value 4 — effort S — risk low — category: lean governance
  Why: T-2503 lets unmeasured growth wait as "pending"; with no deadline, pending is permanent and the rule becomes a loophole. Merges "deadline on pending rows" with "growth needs a waiver".
  Done when: a pending lean row older than N days turns red and files either a measurement task or a retire proposal, and a test with a faked clock shows it.

- **Retire by joint evidence, not one signal** — FEATURE — value 4 — effort M — risk med — category: retirement
  Why: usage census (`fm usage --prune`), the test catch record, the shell-equivalence audit and the cold-read tax each say "delete" alone. The user dropped T-2654 as already built, so the remaining gap is combining them. Output: one ranked "delete candidates" list with all four columns.
  Done when: `fm tidy` lists the top 10 candidates with usage, catch count, shell-equivalent and upkeep cost, and a verb scoring zero on all four ranks first.

- **Prove a deletion by running the suite with it removed** — FEATURE — value 4 — effort M — risk med — category: retirement
  Why: the "delete it and see" ideas lack a safe mechanism. Do it in a scratch worktree: remove the capability, run gates and the duel on a held-out set, and report what failed. Deletions then carry proof like additions do.
  Done when: `fm trim try VERB` leaves the real tree untouched and prints pass/fail of the gates with that verb removed.

- **Keep a tombstone-and-revival record for each retirement** — FEATURE — value 3 — effort S — risk low — category: lean
  Why: the user wants no idea killed for ambition (Genesis rule), so deletions must be reversible. Combines obituary, tombstone hit counts and revival tests: each retired verb leaves a three-line record, its hit count, and the one test that would revive it.
  Done when: retiring a verb writes the record, and a hit on its tombstone increments a counter that `fm doctor` shows.

- **Count only footprint-reducing subtractions in the exchange rate** — FIX — value 3 — effort S — risk low — category: measurement
  Why: a "subtraction" that moves code elsewhere would game lean (gen-0 metric-gaming concern). Compare the footprint score before and after the change.
  Done when: a task that deletes 100 lines and adds 120 elsewhere does not count as a subtraction in the Mission close line.

- **Rank context injection by whether it changed an outcome** — FEATURE — value 4 — effort L — risk med — category: lean context
  Why: the open question "which of Foreman's inputs are stale or self-authored" plus trim's usage counts. Pair each injected block with whether the session acted on it (a cited lesson, a followed Next:). Blocks never acted on are dropped from the default load.
  Done when: a report lists each injected block with injected and acted-on counts over 30 days, and a zero-acted block is flagged.

- **Lean twin that runs on the free arms** — FEATURE — value 3 — effort M — risk med — category: lean evidence
  Why: standing rules forbid session-arm exams until the end of the run, so the nightly twin (wild below) must use only the zero-token arms (finders, oracle) with half the verbs hidden.
  Done when: a twin run reports free-arm scores with and without the hidden verbs and names any capability whose score fell.

- **Wild: Hold a monthly "delete one thing" vote with the evidence attached** — FEATURE — value 3 — effort S — risk low — category: lean governance — wild
  Why: assumption: the user reads one concise prompt more reliably than a list. Foreman picks the top candidate from the joint ranking and files a pre-built deletion task; one yes merges it through `fm ship`.
  Done when: the first of each month a single deletion task exists with its evidence and a one-command accept.

- **Wild: Forecast the date the footprint hits a user-set ceiling** — FEATURE — value 3 — effort S — risk low — category: lean forecast — wild
  Why: assumption: a date lands harder than a count. A linear fit over the footprint history gives "ceiling in 41 days at the current rate", shown in `fm doctor` and the drive receipt.
  Done when: with 10 days of seeded history, the forecast matches the hand-computed date and an unset ceiling prints nothing.

- **Wild: Make Foreman uninstall itself in a sandbox every release** — FEATURE — value 3 — effort M — risk low — category: lean proof — wild
  Why: "prove the uninstall leaves nothing behind" is stated but never rehearsed. Run install → use → uninstall in a temp home, diff the file tree, and fail the release on any leftover. It extends `fm drill --restore` (T-2652).
  Done when: the drill reports zero leftover files after uninstall, and a planted stray file makes it fail.

- **Shed in a pre-registered order under quota pressure** — FEATURE — value 3 — effort M — risk med — category: lean quota
  Why: the standing rule says `--pace off` drops no work, but the quota ideas want a shedding order. Keep the rule: the order only applies when the user opts in, and every shed step is ledgered.
  Done when: with the opt-in set and a simulated 90% quota, the first shed step in the registered order fires and appears in the ledger; with it unset, nothing is dropped.

- **Wild: Publish the ledger formats as an open spec with a small reference reader** — FEATURE — value 2 — effort M — risk low — category: lean interop — wild
  Why: a spec with a roughly 300-line reader lets other tools consume Foreman's records, so Foreman needs fewer of its own readers. `fm drill` already proves readers survive missing classes, so the spec is testable.
  Done when: the reference reader passes `fm drill`'s fault set against a copied ledger, and removing one in-repo reader loses no output.

Next question: which of Foreman's own footprint measures (tokens injected, hook latency, bytes written, files touched) does the user actually feel, and so should be weighed most heavily?
Next question: when a capability is retired, who notices first, and how long does it take them to say so?
