# Brainstorm — lens: usage efficiency

- **Run autofixers on a gate failure before any model call** — PERFORMANCE — value 4 — effort S — risk low — category: gate cost
  Why: assumption: many gate failures (formatting, import order, lint) are mechanically fixable, yet each one currently reaches a paid model turn. The pack lists "Run mechanical tasks with zero model calls" but not the autofix step inside a failing gate.
  Done when: a fixture repo whose only failure is a lint-autofixable error goes green via `fm check` with zero model requests logged in the journal.

- **Undo a failed edit by replaying its stored inverse patch** — FEATURE — value 4 — effort M — risk low — category: undo cost
  Why: assumption: when a fix is rejected, the model currently re-reads files and re-derives the revert. The pack already has "Undo a whole run in one command" and "Checkpoint every tool call into an undo ledger", but not a zero-token revert path.
  Done when: rejecting a task's last edit restores the tree byte-for-byte using the stored inverse patch, and the journal records zero model calls for the revert.

- **Switch models only at a compaction boundary** — FEATURE — value 4 — effort M — risk med — category: cache reuse
  Why: assumption: escalating the model mid-task rebuilds the prompt cache on every switch, which costs more than the escalation saves. The pack has "Escalate the model only when the proof fails" and "Warn when an edit busts the prompt cache" but no rule that ties switches to a cache-safe point.
  Done when: in a replay of a task that escalates twice, both switches happen at compaction events and the cache-miss count stays at or below the single-switch baseline.

- **Send a failing gate's log as its first assertion plus a line count** — PERFORMANCE — value 4 — effort S — risk low — category: tool output
  Why: assumption: failing gate logs are long, and the model reads all of them to find one assertion. The pack has "Trim search and tool output to a byte budget" but nothing specific to gate failures.
  Done when: a gate failure with a 3,000-line log is injected into the pack at under 1 KB and still names the failing test and its assertion line.

- **Route reads along the import graph's shortest path to the edit site** — PERFORMANCE — value 3 — effort M — risk med — category: read cost
  Why: assumption: a model reads files in breadth-first guesses. The pack has "Read one symbol, not the whole file" and "Use cheap local grep before any model read", but no path-based read plan.
  Done when: on the fixture repo, the files read before the first edit drop by at least 40% against the current search order, with the same edit landing.

- **Set each reply's length budget from the weekly headroom left** — FEATURE — value 3 — effort S — risk low — category: reply length
  Why: assumption: replies cost the same whether the week has spare budget or is nearly spent. The pack has "Shorten the receipt when the user's messages are short" but nothing that scales reply length to the remaining budget.
  Done when: with headroom above 50%, the reply budget stays at the default; below 10%, the reply budget is cut to the stated floor, and both values are logged.

- **Count calls per useful edit and flag read-only turns** — FEATURE — value 3 — effort S — risk low — category: usage metrics
  Why: evidence from the pack: "fm cost" and "Count the human decisions per closed task" exist, but no measure of how many reads a task needs before its first edit.
  Done when: `fm cost <task>` prints reads-before-first-edit and flags any task above a set threshold.

- **Flag any single reply that costs more than twice its task's median** — FEATURE — value 3 — effort S — risk low — category: cost outliers
  Why: assumption: a few expensive replies drive most of the spend. The pack has "Predict a task's token cost before it runs" but not per-reply outlier detection during a run.
  Done when: a synthetic task with one reply at 3x the median triggers one journal event naming the reply and its cause, and a normal task triggers none.

- **Wild: a yield curve for context, pricing each added token against its gain** — FEATURE — value 4 — effort L — risk med — category: context pricing
  Why: wild. Each piece of context gets a marginal price, and Foreman stops adding a section when its measured gain on the duel falls below that price. It treats the context window like a market with a clearing price, not a fixed budget.
  Done when: on the duel fixture, the pack is cut to the sections whose removal lowers the pass rate, and the token count drops with no loss in pass rate.

- **Wild: a metronome that spaces model calls to the rate limit's beat** — PERFORMANCE — value 3 — effort M — risk low — category: rate-limit smoothing
  Why: wild. Bursts of parallel calls trip limits, and each retry spends tokens again. A fixed beat paces calls so bursts never reach the limit and the retry tax goes to zero.
  Done when: a 50-call burst on a rate-limited mock produces zero retries and finishes within 10% of the unthrottled time.
