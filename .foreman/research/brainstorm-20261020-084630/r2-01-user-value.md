# Brainstorm — lens: user value

- **Audit the whole setup's per-turn context cost** — FEATURE — value 4 — effort M — risk low — category: cost
  Why: the pack shows the skill listing is re-paid after every compaction, and the long session ran about 60% dearer. Only Foreman's own share is metered, and the user's CLAUDE.md, other plugins' skills, MCP tool schemas and memory files cost the same every turn. Assumption: `claude -p` or the transcript usage fields let `fm` attribute bytes by source.
  Done when: `fm context` prints bytes per source (Foreman, CLAUDE.md, memory, other plugins, MCP), ranks them, and names the three cheapest removals, checked on a fixture setup with a known 5 KB MCP schema.

- **Explain why a turn was expensive** — FEATURE — value 4 — effort M — risk low — category: cost
  Why: Foreman is +10–14% on small tasks and about 60% on the long session, and "bookkeeping calls, hook notes" is a guess. A per-turn breakdown from transcript usage (cache write vs read, output tokens, tool-result bytes, hook-note bytes) would turn the guess into a measurement for any session, with or without Foreman.
  Done when: `fm why-expensive <session>` lists the top 5 costly turns with token and dollar attribution, and its totals match the transcript's summed usage within 1%.

- **Overlap slow proofs with the next step** — PERFORMANCE — value 4 — effort M — risk med — category: speed
  Why: time is a headline metric (Haiku +13%) and each verify command blocks the turn. Assumption: Claude Code's background Bash can carry the verify command while the model starts the next independent sub-request. The step closes only when the proof lands, so the discipline is unchanged.
  Done when: on the long-session case with a verify command slowed to 20s, wall time drops by at least 25% and every hidden test still passes.

- **Make bare "continue" a priced contract** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: the user's latest request is literally "continue, super improve foreman…". A bare "continue" carries no scope, so it can quietly spend a lot. Assumption: the active task, queue and last stop reason are enough to derive a concrete plan.
  Done when: a bare "continue" prompt makes Foreman state in at most 5 lines what it will do next and a rough cost ceiling before the first edit, covered by a fixture-session test.

- **Derive default ceremony per task kind from duel results** — FEATURE — value 4 — effort M — risk med — category: cost
  Why: both sides pass all small specified tasks while Foreman costs more, yet Foreman wins on multi-request sessions and safety. The data already says where ceremony pays. Today the defaults are a hunch, so a table keyed by kind and size could set them.
  Done when: a checked-in `ceremony.json` generated from bench results sets per-kind defaults, and rerunning the Haiku duel with it cuts small-task overhead below +5% while the long-session pass rate stays 6/6.

- **Re-inject only what a compaction dropped** — FEATURE — value 4 — effort M — risk med — category: long sessions
  Why: the sessions where Foreman wins are compaction sessions, and the post-compaction note currently carries a fixed block. Compare a pre-compaction fact snapshot (open sub-requests, failing proof, touched files) against what the summary retained, and re-inject only the missing items, which is cheaper and more targeted.
  Done when: in a forced-compaction test with a summary that omits one open sub-request, exactly that sub-request is re-injected and nothing already present is repeated.

- **Read Claude Code's native memory as a steer source** — FEATURE — value 3 — effort S — risk low — category: learning
  Why: Claude Code now keeps its own feedback memories, and Foreman keeps separate steers, so corrections are stored twice and can contradict. Assumption: memory files have stable frontmatter with a feedback type.
  Done when: a `feedback` memory file appears in `fm steers` with its source marked, and an entry present in both stores is shown once.

- **Show a pre-spend estimate for unattended runs** — FEATURE — value 3 — effort M — risk low — category: cost
  Why: the constraints say usage matters, and the marathon runs across 7 compactions. A dollar range from similar closed tasks, shown before an unattended start, would let the user decline or lower the cap.
  Done when: `fm run` prints a low–high estimate with the basis (N similar closed tasks) and refuses to start without a cap when the estimate exceeds the setting.

- **Wild: Usage thermostat** — FEATURE — value 4 — effort L — risk med — category: cost
  Why: wild. The user wants Foreman to run long without burning their usage. They set a weekly target, and Foreman raises or lowers ceremony, model choice and compaction window to hit it, then reports what it traded away.
  Done when: in a simulated week with a 50% target, the controller keeps projected spend within ±10% of target while the guard rules stay unchanged.

- **Wild: Stop-loss against the median close** — FEATURE — value 3 — effort S — risk low — category: cost
  Why: wild. Stop a session and ask the user when its spend per closed task passes 3× the median for that task kind. This catches runaway loops by cost rather than by detecting a loop shape.
  Done when: a replayed runaway session halts at the threshold with a one-line message naming the median and the current spend.

- **Wild: A "beat-the-baseline" receipt on every close** — FEATURE — value 3 — effort M — risk med — category: trust
  Why: wild. Every claim on the site must be measured, but a user feels their own sessions, not the page. Estimate from recorded tokens what plain Claude Code would have cost for this task and print "Foreman +X% / caught Y" at close. Assumption: a calibrated per-kind multiplier from the duel is honest enough to label as an estimate.
  Done when: the close line shows the estimate flagged "est.", and the multiplier comes from a results file rather than a hard-coded number.

- **Wild: Publish a "when not to use Foreman" page that the tool itself follows** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: wild. The measured result is that small specified tasks gain nothing and cost more. Saying so plainly builds trust, and `fm should-i` can apply the same rule to the user's next prompt.
  Done when: the page is generated from the results file, and `fm should-i "<prompt>"` answers full, light or off with the table row it used.
