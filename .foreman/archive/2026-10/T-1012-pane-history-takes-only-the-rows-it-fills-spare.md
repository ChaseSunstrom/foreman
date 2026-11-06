---
id: T-1012
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T01:21:22Z
updated: 2026-10-16T01:23:02Z
base: 13b9efe0ffedd321919e8e01040530cb5257e8ae
base_tree: 404fc1bdbfac67f22b1ee4791b266a6e56256256
verified: strong
---
# Pane: History takes only the rows it fills; spare rows go to more Activity lanes and taller Today charts first
## Raw request
> Pane: History takes only the rows it fills; spare rows go to more Activity lanes and taller Today charts first
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] layout: a stretch part takes at most what it holds; leftover goes to grow parts up to their limit, then blank rows at the stretch (or under the task); still exactly the dock — verify with `cd mods/foreman-ui && claude plugin test .`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: layout with a short History grows lanes and Today, fills exactly
2. [x] kit layout grow; register: lanes from R.activity, Today rows from R.today
3. [x] docs: README dashboard line; CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 1 fail / Ran 91 tests across 1 file. [6.78s] [ran] [tree 0d7c98d1574d] (2026-10-16T01:22:12Z)
- (step 2) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 91 tests across 1 file. [6.92s] [ran] [tree 887bcb6f3a0c] (2026-10-16T01:22:41Z)
- (step 3) `grep -q 'T-1012' CHANGELOG.md` → exit 0 · (no output) [ran] [tree 887bcb6f3a0c] (2026-10-16T01:22:41Z)
- (ac 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 91 tests across 1 file. [6.87s] [ran] [tree 887bcb6f3a0c] (2026-10-16T01:22:49Z)
- (audit edge) `self` → layout sums to the dock for rows 24-120 (existing sweep) and for short/empty History at 30-90 (new test); a long History keeps the charts at their base size; History with no lines has no title [tree 887bcb6f3a0c] (2026-10-16T01:22:49Z)
- (ac 1) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 91 tests across 1 file. [6.85s] [ran] [tree 887bcb6f3a0c] (2026-10-16T01:23:01Z)
- (audit edge) `layout sweep plus a new short/empty-History test; seen live in the recording's fresh project (History empty mid-pane)` → no History → no title; spare rows to lanes then Today (≤8 rows) then padding [tree 887bcb6f3a0c] (2026-10-16T01:23:01Z)
- (audit self) `layout sweep plus a new short/empty-History test; seen live in the recording's fresh project (History empty mid-pane)` → no findings [tree 887bcb6f3a0c] (2026-10-16T01:23:01Z)
## Log
- 2026-10-16T01:21:22Z created
- 2026-10-16T01:21:22Z focused
- 2026-10-16T01:23:02Z done
- 2026-10-16T01:23:02Z committed faa7b2b (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1000 [FEATURE M, done, 3 steps] Pane: no gaps, everything visual — sections sized to what they hold, the charts stretch to fill the dock exactly; Live shows tool lanes…
- T-0909 [FEATURE L, done, 6 steps] Can you super improve the UI, better animations/visuals for graphs/tasks things going on? — lesson: In the mod test harness a Text elem…
- research T-0909-review: Verdict: changes needed.** The 14-day bars are wrong on this repo today, and the pane order does not match the third acceptance criterion. I coul…
- decision 2026-10-16: Pane remake drops spend-by-feature, bench, research, vetoes, files churn and the week's skills list; skill calls get a lane in Activity; small meter…
## Plan gaps
- failed first: step 1 test: layout with a short History grows lanes and Today, fills exactly
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- CHANGELOG.md
- README.md
