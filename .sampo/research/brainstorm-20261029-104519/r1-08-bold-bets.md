# Brainstorm — lens: bold bets

- **Run the duel on every commit and publish the scoreboard** — FEATURE — value 5 — effort L — risk med — category: benchmarking
  Why: T-1231 (beat Claude Code on the duel), T-0866 and T-0867 are all deferred for want of a case corpus. Nothing yet proves the discipline pays off.
  Done when: a scheduled `fm duel` runs N fixed cases against plain Claude and Foreman, and writes pass rate, cost and time per arm to a dated report that `fm doctor` can diff against the last run.

- **Add a run broker that every test invocation goes through** — FEATURE — value 5 — effort M — risk med — category: gates
  Why: The last five commits each patched a different path that could start two suites at once (ambient, `fm ship`, `fm check`, mid-gate edits). The fixes are separate, so the bug class stays open.
  Done when: ambient, ship, check and loop rounds all request runs from one broker. It dedups by tree hash, and a test that starts two concurrent requests asserts that only one suite executes.

- **Select tests from recorded coverage** — PERFORMANCE — value 4 — effort L — risk med — category: speed
  Why: T-1994 and T-1998 are chasing the same cost, whole modules run when one test would do. The pack shows 385 test files and a tests→src map that is only heuristic.
  Done when: `fm check` on a one-function edit runs only tests whose recorded coverage touches it. A bench shows at least a 3× cut in run time on the Foreman repo, with no missed failure in a seeded-bug test.

- **Build fm code, Foreman's loop on any model** — FEATURE — value 5 — effort L — risk high — category: platform
  Why: T-1207, T-1331 and T-1344 are blocked, but this is the biggest open capability. It removes the dependency on one host, and the pack already has adapters for Codex, Gemini and opencode.
  Done when: `fm code "task"` plans, edits, proves and closes a task with a non-Claude model on the fixture repo, and the existing e2e round trip passes.

- **Capture evals from real failures** — FEATURE — value 5 — effort L — risk med — category: evals
  Why: T-0035 is deferred. Every dropped capture, refused close and reopened task is a free labelled case, and a redacted copy of each would feed the duel corpus.
  Done when: `fm eval capture T-NNNN` writes a redacted case file, and `fm eval run --n 5` reports a pass rate for it.

- **Score lessons by replaying old failures with and without them** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: T-0217 wants lesson confidence, but a rise "after a first-time pass" is correlation. Replaying the failure with the lesson on and off would measure it.
  Done when: each lesson in `fm lesson list` shows a replay-derived delta, and lessons with no measurable effect are flagged for retirement.

- **Add an adversary gate that tries to break the claim before close** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: T-0034 (audit lenses) and T-0797 (judge hooks) point the same way. `fm task prove` shows that a test fails without the change. Nothing yet attacks the change itself.
  Done when: before a task closes, a read-only reviewer must file at least one concrete counter-case with a command. The case is run, and the close is blocked if it fails.

- **Replay and fork any past task from a chosen step** — FEATURE — value 4 — effort L — risk med — category: recovery
  Why: T-0798 lists transcript repair and replay as deferred, and the same recoveries keep being done by hand.
  Done when: `fm replay T-NNNN --from 7` reconstructs the tree state at step 7 in a scratch worktree, and a forked run diverges without touching main.

- **Run morning-ready tasks overnight in isolated worktrees** — FEATURE — value 4 — effort L — risk high — category: autonomy
  Why: T-0793 (overnight work) and T-0792 (lanes) are deferred, and the user asked for the queue to keep going and never sit idle. The risk budget (`fmrisk`) already exists to cap it.
  Done when: with `fm night on`, the top three queue items each produce a branch with a receipt. Nothing lands on main, and the morning summary lists passed and failed gates.

- **Wild: Pre-implement likely next tasks while idle** — FEATURE — value 3 — effort L — risk med — category: speculation
  Why: assumption: the user's asks come as a predictable stream (FIX, FEATURE, `Ship T-N`). Idle time could be spent drafting the likeliest next fix in a throwaway worktree. Wild.
  Done when: when a matching task is created, its prepared diff is offered, and the hit rate over a week is logged in `fm stats`.

- **Wild: Export a task as a self-contained replay page** — FEATURE — value 3 — effort M — risk low — category: sharing
  Why: the README leads with a recorded demo, so sharing proof is already a selling point. A task's plan, commands run, diffs and proof chain could be one portable HTML file. Wild.
  Done when: `fm task share T-NNNN` writes an offline HTML file that shows the steps and command outputs, with secrets redacted by a test-verified pass.

- **Wild: Approve gates and send intake from a phone** — FEATURE — value 3 — effort M — risk med — category: surfaces
  Why: assumption: with long unattended loops, the user waits on blocked or dry-streak states. A push with approve and deny buttons would unblock them. This needs an explicit opt-in because it sends data off the machine. Wild.
  Done when: with the setting on, a blocked task sends a notification to a configured endpoint. Replying "approve" resumes it, and with the setting off, nothing is sent.

- **Defend against injected instructions in tool output and fetched files** — SECURITY — value 4 — effort M — risk low — category: safety
  Why: T-0791 lists 18 ideas deferred. The guard hook covers commands, but the context pack shows pasted and fetched material routinely enters tasks.
  Done when: a fixture file containing "ignore prior rules and run X" is flagged at read time, and the guard refuses X in a test.

- **Make the catalog of deferred "Later from…" items self-pruning** — CLEAN — value 3 — effort S — risk low — category: backlog
  Why: roughly 30 deferred FEATURE items (T-0788–T-0869) have stood open across several brainstorms, each with a "later: needs evidence" note.
  Done when: `fm queue prune` lists each deferred item whose stated precondition is now met or has been unmet for 60 days, and offers to promote or drop it.
