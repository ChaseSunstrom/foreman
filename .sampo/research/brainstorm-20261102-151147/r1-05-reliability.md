# Brainstorm — lens: reliability

- **Test the guard's degraded states, not only its rules** — FIX — value 5 — effort M — risk low — category: guard reliability
  Why: Left open in the pack: what each unattended path does when the guard's rules file, grant store or last-good copy is missing, truncated or unreadable. T-2668 covered hang latency but not missing or corrupt state.
  Done when: a test deletes, truncates and chmods each of the three files and asserts a stated verdict (deny or last-good) for the hook, the drive and a lane. Each case writes one ledger record naming the degraded file.

- **Write hook stdout once, as a single JSON document** — FIX — value 4 — effort S — risk low — category: hooks
  Why: assumption: the host ignores a malformed hook reply, so a stray print, warning or partial write could turn a deny into an allow. Nothing in the pack proves stdout is exactly one document.
  Done when: a test injects a stray stdout write into each hook. The hook still emits one valid JSON object with its original decision, and the stray text goes to stderr.

- **Count unrecognised transcript record types in every reader** — FIX — value 4 — effort S — risk low — category: observability
  Why: T-2667 found `fm burden` silently missing `hook_success` stdout because `fmcost.INJECTS` didn't know that record type. Other readers likely have the same blind spot.
  Done when: `fm doctor` lists record types seen in recent transcripts that no reader handles. A planted new type appears in that list.

- **Price unknown model IDs at the highest known rate** — FIX — value 4 — effort S — risk low — category: spend safety
  Why: `--stall-usd` (T-2669) and the budget cap depend on a price table. A model ID missing from it could read as $0 and the cap would never fire. The environment already lists new IDs such as claude-fable-5-1.
  Done when: a run with an unlisted model ID is priced at the maximum known rate and prints one warning. A test with a fake ID hits the stall cap.

- **Surface a sub-agent's allowlist block as its own outcome** — FEATURE — value 4 — effort M — risk low — category: agents
  Why: Left open in the pack: what a sub-agent does when its allowlist blocks the only way to finish. assumption: today this shows up as a generic failed task.
  Done when: a child that hits a tool block ends with `blocked: needs <tool>`. The line appears in `fm next` and the receipt, and the task is not marked failed.

- **Reset the stall clock only on closes that landed something** — FIX — value 3 — effort S — risk low — category: spend safety
  Why: `--stall-usd` counts dollars since the last task close. A loop closing trivial or Foreman-filed churn tasks keeps resetting it. "A run that keeps closing tasks is never stopped" is exactly that loophole.
  Done when: a fixture run closing five no-diff tasks while spending still trips the stall. A run landing real diffs does not.

- **Refuse to start a task whose p90 cost would breach a cap** — FEATURE — value 3 — effort M — risk low — category: spend safety
  Why: assumption: `--stall-usd` and the budget cap only act between tasks, so a single task can overshoot. The receipt could report the overshoot.
  Done when: a replay with a stored task-cost history declines a task whose p90 cost exceeds the remaining cap. The receipt says why and lists the overshoot.

- **Test complexity growth, not just a fixed bar** — PERFORMANCE — value 3 — effort M — risk low — category: robustness
  Why: T-2668 timed ten pathological guard commands against a fixed bar. Other parsers (transcript, `fm map`, task text) have no such test, and a fixed bar misses a quadratic that is still fast at the test size.
  Done when: a shared helper runs each registered parser at n and 4n, and fails if the time ratio exceeds 8. A planted O(n²) parser fails it.

- **Name the hung test when the ship gate times out** — FIX — value 3 — effort S — risk low — category: gate
  Why: assumption: the suite is large (419 test files) and a hang today gives only a timeout.
  Done when: the gate prints the test name and a stack dump on timeout. A planted `sleep` test is named in the output.

- **Tally retries, fallbacks and hedges in the drive receipt** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: Left open in the pack: which agent behaviours change spend or outcomes without the user seeing until the receipt.
  Done when: the receipt shows counts and dollars for retried, fell-back and skipped steps. A fake host that fails twice shows "2 retries, $X".

- **Fall back to the previous install generation on a hook import failure (wild)** — FIX — value 3 — effort M — risk med — category: self-repair
  Why: assumption: a broken self-change that fails at import would disable every hook until someone notices. A shim could try the previous generation and record that it did.
  Done when: planting a syntax error in the current copy leaves hooks working through the previous copy. One ledger record and one `fm doctor` line name the fallback.

- **Replay a museum of tasks that once hung or crashed the drive (wild)** — FEATURE — value 3 — effort M — risk low — category: regression
  Why: assumption: crash-loop quarantine (T-0798) handles repeats, but nothing keeps the poison tasks as fixtures. Each past hang or crash would become a replayable test.
  Done when: each recorded poison task replays against the current drive with a fake agent and finishes or quarantines within a bound.

- **Run a diagnosability exam: a cold child names a planted fault from `fm` output alone (wild)** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: Reliability includes "can anyone tell what broke". This scores that, with a tool-less child that never sees the code.
  Done when: `fm exam` plants 8 faults and reports how many a child names correctly using only `fm doctor` and `fm status` text.

Next question: Which Foreman gauges or decisions would silently read healthy if the host CLI changed a record or reply shape, and how soon would anyone notice?
Next question: What is the cost of Foreman's own failures to the user, in minutes per week, and which three causes dominate?
