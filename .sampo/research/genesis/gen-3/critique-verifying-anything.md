# Critique — Mission 4, verifying anything (gen 3, #6)

Task: T-2616 (done, 083fa7c6). Mission: gen-3/mission-verifying-anything.md.

## Closed vs planned
- The one planned brief is closed. The docs proof kind now skips history files (fmdocs' changelog rule, T-1817), so it
  no longer flags lines `fm prove --docs` never reads, and it diffs a task's start to its own newest id-prefixed commit
  rather than HEAD. The rollup's cache key carries a rule version, so a rule change is recomputed.
- Unit checks pass: a CHANGELOG-only task isn't listed for docs; a later task's claim isn't charged to an earlier one;
  a task whose own commit adds a claim still is.
- Foreman's own count moved docs 601 → 421 (419 now). That is a recount under a narrower rule, not proof gained: no
  claim became proven. The meaning class (571) is unchanged and is now the largest.
- Carried, not dropped: the 1,582 subcommand and flag claims need the user's `fm prove --yes-run` (never self-granted),
  and intent proof beyond an LLM lens stays open.

## Outside signals
- None. No user or outside run has read the rollup since the change; the proof page shows the new count without a page
  change, but nothing records anyone opening it.

## What failed
- The order put → intake → build wasn't kept: the brief was found and built while grounding, before the Mission was put.
- The first hypothesis was wrong and was logged as wrong. The own-commit diff alone moved docs only 601 → 597, because
  only 70 of the 416 CHANGELOG-first tasks have an id-prefixed commit (older ones landed in merges). The real drop came
  from the history-file rule, found only after the scope was widened mid-task.
- The Mission measured the class size but not which lever moves it. A two-minute count of how many items each fix would
  clear would have picked the history-file rule first.

## What the next Seed should change
- Before a Mission names a fix for a count, it counts what each candidate fix would clear and leads with the biggest.
- A proof kind is defined from the clearing verb's skip list: whatever the clearing run never reads isn't flagged.
- #6's next lever is meaning (571): fm spec's example assertions become runnable criteria at plan time, with no
  confirmation step; a meaning label clears only when such a criterion ran green.
