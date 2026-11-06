# Brainstorm — lens: deepen: cost

- **Build a per-turn cost ledger that attributes every token to its source** — FEATURE — value 5 — effort M — risk low — category: cost-attribution
  Why: the long-session premium (+60%, $0.095 vs $0.059) is attributed only loosely to "bookkeeping calls, hook notes"; T-1231 is deferred for lack of a breakdown. Many listed ideas (meter, explain, decompose, audit) are one mechanism.
  Done when: `fm cost --session SID` prints tokens split into skills listing, hook notes, fm stdout, subagent reports, and model work, and the parts sum to the transcript's billed total within 2%.

- **Make the ledger the optimizer's objective: auto-ablate each injection and keep what pays for itself** — FEATURE — value 5 — effort L — risk med — category: cost-optimization
  Why: assumption: each injection (note, skill, preamble) has a measurable cost and a measurable effect on hidden-test pass rate. The duel and long-session harnesses already produce both numbers; combining them gives a keep/drop verdict per injection.
  Done when: `fm bench ablate` runs the long-session suite on Haiku with one injection removed at a time under a dollar cap, and prints cost delta against pass-rate delta for each.

- **Collapse the 15 skills into one router and shrink the re-sent listing** — CLEAN — value 4 — effort M — risk med — category: context-tax
  Why: the main session notes that Foreman's 15 skills are ~3,200 of ~9,600 listing characters, re-sent after every compaction in 2.1.304. Foreman compacts more than plain Claude Code, so it pays this tax more often.
  Done when: the listing contribution drops below 800 chars, and the skill-trigger eval shows no loss in correct activations.

- **Set the compaction window from a measured cost curve, not a guess** — PERFORMANCE — value 4 — effort M — risk low — category: compaction
  Why: `CLAUDE_CODE_AUTO_COMPACT_WINDOW` now accepts k/M suffixes. The long session forced compaction at 40k, and Foreman's faster context growth means it compacts often. Foreman's own docs/site would need a figure for the cheapest window.
  Done when: a Haiku sweep over at least 4 window sizes on the long-session suite is published, and `fm doctor` suggests the winner with the measured cost and pass rate.

- **Replace the hook-note stream with deltas: say nothing the context already shows** — PERFORMANCE — value 4 — effort M — risk low — category: injection
  Why: the pack names hook notes as a driver of context growth. Notes repeating the active task, steps or the same warning every turn are pure repeat cost.
  Done when: replaying a recorded long session shows at least 30% fewer injected characters, with the guard's refusals unchanged byte for byte.

- **Add a ceremony profile per task kind and model, chosen from duel data** — FEATURE — value 4 — effort M — risk med — category: adaptive-ceremony
  Why: on small fully specified tasks both sides pass everything and Foreman only adds cost (+10–14%), while on long sessions it wins on correctness. One fixed ritual is wrong for one of the two.
  Done when: S tasks on Haiku run in a lean profile (no plan note, criteria-only close) and the duel shows cost within +5% of plain Claude Code with the same pass rate; long sessions keep the full profile.

- **Wild: A usage thermostat that throttles ceremony as the user's budget burns** — FEATURE — value 4 — effort M — risk med — category: budget-control
  Why: wild. The user says "without burning their usage". The ledger knows spend per session; a dollar or percent-of-window cap could step down from full to lean to guard-only, and say so once.
  Done when: with `fm budget set 2.00`, a session approaching the cap switches to the lean profile, prints one line announcing it, and the guard hook still blocks the dangerous-command set.

- **Wild: Fork the lens fan-out and scout calls from one cached prefix** — PERFORMANCE — value 3 — effort M — risk med — category: cache-reuse
  Why: wild. Fork subagents are on by default in `claude -p` in 2.1.304, and brainstorm lenses all share the same context pack. If forks share the parent's cached prefix, N lenses cost about one prefix write plus N small tails, instead of N full reads.
  Done when: a 6-lens `fm ideas` run reports cache-read tokens at least 5x its cache-write tokens, and total cost drops by a measured fraction against separate `claude -p` children.

- **Park idle waits inside the cache window and spend them on compaction** — PERFORMANCE — value 3 — effort M — risk low — category: cache-timing
  Why: the unattended queue waits between tasks, and a cold cache costs a full re-read of the context. The new idle compaction row in `/config` suggests the host can compact while nothing is happening.
  Done when: in a recorded unattended run, no turn follows a gap longer than the cache TTL without a preceding compaction or a logged reason, and cache-miss spend falls against the baseline.

- **Wild: Offload bookkeeping to a Haiku sidecar that writes `fm` state from the transcript** — FEATURE — value 4 — effort L — risk high — category: bookkeeping
  Why: wild. Bookkeeping calls (task, step, criterion updates) occupy the main model's turns and grow its context. A sidecar reading tool results could infer the updates. Risk: wrong inferences corrupt the proof ledger, so every inferred proof would have to be backed by a command that actually ran.
  Done when: on the long-session suite, main-model `fm` calls drop by at least 50% and the hidden-test pass rate stays 6 of 6.

- **Squeeze tool output before it enters context, and stub superseded reads** — PERFORMANCE — value 4 — effort L — risk med — category: output-compaction
  Why: context growth drives the long-session premium. Test logs, repeated file reads and large `fm` outputs are the obvious bulk. T-0828 (compact output rollout) is deferred and still waiting on shadow mode.
  Done when: in shadow mode, the suite shows a measured token cut from tool results, and the fetch-back rate (the model re-asking for what was cut) stays under 5%.

- **Gate per-turn context tax and cost regressions in CI** — CLEAN — value 3 — effort S — risk low — category: regression-guard
  Why: the +29% to +14% Haiku improvement could silently regress with any new hook note. CI already has CPU-time bounds, so a token-count bound fits the same pattern.
  Done when: CI fails if the skill listing, preamble or standard hook notes grow past a committed budget, and the failure names the offending source.

- **Wild: Publish a live "Foreman vs plain" cost receipt at the end of every session** — FEATURE — value 3 — effort M — risk low — category: transparency
  Why: wild. Every site claim must be measured, and the user wants to show the improvement. A session-end line saying "Foreman used X tokens, Y% of the session, and prevented Z refused commands" turns the ledger into evidence and a trust signal.
  Done when: closing a session prints a receipt whose numbers match `fm cost`, and it makes no estimate where there is no measurement.

- **Test a terse-output style and lower effort on bookkeeping turns** — PERFORMANCE — value 3 — effort S — risk low — category: output-tokens
  Why: output tokens cost more than input tokens, and Foreman's turns are heavy on short status text and fixed-format `fm` calls. It is cheap to measure on Haiku.
  Done when: an A/B on the spec suite shows output tokens fall by a stated percentage with no pass-rate change, and the result is kept or rejected in the benchmarks page by the numbers.
