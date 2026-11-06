# Brainstorm — lens: unspoken needs

- **Glue consecutive fragments into one intake item** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: T-0756 to T-0759 are four fragments of one thought ("also, the …", "and reordering of operations…", "can you make sure it doesnt sit idle"). Each was captured as its own task with a truncated title. Assumption: they arrived in a burst.
  Done when: replaying those four messages as a fixture produces one captured task with an imperative title, and the fragments appear as its clauses.

- **Reconcile STATE after a rewind, fork or resume branch** — FIX — value 4 — effort M — risk med — category: resume
  Why: assumption: CC's rewind, edit-and-resend and `--fork-session` move the conversation without firing Foreman's hooks. That would explain the step pointer drifting (T-0759).
  Done when: a test rewinds a transcript two turns and the next hook run moves the step pointer back, and the ledger notes the rewind.

- **Store results as typed records, not prose** — CLEAN — value 4 — effort M — risk med — category: correctness
  Why: two regressions in one release train came from regexes over our own strings: `✗ exit N` vs `exit N` (T-0750) and the track record missing failures from `fm task finish` (T-0749).
  Done when: no module regexes a result string. A grep gate fails the build if one appears, and the existing catch-rate tests pass against the records.

- **Gate on idle-while-queued minutes** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: the user said "make sure it doesnt sit idle like it is" (T-0758). It is a complaint with no number, so it can regress silently.
  Done when: `fm doctor` reports idle minutes with a non-empty queue over the last 7 days, computed from transcript timestamps. `bench` fails above a set threshold.

- **Guard native outward tools as egress** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the focus list says Artifact, PushNotification, SendMessage, RemoteTrigger and remote isolation are unused. Foreman runs in bypass mode. Adopting any of them sends content off the machine, and the guard doesn't classify them. Assumption: PreToolUse sees these tools.
  Done when: each tool call is judged by the guard, redacted and written to an egress ledger. A test that sends a planted secret through an Artifact publish is refused.

- **Title every session for the resume picker and terminal tab** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the user juggles sessions. Assumption: a hook can set the session title, and OSC title/progress escapes work in their terminal.
  Done when: `claude --resume` lists sessions as `T-0760 step 3/7 · running`, and the tmux window title follows the same string.

- **Narrow hooks natively so Python never spawns** — PERFORMANCE — value 3 — effort S — risk low — category: hooks
  Why: hooks are latency-gated by `bench_hooks.py`, and Foreman registers 14 events. Assumption: the installed CC supports hook matchers or `if` filters.
  Done when: `bench_hooks.py --runs 20` shows zero process spawns for tools Foreman ignores, and p50 drops.

- **Answer "can Foreman do X?" from the code** — FEATURE — value 3 — effort S — risk low — category: self-knowledge
  Why: T-0755 asks "can foreman spawn agents of lower models?" The answer is already yes (S-tier lanes pass `sonnet`, the scout runs on haiku). It was captured as work instead of answered.
  Done when: `fm can "spawn haiku agents"` returns yes/no with file:line citations, and intake answers questions that way instead of creating a task.

- **Scan scaffolding on tokens, not text** — CLEAN — value 3 — effort S — risk low — category: gates
  Why: the debug-scaffolding scan flagged CHANGELOG.md:10 and a string literal at test_execution.py:102. Both were closed as false positives.
  Done when: both cases are fixtures that pass, and a real `print(` added in code still fails.

- **Learn from conversation branches** (wild) — FEATURE — value 4 — effort M — risk med — category: learning
  Why: assumption: CC transcripts record forks when the user rewinds or edits and resends. The abandoned branch is a free negative example, and the resent prompt is the fix.
  Done when: `fm learn branches` lists at least 5 real (rejected, accepted) pairs from the user's transcripts. Each pair is a lesson candidate with a trial expiry.

- **Race approaches in forked sessions** (wild) — FEATURE — value 3 — effort M — risk med — category: orchestration
  Why: fresh `claude -p` children re-read everything. Assumption: a fork of the live session inherits context and reuses the cached prefix, so a race of 2–3 forks should cost less than cold children.
  Done when: a race of 2 forks on one task costs fewer input tokens than 2 cold children on the same task, and the winning fork's diff lands.

- **Make the resume picker the queue** (wild) — FEATURE — value 3 — effort M — risk med — category: surfaces
  Why: the user steers through CC itself rather than a separate board. Parked, titled sessions per queued task would make starting work a plain resume of one with its brief and plan already loaded. Assumption: this builds on the title idea above.
  Done when: the top 3 queued tasks each have a parked session, and resuming one opens at its first step with no re-planning.
