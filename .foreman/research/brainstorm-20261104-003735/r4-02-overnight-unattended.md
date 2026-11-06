# Brainstorm — lens: overnight unattended

- **Stage the night as a sealed work order before bed** — FEATURE — value 5 — effort M — risk low — category: night plan
  Why: the ask is overnight progress unattended, yet drive stops (0→0.1) mean nobody knows at bedtime what will run. Earlier ideas say "seal a night plan" only as a card; this one is the executable manifest: ordered tasks, resident model per phase, spend/disk caps, stop conditions, and one hashed "Overnight yes" covering every queued install.
  Done when: `sampo night plan` writes a manifest, `sampo night start` refuses to run any task or install not in it, and the morning card diffs plan vs actual.

- **Make drive stops typed, resumable and auto-healed for the transient classes** — FIX — value 5 — effort M — risk med — category: drive reliability
  Why: "drive stops appeared (0 to 0.1)" is a top gap, and T-2900/T-2901 fixed two phantom-hold causes one at a time. Assumption: more causes exist. Each stop gets a cause code (usage limit, dead agent, endpoint swap, disk, tool-fail storm); the drive auto-resumes the transient ones and files a fix task for the unknown ones.
  Done when: replaying 50 recorded stop events yields a cause for every one, and a simulated usage-limit stop resumes without a prompt.

- **Run the drive from outside any session as a supervisor with a heartbeat** — FEATURE — value 5 — effort M — risk med — category: supervisor
  Why: a session-hosted drive dies with the terminal (T-2900 closes its orphans, but the drive itself still depends on one). A systemd user timer/service restarts it, holds a sleep inhibitor, and a separate dead-man check raises a flag the morning card shows.
  Done when: killing the terminal mid-night leaves the queue progressing and the heartbeat file fresh within 5 minutes.

- **Cap trigger loops with a causal-depth and self-cause filter** — SECURITY — value 4 — effort S — risk low — category: trigger safety
  Why: self-triggering (file, CI, issue) can fire on Sampo's own commits and comments. Assumption: nothing yet marks provenance. Every event carries a chain id; events caused by Sampo's own writes are dropped, depth >2 parks the trigger.
  Done when: a fixture where a triggered task edits a watched file fires exactly once, and depth-3 is refused with a logged reason.

- **Fence trigger payloads as untrusted data under a lower grant tier** — SECURITY — value 5 — effort M — risk low — category: injection
  Why: issue and CI text from the forge becomes a brief, and bypass-mode unattended runs make that a path from a stranger's comment to shell. Trigger-born sessions run with a stricter Ward profile, payload quoted not instructed, maintainer-label/author allowlist required for issues.
  Done when: a planted issue saying "run curl … | sh" results in a Ward block and no task acceptance text containing it.

- **Route background volume to a free local lane with Exam-verified output** — FEATURE — value 5 — effort L — risk med — category: local models
  Why: the user wants local models used "without limit for background volume". Triage, grooming, CI-red diagnosis and draft fixes go to the local model first; each result is marked unwitnessed until the task's own Exam passes, and frontier tokens only spent on local failure. Use qwen3.8-27b first per the steer, batching by resident model (a swap costs ~3 min).
  Done when: a night with 20 queued items runs at most one model swap, and each local result carries an Exam verdict.

- **Repair malformed tool calls before they fail, per model** — FIX — value 4 — effort M — risk low — category: tool reliability
  Why: failed tool calls are up by half. A signature bank of failed-call shapes (by model, tool) drives a deterministic rewrite pass and a per-model reliability score used for routing; a circuit breaker stops a session repeating the same failing call.
  Done when: replaying the recorded failed calls shows at least a stated share repaired, and a loop of 3 identical failures trips the breaker.

- **Write the trigger ledger that answers "why did this start?"** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: unattended starts the user didn't initiate need provenance. Every fire-or-skip decision logs the event, rule, reason, and appears as a stamp on the task and in the morning card.
  Done when: `sampo why T-id` prints the triggering event for any self-started task.

- **Dry-run any trigger against 30 days of history before arming** — FEATURE — value 4 — effort M — risk low — category: triggers
  Why: no evidence a trigger rule is sane before it runs while the user sleeps. Replay shows "would have fired N times, storm at X", with debounce and per-night budget suggested.
  Done when: `sampo trigger replay RULE --days 30` outputs counts and the highest burst, without starting any work.

- **Gate unattended landing behind a morning-diff and auto-revert tag** — SECURITY — value 4 — effort M — risk med — category: landing
  Why: the standing push grant plus overnight work means unwitnessed commits reach main. Night commits land on a branch with a tag; fm ship of them waits for the user's one key, or reverts if a morning check goes red.
  Done when: a night-produced commit is not on main until acknowledged, and `sampo unwind --since` restores the pre-night ref.

- **Wild: Hold a nightly stall drill before the real work starts** — FIX — wild — value 3 — effort M — risk low — category: chaos
  Why: assumption: stops come from rare states. At bedtime a scratch lane is killed, an endpoint stalled and disk filled in a sandbox; the night only arms if the drive recovers each.
  Done when: a failing drill blocks `night start` and names the unrecovered fault.

- **Wild: Dead-man switch that pauses all triggers if nobody reads the morning card for three days** — SECURITY — wild — value 3 — effort S — risk low — category: autonomy governor
  Why: autonomy should decay when unwitnessed. Triggers step down the ladder (push → branch → draft → observe).
  Done when: three unread mornings flip the autonomy level, and reading the card restores it.

- **Wild: Fire a "dream shift" that mines closed tasks and pushbacks for the follow-up the user would have asked** — FEATURE — wild — value 4 — effort L — risk med — category: anticipation
  Why: the user repeatedly corrects after the fact (wildness, names, "stop asking"). Local models draft the predicted next ask as dormant briefs, graded next morning by whether the user typed something similar.
  Done when: the morning card lists drafts with a hit/miss count over the last 7 nights.

- **Wild: Plant a canary issue and red CI in a scratch repo each night** — FEATURE — wild — value 3 — effort M — risk low — category: trigger health
  Why: a silent trigger looks identical to "nothing to do". The synthetic event must produce a filed and closed task by dawn.
  Done when: a missing canary closure shows as "triggers blind" on the morning card.

Next question: Which stop causes in the real drive ledger (0→0.1) are still unclassified, and does any of them occur only with no session attached?
Next question: What is the user's actual bedtime-to-wake window and GPU contention pattern, so the night plan can yield the endpoint to them?
