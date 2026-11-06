# Brainstorm — lens: reliability

- **Expire edit leases with their run** — FIX — value 5 — effort S — risk low — category: concurrency
  Why: a run's edit leases outlive it, so the next run on the same code is refused for 20 minutes (pack: "fm code: a model run's edit leases outlive it").
  Done when: a test kills a worker mid-run, starts a new run on the same code within the window, and the run is accepted with the old leases gone from the lease table.

- **Make `fm quiet` fail loudly on piped stdin** — FIX — value 4 — effort S — risk low — category: silent failure
  Why: a heredoc fed to `fm quiet` does nothing and reports exit 0 (pack: "fm quiet runs its command with no stdin").
  Done when: `fm quiet <<EOF ... EOF` either consumes the input or exits non-zero with a message naming the dropped stdin.

- **Restore the test_followups parser for split plugin/lib rows** — FIX — value 5 — effort S — risk low — category: test robustness
  Why: test_followups reads the T-1713 row, which was split into a module list, and throws IndexError on main (pack).
  Done when: test_followups passes on main, and a new case feeds it a multi-module row and gets the full list back.

- **Give the gate lock a bounded, visible wait for `--affected`** — PERFORMANCE — value 4 — effort M — risk med — category: concurrency
  Why: `fm check --affected` and `--evidence` runs queue behind every other builder's run on the machine-wide lock (pack). Full checks already wait at most 15 minutes.
  Done when: two affected runs in different projects both finish, and any wait over 60 seconds prints the holder's project and PID.

- **Judge the hook bench by median and load, not one p95** — FIX — value 3 — effort S — risk low — category: flaky benchmarks
  Why: PreToolUse:Bash:script p95 hit about 310 ms once, then ran at 272 ms on a quiet machine (pack). Assumption: the 300 ms gate fails on noise.
  Done when: the bench records load per core with each run, and fails only when the median exceeds budget in three consecutive runs.

- **Write state files atomically, with fsync and rename** — FIX — value 4 — effort S — risk low — category: crash safety
  Why: task and journal state lives on disk and must survive `/compact` and crashes (pack). Assumption: writes are not yet atomic.
  Done when: a test kills the writer partway through a state save, and the next read gets the previous complete state, never a truncated file.

- **Turn stalled runs into a timed, journaled recovery** — FEATURE — value 4 — effort M — risk med — category: stall recovery
  Why: the TUI shows a stalled card with manual wait, kill and switch keys (pack). Stalls need a person to notice them.
  Done when: a run with no events past the threshold is marked stalled in the journal, its reason recorded, and it is restarted or killed by policy with no key press.

- **Make the rules-file budget a doctor failure that names what to cut** — CLEAN — value 3 — effort S — risk low — category: budget
  Why: the rules file went over the 6,400-character budget at 6,416 (pack).
  Done when: `fm doctor` fails at over-budget and lists the three largest sections by size.

- **Fuzz the guard hook so it always fails closed** — SECURITY — value 4 — effort M — risk low — category: fail-closed guard
  Why: the guard is a fail-closed hook for bypass mode (pack). Assumption: parser edge cases are untested.
  Done when: 10,000 generated shell lines never crash the hook, and every unparseable line returns deny.

- **Replay a run from its journal to reproduce it** — FEATURE — value 4 — effort L — risk med — category: debugging
  Why: `fm code why` already explains a run from its journal (pack). Replay would turn that explanation into a reproduction.
  Done when: `fm replay <id>` on a fixture reproduces the same event sequence and outcome.

- **Let a supervisor agent repair stalled gates from their journals** — FEATURE — value 3 — effort L — risk high — category: self-healing (wild)
  Why: wild. Stalls, lock holders and stale leases already show up in the journal, so a supervisor could read them and pick a fix, checked by a gate before it acts.
  Done when: given a fixture of a stalled gate, the supervisor names the cause and applies only the fix the gate verifies.

- **Checkpoint every tool call into an undo ledger** — FEATURE — value 4 — effort L — risk med — category: undo (wild)
  Why: wild. Rewinds already reopen steps whose files were reverted (pack). A ledger would make any step revertible in one command, without git.
  Done when: after ten tool calls, one undo restores the files byte-for-byte to the state before the last call.

- **Run the demo as a nightly canary on a seeded repo** — CLEAN — value 3 — effort M — risk low — category: release safety (wild)
  Why: wild. `fm demo` already runs the real hook and `fm` in a throwaway repo with no model calls (pack), so it could run on a schedule and catch regressions before users do.
  Done when: a scheduled job fails and reports when the demo's expected output changes, and passes on an unchanged build.
