# Brainstorm — lens: reliability

- **Run the unattended drive through a real suspend/resume and network-loss soak** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: earlier question "which unattended paths have never been run end-to-end on a real clock while the machine slept, suspended or lost its network?" is unanswered; the user's steers demand waiting out usage limits and resuming where stopped.
  Done when: a scripted test suspends the process (SIGSTOP plus a clock jump), cuts the network for a fake agent, and `fm run` resumes with no duplicate task close and no lost ledger line.

- **Make every ledger writer kill-safe, proven by a kill-point sweep** — FIX — value 5 — effort M — risk med — category: ledgers
  Why: the pack's drill and verify-ledger work covers deletions and mutation, but torn writes at each append are not listed as swept; hash-chained lines break if a write is half done.
  Done when: a test SIGKILLs a writer at every append call site and `fm verify-ledger` plus every reader still loads, naming the torn tail.

- **Add a two-phase grant spend so a crash cannot double-push or lose a grant** — FIX — value 4 — effort M — risk med — category: ship safety
  Why: the push grant is "spent on use" through `fm ship`; assumption: a kill between push and the spend record lets a retry push twice or leaves the grant dangling.
  Done when: killing `fm ship` after the push and before the record, then rerunning, reports "already pushed sha X" and spends the grant exactly once.

- **Print a one-line "running degraded" status that survives every fail-open** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: earlier question "what does the user see in the first minute after a silent fail-open?" is untested; hooks fail open by design, so silence looks like health.
  Done when: forcing a hook import error makes the next `fm` and session start show "degraded: <hook> failed open at <time>", and a test asserts it.

- **Declare fail-open or fail-closed per hook, and crash-test each** — CLEAN — value 4 — effort M — risk med — category: hooks
  Why: the guard stops bypass-mode commands; assumption: not every hook's crash policy is stated, and a guard crash failing open is the worst case.
  Done when: a table lists each hook's mode, and a test injects an exception into each and asserts the declared behaviour.

- **Treat "could not run" as a third result in the ship gate** — FIX — value 4 — effort S — risk low — category: gates
  Why: the user pushes only through a full-suite-gated `fm ship`; a gate that times out or lacks a tool must not read as pass or plain fail, and the ship gate's timeout is already a named gap.
  Done when: a gate step missing its tool or timing out makes `fm ship` refuse with "unrun: <step>" and a distinct exit code.

- **Detect a second live session or drive on the same repo and state dir** — FEATURE — value 4 — effort M — risk low — category: concurrency
  Why: hand and Foreman edits to the same tree, queue and ledger is an open question; parallel lanes, the timer and the user's session can all write.
  Done when: starting a second `fm run` on a locked repo exits with the holder's pid, age and a stale-lock verdict, and a test covers a dead holder.

- **Check which side wins when the user's hand and Foreman both change tree, queue or ledger** — FIX — value 3 — effort M — risk med — category: concurrency
  Why: the pack's open question; assumption: readers choose inconsistently.
  Done when: a table of each reader's precedence exists, and a test edits the queue by hand mid-drive and asserts the drive notices rather than overwrites.

- **Add a dead-man heartbeat for the whole tower** — FEATURE — value 4 — effort M — risk low — category: liveness
  Why: the standing rule says the tower advances itself; a silently stopped tick looks the same as a quiet night.
  Done when: `fm doctor` shows "last alive" per unattended path, turns red past 2× its interval, and a stopped timer in a test triggers it.

- **Wild: Pull-the-plug day, a seeded random SIGKILL of the real drive on a scratch repo** — FEATURE — value 4 — effort M — risk low — category: chaos
  Why: wild; the kill-point sweep covers writes, but only random kills mid-drive find ordering bugs between ledgers.
  Done when: a nightly job kills the fake-agent drive at 20 random moments and every run recovers to a fsck-clean state.

- **Wild: Run the guard in two independent implementations and block on disagreement** — SECURITY — value 4 — effort L — risk med — category: guard
  Why: wild; the guard is regex-based with a known gap on pathological and unparseable commands, and a second 100-line implementation catches parse bugs the first shares with itself.
  Done when: a differential test over the guard exam corpus lists every disagreement, and the run-time vote blocks on any.

- **Wild: Fall back to the last good install generation when a hook fails to import** — FEATURE — value 4 — effort M — risk med — category: install
  Why: wild; a bad self-change landing in the hook path would take down every session, and the foreman-ui host version skew (T-0418, T-1217) shows install drift happens.
  Done when: corrupting a hook module in the live install makes the next session start run the prior generation and print "rolled back, cause X".

- **Fuzz the readers with a fake clock and ledgers at 10× size** — PERFORMANCE — value 3 — effort M — risk low — category: readers
  Why: `c.clock()` with `FOREMAN_NOW` just landed with edge tests, but reader time against a large ledger is not benchmarked.
  Done when: a bench runs each windowed reader on a 10× synthetic ledger and fails any over its recorded bar.

Next question: which of Foreman's own state files live on volatile or sync-folder paths, and what does each reader do when they vanish or fork?
Next question: when a Foreman-initiated push, merge or cherry-pick is interrupted midway, which command does the user have to run by hand, and does Foreman print it?
