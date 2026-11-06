# Brainstorm — lens: reliability

- **Prove the mail monitor armed with a first-turn echo receipt** — FIX — value 5 — effort M — risk low — category: liveness
  Why: the pack says monitor arming in a live interactive session is "unverified", and `fm bus --wake` now skips tmux whenever a heartbeat is fresh. A heartbeat from a monitor that never attached would therefore swallow wakes.
  Done when: a test with a stub `claude` shows `fm bus send` to a session whose monitor is not armed falling back to tmux. `fm doctor --live` reports "armed" only after a monitor-delivered message was echoed back in that session.

- **Require a delivery ack on every monitor wake, or escalate** — FIX — value 5 — effort M — risk med — category: liveness
  Why: assumption: a monitor that crashes mid-session leaves a heartbeat that stays "fresh" for its whole TTL. Every wake in that window is dropped silently, which is the idle-while-queued failure the monitor was built to remove.
  Done when: killing the monitor process mid-session, then sending mail, results in the tmux fallback firing within N seconds. The ledger records the missed ack.

- **Fail loudly and minimally-safe when `python3` is missing or too old** — SECURITY — value 5 — effort S — risk low — category: hooks
  Why: install requires Python ≥3.12.7, hooks are Python, and bypass mode is the default. A broken `python3` after an OS upgrade means every hook errors and the guard silently fails open. Assumption: Claude Code treats a hook that cannot execute as non-blocking.
  Done when: with `python3` shadowed by a stub that exits 127, a `/bin/sh` shim blocks `rm -rf ~` in bypass mode and prints one visible "Foreman hooks down: python3" line.

- **Make compact output provably lossless for failures** — FIX — value 4 — effort M — risk med — category: tokens
  Why: compact output rewrites Bash results over 6,000 chars to head + failure lines + tail, and it is off until the user says yes. A missed failure line is a hidden false pass. Failure-format drift has already bitten (`✗ exit N` vs `exit N`).
  Done when: a replay over stored `state/outputs` pairs asserts every line matching any known runner failure pattern survives compaction. Any output where the extractor finds zero failure lines but the exit code was non-zero is passed through uncompacted.

- **Keep compact-output pointers alive as long as anything can cite them** — FIX — value 4 — effort S — risk low — category: tokens
  Why: `fm tidy` prunes compact-output full texts older than 7 days. A resumed session or a ledger entry can still say "full text in <file>" for a file that no longer exists.
  Done when: tidy skips outputs referenced by any open task or live session transcript. Reading a pruned pointer prints "pruned, re-run: <command>" instead of an error.

- **Lint verify commands for self-expiring premises** — FIX — value 4 — effort S — risk low — category: verification
  Why: a dropped task's check grepped the queue for T-0775, which left the queue once done, so the check was recreated. Plan-time refusal of unrunnable commands exists but does not catch checks whose truth decays.
  Done when: `fm task plan` warns on verify commands that grep queue/task ids, hard-coded dates, `/tmp` paths or PIDs. A fixture with the T-0775 pattern is flagged.

- **Hand back a typed partial result when a child hits `--max-budget-usd`** — FIX — value 4 — effort M — risk med — category: headless children
  Why: round 1 added hard budgets to `claude -p` children. Assumption: a budget cut-off mid-answer currently looks like an empty or truncated reply and gets parsed as a finished brainstorm or review.
  Done when: a stubbed child that exits on budget yields `status: budget_exhausted` plus whatever text arrived. Callers record it as incomplete, never as "no findings".

- **Journal the lane merge so a crash cannot lose the pre-merge start point** — FIX — value 3 — effort S — risk low — category: lanes
  Why: lane-merged tasks now keep their pre-merge start point, but assumption: it is written after the merge. A crash between the two reverts to the empty-diff close check that was just fixed.
  Done when: killing the process between merge and record, then running `fm task finish`, still sees the full diff. The start point is written first and cleaned up on success.

- **Re-verify "done" in a clean checkout of the staged diff** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: evidence is only as good as the tree it ran on. A pass that depends on untracked or stale files (pycache, state/outputs) looks green and ships red. Lane merges already produced one false-empty-diff case.
  Done when: `fm task finish --clean` runs the criteria in a throwaway `git worktree` of exactly the diff. A fixture whose test passes only with an untracked helper file fails.

- **Shed optional hooks under load** — PERFORMANCE — value 3 — effort S — risk med — category: hook latency
  Why: bench was changed to judge by CPU time under load, which shows load distorts hook latency. Assumption: parallel lanes plus gates push hooks past their budget, making the session feel stuck.
  Done when: above a configured loadavg, non-gating hooks (recording, title, hints) exit immediately and write one "shed" count. Gating hooks never shed. A test covers both.

- **Wild: stamp every state write with its writer** — FEATURE — value 3 — effort S — risk low — category: state
  Why: wild. When a state file turns up corrupt or odd, such as a step pointer jumping or a record missing a field, nobody can say which command did it. Assumption: many writers (hooks, `fm`, lanes, monitor) share central state.
  Done when: each write appends `{pid, argv, hook_event, session}` to a ring log. `fm why-state <file>` names the last three writers.

- **Wild: run a disk-full and read-only-home drill in `fm doctor --drill`** — FEATURE — value 3 — effort M — risk low — category: resilience
  Why: wild. Atomic-write work does not show what happens at ENOSPC or with a read-only `~/.claude`. Assumption: hooks currently swallow the write error and report success.
  Done when: in a tmpfs sized to fill mid-run, `fm task finish` refuses to claim "done" and prints "state not saved: disk full". Hooks stay quiet and allow normal work.

- **Wild: a feature kill-switch that auto-trips on repeated silent failures** — FEATURE — value 4 — effort M — risk med — category: self-protection
  Why: wild. Round 1 added many opt-in or unverified mechanisms (monitor, compact output, sessionTitle, outward-tool guard). A feature that fails three times in a row should disable itself, say so once, and file a task, rather than keep failing in the background.
  Done when: injecting three consecutive failures into compact output flips it to off. `fm doctor` shows "auto-disabled: <reason>", and a captured task exists.
