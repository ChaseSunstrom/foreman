# Brainstorm — lens: capability map

- **Meter Foreman's token share per session** — FEATURE — value 5 — effort M — risk low — category: cost
  Why: the long session costs $0.095 vs $0.059 because bookkeeping calls and hook notes grow context. T-1231 has no per-source breakdown to aim at.
  Done when: `fm cost --session` prints tokens by source (fm calls, hook notes, skill listing, compaction re-sends). A test over a recorded transcript sums to the transcript total within 2%.

- **Auto-prove criteria from observed runs** — FEATURE — value 5 — effort M — risk med — category: cost
  Why: bookkeeping calls are the stated cause of the +60% long-session cost. A PostToolUse hook can see the exact verify command exit 0 and record the proof with no model call. Assumption: the verify command matches the Bash input textually.
  Done when: running an AC's verify command in Bash marks it proved with no `fm task prove` call. A forced-compaction long-session case shows fewer fm calls with the same hidden-test pass rate.

- **Collapse the 15 skills into one router stub** — PERFORMANCE — value 4 — effort M — risk med — category: compaction
  Why: Claude Code 2.1.304 re-sends the whole skill list after every compaction, and Foreman's skills are ~3,200 of ~9,600 chars. Seven compactions in the marathon means paying that seven times.
  Done when: Foreman's skill descriptions total ≤ 600 chars. A CI budget check fails above that. Every skill is still reachable by name in an e2e test.

- **Compact at task boundaries with focus instructions** — FEATURE — value 4 — effort M — risk med — category: compaction
  Why: compaction is currently forced mid-task, and the misses of plain Claude Code were written after compactions. Compacting between tasks loses the least. Assumption: a hook or the drive can trigger or request it, and where it can't, the drive stops at the boundary and prints the instruction.
  Done when: on the 8-request long session with the context window at 40k, ≥ 90% of compactions happen at a task close. Hidden tests still pass 6 of 6.

- **Tune the auto-compact window per workload** — PERFORMANCE — value 3 — effort S — risk low — category: cost
  Why: 2.1.304 accepts `CLAUDE_CODE_AUTO_COMPACT_WINDOW` with k/M suffixes and warns when out of range. Foreman compacts more often because its context grows faster.
  Done when: `fm doctor` reports the current window and warns on out-of-range values. A Haiku long-session run at two windows publishes cost and pass counts on the Benchmarks page.

- **Rehearse compaction without a model** — FIX — value 4 — effort S — risk low — category: reliability
  Why: T-1231's work on request text surviving compaction is checked only through paid benchmarks. The hooks themselves are deterministic.
  Done when: a free test replays PreCompact and post-compact SessionStart on a synthetic state. It asserts the injected note holds the active request verbatim, excludes finished ones, and stays under N chars.

- **Gate approvals through `decider: "person"`** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: a 2.1.304 mod `tool.check` can require that only a person approves, and the call is refused where nobody can be asked. That is the same idea as the chat-approval self-grant fix, enforced by the host. Assumption: foreman-ui can reach it.
  Done when: with foreman-ui installed, a guard "ask" in `claude -p` is refused and in an interactive session needs the dialog. A test shows `-p yes` can't resolve it.

- **Pin a headless-drive test for the Stop change** — FIX — value 3 — effort S — risk low — category: compatibility
  Why: 2.1.304 stops a plugin from keeping a headless run alive past Stop or `--max-turns` by spawning subagents. Foreman was last adapted to 2.1.301.
  Done when: an e2e test drives a queue under `claude -p --max-turns N` and asserts it ends at the cap with a "queue not drained, resume with X" receipt.

- **Generate site figures from the results files** — CLEAN — value 3 — effort S — risk low — category: docs
  Why: T-1246 notes the prose numbers are hard-coded, and the rule is that every claim is measured. The cost figure already moved from +29% to +14%.
  Done when: the build fills each prose figure from the bench JSON. CI fails if a figure has no source.

- **Apply the stored theme before first paint** — FIX — value 2 — effort S — risk low — category: site
  Why: T-1244 says `site.js` applies the theme after load, which flashes the wrong theme.
  Done when: an inline head script sets the theme and a headless screenshot at load shows no flash.

- **Wild: Run the safety corpus on every Claude Code release** — FEATURE — value 4 — effort M — risk low — category: benchmarks
  Why: wild; the 24-dangerous / 25-everyday corpus is the strongest measured claim. Guard payloads can drift per release.
  Done when: a scheduled job runs the corpus against the newest Claude Code and fails if blocks drop below 20 of 24 or any everyday command is stopped. The result updates a badge on the Benchmarks page.

- **Wild: Print a "Foreman tax receipt" at session end** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild; the user cares about not burning usage. A line like "Foreman cost 11% of this session; it blocked 2 commands and re-proved 3 criteria" makes the tradeoff visible.
  Done when: the Stop summary shows the share from the meter plus counts of blocks and proofs, and it is absent on sessions under 5 turns.

- **Wild: Fork the lens fan-out from one cached prefix** — PERFORMANCE — value 3 — effort M — risk med — category: cost
  Why: wild; fork subagents are on by default in `claude -p` in 2.1.304, and the lens runs share the same pack. Assumption: forks share the prompt cache.
  Done when: a 10-lens `fm ideas` run reports the same total input tokens at a measurably lower cost, with the result files unchanged.

- **Wild: A/B the compaction instruction text on replayed sessions** — FEATURE — value 3 — effort L — risk med — category: benchmarks
  Why: wild; the one factor behind the long-session misses is what survives compaction. Today it is tuned by hand.
  Done when: `fm bench compact` forks a recorded 40k-token session, compacts it under two note variants on Haiku with a dollar cap, and reports the hidden-test pass counts for each.
