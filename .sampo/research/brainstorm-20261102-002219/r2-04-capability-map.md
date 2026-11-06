# Brainstorm — lens: capability map

Lens: capability map. I compared Devin, Kiro and Spec Kit, Taskmaster, Linear projects, Shape Up/Basecamp, Jira epics, OpenHands and Manus-style todo files against the pack. The ideas below are capabilities the pack's list doesn't show.

- **Set an appetite and a circuit breaker per goal** — FEATURE — value 4 — effort M — risk low — category: scoping
  Why: assumption: the pack has budgets, cost forecasts and a "stuck" declaration, but no Shape Up-style appetite (time/cost the goal is worth) that forces a cut at expiry.
  Done when: a goal created with `--appetite 3d` auto-opens a "cut or extend?" card at 3 days with the cut list pre-drafted, and a test with a faked clock shows it fires once.

- **Order the plan riskiest-first with explicit spike rows** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: "ordered" is in gen-0 #4, but the pack shows only critical-path and wave ideas, not ordering by uncertainty. Assumption: late surprises are what make multi-day goals fail.
  Done when: for a fixture goal with one unknown-API row, the plan puts a time-boxed spike row before its dependents and marks them blocked-on-spike.

- **Draw a hill chart per goal row** — FEATURE — value 3 — effort M — risk low — category: progress
  Why: the pack has burn-up and a bar that can go backward, but nothing that separates "figuring it out" from "executing". That is what makes a stalled row visible before it is overdue.
  Done when: the Goal page shows each row on an uphill/downhill axis, and a row with no new evidence for N commits is flagged as stuck uphill.

- **Ship product-type definition-of-done templates** — FEATURE — value 5 — effort M — risk med — category: completeness
  Why: gen-0 says "what a finished, best-in-class version contains". Best-in-class tools start from a type template (CLI, web app, library, service) with install, docs, errors, upgrade and uninstall. Assumption: the decomposer currently invents this list from scratch each time.
  Done when: `fm goal new` on a fixture CLI repo proposes a checklist from the CLI template, and each row is tagged template-origin versus user-origin.

- **Learn estimate-versus-actual per row kind** — FEATURE — value 3 — effort M — risk low — category: estimation
  Why: assumption: the closed-task ledger has durations and costs, but the finish-date band probably uses flat priors. A per-kind calibration from past goals gives it honest widths.
  Done when: a backtest on closed goals shows the calibrated band covers at least 80% of actual finishes, with the bar stated before the run.

- **Enforce a WIP limit and a parked-goals shelf** — FEATURE — value 3 — effort S — risk low — category: portfolio
  Why: the pack has arbitration between two live goals. A Kanban-style cap with an explicit parked state and "why parked" is the missing piece.
  Done when: starting a goal over the cap refuses and offers `park OTHER`, and a parked goal's resume card names its parking reason.

- **Fork and merge goals** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: assumption: real goals split mid-flight ("auth turned out to be its own project"). The pack has scope-growth ledgers but no split or merge with row lineage.
  Done when: `fm goal split ROWS` creates a child goal, the parent keeps a pointer, and finish on the parent waits on the child.

- **Write a per-goal decision log that finish summarizes** — FEATURE — value 3 — effort S — risk low — category: memory
  Why: assumption: decisions made over days are lost to compaction. The pack has plan versions and rejected-approach ledgers, but not one per-goal chronology that finish quotes.
  Done when: the finish receipt lists each `fm decide` made under the goal, in order, with the row it affected.

- **Generate goal-level release notes from closed rows** — FEATURE — value 3 — effort S — risk low — category: reporting
  Why: Linear and Jira projects produce an update/changelog. The pack has a finish certificate and a postcard but no user-facing changelog drawn from the rows' evidence.
  Done when: finishing a fixture goal writes `GOAL-notes.md` whose every line links to a row and a commit.

- **Check the goal's external dependencies at plan time** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: assumption: keys, accounts, DNS and approvals block multi-day goals late. The pack's user-only list is built as they appear, not predicted when the plan is made.
  Done when: a plan touching a deploy row lists the user-only prerequisites up front, each tied to the row it blocks.

- **Wild: rehearse the goal on a throwaway skeleton** — FEATURE — value 3 — effort L — risk med — category: planning
  Why: wild. A cheap lane builds the thinnest end-to-end slice first, a tracer bullet, and the plan is reordered by what broke.
  Done when: for a fixture goal, the skeleton's failure moves at least one planned row earlier.

- **Wild: stage a quiet mid-goal "are we still building the right thing?" check-in** — FEATURE — value 3 — effort M — risk med — category: scoping
  Why: wild. At the halfway point, a blind child reads only the user's original words and the current done-list and says what drifted or got gold-plated.
  Done when: the check-in produces a short list citing the user's words and rows, and a seeded gold-plated row is flagged.

- **Wild: let the goal page "answer back" with a defence of any row** — FEATURE — value 2 — effort M — risk low — category: transparency
  Why: wild. Clicking "why is this here?" shows the user's phrase, the template or competitor it came from, and what would be lost if cut.
  Done when: every row on the page returns a non-empty provenance answer, and rows with none are marked ungrounded.

- **Gate new rows on a competing-product baseline** — FEATURE — value 3 — effort M — risk med — category: completeness
  Why: the pack's capability-map idea runs in brainstorm. Goals themselves do not diff their plan against named best-in-class products.
  Done when: a goal can attach a baseline list and reports which baseline items have no row or a recorded "no".

Next question: Which of the 58 cells describe a moment where the goal's state is read by something other than the same session that wrote it (a lane, another harness, the night tick), and has a kill-and-resume test covered that reader?
Next question: What do users of Shape Up, Linear or Kiro do when a goal is cut short or re-scoped that Foreman's finish state has no name for?
