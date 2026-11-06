---
id: T-1017
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-16T01:35:46Z
updated: 2026-10-16T01:36:59Z
base: e171ab0cb681bd17e9b88284258df72a2277257b
base_tree: 65d4891208e488a0b598878d875aa9adf3b2109a
verified: strong
---
# Pane on a phone: the remade pane renders at phone width with text twins for every chart
## Raw request
> Pane on a phone: the remade pane renders at phone width with text twins for every chart
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the pane mounts on the mobile surface at 36 columns: every section, no Raster, no drawn rule or chart wider than the screen — verify with `cd mods/foreman-ui && claude plugin test .`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: mobile surface at 36 columns; fix what it finds
## Resume here
## Docs impact
none: test only
## Verification evidence
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 93 tests across 1 file. [13.57s] [ran] [tree 93a2a358d353] (2026-10-16T01:36:34Z)
- (ac 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 93 tests across 1 file. [11.67s] [ran] [tree 93a2a358d353] (2026-10-16T01:36:47Z)
- (audit edge) `self` → mobile surface at 36 columns: all sections, no Raster, rules and chart twins within the screen; the steer input stays off a phone [tree 93a2a358d353] (2026-10-16T01:36:47Z)
- (ac 1) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 93 tests across 1 file. [9.66s] [ran] [tree 93a2a358d353] (2026-10-16T01:36:58Z)
- (audit edge) `probe found no defect; kept as a regression test` → phone width holds [tree 93a2a358d353] (2026-10-16T01:36:58Z)
- (audit self) `probe found no defect; kept as a regression test` → no findings [tree 93a2a358d353] (2026-10-16T01:36:58Z)
## Log
- 2026-10-16T01:35:46Z created
- 2026-10-16T01:35:46Z focused
- 2026-10-16T01:36:20Z set type=FEATURE
- 2026-10-16T01:36:58Z done
- 2026-10-16T01:36:59Z committed 4c98791 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0909 [FEATURE L, done, 6 steps] Can you super improve the UI, better animations/visuals for graphs/tasks things going on? — lesson: In the mod test harness a Text elem…
- research T-0909-review: Verdict: changes needed.** The 14-day bars are wrong on this repo today, and the pane order does not match the third acceptance criterion. I coul…
- T-0998 [FEATURE S, done, 2 steps] Re-record the README demo with the remade pane
- decision 2026-10-15: Pane order: Needs you and waiting plans above the hero (T-0909)
- similar finished tasks took 2–6 steps
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
