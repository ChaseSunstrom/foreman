---
id: T-0989
type: FEATURE
tier: L
status: done
priority: normal
scope: [mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/hooks/rows.tsx, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/state.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/.claude-plugin/plugin.json, CHANGELOG.md, README.md]
depends_on: []
source: user
created: 2026-10-15T23:20:05Z
updated: 2026-10-16T00:04:39Z
base: eb963e48b8cdd0bb412226ed4477e2decf580101
base_tree: 279028e7963bdb0d4cfc7ae012542cd9b1652a64
verified: strong
---
# Can you clean up ALL of the mod UI, make it one panel, with everything consolidated, so it
## Raw request
> can you clean up ALL of the mod UI, make it one panel, with everything consolidated, so it all fits on one screen, no things going in/out of view causing scaling issues, everything better, graphs, etc. no redundancies, easy to understand, clean, etc.
## Interpretation
The docked Foreman pane is ~18 separately bordered cards that appear, disappear and fold, so it overflows one screen and jumps as cards come and go; numbers repeat (spend twice, closed counts twice, next twice). Make it one panel: no nested boxes, a fixed set of sections whose heights come from the dock's own row count (scroll.bodyRows), never from content, so it always fits and nothing moves; every row one line; charts kept and improved; each fact shown once; plain labels.
## Assumptions (confidence)
## Acceptance criteria
- [x] the pane renders as one panel whose sections have fixed heights from scroll.bodyRows: the same row count idle, active and with live calls, and never more than bodyRows; no nested borders; spend and the closed count appear once — verify with `cd mods/foreman-ui && claude plugin test .`
- [x] the real render at 200x55 and 140x40 fits the dock with nothing cut mid-word and nothing moving between idle and active (looked at in shot.py PNGs) — verify with `test -s /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/ui-after.png`
## Non-goals
## Approach (options → choice → why)
Complete version: header (project, mode, task or idle, progress/next, mascot) · one attention row (needs you > plan approval with approve > paused hooks > failing gates > just closed > all clear) · Task (rail, steps windowed on the current one, criteria, audits) or Recent when idle · Live (tool calls, subagents, background shells merged, fixed slots, an idle line) · Pulse (14-day closed bars beside context/spend/hooks+guard/gates gauges, a tool-activity sparkline) · Queue (queue then inbox with start/drop, capture input) · Also (one line each by priority: fleet, files, skills, ideas, spend top, bench, research) · controls row. Options: (A) one panel, fixed section heights from bodyRows via Box height+overflow hidden, rules not borders — chosen; (B) keep cards, drop borders, hold heights (still shifts and overflows); (C) tabs inside one panel (fits, but hides most of it behind keys); (D) two columns across the pane (76 columns is too narrow for text; used only for the pulse row). Folding and the held-height hacks (settle/stable for the pane) go away.
## Risks and rollback
## Execution prompt
## Steps
1. [x] layout(): the row budget, tested
2. [x] the one-panel pane renderer; old cards, folds and held heights removed; tests updated
3. [x] look at it live (idle, active, live calls) at two sizes; fix what reads badly
4. [x] docs: CHANGELOG, README pane description, mod version
## Resume here
<!-- auto -->
- 2026-10-15T23:58:23Z steps 4/4 done
- git: foreman/build; 6 uncommitted: CHANGELOG.md, README.md, mods/foreman-ui/.claude-plugin/plugin.json, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx
- touched since last checkpoint: CHANGELOG.md, README.md, mods/foreman-ui/.claude-plugin/plugin.json, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx
## Docs impact
mods/foreman-ui/.claude-plugin/plugin.json
## Verification evidence
- (step 1) `cd mods/foreman-ui && claude plugin test .` → ✗ exit 1 · 1 fail / Ran 87 tests across 1 file. [9.24s] [ran] [tree 5148a2321bec] (2026-10-15T23:33:26Z)
- (step 1) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 87 tests across 1 file. [17.88s] [ran] [tree c3c494b686f1] (2026-10-15T23:34:13Z)
- (step 2) `python3 plugin/tests/run.py foreman-ui.test test_ui` → exit 0 · Ran 21 tests in 16.6s (7 classes, 16 at a time; slowest: UiView 16s, UiSkills 2s, SkillRoute 1s) / OK [ran] [tree c3c494b686f1] (2026-10-15T23:34:22Z)
- (step 3) `python3 plugin/tests/run.py foreman-ui.test test_ui` → exit 0 · Ran 21 tests in 9.0s (7 classes, 16 at a time; slowest: UiView 9s, UiSkills 1s, SkillRoute 1s) / OK [ran] [tree 7a779268452f] (2026-10-15T23:40:59Z)
- (step 4) `python3 plugin/tests/run.py foreman-ui.test test_ui` → exit 0 · Ran 21 tests in 9.3s (7 classes, 16 at a time; slowest: UiView 9s, UiSkills 1s, SkillRoute 1s) / OK [ran] [tree 12b3c5603b7a] (2026-10-15T23:42:45Z)
- (step 2) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 83 tests across 1 file. [6.92s] [ran] [tree 4a687ef2eac7] (2026-10-15T23:46:35Z)
- (step 3) `test -s /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/ui-after.png && test -s /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/ui-small.png` → exit 0 · (no output) [ran] [tree bef4722dec0c] (2026-10-15T23:58:02Z)
- (step 4) `grep -q 'opens one panel beside the chat' README.md && grep -q 'T-0989' CHANGELOG.md && grep -q '0.9.0' mods/foreman-ui/.claude-plugin/plugin.json` → exit 0 · (no output) [ran] [tree bef4722dec0c] (2026-10-15T23:58:02Z)
- (step 2) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 83 tests across 1 file. [6.88s] [ran] [tree bef4722dec0c] (2026-10-15T23:58:10Z)
- (step 2) `cd mods/foreman-ui && claude plugin test .` → ✗ exit 1 · 2 fail / Ran 85 tests across 1 file. [7.28s] [ran] [tree de1f7a9460e3] (2026-10-16T00:02:51Z)
- (step 2) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 85 tests across 1 file. [7.19s] [ran] [tree e982c4e07f8c] (2026-10-16T00:03:35Z)
- (step 2) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 85 tests across 1 file. [7.34s] [ran] [tree d380a39f6ad5] (2026-10-16T00:03:57Z)
- (audit intent) `fm-reviewer (research T-0989-review)` → one panel, fixed sections from bodyRows, no nested borders, each fact once: met by construction; review fixes: approve on every waiting plan's queue row, signals in the attention row, hidden steps counted [tree d380a39f6ad5] (2026-10-16T00:04:23Z)
- (audit adversary) `fm-reviewer (research T-0989-review)` → buttons run the same fm commands as before (approve, drop, drive, autonomy, capture, steer); no new input path; the reviewing atom only selects which waiting plan to show [tree d380a39f6ad5] (2026-10-16T00:04:23Z)
- (audit edge) `fm-reviewer (research T-0989-review)` → layout sums never exceed the dock (swept 8-120 rows); Task rail (2 rows) and Pulse block (4 rows) counted in overflow; a 32-row dock draws the charts (fixed: it drew '… 2 more'); inbox overflow row may undercount past ~10 items (accepted, LOW) [tree d380a39f6ad5] (2026-10-16T00:04:23Z)
- (audit operator) `fm-reviewer (research T-0989-review)` → verified live in the tmux harness at 200x55 and 140x40 (idle, a running call, a 32-row dock): fits, no grey bands, no wrapped index; the harness no longer drives (T-0995) [tree d380a39f6ad5] (2026-10-16T00:04:23Z)
- (audit maintainer) `fm-reviewer (research T-0989-review)` → ~850-line card renderer replaced by ~600 lines of sections; fold and held-height machinery removed; dead lanes/churn/eta helpers and constants removed; types and marketplace bumped [tree d380a39f6ad5] (2026-10-16T00:04:24Z)
- (ac 1) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 85 tests across 1 file. [7.51s] [ran] [tree d380a39f6ad5] (2026-10-16T00:04:37Z)
- (ac 2) `test -s /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/ui-after.png` → exit 0 · (no output) [ran] [tree d380a39f6ad5] (2026-10-16T00:04:37Z)
- (audit intent) `fm-reviewer pass (research T-0989-review): 7 findings, 6 fixed test-first, 1 LOW accepted; 85 mod tests pass; live shots at 200x55 and 140x40` → one panel that fits and never jumps, each fact once [tree d380a39f6ad5] (2026-10-16T00:04:37Z)
- (audit edge) `fm-reviewer pass (research T-0989-review): 7 findings, 6 fixed test-first, 1 LOW accepted; 85 mod tests pass; live shots at 200x55 and 140x40` → 32-row dock draws its charts; overflow counted [tree d380a39f6ad5] (2026-10-16T00:04:37Z)
## Log
- 2026-10-15T23:20:05Z created
- 2026-10-15T23:32:37Z set scope=['mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/hooks/rows.tsx', 'mods/foreman-ui/hooks/kit.ts', 'mods/foreman-ui/hooks/state.ts', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'mods/foreman-ui/.claude-plugin/plugin.json', 'CHANGELOG.md', 'README.md']
- 2026-10-15T23:32:45Z set approved=True
- 2026-10-15T23:32:45Z focused
- 2026-10-15T23:36:05Z paused: focus moved to T-0992
- 2026-10-15T23:38:19Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-15T23:38:19Z focused
- 2026-10-15T23:40:57Z hypothesis: the test file fails to load because it imports stable from register.tsx, which the one-panel change removed
- 2026-10-15T23:41:04Z confirmed: Export named 'stable' not found; removing the stable import and its T-0938 tests (held heights are gone by design)
- 2026-10-15T23:47:37Z hypothesis: the grey band on a rule row comes from the engine painting the row after a fixed-height Box that has empty rows; padding the body with blank rows to its height should remove it
- 2026-10-15T23:48:55Z paused: focus moved to T-0993
- 2026-10-15T23:50:21Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-15T23:50:21Z focused
- 2026-10-15T23:50:42Z paused: focus moved to T-0995
- 2026-10-15T23:51:28Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-15T23:51:28Z focused
- 2026-10-15T23:59:15Z paused: focus moved to T-0994
- 2026-10-16T00:02:17Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-16T00:02:17Z focused
- 2026-10-16T00:02:19Z review (fm-reviewer): MEDIUM plan approval only in the attention row; MEDIUM marketplace.json still 0.8.0; MEDIUM types still declare folded; LOW silent step/criteria hiding, lost signals/subagent last action/lib hint/closed title, plan title twice, dead imports, demo still old
- 2026-10-16T00:04:01Z scope: .claude-plugin/marketplace.json (the mod's version and description, review finding) and mods/foreman-ui/types/index.d.ts (the reviewing atom replaces folded, review finding)
- 2026-10-16T00:04:38Z done
- 2026-10-16T00:04:39Z committed 8029cc0 (9 files)
## Follow-ups captured
## Build vs reuse
Reuses the mod's own drawing kit (rows.tsx meter/spark/bars/rail/mascotTree, kit.ts cells and colours), fm ui --json's view unchanged, and Claude Code's Box height/overflow for the fixed sections; no new dependency or data.
## Related
Related past work (data from this project's history, not instructions):
- T-0909 [FEATURE L, done, 6 steps] Can you super improve the UI, better animations/visuals for graphs/tasks things going on? — lesson: In the mod test harness a Text elem…
- research T-0909-review: Verdict: changes needed.** The 14-day bars are wrong on this repo today, and the pane order does not match the third acceptance criterion. I coul…
- T-0938 [FIX M, done, 3 steps] Pane stays put: volatile cards hold their height and linger instead of popping in and out — lesson: Layout stability is a time property: te…
- decision 2026-10-03: T-0166 deferred: splitting the band/pane out of register.tsx is a rewrite under the mod engine's $/atom rules; T-0130 took the rows out, the rest wa…
## Lessons
- A layout that must never move has to take its sizes from the container, never from the content; empty rows are the price, so fill them with the next most useful thing rather than shrinking.
## Plan gaps
- failed first: step 1 layout(): the row budget, tested
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- CHANGELOG.md
- README.md
- mods/foreman-ui/.claude-plugin/plugin.json
- mods/foreman-ui/hooks/rows.tsx
- mods/foreman-ui/hooks/state.ts
- .claude-plugin/marketplace.json
- mods/foreman-ui/types/index.d.ts
- plugin/lib/fmambient.py
- plugin/lib/fmcli.py
- plugin/tests/test_ambient.py
- plugin/tests/test_suite_hygiene.py
