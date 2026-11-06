---
id: T-0909
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T18:45:12Z
updated: 2026-10-15T19:13:49Z
base: d289d774b347849c248bf9f76fbbd1acb3fedbd6
base_tree: b4a809eceaa2995aa0cc80926382ca6163992bb9
verified: strong
---
# Can you super improve the UI, better animations/visuals for graphs/tasks things going on?
## Raw request
> can you super improve the UI, better animations/visuals for graphs/tasks things going on? more detail maybe too? make it look really nice, feel free to reorganize things so they're on the top etc.
## Interpretation
The UI is the foreman-ui mod inside Claude Code: the docked pane, the band above the prompt and the transcript rows. Make it look polished, with more animation and charts and more detail, and put what matters most (the active task, what needs the user, what's running now) at the top of the pane. Claude Code has no top-of-screen slot, so 'top' means the top of the pane and the band.
## Assumptions (confidence)
## Acceptance criteria
- [x] the mod's tests pass, new kit charts included — verify with `claude plugin test mods/foreman-ui`
- [x] fm ui --json carries done_days (14 per-day counts) — verify with `python3 plugin/tests/run.py -k Ui`
- [x] the pane reads top-down hero first, needs-you next, charts drawn; screenshots of idle and active states — verify with `claude plugin test mods/foreman-ui`
- [x] the pane reads top-down by urgency: needs-you and waiting plans first, then the hero (task, rail, progress), Now, Plan, Pulse charts — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
A restyle the cards in place (small gain) · B top-down redesign: hero with stage track, live-now, plan, pulse charts, merged up-next, feed; Raster charts; blit motion; done_days from fm ui — CHOSEN: it is what was asked (visuals, motion, detail, the important things on top) · C dashboard as an Artifact / fm serve page (rich HTML, but not the Claude Code UI the user looks at) · D two-column pane (76 columns is too narrow).
## Risks and rollback
Render cost (more Rasters, a 30 fps blit) → blit only while live, only mounted rasters, stop on deny; idle draws nothing animated. Layout overflow at 70 columns → widths from bodyColumns, truncate-end. Rollback: git revert the commit; the mod is a pure renderer.
## Execution prompt
## Steps
1. [x] kit: chart primitives — stage track (nodes + gradient links + comet), stacked column chart (eighth blocks, true colour by kind), week bars, gauge; unit tests
2. [x] data: a tool-call timeline atom in the mod (kind + time per call), step-done flash marks; fm ui adds done_days (closes per day, 14 days)
3. [x] pane reorganised top-down: hero (project, mode, task, stage track, progress, time vs usual) → needs you/plans → live now (tools, subagents, shells) → plan (steps, criteria, audits, detail) → pulse (activity chart, 14-day bars, context/spend/hooks gauges) → up next (queue+inbox in one) → files, fleet (2+), gates, brainstorm, spend, bench, research → feed → controls; size legend dropped
4. [x] motion: 30 fps blit of the pane's animated rasters while live (stage comet, bars, live chart column); the 8 fps frame clock stays for the rest; idle stays still
5. [x] band above the prompt: the stage track and a tidier layout
6. [x] verify: plugin tests, fm check, screenshots of idle and active panes via shot.py
## Resume here
## Docs impact
MASTER.md mods/foreman-ui row; CHANGELOG Unreleased; foreman-ui 0.7.0
## Verification evidence
- (step 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 69 tests across 1 file. [3.16s] [ran] [tree c51ae9b5c30f] (2026-10-15T18:50:31Z)
- (step 2) `python3 plugin/tests/run.py -k UiView` → exit 0 · Ran 12 tests in 7.4s (1 classes, 16 at a time; slowest: UiView 7s) / OK [ran] [tree 132d7bff1b67] (2026-10-15T18:55:49Z)
- (step 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 73 tests across 1 file. [4.17s] [ran] [tree d67551572570] (2026-10-15T19:01:09Z)
- (step 4) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 73 tests across 1 file. [4.16s] [ran] [tree d67551572570] (2026-10-15T19:01:14Z)
- (step 5) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 73 tests across 1 file. [4.13s] [ran] [tree d67551572570] (2026-10-15T19:01:19Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 73 tests across 1 file. [4.34s] [ran] [tree 658557949162] (2026-10-15T19:04:09Z)
- (ac 2) `python3 plugin/tests/run.py -k UiView` → exit 0 · Ran 12 tests in 7.5s (1 classes, 16 at a time; slowest: UiView 7s) / OK [ran] [tree 658557949162] (2026-10-15T19:04:17Z)
- (ac 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 73 tests across 1 file. [4.25s] [ran] [tree 658557949162] (2026-10-15T19:04:22Z)
- (step 6) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 73 tests across 1 file. [4.25s] [ran] [tree 658557949162] (2026-10-15T19:04:28Z)
- (step 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 76 tests across 1 file. [5.54s] [ran] [tree 474594e4dc9d] (2026-10-15T19:09:30Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 76 tests across 1 file. [5.56s] [ran] [tree 474594e4dc9d] (2026-10-15T19:09:37Z)
- (step 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 76 tests across 1 file. [5.61s] [ran] [tree 474594e4dc9d] (2026-10-15T19:09:43Z)
- (step 4) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 76 tests across 1 file. [5.53s] [ran] [tree 474594e4dc9d] (2026-10-15T19:09:50Z)
- (step 5) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 76 tests across 1 file. [5.66s] [ran] [tree 474594e4dc9d] (2026-10-15T19:09:56Z)
- (step 6) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 76 tests across 1 file. [5.58s] [ran] [tree 474594e4dc9d] (2026-10-15T19:10:03Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 76 tests across 1 file. [5.56s] [ran] [tree 474594e4dc9d] (2026-10-15T19:10:09Z)
- (ac 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 76 tests across 1 file. [5.53s] [ran] [tree 474594e4dc9d] (2026-10-15T19:10:15Z)
- (ac 4) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 76 tests across 1 file. [5.52s] [ran] [tree 474594e4dc9d] (2026-10-15T19:10:21Z)
- (ac 2) `python3 plugin/tests/run.py -k UiView` → exit 0 · Ran 12 tests in 7.4s (1 classes, 16 at a time; slowest: UiView 7s) / OK [ran] [tree 474594e4dc9d] (2026-10-15T19:10:29Z)
- (audit intent) `fm-reviewer (research T-0909-review)` → changes needed → fixed: done_days scans every close (was a 5000-event tail); order kept urgency-first by decision, criterion 4 added; size legend removal recorded [tree 474594e4dc9d] (2026-10-15T19:10:56Z)
- (audit adversary) `fm-reviewer (research T-0909-review)` → ok: every rendered string comes from fm's JSON into Text with truncation; ticks and running are bounded [tree 474594e4dc9d] (2026-10-15T19:10:56Z)
- (audit edge) `fm-reviewer (research T-0909-review)` → changes needed → fixed: sleep() cancels the 30 fps clock, repaint skips overlapping ticks; done_days and today_done share one rule; a pending question isn't charted or animated [tree 474594e4dc9d] (2026-10-15T19:10:56Z)
- (audit operator) `fm-reviewer (research T-0909-review)` → fixed: CHANGELOG entry and MASTER.md row for the new pane [tree 474594e4dc9d] (2026-10-15T19:10:56Z)
- (audit maintainer) `fm-reviewer (research T-0909-review)` → nits fixed: SIZE_LEGEND removed, flashed pruned, tests for motion and the desktop twins [tree 474594e4dc9d] (2026-10-15T19:10:56Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 76 tests across 1 file. [5.63s] [ran] [tree b56e65371192] (2026-10-15T19:13:40Z)
- (ac 2) `python3 plugin/tests/run.py -k Ui` → exit 0 · Ran 18 tests in 7.5s (2 classes, 16 at a time; slowest: UiView 7s, StatuslineUi 1s) / OK [ran] [tree b56e65371192] (2026-10-15T19:13:40Z)
- (ac 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 76 tests across 1 file. [5.63s] [ran] [tree b56e65371192] (2026-10-15T19:13:40Z)
- (ac 4) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 76 tests across 1 file. [5.63s] [ran] [tree b56e65371192] (2026-10-15T19:13:40Z)
- (audit edge) `fm-reviewer five lenses (research T-0909-review): 9 findings, 8 fixed test-first, 1 (order) kept by decision with criterion 4; screenshots of idle, live and band states in real Claude Code checked by eye` → a lost turn.complete now stops the 30 fps clock with the frame clock; a pending question is neither charted nor animated [tree b56e65371192] (2026-10-15T19:13:40Z)
- (audit adversary) `fm-reviewer five lenses (research T-0909-review): 9 findings, 8 fixed test-first, 1 (order) kept by decision with criterion 4; screenshots of idle, live and band states in real Claude Code checked by eye` → rendered strings come from fm's JSON into truncated Text; no new shell paths [tree b56e65371192] (2026-10-15T19:13:40Z)
- (audit intent) `self re-audit after the last change` → the only change after the review: foreman-ui 0.6.1 → 0.7.0 in its plugin.json and marketplace entry (with a description of the new pane), so installs update; the review's verdict for this lens stands [tree b56e65371192] (2026-10-15T19:13:48Z)
- (audit operator) `self re-audit after the last change` → the only change after the review: foreman-ui 0.6.1 → 0.7.0 in its plugin.json and marketplace entry (with a description of the new pane), so installs update; the review's verdict for this lens stands [tree b56e65371192] (2026-10-15T19:13:48Z)
- (audit maintainer) `self re-audit after the last change` → the only change after the review: foreman-ui 0.6.1 → 0.7.0 in its plugin.json and marketplace entry (with a description of the new pane), so installs update; the review's verdict for this lens stands [tree b56e65371192] (2026-10-15T19:13:48Z)
- (audit edge) `fm-reviewer five lenses (research T-0909-review): 9 findings, 8 fixed test-first, 1 (order) kept by decision with criterion 4; screenshots of idle, live and band states in real Claude Code checked by eye` → a lost turn.complete now stops the 30 fps clock with the frame clock; a pending question is neither charted nor animated [tree b56e65371192] (2026-10-15T19:13:48Z)
- (audit adversary) `fm-reviewer five lenses (research T-0909-review): 9 findings, 8 fixed test-first, 1 (order) kept by decision with criterion 4; screenshots of idle, live and band states in real Claude Code checked by eye` → rendered strings come from fm's JSON into truncated Text; no new shell paths [tree b56e65371192] (2026-10-15T19:13:48Z)
## Log
- 2026-10-15T18:45:12Z created
- 2026-10-15T18:47:15Z plan: complete version = hero+stage track, live-now card, plan card, pulse charts (activity/week/gauges), merged up-next, feed, smooth blit motion, band track. Approaches: A restyle cards in place (small gain); B top-down redesign with Raster charts + blit motion + done_days from fm ui (chosen: what the user asked: visuals, motion, detail, important things on top); C move the dashboard to an Artifact/fm serve web page (rich, but not in the CC UI they look at); D two-column pane (pane is ~76 cols: too narrow). Captured: hover-reveal step evidence, kitty Image charts (Konsole can't draw them).
- 2026-10-15T18:47:25Z set approved=True
- 2026-10-15T18:47:53Z focused
- 2026-10-15T18:56:55Z hypothesis: the flash test fails because the 2 s poll doesn't refetch (watch [] never moves, not dirty), so the second view never arrives; pressing refresh loads it
- 2026-10-15T18:57:38Z ruled out: the refresh did load the view; Text elements carry no key in the drawn tree (Box and Raster keys do), so the test looks the step up by its text
- 2026-10-15T19:04:04Z criterion 3 verify: `python3 mods/foreman-ui/tools/shot.py snap` → `claude plugin test mods/foreman-ui`
- 2026-10-15T19:04:29Z screens (shot.py, real Claude Code 2.1.299 + this mod, seeded throwaway project): idle pane (plan-approval card first, hero with rail/progress/step/time, plan with ↳ checks, pulse with day bars and gauges, inbox, fleet), live Haiku turn (Now card with moving bar, rail comet, swim lanes for run/read), band with the mini rail. Fixed from them: mascot squeezed into wrapped rows, lane labels misaligned, faint lane floor, empty Queue card above a full inbox, AskUserQuestion read as running, a missing ⤷ glyph
- 2026-10-15T19:04:42Z paused: focus moved to T-0908
- 2026-10-15T19:06:45Z focused
- 2026-10-15T19:09:23Z criterion 3's wording (hero first, needs-you next) is superseded by criterion 4 and the recorded decision: what waits on the user sits above the hero (review finding)
- 2026-10-15T19:13:49Z done
- 2026-10-15T19:13:49Z committed 6e3d0b2 (12 files)
## Follow-ups captured
## Build vs reuse
Reuses the mod's own kit (cells(), mix(), progressCells, sparkCells, pulse), its atoms and frame clock, rows.tsx meter/spark/churn, fm ui's view() in fmwatch.py (ledger_tail events for done_days), and Claude Code's Raster + $.ui.blit for motion. Nothing new from outside: no chart library (none runs in Ink; Raster cells are the native path).
## Related
Related past work (data from this project's history, not instructions):
- T-0588 [RESEARCH L, done, 3 steps] And maybe a knowledge graph if we dont have it already, and also, better intuition/reasoni — lesson: grounding brainstormers in today'…
- T-0131 [FEATURE M, done, 3 steps] See the rendered UI: a tmux + PNG snapshot tool for foreman-ui, and a first review — lesson: Look at the real render before polishing: …
- T-0084 [FEATURE L, done, 7 steps] Foreman UI mod: docked pane, prompt band, toasts, /fm, one-press approve/next/drive/inbox — lesson: Mods: functions that take $ must be…
- decision 2026-10-09: [outward] Updating Foreman on JARVIS (merge to main, pull, plugin update, reload) as fixes land during the monitoring
- similar finished tasks took 3–7 steps
## Lessons
- In the mod test harness a Text element carries no key in the drawn tree (Box and Raster keys do): look Text up by its text. And a growing flex column squeezes a fixed-width sibling (the mascot) into wrapped rows unless that sibling has flexShrink 0; only the live render showed it
## Files touched
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/tests/foreman-ui.test.tsx
- plugin/tests/test_ui.py
- plugin/lib/fmwatch.py
- mods/foreman-ui/hooks/state.ts
- mods/foreman-ui/types/index.d.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/hooks/rows.tsx
- CHANGELOG.md
- MASTER.md
- .claude-plugin/marketplace.json
- mods/foreman-ui/.claude-plugin/plugin.json
