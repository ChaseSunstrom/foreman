# Brainstorm — lens: reasoning ahead

- **Group blocked items by the one action that frees them** — FEATURE — value 4 — effort S — risk low — category: blocked pile
  Why: T-0335 and T-0336 both wait on real codex, gemini and opencode installs, and T-0418 and T-0325 each name a single install step. The pile reads as ten separate waits when it is about three actions.
  Done when: `fm status` prints one line per unblock action with the count of items it frees, and a fixture with two items sharing a reason shows them under one line.

- **Pre-flight a request's checks against the current tree before filing** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: the journal shows requests re-filed after the work already landed, such as "Push foreman/build to main" redone at a new sha and "Cut usage burn" recreated. Assumption: many of these re-filings describe a state that already passes.
  Done when: filing a request whose acceptance check already passes prints "already passing at <sha>" and does not queue a task.

- **Serialize queued tasks by symbol, not by file** — FEATURE — value 4 — effort M — risk med — category: queue overlap
  Why: file-level overlap is flagged, but `plugin/lib` is large and tasks that touch different functions in one file are needlessly serialized. Assumption: most edits in those files are function-scoped.
  Done when: two tasks editing different functions in one fixture file run in parallel, and two tasks editing the same function are serialized, both verified in a test.

- **Refuse a queue that cannot finish before the next usage reset** — FEATURE — value 4 — effort M — risk low — category: usage budget
  Why: the weekly reset is the forcing deadline, and today a queue planned past it is only deferred, which hides the cost. The user has asked for both the reset and burn control.
  Done when: `fm queue` run with a two-hour window and ten tasks lists the cut set, names the tasks cut, and shows the total it would spend.

- **Name what the proof did not cover, on the same receipt line** — FEATURE — value 3 — effort S — risk low — category: close receipts
  Why: T-1807 showed a crash-hygiene test passing only because its fake git was broken, so "green" overstated coverage. A receipt that says only "passed" invites the same mistake.
  Done when: a fix whose proof ran only affected tests prints "not run: full suite" on the same line as "passed".

- **Reserve recovery budget in each lane before the next task starts** — FEATURE — value 3 — effort M — risk med — category: recovery budget
  Why: assumption: a crashed run currently draws its resume cost from the next queued task's budget, so one crash shifts cost onto unrelated work.
  Done when: a run killed mid-task resumes from its journal with a reserved amount, and the next queued task's budget in the journal is unchanged.

- **Write a degraded plan per task for a mid-run model downgrade** — FEATURE — value 3 — effort M — risk med — category: model resilience
  Why: the governor already moves builders to Sonnet. Assumption: a downgrade in the middle of a queue restarts the task rather than continuing it.
  Done when: forcing the governor to a cheaper model mid-run keeps the same plan file and the task finishes with no restart event in the journal.

- **Start the longest CI job first when runners are scarce** — PERFORMANCE — value 3 — effort S — risk low — category: CI latency
  Why: the 35-minute experimental macOS job cancelled main's test run (T-1809), and a short job that queues behind it waits for the same slot.
  Done when: a replay of the recorded job durations shows main's run finishing before the 20-minute job cap, and no main run is cancelled in that replay.

- **Let a queued item argue its own case a week later** — FEATURE — value 3 — effort S — risk low — category: queue judgement — wild
  Why: wild. The queue has many items with no review of whether the user would still want them.
  Done when: a queue where one item is marked "rejected in a week" shows the reason at queue time and does not start that item.

- **Hold a cold-start drill each morning** — PERFORMANCE — value 2 — effort S — risk low — category: startup cost — wild
  Why: wild. Hook and startup cost was the whole profile cost in the last round, and no check measures time-to-first-useful-step from a cold cache.
  Done when: the drill clears the caches, runs bare `fm`, and records the time to first useful output in the journal.

- **Leave the next risk in every commit body** — FEATURE — value 2 — effort M — risk low — category: handoff — wild
  Why: wild. A commit records what changed but not what the author expected to break next, so the next run starts blind.
  Done when: a closed task's commit body contains a "next risk" line, and the next run on that file reads it into its pack.
