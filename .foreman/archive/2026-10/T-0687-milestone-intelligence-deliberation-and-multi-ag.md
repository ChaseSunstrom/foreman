---
id: T-0687
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:17Z
updated: 2026-10-09T20:02:00Z
batch: [T-0642, T-0662]
base: 5a60245f826fd6409b362b2b0eacc952a509886b
base_tree: 0082d57555af3c1bd420f0370696f31f53f0e692
verified: strong
---
# Milestone: Intelligence — Deliberation and multi-agent thinking
## Raw request
> T-0642: FEATURE: Dissent that survives (I097, value 3/5, effort S, risk low)
>   first version: Save refuted/unresolved objections as a Dissent section in the brief and make fm task done list those still open. Small extension of fm second.
>   what it is: Keeps minority reports, dissent registers and what-we-did-not-discuss sections.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 6 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0662: FEATURE: Panel design and roles (I096, value 3/5, effort M, risk low)
>   first version: Make panel charters data: a protocols file naming roles, count and stop rule, sized by tier/risk, reused by fm ideas and fm second. First step: a size-by-stakes rule so S tasks skip panels and L get fm second plan automatically.
>   what it is: Fixes the panel's charter, roles and protocols as data, and sizes the panel by the stakes.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 14 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Do T-0642, T-0662 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0687. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0642: Dissent that survives (I097, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_deliberation.py -k Dissent`
- [x] T-0662: Panel design and roles (I096, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_deliberation.py -k Panel`
## Non-goals
## Approach (options → choice → why)
T-0642: fm second plan also writes each objection as an open item in a Dissent section; fm task dissent ID add|resolve N manages it; the close lists dissent still open (a warning: an unanswered objection is information, not a veto). T-0662: panel charters as data — plugin/protocols.json says per tier what deliberation runs (S: none; M: optional; L: fm second plan before approval); fm second plan on an S task says it's skipped unless --force, and fm next on an unapproved L plan without a Plan review names fm second plan. Options: a voting panel per decision, or dissent as a gate — more calls and friction than the evidence supports.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0642: Dissent that survives (I097, value 3/5, effort S, risk low)
2. [x] T-0662: Panel design and roles (I096, value 3/5, effort M, risk low)
## Resume here
## Docs impact
CHANGELOG; MASTER.md (fmsecond); plugin/protocols.json
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_deliberation.py` → ✗ exit 1 · Ran 2 tests in 0.4s (2 classes, 16 at a time; slowest: Dissent 0s, Panel 0s) / FAILED (2 classes) [ran] [tree 5dbc349e94b1] (2026-10-09T20:00:01Z)
- (step 1) `python3 plugin/tests/run.py -p test_deliberation.py -k Dissent` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Dissent 1s) / OK [ran] [tree e6682e691783] (2026-10-09T20:00:49Z)
- (step 2) `python3 plugin/tests/run.py -p test_deliberation.py -k Panel` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Panel 1s) / OK [ran] [tree e6682e691783] (2026-10-09T20:00:50Z)
- (ac 1) `python3 plugin/tests/run.py -p test_deliberation.py -k Dissent` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Dissent 1s) / OK [ran] [tree c75905e154b6] (2026-10-09T20:01:59Z)
- (ac 2) `python3 plugin/tests/run.py -p test_deliberation.py -k Panel` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Panel 1s) / OK [ran] [tree c75905e154b6] (2026-10-09T20:01:59Z)
- `python3 plugin/tests/run.py` → exit 0 · Ran 1182 tests in 67.7s (359 classes, 16 at a time; slowest: Stop 43s, TaskLifecycle 28s, Bench 25s) / OK [ran] [tree c75905e154b6] (2026-10-09T20:01:59Z)
- (audit intent) `self review of both members; the full suite runs as the close's final check` → both first versions shipped as noted: open objections survive in the brief and show at close; S tasks skip the plan panel and L plans are pointed at one before approval [tree c75905e154b6] (2026-10-09T20:01:59Z)
- (audit edge) `self review of both members; the full suite runs as the close's final check` → an objection already recorded isn't added twice on a second review; resolve names a missing number; dissent warns at close, it never blocks; a broken protocols.json means no skipping [tree c75905e154b6] (2026-10-09T20:01:59Z)
## Log
- 2026-10-09T15:40:17Z created
- 2026-10-09T19:59:47Z criterion 1 verify: `` → `python3 plugin/tests/run.py -p test_deliberation.py -k Dissent`
- 2026-10-09T19:59:47Z criterion 2 verify: `` → `python3 plugin/tests/run.py -p test_deliberation.py -k Panel`
- 2026-10-09T19:59:47Z focused
- 2026-10-09T20:02:00Z done
- 2026-10-09T20:02:00Z committed 6c93555 (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0674 [FEATURE M, done, 3 steps] Milestone: Features — Observability, replay and trust — lesson: Check where secrets enter before adding redaction: every write path her…
- T-0676 [FEATURE M, done, 7 steps] Milestone: Features — Performance and cost — lesson: A 'degrade when over pace' rule must name what is optional: side offers and self-i…
- T-0673 [FEATURE M, done, 7 steps] Milestone: Features — Multi-machine, multi-project and ecosystem — lesson: a capture into another project must not run that project's e…
- decision 2026-10-09: Self-approve T-0679 (FEATURE L, first versions only)
- similar finished tasks took 3–7 steps
## Lessons
- Deliberation should cost by stakes, and its output should outlive the review: open objections in the brief, closed by an answer
## Files touched
- plugin/tests/test_deliberation.py
- plugin/protocols.json
- plugin/lib/fmsecond.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- CHANGELOG.md
- MASTER.md
