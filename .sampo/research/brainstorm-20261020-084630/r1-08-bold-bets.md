# Brainstorm — lens: bold bets

- **Infer bookkeeping from tool results** — FEATURE — value 5 — effort L — risk med — category: cost
  Why: Foreman costs ~60% more in the long session because "bookkeeping calls, hook notes" grow context and force extra compactions. T-1231 is still deferred.
  Done when: a PostToolUse hook closes criteria, steps and `prove` records from the commands the model already ran, and the long-session duel shows zero `fm task` calls from the model for a plain S task with hidden tests still passing.

- **Compact at task seams, not mid-task** — FEATURE — value 5 — effort M — risk med — category: long sessions
  Why: plain Claude Code's misses came after compactions, and Foreman compacts more often. `CLAUDE_CODE_AUTO_COMPACT_WINDOW` now takes k/M suffixes. Assumption: the drive can trigger or time compaction right after a close.
  Done when: in the 8-request long session, at least 80% of compactions begin within one turn of a task close, and compaction count or cost is lower than the 1.2.40 baseline.

- **Replace 15 skills with one router skill** — PERFORMANCE — value 4 — effort M — risk low — category: context cost
  Why: 3,200 of the ~9,600 listing chars are Foreman's skills, re-sent after every compaction as of Claude Code 2.1.304. The router's description would be under 400 chars and the bodies load on demand.
  Done when: a measured session shows the post-compaction skill listing at least 2,500 chars smaller, and the skill-trigger evals still pass.

- **Add a "ask a person" tier to the guard** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: 2.1.304 lets a mod's `tool.check` answer `decider: "person"`, which only the dialog or a host callback can approve. Today the guard's 4 "saved first" and borderline cases can only block or allow. The guard must never weaken, so this tier only turns some allows into asks.
  Done when: `fm guard try` shows an "ask" verdict for at least one command class, the same command is refused where nobody can be asked, and the 24 dangerous and 25 everyday benchmark commands keep their current outcomes or stricter.

- **Make headless drive survive the new Stop rule** — FIX — value 4 — effort S — risk med — category: compatibility
  Why: a plugin can no longer keep a `claude -p` run going past Stop or `--max-turns` by spawning subagents. Foreman was last adapted to 2.1.301 and its unattended drive and done-gate may depend on that behaviour. Assumption: the drive does depend on it.
  Done when: an e2e test on 2.1.304 shows `fm run` continuing a queue across turns through an outer loop, with no Stop-hook subagent trick, and `fm doctor` flags a Claude Code version newer than the last tested one.

- **Scout through fork subagents for cache reuse** — PERFORMANCE — value 3 — effort S — risk low — category: cost
  Why: fork subagents are on by default in `claude -p` as of 2.1.304, and the demo already uses scout subagents. Forks share the parent's cached prefix, so scouts should cost less than cold ones.
  Done when: the duel logs show a scout run with a measured cache-read share above X% and lower cost than a cold subagent for the same lookup.

- **Show a live "Foreman tax" meter** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: the user wants it cheaper but there is no per-session number for tokens Foreman added (hook notes, skill listing, bookkeeping turns). Assumption: injections can be counted in the hook layer.
  Done when: the pane and `fm usage` show injected tokens and bookkeeping turns per session, and the figure matches the duel's cost delta within 10%.

- **Add a fresh-eyes pass after every compaction** — FEATURE — value 4 — effort M — risk med — category: long sessions
  Why: in the marathon Foreman "found and fixed 3 things through 7 compactions" after the asked work was done. The user wants new ideas after compactions without burning usage.
  Done when: after a compaction, a capped Haiku reviewer reads only the diff and the request text and files findings as captured tasks, and a marathon run shows at least one real finding per three compactions at under a set dollar cap.

- **Generate benchmark prose and figures from result files** — FIX — value 3 — effort S — risk low — category: docs
  Why: T-1246 says the site's prose figures are hard-coded, and every claim on the site must be measured. T-1244 (theme applied only after load) could be fixed in the same pass with an inline head script.
  Done when: changing a results JSON and rebuilding changes every number in the Benchmarks page prose, and CI fails if a hard-coded figure disagrees with the data.

- **Wild: Let the spec suite grow itself by mutation-checked generation** — FEATURE — value 4 — effort L — risk med — category: benchmarks
  Why: T-0866 and T-0867 are deferred for lack of cases, and hand-written suites are slow to build. wild. A cheap model drafts tasks plus hidden tests, and a task counts only if the tests fail on the seed and pass on a reference solution.
  Done when: `fm bench` gains N generated tasks that all pass the red-on-seed, green-on-reference check, and a duel runs on them.

- **Wild: Schedule the queue around the prompt-cache window** — PERFORMANCE — value 3 — effort M — risk med — category: cost
  Why: wild. Unattended runs pay cold-cache costs after idle gaps. The drive could batch related tasks inside the cache TTL, or delay a start until related work is ready. Assumption: the cache TTL is observable from usage fields.
  Done when: an unattended run of 6 queued tasks shows a higher cache-read share than the same run started task by task, with equal pass rate.

- **Wild: Run a perpetual marathon on the Pages site** — FEATURE — value 3 — effort M — risk med — category: proof
  Why: the user wants Foreman visibly better and cheaper, and the marathon already works on Haiku with dollar caps. wild. A scheduled capped run publishes a rolling scoreboard of Foreman vs plain Claude Code.
  Done when: the Benchmarks page lists dated marathon results from a scheduled job, each with spend under its cap, and a regression turns the badge red.

- **Wild: Ship a "Foreman Lite" session that turns itself on only when a failure is predicted** — FEATURE — value 4 — effort L — risk high — category: cost
  Why: on small fully specified tasks both sides pass everything and Foreman costs 10–14% more. wild. Start with only the guard active and add planning and proof ceremony when the task looks hard, shows a failed check, or crosses a compaction.
  Done when: on the spec suite, Lite matches plain Claude Code cost within 3% on easy tasks, and on the round-2 and long-session suites it keeps Foreman's pass rate.
