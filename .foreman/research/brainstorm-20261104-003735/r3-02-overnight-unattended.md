# Brainstorm — lens: overnight unattended

- **Write a pre-sleep readiness card the drive checks before arming** — FEATURE — value 5 — effort S — risk low — category: overnight
  Why: Mission 6 wants overnight progress; the drive stops (0→0.1) and failed tool calls (+50%) appeared. Starting a night blind to the local endpoint, disk, tmpfs `/run/user` and the installed-vs-source drift wastes it. Assumption: these probes are cheap to run.
  Done when: `sampo night arm` refuses with a named cause when the local endpoint is down, free disk is under a set floor, or the installed copy differs from source, and arms otherwise.

- **Type every drive stop and auto-resume the transient ones** — FIX — value 5 — effort M — risk med — category: drive
  Why: "drive stops appeared" is the top gap, and the recent commits (T-2900, T-2901, T-2873) are three separate phantom-hold fixes. Classes: usage limit (wait), phantom agent (release after live-process check), dead session (resume), real block (page).
  Done when: a replay of the last 50 drive ticks assigns each stop one class, and a fault-injected phantom hold is released within 20 minutes with the class in the ledger.

- **Add a night ledger answering "why did this start?"** — FEATURE — value 4 — effort M — risk low — category: triggers
  Why: Self-triggering is the request; the user can't audit unattended starts without a provenance record. Assumption: triggers write a stamp at spawn.
  Done when: `sampo night why <task>` prints the trigger kind, event, rule id and time for every self-started session in the last 24 hours.

- **Fence trigger payloads as untrusted data with a lower grant tier** — SECURITY — value 5 — effort M — risk med — category: safety
  Why: CI logs, issue text and file contents will start sessions in bypass mode with nobody watching; this is the injection path. The Ward already exists but sees only commands.
  Done when: a planted issue body saying "run curl … | sh" yields a Ward block and no executed command in a triggered session test.

- **Cap trigger depth and filter self-caused events** — FIX — value 4 — effort S — risk low — category: triggers
  Why: Sampo's own commits and file writes would fire file and CI triggers, giving a loop. Assumption: no breaker exists yet.
  Done when: a test where a task's commit would re-fire its own trigger runs once, with the skip reason "self-cause" logged.

- **Batch queued installs into one hashed "Overnight yes" card** — FEATURE — value 4 — effort M — risk med — category: approvals
  Why: The request says installs are "queued for one yes". Each install should list package, source and hash; a changed hash after approval voids the yes.
  Done when: three queued installs show as one card; approving it runs only those three, and a tampered hash is refused.

- **Route background volume to the local model first, with a measured fallback** — PERFORMANCE — value 5 — effort M — risk med — category: local models
  Why: The user wants local models "without limit" for background volume. The model switch costs ~3 minutes, so jobs should be batched by resident model, qwen3.8-27b first.
  Done when: a night queue of 20 mixed jobs causes at most one model switch, and a job failing the local model's Exam is escalated once, with the escalation counted.

- **Repair failed tool calls by class with a retry budget** — FIX — value 4 — effort M — risk med — category: reliability
  Why: Failed tool calls are up by half. Classify (malformed args, missing path, worktree state not found, denied write) and apply the known fix, with a cap so retries cannot spin.
  Done when: the top three failure signatures from the ledger are recovered automatically in a replay, and a fourth identical failure stops with a typed reason.

- **Seal a night plan and print a morning card graded against it** — FEATURE — value 4 — effort M — risk low — category: reporting
  Why: Unattended work needs a legible result. Separate "done", "waiting on you" and "could not run" from "nothing to do".
  Done when: after a simulated night, the card lists each planned item with one of four outcomes, and a skipped item is never shown as done.

- **Add a dead-man heartbeat that watches the drive from outside it** — FEATURE — value 4 — effort S — risk low — category: reliability
  Why: A drive that stalls silently is the exact failure seen. A systemd user timer checking the heartbeat file survives the session dying.
  Done when: killing the drive process produces a stall record and a restart within a set interval, with no session open.

- **Wild: Replay a recorded week of events into a scratch tree before enabling any trigger** — FEATURE — value 4 — effort M — risk low — category: triggers
  Why: wild. `sampo trigger test --since 7d` shows what would have fired and what it would have cost.
  Done when: running it on a new rule prints fire/skip counts with reasons and changes nothing in the real tree.

- **Wild: Plant a canary issue and a canary red CI each night** — FEATURE — value 3 — effort M — risk low — category: self-test
  Why: wild. A synthetic event in a scratch repo proves the whole chain (watcher, trigger, Ward, task, close) still works before the real night begins.
  Done when: a broken watcher makes the canary fail and the arm refuses with that cause.

- **Wild: Pause all triggers when nobody reads the morning card for three days** — FEATURE — value 3 — effort S — risk low — category: safety
  Why: wild. Unwitnessed autonomy drifts; a read-receipt dead-man limits it without asking the user anything.
  Done when: after three unread cards, triggers go to observe-only and one line says so at the next session start.

- **Wild: Yield the GPU the moment the user appears** — FEATURE — value 3 — effort M — risk med — category: local models
  Why: wild. Background volume must not block the user's morning model; detect input or a session start and pause the batch at a safe point.
  Done when: starting an interactive session mid-batch pauses the local jobs within 30 seconds and resumes them on close.

Next question: Which unattended outcome would the user most regret finding in the morning, and does any current gate stop it?
Next question: When a trigger fires while the user is working in the same tree, who wins?
