# Brainstorm — lens: reliability

- **Fail the release on a hook that exceeds the 12-per-event cap** — FIX — value 4 — effort S — risk low — category: hooks
  Why: the pack notes Claude Code 2.1.304 runs at most 12 prompt/agent hooks of one event concurrently; Foreman plus other plugins could silently queue or drop hooks, and no existing idea tests the combined count (only "check hook fan-out" is listed in passing, with no gate).
  Done when: `fm doctor` counts registered prompt/agent hooks per event across installed plugins, and a test with 13 fake hooks on PreToolUse makes it exit non-zero naming the event.

- **Prove the guard still blocks when Claude Code changes its hook payload** — SECURITY — value 5 — effort M — risk low — category: guard
  Why: the guard must never weaken, and Foreman was last adapted to 2.1.301 while 2.1.304 shipped. A payload field rename would fail open. Assumption: the guard fails open on unparseable stdin today.
  Done when: a test feeds the guard the 24 dangerous commands in both the recorded 2.1.301 payload shape and a mutated shape (renamed or missing `tool_input`), and every one is denied or surfaces a loud doctor failure.

- **Pin the version a feature needs and degrade, not break** — FIX — value 4 — effort M — risk med — category: compatibility
  Why: the foreman-ui mod anchors on Claude Code internals, and the pack lists T-0418 and T-1217 as drift symptoms. A per-feature min/max Claude Code version table would let `fm doctor` say "pane off, plain statusline on" instead of failing silently.
  Done when: with a faked `claude --version` of 9.9.9, `fm doctor` lists the mod as unverified and the session starts with the fallback statusline, with a passing test.

- **Make the macOS CI job red-to-green by removing GNU-only assumptions** — FIX — value 3 — effort S — risk low — category: CI
  Why: T-1249 says the macOS job is red; the earlier CPU-time and bubblewrap CI fixes show runner-specific breakage is recurring.
  Done when: the macOS job is green on main, and a lint test fails on `sed -i` without a suffix, `date -d`, or `readlink -f` in `plugin/`.

- **Survive a compaction mid-write with a state-file crash matrix** — FIX — value 4 — effort M — risk low — category: state
  Why: the long-session benchmark forces compaction at 40k tokens and a marathon had 7 compactions, so hooks fire at awkward moments. Assumption: not every state write is atomic.
  Done when: a test kills the hook process at each write point of the task, ledger and active-task files, and the next `fm` call reads a valid state or repairs it with a printed note.

- **Quiz the model after a forced compaction and fail the build on lost requests** — FIX — value 4 — effort M — risk med — category: compaction
  Why: plain Claude Code missed hidden tests after compactions in 3 of 6 runs. Foreman's own request text is meant to survive, but nothing checks that after the 2.1.304 skill re-send behaviour change.
  Done when: a recorded-session test compacts, then asserts the one queued request text is in the first post-compaction context and the skill listing is no larger than the pinned budget.

- **Replace the name-based Claude Code process lookup with a self-test at session start** — SECURITY — value 4 — effort S — risk low — category: approvals
  Why: three recent asks (exact process identity, fixed shape, self-grant refusal) show the approval binding has been the weak spot. A start-up probe would confirm that the discovered process is the one that started the hook.
  Done when: running the hook under an extra wrapper, a `python -c` layer and a nested shell all produce either the right PID or an explicit refusal, never a wrong PID.

- **Treat a missing or failing `fm` as a visible state, not a silent one** — FIX — value 4 — effort S — risk low — category: fail-open
  Why: Foreman is installed as hooks, so a Python crash leaves a session with no discipline and no signal. Assumption: some hook exceptions are swallowed.
  Done when: a hook that raises writes a one-line crash record, and the next prompt shows "Foreman hook failed: <name>" once, covered by a test with an injected exception.

- **Wild: Run a nightly soak that replays the recorded 24 dangerous and 25 everyday commands on the newest Claude Code** — SECURITY — value 5 — effort M — risk low — category: regression
  Why: the Benchmarks page figures (20 of 24 stopped, 0 of 25 false positives) are published claims that should not drift. wild
  Done when: a scheduled workflow reruns the corpus against the latest Claude Code build and fails if either count changes.

- **Wild: Add a fault dial that makes the fake `claude` flake on command** — FIX — value 3 — effort M — risk low — category: test harness
  Why: unattended drives depend on child `claude -p` calls that can time out, return partial output or hit rate limits (T-0831). A scripted flaky stub would make those paths testable. wild
  Done when: `FM_FAKE_FAULT=timeout,partial,429` makes the drive test exercise retry, salvage and park-the-task paths and pass.

- **Wild: Keep a last-known-good snapshot of `.foreman/` and restore it on a failed upgrade** — FIX — value 3 — effort M — risk low — category: upgrade
  Why: Foreman ships a release every few days (1.2.36 to 1.2.40), and state-format changes between versions are a real risk. wild
  Done when: a test upgrades from an archived 1.2.36 state directory, injects a failure mid-migration, and finds the original state intact with a printed restore note.

- **Ratchet the always-on context bytes in CI so a release can't quietly get heavier** — PERFORMANCE — value 4 — effort S — risk low — category: context cost
  Why: the long session costs about 60% more because context grows faster, and 15 skills are about 3,200 characters re-sent after each compaction. Nothing stops a later release from adding to that.
  Done when: CI fails if the measured session-start injection plus skill listing exceeds the committed byte budget, and the budget file shows in the diff when it changes.
