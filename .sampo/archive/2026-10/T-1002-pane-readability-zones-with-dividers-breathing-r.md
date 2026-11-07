---
id: T-1002
type: FEATURE
tier: M
status: done
priority: normal
scope: [mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/rows.tsx, mods/foreman-ui/hooks/state.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/.claude-plugin/plugin.json, .claude-plugin/marketplace.json, README.md, CHANGELOG.md, plugin/lib/fmwatch.py]
depends_on: []
source: user
created: 2026-10-16T00:24:33Z
updated: 2026-10-16T01:00:04Z
base: 59869e15d84baa3bb5f3f0e13e6cc444914cb4cc
base_tree: c1e05b25eac5d838f23526862279d9014be8a4e6
inferred_deps: [T-0166]
inferred_why: T-0166: readability edits are easier once the pane is moved out
group: foreman-ui pane work
verified: strong
---
# Pane readability: zones with dividers, breathing room between sections, aligned label/picture/value rows, fewer facts per line; still fills the dock exactly
## Raw request
> Pane readability: zones with dividers, breathing room between sections, aligned label/picture/value rows, fewer facts per line; still fills the dock exactly
## Interpretation
The user on the filled panel: 'everything feels scrunched together and too close and it's hard to digest… organize it correctly, you can have dividers and stuff and it all needs to be easy to understand'. Keep filling the dock exactly, but give it structure: zones split by dividers, blank rows between sections, plain titles, one picture and one value per row in aligned columns.
## Assumptions (confidence)
## Acceptance criteria
- [x] layout(rows, plan) fills the dock exactly with titled dividers and the gaps above them counted; sections never exceed what they hold — verify with `cd mods/foreman-ui && claude plugin test .`
- [x] live render at 200x55 and 140x40: titled sections, an Activity lane plot, tank gauges instead of small bars, History filling to the controls — verify with `test -s /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/ui-remake.png && test -s /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/ui-remake-small.png`
## Non-goals
## Approach (options → choice → why)
Options: (1) four zones (status: head, hero, attention | work: Task, Live | board: Queue, Sessions, Usage, Recent | health: charts) with a divider between zones and a blank row between sections in a zone, spacing counted by layout so the panel still ends at the dock's bottom; spec-sheet rows (label column, picture column, value) — chosen; (2) tabs/pages inside the pane (less on screen, but hides most of it); (3) only add blank rows to the current layout (still mixed alignment and middot-chained lines, the real cause of 'hard to digest'). Spend moves to Usage only; the closed count lives in Health; revisit and 'you said' go back to the attention row.
## Risks and rollback
## Execution prompt
## Steps
1. [x] layout over a plan of sections and zones, tested
2. [x] renderer: zones, dividers, titled sections, aligned rows, hero block
3. [x] look at it live at two sizes; docs
## Resume here
<!-- auto -->
- 2026-10-16T00:31:29Z step 1/3: layout over a plan of sections and zones, tested
- git: foreman/build; 3 uncommitted: mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/pane3.tsx, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `cd mods/foreman-ui && claude plugin test .` → ✗ exit 1 · 1 fail / Ran 85 tests across 1 file. [7.40s] [ran] [tree 6d1b5eeb9ba1] (2026-10-16T00:25:09Z)
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 86 tests across 1 file. [6.97s] [ran] [tree d9e64adea105] (2026-10-16T00:49:18Z)
- (step 2) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 86 tests across 1 file. [7.11s] [ran] [tree d9e64adea105] (2026-10-16T00:49:26Z)
- (step 3) `python3 plugin/tests/run.py test_ui` → exit 0 · Ran 21 tests in 9.0s (7 classes, 16 at a time; slowest: UiView 9s, UiSkills 1s, CloseOut 1s) / OK [ran] [tree f8524430bce6] (2026-10-16T00:52:33Z)
- (step 3) `test -s /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/ui-remake.png && test -s /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/ui-remake-small.png && python3 plugin/tests/run.py test_ui` → exit 0 · Ran 21 tests in 8.0s (7 classes, 16 at a time; slowest: UiView 8s, UiSkills 1s, CloseOut 1s) / OK [ran] [tree ea91db325759] (2026-10-16T00:53:39Z)
- (ac 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 87 tests across 1 file. [7.42s] [ran] [tree ea91db325759] (2026-10-16T00:53:51Z)
- (ac 2) `test -s /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/ui-remake.png && test -s /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/ui-remake-small.png` → exit 0 · (no output) [ran] [tree ea91db325759] (2026-10-16T00:53:52Z)
- (step 2) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 90 tests across 1 file. [7.59s] [ran] [tree 309363f79c2b] (2026-10-16T00:59:31Z)
- (ac 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 90 tests across 1 file. [7.13s] [ran] [tree 309363f79c2b] (2026-10-16T00:59:39Z)
- (audit intent) `fm-reviewer` → 1 medium (plan cut silently) fixed with a counted last row; criteria list → proved count is the user's declutter ask (decision recorded) [tree 309363f79c2b] (2026-10-16T00:59:39Z)
- (audit edge) `fm-reviewer` → short task block window, narrow Today, stop button, lane swaps, controls gap, off-terminal width: fixed test-first (3 new tests); 5th plan's approve on a 24-row dock left (plan 1's approve stays in the attention row) [tree 309363f79c2b] (2026-10-16T00:59:39Z)
- (ac 1) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 90 tests across 1 file. [6.95s] [ran] [tree 309363f79c2b] (2026-10-16T01:00:03Z)
- (ac 2) `test -s /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/ui-remake.png && test -s /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/ui-remake-small.png` → exit 0 · (no output) [ran] [tree 309363f79c2b] (2026-10-16T01:00:03Z)
- (audit edge) `fm-reviewer pass (intent, edge) + live renders at 200x55 and 140x40 with a real Haiku session's calls` → short and narrow docks: task window keeps the current step and counts the rest, Today drops the days before clipping tanks, stop button keeps its cells (3 new tests) [tree 309363f79c2b] (2026-10-16T01:00:03Z)
- (audit intent) `fm-reviewer pass (intent, edge) + live renders at 200x55 and 140x40 with a real Haiku session's calls` → decluttered per the user's ask; dropped facts stay in fm (decision recorded) [tree 309363f79c2b] (2026-10-16T01:00:03Z)
## Log
- 2026-10-16T00:24:33Z created
- 2026-10-16T00:24:34Z focused
- 2026-10-16T00:33:59Z steer: user after reload — still cluttered, graphs too big, liked the old plot chart, panel must be completely filled, drop the small horizontal bars (make them one bigger graph), declutter text, completely remake
- 2026-10-16T00:40:33Z set scope=['mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/hooks/kit.ts', 'mods/foreman-ui/hooks/rows.tsx', 'mods/foreman-ui/hooks/state.ts', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'mods/foreman-ui/.claude-plugin/plugin.json', '.claude-plugin/marketplace.json', 'README.md', 'CHANGELOG.md', 'plugin/lib/fmwatch.py']
- 2026-10-16T00:40:33Z scope: + state.ts (skill lane), plugin/lib/fmwatch.py (24 history lines so History fills the dock)
- 2026-10-16T00:49:07Z criterion 1 text: layout(rows, plan) fills the dock exactly with zone dividers and section spacing counted; sections never exceed what they hold → layout(rows, plan) fills the dock exactly with titled dividers and the gaps above them counted; sections never exceed what they hold
- 2026-10-16T00:49:07Z criterion 2 verify: `test -s /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/ui-zones.png` → `test -s /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/ui-remake.png && test -s /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/ui-remake-small.png`
- 2026-10-16T00:49:07Z criterion 2 text: live render at 200x55 and 140x40 reads in zones (status, work, board, health) with blank rows between sections and aligned columns → live render at 200x55 and 140x40: titled sections, an Activity lane plot, tank gauges instead of small bars, History filling to the controls
- 2026-10-16T01:00:04Z done
- 2026-10-16T01:00:04Z committed 5596cf9 (10 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1000 [FEATURE M, done, 3 steps] Pane: no gaps, everything visual — sections sized to what they hold, the charts stretch to fill the dock exactly; Live shows tool lanes…
- T-0989 [FEATURE L, done, 4 steps] Can you clean up ALL of the mod UI, make it one panel, with everything consolidated, so it — lesson: A layout that must never move has …
- research T-0989-review: Verdict:** changes needed. The row budget holds. There is one functional regression (plan approval) and two housekeeping misses (version, types).…
- decision 2026-10-03: T-0166 deferred: splitting the band/pane out of register.tsx is a rewrite under the mod engine's $/atom rules; T-0130 took the rows out, the rest wa…
## Lessons
- A fixed-height Box with more children than rows doesn't clip the extras: flex shrink squeezes rows unpredictably (History showed only its failures); always slice a list to the rows it gets.
## Plan gaps
- failed first: step 1 layout over a plan of sections and zones, tested
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/hooks/rows.tsx
- mods/foreman-ui/hooks/state.ts
- plugin/lib/fmwatch.py
- .claude-plugin/marketplace.json
- CHANGELOG.md
- README.md
- mods/foreman-ui/.claude-plugin/plugin.json
