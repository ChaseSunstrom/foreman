# Brainstorm — lens: reliability

- **Enumerate crash points in every state-writing verb** — FEATURE — value 5 — effort M — risk low — category: crash safety
  Why: Rounds 1–2 fixed race and edge bugs one at a time (T-0833 lane rm, T-0839 tidy race, T-0841 resume watcher). The idea list has torn-write fuzzing and kill drills, but they only sample failures. Run each verb under `sys.addaudithook`, make the Nth `open`, `replace`, `rename` or `fsync` raise, and loop N from 1 to the end. After each failure, assert that state loads, `fm doctor` is clean, and a re-run converges.
  Done when: a test enumerates every file-mutating call of `task finish`, `lane rm`, `tidy` and `compact`. Every injected failure leaves loadable state, and the suite fails if a verb's call count rises without a re-run.

- **Lock the session down after repeated guard fail-opens** — SECURITY — value 5 — effort S — risk med — category: guard integrity
  Why: Foreman blocks dangerous commands in bypass mode, and the hooks fail open on error. A guard that keeps crashing, timing out or hitting a bad payload means no protection, and the user never finds out. The list has "record the reason for a fail-open" but no escalation. Keep a per-session counter. After N fail-opens, the next outward or destructive command gets a hard ask or refusal, and the band shows the cause.
  Done when: forcing three guard exceptions in a test session makes the fourth `rm -rf` or `git push` return an ask or deny, and the reason line names the failing hook.

- **Differential-test the guard's parsing against real shells** — SECURITY — value 5 — effort M — risk med — category: guard correctness
  Why: The guard has its own chain, `cd` and script-file reading (T-0275, `_chain_dir`, `_run_dir`). Any gap between its tokenizer and what bash actually runs is a bypass. Feed a corpus of quoting, heredoc, `$(...)`, brace and alias cases to `bash -n` and to a sandboxed `bash -x` expansion with stubbed binaries. Assert that the guard sees every command the shell would execute.
  Done when: a generated corpus of at least 500 commands shows zero cases where the shell would run a binary the guard didn't parse, and each known gap is an xfail test with a T-id.

- **Swap Foreman's code tree atomically under live sessions** — FIX — value 4 — effort M — risk med — category: upgrade safety
  Why: `install.sh` clones or pulls into `~/.claude/foreman` while sessions are running hooks from the same path. A pull that lands mid-turn can run a half-updated mix of `lib/` modules. Install into `versions/<sha>/` and flip a `current` symlink. Each session pins its version at SessionStart, and old versions are reaped when no pin remains.
  Done when: a test runs a hook loop while an update swaps the tree and sees zero import errors or mixed-version runs. A live session keeps its pinned sha until it ends.
  Assumption: hook command paths can go through the symlink.

- **Rehearse every upgrade on a clone of the user's real state** — FEATURE — value 4 — effort M — risk low — category: upgrade safety
  Why: The suite uses fixtures, but real ledgers carry years of odd shapes (lone surrogates, old fields, T-0001 era rows). Before an update goes live, copy the state read-only into a scratch HOME. Run `fm doctor`, `status`, `digest` and a replay of the last 20 hook payloads with the new code. Block the update on any new error.
  Done when: an update fails closed in a test where the new version cannot parse a planted legacy row. The failure names the row and the live install is untouched.

- **Take point-in-time snapshots of Foreman's own state** — FEATURE — value 4 — effort M — risk low — category: recoverability
  Why: Round 5 snapshots the user's uncommitted work, but the queue, ledger, lessons and decisions have only fsck and journal ideas, which detect damage but can't undo it. Make hardlink-deduplicated snapshots at task boundaries and daily, with retention. `fm state restore --at <time|T-id>` restores the older copy. Snapshots go into a private mode-0700 folder.
  Done when: corrupting `tasks` in a throwaway HOME and running `fm state restore --at -1h` returns the exact earlier queue. The snapshot folder stays under a configured byte cap.

- **Shuffle and parallelise Foreman's own 155-file test suite** — CLEAN — value 3 — effort S — risk low — category: test reliability
  Why: Gates are `fm doctor`, roundtrip and bench, and CI runs the suite in a fixed order. Order dependence, shared temp names and leaked env show up only under shuffle or parallel runs. Add a `--shuffle seed` mode and a 4-way parallel mode to CI. Print the seed on failure.
  Done when: CI runs three shuffled seeds and one parallel run green, and a deliberately order-dependent test fails with a replayable seed.

- **Track five reliability SLOs with a burn-rate line** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: Many reliability ideas exist (watchdogs, receipts, canaries) but no single measure says whether Foreman got more or less dependable. Define hook fail-open rate, wake delivery rate, resume success, silent-recovery count and guard-timeout rate. Compute them from existing logs over 7 days and show one line in `fm digest` and the release gate.
  Done when: `fm digest` prints five rates with denominators, and the release script refuses when any rate is past its threshold.

- **Warn when two live sessions edit the same file** — FEATURE — value 3 — effort M — risk med — category: concurrency
  Why: T-0841 shows two sessions on one repo already happen, and the session claim tracks only who owns the task. Record a short edit claim (file, session, time) on each edit. When a second session edits a claimed file, the PostToolUse nudge names the other session and its task.
  Done when: two simulated sessions editing one file within five minutes produces exactly one warning in the later session, and none after the claim expires.

- **Run a coexistence matrix against rival plugins' hooks in CI** — FEATURE — value 3 — effort M — risk low — category: coexistence
  Why: The rival survey (superpowers, ECC, claude-mem, ruflo and others) and the installer's conflict report show that hook interference is real. Replay recorded payloads through Foreman's hooks with each rival's hook config merged in. Assert that the guard decision, step pointer and Stop verdict don't change.
  Done when: CI has one row per rival and fails when merging a rival's hooks changes any recorded Foreman decision.
  Assumption: rival hook configs can be fetched pinned and offline.

- **Wild: Bisect Foreman's own repo automatically when doctor goes red after an update** — FEATURE — value 4 — effort M — risk med — category: self-healing
  Why: `fm bisect` and the replay corpus exist, but only for user repos. After an update, if `fm doctor` or the replay fails, run bisect over the range of Foreman commits just pulled. Pin the install to the last good sha and file a task naming the culprit commit.
  Done when: a test plants a breaking commit in a three-commit update range. The install ends on the parent sha, and a task names the bad commit.

- **Wild: Restore the user's own state into a scratch HOME monthly** — FEATURE — value 3 — effort M — risk low — category: recoverability
  Why: A backup you never restored isn't one. Once a month, `fm night` takes the latest snapshot, restores it into a scratch HOME, runs `fm doctor` and `fm status` there, and records pass or fail with the age of the snapshot.
  Done when: `fm night` logs a "restore drill" row with pass or fail. A deliberately corrupted snapshot makes the next digest say "last restore failed".

- **Wild: Forecast reliability problems from trends before they bite** — FEATURE — value 2 — effort M — risk low — category: predictive health
  Why: Disk fill, hook p99 creep and a fresh Claude Code version are all visible in data Foreman already logs. Fit simple trends. When the disk will fill within about a week, or hook latency is rising for a week, say so once in the greeting with the single fix command.
  Done when: replaying a fixture where state grows 5% a day yields a one-line warning with days remaining. A flat fixture yields none.
