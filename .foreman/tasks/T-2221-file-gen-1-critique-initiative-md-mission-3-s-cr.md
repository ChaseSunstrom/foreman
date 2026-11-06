---
id: T-2221
type: RESEARCH
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T21:55:45Z
updated: 2026-11-06T03:54:30Z
base: 27711d6d123663964f4edbb4d2506f57fd85bdc8
base_tree: 4839ace78394814b5dc8c6816e3fae23fcf41d19
plan0_at: 2026-10-30T23:30:45Z
plan0_scope: []
paused_tree: 4839ace78394814b5dc8c6816e3fae23fcf41d19
---
# File gen-1/critique-initiative.md (Mission 3's critique) through the cold read
## Raw request
> File gen-1/critique-initiative.md (Mission 3's critique) through the cold read
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] the critique is the tower's gen-1 file — verify with fm genesis status
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] revise per the carried findings; put  <- CURRENT
## Resume here
<!-- auto -->
- 2026-10-31T00:46:37Z step 1/1: revise per the carried findings; put
- git: foreman/build; 2 uncommitted: CHANGELOG.md, MASTER.md
- failures met: raise modelerror(f"no model profile named {name!r} (models.json, {', '.join(n for n, *_ i…
## Docs impact
## Verification evidence
## Log
- 2026-10-30T21:55:45Z created
- 2026-10-30T21:56:04Z 3 cold-read rounds: 6, 4, 6 failed lines. Round 3 reverses round 2 on the s31-006 Haiku-smoke gap (round 2: steer 3 makes it the next Seed's top gap; round 3: steer 1, a 1-of-18 Haiku difference can't direct work). Next revision: say fm exam scorecard lists it labelled Haiku smoke, it moves nothing (steer 1), and the Seed's Top gap reads train lines only; rows: six built, find→prove→fix built for 4 of 8 kinds, surfaces without Desktop; #1 exam row 'built, unmeasured'; survival from fm outcomes, not git log; the score-test lesson needs an automatic check (T-2222); coverage refresh now (T-2223). Draft: research/draft-critique-initiative-gen1.md
- 2026-10-30T21:56:04Z blocked: 3 failed cold-read rounds (6, 4, 6 lines), the reader reversing itself on a steer-1 vs steer-3 line; next revision and its two prerequisites are logged
- 2026-10-30T23:30:44Z unblocked
- 2026-10-30T23:30:45Z focused
- 2026-10-30T23:30:47Z unblocked: T-2207/T-2228/T-2229 make long puts converge; retrying with crit4 (coverage section updated to the re-filed coverage.md)
- 2026-10-30T23:31:21Z paused: focus moved to T-2231
- 2026-10-30T23:37:51Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-30T23:37:51Z focused
- 2026-10-30T23:47:33Z paused: focus moved to T-2233
- 2026-10-30T23:53:08Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-30T23:53:08Z focused
- 2026-10-30T23:56:19Z blocked: Diagnosis: the cold read on this narrative critique doesn't converge. 10 puts this session (scratch crit4→crit14), after T-2207/T-2228/T-2229/T-2231 fixed the put's own deadlocks; each read flags 1-6 lines. Real fixes landed every round (Initiative 8 of 64 cells, outside vs inside signals split, a cold Haiku review of #1 run and filed as T-2235, surfaces row marked partial), but objections rotate and reverse: the Haiku review as outside signal → not outside; the s31-006 top gap carried → not carried → carried; not-yet listed → needs a blocker and two approaches. It also writes newlines as literal \n in quotes spanning a heading and its next line (strays, T-2236). Draft to resume from: the session scratch crit14.md, saved as research/draft-critique-initiative.md. Next approach: T-2236's matching fix, then judge the critique section by section against the critique template rather than the whole narrative at once.
- 2026-10-31T00:24:26Z unblocked
- 2026-10-31T00:24:26Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-31T00:24:26Z focused
- 2026-10-31T00:24:27Z unblocked: T-2236 (multi-line quotes) landed; retrying crit14
- 2026-10-31T00:26:28Z blocked: Diagnosis (second block): 13 puts this session. After T-2236 fixed multi-line quotes, two more puts each drew 2-4 new objections on lines earlier reads passed (the table's columns, the coverage section, outside signals, the Seed's order). The whole-file cold read rotates objections on long narrative files. Draft: research/draft-critique-initiative.md (the session scratch's crit15.md is newer: long-horizon row and open-gap line added). Next approach: T-2243 (one cold read per ## section, each with its own acceptance).
- 2026-10-31T00:43:14Z unblocked
- 2026-10-31T00:43:14Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-31T00:43:14Z focused
- 2026-10-31T00:43:16Z unblocked: T-2243 (section-by-section cold reads) landed; retrying crit15
- 2026-10-31T00:46:37Z paused: focus moved to T-2245
- 2026-10-31T00:50:00Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-31T00:50:00Z focused
- 2026-10-31T00:53:52Z blocked: Diagnosis (third block): 18 puts. Section reads (T-2243, T-2245) work mechanically, but editing any section changes the outline every section's pass hash includes, so passed sections are re-read; the top section read alone looks like 'no critique'; and the Haiku reader keeps raising new objections (19 on the last put), some reversing earlier rounds. The fix is to the gate's blocking rule, which comes from the user's steer: proposal captured as T-2246 for the final report. Latest draft: research/draft-critique-initiative.md (crit18).
- 2026-10-31T04:28:49Z unblocked: retrying with a 45-line version: every claim names a task or file, statuses re-checked today
- 2026-10-31T04:28:49Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-31T04:28:49Z focused
- 2026-10-31T04:30:00Z blocked: Diagnosis (fourth block): a 45-line version with a task id or file on every claim drew 14 objections across all sections, most asking for graded #1 results that only the end-of-run production exam can produce (seed rule 6). Shortening doesn't converge it; the rule change is T-2246, the user's call (steer 2). Draft kept: scratchpad crit16.md
- 2026-10-31T14:13:37Z 2026-10-31 after T-2246 (grounded FAILs), T-2366 (the reader sees the cited numbers) and T-2400 (honest gap reports break nothing): 8 more puts; passed sections stay passed, but the failing ones oscillate (the smoke line was failed for deferring the top gap, then for naming it from a smoke run) and previous-reads re-fail capability gaps a critique can only report ('fail again one still unmet'). Draft: scratchpad critique-initiative.md (exam-sourced numbers, every row open). Diagnosis: previous-reads treats a reported capability gap as a file defect, so a critique of unfinished work can't converge; the fix is the user's rule-7 call, in the final report
- 2026-11-06T03:54:30Z dropped: superseded: Rune ran gens 2-4 since (seeds and critiques filed); gen-1's narrative filing no longer changes anything (2026-11-06 blocked review)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2078 [FEATURE M, done, 3 steps] fm genesis: the tower's home: init saves gen-0 verbatim and read-only, put files tower docs under research/genesis, status shows the to…
- T-2182 [FEATURE M, blocked, 1 steps] File gen-1/mission-exam.md and mission-genesis.md through the cold read: 16 rounds each…
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (second): standing rule] Every tower file (seed, mission, critique, coverage, not-yet, exam entry) gets a cold H…
- similar past tasks were M: consider --tier M
## Draft (unfiled, 2026-11-01)
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
  vuln 45/45; bug 0/72, trigger 0/9. By language, c 47/67 is the best share and ts 24/41 the worst; the gap is the
  bug rows, which every language has.
- T-2415 replay: fm find on the parents of Foreman's last 40 FIX commits. 26 changed code; 0 of the 26 had a lead
  within 3 lines of a changed line. Every one is a logic or behaviour fix.
- Together these show what the finders are: a zero-token hygiene arm (missing tests, stale docs, deps, quadratic
  loops, injection, flaky tests) with no reach into logic bugs, which are most of what a user's FIX tasks are.
- The scorecard's top gap, from a Haiku smoke run on s31-006, says the foreman session found 15/18 where finders found
  16/18: the session doesn't use what Foreman built. It is a smoke signal only (rule 6) and is carried to the end-of-run
  exam.

## Spike verdicts
- Replay git history (T-2415): run. Verdict above; no lexical rule can catch the misses.
- Cold refuter (T-2414): dropped. It was to cut false alarms (19 on s70-010); the finders now raise none over 306
  scenarios, so a refuter could only lose true finds. Revisit if false alarms return.
- Canary mutation planter and a clean twin of a real repo: not run in gen 1; the replay answers the same question
  (do the finders see real defects?) more cheaply.

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
