# Brainstorm — lens: user value

- **Capture a baseline at goal start and print the delta at finish** — FEATURE — value 5 — effort M — risk low — category: outcome
  Why: the pack's "done" checks all test output (rows, oracles, probes), not benefit. A goal like "make it faster" or "cut flaky tests" is only worth it if the number moved. Assumption: most vague goals hide one measurable outcome.
  Done when: `fm goal` with a measurable goal runs a baseline command at creation, and the finish card shows before, after and delta from stored values; a goal with no measurable outcome says so.

- **Rank user-only decisions by what each one blocks** — FEATURE — value 5 — effort S — risk low — category: attention
  Why: the pack has a running list of user-only items but no ordering. After days away, the user's first question is "what do I have to decide so work continues?"
  Done when: the resume view lists each pending decision with the count of rows and estimated hours it blocks, sorted descending, and a test shows a decision blocking 3 rows ranks above one blocking 1.

- **Name the off-the-shelf alternative for every plan row** — FEATURE — value 4 — effort M — risk med — category: build-vs-buy
  Why: ideas so far cover "check the XY problem" and "search the user's other repos", but not "a maintained library or tool already does this row". Reuse is the cheapest finish. Assumption: stack cards and manifests give enough signal to name candidates.
  Done when: each plan row carries an "adopt:" field (a named tool, or "none found, searched X") and the plan gate refuses a row where the field is empty.

- **Leave a verify-without-Foreman kit in the repo** — FEATURE — value 4 — effort M — risk low — category: ownership
  Why: users who might later leave Foreman, or whose collaborators don't have it, need to know the goal is still true. The pack has "done as one exit code" but not a standalone artifact.
  Done when: finishing a goal writes `GOAL-CHECK.sh` and a short README into the repo, and running them on a clean clone with Foreman absent from PATH gives the same pass/fail as the finish oracle.

- **Warn at plan time about the row this user historically stalls on** — FEATURE — value 4 — effort M — risk med — category: personal-planning
  Why: the dropped and closed-goal ledgers record where past work died. The pack has estimate-vs-actual per row but nothing that predicts the stall point from the user's own history. Assumption: at least 5 finished or dropped goals exist to learn from.
  Done when: on a fixture history where 3 of 4 abandoned goals stalled at a "migration" row, a new plan with such a row shows a one-line warning citing those goals, and a plan with no such row shows nothing.

- **Compare a new goal against the deferred backlog's value per cost** — FEATURE — value 3 — effort S — risk low — category: prioritisation
  Why: there are about 30 deferred "Later from T-07xx" items and the pack says nothing about weighing a new goal against them. Arbitrating between two live goals exists, but this compares against dormant work.
  Done when: creating a goal prints the three deferred tasks with the best value-to-effort ratio next to the goal's estimate, and a test shows a high-value S task surfaces.

- **Draft the upward status update the user has to send** — FEATURE — value 3 — effort S — risk low — category: communication
  Why: the pack has a handoff page and a morning note, but those speak to the user. Users with a manager or client must translate them. Assumption: the audience is declared once per goal.
  Done when: `fm goal update --for <audience>` writes a 5-line draft (done, next, blocked, date band, ask) from files only, staged and not sent.

- **Watch for upstream shipping the goal's feature** — FEATURE — value 3 — effort M — risk med — category: obsolescence
  Why: multi-day goals outlive release cycles. The pack watches host release notes for Foreman's own code but not for the user's open goals. Assumption: a goal's key nouns can be matched against changelogs of its dependencies.
  Done when: a fixture dependency changelog that adds the feature of an open row makes the next session note propose "shrink or close row N", citing the changelog line.

- **Seed the next goal from real end-user feedback after finish** — FEATURE — value 3 — effort M — risk med — category: sequel
  Why: sequels spawn from parked growth, not from what people actually said about the shipped result. Issue watchers exist but aren't tied to a closed goal.
  Done when: an issue filed against a closed goal's shipped paths is clustered into the goal's sequel candidates and shown on the finish card's "since" section.

- **Wild: Draft a three-line pre-sell pitch for the user to show one real person** — FEATURE — value 3 — effort S — risk low — category: validation
  Why: wild. Before days of work, the cheapest test of "do I even want this" is one outside reaction. Foreman stages the pitch, never sends it, and records the user's one-word reaction as evidence on the goal.
  Done when: `fm goal pitch` writes the pitch to a file, and a later `fm goal react <word>` appears in the goal's evidence and the finish card.

- **Wild: Share a read-only goal board where a friend can only vote on rows** — FEATURE — value 2 — effort L — risk high — category: collaboration
  Why: wild. Collaborators currently can't weigh in without Foreman access. Votes arrive as a local file, with nothing sent unless the user enables it.
  Done when: exporting a board yields a static page with up and down controls that produce a votes file, and importing it re-ranks the could-have rows.

- **Wild: Opt-in plan potluck of anonymised plan shapes** — FEATURE — value 2 — effort L — risk high — category: shared-knowledge
  Why: wild. Row titles, order and actual-vs-estimate ratios (no code or text) from willing installs could ground "what a finished X contains". It must be an explicit setting, off by default, and the shapes must be redacted and inspectable before any share.
  Done when: with the setting off, a network-denied test run makes zero calls; with it on, `fm goal share --dry` prints exactly the bytes that would leave.

Next question: Which finished goal's outcome did the user actually keep using 30 days later, and what did that goal's plan contain that the dropped ones lacked?
Next question: When the user returns after a long gap, which single sentence would let them decide in under a minute whether the goal still matters?
