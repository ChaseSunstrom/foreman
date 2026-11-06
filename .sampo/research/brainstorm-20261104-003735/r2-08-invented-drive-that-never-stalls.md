# Brainstorm — lens: invented: drive that never stalls

- **Add a stall taxonomy with per-class recovery** — FEATURE — value 5 — effort M — risk med — category: drive reliability
  Why: the request says "drive stops appeared (0 to 0.1)"; recent fixes T-2873, T-2900, T-2901 each patched one phantom-wait cause (ghost agents, dead-session shells, re-push churn).
  Done when: every drive pause writes a typed record (phantom-wait, usage-limit, endpoint-down, blocked-on-user, tool-failure-loop, gate-red), and a test injects each class and asserts the drive's recovery action (release, wait, fallback, skip, retry, fix-task) for that class.

- **Release phantom holds by checking live OS processes** — FIX — value 5 — effort S — risk low — category: drive reliability
  Why: the running-set has been wrong three times in a row (engine list omits agents, tail scan too short, union adds finished ones). Counting an agent the OS no longer runs is what stalls a night.
  Done when: a drive holding on N agents whose pids are gone releases within one tick, tested with a fake engine list naming dead pids.

- **Run the drive under a user systemd timer, not just the session** — FEATURE — value 5 — effort M — risk med — category: unattended
  Why: the user wants overnight progress; a drive that lives and dies with a terminal stops when the terminal does (T-2900 shows dead sessions already leave work open). assumption: Arch with systemd user units.
  Done when: killing the session mid-queue leaves a timer that resumes the drive within 5 minutes, verified by a script that kills and waits.

- **Add a progress watchdog with an escalation ladder** — FEATURE — value 5 — effort M — risk low — category: drive reliability
  Why: stalls are only noticed by the user today. assumption: no ledger measure of "no task state change in N minutes" exists.
  Done when: after 20 quiet minutes with work queued, the drive logs a stall record, tries re-tick, then releases holds, then switches the next task to a different lane, then writes a morning card line; each rung is tested.

- **Trip a circuit breaker on repeated failing tool calls** — FIX — value 4 — effort M — risk low — category: tool failures
  Why: failed tool calls are up by half. Retrying the same failing call burns the night.
  Done when: the third identical failing call signature in a task is refused with a "Next:" naming a different approach, and the breaker count shows in `sampo doctor`.

- **Fall back to local models while a usage limit is waited out** — FEATURE — value 5 — effort M — risk med — category: unattended
  Why: the user wants local models used without limit for background volume, and the standing rule says to wait out limits, which is idle time. Local work (triage, review, drafts) can fill it, marked unwitnessed.
  Done when: with a simulated usage limit, the drive runs at least one local-model task from the queue and tags its result unwitnessed.

- **Keep a never-empty ladder of unblocked work** — FEATURE — value 4 — effort M — risk low — category: queue
  Why: the drive stops when the next item is user-blocked or held (T-0325, T-0335 blocked; round-first holds Foreman-filed items). A stop with open work behind is a stall.
  Done when: when the head of the queue is blocked, the drive picks the next unblocked item, and a test with a queue of all-blocked-but-one proves it picks that one.

- **Replay the drive's last 50 ticks against a candidate fix** — FEATURE — value 4 — effort M — risk low — category: testing
  Why: the same class of bug returned three times, each fixed from one observed case. Recorded engine shapes would catch the next one first.
  Done when: a fixtures file of real running-set payloads runs through the wait function in CI and fails on a planted ghost agent.

- **Check the model endpoint before a swap and batch around it** — FEATURE — value 3 — effort S — risk low — category: local models
  Why: steers say a switch on llama-swap costs about 3 minutes with no detection, which looks like a hang.
  Done when: the drive records "model switch, expect 3 min" instead of a stall and orders local jobs by the resident model, shown by a test with two queued models.

- **Wild: Run a stall drill every night first** — FEATURE — value 3 — effort M — risk low — category: drive reliability — wild
  Why: assumption: stalls come from unrehearsed states. A 2-minute synthetic goal with planted faults (dead agent, killed shell, 429) runs before bed and must pass or the morning card says the night is unsafe.
  Done when: the drill runs from a timer, writes pass/fail, and a deliberately broken wait function makes it fail.

- **Wild: Have a second drive audit the first** — FEATURE — value 3 — effort L — risk med — category: agents
  Why: assumption: a stuck process cannot see its own stuck. A tiny local-model sentry reads the ledgers every 10 minutes and files a stall record or nudges the drive.
  Done when: freezing the main drive's tick makes the sentry write a typed stall record within 15 minutes.

- **Wild: Let a stalled drive page the user with one glyph** — FEATURE — value 2 — effort S — risk low — category: notifications — wild
  Why: the user said "stop asking me for stuff", so a page must carry no question: one status-line glyph and a phone notification only when a stall exceeds the ladder.
  Done when: an unrecoverable stall sets a glyph in the pane and sends one notification with the typed reason and no prompt.

- **Write a night plan the drive grades itself against** — FEATURE — value 3 — effort M — risk low — category: unattended
  Why: "overnight progress" is not measurable today. assumption: no sealed plan exists.
  Done when: before the night a plan lists expected tasks and a minimum count; the morning card shows plan vs done and names each shortfall's stall class.

- **Split drive stops from drive waits in the ledger** — CLEAN — value 3 — effort S — risk low — category: metrics
  Why: the "stops 0 to 0.1" gap counts both real stops and legitimate waits (usage limits, gates), so the number cannot guide fixes.
  Done when: the stop metric excludes records typed as expected waits, and the before/after number is printed by `sampo outcomes`.

Next question: What fraction of drive stops over the last 30 nights were true stalls rather than legitimate waits, and does any ledger record the cause well enough to tell?
Next question: If the user's terminal and the host session both vanish at 3 a.m., what is the full set of processes that could still resume the queue, and who owns each?
