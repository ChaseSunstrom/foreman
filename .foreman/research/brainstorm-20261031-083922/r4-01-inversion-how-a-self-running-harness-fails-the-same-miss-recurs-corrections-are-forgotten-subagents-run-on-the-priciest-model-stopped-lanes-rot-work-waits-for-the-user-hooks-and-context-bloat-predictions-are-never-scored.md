# Brainstorm — lens: inversion: how a self-running harness fails: the same miss recurs, corrections are forgotten, subagents run on the priciest model, stopped lanes rot, work waits for the user, hooks and context bloat, predictions are never scored

- **Check a self-filed task's premise before it is filed** — FIX — value 5 — effort M — risk low — category: self-repair
  Why: 3 of the 5 recent drops were self-filed tasks whose premise was wrong or already done (T-2269 plan-gate premise, T-2298 done inside another task, T-1208 already covered). The 4th was a baseline-red duplicate the dedupe missed.
  Done when: filing a task that cites a `file:line` or behavior that doesn't exist, or that matches a done task's diff, is refused with the evidence, and a test replays the 3 dropped cases.

- **Randomly withhold one injected block per session and compare outcomes** — PERFORMANCE — value 4 — effort M — risk low — category: context lean
  Why: the lean ratchet only caps growth. Nothing shows which always-on rules or lessons change the outcome.
  Done when: `fm doctor` lists each injected block with its with/without first-pass rate, and a block with no measurable effect after N sessions is proposed for deletion.

- **Lint stored lessons and steers for contradiction** — FIX — value 4 — effort M — risk low — category: memory
  Why: there are 20+ standing steers plus learned lessons, and "Detect a learned rule the user keeps correcting" is already listed. Two rules that conflict, such as "ship through fm ship" and "no new maintenance tasks", are never checked against each other.
  Done when: adding a steer that conflicts with an existing one prints both, with a one-line resolve command. A planted conflicting pair in tests is caught.

- **Carry the applicable steers into every lane brief and verify it** — FIX — value 4 — effort M — risk med — category: orchestration
  Why: the lane brief is a handoff, and standing rules live in a different place. Assumption: briefs drop steers such as the push grant, the cold-read rule and the testing cadence.
  Done when: `fm lane brief` ends with a "rules in force" list chosen by the task's scope, and a test fails when a steer whose scope matches is absent.

- **Never truncate a standing rule on any injected surface** — FIX — value 3 — effort S — risk low — category: memory
  Why: steers in the pack end mid-sentence ("Haiku scores never decide done, s…", "an exam fails a…"). A model reading the same cut text may act on half a rule.
  Done when: no steer is shortened in the session-start injection, the lane brief or the pack. If space is short, the output shows `[+N chars: fm decide show ID]` and a test asserts that marker.

- **Measure Foreman's own overhead per session** — PERFORMANCE — value 4 — effort M — risk low — category: lean
  Why: the ratchet counts characters and hook p50, not the tokens and minutes the harness itself spends on cold reads, briefs and checks per unit of user-visible work.
  Done when: `fm doctor` prints "overhead share" (harness tokens/minutes ÷ total) per week, and the ratchet warns when it rises more than 10% without a matching outcome gain.

- **Harvest a lane before it is reaped** — FEATURE — value 3 — effort S — risk low — category: lane recovery
  Why: stopped lanes rot, and reaping one discards its tests and notes. `fm lane rm` already has special handling for scratch folders.
  Done when: removing a stopped lane first writes a salvage note (commits, new tests, last error) and files one follow-up task if any of those exist.

- **Give each task waiting on the user a default and a deadline** — FEATURE — value 4 — effort M — risk med — category: user wait
  Why: "waits_on_user" tasks pile up, and the standing steer says to keep going on everything the wait doesn't block.
  Done when: each waiting task shows "default: X on DATE". Past the deadline, a lane runs the default and leaves it unmerged for the user's yes, and a test checks that the lane doesn't merge.

- **Give hooks one shared latency budget per event, with eviction** — PERFORMANCE — value 3 — effort M — risk med — category: hooks
  Why: hooks can only be added and the bench checks each one separately. Assumption: the cost adds up across hooks on the same event.
  Done when: `bench_hooks.py` fails if the summed p95 on one event exceeds its budget. The failure names the hook with the lowest hit rate as the eviction candidate.

- **Fail the docs when a verb or number they quote has drifted** — FIX — value 3 — effort S — risk low — category: docs
  Why: the user had to ask "make sure the website is updated, it doesn't look like it has been". T-2326 fixed the stats refresh, but prose claims in `MASTER.md`, the README and the site can still drift.
  Done when: `fm check` fails if a doc names an `fm` verb or flag that doesn't exist, or if a stat's stamp is older than its source.

- **Wild: Run both answers while a question waits** — FEATURE — value 4 — effort L — risk med — category: user wait
  Why: assumption: many `fm ask` questions are binary. Running both branches as unmerged lanes turns the user's yes into a pick instead of a start.
  Done when: for a yes/no ask, two lanes exist and the user's reply merges one and removes the other. A test uses stub lanes.

- **Wild: Keep a graveyard of dropped and reverted self-changes and consult it before proposing a similar one** — FEATURE — value 3 — effort M — risk low — category: self-repair
  Why: the drop reasons ("premise doesn't hold") are already written down and nothing reads them.
  Done when: a new self-filed task similar to a graveyard entry cites it, or is not filed.

- **Wild: Hold a monthly "autopsy of the harness" that picks the worst miss and rebuilds it as a scenario** — FEATURE — value 3 — effort M — risk low — category: self-repair
  Why: the lens says the same miss recurs. This turns the worst one into a permanent held-out exam scenario, written by a tool-less child that never sees Foreman's code (per the exam-scenario steer).
  Done when: each month adds one scenario to the exam set from a real recurrence, with its date and source task.

Next question: Which of Foreman's self-filed tasks in the last 30 days were dropped, and what single check at filing time would have caught each?
Next question: For each standing steer, is there a surface where it is silently absent (lane brief, pack, headless `fm run`, `fm code`)?
