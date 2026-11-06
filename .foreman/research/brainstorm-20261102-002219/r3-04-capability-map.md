# Brainstorm — lens: capability map

- **Add a goal risk register with recovery playbooks** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: the pack shows pre-mortem and circuit-breaker ideas, but no per-goal list of "how this stalls" with a pre-written recovery for each. Jira and PMBOK risk registers do this. The user sees it on resume.
  Done when: a goal file has a `## Risks` block of at most 5 rows (trigger, recovery step), and a test shows `fm next` prints a row's recovery step once its trigger file or command fires.

- **Grow a goal regression suite as rows close** — FEATURE — value 5 — effort M — risk med — category: done-detection
  Why: assumption: "finish oracle" exists, but a row's proof is run once at close. Nothing re-runs earlier rows' checks, so a later row can silently break an earlier one while the goal still reads "finished".
  Done when: closing a row appends its probe to the goal's suite. A planted regression (row 2's probe broken by row 5) makes `fm goal check` fail and name row 2.

- **Bisect to the row that broke the oracle** — FIX — value 4 — effort M — risk low — category: done-detection
  Why: assumption: the commit-trailer idea (goal and row on every commit) exists, but nothing uses it for a regression found mid-goal. This pairs the trailers with the suite above.
  Done when: with a fixture goal where row 3's commit breaks a suite probe, `fm goal bisect` prints row 3 and its commit hash.

- **Sync a goal with GitHub milestones and Projects, both ways** — FEATURE — value 4 — effort L — risk med — category: integration
  Why: the pack exports to Spec Kit and Kiro files, but Linear, Jira and GitHub Projects are where teams already track a goal. Assumption: the user also works with others sometimes.
  Done when: a goal's rows map to milestone issues. Closing a row closes its issue, and an issue closed upstream marks the row "closed elsewhere, unverified" until its probe passes.

- **Assign a model tier to each row at plan time** — PERFORMANCE — value 4 — effort M — risk low — category: cost
  Why: Pillar 1 says to use the cheapest model that can. Nothing shows a per-row choice that is recorded and later corrected by outcomes.
  Done when: each row carries `tier:` and an estimate. After close, `fm goal retro` shows tier against reopen rate, and a row that reopened twice is bumped one tier on its next attempt.

- **Add a critical-chain buffer to the finish-date band** — FEATURE — value 3 — effort S — risk low — category: forecasting
  Why: a date band exists. Goldratt-style buffer consumption (a shared tail buffer eaten by overruns) gives the user a single "buffer left: 40%" number, which is easier to act on than a band.
  Done when: the goal page and status line show buffer percent, and a fixture where two rows overrun drops it by exactly their summed overrun.

- **Freeze scope before the final stretch** — FEATURE — value 3 — effort S — risk low — category: scope
  Why: a scope-growth ledger exists, but no state stops growth. Feature freezes in shipped products work because the change-request path is explicit.
  Done when: `fm goal freeze` makes `fm capture` of a new row ask "defer to next goal?". Only a must-fix row passes, and the freeze is logged in the finish card.

- **Lint each row against ready-to-build rules** — CLEAN — value 3 — effort S — risk low — category: planning
  Why: rows without probes are flagged, but not rows that are too big, vague or dependent on something unnamed. INVEST-style checks catch these before a lane burns tokens on them.
  Done when: a row estimated over one session, or lacking a verb and a noun, is flagged at `fm goal plan`, and a test covers 3 bad rows and 1 good one.

- **Tag open decisions with their last responsible moment** — FEATURE — value 4 — effort M — risk low — category: user-only items
  Why: user-only items are collected, but with no date by which each must be answered or it blocks work. The batching idea needs this to decide when to ask.
  Done when: each user-only item shows "blocks row N, ask by <date or row>", and `fm next` hides it until that moment unless the user opens the list.

- **Gate finish on goal-level budgets** — FEATURE — value 3 — effort M — risk med — category: quality
  Why: assumption: non-functional checklists exist per touched path, but a goal like "best-in-class" also needs targets such as install size, hook p95, page weight and contrast. Today they are checked row by row, if at all.
  Done when: a goal can declare `budget: hook_p95<=X` and finish refuses with the measured number when it is exceeded.

- **Wild: run a nightly resume canary on live goals** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: wild. Kill-and-resume drills exist as one-off ideas. A scheduled run would clone the goal state to a scratch directory with no session memory, ask a cheap child "what is next and what is blocked?", and score it against `fm next`. Rot in goal files then shows up before the user hits it.
  Done when: the night tick writes a canary score per goal, and a deliberately corrupted baton drops it below the bar and names the missing field.

- **Wild: inject a late requirement into drills** — FEATURE — value 3 — effort S — risk low — category: scope
  Why: wild. A drill adds a synthetic mid-goal requirement ("also support X") and checks that freeze, the scope ledger and replan each respond, instead of the plan quietly absorbing it.
  Done when: a fixture run shows the requirement ending up in the ledger, not in rows, once frozen.

- **Wild: write a retro that becomes next goal's first row** — FEATURE — value 3 — effort M — risk low — category: learning
  Why: wild. Estimate-vs-actual and shape libraries exist, but the retro itself is not turned into a plan row. Each finished goal would write its 3 worst surprises as a "Day-zero checks" row that seeds the next goal in the same repo.
  Done when: finishing goal A, then planning goal B in the same repo, yields a first row quoting A's surprises, each tied to A's evidence.

- **Plan goals that span repos with one shared oracle** — FEATURE — value 3 — effort L — risk high — category: scale
  Why: assumption: the user's other repos matter (prior-art search exists). Goal state keyed by repo identity cannot track a change that needs two repos to land together.
  Done when: a fixture goal across two scratch repos shows rows per repo and one finish check that fails until both pass.

Next question: Which of the 58 empty cells are the same capability seen from a different surface (goal page, status line, `fm next`), so one probe stamps several of them?
Next question: Does the user ever hand a goal to someone else's repo or tracker, and if so which tracker, since the sync item depends on it?
