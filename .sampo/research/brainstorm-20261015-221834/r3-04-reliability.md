# Brainstorm — lens: reliability

- **Make the Stop hook idempotent under re-entry** — FIX — value 4 — effort S — risk low — category: hook safety
  Why: shot.py's interactive session was driven by the Stop hook into the queue, planning three tasks and stealing focus; the fence was added per-case, not as a rule. Assumption: a stop_hook_active-style guard isn't applied to every entry path.
  Done when: a test that fires Stop twice in a row, and once from a session marked as a harness, adds zero tasks and zero queue focus changes on the second and harness calls.

- **Pin every task to one owner session with an expiring lease** — FEATURE — value 4 — effort M — risk med — category: concurrency
  Why: worktree resume (T-1028) and the parallel builders both touch the same task and worktree; a resumed agent and a still-live original could both write. Assumption: no lease exists yet (the pack's earlier "single-owner lease" idea is only a proposal).
  Done when: starting a second builder on a leased task fails with a message naming the holder and its expiry, and an expired lease can be taken over by `fm resume`.

- **Write ledger appends with a torn-write check and self-heal on read** — FIX — value 4 — effort S — risk low — category: state integrity
  Why: a malformed ledger time already raised in gather() (T-1026); a kill mid-append can leave a half line that breaks other readers differently. Assumption: appends aren't length-prefixed or checksummed.
  Done when: a test truncates the ledger mid-line, and every reader (pane, history, next, tour) still loads, skips the line, and reports one "1 damaged line" note in `fm doctor`.

- **Run a startup crash-loop detector per hook** — FEATURE — value 3 — effort M — risk med — category: hook safety
  Why: in bypass mode a hook that throws on every call either blocks all work or silently stops guarding; today's ideas cover "fail closed" but not "stop thrashing". Assumption: hooks don't currently count their own consecutive failures.
  Done when: forcing a hook to raise 3 times in a row trips a visible degraded state (guard stays fail-closed, the recording-only hooks disable themselves), `fm doctor` names it, and one clean run clears it.

- **Make every test lock out the paid `claude` binary through one shared fixture** — FIX — value 5 — effort S — risk low — category: test isolation
  Why: T-0990's ~/.local/bin fallback let test runs reach the paid binary when a test replaced PATH; two tests faked "no claude" with PATH alone. Spot fixes aren't a guarantee.
  Done when: a suite-wide autouse fixture sets a resolver override, and a canary test that deliberately replaces PATH and calls the resolver proves no real binary path is returned.

- **Reconcile a stopped builder against git before offering resume** — FEATURE — value 5 — effort M — risk med — category: resume
  Why: the user asked for easy resume (T-1028). A worktree may have been pruned, rebased, or merged since the stop, so blind resume would continue on a dead or already-landed branch. Assumption: resume metadata is stored apart from git state.
  Done when: `fm resume` classifies each stopped builder as resumable, landed, diverged, or lost, and refuses to relaunch the last three with the reason and the repair command.

- **Detect Bash env-prelude growth and dedupe it at write time** — FIX — value 3 — effort S — risk low — category: idempotency
  Why: SessionStart appends exports on every start/compact, with 8x repeats seen. Assumption: the append has no marker block.
  Done when: running SessionStart ten times leaves exactly one Foreman export block in the env file, byte-identical after each run.

- **Give every child process a deadline and a process-group reaper** — FIX — value 4 — effort M — risk med — category: process control
  Why: capped `claude -p` children can leave partial results (T-0831) and orphans; fan-out brainstorms and reviews multiply the exposure. Assumption: not all spawn sites set a group and a timeout.
  Done when: killing the parent in a test leaves no child alive within 5 seconds, and a child past its deadline is killed with its partial output saved to a named file.

- **Wild: Run a nightly chaos soak that kills Foreman mid-task and demands a clean resume** — FEATURE — value 4 — effort L — risk med — category: chaos testing
  Why: wild; resume, leases and torn-write handling are only trustworthy if killed at random points, and the roundtrip gate runs only the happy path. Assumption: a fake-model mode exists for the e2e roundtrip.
  Done when: a scripted run SIGKILLs a fake-model task at 20 random points, and after each kill `fm resume` completes the task with a passing proof and no duplicate ledger entries.

- **Wild: Keep a "last known good" snapshot of state and roll back on a failed upgrade** — FEATURE — value 3 — effort M — risk low — category: upgrades
  Why: wild; releases (1.2.16, plugin updates) change state shapes, and the pack's migration ideas only move forward. Assumption: no pre-upgrade state copy is taken.
  Done when: after a simulated upgrade that corrupts a state file, `fm rollback` restores the previous version's state and `fm doctor` passes.

- **Wild: Add a dead-man's switch that parks the queue when the user's Stop-hook stream goes quiet or loops** — FEATURE — value 3 — effort M — risk med — category: runaway control
  Why: wild; unattended loops (super brainstorm, overnight work) can spin forever on a bad state, and the recursion governor idea covers brainstorm only. Assumption: no global cap on closes or spend per hour.
  Done when: a test driving a fake loop of 50 turns with no user input stops after the configured cap, writes a "parked" note with the reason, and resumes only on an explicit `fm unpark`.

- **Verify each hook's stdin schema against the installed Claude Code version at doctor time** — FIX — value 3 — effort S — risk low — category: compatibility
  Why: the PostToolUseValidate matcher test predated T-0972, and native-install paths changed under the tool; the harness changes under Foreman. Assumption: doctor doesn't replay a recorded payload per event.
  Done when: `fm doctor` feeds one recorded payload per hook event to the installed hooks and reports a mismatch by event name when a field is missing or renamed.
