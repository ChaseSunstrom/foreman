# Brainstorm — lens: deepen: ops

- **Climb a proof ladder for every infra change** — FEATURE — value 5 — effort M — risk low — category: ops
  Why: the request says what can't be proven gets labelled unproven; today there is no shared scale. Rungs are declared, linted, dry-run, throwaway target, live read-only, canary. `fm task finish` prints the top rung reached and names the next one up.
  Done when: finishing a task that edits a systemd unit with only a lint run prints "ops: linted, not rehearsed" and the closing record stores that rung.

- **Diff declared ops config against the live host** — FEATURE — value 5 — effort M — risk low — category: ops
  Why: T-2542 checks that installed foreman-* timers are alive, but not that they match what the repo declares. `fm ops drift` compares units, timers, CI workflows and env files with the host. It also catches hand edits to generated files such as steers, goals and coverage, and names which reader would overwrite or ignore each one (answers the hand-edit question).
  Done when: editing an installed unit by hand makes `fm ops drift` print the changed line and which Foreman writer would clobber it.

- **List the provers this machine can run today** — FEATURE — value 4 — effort S — risk low — category: ops
  Why: T-0325 is blocked on libappindicator, and T-0336 is blocked on codex/gemini/opencode not being live-verified. `fm ops provers` prints a table of runnable, missing (with install line) and unreachable provers. A missing one lowers the proof ladder's ceiling for that claim and is queued through the install path.
  Done when: on a host without codex, the table shows it missing, and a task whose proof needs it finishes with "unproven: prover absent".

- **Probe every path Foreman executes from for noexec, read-only and volatile mounts** — FIX — value 4 — effort S — risk low — category: ops
  Why: this very session runs from /run/user/1000, a tmpfs on a hardened kernel. Hook scripts, child runs and journals can silently fail or vanish on reboot. `fm doctor` tests exec, write and persistence for each path and flags state that lives only in volatile storage.
  Done when: remounting the state directory noexec in a test makes `fm doctor` WARN with the path and mount options.

- **Run deep provers on idle CPU overnight** — FEATURE — value 4 — effort M — risk med — category: ops
  Why: T-2607 already makes the night tick report what it couldn't watch. Add a queue of slow checks (mutation runs, full-flow replays, long-horizon smoke) that runs only while load is low and lands in the digest with its rung. The rung ledger decides which claims get deep proof first.
  Done when: a tick with a 20-minute prover queued runs it under a load cap, and the next session note lists the result.

- **Build one expiry and next-fire board** — FEATURE — value 4 — effort M — risk low — category: ops
  Why: expiry clocks (push grants spent on use, publish grants, tokens, usage-limit waits, timers) are scattered across features. `fm ops clocks` merges them into one table of next fire time and time until lapse, and warns before a grant or token the drive depends on lapses.
  Done when: a timer set to fire in an hour shows that fire time in the table, and an expired publish grant makes the drive stop with the reason named.

- **Inventory persisted state outside the repo and classify it** — SECURITY — value 4 — effort M — risk low — category: ops
  Why: answers the open question about journals, bet ledgers, memory and units. `fm ops state` lists each path, its size, whether it holds prompt text or identifiers, and whether common backup or sync tools would copy it. Nothing is deleted.
  Done when: the command lists the journal and bet-ledger paths with a "contains prompts" flag and names any of them under a synced folder.

- **Turn passing flows into a post-ship canary** — FEATURE — value 4 — effort L — risk med — category: ops
  Why: `fm flow` and `fm shot` already prove the UI before ship. Re-running the same flow on a schedule after `fm ship` catches regressions the suite can't, and a failure files a task that cites the shipping commit.
  Done when: a flow breaks after ship, the next scheduled run files a task naming that commit, and the doctor shows the canary's last pass time.

- **Test alert rules and runbook references** — FEATURE — value 3 — effort M — risk low — category: ops
  Why: docs-against-code is in scope, and runbooks rot. `fm ops runbook` checks that every alert maps to a runbook, that every command in the runbook exists and passes a dry run, and that every linked path resolves.
  Done when: a runbook citing a verb that was renamed fails the check with the line number.

- **Settle a two-device lease conflict and tell the loser** — FEATURE — value 3 — effort M — risk med — category: ops
  Why: answers the desk-lease-versus-phone-tap question. A goal row takes a lease with a holder id and timestamp. A second actor is refused with the holder named, and a lease older than three intervals is flagged stale instead of silently stolen.
  Done when: two simulated actors claim one row, the second gets "held by desk since 10:02", and an expired lease is reclaimed with a notice to the first.

- **Replay the project's own real logs through old and new builds (wild)** — FEATURE — value 5 — effort L — risk med — category: ops
  Why: wild. The journals, hook payloads and guard decisions already recorded are real traffic. `fm ops replay A..B` feeds them to both builds and shows changed decisions. It would have caught the hook-wait regression behind T-2605 with real inputs instead of a bench.
  Done when: replaying 1,000 recorded guard events through two commits prints the count of changed allow/deny outcomes with the first three examples.

- **Run a chaos game day against Foreman's own ops (wild)** — FEATURE — value 4 — effort L — risk high — category: ops
  Why: wild. In a throwaway copy, kill a timer, fill the disk, skew the clock, break the library import and corrupt the bet ledger. Then check that `fm doctor` and the next session note name each fault. Each undetected fault becomes a task and a recorded bet, so the doctor's blind spots get measured.
  Done when: a scripted run injects 6 faults in a sandbox copy and prints which ones the doctor missed.

- **Cross-check proofs on a second machine (wild)** — FEATURE — value 3 — effort L — risk med — category: ops
  Why: wild. A proof that passes only on the author's host is weak. A disposable container, or a second box the user names, re-runs the task's proof commands and reports agreement. Disagreement downgrades the rung to "works here only" and uses the same ladder.
  Done when: a task that passes locally but depends on an unlisted local file shows "unproven elsewhere" after the second run.

- **Hand over a signed proof passport per release (wild)** — FEATURE — value 3 — effort M — risk low — category: ops
  Why: wild. The README and site make claims, and a steer says claims need proof. `fm ship` bundles each claim, its command, its output hash, its rung and its unproven list into a file anyone can re-verify offline, and the site links it.
  Done when: tampering with one recorded output makes `fm verify-passport` fail and name that claim.

Next question: Which ops gauges does Foreman only trust because it wrote them (timer liveness, bet settlement, canary state), and what outside signal could contradict each?
Next question: When the host Foreman runs on is wiped or replaced, what must be rebuilt by hand, and could a restore drill prove the rest comes back?
