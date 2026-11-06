# Brainstorm — lens: invented: drive that never stalls

- **Run the drive under a user systemd timer that outlives the session** — FEATURE — value 5 — effort M — risk med — category: unattended
  Why: Mission 6 asks for work that starts without the user, and a drive tied to one terminal dies with it (T-2900 closes what a dead process left open). Assumption: systemd --user is available, as on this Arch box.
  Done when: killing the terminal mid-queue, the timer starts a headless drive within 2 minutes and the next task is picked with no user input.

- **Write a typed stall record on every pause** — FEATURE — value 5 — effort S — risk low — category: observability
  Why: Drive stops went from 0 to 0.1 and the recent fixes (T-2873, T-2901) were each found by hand. Assumption: stops today carry free-text reasons.
  Done when: every drive pause appends one row with a reason from a closed set (usage-limit, phantom-agent, user-only grant, model-swap, tool-fail-loop, empty-queue) plus a deadline, and `sampo drive why` prints the last one.

- **Add a progress watchdog with an escalation ladder** — FEATURE — value 5 — effort M — risk med — category: reliability
  Why: Phantom waits held the drive twice. Assumption: there is no "no commit, ledger row or tool call for N minutes" signal.
  Done when: a fake wait injected into the drive is cleared by rung 1 (re-probe live processes), then rung 2 (release the lease), then rung 3 (a one-line report), each within its stated time.

- **Trip a circuit breaker on repeated failing tool calls** — FIX — value 4 — effort M — risk low — category: reliability
  Why: Failed tool calls are up by half. Assumption: the same call shape often fails repeatedly in a single session.
  Done when: three identical failures in a row stop the loop, put the task into "park with reason", and the drive moves on to the next task.

- **Keep a never-empty ladder of unblocked work** — FEATURE — value 5 — effort M — risk med — category: scheduling
  Why: The user wants overnight progress, and "wait for the user" stalls are real. Assumption: parked tasks wait on user-only grants.
  Done when: with the top task blocked on a user grant, the drive picks, in order, an unblocked queue item, then a local-model volume job (re-proof, doc claims, brainstorm), and logs the choice.

- **Fire triggers from files, CI and issues into the same queue** — FEATURE — value 5 — effort L — risk med — category: triggers
  Why: This is Mission 6's literal ask (schedules, file and event triggers, CI and issue watchers). Installs are queued for a single yes.
  Done when: a failing CI run and a new matching issue each file one dormant, deduplicated task, and a pending install appears as one batched yes in the morning card.

- **Check the model endpoint before a swap and batch around it** — PERFORMANCE — value 4 — effort S — risk low — category: local models
  Why: A model switch on the llama-swap endpoint costs about 3 minutes, and `/running` isn't relayed. Assumption: queued local jobs are not grouped by resident model today.
  Done when: a mixed queue of 6 local jobs triggers at most one swap, and the pace line names that swap rather than showing it as a stall.

- **Replay the drive's last 50 ticks against a candidate fix** — FIX — value 4 — effort M — risk low — category: testing
  Why: T-2873 and T-2901 each regressed the previous wait fix, so fixes are untested against real history. Assumption: engine events are logged enough to replay.
  Done when: `sampo drive replay --since N` reproduces a recorded phantom wait on the old code and shows it gone on the new, and this runs in the ship gate.

- **Wild: have a second drive audit the first** — FEATURE — value 3 — effort M — risk med — category: reliability
  Why: Assumption: a cheap local model can read the stall ledger and the live process list and flag "this wait is false" without sharing the main drive's blind spots. wild.
  Done when: against a planted false wait, the auditor flags it within 10 minutes and the main drive releases it.

- **Wild: write a "night plan" the drive grades itself against** — FEATURE — value 3 — effort S — risk low — category: unattended
  Why: Assumption: the user wakes to a card saying "done / stuck / unsure" and trusts a plan sealed before sleep more than a summary written afterward. wild.
  Done when: before the first night task the drive seals a plan file, and the morning card lists each planned item with its outcome and the first stall reason.

- **Wild: run a stall drill every night first** — FEATURE — value 3 — effort S — risk low — category: reliability
  Why: Assumption: breakages (usage limit, killed agent, dead endpoint) are the cheapest to find on a scratch task before the real queue runs. wild.
  Done when: a scratch lane is killed on purpose at 23:00, and the drive's recovery time is logged and compared with the previous night's.

- **Wild: let a stalled drive page you by a single glyph** — FEATURE — value 3 — effort S — risk low — category: notifications
  Why: Assumption: the user doesn't want prompts, only silence unless the drive is stuck for more than 20 minutes. wild.
  Done when: a stall past the threshold sends one desktop or phone notification with the typed reason, and nothing is sent while the drive is healthy.

- **Spend frontier tokens on stalls only after local models have failed** — FEATURE — value 4 — effort M — risk med — category: cost
  Why: The user wants local models used without limit for background volume. Assumption: no rule today decides which tier works on a stalled task.
  Done when: a stalled task is first retried on the local model with the scaffold, and a frontier call happens only after two local failures, with the escalation recorded.

Next question: Which of the 0.1 drive stops are real stalls and which are the drive correctly waiting on something, and does any ledger separate the two?
Next question: When a trigger fires while the user is actively working in the same repo, who yields, and is that written anywhere?
