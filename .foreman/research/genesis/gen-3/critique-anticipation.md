# Critique — Mission 7, anticipation (gen 3, #3)

Tasks: T-2677 (grounding and filing), T-2681, T-2682, T-2683, T-2684 (all done). Mission: gen-3/mission-anticipation.md.

## Closed vs planned
- Brief 1 (T-2681) is closed. fmforesight.lines names the newest unscored next-request guess at session start and books
  a write-once "shown" row. Review added a floor the builder left out: the line waits for MUTE_MIN (20) scored rows, so
  one lucky score shows nothing. It also added the split the Exam needs: `fm outcomes --predictions` now prints "shown at
  session start: N scored, hit X%". On this project's book (23 scored, 52% vs 39% for "same as last") the line shows.
- Brief 2 (T-2682) is closed, after review rewrote its core rule. The builder counted commits main lacks by a whole-tree
  diff against origin/main. Here main also takes `fm genesis live`'s site/ pushes that HEAD never has, so that diff
  always differs and the line would never go quiet. It now counts what fm ship itself would pick (first-parent commits
  since refs/foreman/shipped, else git cherry by patch). A bare "fm ship" action would be refused, since fm ship needs
  the active task's publish grant, so the action names the full path. A steer that says never push to main voids the
  grant. On this repo it read (8, granted) before the ship task opened.
- Brief 3 (T-2683) is closed, after review widened it. As built it grouped tasks by `fm ask` and `depends_on`, and on
  the real pile of 44 blocked tasks it found neither: every wait there is written in the block reason. It now also reads
  "waits for T-…" and "depends on T-…" in the reason, and a task whose named blockers have all closed groups under
  `fm task unblock`. The real line now reads "5 of them wait on tasks already closed: fm task unblock T-1207 T-1344
  T-1390 T-1476 T-2261".
- Brief 4 (T-2684) is closed. _notify records each delivery (exit code, timeout or exception, and the run of failures),
  and fm doctor warns at three failures in a row, naming the command.

## Measures (first readings and due dates)
- Brief 1: shown-guess hit rate against the baseline, read with `fm outcomes --predictions`. First reading: 0 shown
  guesses scored yet (the line first runs at the next session start). Due 2026-11-09.
- Brief 2: hours landed work waits before a push. Before, from origin/main's re-picked commits since 2026-11-01 (committer
  time minus author time, 104 commits): median 0.50 h, 90th percentile 2.2 h, longest 7.6 h. This Mission's own batch:
  the oldest commit landed at 16:15 and its ship task opened at 16:36, about 21 minutes, shipped by hand on the Mission's
  rule rather than by the drive. Due 2026-11-09: the same reading over the week, when the drive follows fm next.
- Brief 3: blocked count. Today 44. Due 2026-11-09. First reading of the line itself: it named 5 tasks blocked on work
  that closed between 6 and 21 days ago.
- Brief 4: notify failures surfaced. First reading: none of this machine's projects has a notify command set, so there
  are no deliveries to count. The measure can't move until someone uses fm notify.

## Mission 6's measures, carried back
- Canary (T-2674): 169 of the 170 "new" verdicts in this Mission's catalogue carry a canary result. But 156 of the 169
  used one generic term, "def main", and 13 used "def predict". "def main" shows the grep ran over the scope, not that
  the idea's own phrasing could find a built neighbour. The rule was met to the letter and mostly missed in intent.
- Grid lens (T-2672): 27 of the 41 grid-cell ideas grounded as new or partial, that is, as real gaps. The other 14 did
  not.
- Both numbers go into gen-3/critique-exhaustive-thinking.md's Measures as their first reading.

## Outside signals
- None from a user. Every reading above comes from Foreman's own book, git history and pile.

## What failed
- Three of four builders shipped code that passed its tests and did nothing useful on this project's real data. The
  ship rule could never go quiet, the pile line grouped nothing, and the next-request line would show after one lucky
  score. Each brief's Exam named a synthetic case: two asks and one grant, a temp repo with a bare remote. None said
  "run it on this project's state first". Review caught all three only because it ran the code on real state.
- Brief 4 was built for a channel nobody here uses. The grounding read the code (an ignored exit code) but never
  checked for a notify command to fail. A cheaper first step was one look at the projects' meta.
- The pile line's first real result is debt: 5 tasks have sat blocked on closed work for up to three weeks, and nothing
  named them until now.

## What the next Seed should change
- Each brief's Exam includes one reading on this project's live state (its own book, pile or repo) before the brief
  closes. A synthetic test proves the logic; the live reading proves the premise.
- Grounding checks that the surface a brief improves is in use (a configured command, a non-empty book) before the brief
  is filed. An unused surface is noted as such, not built for first.
- A canary must be a built feature near the idea (same nouns, same module), not a term any search finds. The brainstorm
  skill's step 4 says so, and the catalogue counts distinct canary terms; one term across most verdicts is a failure.
- The 5 tasks the pile line named go to the next Mission's triage, not to a silent unblock.
