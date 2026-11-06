# Brainstorm — lens: user value

- **Trace every phrase of the goal to a verdict** — FEATURE — value 5 — effort M — risk low — category: done-ness
  Why: assumption: "knows when it's actually done" is only trusted if the user can see their own words land. Eight missed asks in the pack are things the user had to say twice.
  Done when: `fm goal finish` refuses while any phrase from the original request, inbox briefs or mid-run steers has no row (done with evidence, deferred with a revisit date, or dropped with a reason). A planted goal with one forgotten phrase is refused.

- **Name why every stop happened** — FEATURE — value 5 — effort S — risk low — category: stop reason
  Why: the capability says "done rather than merely stopped". Nothing in the pack shows a closed-vocabulary stop reason. Answers the question about outputs the user only misses after they cost a task.
  Done when: every goal halt writes one of done / blocked-on-user / budget / usage-limit / gate-red / crash, and the next session's first line shows it. A killed run shows "crash", never "done".

- **Order the plan so any stopping day leaves something runnable** — FEATURE — value 5 — effort M — risk med — category: plan order
  Why: assumption: goals run over days with limits and crashes, so an interrupted run should still leave something usable.
  Done when: for a planted 10-item goal, item 1–2 form an end-to-end skeleton that passes the goal's smoke check, and an abort after item 2 leaves a repo that runs.

- **Tag every plan item must, should or could with a cut line** — FEATURE — value 4 — effort M — risk low — category: scope
  Why: "best-in-class version" plans grow large (the capability map pillar). The user needs a way to stop at 80% knowingly.
  Done when: the plan page shows a cut line, `fm goal cut should` drops everything below it to deferred with revisit dates, and the finish verdict reads "done at the should line".

- **Make the progress bar able to go backward, with the reason** — FIX — value 4 — effort S — risk low — category: honesty
  Why: assumption: discovered work inflates scope silently, and a bar that only rises misleads. The pack's "form-only gauges" blind spot points at the same thing.
  Done when: adding items after acceptance moves the bar down and logs "+3 items: found in T-n". A test adds items mid-goal and asserts the percentage drops.

- **Write a scope-growth ledger and ask once at a threshold** — FEATURE — value 4 — effort M — risk med — category: drift
  Why: the plan can drift from the user's original ask over days. The steers say never to block on process, so the check is one line in the final report, not a mid-run stop.
  Done when: items added beyond N% of the accepted plan are listed with their origin (user, Foreman-filed, discovered) in `fm goal status`, and the final report carries the list.

- **Hand over a "try this first" finish card** — FEATURE — value 4 — effort S — risk low — category: handoff
  Why: assumption: the user opens a finished goal cold. They need the first command to run, the known gaps and the deferred items with their revisit dates.
  Done when: finish emits a card of at most 15 lines, and every command on it exits 0 in a fresh checkout.

- **Show a single goal page with days, crashes and compactions as markers** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: surface is the web UI, and the "carries the plan over days" claim has no visible proof today. Assumption: the baton and ledger carry timestamps for these events.
  Done when: the goal page renders a timeline with markers for crash, compaction and usage-limit pause, plus an empty state for a new goal. The page loads from state files only.

- **Arbitrate between two live goals** — FEATURE — value 3 — effort M — risk med — category: multi-goal
  Why: assumption: Missions 5–8 already run in parallel lanes, so two goals compete for lanes and budget with no stated rule.
  Done when: with two goals open, `fm goal status` names which gets lanes first and why (dependency, deadline, user's last word), and a steer flips the order.

- **Wild: rehearse the finished state before building** — FEATURE — value 4 — effort L — risk med — category: preview
  Why: wild. A mock of the end state (CLI output, a screenshot, a sample file) is shown for a one-word yes before the plan is accepted, so misreadings surface on day 0 instead of day 3.
  Done when: for a UI goal, plan acceptance shows a rendered mock, and the user's "no" changes the plan.

- **Wild: write the goal's postcard at finish** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. A short human-voice story of the goal: what was asked, what changed on the way, what surprised. It is useful in a week when the user has forgotten the details.
  Done when: finish writes `goal-<id>.md` in plain prose with no tool jargon, and a cold read passes it for accuracy against the ledger.

- **Wild: let the user veto a plan item by a single reaction** — FEATURE — value 3 — effort M — risk med — category: plan control
  Why: wild. The queue is read on a phone as a swipe list (keep / cut / later). It maps to the same must/should/could tags and the cut-line verb.
  Done when: swiping an item changes its tag in the plan file, and the next session honours it.

- **Fill the 58 cells as one rule table, one cell per user-visible moment** — CLEAN — value 3 — effort M — risk med — category: coverage
  Why: the pack's open mission request. Assumption: most cells collapse to a handful of mechanisms (stop reason, resume card, finish card, cut line), so each cell names the verb and the session path that reads it.
  Done when: 0 empty and 0 templated cells, every cell cites a real file and session path, and the sweep's coverage pass is green.

Answers to earlier questions: the stop reason and the trace-to-verdict ledger are outputs the user would notice missing only after a lost task. The 58 cells likely have too little history to backtest for crash and compaction recovery, so plant those faults rather than measure them.

Next question: which goal outcomes does the user re-open within a week, and does any finish check predict that?
Next question: when the user returns after days away, what is the first thing they ask the goal, and is that question answerable from state files alone?
