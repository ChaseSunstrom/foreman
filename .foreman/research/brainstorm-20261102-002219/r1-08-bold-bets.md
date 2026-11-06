# Brainstorm — lens: bold bets

Answering one earlier question first: cells that rely on Claude-only hooks (compaction survival, session resume) quietly depend on that harness. Any cell citing `PreCompact` or a session baton should name its non-Claude equivalent, or be marked n/a.

- **Make the goal a git ref that rebuilds itself** — FEATURE — value 5 — effort M — risk med — category: durability
  Why: assumption: the goal plan lives in state files that a crash, compaction, wiped state dir or second machine can desync from the repo.
  Done when: after the session, state dir and baton are deleted mid-goal, `fm goal resume` rebuilds the plan, the finished rows and the next step from `refs/foreman/goal` plus commits alone, and a test asserts the same next step as the uninterrupted run.

- **Compile "done" into a finish oracle the goal cannot close without** — FEATURE — value 5 — effort M — risk med — category: done-detection
  Why: the capability says "knows when it's actually done rather than merely stopped". Assumption: today that rests on rows marked by the builder.
  Done when: `fm goal finish` runs one generated script (a probe per capability-map row) and refuses with the failing row named. A planted half-built goal is refused, and a fully built one passes.

- **Split "stopped" from "done" into a typed ending with a why** — FEATURE — value 4 — effort S — risk low — category: done-detection
  Why: the lessons say most of #2, #3, #11 and #12 was already built, so goals that merely stop look finished. Assumption: no ending type exists.
  Done when: every goal ends as done, stopped-by-choice (marginal value under a floor), stopped-by-blocker (names a grant or a wait) or abandoned, and `fm status` and the final report print the type.

- **Dogfood: fill the 58 cells by running #4 on the cell grid** — FEATURE — value 5 — effort M — risk med — category: self-hosting
  Why: the request is the 58 empty cells. Treating "fill coverage.md" as a goal makes each cell a capability-map row with its own probe, so the engine is tested on a real multi-day job.
  Done when: the 58 cells become rows. Each closes only on a probe that names a concrete file or a recorded n/a, and the sweep's coverage pass goes green with no templated cell.

- **Rebase the plan when the codebase moves under a multi-day goal** — FEATURE — value 4 — effort L — risk med — category: long-horizon
  Why: assumption: plans are written once, but days pass, other tasks land, and files rows cite are renamed or already built by someone else.
  Done when: after a fixture repo gets 30 commits that rename a cited file and build one row, `fm goal rebase` marks the built row done with its commit, retargets the renamed one, and reports what changed. A test pins both.

- **Offer three finish lines and tag each one** — FEATURE — value 4 — effort M — risk low — category: scope
  Why: "best-in-class" has no natural stopping point. Assumption: a vague goal produces an open-ended plan the user must cut by hand.
  Done when: goal intake emits minimum, solid and best-in-class row sets. The user picks one by a single word, and reaching a tier tags the repo and reports "tier 2 of 3 reached".

- **Run a crash-fidelity drill on every goal engine change** — PERFORMANCE — value 4 — effort M — risk low — category: reliability
  Why: the capability promises survival of crashes and compactions. Assumption: it is tested by unit tests, not by killing a real mid-goal run.
  Done when: a harness kills a scripted goal at 10 random points, resumes cold, and scores whether the next action matches the uninterrupted run. The score is printed in `fm doctor`, with a floor.

- **Calibrate the done-detector against reopens** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: the steer on bets and Brier scores exists for judgment. Assumption: goal finish is not scored the same way.
  Done when: each goal's finish writes a bet "this stays closed for 14 days". `fm outcomes` shows the reopen rate per goal size, and a rate above a stated bar tightens the oracle.

- **Wild: seal the finished product's demo script at the start and diff it at the end** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. Writing "what a stranger would do in the finished product" up front exposes scope gaps early and gives a final comparison no builder wrote afterward.
  Done when: `fm goal start` stores a hashed demo script. At finish it is run, and every line is shown as passes, changed or missing.

- **Wild: dispatch rival decompositions and keep the plan that survives its first step** — FEATURE — value 3 — effort L — risk med — category: planning
  Why: wild. Two planners, one cheap and one strong, each make a plan, and the first step of each runs in a scratch worktree.
  Done when: the picked plan is the one whose first step passes its probe and touches fewer unplanned files, and the rejected plan is stored with the reason.

- **Wild: show the goal as a fog-of-war map on the web UI** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: wild, and assumption: nothing on the web UI shows a goal's territory. The 58-cell grid is a natural map.
  Done when: a goal page draws rows as regions. Unknown ones are fogged, proven ones lit, and a clearing animation plays only when a probe passes, with reduced-motion honoured.

- **Wild: let a sleeping goal wake on a trigger instead of a command** — FEATURE — value 3 — effort M — risk med — category: autonomy
  Why: wild, and assumption: goals resume only when the user returns. A goal parked on a blocker, a usage window or a grant already has a wake condition in its row.
  Done when: a parked goal resumes from the night tick the moment its wake condition is true, lands its work on a branch, and the morning report names the row it moved.

- **Mark goal rows as evidence-backed or builder-claimed** — SECURITY — value 3 — effort S — risk low — category: proof
  Why: standing steers on gaming and cold reads. Assumption: a row marked built by its own builder carries no distinction.
  Done when: each row shows who proved it (probe, cold reader or self), and finish refuses a goal where the share of self-claimed rows is above a set bar.

- **Budget the goal with a burn-down and a marginal-value floor** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: assumption: unlimited-length goals have no stop signal besides running out of rows.
  Done when: rows carry value and effort. `fm goal` ranks them by value per effort, shows remaining value, and proposes stopping when the next row falls below the floor.

Next question: Which of the 58 cells describe behaviour only visible across a compaction or crash, and can a kill-and-resume drill actually reach each of them?
Next question: When a goal is done by its oracle but the user reopens it, which kind of row was missing, and does the capability map have a column for it?
