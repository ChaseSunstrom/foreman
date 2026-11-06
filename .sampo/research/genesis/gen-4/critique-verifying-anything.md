# Critique — Mission 3, verifying anything (gen 4, #6)

Tasks: T-2914 (done). Mission: gen-4/mission-verifying-anything.md.

## Closed vs planned
- Brief 1 (T-2914) is closed and merged. Two things landed.
  - Plan time: for a user's M or L brief not yet started, `plan_gaps` (core.py) names each clause of the Raw request
    that no criterion checks, with the `sampo task ac add` line that would close it. It uses a new
    `recall.unchecked_clauses`, because `recall.bind` marks every clause "no green run" before anything has run. A
    clause echoed in Non-goals counts as accounted. S tasks, harness and hook plans and Sampo-sourced briefs are not
    gated.
  - Rollup: the meaning kind now splits into the user's words and Sampo's own notes. The task log records the live
    split: meaning-user 244 and meaning-notes 355, summing to 599, which equals the old meaning count. The sum is held
    by a test, so the split cannot quietly shrink.
- Review changed the plan gate after the builder shipped it. It now skips title restatements and batch hosts, and
  four test fixtures had to be rewritten to echo their request in a criterion (test_recall, test_second,
  test_judgment). That is a cost the Mission's risks did not list: the gate broke tests that had passed for months.
- Left out, as planned: three-valued verdicts, and a local model that drafts checks. The latter waits on the
  vacuous-check proof (T-2878).

## Measures (first readings and due dates)
- Share of user M and L closes landing with meaning unproven. Before: 53 of 302. After: not recomputed. The task log
  says so itself: "user M/L share not recomputed (53 of 302 per the brief)". Planned reading: closes after T-2914,
  read at the end of the window. There are no such closes yet worth a share, because the gate began mid-day.
  Due 2026-11-11, and again 2026-12-04 (30 days).
- The rollup split. First reading at close: 244 user, 355 notes. Today the whole rollup reads "unproven: 809 (done
  in the last 30 days)". The 809 is the sum of all kinds (typed 37, red 75, ui-unshot 22, tui-unshot 8, docs 108,
  and others). The meaning part is not the whole of it, and I could not re-split meaning today without running a
  long query. So no movement is claimed. The first look at the rows suggests many of the listed meaning rows are
  provenance lines such as "(noticed by an agent;", which is exactly what the notes half exists to hold.
- Honest reading of the split: 355 of 599 meaning rows, 59%, are Sampo's own words, not the user's. That is a real
  finding. More than half of "meaning unproven" was never the user's. The old number overstated how much the user
  had been left unchecked, by about half. It also means the user's count, 244, is the one that must go to zero.

## Outside signals
- None. This Mission's evidence is all Sampo's own rollup. The one thing a user has done in the same days is steer the
  live page. That gives no read on whether plan-time gaps help.

## What failed
- Nothing is proven to be better, only more honestly counted. The gate asks for a check per clause. It cannot
  tell if the check is real. The Mission's own risk said bind's two-shared-words rule could pass a clause against an
  unrelated criterion. There is no number for how often that happens.
- The measure waited on closes that do not yet exist, and the builder did not take the "before" reading's other half.
  So the critique has the denominator before and nothing after. The fix was one command, `sampo prove --rollup`
  filtered to user M and L, run on a stated date.
- The rollup keeps growing. 809 unproven in 30 days is large, and kinds like red (75), docs (108) and the unshot UI rows remain. The Mission aimed at one kind of the gap. It
  moved the label of the biggest kind and did not close one row.
- Rival plan reading: its likeliest was a plan-schema field. The builder chose a gap in the existing gate. That was
  the cheaper path and is right. The risk it carries is that the gap lives in core.py's plan checks, not in a field
  a later tool can read.

## What the next Seed should change
- Close the 244 by proof, with a sweep: for each user-words row, either add a criterion that can fail or file the
  clause in Non-goals. Rank by recency. A Mission that works that list is measurable the same day.
- Take the after reading with a command, on a named date, in the task log: user M and L closes after T-2914, how
  many carry meaning-unproven. The Mission wrote the want and left the number out.
- Fix the 59%: the provenance lines ("noticed by an agent", "Captured by fm check") should never enter Raw request.
  That is #7's capture-format question, and it stops 355 false rows at the source.
- Then do the three-valued verdict (proved, unproven, disproved) as the next step the Mission itself named.
