---
id: T-1000
type: FEATURE
tier: M
status: done
priority: normal
scope: [mods/foreman-ui/hooks/register.tsx,mods/foreman-ui/hooks/rows.tsx,mods/foreman-ui/hooks/kit.ts,mods/foreman-ui/tests/foreman-ui.test.tsx,mods/foreman-ui/.claude-plugin/plugin.json,.claude-plugin/marketplace.json,CHANGELOG.md,README.md]
depends_on: []
source: user
created: 2026-10-16T00:08:54Z
updated: 2026-10-16T00:17:38Z
base: 8029cc05c5776cbfc8f894bc1b6063d44f441528
base_tree: f381b79b2b67bcf2f095a802791d5b04bc9903f4
verified: strong
---
# Pane: no gaps, everything visual — sections sized to what they hold, the charts stretch to fill the dock exactly; Live shows tool lanes when quiet; every More line gets a bar or meter
## Raw request
> Pane: no gaps, everything visual — sections sized to what they hold, the charts stretch to fill the dock exactly; Live shows tool lanes when quiet; every More line gets a bar or meter
## Interpretation
The user on the T-0989 panel: 'why is everything on the right spaced out? some things are just text, I want everything to have visuals and stuff, and take up the entire space, no more, no less'. Fixed section heights left blank rows; More lines and quiet Live were plain text. Keep it one panel that fits exactly, without gaps, with a visual on every line, and without the old jumping.
## Assumptions (confidence)
## Acceptance criteria
- [x] layout fills the dock exactly (sum == rows) from section demands; sections hold no blank rows; More lines and quiet Live carry visuals — verify with `cd mods/foreman-ui && claude plugin test .`
- [x] a live render at 200x55 shows no blank run of rows and the panel ends at the dock's bottom — verify with `test -s /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/ui-fill.png`
## Non-goals
## Approach (options → choice → why)
Options: (1) sections sized to their content (capped), Live fixed with tool-call swim lanes filling its quiet rows, and Pulse at the bottom absorbing the rest by stretching its charts (taller 14-day bars, more gauges, lanes) — chosen: no blank rows, the sum is exactly the dock, and only the bottom chart changes height when a list grows; (2) keep fixed heights and invent filler visuals for each gap (contrived charts, still gaps when content is short); (3) fully elastic sections (every boundary moves as lists change: the old jumping). Visual More lines: fleet with a context meter per session, spend as a stacked bar by feature, skills as bars per skill, files as a +/- churn bar, bench and research as pass meters, ideas as an answers meter while running.
## Risks and rollback
## Execution prompt
## Steps
1. [x] layout(rows, demand) that sums exactly, tested
2. [x] renderer: demand-sized Task/Queue/More, lanes in quiet Live, stretching Pulse, visual More lines
3. [x] look at it live; fix what reads badly; docs
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `cd mods/foreman-ui && claude plugin test .` → ✗ exit 1 · 1 fail / Ran 85 tests across 1 file. [29.31s] [ran] [tree b70849081a05] (2026-10-16T00:10:52Z)
- (step 1) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 85 tests across 1 file. [8.12s] [ran] [tree b763701c9e0e] (2026-10-16T00:15:54Z)
- (step 2) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 85 tests across 1 file. [7.79s] [ran] [tree b1b0ce6f8ca7] (2026-10-16T00:17:27Z)
- (step 3) `test -s /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/ui-fill.png && test -s /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/ui-fill-small.png && grep -q 'fills the dock exactly' README.md` → exit 0 · (no output) [ran] [tree b1b0ce6f8ca7] (2026-10-16T00:17:27Z)
- (ac 1) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 85 tests across 1 file. [7.71s] [ran] [tree b1b0ce6f8ca7] (2026-10-16T00:17:37Z)
- (ac 2) `test -s /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/ui-fill.png` → exit 0 · (no output) [ran] [tree b1b0ce6f8ca7] (2026-10-16T00:17:37Z)
- (audit intent) `self: layout(rows, demand) test sweeps 14-120 rows x three demand shapes and asserts the sum is exactly the dock and no section exceeds what it holds; a rendered 60-row pane sums to 60; live shots at 200x55 and 140x40 show no blank runs and the panel ends at the dock's bottom` → no gaps, a picture on every row, exactly the dock's height (the user's three asks) [tree b1b0ce6f8ca7] (2026-10-16T00:17:37Z)
- (audit edge) `self: layout(rows, demand) test sweeps 14-120 rows x three demand shapes and asserts the sum is exactly the dock and no section exceeds what it holds; a rendered 60-row pane sums to 60; live shots at 200x55 and 140x40 show no blank runs and the panel ends at the dock's bottom` → a crowded dock (20 steps at 40 rows) caps the task and counts what's hidden; plans waiting sort first so a short queue keeps their approve buttons; empty lanes draw a faint track instead of blank rows [tree b1b0ce6f8ca7] (2026-10-16T00:17:37Z)
## Log
- 2026-10-16T00:08:54Z created
- 2026-10-16T00:09:17Z focused
- 2026-10-16T00:17:27Z scope: .claude-plugin/marketplace.json version bump for the mod
- 2026-10-16T00:17:38Z done
- 2026-10-16T00:17:38Z committed 880fac1 (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0989 [FEATURE L, done, 4 steps] Can you clean up ALL of the mod UI, make it one panel, with everything consolidated, so it — lesson: A layout that must never move has …
- research T-0989-review: Verdict:** changes needed. The row budget holds. There is one functional regression (plan approval) and two housekeeping misses (version, types).…
- T-0909 [FEATURE L, done, 6 steps] Can you super improve the UI, better animations/visuals for graphs/tasks things going on? — lesson: In the mod test harness a Text elem…
- decision 2026-10-03: T-0166 deferred: splitting the band/pane out of register.tsx is a rewrite under the mod engine's $/atom rules; T-0130 took the rows out, the rest wa…
## Lessons
- Fit-to-screen means sizing from content and letting one elastic chart absorb the remainder: fixed shares leave gaps, fully elastic sections jump.
## Plan gaps
- failed first: step 1 layout(rows, demand) that sums exactly, tested
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- .claude-plugin/marketplace.json
- CHANGELOG.md
- README.md
- mods/foreman-ui/.claude-plugin/plugin.json
