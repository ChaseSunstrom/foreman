# Critique — Mission 6, exhaustive thinking (gen 3, #2)

Tasks: T-2671 (grounding and filing), T-2672, T-2673, T-2674 (all done). Mission: gen-3/mission-exhaustive-thinking.md.

## Closed vs planned
- Brief 2 (T-2673) is closed and measured. `c.more` tells the reader what a cut list left out, and the silent-cut count
  in fmcli.py went from 22 to 0 by the scan that found them, which test_left_out now runs. Three sites are marked
  `# not a list` with their reason. The scan covers fmcli.py only; the other modules are captured as T-2676.
- Brief 1 (T-2672) is closed: `fm ideas --lens grid` sends a note crossing surfaces, actors and failure modes.
- Brief 3 (T-2674) is closed: the brainstorm skill's grounding step requires a canary before any "not found", and each
  "new" verdict records it.
- Not yet measured, by the Mission's own design: briefs 1 and 3 are judged by use on Mission 7's grounding (grid cells
  that yield a grounded idea; "new" verdicts that carry a canary). Mission 7's catalogue reports both, and its critique
  carries them back here. Until then, these two briefs are built, not proven.
- Counted and carried, as planned: the plan-time citation check (3 of 432 citations broken), the repeat-correction
  sweep, brief claim resolution and stop-reason codes stay in the catalogue (research/brainstorm-20261102-m6.md).

## Outside signals
- None from a user. The truncation count is Foreman's own scan of its own code.

## What failed
- Counting the citation check before choosing it was the planned discipline working, and it cleared only 3 of 432.
  Without that count, a brief would have been built that fixes almost nothing.
- The Mission took four cold reads to file. The Exam first measured brief 3 by its text alone. Done when first listed a
  CHANGELOG line where an outcome belonged. A "dropped" idea had to be restated as carried. Each was a real gap in the
  plan, not wording.
- T-2673's builder changed 18 sites without an output test for any of them. Only the helper's unit tests and the scan
  cover them, so a typo in a rarely hit branch would pass.

## What the next Seed should change
- A Mission's Exam names an outcome measure for every brief before it is filed; "the test asserts the text is there" is
  a format check, never the exam.
- A brief that changes many output sites gets one output test per verb it touches, not only a scan.

## Measures (read by Mission 7, research/brainstorm-20261102-m7.md)
- Brief 1, grid lens: 27 of 41 grid-cell ideas grounded as new or partial, that is, as real gaps. Not zero, so the lens
  passes its Done-when.
- Brief 3, canary: 169 of 170 "new" verdicts carry a canary, but 156 of them used the generic term "def main". That
  passes the letter of Done-when and fails its intent: such a canary shows the search ran, not that its phrasing could
  find a neighbour. gen-3/critique-anticipation.md carries the fix to the next Seed: the canary must be a built feature
  near the idea, and the catalogue counts distinct canary terms.
