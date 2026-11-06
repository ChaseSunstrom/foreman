# Brainstorm — lens: reliability

Answers to earlier questions through the reliability lens:
- **Gauge nobody could falsify:** the "done" verdict itself. Outside check: a nightly re-run of each closed goal's oracle in a clean clone.
- **Self-started action fails during the install-free period:** the user should see it first in a file, `fm doctor` and the next session's first card. Injected text alone can be lost to compaction.
- **Fake-clock week vs. the real timer:** trust the real timer. Record the disagreement in the tick ledger as a clock-class mismatch.

- **Refuse a second push by making grant spending two-phase** — FIX — value 4 — effort S — risk low — category: durability
  Why: the push grant is "spent on use", and a crash between the push and the mark-spent write either leaves the grant live or loses the record. Assumption: the spend is one write after the push.
  Done when: a test kills the process between push and mark. On resume, `fm ship` sees the commit on the remote, marks the grant spent and pushes nothing further.

- **Stop the line when the goal engine has an incident** — FEATURE — value 4 — effort M — risk low — category: process
  Why: the user's rules say "finish round 1 completely... no new maintenance until that's done", and a false-done is the worst failure for a plan carrier. Assumption: incidents are recorded as typed ledger entries.
  Done when: after a recorded false-done or lost-plan incident, `fm next` offers no new FEATURE task until a red-first regression for that incident is committed, and says why.

- **Boot into safe mode after repeated hook crashes** — FEATURE — value 4 — effort M — risk med — category: degradation
  Why: hooks run on every tool call, and a bug in Foreman should never wedge the user's session. T-0798 lists crash-loop quarantine only as a deferred idea.
  Done when: three consecutive hook exceptions flip a state file to guard-only mode, `fm doctor` names the cause, and one successful `fm doctor --fix` flips it back.

- **Run a clean-container proof with no `claude` on PATH** — FEATURE — value 4 — effort M — risk low — category: portability
  Why: a standing rule says install.sh, `fm`, `fm doctor` and the task loop work with no claude installed. Nothing in the pack shows a test for it.
  Done when: a CI job in a bare container runs install.sh, `fm doctor` and a task create, prove and close, and goes red if any step reaches for `claude`.

- **Survive terminal hangup by detaching the drive** — FIX — value 4 — effort M — risk med — category: survival
  Why: the goal "carries the plan over days", and a dropped SSH or closed terminal SIGHUPs a foreground drive. Assumption: the drive is currently tied to the launching terminal.
  Done when: killing the controlling terminal leaves `fm drive` running under its own session or scope, and `fm status` reports it still alive.

- **Protect goal state from `git clean`, `checkout` and worktree removal** — FIX — value 4 — effort S — risk low — category: durability
  Why: the guard blocks commands the user would never want, but untracked state inside the work tree is exactly what `git clean -fdx` eats. Assumption: some goal or task state sits in untracked repo paths.
  Done when: a test runs `git clean -fdx` and `git worktree remove` in a fixture repo and the goal state survives, or the guard refuses the command with the repair line.

- **Cap each plan row's memory, output and wall time** — FEATURE — value 3 — effort M — risk med — category: containment
  Why: T-0831 (capped `claude -p` children) and T-0798 (crash-loop quarantine) show runaway children are a known failure class. A row that OOMs the host is blamed on nobody.
  Done when: a fixture row that allocates without limit is killed at its ceiling, parked with "exceeded memory cap", and the next row proceeds.

- **Lint every subprocess call for a deadline** — CLEAN — value 3 — effort S — risk low — category: hangs
  Why: the pack has fixes for a hung tick and for a waiting hook (T-2605). Whether every `git`, `gh`, `claude -p` and `systemctl` call is bounded is not shown. Assumption: some are not.
  Done when: a test walks the AST of `plugin/lib` and fails on any `subprocess` call without a timeout, with an allowlist file whose entries each carry a reason.

- **Mark a verdict unstable when it flips done and not-done twice** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: T-2606 (a criterion whose runs matched no test) and the flaky bench show verdicts can change with no code change.
  Done when: a goal whose verdict flips twice in a week shows "unstable: flipped N times, last cause X" and cannot print a plain "done".

- **Correlate every hook, lane and ledger line with a goal id** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: after a crash on day three, reconstructing "what was happening" means joining many logs by guesswork. Assumption: there is no shared id today.
  Done when: `fm trace GOAL` prints one time-ordered list of hook decisions, lane events and ledger writes for that goal, each with the id.

- **Wild: run a Jepsen-style fault filesystem under the state dir** — TEST — value 3 — effort L — risk med — category: durability
  Why: assumption: atomic rename and lock code is only tested on a healthy disk. A FUSE or LD_PRELOAD layer can inject EIO, ENOSPC, torn writes and reordered renames while three concurrent `fm` processes run.
  Done when: a checker replays the operation history, asserts no acknowledged write is lost or doubled, and the suite fails when a planted torn-write bug is enabled.

- **Wild: hold a weekly brownout day with cgroup limits** — TEST — value 3 — effort M — risk low — category: resilience
  Why: assumption: Foreman is only tested at full speed. A day under `systemd-run` limits (io.max, CPU quota, a small memory.max) shows which verbs time out, retry or lie.
  Done when: the brownout run writes a table of verb, limit and outcome, and any verb that returns wrong output instead of an error is filed as a FIX.

- **Wild: feed hostile real-world pastes through every hook** — TEST — value 3 — effort S — risk low — category: robustness
  Why: users paste whole logs and binary junk, and the harness already wraps pasted text. A corpus of 1 MB logs, ANSI, NUL bytes, invalid UTF-8 and very long lines through UserPromptSubmit and PreToolUse should never crash a hook.
  Done when: a corpus test runs every hook on each sample and asserts exit 0 or a deliberate deny within the latency budget.

Next question: Which Foreman state file would cost the user the most days if lost tonight, and does anything outside Foreman hold a restorable copy?
Next question: When two harnesses write the same repo's goal state on the same day, which one's version wins, and who is told?
