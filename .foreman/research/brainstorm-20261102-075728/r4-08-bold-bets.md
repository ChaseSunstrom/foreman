# Brainstorm — lens: bold bets

- **Spend a done-error budget** — FEATURE — value 5 — effort M — risk low — category: done-detection
  Why: gen-2 review #1 found false dones on the long-horizon tier, and the pack lists calibrating the done-detector against reopens. Treat reopens like an SRE error budget: each row reopened after "done" burns budget.
  Done when: a fixture goal with 3 reopened rows flips `fm goal` to verify-only mode, prints "error budget spent" as the stop reason, and a test pins both.

- **Make probe authorship a separate duty** — SECURITY — value 5 — effort M — risk med — category: anti-gaming
  Why: the standing rules distrust signals Foreman authored, and the pack has "blind child writes the test" only as a wild idea. Make it the default: a row's verify command counts as proof only if a tool-less child that saw only the row text wrote it. Builder-written probes carry weight 0.
  Done when: closing a row whose probe the same lane wrote refuses with "unseparated proof", and a blind-authored probe is accepted.

- **Cassette every lane's model I/O** — FEATURE — value 4 — effort L — risk med — category: crash recovery
  Why: T-0831 (salvage capped `claude -p` children) is deferred, and the request stresses carrying a plan across crashes. Record each lane's prompts and responses by content hash. A killed lane resumes without re-paying, and a cheaper model can be swapped in and its diff compared.
  Done when: killing a fixture lane at step 3 of 5 and resuming makes zero repeat model calls for steps 1-3, and the cassette replay yields a byte-identical tree.

- **Land every row behind a dark-launch flag** — FEATURE — value 4 — effort M — risk med — category: integration
  Why: assumption: multi-day goals accumulate long-lived unmerged branches, while `fm ship` already gates pushes to main. Each row merges behind a flag that flips only when its probe passes, so main always holds the unfinished goal and any stopping day is shippable.
  Done when: a two-row fixture goal ships row 1 with row 2 absent and its flag off, and `fm goal` lists the flag state per row.

- **Ship a migration goal kit with a parity oracle** — FEATURE — value 4 — effort L — risk med — category: goal kits
  Why: assumption: "port X to Y" is a common vague goal where done means behaviour parity. The kit records the old system's inputs and outputs, then replays them against the new one. The plan is strangler-style slices, and the oracle is the parity rate.
  Done when: a fixture two-implementation project reaches done only when 100% of the recorded cases match, and one planted divergence blocks it.

- **Ship a metric-gated goal kit for ML and data work** — FEATURE — value 3 — effort M — risk low — category: goal kits
  Why: assumption: "make the classifier good" has no pass/fail test. The kit defines done as a held-out metric threshold over N seeds, with the seeds and data hash pinned so resume can't quietly change the result.
  Done when: a toy training goal closes only when the median of 5 seeds clears the threshold, and a changed data hash invalidates the earlier proof.

- **Score oracle escapes per finished goal** — FEATURE — value 4 — effort M — risk low — category: done-detection
  Why: the finish oracle is only trusted if bugs found after done are rare. Count post-finish failures (CI red, issues, fixes touching closed rows) as escapes. Each escape becomes a permanent probe, and the rate shows beside "done".
  Done when: a fixture bug fix in a closed goal's files adds one probe row and raises the goal's escape count to 1.

- **Make the plan a repo of NOT_BUILT stubs** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: assumption: a prose plan drifts from the repo across days and compactions. Scaffold the finished surface (commands, routes, modules) with every stub exiting `NOT_BUILT: row-id`. Progress is the stub count, and resume needs no memory because the repo is the plan.
  Done when: a three-command fixture goal shows 3 stubs, the count drops to 2 after one row closes, and a stub with no row id fails lint.

- **Wild: pay row bounties against public probes** — FEATURE — wild — value 3 — effort L — risk med — category: collaboration
  Why: the pack mentions GitHub Projects sync. Take it further: publish each row's blind-authored probe as a contract, and any PR that passes it and the ship gate closes the row. Humans and other agents become builders under the same oracle.
  Done when: a fixture PR passing row 3's probe auto-closes it with the PR cited as evidence, and a PR that edits the probe is rejected.

- **Wild: auto-publish a per-goal devlog page** — FEATURE — wild — value 3 — effort M — risk low — category: delight
  Why: the Genesis site already auto-publishes tower data from the ledger. Do the same per goal as a shareable static page of closed rows, proof receipts, scope changes and stop reasons, ready for the user to show others.
  Done when: closing a row regenerates a static page that renders offline, lists the row with its proof line, and contains no absolute home path.

- **Wild: let estimate accuracy gate unattended length** — FEATURE — wild — value 4 — effort M — risk med — category: autonomy
  Why: the pack has bets and Brier scores but nothing tying them to autonomy. Foreman prices each row in minutes and tokens before building. A rolling accuracy score sets how long an unattended shift may run without a check-in, so trust is earned from the ledger.
  Done when: a fixture with 5 badly missed estimates cuts the allowed shift length, `fm doctor` prints the score and its denominator, and the cut is reversible by 5 good ones.

- **Wild: run a "no-Foreman" completion drill** — CLEAN — wild — value 3 — effort M — risk low — category: portability
  Why: the standing rule says Foreman isn't specific to Claude Code. A weekly canary hands a finished goal's repo and plan to a plain session with no Foreman installed and asks it to continue one row. The repo should be enough on its own.
  Done when: the drill ends with pass or fail in `fm doctor`, and a fixture whose plan lives only in hidden state fails it.

Next question: Which of these closed goals' rows were reopened by the user, not by a probe, and what did their first words about the problem sound like?
Next question: What does the user do in the first five minutes after a goal says "done", and could that action itself be the oracle?
