---
id: T-1056
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmideas.py, plugin/tests/test_ideas.py]
depends_on: []
source: discovered
created: 2026-10-16T04:02:44Z
updated: 2026-10-16T07:02:36Z
base: f024d39d3a54449a4a427232f35043091878dd58
base_tree: 5b4db2e130661e54afc237c5cef5b37b5f3e7ae0
verified: strong
---
# Ideas.md` reports 409 ideas but lists about 290 titles. Per-lens counts "bold bets: 40" an
## Raw request
> ideas.md` reports 409 ideas but lists about 290 titles. Per-lens counts "bold bets: 40" and similar don't add up to the list
> (noticed by an agent; research brainstorm-20261016-wild-clusters)
## Interpretation
ideas.md mixes idea bullets with tally bullets (per-lens yield '- lens: N', coverage '- category N', kills '- title — kill'), so a bullet count (409) overstates the ideas (~290), and --seen reads the coverage and kill lines back as idea titles, polluting later rounds' dedupe. ideas.md states its distinct count at the top, and --seen reads only the idea sections (Round, Deepened, Cross-bred).
## Assumptions (confidence)
## Acceptance criteria
- [x] --seen on an ideas.md reads exactly the idea titles (not lens, coverage or kill lines), and ideas.md's first lines state the distinct count — verify with `python3 plugin/tests/run.py test_ideas`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test for seen_titles and the count line; then fix
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ideas` → ✗ exit 1 · Ran 22 tests in 14.7s (5 classes, 16 at a time; slowest: Ideas 14s, BoardIdeas 5s, DegradeOnPace 2s) / FAILED (1 classes) [ran] [tree 16b18825ad06] (2026-10-16T07:00:23Z)
- (step 1) `python3 plugin/tests/run.py test_ideas` → exit 0 · Ran 22 tests in 16.4s (5 classes, 16 at a time; slowest: Ideas 16s, BoardIdeas 6s, DegradeOnPace 3s) / OK [ran] [tree 25417392b7bc] (2026-10-16T07:00:51Z)
- (ac 1) `python3 plugin/tests/run.py test_ideas` → exit 0 · Ran 22 tests in 17.4s (5 classes, 16 at a time; slowest: Ideas 16s, BoardIdeas 7s, DegradeOnPace 3s) / OK [ran] [tree 7e8060c5b0ab] (2026-10-16T07:01:33Z)
- (audit self) `self: seen_titles tested on an index with every section kind; the pane's own reader already stops before the tallies` → no findings [tree 7e8060c5b0ab] (2026-10-16T07:01:33Z)
## Log
- 2026-10-16T04:02:44Z created
- 2026-10-16T06:59:47Z set type=FIX, scope=['plugin/lib/fmideas.py', 'plugin/tests/test_ideas.py']
- 2026-10-16T06:59:53Z set tier=S
- 2026-10-16T06:59:55Z focused
- 2026-10-16T07:01:14Z scope: CHANGELOG.md — release note
- 2026-10-16T07:02:34Z done
- 2026-10-16T07:02:36Z committed 017c0b7 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-intelligence-20261009: 768 ideas from 15 lenses over 4 rounds plus 3 deepened categories, in 106 capabilities; every idea under exactly one capabilit…
- T-1072 [CLEAN M, done, 2 steps] Rule and hint hygiene: cards, known fixes, rules and lessons that never fired or never hel — lesson: A cleanup that deletes what users ta…
- T-0684 [FEATURE M, done, 5 steps] Milestone: Intelligence — Brainstorming and ideation — lesson: Brainstorm quality needs feedback the catalogue can carry: store it stru…
- decision 2026-10-14: Round 2 slate: 437 ideas in 29 clusters grounded → 3 build (compact spill cap T-0824, closed-pipe verb sweep T-0825, verb-usage evidence attached to…
- likely tests for the scope: plugin/tests/test_ideas.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmideas.py; re-ground the plan against them before editing
## Lessons
- A file that mixes items and tallies in one bullet style needs its readers to know the sections; say the count in words at the top
## Plan gaps
- failed first: step 1 Failing test for seen_titles and the count line; then fix
## Files touched
- plugin/tests/test_ideas.py
- plugin/lib/fmideas.py
- CHANGELOG.md
