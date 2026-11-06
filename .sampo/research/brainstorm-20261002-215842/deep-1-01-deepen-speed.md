# Brainstorm — lens: deepen: speed

- **Build a content-addressed gate cache with affected-test selection** — FEATURE — value 5 — effort M — risk med — category: speed
  Why: gates are 18.8 of 125 hours, and one project's `cargo test` takes a median 8 min about once per task. Combine the tree-hash cache and diff-affected tests into one key: (tree hash of the gate's inputs, gate command, toolchain version). A hit costs 0 s. A miss runs only the tests the diff reaches, via a per-language import or crate dependency map. A full run is forced at queue end and whenever the selector is unsure.
  Done when: running `fm gate` twice on an unchanged tree makes the second run return in under 1 s with "cached", and a one-file edit runs fewer tests than the full suite.

- **Run gates in a background worktree while the next step starts** — FEATURE — value 5 — effort L — risk high — category: pipelining
  Why: close-out and gates dominate wall time, and the work is serial. Snapshot the tree, run gates in a throwaway `git worktree`, and begin planning the next task meanwhile. A failure posts a toast and pulls the session back to the failed task before anything else is marked done. "Done" stays refused until the gate result is recorded.
  Done when: in a two-task queue, task 2's planning starts before task 1's gate finishes, and an induced gate failure blocks task 1's close and reopens it.

- **Score each gate by cost per catch and skip the low scorers** — FEATURE — value 4 — effort M — risk med — category: gate policy
  Why: the 287 task events already record gate runs, durations and outcomes. Compute minutes spent per real failure caught for each gate in each project. Gates that have never failed in N runs drop to run-at-queue-end only. A per-project profile stores this and can be overridden.
  Done when: `fm gates --cost` lists each gate's runs, failures caught and minutes per catch, and a gate with 0 catches in 30 runs is deferred automatically with a visible note.

- **Make planning ceremony size-proportional by default** — CLEAN — value 5 — effort M — risk med — category: ceremony
  Why: planning has the highest call count (task_set 1290 events), the median is 18 bookkeeping calls per task, and the user complains about hours. Tiny tasks take one `fm task quick` call that captures, plans and records in a single step. Ceremony escalates with size or when the touched files include protected core. The user's "make done the default" idea becomes the rule, and ceremony becomes opt-in by size.
  Done when: a one-file change completes with at most 3 fm calls, and a protected-core edit still triggers the full flow.

- **Batch fm calls into one transactional `fm do` call** — PERFORMANCE — value 4 — effort M — risk low — category: call count
  Why: 18 calls per task is 18 Python startups plus 18 model round-trips. Accept a JSON or heredoc list of ops (`task_set`, step update, evidence, note) applied atomically, with a single combined result. The model round-trips are the real cost, so fewer tool turns matters more than the hook milliseconds.
  Done when: a task's plan, steps and criteria are recorded in 1 call and the event log is identical to the multi-call version.

- **Show a live time ledger per task in the band** — FEATURE — value 3 — effort S — risk low — category: visibility
  Why: the user said "it takes hours" but can't see where. A band row shows wall time split into model, gates, hooks and waiting on the user, with the biggest slice highlighted. This also feeds the cost-per-catch scores.
  Done when: the band shows the split for the current task and it sums to within 5% of wall time.

- **Add a flaky and slow-test quarantine that learns** — FEATURE — value 3 — effort M — risk med — category: gate policy
  Why: assumption: with 8-minute suites, some tests are the slow or flaky tail. Track per-test duration and flip history from gate output. Report the top offenders and propose splitting them out or running them at queue end only.
  Done when: `fm gates --slow` lists the 10 slowest tests per project, and a test that flips pass/fail across identical tree hashes is flagged.

- **Wild: Offer an 80% exit ramp at task midpoint** — FEATURE — value 4 — effort M — risk med — category: scope
  Why: wild, extends the user's own idea. When the criteria that matter are met and the remainder is polish, a toast offers "ship now, capture the rest as a follow-up task". The follow-up goes into the inbox, so nothing is lost.
  Done when: with 3 of 4 criteria evidenced, the band offers a one-press close that creates a follow-up for the unmet one.

- **Wild: Speculatively pre-plan the whole queue overnight in cheap Haiku passes** — FEATURE — value 4 — effort L — risk med — category: pipelining
  Why: wild. Planning is the largest call count and the queue is known ahead. fm-scout drafts plans, file lists and probable gates for the next N tasks while idle or during a long gate. The real planner then only edits the draft. Drafts are invalidated when files they touched change.
  Done when: starting a queued task finds a draft plan, and the plan stage takes at most 1 call.

- **Wild: Keep a warm gate daemon that holds the build state** — PERFORMANCE — value 4 — effort L — risk high — category: build speed
  Why: wild. Much of an 8-minute `cargo test` is rebuild and cold start. A per-project daemon holds the incremental build dir, a shared target dir across worktrees and a watcher, so gates start already compiled. It cuts the hook cost too, since classic hooks could talk to the daemon rather than spawning Python.
  Done when: a gate run after a small edit starts executing tests within 5 s, and hook latency through the daemon is under 5 ms.

- **Wild: Predict gate failure before running it** — FEATURE — value 3 — effort L — risk med — category: prediction
  Why: wild. Train a tiny model on past diffs and outcomes, so a risky diff runs the gate first and gets fast feedback, while a diff like prior green ones defers it to queue end. The user is usage-sensitive, so it needs no LLM calls.
  Done when: on held-out history, the predictor ranks the gate-failing tasks in its top quartile at least 70% of the time.
