---
id: T-1350
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, CHANGELOG.md, README.md]
depends_on: []
source: followup
created: 2026-10-21T03:47:40Z
updated: 2026-10-23T14:21:53Z
base: 6b893c906cd82a1e78175b9d59f1a432ec951417
base_tree: 84657d13ba0ac3adfcbddd0076b61b69814e929a
plan0_at: 2026-10-23T14:19:38Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, CHANGELOG.md, README.md]
verified: strong
---
# Fm code queue as tickets (U15, after T-1330): n during a run captures the request as a tic
## Raw request
> fm code queue as tickets (U15, after T-1330): n during a run captures the request as a ticket on a rail under the track that starts when the run ends; in the queue view space picks and arrows reorder
## Interpretation
During a run, n opens the box as a question (T-1770: ask ›). A request for after this run has nowhere to go but memory. Tab in that box switches it to next ›: Enter then puts the request on a rail of tickets drawn under the track (① … ② …), and when the run ends the first ticket starts as the next run, and so on (a blocked or stopped run holds the rail, said in Activity). T opens the rail as a list where space picks a ticket up, arrows move it, space puts it down, and Delete drops one. Tickets live in this app session; quitting with tickets left lists them in the scrollback.
## Assumptions (confidence)
## Acceptance criteria
- [x] Tab turns the during-run box into next ›; Enter puts a ticket on the rail under the track; a closed run starts the first ticket, a blocked one holds the rail and says so; T lists them, space picks and puts down, arrows move, Delete drops; tickets left on quit are listed in the scrollback — verify with `python3 plugin/tests/run.py test_code_tui`
## Non-goals
## Approach (options → choice → why)
Complete version: capture without leaving the run, the rail visible, order editable, the hand-off at run end honest about blocks, nothing lost silently on quit. Options: in-app tickets (chosen: what was asked, no state to keep in sync), fm capture each one (an inbox item needs planning before fm code --task can work it), fm queue order (the project's queue is planned briefs; a ticket is a raw request).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: the box, the rail, the hand-off, the view
2. [x] tickets in the app, the rail, the view and its keys, the quit note; CHANGELOG and README
## Resume here
## Docs impact
README.md (fm code tui paragraph: tickets), CHANGELOG.md; the help poster lists T (tickets)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_tui` → ✗ exit 1 · Ran 228 tests in 8.1s (44 classes, 16 at a time; slowest: Fuzz 8s, Command 7s, Events 3s) / FAILED (1 classes) [ran] [tree e3d64b9a4d1a] (2026-10-23T14:20:00Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 228 tests in 12.8s (44 classes, 16 at a time; slowest: Command 12s, Fuzz 12s, Events 6s) / OK [ran] [tree 543c831803c2] (2026-10-23T14:21:12Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui test_suite_hygiene test_settings test_docs` → exit 0 · Ran 408 tests in 11.4s (83 classes, 16 at a time; slowest: Command 10s, Fuzz 10s, Fences 9s) / OK [ran] [tree 543c831803c2] (2026-10-23T14:21:24Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 228 tests in 8.1s (44 classes, 16 at a time; slowest: Fuzz 8s, Command 8s, Events 3s) / OK [ran] [tree 543c831803c2] (2026-10-23T14:21:33Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 228 tests in 8.1s (44 classes, 16 at a time; slowest: Fuzz 8s, Command 8s, Events 3s) / OK [ran] [tree 543c831803c2] (2026-10-23T14:21:41Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): the box keeps asking as its default (T-1770) and Tab switches to a ticket and back; a ticket starts only after a close, never after a block or a stop (said in Activity), and never while the queue (g) runs; the rail draws under the track with each ticket cut to 24 columns and printable; the list view joined the hostile-width sweep; tickets are this session's, and the ones left are printed on quit` → a request thought of mid-run is captured without interrupting the run and runs right after it [tree 543c831803c2] (2026-10-23T14:21:41Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): the box keeps asking as its default (T-1770) and Tab switches to a ticket and back; a ticket starts only after a close, never after a block or a stop (said in Activity), and never while the queue (g) runs; the rail draws under the track with each ticket cut to 24 columns and printable; the list view joined the hostile-width sweep; tickets are this session's, and the ones left are printed on quit` → more tickets than circled numbers (the rail shows nine; the list numbers the rest), a / command in the box (Tab completes it), Delete on an empty list, a held ticket at either end, quitting with tickets left [tree 543c831803c2] (2026-10-23T14:21:41Z)
## Log
- 2026-10-21T03:47:40Z created
- 2026-10-23T14:14:58Z set tier=M, scope=['plugin/lib/fmcodetui.py', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md', 'README.md']
- 2026-10-23T14:19:38Z focused
- 2026-10-23T14:20:58Z set scope=['plugin/lib/fmcodetui.py', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md', 'README.md']
- 2026-10-23T14:21:52Z done
- 2026-10-23T14:21:53Z committed 8ebdea8b (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1340 [FEATURE M, done, 1 steps] Fm code follow-ups (R22+U22): fm code --after T-ID "<follow-up>" (and Enter after a close — lesson: Before adding an attribute to a cla…
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- research T-1511-review: Verdict: changes needed.** The runner test is sound. Key capture can lock the user out of list navigation, and two other findings are real but na…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, README.md, plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py; re-ground the plan against them before editing
## Lessons
- Default a shared key to its existing meaning and add the new one behind a toggle, so earlier habits keep working
## Plan gaps
- failed first: step 1 red tests: the box, the rail, the hand-off, the view
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodetui.py
- CHANGELOG.md
- README.md
