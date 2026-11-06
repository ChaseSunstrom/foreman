# Brainstorm — lens: capability map

- **Interview the vague goal before planning** — FEATURE — value 5 — effort M — risk low — category: intake
  Why: the request is to turn a vague goal into a plan, and no listed idea asks the user anything. Best-in-class planners (Kiro, Spec Kit) run a clarify step. Assumption: users answer short questions with stated defaults.
  Done when: a one-line goal yields at most 5 questions, each with a default of the form "assuming X unless you say", and planning proceeds on those defaults without blocking. Each answer is recorded as a provenance-tagged row.

- **Tier rows Must/Should/Could so "shippable" differs from "complete"** — FEATURE — value 5 — effort M — risk med — category: scope
  Why: the pack has a cut list and a gold-plating cutoff, but one binary done. MoSCoW tiers let a goal reach "shippable" (all Musts proven) early and keep running toward "complete".
  Done when: a goal with unmet Coulds reports `shippable`, and the Stop hook allows a stop only when the tier is explicit in the verdict.

- **Add spike rows that end in a decision, not code** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: assumptions have probes, but unknowns like "which approach" have no row type (Shape Up and XP use time-boxed spikes). Blocked items T-0335 and T-0336 are really unanswered questions.
  Done when: a spike row closes only when `fm decide` is filed with its evidence, and its box expiring forces a keep/cut prompt.

- **Rank rows on a hill: figuring out vs making it happen** — FEATURE — value 4 — effort M — risk low — category: progress
  Why: percent-done hides unknown-heavy rows (Basecamp hill charts). Assumption: rows can carry an uphill/downhill flag set by the first passing probe.
  Done when: `fm goal` lists rows with a hill position, and a row that stays uphill past its box is flagged.

- **Groom the "Later from T-07xx" bundles into closable rows or expire them** — CLEAN — value 4 — effort M — risk low — category: backlog
  Why: T-0788 to T-0799 are single deferred tasks holding 7 to 29 ideas each (T-0799 holds 29). A task of 29 ideas can never be finished, so it is never done.
  Done when: each bundle either splits into rows with a done-when or is closed with a recorded reason. No open task names "N ideas" without a decomposition.

- **Give every blocked task a probe that unblocks it itself** — FEATURE — value 4 — effort S — risk low — category: blockers
  Why: T-0325 (needs libappindicator), T-0418 and T-0352 wait on outside facts, and nothing re-checks them. Typed waits exist, but no probe command does the re-check.
  Done when: a blocked task stores a probe command, `fm doctor` re-runs it, and a passing probe moves the task to open with a ledger event.

- **Set an appetite per goal and propose cuts at 80%** — FEATURE — value 4 — effort M — risk med — category: scope
  Why: the pack sizes DRIVE_MAX and reserves budget, but the user never states how much they will spend. Shape Up fixes the time and varies the scope. The environment shows a $35 budget, so spend is a real constraint.
  Done when: `fm goal open --appetite 2d` records it, and at 80% burn the planner proposes a ranked cut list and waits for a yes.

- **Show cost per goal and per criterion** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: cost appears only as a cap sizer. Linear and Jira show spend against progress. Assumption: token and dollar data is already logged per session.
  Done when: the goal card shows dollars spent, the cost of the last closed criterion, and a warning when burn runs ahead of closure.

- **Work backward from a deadline** — FEATURE — value 3 — effort M — risk med — category: schedule
  Why: nothing in the pack handles "by Friday". Assumption: users state dates in plain words.
  Done when: `--due` back-schedules rows against the critical path and flags the goal "will miss" with the cheapest cut that fixes it.

- **Detect two open goals colliding on the same files or rows** — FEATURE — value 4 — effort M — risk low — category: multi-goal
  Why: goal stacks and resume routing exist, but no idea compares goals' footprints. Gen-0 work like Genesis and Initiative edits shared files (the site, MASTER, README).
  Done when: opening a goal whose predicted footprint overlaps another open goal prints the overlap and asks for an order.

- **Ship plan archetypes for recurring goal kinds** — FEATURE — value 3 — effort M — risk low — category: templates
  Why: the Genesis briefs share a shape (map, find, prove, surfaces, MASTER, README, CHANGELOG). Templates for new CLI verb, migration and release would seed the contents list. Learned priors come from misses, not from known recipes.
  Done when: `fm goal open --kind verb` pre-fills rows from the archetype and tags them, and an edit that drops an archetype row needs a reason.

- **Write an automatic retro when a goal finishes** — FEATURE — value 3 — effort S — risk low — category: learning
  Why: autopsies exist for non-finishes and a timelapse exists for replay, but a finished goal gets no plan-versus-actual summary.
  Done when: closing a goal writes a one-page retro (planned rows, added rows, cuts, surprises, cost) and links it from the goal card.

- **Wild: Mine peers' changelogs for the features that arrived after v1** — FEATURE — value 3 — effort M — risk med — category: references
  Why: the pack teardown idea needs a grant and cites sources, but changelogs are free, public data on what real products added later. Assumption: the goal names peer products.
  Done when: for a goal naming 3 peers, the plan gains cited "day-2" rows drawn from their release notes, each marked with its source URL.

- **Wild: Keep a user-twin that answers clarifying questions between legs** — FEATURE — value 4 — effort L — risk high — category: autonomy
  Why: runs last days, and the user's recorded steers carry their preferences. A twin could answer a blocking question provisionally and queue it for later confirmation. Assumption: steer history is enough to predict answers.
  Done when: a question raised while the user is away gets a twin answer tagged `provisional`, work continues, and the user's later confirm or reversal is scored as the twin's hit rate.

- **Wild: Check the ecosystem for each row before planning to build it** — FEATURE — value 3 — effort M — risk med — category: reuse
  Why: the pack searches the repo for each row, but never asks whether an installed package or tool already does it.
  Done when: each Must row shows a "reuse found or none" line from installed tools and lockfiles, and a found match turns the row into an integrate step.

Next question: Which kinds of vague goal ("make it faster", "polish it", "make it best in class") need a different plan shape, and what does a plan for each look like?
Next question: Who besides the user ever reads the plan (a teammate, a reviewer, a future agent), and what do they need that the user's copy lacks?
