---
id: T-1239
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T19:27:50Z
updated: 2026-10-16T19:43:20Z
base: a64cc0fc6beb48389f68afb2a0750d8aebfd53f8
base_tree: 37a7c412ced0ac155e61aee82dcd02abae84f93a
plan0_at: 2026-10-16T19:38:26Z
plan0_scope: []
verified: strong
---
# Benchmarks page: text runs outside its boxes (user report)
## Raw request
> Benchmarks page: text runs outside its boxes (user report)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] Chart labels sit above their bars at full width, so no label leaves its card at desktop or phone width; the site test passes — verify with `python3 plugin/tests/run.py -k Site`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Labels above bars in pairs(); a test that a long label can't overflow; screenshots at 1440 and 390
## Resume here
<!-- auto -->
- 2026-10-16T19:39:14Z step 1/1: Labels above bars in pairs(); a test that a long label can't overflow; screenshots at 1440 and 390
- git: foreman/build; 2 uncommitted: plugin/tests/test_docs.py, site/build.py
- touched since last checkpoint: plugin/tests/test_docs.py, site/build.py
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_docs.Site` → exit 0 · Ran 2 tests in 0.042s / OK [ran] [tree 7bbe310de2ac] (2026-10-16T19:42:12Z)
- (ac 1) `python3 plugin/tests/run.py -k Site` → exit 0 · Ran 6 tests in 0.4s (2 classes, 16 at a time; slowest: UntestedRuleSites 0s, Site 0s) / OK [ran] [tree 7bbe310de2ac] (2026-10-16T19:42:18Z)
- (audit edge) `self: screenshots at 1440 and 390 px show labels, values and table cells inside their cards; long-label test red on old code, green now` → a 40-character task name stays inside the chart (test); phone text bumped only for the pairs chart [tree 7bbe310de2ac] (2026-10-16T19:42:18Z)
- (audit self) `self: screenshots at 1440 and 390 px show labels, values and table cells inside their cards; long-label test red on old code, green now` → no findings [tree 7bbe310de2ac] (2026-10-16T19:42:18Z)
## Log
- 2026-10-16T19:27:50Z created
- 2026-10-16T19:38:26Z focused
- 2026-10-16T19:43:19Z done
- 2026-10-16T19:43:20Z committed 8fa85158 (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1238 [CLEAN S, done, 1 steps] Release 1.2.37: guard credential reads, approval binding, fm code, cheaper Foreman turns, neutral benchmark suites and the Benchmarks page
- T-1220 [FEATURE L, planned, 3 steps] Feature pages for the site: one page per Foreman capability, each with real graphs from Foreman's own history
- T-0972 [SECURITY S, done, 2 steps] Flag instruction-like text in fetched and tool output (WebFetch, WebSearch, MCP, curl/wget — lesson: Widen a sync hook's matcher only …
- decision 2026-10-16: Pane remake drops spend-by-feature, bench, research, vetoes, files churn and the week's skills list; skill calls get a lane in Activity; small meter…
- similar finished tasks took 1–2 steps
## Regression test
plugin/tests/test_docs.py Site.test_a_long_chart_label_stays_inside_its_card: failed on the 120 px label column, passes with labels above the bars
## Files touched
- plugin/tests/test_docs.py
- site/build.py
- site/pages.py
- site/stats.py
- site/data/stats.json
- site/style.css
- CHANGELOG.md
