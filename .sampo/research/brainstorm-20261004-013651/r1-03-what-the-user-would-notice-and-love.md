# Brainstorm — lens: what the user would notice and love

- **Detect and repair corrupt git objects in fm doctor** — FIX — value 4 — effort S — risk low — category: reliability
  Why: a crash left four zero-byte loose objects that broke `git diff`, and fm doctor passed. The user would notice a "healthy" report on a broken repo.
  Done when: with an empty file planted in `.git/objects`, `fm doctor` fails, names the file, and prints the exact quarantine command (it doesn't run it itself).

- **Give "waiting on background work" a first-class drive state** — FEATURE — value 5 — effort M — risk med — category: drive
  Why: 18 drive turns ended only to wait on a reviewer subagent. Each is a visible stall and a resume prompt. This is the most frequent friction. A drive that parks, shows "waiting on fm-reviewer, 2m", and resumes silently feels much smoother. Cut or merge the earlier "ghost task" idea, which was dropped.
  Done when: in a drive with a background reviewer, the log shows zero extra turn-ends for the wait, and the UI shows a "waiting on X" row with elapsed time.

- **Show why the guard blocked and offer a one-key precise allow** — FEATURE — value 5 — effort M — risk med — category: guard UX
  Why: false positives on `git stash list`, read-only python on state files, and python heredocs that edit plugin source. The user hits friction and can't see the rule. Print the rule id, the matched fragment, and a "grant this exact command once" line. Do not weaken the guard.
  Done when: a blocked `git stash list` prints its rule id and match. Granting it once lets that exact command pass and a similar write command stay blocked.

- **Fix the three known guard false positives with replay cases** — FIX — value 4 — effort S — risk med — category: guard
  Why: the friction list names the commands. Each becomes a `fm replay` case: allowed (`git stash list`, read-only state reads) and still-blocked (`git stash drop`, state writes).
  Done when: the replay corpus has these six cases and passes. The guard gate passes with the new rules.

- **Run flaky-test triage on gate failure** — FEATURE — value 3 — effort S — risk low — category: gates
  Why: one test class failed under load and passed on rerun. Gates should rerun only the failed tests once, mark the result "flaky-pass" in evidence, and count it. A silent retry hides signal.
  Done when: a test that fails once and then passes yields a gate pass flagged flaky, visible in `fm friction`. A test that fails twice fails the gate.

- **Add a "morning report" that opens each session** — FEATURE — value 5 — effort M — risk low — category: delight
  Why: the user is running long multi-pass loops and night-shift items. When they return, a one-screen summary helps: done, blocked, decisions awaiting them, spend vs caps, and the one thing needing a yes. Assumption: they come back to a cold terminal.
  Done when: `fm morning` (and a UI card at session start) lists the finished and blocked tasks and the pending yes/no items since the last visit, in under 25 lines.

- **Pre-flight a queue's cost and time before drive starts** — FEATURE — value 4 — effort M — risk low — category: budget
  Why: the user cares about savings that only prevent overuse, not capability. A forecast from the tier and past actuals ("this queue: ~$3.10, ~40 min, 2 reviewer passes") lets them say go. Past actuals exist in fmcost.
  Done when: `fm drive --estimate` prints a range per task and a total. After a run, the actual falls inside the range for most of the sampled queues.

- **Wild: Make a "why did this take so long" flame strip per task** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. A horizontal timeline in the UI shows each task split into think, edit, gate, wait on child, and review. The user's speed request gets a picture of where time goes and shows which batching idea helps.
  Done when: the UI shows a proportional strip for a finished task. Segment totals match the ledger's timestamps within 5%.

- **Wild: Have Foreman say what it would refuse to do before asked** — FEATURE — value 3 — effort M — risk med — category: trust
  Why: wild. At session start, show a short "I will not: push, publish, delete X without your yes" card, built from the guard categories and the user's saved vetoes. It makes the boundaries visible and it is the first thing a stranger-test session would find.
  Done when: `fm boundaries` lists each guard category with its current approval state and each active veto. The text is generated from the guard config, not hand-written.

- **Wild: Let the pane celebrate a clean first-time close** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. A task closed with all criteria green first time, no inconclusive runs, and a clean review gets a small, quiet marker plus a running streak. It shows which of the user's rules are working. It also gives the lesson-confidence idea a visible payoff.
  Done when: a first-time-clean close shows the marker in the UI. A task with any rerun or review fix does not.

- **Add a self-check that gates trust their own timeouts** — CLEAN — value 2 — effort S — risk low — category: reliability
  Why: assumption: with load-sensitive tests and the crash, a gate that hangs or is killed may be recorded as "no result" rather than a failure. Make that state loud.
  Done when: a gate killed by timeout records "timed-out", not pass. `fm next` asks to rerun it.
