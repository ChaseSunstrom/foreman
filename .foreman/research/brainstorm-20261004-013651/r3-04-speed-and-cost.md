# Brainstorm — lens: speed and cost

- **Make children's token spend predictable with a pre-call estimate and overrun abort** — FEATURE — value 4 — effort M — risk low — category: cost control
  Why: fm budget caps spend after the fact ($6/command, 4M tokens/day); the user wants subagents used freely but not eating "a crap ton of tokens". assumption: children report usage only on completion, so a runaway child is only caught afterwards.
  Done when: a child given a 20k-token estimate that streams past 2× is stopped, and the ledger records "aborted at overrun" with the partial output kept.

- **Make a drive turn do one hook-run's worth of work by coalescing PostToolUse hooks** — PERFORMANCE — value 3 — effort M — risk med — category: hook latency
  Why: hook p95 is 35 ms over 888 runs, which is fine per call but multiplied by every tool call in a drive. assumption: several hooks fire on the same event and each re-reads state files.
  Done when: a replayed 200-call session reads each state file once per event (counted by a test shim) and verdicts are byte-identical to before.

- **Gate reviewer cost on a changed-hunk fingerprint, so re-review after a fix covers only the delta** — PERFORMANCE — value 4 — effort M — risk med — category: review cost
  Why: every review pass found 3–7 real issues, so a fix cycle follows, and a re-review of the whole diff likely repeats the first pass's cost. assumption: re-reviews currently get the full diff.
  Done when: after a one-hunk fix, the second reviewer prompt contains only the changed hunk plus the prior findings, and is ≥50% smaller by token count.

- **Add a stable-prefix ordering for all child prompts, so provider prompt caching actually hits** — PERFORMANCE — value 4 — effort S — risk low — category: prompt caching
  Why: "share one prefix across sibling children" is already listed, but nothing checks that cache hits happen. This is the verification half: order the pack so static parts come first and log cache-read tokens per child.
  Done when: fm cost shows a cache-hit ratio per child kind, and a test fails if a volatile field (timestamp, task id) appears before the static prefix.

- **Replace the always-on rules with a measured per-turn token bill and a "rules that fired" trim** — PERFORMANCE — value 3 — effort M — risk med — category: always-on cost
  Why: the rules file is capped at 120 lines / 6000 chars and paid on every turn of every session. Pruning "rules that never earn their tokens" is listed for bench, but a cheap offline version needs no bench: count which rules a hook or nudge ever cited.
  Done when: fm cost prints per-rule citation counts over the last 30 days and flags rules with zero citations and a token cost.

- **Pipeline the gate runner so independent checks run in parallel with a load-aware width** — PERFORMANCE — value 4 — effort M — risk med — category: gate speed
  Why: 704 tests take ~30 s, and one flaky class failed under heavy load. Parallelism helps speed, and the load-aware width fixes the flake cause in the same change. assumption: gates currently run serially.
  Done when: fm check on a suite with 3 independent gates takes close to the slowest gate's time, and the width drops to 1 when the 1-minute load average exceeds the core count.

- **Wild: Run the reviewer speculatively while the last step is still being implemented** — FEATURE — value 3 — effort L — risk high — category: latency hiding
  Why: 18 drive turns ended just to wait on a reviewer, so review latency is on the critical path. Start review on the stable files at step N−1 and fold in the last step's delta afterward; discard if the diff shifts too much. Wild.
  Done when: on a 3-step task, the final review wall-clock after the last edit is under half of the unspeculated baseline, and the findings match a full review on a recorded diff.

- **Wild: Learn a per-user "cost of being wrong" curve to pick tier S/M/L from history** — FEATURE — value 3 — effort M — risk low — category: tier calibration
  Why: tiers drive review, gate and child spend. Tasks that escalated mid-task or closed first time give labeled data on whether the initial tier was right. assumption: tier and outcome are both in the ledger. Wild.
  Done when: fm cost reports tier over-/under-assignment rates, and a replay shows a suggested tier matching actual escalations on ≥70% of past tasks.

- **Wild: Make a "token-free path" for read-only questions by answering from fm's own indexes** — FEATURE — value 3 — effort M — risk low — category: zero-token answers
  Why: recall, the repo map, impact and tour are all local and deterministic, yet the model is still asked "where is X used / what did we decide". Expose them as one `fm ask` that returns a cited local answer and only falls through to the model on a miss. Wild.
  Done when: five scripted lookups (decision, symbol users, last failure, lesson, file owner) return correct answers with zero child tokens, and a miss reports "no local answer".

- **Make the spend ledger attribute cost to the brief step and the pipeline stage** — FEATURE — value 4 — effort S — risk low — category: cost visibility
  Why: the user cares that subagents don't eat tokens, but a total or per-command number doesn't show whether intake, research, review or ideas is the hog. assumption: the ledger has per-command rows but no step or stage key.
  Done when: fm cost --by stage prints a table whose rows sum to the daily total, and the UI spend card shows the top stage.

- **Cut cold-start cost with a session-start digest cached by state hash** — PERFORMANCE — value 2 — effort S — risk low — category: startup
  Why: each session or resume re-derives state, next hints and drive position. assumption: this is recomputed on every start, and the output is identical when state hasn't changed.
  Done when: a second `fm next` with unchanged state is served from the cache (a counter shows no re-derivation) and any state write invalidates it.
