# Brainstorm — lens: local models without limit

- **Run a free-lane overnight queue on the local model** — FEATURE — value 5 — effort M — risk med — category: background volume
  Why: the user wants "local models used without limit for background volume" and overnight progress unattended. Triggers currently have no executor that costs nothing. Assumption: the local endpoint stays up overnight.
  Done when: a trigger-born task with `lane: free` runs to a closed-or-parked state on qwen3.8-27b with zero frontier tokens, and the ledger shows 0 frontier spend for it.

- **Verify every local result with the task's own Exam, mark it unwitnessed** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: local output is cheap but untrusted; the Exam-per-brief machinery exists (T-2894 and the earlier Exam ideas). Assumption: most queued tasks already carry a runnable Exam.
  Done when: a local-made commit cannot reach `fm ship` unless its Exam ran and passed, and the morning card lists it as "unwitnessed" until a human or a stronger model reads it.

- **Repair malformed tool calls locally before they fail** — FIX — value 4 — effort S — risk low — category: tool reliability
  Why: failed tool calls rose by half in this generation's top gaps, and T-2893 shows local models needing request extras and empty-reply handling. A deterministic repair pass (JSON fixes, path normalisation, argument-name aliases) costs no tokens.
  Done when: a replay bank of 50 recorded failed calls shows at least 60% now succeed after repair, with no false repair that changes intent.

- **Race N local attempts per task, keep the first Exam-passing one** — FEATURE — value 4 — effort M — risk low — category: best-of-N
  Why: local tokens are free, so volume substitutes for quality; the Exam supplies the judge. Assumption: the endpoint tolerates 2–4 concurrent requests (unmeasured; the drive's own concurrency knee is unknown).
  Done when: on 10 closed held-out tasks, best-of-4 on the local model passes strictly more Exams than best-of-1, with the pass counts printed.

- **Batch the night's local work by resident model** — PERFORMANCE — value 4 — effort S — risk low — category: scheduling
  Why: the pack says a llama-swap switch costs about 3 minutes and isn't detectable, and the steer says use qwen3.8-27b first and switch to the MoE only late. A queue ordered by model avoids repeated swaps.
  Done when: a night with mixed-model jobs shows at most one switch in the ledger, and the plan names the model order up front.

- **Triage every trigger event with a local gate before it can start work** — SECURITY — value 4 — effort M — risk med — category: triggers
  Why: file, CI and issue events are untrusted text; a local classifier (the Jev/Jeff decision backends from T-2887) can say "act / ignore / ask" at zero cost. Fixed fallback is "ask" if the model is down.
  Done when: a planted issue containing an injected instruction is classified "ignore" or "ask" in a replay, and every verdict is logged with its reason.

- **Fall back to the local model while a usage limit is waited out** — FEATURE — value 4 — effort M — risk med — category: drive continuity
  Why: the standing rule says to wait out real limits; waiting wastes the night. Local work on Exam-checkable tasks can continue inside the wait. Assumption: the drive can switch executors per task.
  Done when: a simulated usage-limit wait produces at least one closed local task whose Exam passed, and the frontier work resumes unchanged afterwards.

- **Score tool-call reliability per model and route by it** — PERFORMANCE — value 3 — effort M — risk low — category: routing
  Why: failed calls are up by half, and Louhi already runs Smith on a local model (T-2908). Per-model, per-tool failure rates tell the router which model gets which job.
  Done when: `sampo louhi models` prints a failure rate per model and tool, and the router skips a model whose rate exceeds a set threshold for that tool.

- **Yield the endpoint the moment the user shows up** — FEATURE — value 3 — effort S — risk low — category: resource courtesy
  Why: unlimited background volume competes with the user's own interactive use of the same GPU. Assumption: the user shares one endpoint.
  Done when: starting an interactive session pauses queued local jobs within 10 seconds, and they resume on session end.

- **Wild: Run a dream shift that mines closed tasks for the follow-up the user would have asked** — FEATURE — value 3 — effort M — risk low — category: anticipation
  Why: wild — idle local hours can draft dormant briefs from the user's repeated phrasings ("also do it for X", "stop asking me"). Drafts are filed dormant, never started.
  Done when: after a night, the inbox holds dormant drafts marked "predicted, not asked", and a week later the share the user accepted is reported.

- **Wild: Fork a rival Sampo the local model keeps** — FEATURE — value 3 — effort L — risk med — category: self-improvement
  Why: wild — a local model proposes self-edits on a throwaway clone every night at no cost; only edits that pass the held-out exam reach the user as a morning digest. Nothing merges unattended.
  Done when: a night produces at least one candidate patch with its exam result, and the digest shows it with a one-key revert.

- **Wild: Fire local volume when power is cheap** — FEATURE — value 2 — effort M — risk low — category: scheduling
  Why: wild — "without limit" has an electricity cost the user never mentioned; scheduling heavy runs into cheap tariff or solar-surplus hours makes unlimited honest. Assumption: the user can supply a tariff or hours file.
  Done when: with a tariff file set, the night plan places heavy jobs in the cheapest window and the receipt prints kWh estimated.

- **Compile one-sentence triggers into rules with a local model** — FEATURE — value 3 — effort M — risk med — category: triggers
  Why: the user shouldn't hand-write trigger files. The compiled rule is shown as a diff and dry-run against 30 days of history before arming.
  Done when: "when CI goes red on main, diagnose it" yields a valid trigger spec plus a replay count of how often it would have fired.

Next question: What is the real concurrency and uptime profile of the llama-swap endpoint (parallel requests, model-swap cost, hours it's down), since every local-volume idea depends on it?

Next question: Which background tasks have a runnable Exam today, and what share of the deferred backlog could the free lane close without any frontier review?
