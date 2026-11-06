# Brainstorm — lens: unspoken needs

- **Confirm a red CI alarm against the newest run before it pages** — FIX — value 5 — effort S — risk low — category: alerts
  Why: T-1810's first sweep reported "CI red on main" from a cancelled run (be5743a6, cut off by the macOS job's 35-minute limit). The user had to chase a false alarm.
  Done when: a fixture where the newest run is cancelled and the previous run is green emits no red-CI alarm, and a test asserts it.

- **Re-plan the remaining steps from each step's measured result** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: the user steered twice mid-run. The finished profile (124 s CPU) reshaped step 2 into a budget, and the watchdog step was dropped once the existing USAGE_LIMIT wait was found. Assumption: the user expects each step's output to change the next step.
  Done when: after a step closes with a different result, the next step's text in the plan changes, shown by a test with two different first-step outputs.

- **Show before and after cost for every change that touches spend** — FEATURE — value 4 — effort S — risk low — category: cost measurement
  Why: the user asked to "first measure T-1796 with fm cost" before judging it, and asked for the cost math to be redone when the model changed.
  Done when: a task that edits a cost-affecting file closes with a before and after `fm cost` line in its receipt.

- **Wake a deferred item when its trigger fires** — FEATURE — value 4 — effort M — risk low — category: scheduling
  Why: items such as T-0788 through T-0799 and T-1266 sit deferred with no wake condition. The user's `defer --until reset` habit shows they expect the item to return without being asked again.
  Done when: a deferred item with trigger "claude-code-version-change" re-enters the queue in a test that changes the recorded Claude Code version.

- **Close the loop on every brainstormed idea's fate** — CLEAN — value 3 — effort S — risk low — category: ideas ledger
  Why: the ideas-so-far list holds hundreds of entries with no shipped, dropped or open state, so each round can re-propose work that is already done.
  Done when: every idea in the next round's pack carries one of shipped, dropped or open, and a test over the ledger confirms no shipped idea is offered again.

- **Mirror the user's own vocabulary in receipts** — FEATURE — value 3 — effort S — risk low — category: receipts
  Why: wild. The user says "dropped", "steered", "pushed back", "full force". When receipts use Foreman's terms, the user has to translate them back.
  Done when: a receipt for a task whose request uses "steered" reuses that exact word in its summary line, checked by a fixture test.

- **Pace spend to the hours the user actually types** — PERFORMANCE — value 3 — effort M — risk med — category: scheduling
  Why: wild. Assumption: the user works in bursts after the weekly reset, so queued runs are most useful when they finish just before the next session.
  Done when: replaying a log of request timestamps, a queue with a time-of-day window starts before the first request of the next burst.

- **Keep a worry list of the three riskiest queued items** — FEATURE — value 3 — effort S — risk low — category: risk triage
  Why: wild. The user asks what went wrong only after a run. A short list ranked by past failure odds from the journal would show the risk before the queue starts.
  Done when: `fm status` prints three queued items with a failure-odds figure drawn from the journal, and a fixture confirms the ordering.

- **Show what the user's recent messages already decided in each new pack** — FEATURE — value 3 — effort S — risk low — category: intent memory
  Why: the user's messages restate earlier choices ("don't ask me for anything", "step 1 is the profile"), and new tasks often start without them.
  Done when: the pack for a new task has an "already decided" section quoting the last three user decisions with their message ids, verified in a pack-builder test.

- **Warn when the installed fm lags the repo the user last approved** — CLEAN — value 3 — effort S — risk low — category: install health
  Why: the user asked why `fm` was not recognized. A terminal opened before the symlink was created kept an old copy, and nothing flagged the mismatch.
  Done when: `fm doctor` prints a one-line warning when the installed binary's commit differs from the approved commit, and a test covers both states.
