# Brainstorm — lens: reliability

- **Identify processes by identity, not bare PID** — FIX — value 4 — effort M — risk low — category: liveness
  Why: round 1 had to fix `record_pid` surviving overlapping SessionStarts, and the mail monitor's wake path trusts a "fresh" heartbeat file. Both break when a PID is recycled or the clock jumps. Assumption: no pidfile currently stores a start-time or cmdline.
  Done when: a test that recycles a PID (a stale pidfile pointing at an unrelated live process) makes `fm bus --wake` fall back to tmux and `fm doctor` flag the pidfile as foreign. Heartbeat freshness uses a monotonic or boot-id-qualified stamp.

- **Isolate faults per record** — FIX — value 4 — effort M — risk low — category: state
  Why: Foreman keeps tasks, lessons, vetoes and ledger lines in many files, and every verb parses them. Assumption: one hand-edited or torn record can currently raise out of `fm next`, `fm task list` or a hook. The hook failure would then block all tool calls.
  Done when: a fixture with one malformed task file and one torn ledger line still lets `fm next`, the hooks and `fm task list` run. The bad record appears as a flagged "unreadable: path" row and `fm doctor` names it.

- **Detect double-registered or duplicate Foreman installs** — FIX — value 4 — effort S — risk low — category: wiring
  Why: the installer both clones to `~/.claude/foreman` and installs a plugin, and the wiring step edits `~/.claude`. Assumption: hooks can be registered twice, or two copies of `lib/` can resolve at once, so hooks double-fire or run mixed versions.
  Done when: `fm doctor` resolves every registered hook command to a real path and version. It fails if the same event has two Foreman entries, or if two distinct Foreman versions are reachable. A test fixture with a duplicate registration trips it.

- **Fail the suite on any write outside its sandbox** — CLEAN — value 4 — effort M — risk low — category: tests
  Why: round 2 found compact output ignoring `FOREMAN_STATE`, which is a write that escaped the configured state dir. 154 test files are a lot of places where that can recur unseen. Assumption: no tripwire exists today.
  Done when: the test runner installs `sys.addaudithook` on `open` and `os.rename`. Any write-mode open outside the per-test temp tree, including real `~/.claude` and the repo, fails the test with the offending path. A deliberately leaky fixture proves it fires.

- **Lint that all state paths come from one resolver** — CLEAN — value 3 — effort S — risk low — category: state
  Why: the `FOREMAN_STATE` miss in compact output is the evidence. Assumption: other modules compute `~/.claude/...` or `Path.home()` paths directly.
  Done when: a test walks every `plugin/lib/*.py` AST and fails on a literal home-dir path or `Path.home()` or `expanduser` outside the resolver module. The current violations are listed and fixed or allowlisted with a reason.

- **Make the mail watcher self-supervising** — FEATURE — value 4 — effort S — risk low — category: liveness
  Why: monitors start only in new sessions, so a watcher that crashes mid-session is silent until the next session, and "never idle" is lost with no sign. Assumption: `fm bus watch` has no in-process restart loop.
  Done when: killing the watcher's inner loop with an injected exception makes it log one line, back off, and resume. A line "foreman-mail restarted (n)" reaches the session, and after repeated crashes it exits non-zero with a reason.

- **Read multi-file state as one consistent snapshot** — FIX — value 3 — effort M — risk med — category: state
  Why: the statusline, hooks and `fm page` each read several state files, while writers update them one by one, so a reader can see a new step pointer with an old task. Assumption: no generation stamp or read-retry exists.
  Done when: a stress test with one writer cycling transitions and N readers never observes an inconsistent pair of values. Readers retry once on a changed generation counter, with no lock held.

- **Dry-run verify commands in the close-time environment at plan time** — FIX — value 3 — effort S — risk low — category: gates
  Why: round 1 refuses unrunnable verify commands at plan time, but a task's verify command later broke because it grepped the queue after the task left it. Assumption: plan-time and close-time environments differ, for example the lane worktree versus main and the scrubbed env.
  Done when: the plan-time runnability check executes under the same cwd and env scrubbing as the close gate. A verify command that works only from a lane checkout is refused at plan time with a message naming the difference.

- **Wild: Measure detection latency for injected silent faults** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: round 1 and 2 bugs (metric readers missing `✗ exit N`, an unarmed monitor) lived until the user or a review noticed. Assumption: nobody measures how long Foreman takes to notice its own silent failures. wild
  Done when: `fm doctor --drill` injects N named silent faults in a throwaway project (a reader mismatch, a dead heartbeat, a write error) and reports seconds until each is flagged. It exits non-zero if any is never detected or exceeds a set limit.

- **Wild: Report a self-caught rate for each round** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: the recursive-improve loop treats user complaints and Foreman's own reviews as the same stream. Assumption: tasks can be tagged by origin (user report, cross-task review, doctor probe) from the ledger. wild
  Done when: the round close prints "bugs found by Foreman: X of Y; found by you: Y−X", computed from task origins. A test with a fixture ledger checks the arithmetic.

- **Wild: Make every shipped feature declare its silent-failure signature** — FEATURE — value 4 — effort M — risk low — category: doctor
  Why: round 1's "known gaps" were prose, such as the monitor arming and compact output being off. Assumption: no machine-readable record says what "this feature quietly stopped working" looks like. wild
  Done when: each Claude Code integration carries a manifest entry with `fires_when`, `silent_if` and a probe command. `fm doctor` runs the probes and fails CI when a manifest entry has no probe or a probe cannot fail.

- **Wild: Add a poison-pill corpus mined from the user's real state** — FEATURE — value 3 — effort M — risk med — category: tests
  Why: real stored strings (for example `✗ exit N`) were wrong for readers that only synthetic data had passed. Assumption: real ledger and task files can be redacted into fixtures. wild
  Done when: a command exports a redacted, size-capped sample of real record shapes into a fixtures folder. A test replays every reader and writer verb over them, and any verb that raises or silently drops a record fails the suite.
