# Brainstorm — lens: reliability

- **Add a hook-schema contract test against the installed `claude` binary** — FIX — value 5 — effort M — risk low — category: reliability
  Why: Foreman depends on 14 hook events and `claude plugin eval`; CC ships new releases often and the prior list only proposes a "nightly canary" in passing. Assumption: payload field names can drift silently, and fm doctor doesn't diff them against what the live binary emits.
  Done when: `fm doctor` runs each registered hook with a captured real payload from the installed `claude --version`, and fails with the field name when a payload key Foreman reads is missing or renamed.

- **Write step state transactionally with a crash-safe journal** — FIX — value 5 — effort M — risk med — category: durability
  Why: T-0759 says it works on steps without updating the step index; resume-at-exact-step after `/compact` depends on that state being right. Assumption: step updates are plain file writes, so a kill mid-write can leave plan and ledger disagreeing.
  Done when: a test that SIGKILLs `fm task step` at every write point leaves the store loadable, and resume lands on either the old or new step, never a torn one.

- **Detect idle with a heartbeat the Stop and Notification hooks both stamp** — FIX — value 5 — effort S — risk low — category: liveness
  Why: T-0758 "make sure it doesn't sit idle like it is" — the current wake path depends on tmux send-keys reaching a pane, with no proof that the wake landed.
  Done when: a session whose queue is non-empty and last heartbeat is older than N minutes gets a recorded wake attempt plus an acknowledged result, and `fm status` shows "wake unacked" when none arrives.

- **Make every hook fail open with a recorded, bounded reason** — FIX — value 4 — effort S — risk med — category: resilience
  Why: hooks are latency-gated by bench_hooks.py; a hook that times out or throws in bypass mode either blocks work or silently skips the guard. Assumption: the outcomes differ per hook and aren't uniformly logged.
  Done when: forcing an exception in each of the 14 hooks yields a documented allow/deny per hook and one line in a `hook-faults` log that `fm doctor` summarizes.

- **Quarantine a lesson or rule that preceded repeated regressions** — FEATURE — value 4 — effort M — risk med — category: learning safety
  Why: recent commits add retired lessons and eval-inbox guard blocks; nothing shown stops a bad auto-learned rule from compounding. T-0217 (confidence) is still deferred.
  Done when: a lesson recalled before N failed first attempts is auto-demoted to "quarantined", excluded from recall, and listed in `fm lessons --quarantined` with its evidence.

- **Verify the installer end-to-end in a clean container on every release** — FIX — value 4 — effort M — risk low — category: release
  Why: install.sh pulls Python, plugins and wiring across Linux/macOS/WSL, and the releases 1.2.17–1.2.27 are shipped by hand. Assumption: no automated fresh-machine install check exists.
  Done when: `release.py` refuses to publish unless a fresh-container run of the one-line install passes `fm doctor` and the roundtrip e2e.

- **Give every fm command a lock with stale-owner recovery** — FIX — value 4 — effort M — risk med — category: concurrency
  Why: worktree lanes, `fm night`, the bus, and several sessions all write the central store at once; the pack mentions "fsck and journal" only as an idea title.
  Done when: a stress test of 8 concurrent writers plus a killed lock holder finishes with no lost update and the stale lock reclaimed within a bounded time.

- **Replay the last 100 guard decisions against every guard change** — SECURITY — value 4 — effort M — risk low — category: regression
  Why: the guard keeps being tuned (pipe-to-bash, heredoc, `_drives_fm`), with dropped items showing delicate allow/deny boundaries; one loosening could silently let a block through.
  Done when: CI replays recorded decisions and fails with a diff listing each command whose verdict changed, unless the change is annotated as intended.

- **Detect a "checked" criterion whose verify ran nothing** — FIX — value 5 — effort S — risk low — category: verification
  Why: the dropped item shows a criterion whose `-k a or b` verify ran no tests, and another used a missing pytest; both were accepted as evidence.
  Done when: a verify command exiting 0 with "0 tests ran", "no tests collected" or a missing-tool message is recorded as "vacuous", cannot satisfy a criterion, and the message names the command.

- **Probe a deliberately failing twin of every verify before trusting it (wild)** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: assumption: a verify that can't fail is worthless; the pack's "negative twins" suggests the idea exists for claims but not for the verify command itself.
  Done when: for a new criterion, Foreman mutates the target in a scratch worktree, confirms the verify turns red, and refuses the criterion if it stays green.

- **Run a scheduled "fire drill" that kills a session mid-task and checks resume (wild)** — FEATURE — value 3 — effort M — risk low — category: chaos
  Why: resume at the exact step is the core promise, yet it is only exercised by hand after `/compact`. Assumption: no recurring automated drill covers it.
  Done when: a nightly job starts a scripted task in a throwaway repo, kills it at a random step, resumes, and posts pass/fail with the step where state diverged.

- **Keep a last-known-good Foreman snapshot and auto-roll back on failed doctor (wild)** — FEATURE — value 3 — effort M — risk med — category: self-update
  Why: Foreman edits its own plugin and ships updates every few days; a broken release in bypass mode could disable its own guard. Assumption: no automatic rollback exists.
  Done when: after an update, a failing `fm doctor` restores the previous version tree, and the rollback is recorded with the failing check.

- **Pin and diff the model-visible prompt surface between versions** — CLEAN — value 3 — effort S — risk low — category: drift
  Why: 73 skills, six agents and an output style are injected into context; the host's `/skill-doctor` isn't used, and prompt edits can bloat tokens or alter behavior unnoticed.
  Done when: `fm doctor --prompt-surface` prints token counts per injected file, and a release fails if the total grows more than a set percent without a changelog note.
