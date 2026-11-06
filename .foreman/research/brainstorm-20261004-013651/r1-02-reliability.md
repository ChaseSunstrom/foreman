# Brainstorm — lens: reliability

- **Verify repo integrity in fm doctor** — FIX — value 5 — effort S — risk low — category: integrity
  Why: a crash left four zero-byte loose git objects that broke `git diff`, and fm doctor passed. Nothing checks the substrate Foreman's evidence depends on.
  Done when: with an empty file planted in a temp repo's `.git/objects`, `fm doctor` fails naming the file and prints a safe quarantine command. It also checks that state files parse and that the ledger's last line is complete JSON.

- **Make state writes atomic and crash-recoverable** — FIX — value 5 — effort M — risk med — category: durability
  Why: the machine crash corrupted git objects. Briefs, ledger and queue are plain files, so a crash mid-write could do the same. Assumption: writes are not yet temp-file, fsync and rename.
  Done when: a test that kills the writer mid-write (injected fault) leaves state either old or new, never truncated. A torn trailing ledger line is detected and skipped with a warning on load.

- **Make the drive wait on background work without ending the turn** — FIX — value 4 — effort M — risk med — category: drive
  Why: 18 drive turns ended only to wait on a reviewer subagent. This is the top friction item and it costs a resume round each time.
  Done when: a drive run with one pending reviewer records zero "ended turn to wait" events (or the waits are measured and recorded as an explicit state with no wasted turn). It resumes on completion in the same drive.

- **Add a guard false-positive corpus with a precision gate** — FIX — value 4 — effort S — risk low — category: guard
  Why: `git stash list`, a read-only python state read and a plugin-source heredoc were all wrongly blocked. The guard is "never weakened, only made more precise", so each false positive should become a permanent allow-case next to the must-block cases.
  Done when: those three commands are in a corpus file, and `fm check` fails if any allow-case is blocked or any block-case is allowed. Read-only git verbs (`stash list`, `worktree list`) are classified as reads.

- **Quarantine and score flaky tests** — FIX — value 4 — effort S — risk low — category: gates
  Why: one test class failed under load and passed on rerun. An untracked flake teaches everyone to distrust red, which undermines "evidence fm ran itself".
  Done when: a gate failure is automatically rerun once, and a fail-then-pass is recorded as "flaky" with the test name. `fm friction` lists flake counts, and a test flaking 3 or more times gets a ticket. A real failure still fails the gate.

- **Add a hook watchdog with fail-open or fail-closed policy per hook** — FEATURE — value 4 — effort M — risk med — category: hooks
  Why: hooks gate every edit, and latency p95 is 35 ms today. A hung or crashing hook would either block all work or silently drop enforcement. Assumption: no per-hook timeout or crash policy exists.
  Done when: an injected hang in a non-guard hook is cut off at a timeout and logged, and work proceeds. An injected crash in the guard denies the action with a clear message. `fm doctor` shows the policy table.

- **Reconcile state against reality on session start** — FEATURE — value 4 — effort M — risk low — category: recovery
  Why: the crash left Foreman unaware that its world was damaged. Assumption: the session-start hook doesn't compare the active brief's recorded commits, files and lanes with disk and git.
  Done when: after deleting a lane worktree or resetting a commit a brief cites, session start prints a short drift report. It names each stale reference and the command to repair it.

- **Wild: Run chaos drills for Foreman itself** — FEATURE — value 3 — effort M — risk low — category: resilience
  Why: crash, full disk, clock skew, a second concurrent session and a killed child are all untested. Assumption: only the happy path and some failure cases have tests. wild
  Done when: `fm drill` runs each fault in a temp copy. It prints a pass/fail table showing that Foreman either recovers or fails loudly, and each failure becomes a tracked item.

- **Wild: Keep a rolling black-box snapshot of state with one-command rewind** — FEATURE — value 3 — effort M — risk low — category: recovery
  Why: the drive makes many autonomous changes, and a corrupted or wrongly edited state needs a way back that doesn't touch the user's git history. Assumption: no state snapshots exist. wild
  Done when: state is snapshotted at each task close and each drive start, kept for the last N. `fm rewind --list` shows them, and `fm rewind ID` restores state after a diff preview and a yes.

- **Wild: Add a canary brief that proves the enforcement path works end to end** — FEATURE — value 3 — effort S — risk low — category: self-test
  Why: fm doctor passed while the substrate was broken, so it checks configuration, not behaviour. A synthetic brief that tries an edit without a brief, records evidence and closes would catch silent hook wiring failures. wild
  Done when: `fm doctor --canary` in a scratch repo shows the edit refused without a brief, allowed with one, and closing refused without evidence. It fails if any step behaves differently, and runs at plugin-update time.

- **Cap and age out the reviewer wait with a fallback verdict** — FIX — value 3 — effort S — risk low — category: drive
  Why: a reviewer subagent that never reports would stall the drive indefinitely. Assumption: no deadline exists on pending reviews.
  Done when: a review pending past its deadline is marked "timed out" in the brief. The drive continues, and the task cannot close as audited until it is rerun or the user explicitly waives it.
