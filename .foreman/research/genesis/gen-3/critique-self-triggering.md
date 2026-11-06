# Critique — Mission 1, self-triggering (gen 3, #11)

Tasks: T-2607 (done), T-2608 (done). Mission: gen-3/mission-self-triggering.md.

## Closed vs planned
- The one planned brief is closed. The tick names what it could not watch (T-2607): fmnight._blind derives each skipped
  trigger kind and its reason from the same conditions the tick's branches test (a sensitive project, FOREMAN_NO_NET,
  no watch yes for CI or for the repo's issues). tick-blind.json keeps the newest list, stamped when it changes.
  fm doctor's night-timers row names each kind with the command that opens it, as information rather than a WARN, and
  the session's Watch line does so only while a tick timer is installed and the change is recent.
- Its exam (T-2608): about a third of watch scenarios now set no watch yes for issues. The replay runs Foreman's real
  tick, which skips those issues and reports them blind; the grade needs no work from them and "issues" named blind.
- Not filed, as planned: the brainstorm's fake-clock week harness, an exact duplicate of the watch kind (T-2360).
- Carried, not dropped: the canary order is T-2609, deferred to 2026-12-01 because no trigger-chain failure is on
  record yet; the tick's blind list (T-2607) is the signal that would bring it back sooner.

## Outside signals
- None from real use yet: no tick timer is installed on this machine (the user's install is carried by the seed), so
  the Watch line can't have fired outside the tests.
- The full gate passed on both tasks; the watch kind's replay test, which runs the real tick, passes with the new
  variants.

## What failed
- The Mission's exam line first promised "a variant per reason". Only one reason, no watch yes, can be shown in a
  replayed stream; "sensitive" and "no network" are conditions of the machine the tick runs on, so T-2608 narrowed to
  the one and T-2607's unit tests cover the other two. The Mission should have said so before filing.
- The first doctor design would have turned the night-timers row into a permanent WARN for every user who never asked
  to watch; it became information instead, and the session line was gated on an installed timer after it broke two
  foresight tests that expected silence.

## What the next Seed should change
- An exam line in a Mission names only variants the exam's harness can actually produce; a condition of the machine is
  a unit test, not an exam variant.
- A new status line defaults to information; it is a WARN only when the user asked for the thing it reports missing.
