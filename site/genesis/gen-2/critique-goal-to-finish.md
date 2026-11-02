# Critique — Mission 7, goal to finish (gen 2, #4)

Tasks: T-2556 (done), T-2557 (done), T-2558 (carried: deferred to 2026-12-01, revives at 5 mid-run grant_queued
events within 30 days). Mission: gen-2/mission-goal-to-finish.md.

## Closed vs planned
- Why long goals false-done (T-2556): each failed hidden check of the foreman arm on l001 and l002 was rerun on the
  session's kept tree, the grader's way, and classed by its first error line (research long-false-done). Of 31
  failures, 17 are out of the goal's reach: the check demands an interface the goal never states (attribute names,
  JSON keys, return shapes, an exact viewBox, an installed binding's API). 9 are stated requirements planned but not
  built, or built incomplete. 5 are built differently from what the check expects.
- A done claim checked against each stated Done-when line (T-2557): a goal keeps its raw text's Done-when bullets.
  The verdict names each one that no item's done-when command covers, so a stated line with no check behind it keeps
  the goal open. The grounding case was l002's T-2020: the session built fmcore.lazy, tested none of its three
  Done-when lines, and claimed done.
- Carried: T-2558 (user-only needs at plan time) with its revival condition.

## Outside signals
- The long tier's own grades, which Foreman doesn't write: foreman 0 of 6 true and 6 false dones on l001 and on
  l002; plain 1 of 6 true and 5 false on l002. T-2557's effect is measured only at the end-of-run long tier (rule 6:
  session arms wait for --final). Until then it is unproven on the exam and proven by its tests.
- The exam's reach class is a finding about the keys, and Foreman never rewrites its own keys. It goes to the final
  report, and any re-keying is done by the tool-less child author.

## What failed
- The first draft of this Mission missed the gap entirely and filed a minor brief. The cold reader brought the
  long-tier numbers. Grounding had read the code and the ledger but not the exam's own results for #4.
- My first read of those results was wrong twice: I took an "unknown" count for the false-done count, then took a
  missing answers file for a run that never happened. The sessions had run, and their per-goal grades settled it.

## What the next Seed should change
- Grounding for each Mission reads its capability's exam results first (fm exam long grade and the kinds' lines),
  then the code and the ledger.
- The end-of-run long tier reports false dones split by T-2556's classes, so the exam's reach and Foreman's misses
  are never one number again.
