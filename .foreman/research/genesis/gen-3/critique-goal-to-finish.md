# Critique — Mission 3, goal to finish (gen 3, #4)

Tasks: T-2613 (done). Mission: gen-3/mission-goal-to-finish.md.

## Closed vs planned
- The one planned brief is closed. The long tier's runner keeps each failing check's last traceback line; the grade
  classes a failure that names a missing attribute, key or import the goal text never mentions as out of the goal's
  reach, carries every failed check's line and class in its JSON, and prints "false done N (M only on names the goal
  never states)".
- Found on the way, fixed inside T-2613: an answer's exception whose str() raises would have crashed the runner in its
  except block and lost every other check's result.
- From the brainstorm (512 ideas): two of the three closest ideas were already partly built (T-1228, T-2557, T-0886)
  and not filed; the third, a verdict that flips, is T-2614, deferred until a flip is on record.

## Outside signals
- Regrading the kept runs costs no tokens. l001 foreman: "false done 6 (2 only on names the goal never states)".
  l002 foreman: "false done 6 (0 only …)". l002 plain: "false done 5 (0 only …)".
- At the check level the rule finds 13 of 31 failed checks out of reach; T-2556's hand read found 17. The four it
  doesn't class: three return-shape failures ("'Result' object is not subscriptable") and one missing binding API in
  the environment.
- So l002 reads 0 reach for both arms: its goals already carry T-2304's "The checks use these new names" hint, and
  its remaining unstated keys ('read', 'problems') appear in the goal text as plain words, so the conservative rule
  calls them real.

## What failed
- The Mission's exam line promised the split "must match T-2556's hand classes on the named misses (17 checks out of
  reach)". It reached 13. The rule only counts a name the goal text lacks entirely; a key that appears as an ordinary
  word is read as stated. That keeps the split from ever excusing a real miss, but it undercounts.
- The first Ideas section skipped the brainstorm for pace; the cold read refused it under the user's steer that pace
  never stops work, and the brainstorm then ran in full. The budget guard holds subagents, not fm ideas.

## What the next Seed should change
- An exam line that compares an automatic rule with a hand read states which way the rule may differ (here, a lower
  bound) before it is filed, so a 13 against 17 reads as the design and not a miss.
- A brainstorm is never skipped for pace: when subagents are held, fm ideas still runs, and the Mission waits for it.
