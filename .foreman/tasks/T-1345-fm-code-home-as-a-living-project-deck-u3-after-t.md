---
id: T-1345
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/lib/fmwatch.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-21T03:47:33Z
updated: 2026-10-23T14:18:58Z
base: 71c0ed31154e77fd2426f3870b894acd12f0a206
base_tree: 4e31c78d89d5b1fc462ebfc55e2e190fe6a0e722
plan0_at: 2026-10-23T14:16:35Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/lib/fmwatch.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
verified: strong
---
# Fm code home as a living project deck (U3, after T-1330): projects as cards (mini station
## Raw request
> fm code home as a living project deck (U3, after T-1330): projects as cards (mini station track, queue depth, blocked/inbox badges, runner glyph), a focus ring that glides between them, Enter morphs the card into its run view; motion reduced/off draws the end state
## Interpretation
The app's home lists every Foreman project as one text row. A deck reads faster: each project a card with its name, a mini station track of the active task (plan, steps, checks, close, lit to its stage), its task, queue/inbox/blocked badges (blocked red, inbox dim), and the project's runner as a glyph. The selected card wears a focus ring that glides from the last card to the new one; Enter grows the card to the full screen as the project view opens. With motion reduced or off the end state is drawn: the ring where it lands, the view at once. Narrow screens get one column of cards.
## Assumptions (confidence)
## Acceptance criteria
- [x] the home draws a card per project with track, task, badges and runner; arrows move the focus by card in a grid; the ring glides and Enter grows the card under full motion, and both land at once with motion off — verify with `python3 plugin/tests/run.py test_code_tui`
## Non-goals
## Approach (options → choice → why)
Complete version: cards in as many columns as fit, every field fm projects has (active stage and steps, counts, runner), noticed and error and gone projects as cards too, arrows moving by column and row, the glide and the grow honest under motion settings, and the CJK width safety the rows have. Options: a card grid drawn on the canvas as a new view beside the list (chosen: the list view stays for the project view), restyle the rows only (not a deck), a separate curses-like widget layer (no). fm projects --json gains the runner (meta code_runner), a stat already loaded.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: the cards, the grid keys, the glide and grow
2. [x] the deck view, the runner field, the motion; CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md; the home's own note line names its keys; fm projects --json's runner field (plugin/lib/fmwatch.py)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_tui` → ✗ exit 1 · Ran 225 tests in 8.2s (43 classes, 16 at a time; slowest: Fuzz 8s, Command 7s, Events 3s) / FAILED (2 classes) [ran] [tree 951000c05ae7] (2026-10-23T14:16:57Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 225 tests in 8.1s (43 classes, 16 at a time; slowest: Fuzz 8s, Command 7s, Events 3s) / OK [ran] [tree 84657d13ba0a] (2026-10-23T14:17:43Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui test_suite_hygiene test_cli` → exit 0 · Ran 352 tests in 24.1s (82 classes, 16 at a time; slowest: TaskLifecycle 24s, Command 10s, Fuzz 10s) / OK [ran] [tree 84657d13ba0a] (2026-10-23T14:18:08Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 225 tests in 8.2s (43 classes, 16 at a time; slowest: Fuzz 8s, Command 7s, Events 3s) / OK [ran] [tree 84657d13ba0a] (2026-10-23T14:18:17Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 225 tests in 8.1s (43 classes, 16 at a time; slowest: Fuzz 8s, Command 7s, Events 3s) / OK [ran] [tree 84657d13ba0a] (2026-10-23T14:18:34Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): the deck replaces the home's rows (the old row function removed: the hygiene test would flag it); cards hold every kind the rows did (noticed, error, gone, active, idle), a runner name is printable text only, 20 characters; arrows move by card using the columns the last frame drew (1 before any frame, so keys before a render move as before); the grow is drawing only, so Enter opens the project at once and state never waits on an animation; rendered with this machine's 19 projects at 130 columns: three columns, badges and gone folders read clearly` → the home shows each project's state at a glance as a card, and moving between them and into one feels continuous [tree 84657d13ba0a] (2026-10-23T14:18:34Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): the deck replaces the home's rows (the old row function removed: the hygiene test would flag it); cards hold every kind the rows did (noticed, error, gone, active, idle), a runner name is printable text only, 20 characters; arrows move by card using the columns the last frame drew (1 before any frame, so keys before a render move as before); the grow is drawing only, so Enter opens the project at once and state never waits on an animation; rendered with this machine's 19 projects at 130 columns: three columns, badges and gone folders read clearly` → one project (one column), a narrow screen (one column), more cards than fit (it scrolls to keep the selected one), a CJK name and a long title (cut with …, the border kept), motion reduced or off (ring and view land at once), no projects (says how to make one) [tree 84657d13ba0a] (2026-10-23T14:18:34Z)
## Log
- 2026-10-21T03:47:33Z created
- 2026-10-23T13:59:14Z set tier=M, scope=['plugin/lib/fmcodetui.py', 'plugin/lib/fmwatch.py', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md']
- 2026-10-23T14:16:35Z focused
- 2026-10-23T14:18:56Z done
- 2026-10-23T14:18:58Z committed 6b893c90 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Terminal and mod UI (fm playbooks show ui/terminal-ui)
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- T-1305 [FEATURE S, done, 1 steps] Fm code tui close receipt: on close a receipt card (task, checks, files, tokens, time, com
- decision 2026-10-21: T-1330 approved by self-critique (full autonomy): the app is views inside fm code tui's existing App; --task works a planned brief with a per-task l…
- similar finished tasks took 1–3 steps
- start here (files T-1762 touched): plugin/tests/test_code_tui.py, plugin/lib/fmcodetui.py, CHANGELOG.md, MASTER.md
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, plugin/lib/fmcodetui.py, plugin/lib/fmwatch.py, plugin/tests/test_code_tui.py; re-ground the plan against them before editing
## Lessons
- Animate transitions as drawing over state that already changed: tests and keys never wait on motion
## Plan gaps
- failed first: step 1 red tests: the cards, the grid keys, the glide and grow
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmwatch.py
- CHANGELOG.md
