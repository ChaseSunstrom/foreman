# Brainstorm — lens: user value

Four of the earlier open questions fall to this lens. Three of the answers are my assumptions, since the pack carries no data on them.

- **Outputs the user would only miss after it cost a task:** the cut-rows list, the time breakdown and the cost of re-orienting after a resume. None of them shows up until the user has already lost a day.
- **Harness dependence:** I assume resume cells lean on Claude Code's hooks, and no probe in the pack runs elsewhere. Cells 1 and 4 below would show it.
- **Too little history to backtest:** the user's closed goals are probably too few to backtest per-goal predictors, so those cells need planted fixtures.
- **Unread outputs:** the cut-rows list and the time breakdown would have no reader unless a session path surfaces them. Each idea below names one.

Ideas, best first:

- **Count "where were we" messages after every resume** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: the capability promises carrying a goal over days, crashes and compactions, but nothing measures whether the user ever has to re-orient. The pack says "user words per landed task" is Anticipation's north star, and this is the Goal equivalent. Assumption: the first message after SessionStart is classifiable with cheap rules.
  Done when: a fixture with a kill-and-resume run logs one re-orientation count per resume. `fm doctor` prints the median across the last 10 goals.

- **Adopt the work already done as a goal** — FEATURE — value 4 — effort M — risk med — category: goal intake
  Why: assumption: much real work starts as ad hoc asks and only later turns out to be a goal. Today the plan, contents and resume protection exist only if the user asked for a goal first.
  Done when: after 3 or more related commits with no open goal, `fm next` offers one line. Accepting it files a goal whose contents rows cite those commits as already done.

- **Redo one row, not the goal** — FEATURE — value 4 — effort M — risk med — category: recovery
  Why: assumption: "that row came out wrong, redo it" is a common mid-goal ask. The pack lists a whole-goal gated revert but no row-level rewind.
  Done when: `fm goal redo ROW` reverts only that row's commits through a gated revert and marks dependent rows stale. The test shows the other rows' evidence untouched.

- **Check plan size against the ask** — FIX — value 4 — effort S — risk low — category: goal planning
  Why: assumption: a one-sentence vague goal that expands to 40 rows costs the user attention for rows they never wanted. The pack has "cap questions" and an MVP cut, but no proportionality check.
  Done when: a plan with more than N rows per 10 words of the ask, compared with the user's closed-goal median, prints "this plan is large for this ask; keep, trim to must-only, or split".

- **Break down where the goal's days went** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: multi-day goals stall on gates, usage limits, user-only items and compaction, and the user sees only "still open". The steers say limits are waited out, so that wait should be visible.
  Done when: the resume note shows a four-way split of wall time: building, waiting on a gate, waiting on a limit, waiting on the user. The split sums to the elapsed time.

- **Carry the cut rows into a successor goal** — FEATURE — value 3 — effort S — risk low — category: continuity
  Why: the pack covers a "not in this cut" list, but the cut rows currently end at the finish. The natural next ask is one the user shouldn't have to retype.
  Done when: finishing a goal with cut or deferred rows prints "next: goal 'X' with these 5 rows, say go". Saying go files it, with the rows' grounding lines carried over.

- **Verify the anti-goals** — FEATURE — value 3 — effort S — risk low — category: done-detection
  Why: users state what finished must not contain, such as no new dependency or no UI rewrite. Nothing checks absence. Assumption: these are stored only as prose today.
  Done when: a goal row "must not: new dependency" compiles to a check against the diff, and the finish oracle refuses while it fails.

- **Use a stored purpose line to break ties** — FEATURE — value 3 — effort S — risk low — category: unattended decisions
  Why: the steers say to decide rather than ask when unattended. The "why" the user gave for the goal is the best tie-break and is not stored as a first-class field. Assumption: the user states a why at intake often enough to matter.
  Done when: every `fm decide --kind costly` taken inside a goal records the purpose line it was weighed against.

- **Keep a per-goal question ledger** — FEATURE — value 3 — effort S — risk low — category: attention
  Why: the user pays in attention, and the pack has only an intake cap on questions. Nothing totals what a goal asked in all.
  Done when: the finish card says "asked you 4 questions, 3 predictable from your history", and the count is readable by the sweep.

- **Wild: run a pilot row to pick the model tier** — FEATURE — value 3 — effort M — risk med — category: cost
  Why: pillar 1 wants the cheapest model that can do each row, but the choice is guessed. Assumption: the first buildable row is representative.
  Done when: the first S or M row runs on the cheap tier and the next tier up. The goal records which passed its criterion, and later rows use the cheaper passing tier.

- **Wild: pre-grieve the rows likely to be cut** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: assumption: closed goals show a pattern in which kinds of rows get cut at the end. Showing that at plan time lets the user decide early instead of at the deadline.
  Done when: the plan view marks each could-row with a cut probability from the closed-goal history. A planted-history fixture reproduces the known cut pattern.

- **Wild: add a goal interest meter** — FEATURE — value 2 — effort S — risk low — category: motivation
  Why: assumption: a goal that sits for days gets harder to finish as main moves, but this isn't visible. The pack has plan rebase and drift detection, but no single number.
  Done when: resume shows "3 rows went stale since you left" with the commits that caused it. A test with a moved main shows the right count.

Next question: Which of the 58 cells has no user-typed message in the asked stream that it would have prevented, so it should be filled as `n/a` or `unreached` rather than as a capability?
Next question: Does the user act on any goal output today, such as a resume note, a finish card or a cut list, and which of those has never been read?
