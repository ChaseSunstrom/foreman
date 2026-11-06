# Critique — Mission 3, initiative (gen 1, #1)

Tasks: T-2120 to T-2127 (briefs 1-8, all done), spikes T-2415 (done) and T-2414 (dropped as moot). Mission:
gen-1/mission-initiative.md. Numbers are from exam run s21-013 (2026-11-01, zero-token arms, 306 scenarios, 102 held
out) and the T-2415 replay; nothing here rests on a session arm (seed rule 6: those wait for the end-of-run exam).

## Closed vs planned
| Planned (Done when) | State |
|---|---|
| Clean renders keep their edge contract in six languages; the README command runs (T-2120) | closed: oracle 306/306, empty closes only the 9 clean scenarios (s21-013) |
| fm find, fm find prove, --rank work and are tested (T-2121, T-2122, T-2125) | closed: test_find, test_prove; finders 180/261 found, 0 false alarms |
| Scout files only proven findings, at most 3 a day, Foreman's faults to the self-inbox (T-2124) | closed: test_scout |
| /foreman:initiative in Claude Code; fm find in fm code and MCP (T-2123, T-2127) | closed: test_mcp, test_code; coverage #1: 8 of 8 cells filled |
| The finders arm runs every scenario every generation | closed for gen 1: s21-013, held out 60/87 found |
| foreman and plain arms on the held-out #1 exam | open by design: end-of-run exam on the production model (seed rule 6) |
| MASTER, README, CHANGELOG and the site's Initiative page (T-2127) | closed: test_site, test_docs |

DONE-WHEN reads "the held-out #1 exam runs all three arms and the clean renders file nothing". The clean renders file
nothing (finders: 0 false alarms over 306 scenarios). One arm of three has run; the other two wait for the end-of-run
exam, so #1 is not done.

## Outside signals (zero tokens)
- Finders recall by defect kind (s21-013): dep 9/9, docs 36/36, flaky 9/9, fork 9/9, slow 45/45, untested 27/27,
  vuln 45/45; bug 0/72, trigger 0/9. By language (s21-013): ruby 19/26 (73%), rust 28/39 (72%), js 30/42 (71%), c 47/67 (70%), python
  32/46 (70%), ts 24/41 (59%); the gap is the bug rows, which every language has.
- T-2415 replay: fm find on the parents of Foreman's last 40 FIX commits. 26 changed code; 0 of the 26 had a lead
  within 3 lines of a changed line. Every one is a logic or behaviour fix.
- Together these show what the finders are: a zero-token hygiene arm (missing tests, stale docs, deps, quadratic
  loops, injection, flaky tests) with no reach into logic bugs, which are most of what a user's FIX tasks are.
- Open: whether a real foreman session uses what Foreman built is not measured in gen 1. Session arms wait for the
  end-of-run exam (rule 6), so no number here speaks to it.

## Spike verdicts
- Replay git history (T-2415): run. Verdict above; no lexical rule can catch the misses.
- Cold refuter (T-2414): not built in gen 1, and still open. It was to cut false alarms (19 on s70-010); s21-013 shows
  0 false alarms over 306 scenarios, so gen 1 had nothing for it to cut. It goes to gen 2's selection as an open idea,
  to run when an exam shows false alarms again.
- Canary mutation planter and a clean twin of a real repo: not run in gen 1, and still open. Gen 1 ran the replay
  first; the planter would add defects no replay holds. Both go to gen 2's selection as open ideas.

## What failed
- Logic bugs: 0/72 planted, 0/26 real. Mission 3 planned find → prove → fix as the pipeline, but the find step can't
  see the largest class of defects, so prove and fix never get a lead for them.
- Filing this critique: T-2221 put it through the cold read 26 times without convergence (decision 2026-10-31); this
  draft waits for the user's call on the cold-read rule.

## What the next Seed should change
- Aim #1 at logic bugs with proofs, not patterns: the session arm proposes a failing test (fm find prove's red-first
  rule), mutation or property tests on the files fm find --hotspots ranks, and #7's recurring-failure signal (recur).
- Score #1 on the project's own history every generation: the T-2415 replay as a zero-token arm beside the planted
  exam, so planted-kind recall can't hide real-fix recall.
- Keep the finders as the hygiene arm and keep their 0 false alarms as a gate.
