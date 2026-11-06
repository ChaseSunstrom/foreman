# Brainstorm — lens: user value

- **Add a per-stage token ledger with tier budgets**: PERFORMANCE, value 5, effort M, risk low
  Why: the user says one session burned 20% of their weekly usage, and `fm cost` only totals per task, not per stage. Assumption: transcripts give enough usage data to attribute tokens to stages. Frontmatter gets a `budget` by tier, and the per-turn note adds one line at 80%.
  Done when: `fm cost --stages` prints tokens per stage for a finished task, and a task over budget gets exactly one ≤400-char warning note.

- **Detect thrash and force a hypothesis**: FEATURE, value 5, effort M, risk med
  Why: nothing notices the same file edited 5×, or the same test failing with different errors. PostToolUse counters per file and failure signature would trigger a Next note: "state a hypothesis, run the cheapest experiment". A step at 5× its estimate would trigger it too.
  Done when: a replayed fixture of 5 edits to one file emits one note, and a normal 3-step flow emits none.

- **Log ruled-out approaches into handoffs**: FEATURE, value 4, effort S, risk low
  Why: `fm run` and resumed sessions get only the brief and resume note, so failed approaches get retried. Thrash triggers and failed verifies would append to a "tried/ruled out" section of the brief, and resume and `fm run` would inject ≤300 chars of it.
  Done when: a resumed session's start context includes a prior ruled-out entry, and the section is capped and deduplicated.

- **Split L tasks into dependent children**: FEATURE, value 4, effort L, risk med
  Why: there is one plan per task and no automatic decomposition. `fm split` would create S/M child briefs with `depends_on`, and the queue order and `fm focus` would respect the dependencies.
  Done when: an L brief with 6 steps splits into children, and `fm focus` refuses a child whose dependency isn't done.

- **Show a weekly digest at SessionStart**: FEATURE, value 4, effort S, risk low
  Why: the user never runs commands and has no view of what Foreman did, cost, or learned. A markdown digest of tasks done, tokens, lessons, and repeats would be written once per week, with a one-line pointer at SessionStart. Its size would be counted against the 2,000-char budget.
  Done when: the first session after 7 days shows the pointer, the digest file lists tasks, cost and lessons, and later sessions stay silent.

- **Slim skills into core and on-demand sections**: PERFORMANCE, value 4, effort M, risk med
  Why: skills are long markdown, and injected bytes per session are unmeasured. Assumption: most skill runs need under half of the text. Measure injected chars per session, split each skill into core and lazy sections, and check with the eval cases.
  Done when: median skill chars loaded per run drop ≥30% and the existing evals still pass.

- **Require before/after numbers for PERF tasks**: FEATURE, value 3, effort M, risk low
  Why: verification is exit codes only, with no perf or size baselines. `fm check --baseline` would record timing and size before the change, and `fm task done` on a PERF task would need an after-measurement, flagging a >20% regression elsewhere.
  Done when: a PERF task can't be completed without a recorded before/after pair, and a seeded 30% slowdown is flagged.
