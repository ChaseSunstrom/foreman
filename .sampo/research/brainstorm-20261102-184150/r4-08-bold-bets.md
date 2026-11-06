# Brainstorm — lens: bold bets

- **Run a pre-registered counterfactual Mission** — FEATURE — value 5 — effort L — risk med — category: exhaustive thinking
  Why: the pack's standing rules demand outcome-grounded weakness-finding, yet every Mission is judged only by its own filing. Assumption: a held-out twin run is affordable at zero tokens via the free arms.
  Done when: for one closed Mission, `fm genesis twin` re-plans from the same request with the filed briefs hidden and prints the briefs only one side produced, with counts.

- **Make dissents stakeable and cashable** — FEATURE — value 4 — effort M — risk low — category: dissent scoring
  Why: the carried gap is "dissents scored against outcomes". Each dissent records a predicted outcome and a 14-day horizon; `fm outcomes` settles it from the close-survival data it already has.
  Done when: a dissent filed with a prediction is settled at day 14 and appears in `fm outcomes --predictions` as right or wrong, with a test using a fixture ledger.

- **Compile the Exam into an executable capsule** — FEATURE — value 5 — effort M — risk med — category: exam
  Why: the carried gap is that every brief's Exam names an outcome measure and a live-state reading. The earlier question "which Exams are re-runnable cold?" shows this isn't checked. A capsule is a script plus a pinned expected shape, runnable with `python3 -I` and no session state.
  Done when: `fm exam brief T-id` runs the capsule in a scratch home and prints one typed line (`pass|fail|unreadable`, reason), and a brief without a capsule is refused at filing.

- **Reject measures that the builder's own work satisfies** — SECURITY — value 4 — effort M — risk med — category: gaming
  Why: the standing steer says weakness-finding must use signals Foreman didn't author. Run each Exam on the parent commit and with the fix mutated; a measure that reads the same in both is vacuous.
  Done when: a planted vacuous Exam (counting the brief's own files) is refused at filing with the reason, and a real one passes.

- **Print "Left out" with a receipt on every request** — FEATURE — value 4 — effort S — risk low — category: exhaustive thinking
  Why: the request is "say what it left out". Assumption: the model can't prove "nothing" without a list. Output is parsed from a required last line in each lens child's output and joined with the canary hits.
  Done when: every Mission page ends with a `Left out:` block holding a count and at least one cell or "0 (grid of N cells checked)", and `fm genesis check` fails when it is missing.

- **Put a canary positive control beside every "not built"** — FIX — value 4 — effort S — risk low — category: canaries
  Why: the carried gap is canaries near the idea. A search that finds nothing proves nothing unless the same search finds a known thing, and "dropped" items show "already built" misses.
  Done when: each "not built" claim prints three nearest hits plus one control query that must hit, and a test with a broken grep shows the claim refused.

- **Settle left-out cells against the user's later asks** — FEATURE — value 4 — effort M — risk low — category: feedback loop
  Why: the pack's "what earlier brainstorms missed" list shows eight asks no idea predicted. Matching each later ask to a prior left-out cell gives exhaustiveness a score.
  Done when: `fm outcomes` shows "left-out hit rate: k of n" for the last generation, derived from the task ledger by text and file overlap.

- **Wild: Run a saboteur that tries to pass the Exam without work** — FEATURE — value 4 — effort L — risk med — category: adversary
  Why: wild. Gaming is the standing worry; a cold child with only the Exam and the repo tries the cheapest way to make it read green, and each success is a bug in the Exam, filed as a task.
  Done when: for one Mission, the saboteur's attempts are recorded and at least one Exam is tightened or confirmed unbreakable, with the transcript kept.

- **Wild: Seal tomorrow's left-out forecast** — FEATURE — value 3 — effort M — risk low — category: prediction
  Why: wild. Each Mission seals a hash of its predicted "things the user will ask about next" and settles it against the next three typed asks, so exhaustiveness earns a hit rate instead of a claim.
  Done when: the sealed file exists before the next ask and `fm outcomes` reports hits and misses against it.

- **Wild: Reconstruct the request from the Exams alone** — FEATURE — value 3 — effort M — risk low — category: coverage
  Why: wild. A tool-less child reads only the filed Exams and writes what the request must have been; the diff from the real request lists the clauses no Exam checks.
  Done when: the run prints the clause list with unchecked clauses marked and a test shows a planted dropped clause being found.

- **Mark an unreadable reading as "unmeasured", never pass** — FIX — value 4 — effort S — risk low — category: exam
  Why: an earlier question asks what to do when a snapshot can't be taken. A third state with a reason and a carried-forward deadline avoids silent passes.
  Done when: a reading that times out or hits a missing service is stored as `unmeasured` with a reason and blocks "done" only after its deadline.

- **Bind each reading to its checkout and environment** — FIX — value 3 — effort S — risk low — category: provenance
  Why: warm and cold readings can differ by state dir, uid, home or host, and a mismatch makes an Exam read different in the user's shell than in the builder's.
  Done when: every stored reading carries a provenance line and `fm exam brief` flags a mismatch between filing and close.

- **Rank left-out cells by what a mistake would cost** — FEATURE — value 3 — effort M — risk low — category: triage
  Why: assumption: a flat left-out list gets ignored; ordering by past drops, blast radius and the user's earlier corrections lets the top three be read at a glance.
  Done when: the Left out block lists at most five cells, each with a one-line cost reason, with the remainder behind a count.

Next question: what does the user do the first time they open a Mission page, and does anything on it let them tell "covered" from "unvisited" within ten seconds?
Next question: which of the carried gaps would still matter if every Exam had to run in a no-network, no-write capsule?
