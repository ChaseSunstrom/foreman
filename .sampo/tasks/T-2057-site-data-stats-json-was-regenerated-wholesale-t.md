---
id: T-2057
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T21:31:48Z
updated: 2026-10-31T01:11:47Z
base: 564cc7fb3ff863d8132117010d2ee763e1e95e7b
base_tree: b82351e0401f660cf2756334ebc7c84ec6a5e89c
plan0_at: 2026-10-31T00:40:00Z
plan0_scope: []
verified: strong
---
# - site/data/stats.json was regenerated wholesale. The `features/benchmarks` bench cases…
## Raw request
> - site/data/stats.json was regenerated wholesale. The `features/benchmarks` bench cases changed (the `csvlite`/`tokenbucket` cases became `honour` cases, and `tests: null` fields were added). Worth a…
> (noticed by an agent; research T-2040-review)
## Interpretation
A T-2040 review note: site/data/stats.json was regenerated and its bench cases changed shape (csvlite/tokenbucket became honour cases; tests: null fields appeared). Nothing checks that features/benchmarks.html still renders them: a null could print as 'None' or 'null', or a renamed case could vanish.
## Assumptions (confidence)
## Acceptance criteria
- [x] every bench case in site/data/stats.json shows on the built benchmarks page, and no built page prints a bare None, null, undefined or NaN — verify with `python3 plugin/tests/run.py test_site`
## Non-goals
## Approach (options → choice → why)
Options: (1) a site test that builds the pages and asserts every bench case in stats.json appears on the benchmarks page and no built page shows a bare None, null, undefined or NaN; fix what it finds; (2) a one-off look at the page now (doesn't stay true); (3) a schema for stats.json (heavier; the page is what readers see). Choice 1.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test over the built site; fix the renders it catches; fm shot the benchmarks page
## Resume here
## Docs impact
none: test only
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_site test_site_build` → exit 0 · Ran 29 tests in 4.8s (13 classes, 16 at a time; slowest: Header 5s, Landing 2s, Session 1s) / OK [ran] [tree ce31bb9a8441] (2026-10-31T01:10:41Z)
- (step 1) `python3 plugin/tests/run.py test_site test_site_build` → exit 0 · Ran 29 tests in 5.4s (13 classes, 16 at a time; slowest: Header 5s, Landing 2s, Session 2s) / OK [ran] [tree 1056db833d97] (2026-10-31T01:11:05Z)
- (ac 1) `python3 plugin/tests/run.py test_site` → exit 0 · Ran 29 tests in 4.8s (13 classes, 16 at a time; slowest: Header 5s, Landing 2s, Session 1s) / OK [ran] [tree 1056db833d97] (2026-10-31T01:11:27Z)
- `python3 plugin/tests/run.py test_site test_site_build` → exit 0 · Ran 29 tests in 4.8s (13 classes, 16 at a time; slowest: Header 5s, Landing 2s, Session 1s) / OK [ran] [tree 1056db833d97] (2026-10-31T01:11:27Z)
- (audit edge) `self: read the test; it builds the site into a temp dir, asserts each duel case shows on the benchmarks page and no built page prints a bare None/null/undefined/NaN outside scripts and styles; added an assert that stats.json has cases so it can't pass empty` → an empty duels list now fails the test instead of passing it [tree 1056db833d97] (2026-10-31T01:11:27Z)
- (audit self) `self: read the test; it builds the site into a temp dir, asserts each duel case shows on the benchmarks page and no built page prints a bare None/null/undefined/NaN outside scripts and styles; added an assert that stats.json has cases so it can't pass empty` → no findings [tree 1056db833d97] (2026-10-31T01:11:27Z)
## Log
- 2026-10-29T21:31:48Z created
- 2026-10-31T00:36:01Z planned: it has criteria and steps
- 2026-10-31T00:36:01Z set tier=S, approved=True
- 2026-10-31T00:38:37Z grounded: stats.json's nulls sit in duels[*].cases[*].{foreman,bare}.{tests,compactions,capped,requests} and duels[0].claude; pages.py:307 already falls back for a null tests ('or [0, 1]'), so the check to write is that the built benchmarks page shows each duel case and prints no bare None/null/NaN
- 2026-10-31T00:39:45Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2057.builder.md
- 2026-10-31T00:39:59Z focused
- 2026-10-31T01:10:00Z merged worktree-agent-accf7c86a9928e307 (1 file(s))
- 2026-10-31T01:10:12Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-accf7c86a9928e307
- 2026-10-31T01:10:22Z focused
- 2026-10-31T01:10:50Z scope: plugin/tests/test_site_build.py only, the test this brief asks for; no render needed fixing (the test was green first run, so it stands as a regression guard), so no fm shot: the page didn't change
- 2026-10-31T01:11:46Z done
- 2026-10-31T01:11:47Z committed 5df339d8 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2040-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** approve with nits. I couldn't run the tests here, so the …
- research T-1220-review: Changes needed. Nothing is critical. Three MEDIUM defects are worth fixing before the next publish. I read the code and the data files and did no…
- T-2062 [FEATURE M, done, 3 steps] Site shows the shader cards live: each shader-* card's fragment shader running in a… — lesson: Headless shots of one section: cut it in…
- decision 2026-10-30: Recommendation: keep the free finders arm as the zero-token per-generation check for the find capabilities; on s0-001 it found 90/108 (held out 30/3…
## Regression test
none for this task: the fmgenesis.py change in its range is T-2160's merge (87070bc0), proven red to green under T-2160; this task adds only a site test
## Lessons
- A presence check over a list from data needs a non-empty assert, or an emptied data file turns it green
## Files touched
- plugin/tests/test_site_build.py
- plugin/lib/fmcore.py
- plugin/lib/fmloop.py
- plugin/lib/fmmission.py
- plugin/tests/test_loop.py
- plugin/tests/test_mission.py
