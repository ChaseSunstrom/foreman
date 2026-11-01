# Critique — Mission 4, goal to finish (gen 1, #4)

Tasks: T-2135 to T-2141 (briefs 1-7, all done by 2026-10-31T02:41Z). Mission: gen-1/mission-finish.md. Numbers are
from exam run s21-013 (2026-11-01, zero-token arms) and the long-horizon runs l001-l003 (2026-10-31, after the
Mission closed, the default model).

## Closed vs planned
| Planned (Done when) | State |
|---|---|
| fm goal set/plan/show/verdict work and are tested (T-2135, T-2136, T-2137) | closed: test_goal |
| A done claim with unaccounted clauses or an unfinished goal blocks once at Stop and never traps (T-2138) | closed: test_hooks; not seen working in the long-horizon runs (below) |
| The goal line survives a new session, a compaction and a crash (T-2139) | closed: test_goal, test_hooks |
| The #4 exam runs the foreman and plain arms on its held-out third (T-2140) | built (T-2140: kinds vague, goal, resume; test_exam); not yet measured: their scores come from the session arms, which wait for the end-of-run exam (rule 6) |
| fm code, MCP, AGENTS.md block, site page, pane line, MASTER, README, CHANGELOG (T-2141) | closed on T-2141's recorded runs: test_code and test_code_envelope (fm code), test_mcp (MCP), test_site and test_export (site page), test_ui_signals (pane line), test_goal; the AGENTS.md block and the docs have no run of their own here (test_agents and test_docs check them in fm check); coverage #4: 6 cells filled |

## Outside signals
- s21-013: the #4 kinds (vague, goal, resume, 27 scenarios) close only for the oracle; no zero-token arm can do the
  work they grade, so they wait for the session arms.
- Long-horizon (the deciding tier, paused by the user's 2026-10-31 steer until the end of the run): over 6 goals the
  foreman arm finished 0 and claimed done on all 6 (false-done 6), with 4 of 20 checks passing; plain finished 1 with
  5 false-done claims, at the same total cost ($13.08). On l002 the foreman arm passed 0 checks on its first goals
  (T-2093: 0/5, T-2020: 0/3) and still said done.

## What failed
- False done is what Mission 4 exists to stop, and the foreman arm claimed done on every long-horizon goal it didn't
  finish. Why is not established yet: the Stop wiring holds a claim against a goal set with fm goal set or the last
  request's unaccounted clauses, and the runs' transcripts weren't read for which of these fired. The working
  hypothesis is that a headless session never set a goal and its clauses read as accounted for, so nothing held the
  claim; the end-of-run exam's long-horizon tier should log the Stop decisions to settle it.
- One long-horizon sample on one model can't separate Foreman from plain (1 finish in 12); the end-of-run exam decides.

## Spike verdicts
None planned as tier-4 spikes in this Mission.

## What the next Seed should change
- Make the goal automatic: a request with a done-when, or one fm goal plan sizes past a single task, becomes the
  standing goal, so Stop always has a goal to block a false done against; test it on a long-horizon goal, not a unit.
- Count a session's "done" against the goal's own checks at Stop (fm goal verdict), never against its own say-so.
- Re-run the long-horizon tier at the end of the run, with the false-done count as #4's headline number.
