# Brainstorm — lens: approaches

- **Mark hooks that run inside Foreman's own children** — PERFORMANCE — value 4 — effort S — risk low — category: hook latency
  Why: round 1 made `claude -p` children budgeted and non-driving, but each child still pays every Python hook per tool call. Approach: set one env sentinel (`FM_CHILD=1`) that makes each hook exit after a single env check, with the guard kept active. Trade-off: child tool calls lose advisory hints, which tool-less brainstormers never needed.
  Done when: a scripted child making 20 tool calls spends under 5 ms of hook time in total, and the guard still blocks a seeded dangerous command.

- **Gate bench on a replayed concurrent hook trace** — PERFORMANCE — value 4 — effort M — risk low — category: bench
  Why: bench already judges by CPU time under load, but it runs 20 solo iterations. Approach: record 10 minutes of real hook payloads and replay them at 4x concurrency, reporting p95 per event. Trade-off: this needs payload scrubbing and a fixture refresh policy. A solo bench misses contention, such as many lanes sharing the state lock. Assumption: contention exists with lanes plus children.
  Done when: `fm doctor` prints a per-event p95 under replay, and a deliberately slowed hook fails the gate.

- **Reuse native agent memory instead of injecting lessons into briefs** — FEATURE — value 3 — effort M — risk med — category: agents
  Why: round 1 already set effort and maxTurns in agent frontmatter, so frontmatter is the natural next home for per-role knowledge. Assumption: the installed Claude Code supports a persistent per-agent memory scope; `fm doctor` would verify that. Trade-off: this duplicates recall and splits the source of truth, but it removes the lesson tokens from every brief.
  Done when: a reviewer agent run in a fresh session recalls a seeded role lesson with no lesson text in its brief, and the brief shrinks measurably.

- **Collapse the fm-* specialists into one agent with a role argument, and let bench decide** — CLEAN — value 3 — effort M — risk med — category: agents
  Why: the do-less approach. Fewer agent files means fewer frontmatter fields to keep in sync with Claude Code's schema, which is the drift `fm doctor` now polices. Trade-off: it loses per-role tool allowlists and model pins, and it is only worth doing if bench shows no quality loss.
  Done when: a bench A/B of the merged agent against the specialists shows pass rate within the variance floor, or the idea is closed as dropped with that evidence.

- **Hold a round-close checklist as data, so "recursive" is a procedure** — FEATURE — value 4 — effort M — risk low — category: recursion
  Why: the user said "recursively improve" means finish the tasks, review what shipped, and brainstorm again, repeatedly. Today that is conversational. Approach: a small file (`round.json`) listing round-close steps (tick the board, audit the diff, measure claimed savings, brainstorm, queue). `fm next` reads it when the queue drains. Trade-off: it adds a file, but it gives the loop a resumable step pointer after `/compact`.
  Done when: killing a session mid-round and resuming lands on the exact remaining round step.

- **Brainstorm only the delta: feed children round N's shipped diff plus open friction, not the full idea pile** — PERFORMANCE — value 4 — effort M — risk med — category: brainstorm cost
  Why: this pack carries thousands of prior idea lines, and round 3 still produces near-repeats. Approach: send each child the shipped-items list, drops with their reasons, and only cluster names for the idea pile. Trade-off: it risks re-proposals, so pair it with a mechanical post-filter against cluster names.
  Done when: the pack is under a set token budget, and a replay of round 2 through it yields no more duplicates than the full-pile run.

- **Add a spend-per-verified-task line to every round receipt** — FEATURE — value 3 — effort S — risk low — category: cost proof
  Why: round 1 claimed about 1.04M tokens saved per 30 days, but that figure is an estimate. Approach: log actual tokens and USD per closed task from the child-budget path. Trade-off: it only covers Foreman-spawned children, not the main session.
  Done when: closing a task prints its real token and dollar cost, and a round receipt sums them.

- **Test the arming of every plugin monitor against the real CLI at install time** — FIX — value 4 — effort S — risk low — category: liveness
  Why: the mail monitor's arming in a live session is flagged as unverified. Approach: the installer spawns a throwaway `claude -p` session, waits for the monitor's first heartbeat file, and records pass or fail. Trade-off: it costs one tiny child call at install.
  Done when: install output states "monitor armed: yes/no", and breaking `monitors.json` makes it say no.

- **Wild: Run a hook "diet week" shadow where each hook is disabled in turn on a throwaway lane** — PERFORMANCE — value 3 — effort L — risk med — category: ablation
  Why: assumption: some hooks never change an outcome, and nobody has measured which. Approach: for each hook, replay the same bench cases without it and compare pass rate and time. Trade-off: it is expensive and noisy.
  Done when: a table lists each hook with its latency cost and measured catch rate, and at least one hook is flagged as safe to retire or demote.

- **Wild: Let a night lane write the next round's brief from what the user said "etc." about** — FEATURE — value 4 — effort M — risk med — category: unattended
  Why: the user's own words trail off with "etc. etc. etc.", which reads as a standing mandate to keep improving. Approach: an unattended lane drafts a round-N+1 brief and stops at "ask", with a preset budget and no code edits. Trade-off: the user may not want to be drafted for.
  Done when: the morning shows a drafted brief in the queue as captured, with nothing executed.

- **Wild: Hedge each slow read-only child with a second cheaper attempt and keep the first answer back** — PERFORMANCE — value 3 — effort M — risk med — category: agents
  Why: assumption: scouts and recon children sometimes stall on one model while a cheaper one answers fast. Approach: start a haiku twin after a delay and take the first valid return, cancelling the other. Trade-off: it costs extra tokens on the slow tail only.
  Done when: a seeded stalled child is replaced by the twin's answer within the delay plus the twin's runtime, with cost logged for both.

- **Wild: Make the idea pile queryable by `fm ideas ask "did we cover X"` so the user and children stop re-reading it** — FEATURE — value 3 — effort M — risk low — category: ideation
  Why: the pack's idea list is far larger than any reader can scan. Approach: substring and cluster lookup over the stored catalogue, returning the status (shipped, dropped with reason, deferred). Trade-off: it is only useful if children can call it, and this lens runs tool-less, so it works for the main thread and the user.
  Done when: asking about a shipped idea returns its task id, and asking about an unknown one returns "not covered".
