# Brainstorm — lens: Claude Code native integration

- **Fill agent-wait time with the next independent step** — FEATURE — value 5 — effort M — risk med — category: orchestration
  Why: T-0758 ("make sure it doesnt sit idle"). Agent calls are background by default, and Stop-hook blocking or polling are the only waits Foreman has now. Assumption: ListAgents can report which agents are still running.
  Done when: with one background reviewer outstanding and a queued task that touches no overlapping files, the ledger shows that task's step starting before the reviewer returns, and a test pins this.

- **Coalesce wakes with a debounce window** — PERFORMANCE — value 4 — effort S — risk low — category: tokens
  Why: Monitor and ScheduleWakeup ideas above would turn every output line into a model turn, and each turn re-reads the context. Assumption: a wake costs a full turn.
  Done when: a command emitting 200 lines over 20s produces at most 2 wakes with a digest, and `fm doctor` shows the wake count and cost per session.

- **Gate the apply-back of worktree and remote lane results** — SECURITY — value 5 — effort M — risk low — category: lanes
  Why: lanes already use isolation "worktree", and "remote" is available. A lane's diff is merged back with the same trust as local edits. Assumption: nothing checks a returned diff against the footprint the plan declared.
  Done when: a fixture lane that adds a `.github/workflows` file, a hook entry or a settings change outside its declared footprint is refused at merge with the offending paths named.

- **Sweep and expire everything Foreman publishes** — SECURITY — value 4 — effort M — risk low — category: egress
  Why: Artifact pages are outward-facing and may stay cached or indexed after deletion (system guidance). The pile has projection and redaction ideas but nothing on retention. Assumption: a cron or `fm` command can list and delete Artifacts and ArtifactData.
  Done when: a published page past its TTL is deleted by the sweeper, `fm publish ls` lists live pages with their age, and a task close removes its own page.

- **Propagate `fm pause` to cloud routines and session crons** — SECURITY — value 4 — effort M — risk med — category: control
  Why: "pause holds every launcher" shipped in 1.2.18, but RemoteTrigger routines, `/schedule` and CronCreate run outside the local process. Adopting them (several ideas above) would open a path that pause can't reach. Assumption: those entries can be listed and disabled programmatically.
  Done when: with one cron and one routine registered, `fm pause` disables both, `fm resume` re-enables only those it paused, and a registry test fails if any scheduler is created without being recorded.

- **Cap subagent returns and spill the rest to a file** — PERFORMANCE — value 4 — effort S — risk low — category: tokens
  Why: the existing idea rejects hollow returns, but long returns land whole in the main context. Assumption: SubagentStop can see or reject the return text.
  Done when: a reviewer returning 4,000 words is bounced once to produce a ≤300-word summary plus a file path, and `fm doctor` reports main-thread tokens saved per role.

- **Use ReportFindings dismissals as reviewer-precision labels** — FEATURE — value 3 — effort M — risk med — category: learning
  Why: the ideas above adopt ReportFindings for display, but a finding the user dismisses or accepts in the host UI is a free label, and T-0035 and "reviewer precision" (1.2.27) need exactly those. Assumption: dismissal state is readable from the CLI side.
  Done when: after a review round with one dismissed finding, the reviewer's precision in `fm bench` changes and links back to that finding.

- **Audit every child session's guard coverage** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: Foreman runs bypass mode, and it launches `claude -p` children, Agent lanes, and (soon) remote lanes. Assumption: no single record shows which of them ran with the guard hook loaded.
  Done when: `fm doctor` lists each child launched in the last 7 days with its permission mode and whether the guard fired at least once, and fails on a bypass child with the guard absent.

- **Plant decoy skills and agents as prompt-injection tripwires** — SECURITY — wild — value 3 — effort S — risk low — category: tripwire
  Why: honeytokens are in the pile, but invoking a tool or skill is a signal tokens can't give. Assumption: a decoy named like a high-value action (`deploy-prod`, `export-secrets`) is never invoked legitimately.
  Done when: invoking the decoy blocks the call, writes a ledger alert naming the preceding tool results as suspects, and pushes one notification.

- **Share lessons between sessions in real time** — FEATURE — wild — value 3 — effort M — risk med — category: fleet
  Why: the failure fingerprint index and SendMessage both exist or are proposed, but nothing connects them across the user's other live sessions. Assumption: ListAgents reaches other local sessions.
  Done when: when session B's failure matches a fingerprint with a recorded lesson, session A receives that lesson as a message, labelled as peer-sourced and untrusted, within 10s in a two-session test.

- **Question a cold reader after every compaction** — FIX — wild — value 4 — effort M — risk low — category: resume
  Why: the user asked for exact-step resume after /compact, and current checks (injected resume text, "test that resume survives compaction") never test whether the model understood. Assumption: a haiku Agent can answer from only the post-compact context.
  Done when: after a compaction the cold agent states the current step and the next action, a mismatch with STATE re-injects the handoff, and the mismatch rate is logged.

- **Run a cheap mirror session that rewrites the user's rambles into briefs** — FEATURE — wild — value 3 — effort M — risk med — category: intake
  Why: T-0756, T-0757 and T-0759 are fragments of one rambling message, all captured as separate S tasks. The earlier ideas (glue fragments, reorder) don't say who does it before the main thread burns tokens. Assumption: UserPromptSubmit can hand a draft brief to a background haiku Agent without delaying the turn.
  Done when: a 4-clause message yields one milestone task with the clauses as ordered steps, within the hook latency gate in `bench_hooks.py`.
