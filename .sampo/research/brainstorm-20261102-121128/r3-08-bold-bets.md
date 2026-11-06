# Brainstorm — lens: bold bets

- **Run a cold-start apprentice that re-derives each closed task from its ask alone** — FEATURE — value 5 — effort L — risk med — category: verification
  Why: assumption: "proven" labels are authored by Foreman; the open question on reversed labels has no outside check. A sandboxed child sees only the original ask and the pre-task commit, builds its own fix, and the result is diffed against what landed, so disagreement is a signal Foreman didn't author.
  Done when: `fm audit rederive T-NNNN` prints the child's diff, whether the task's proof command passes on it, and a similarity score, for a closed task in a scratch worktree.

- **Add a spend-the-idle-budget planner that queues only measurement runs** — FEATURE — value 4 — effort M — risk low — category: budget
  Why: the request says usage is 0% and to go wild; deferred exams (end-of-run only per steers) and blind-language scenarios are waiting. Pack evidence: the steer "wait for --final or --regressing" means idle usage is wasted.
  Done when: `fm budget idle --plan` lists runs ranked by evidence-per-token, only from the steer-allowed set, and refuses any run a steer forbids, naming the steer.

- **Give every receipt a hatched third state with a reason code** — FEATURE — value 5 — effort M — risk low — category: receipts
  Why: earlier ideas repeat "unproven" and "override" but never specify the state machine. Assumption: today a check that couldn't run reads as absent, not as a state. Define proven / unproven(reason) / overridden(by whom), where only a re-run can move unproven to proven.
  Done when: a test that forces a headless UI check renders "unproven (no display)" in the receipt and `fm task finish` refuses to count it as a pass.

- **Make the steers a compiled policy with a conflict detector** — FEATURE — value 4 — effort M — risk med — category: governance
  Why: 30+ dated prose steers include supersessions (pause exams, then run at end; round-first holds). Prose contradiction is invisible; T-2583's own criterion contradicted its example.
  Done when: `fm decide --lint` reports every pair of active steers whose checks disagree on the same scenario, and a seeded contradiction is caught.

- **Wild: Dead-reckoning twin that predicts the next session's first hour** — FEATURE — value 3 — effort M — risk low — category: user model
  Why: wild; the sealed-prediction idea exists, but it predicts steers. This predicts concrete first actions (which task `fm next` will offer, which verb gets typed) from history, and scores itself each morning.
  Done when: the session-start note shows yesterday's prediction with a hit or miss, and a hit-rate over 14 days appears in `fm doctor`.

- **Wild: Adversarial twin agent that tries to get a false "done" past the finish gate** — SECURITY — value 5 — effort L — risk med — category: red team
  Why: wild; the guard and finish gates were only tested by Foreman's own tests. A tool-less-to-code child is given the task text and the gate's public rules, and rewards itself for passing a seeded broken change. Each success becomes a red-first test.
  Done when: a nightly run yields at least one recorded bypass attempt per gate, and every success files a task with a failing test.

- **Wild: Fossil mode: boot Foreman against a six-month-old ledger snapshot** — FIX — value 4 — effort M — risk low — category: compatibility
  Why: wild; answers the missing-record-class question from a different angle. Readers evolve faster than the ledgers, and 2,000+ tasks of history exist. Replay the oldest snapshot through today's readers and diff the answers.
  Done when: `fm doctor --fossil` loads a dated snapshot read-only and lists every verb whose output changed or errored, with a count.

- **Wild: Let Foreman bet its own budget on whether a deferred task is worth doing** — FEATURE — value 3 — effort M — risk low — category: prioritization
  Why: wild; 30+ "Later from" tasks sit deferred with no evidence rule. Each gets a stated bet (value, success chance) scored by the existing Brier machinery after a cheap spike, so the backlog sorts by calibrated expectation.
  Done when: `fm next --deferred` ranks deferred tasks by expected value with the bet shown, and settled spikes update the rank.

- **Cache hook verdicts per input hash to cut hook p95** — PERFORMANCE — value 3 — effort M — risk med — category: performance
  Why: the hook bench and the self-change gate are recurring concerns (T-2605, T-0832). Assumption: repeated identical read-only tool calls get recomputed. A content-addressed verdict cache, invalidated on rule change, skips them; the guard stays uncached.
  Done when: `bench_hooks.py` shows a lower median for a repeated-call workload with identical verdicts, and a rule edit invalidates the cache in a test.

- **Ship a single-file `fm doctor --explain` that turns each warning into one command** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: the thin area is developer experience and the pack shows many gauges (timers, bets, canaries, ratchet). Assumption: warnings name a problem but not the next keystroke.
  Done when: every WARN and FAIL line in a seeded broken home prints a copy-pasteable fix command or "needs you: <reason>".

- **Add a cross-harness conformance run that fills T-0335/36/37 with evidence** — FEATURE — value 3 — effort M — risk low — category: devices
  Why: three adapter tasks are blocked for live verification; the standing rule says Foreman isn't Claude-specific. A recorded-fixture harness replays canned Codex, Gemini and opencode hook payloads through the guard and drive, and prints a parity table.
  Done when: `fm agents conform` prints a per-harness table of guard, plan, prove and stop behaviours, with each cell passing, failing, or "needs live".

- **Wild: Hand the whole queue to a phone-sized "pocket foreman" read model** — FEATURE — value 3 — effort M — risk med — category: surfaces
  Why: wild; the web UI exists, and the pack names devices as thin. A static, signed, read-only snapshot (queue, receipts, unproven rows, blocked-on-you list) is served over the local network and works offline as a PWA.
  Done when: opening the snapshot URL on a second device shows the queue and unproven receipts with no server write path, verified by a test that POST returns 405.

Next question: Which Foreman verdict has the user never been able to check without Foreman's own tools, and what independent oracle could stand in for it?
Next question: If the user stopped steering for a month, which standing rules and ledgers would drift fastest, and what would signal it?
