# Brainstorm — lens: deepen: orchestration

- **Run a lane flight recorder with replay** — FEATURE — value 5 — effort M — risk low — category: orchestration
  Why: T-0798 (replay, blackstart) is deferred and the lane autopsy idea only writes after a stop. Combine autopsy, state-hash progress and the argv proof into one append-only per-lane log (brief hash, model, argv, state hashes, tool outcomes). `fm lane replay ID` re-runs the brief on a cheaper tier against the recorded inputs and diffs the result.
  Done when: killing a lane mid-run leaves a log from which `fm lane replay` reproduces the brief and argv byte for byte, and a test asserts it.

- **Close the router loop with a per-tier pass ledger** — FEATURE — value 5 — effort M — risk med — category: orchestration
  Why: T-2291 picks a model from history, and "probe one tier down on a sample" plus "cheapest tier that passed" both need the same data. Keep one ledger of (task tier, type, model, outcome after merge) and let the router spend ~10% of lanes on a downward probe. Promote the probe when it passes N times, demote on a re-fix or revert.
  Done when: a fixture history of 20 lanes makes `fm lane brief` choose the cheaper model for a class, and a single red-after-merge demotes it on the next brief.

- **Forecast conflicts, then partition lanes to avoid them** — FEATURE — value 4 — effort M — risk low — category: orchestration
  Why: the T-2208 conflict-brief test shows conflicts are common. Combine the forecast with the blast-radius co-change data from T-2291's era (`fm graph blast`). Before spawning, group tasks into conflict-free batches and serialize the overlapping ones, naming the shared file.
  Done when: two tasks with overlapping scope paths are never spawned in the same batch, and the refusal names the shared path.

- **Make the merge train bisect automatically** — FEATURE — value 4 — effort M — risk med — category: orchestration
  Why: steer "merge in mission order" plus "bisect when the result goes red". A train lands lanes one at a time on a scratch branch, runs the gate after each and ejects the culprit lane back to its builder with the failing output as the brief.
  Done when: with 3 lanes where the second breaks a test, the first and third merge and the second returns to its builder with the test output attached.

- **Treat steers as a lane-brief contract that is machine-checked** — SECURITY — value 5 — effort S — risk low — category: orchestration
  Why: the pack holds about 25 standing steers, and "carry steers into every lane brief" is only a hope. A brief linter checks the applicable steer ids are present, and a post-run check confirms the lane's diff doesn't violate the ones that have an automatic check (T-2327 style).
  Done when: a brief missing an applicable steer is refused at spawn, and a lane whose diff breaks a checked steer fails its merge gate.

- **Add a stop-reason classifier that drives recovery** — FEATURE — value 4 — effort M — risk low — category: orchestration
  Why: the pack wants to "recover stopped ones" (Mission 8, #9) and steer 3 says to wait out usage limits. Classify limit, crash, stuck loop, context blowup or guard denial from the transcript tail, then resume, shrink the brief, switch the model, or ask once with `fm ask`.
  Done when: five recorded stop transcripts each map to the expected recovery action in a table test.

- **Give lanes a shared blackboard with budgets** — FEATURE — value 3 — effort M — risk med — category: orchestration
  Why: lanes currently only meet at merge. A small file-backed board (facts found, files claimed, questions) lets a scout lane's findings be read by builders and keeps two lanes from researching the same thing. The USD budget is per lane, and the board tracks the spend.
  Done when: a second lane's brief includes the first lane's posted finding without re-running the search, and a lane over budget is paused, not killed.

- **Score the orchestrator's briefs by landing rate** — FEATURE — value 3 — effort S — risk low — category: orchestration
  Why: "shrink lane briefs to the smallest that still lands" needs a measure. Record brief size against first-pass landing and re-fixes (T-2290 already scores predictions), then have `fm lane brief` trim sections whose removal never changed the outcome.
  Done when: `fm lane stats` prints brief-size buckets with landing rates, and a trim rule fires on a fixture.

- **Wild: Run a night shift with a morning handover** — FEATURE — value 5 — effort L — risk med — category: orchestration
  Why: wild; combines Mission 8's self-triggering with lanes. Triggers queue the night's tasks, the router sets the tiers, the train merges what passes, and a single page ranks what's green, what stopped and why, and the one yes it needs.
  Done when: a fixture night run of 4 queued tasks ends with a handover file listing each lane's outcome and a single pending decision.

- **Wild: Run a stub-model day with a deliberately dumb driver** — FEATURE — value 3 — effort M — risk low — category: orchestration
  Why: wild; extends the idea already listed. A weak driver in a sandbox shows which Foreman gates catch a bad lane and which ones only work because the model is strong. Each hole becomes a task.
  Done when: a report lists the gates the stub got through and files at least one task per hole.

- **Wild: Hold a lane auction between model tiers** — FEATURE — value 3 — effort L — risk high — category: orchestration
  Why: wild; for tasks with an Approach naming alternatives (T-2269-style stuck ladder), spawn the cheap and the strong tier on the same step and let the first one to pass its verify command win. The loser is cancelled, and the cost and the winner feed the router.
  Done when: a fixture task with two lanes cancels the slower one after the first verified pass and records both costs.

- **Wild: Give lanes a peer review swap** — FEATURE — value 3 — effort M — risk med — category: orchestration
  Why: wild; answers the question about a model on both sides with no check between them. A lane's diff is reviewed cold by a different model's lane that never saw the builder's reasoning, and only its quoted-clause failures (the T-2246 rule) block the merge.
  Done when: a seeded violation in a builder's diff is caught by the reviewer lane and blocks the merge, and a reviewer FAIL with no quoted clause only warns.

- **Prove the whole lane chain with one canary task** — CLEAN — value 4 — effort S — risk low — category: orchestration
  Why: several ideas rest on "does the router's pick reach argv" and "does the brief reach the child". A daily canary task with a no-op change runs spawn, brief, check, merge and cleanup, and fails loudly where the chain breaks. It also covers T-2289's scratch-folder cleanup.
  Done when: `fm doctor` reports the canary's last pass time, and breaking the argv pass-through turns it red.

Next question: Which lane failures are caused by the brief, not the model, and does the pack record enough to tell them apart?
Next question: When two lanes both succeed but their merged result is wrong, what does Foreman check, and who is told?
