# Brainstorm — lens: bold bets

- **Predict each proof command's result before running it** — FEATURE — value 4 — effort M — risk med — category: calibration
  Why: bets already exist for tasks and closes, but not for the cheapest, most frequent event, which is a command's own outcome. Assumption: surprises (predicted pass, got fail, or the reverse) correlate with wrong plans.
  Done when: a task's receipt lists each proof command with its predicted and actual result, and a surprise raises the ceremony level on the next step (a test asserts the raise).

- **Harvest the user's rewrites of landed Foreman lines into lessons** — FEATURE — value 5 — effort M — risk low — category: learning
  Why: the user's steers are mostly corrections, and outcome survival exists but doesn't ask what the user changed. Assumption: `git blame` can tie lines to a Foreman task id by its commit prefix (T-NNNN commits).
  Done when: a fixture where the user edits a line from T-X within 7 days produces a proposed lesson that cites the before/after hunk, and `fm outcomes` counts it as a partial rejection.

- **Write the acceptance test blind** — FEATURE — value 5 — effort M — risk med — category: proof
  Why: the standing rule says to use signals Foreman didn't author, yet the implementer still writes its own test. Assumption: a tool-less child can write a useful test from the ask and DONE-WHEN alone.
  Done when: on a FIX task a hidden test is written from the ask alone, run only at finish, and a receipt line shows "blind test: pass/fail". A fixture where the implementer's own test passes but the blind one fails blocks the close.

- **File repro tasks from the user's own runtime failures** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: intake reads only asks, CI and sessions. The host runs systemd, and Foreman installs its own timers and reads their liveness. Assumption: the user runs services whose failures show in `journalctl --user` or `systemctl --failed`.
  Done when: with an opt-in list of units, a unit that exits non-zero produces one inbox item holding the log excerpt (credentials redacted), deduplicated by signature.

- **Run bypass sessions on a copy-on-write overlay of $HOME with a side-effect diff** — SECURITY — value 5 — effort L — risk high — category: sandbox — wild
  Why: the guard stops listed commands, but nothing shows what a bypass-mode run changed outside the repo. Assumption: bwrap/overlayfs is usable on this hardened kernel.
  Done when: a session that writes `~/.config/x` shows that file in a post-run "outside the repo" report, and `fm rollback` restores it byte-for-byte.

- **Fork a finished or live session at any step into a counterfactual branch** — FEATURE — value 4 — effort L — risk med — category: replay — wild
  Why: the user steers by correcting mid-flight. Assumption: transcripts hold enough to resume from step N.
  Done when: `fm fork T-id@12 --say "use the other parser"` starts a lane from that step's tree and prompt, and `fm compare` prints both outcomes side by side.

- **Run lanes on the user's other machines over ssh** — FEATURE — value 3 — effort L — risk med — category: fleet — wild
  Why: T-0792 (lanes and fleet) is deferred, and the user is on one Arch box with usage idle at 0%. Assumption: the user has a second machine or VM.
  Done when: `fm lane --on host` runs a brief remotely, brings back the commit and the proof receipt, and a fixture with a dropped connection leaves no half-claimed task.

- **Compile steers, lessons and guard rules into AGENTS.md, GEMINI.md and .cursor/rules** — FEATURE — value 4 — effort S — risk low — category: portability
  Why: the steers say Foreman isn't specific to Claude Code, and T-0365 (generated repo section) is deferred. Other agents could inherit the discipline text even without the hooks.
  Done when: `fm export rules` writes the three files from stored state, and a doctor check flags any that are older than the newest steer.

- **Distill repeated winning trajectories into skills, kept only if they cut cost** — FEATURE — value 3 — effort L — risk med — category: skills
  Why: there are 1,388 skill files, written by hand. Lesson confidence (T-0217) is deferred. Assumption: closed tasks keep tool-call traces.
  Done when: three similar closed tasks yield a draft skill, a held-out replay shows fewer calls or tokens with it than without, and a draft that doesn't is discarded with the numbers kept.

- **Measure real-session code coverage of Foreman itself and file deletion candidates** — CLEAN — value 4 — effort M — risk low — category: subtraction
  Why: the lean ratchet counts lines and verbs, but nothing records which code real sessions execute. Assumption: sampling 1-in-20 sessions with `sys.monitoring` stays within the hook p95 budget.
  Done when: after 30 days of samples, `fm doctor` lists modules and functions with zero executions, each with its last-run date, and the hook bench shows no p95 regression.

- **Guard with a local small-model intent check for commands no rule matches** — SECURITY — value 4 — effort L — risk high — category: guard — wild
  Why: the guard works from known patterns, and "taint untrusted content" is in the catalog. Assumption: a local model can answer "could this destroy data?" in under 300 ms. Nothing leaves the machine.
  Done when: on a corpus of 100 obfuscated destructive commands plus 100 benign ones, recall is at least 90% with at most 2 false blocks, and the check is off unless a setting enables it.

- **Git-native team mode: the queue, claims and receipts in `refs/foreman/*`** — FEATURE — value 3 — effort L — risk med — category: team
  Why: the ledgers are single-host files (a host-wipe drill is already proposed). Assumption: the user will eventually share a repo with another person.
  Done when: two clones claim different tasks offline, fetch and merge with no conflict, and each receipt carries its author and host.

- **Keep a pre-registered prediction on every self-change and settle it from data** — FEATURE — value 4 — effort S — risk low — category: self-audit
  Why: the lean and ablation work needs a per-change claim to subtract by. Assumption: each change can state one measurable effect (hook p95, injected chars, pass rate).
  Done when: `fm ship` on a self-change requires a "predicts: metric ±N" line, and 14 days later a task is auto-filed to revert any change whose metric missed.

Next question: Which of Foreman's own high-frequency events (hook calls, command outcomes, reads of the ledger) have no measured expectation, so that drift in them could go unseen?
Next question: What would the user need to see in the first five minutes to trust a run they didn't watch, and which of those things would an outside observer be able to check?
