# Brainstorm — lens: reliability

- **Recognise Claude Code's blocking dialogs in the pane and clear them** — FEATURE — value 5 — effort M — risk med — category: liveness
  Why: the user said "make sure it doesn't sit idle like it is", and `fm bus` already drives sessions through tmux. Unattended sessions can stall on dialogs no hook sees: folder or MCP trust prompts, expired login, a rate-limit wait screen, plan mode, update or feedback prompts. Assumption: these dialogs are what the user is seeing.
  Done when: golden pane captures of each dialog, one set per tested Claude Code version, are classified correctly by a test, and an `fm doctor` canary shows the watcher clearing or escalating each one.

- **Detect a tool call that never returned** — FIX — value 4 — effort M — risk low — category: liveness
  Why: assumption: a Bash call stuck on an interactive prompt (git credentials, npm, a pager) looks like idleness to every hook. The transcript shows a `tool_use` with no `tool_result` for N minutes, and `fm` can read that without any hook firing.
  Done when: a fixture that hangs on stdin is flagged within the threshold, interrupted, and recorded as "hung tool" rather than a test failure.

- **Write a result sidecar for every gate run** — FIX — value 4 — effort M — risk low — category: evidence
  Why: T-0749, T-0750 and T-0754 were all misreads of terminal text (`✗ exit N` vs `exit N`). A runner that writes `{exit, signal, timed_out, truncated, duration}` to a file would end this class of bug. It would also separate "killed by the tool timeout" from "the test failed", which today pollutes catch rates.
  Done when: a gate killed by the timeout is recorded as `timed_out`, not as a failure, and catch-rate code reads only the sidecar.

- **Check the pane before typing into it** — FIX — value 4 — effort S — risk low — category: safety
  Why: `fm bus` uses `send-keys`. If Claude Code has exited, the pane is a shell, and the wake text executes as commands. If the user is mid-draft, it mangles their input.
  Done when: sending to a pane whose foreground process isn't `claude`, or whose input line is non-empty, is refused and deferred, and a test covers both cases.

- **Keep a schedule registry with fire receipts** — FEATURE — value 4 — effort M — risk low — category: scheduling
  Why: assumption: session crons and wakeups die with their session and fail silently. Foreman would record every CronCreate, ScheduleWakeup and RemoteTrigger it arms, re-arm them at SessionStart, and flag a missed fire.
  Done when: a session killed after arming a wakeup is re-armed on the next start, and a fire that never arrived appears in `fm doctor` as missed.

- **Reject hollow subagent returns at SubagentStop** — FEATURE — value 4 — effort S — risk low — category: delegation
  Why: SubagentStop is already hooked. A child that returns empty, is cut off at max turns, or reports files that don't exist is currently indistinguishable from success.
  Done when: a stub child that returns nothing or names a missing path is re-dispatched once with a narrower brief, and the failure is logged.

- **Cap Stop-hook continuations and change tactics** — FIX — value 3 — effort S — risk low — category: liveness
  Why: the drive keeps going by blocking Stop. Assumption: nothing bounds repeated blocks that produce no progress, which burns tokens in a loop.
  Done when: N consecutive Stop blocks with no new ledger event switch to a different move (re-plan, ask, or park) instead of repeating, and a test shows the switch.

- **Track permission mode and plan mode every turn** — FEATURE — value 3 — effort S — risk low — category: mode drift
  Why: Foreman assumes bypass mode. Assumption: a mid-session switch (shift-tab, plan mode, or a managed-settings override) changes which prompts appear and could stall an unattended run.
  Done when: a mode change is recorded as an event, the drive adapts (no pushing in plan mode), and a test simulates the change.

- **Mirror the step pointer into the native todo list** — FEATURE — value 3 — effort S — risk med — category: drift
  Why: T-0759 reports that steps start without the pointer moving. Assumption: Claude Code has a native todo or task-list tool that survives compaction. Foreman would write its current step there and flag any disagreement between the two.
  Done when: after `/compact`, the model's todo view matches `fm` STATE, and a mismatch raises a visible drift event.

- **Stop child sessions from re-entering Foreman's hooks** — FIX — value 3 — effort S — risk low — category: recursion
  Why: Foreman launches `claude -p` children for ideas and second-session work. Assumption: they inherit the hooks, which can pollute state or recurse.
  Done when: every launcher sets a role env flag, hooks short-circuit on it, and a test asserts no child writes to the parent's STATE.

- **Reconcile after suspend or clock jumps** — FIX — value 3 — effort S — risk low — category: time
  Why: assumption: laptop sleep skews leases, budget timers, wakeups and the prompt-cache assumptions that depend on wall time. Foreman would detect the gap and re-validate lanes and schedules.
  Done when: a simulated 2-hour clock jump re-checks every lease and in-flight lane and logs the reconciliation.

- **Wild: Repair a half-written transcript so `--resume` works** — FIX — value 3 — effort M — risk med — category: recovery — wild
  Why: assumption: a session killed mid-write can leave a truncated last line or a `tool_use` with no result, and resume then fails or confuses the model. A repair step would truncate to the last valid record and close dangling calls.
  Done when: a deliberately corrupted transcript fixture resumes at the exact step after `fm repair`.

- **Wild: Keep a ring buffer of pane frames as a stall flight recorder** — FEATURE — value 3 — effort S — risk low — category: observability — wild
  Why: when a stall happens, hook logs say nothing about what the terminal showed. Capturing the pane every few seconds into a small ring would let `fm incident` attach the last 30 frames.
  Done when: an induced stall produces an incident bundle containing the preceding frames, with secrets redacted.

- **Wild: Add an offline mode for API outages** — FEATURE — value 3 — effort M — risk med — category: resilience — wild
  Why: usage-limit failover exists, but nothing covers a Claude outage or 529 storm. Foreman could keep doing the non-model work (gates, map refresh, queue grooming, state repair), park the steps that need a model, and resume them when the API returns.
  Done when: with the API stubbed to fail, `fm` runs the queued non-model chores, parks the rest with a reason, and picks them up after the stub recovers.
