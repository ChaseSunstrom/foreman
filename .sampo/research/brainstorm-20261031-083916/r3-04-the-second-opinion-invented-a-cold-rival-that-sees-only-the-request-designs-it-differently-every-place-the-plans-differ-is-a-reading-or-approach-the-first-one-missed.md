# Brainstorm — lens: the second opinion (invented): a cold rival that sees only the request designs it differently; every place the plans differ is a reading or approach the first one missed

**Lens: the second opinion.** One earlier question I can answer from this lens: the cold Haiku second reads are the only judge of model-written tower files, and no user-owned check sits between them. Ideas 7 and 10 below add one.

- **Verify a task's premises before filing it** — FIX — value 4 — effort S — risk low — category: intake
  Why: three recent drops had false or stale premises: `check_plan` already refuses L, `_next_runnable` was not a stall, and a duplicate was already done in T-2298. A cold rival given only the title and the repo can test the claims.
  Done when: `fm task new` with a body citing `file:line` or "X refuses Y" runs a free grep check, and a claim that doesn't match prints a note naming the mismatch.

- **Propose the runner-up blind when the Approach names none** — FEATURE — value 4 — effort M — risk med — category: stuck ladder
  Why: T-2271 races only when the Approach names an alternative. S tasks have no required options, so the third failed run falls through to the hypothesis table. Assumption: S tasks often lack an alternative.
  Done when: an S task with three failed runs and no named alternative gets a rival-proposed approach, seeing only the criterion and the error, and `fm lane race` runs it.

- **Recover the approach from the diff and compare it with the chosen one** — FEATURE — value 4 — effort M — risk low — category: approach drift
  Why: the plan gate checks that a choice is written, not that the diff implements it. A rival reads only the diff and names the approach it sees.
  Done when: `fm task finish` records "plan chose A, diff shows B" when they differ, and refuses until the Approach is amended or the diff changed.

- **Write the tests blind from the request** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: the writer of the fix also writes its red-first test. Exam scenarios already come from a separate child, but task tests don't.
  Done when: M/L tasks can run a tool-less child that writes 2–3 acceptance checks from the title and criteria, and any that fail on the finished tree are listed in the receipt.

- **Audit the stops Foreman didn't make** — FEATURE — value 4 — effort M — risk med — category: calibrated judgment
  Why: "stop only for irreversible and ambiguous" has a false-negative side that nothing measures. Earlier ideas only score asks that were sent.
  Done when: a rival reads the request plus the action list and names steps it would have stopped on. `fm decisions` shows each unasked one with its door type.

- **Estimate tier blind and treat disagreement as a depth signal** — FEATURE — value 3 — effort S — risk low — category: tiering
  Why: the plan gate scales by the tier label, which the same session assigned.
  Done when: a task whose blind tier is higher than its assigned tier gets the higher tier's plan gate and a one-line note.

- **Probe blast radius for graph blindness** — FEATURE — value 3 — effort M — risk low — category: blast radius
  Why: the map shows 1388 skill files and a site. `fm graph blast` uses co-change, which misses docs, site and skill couplings that nothing changes together yet. A rival lists the files it expects touched from the title alone.
  Done when: files the rival names that blast omits are shown in the plan Risks as "unconfirmed neighbours".

- **Calibrate the plan gate's option check against rival judgments** — FIX — value 3 — effort S — risk low — category: plan gate
  Why: T-2285 shows the marker-counting gate missed an option starting with a flag. A rival judging "three distinct options?" on a labelled corpus finds other misses. The free gate is tuned from it and never replaced.
  Done when: a test runs the corpus (including flag-first and code-first options) through the free gate, with at least 95% agreement against the labels.

- **Check README and site claims against verbs** — FIX — value 3 — effort M — risk low — category: docs
  Why: the user said the website "doesn't look like it has been" updated. A rival reads only the site and README and tries to find the `fm` verb behind each claim.
  Done when: `fm doctor` lists claims that match no verb or test, and the site stats task fails when a claim is orphaned.

- **Wild: Reverse the request from the receipt** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: wild. A cold child reads only the finish receipt and writes the request it thinks produced it. A big distance from the real request means the receipt isn't plain.
  Done when: `fm task finish` records a similarity score, and receipts scoring below the threshold are flagged for rewrite.

- **Wild: Malicious-compliance rival for steers** — SECURITY — value 4 — effort M — risk med — category: steers
  Why: wild. Every steer becomes a rule plus an automatic check. A rival writes the most literal behaviour that obeys the steer while breaking its intent, such as a push through a side door. Each case becomes a regression check.
  Done when: for 5 stored steers, the rival's loophole cases run in `fm genesis sweep`, and one that passes unflagged fails the sweep.

- **Wild: Diff against a speedrun** — PERFORMANCE — value 3 — effort L — risk med — category: simplicity
  Why: wild. A rival implements the request in a throwaway lane, blind to the plan. If it passes the same checks with a much smaller diff, the surplus in Foreman's diff is named.
  Done when: for a sampled M task, `fm lane race --blind` reports both diff sizes and the hunks only the builder wrote.

- **Wild: Plan at a tenth and ten times the budget** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: wild. The rival plans the same request at 1/10 and 10x effort. Rows present in both plans are the core, and rows in only one are optional or gold-plating.
  Done when: the plan view marks each row core, stretch or cuttable, and the user can cut all non-core rows with one command.

Next question: which of Foreman's own gates have never had a cold rival tried against them, and what do they miss on tasks nobody has filed yet?
Next question: when the rival and the builder disagree, how often does the user's later steer side with the rival?
