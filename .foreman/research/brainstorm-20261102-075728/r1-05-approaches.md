# Brainstorm — lens: approaches

- **Estimate plan completeness by capture-recapture** — FEATURE — value 5 — effort M — risk low — category: planning
  Why: assumption: the pack has no way to say "the plan is complete" beyond the sweep's cell checks. Two independent tool-less children list the best-in-class capabilities with no sight of each other. Foreman counts the overlap and applies the Lincoln-Petersen estimate to get the number of capabilities still unnamed. A low overlap means "plan not yet saturated", whatever the row count says.
  Done when: `fm goal plan` prints "N named, ~M estimated total, overlap X%" and refuses to call the plan complete below a set overlap, shown on a fixture with a planted 30-item truth list.

- **Plan with consensus core and disputed fringe** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: the request is a vague goal; the existing ideas fuzz it only to test the planner. Here the planner runs 3 tool-less paraphrase-readings, takes the rows every reading produces as the core plan, and puts rows only some readings produce into a short "you decide" list. Trade-off: 3x planning tokens, but it replaces open-ended questions with one pick-list.
  Done when: a vague goal yields two sections, core and disputed, and each disputed row names which readings produced it.

- **Harvest capability lists from rivals already on the machine** — FEATURE — value 3 — effort S — risk low — category: local-first
  Why: assumption: tools in the goal's space are often installed locally. Parse their `--help`, man pages, shell completions and config schemas into a free, offline "what the best tools expose" list, then diff it against the plan, with no network or model call.
  Done when: against a fixture with a fake rival CLI, the plan gains a row for each flag group the plan lacked.

- **Keep plan rows as `FM-GOAL:` markers in the code** — FEATURE — value 3 — effort M — risk med — category: persistence
  Why: the standing ask is to survive days, crashes and compaction. A marker in the file it concerns survives any state-dir loss, rides git, and `grep` is the whole read path. Trade-off: it pollutes source and doesn't fit non-code rows, so it is a mirror for code rows, not the store.
  Done when: deleting the goal state dir and running `fm goal adopt` rebuilds the open code rows from markers alone.

- **Mirror the plan into the host's native todo list at every resume** — FEATURE — value 3 — effort S — risk med — category: harness reuse
  Why: assumption: Claude Code and the others keep their own task list across compaction. Reusing it makes the host re-surface the plan for free. Foreman stays the source of truth and the mirror is rewritten from it on each resume, so drift can't accumulate.
  Done when: after a forced compaction, the first model turn lists the same open rows as `fm goal` without a Foreman call.

- **Order rows by pairwise tournament** — FEATURE — value 3 — effort M — risk low — category: ordering
  Why: single-shot ordering by one model is the weakest part of any plan. A cheap model answers "which of these two first, given this goal?" over a sampled set of pairs, and a Bradley-Terry fit gives the order plus a confidence. Close calls go to the topological order instead.
  Done when: the same 20-row plan ordered twice gives the same top 5, and a dependency edge always beats the tournament.

- **Regenerate the plan from goal text and repo diff, caching by hash** — CLEAN — value 3 — effort M — risk med — category: persistence
  Why: assumption: stored plans rot when the repo moves under a multi-day goal. Store only the goal, the oracle and verdicts keyed by tree hash. Re-derive the open rows on resume, and reuse a cached row while its cited paths are unchanged. Trade-off: planning cost per resume, offset by the cache.
  Done when: changing a file a done row cites turns that row stale on the next resume, and an untouched row stays cached.

- **Do less: make a goal a saved query over the existing task queue** — CLEAN — value 4 — effort S — risk low — category: simplicity
  Why: Foreman already has tasks with DONE-WHEN. A goal becomes a label and a "done" is "no open task carries it and every closed one's proof still passes". No new store, no new verbs. Trade-off: no plan-level history, and growth becomes visible only as new tasks.
  Done when: `fm goal done?` exits 0 or 1 from the task ledger alone, with a typed reason for 1.

- **Run an auction for the last mile** — FEATURE — value 3 — effort M — risk med — category: finish
  Why: "done rather than merely stopped" needs a finder that wants to say not-done. Several cheap lanes each bid one concrete missing thing with a runnable probe, and a bid whose probe fails is a new row. The goal closes only after a round with zero valid bids. Trade-off: it costs lane tokens on every close attempt, so cap it at one round per day.
  Done when: a fixture goal with one planted gap gets a failing-probe bid, and the closing round returns empty after the gap is fixed.

- **Wild: Read the plan back as a user-journey screenplay** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. A child writes the finished product as a 12-step "day in the life" script. Each step must map to a plan row or become one. Steps nobody can map show the gap the way a user would feel it.
  Done when: every script step links to a row id, and an unmapped step is printed as a gap.

- **Wild: Let the goal retire itself on a decay curve** — FEATURE — value 2 — effort S — risk med — category: finish
  Why: wild. Each row's proof carries a half-life, so "done" is a posterior that fades as the repo churns around it. A finished goal quietly turns "probably still done" amber instead of staying green forever.
  Done when: a done goal whose cited files changed 50 commits ago prints "done, 3 rows aging" at resume.

- **Wild: Fork two independent builders on the same plan and diff the product** — FEATURE — value 3 — effort L — risk high — category: verification
  Why: wild. Two cheap models build the top 5 rows in separate worktrees. Where their behaviour differs on the acceptance probes, the row was under-specified, and that disagreement is the plan defect to fix before the real build.
  Done when: a planted ambiguous row produces different outputs from the two forks and is flagged "underspecified".

- **Wild: Price each row in the user's own minutes and cut at a budget line** — FEATURE — value 3 — effort M — risk low — category: scope
  Why: wild. Estimate cost per row from past closed tasks of the same kind, draw a "this fits Friday" cut line, and show what falls below it. Scope growth then reads as "+40 minutes", not "+3 rows".
  Done when: the plan shows a cumulative estimate per row from ledger medians and a cut line at a stated budget.

Next question: Which "done" verdict has Foreman never seen reopened, and what would a reopen of it look like?
Next question: Does the user ever read a plan longer than one screen, and what do they do with the rows beyond it?
