---
id: T-1255
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmbench.py, site/stats.py, site/pages.py, site/style.css, plugin/tests/test_bench.py, plugin/tests/test_bench_family.py, plugin/tests/test_evolve.py, plugin/tests/test_docs.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-20T14:01:16Z
updated: 2026-10-20T14:39:36Z
base: a61bcfc3b72d7e6f906b2c55f8a931f74a38cc8f
base_tree: 6cf520d187aac8234d336cb125c4b29120d27849
plan0_at: 2026-10-20T14:31:49Z
plan0_scope: [plugin/lib/fmbench.py, site/stats.py, site/pages.py, plugin/tests/test_bench.py, plugin/tests/test_docs.py, CHANGELOG.md]
verified: strong
---
# Every bench result records the Claude Code version it ran on, and the Benchmarks page name
## Raw request
> FEATURE: Every bench result records the Claude Code version it ran on, and the Benchmarks page names it
> CONTEXT: brainstorm 2026-10-20 (research brainstorm-20261020), T-1252; Claude Code 2.1.304 re-sends the skill list after each compaction
## Interpretation
Every benchmark result says which Claude Code it ran on, and the Benchmarks page shows it under each duel, so results from different Claude Code releases aren't silently compared; old runs say the version wasn't recorded.
## Assumptions (confidence)
## Acceptance criteria
- [x] every bench arm result records the Claude Code version it ran on (claude --version), and the Benchmarks page names the version under each duel — verify with `python3 plugin/tests/run.py test_bench test_docs`
## Non-goals
## Approach (options → choice → why)
Options: (a) stamp in run_arm from fmeco.claude_version(), carried by site/stats.duel and shown by a helper under each duel and long run; (b) read it from each transcript's version field per case; (c) only in the page's method text. Choice: (a): one call per arm, already used by the canary, and the page names it where the figures are. No backfill: an old run's version isn't known.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: run_arm's result carries the version; stats.duel passes it on; the page names it
2. [x] Stamp it in fmbench.run_arm (fmeco.claude_version), carry it in site/stats.py, show it in site/pages.py, changelog
## Resume here
## Docs impact
CHANGELOG entry; the page names it itself
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bench test_docs` → ✗ exit 1 · Ran 82 tests in 75.3s (23 classes, 16 at a time; slowest: Bench 75s, Judged 43s, Duel 29s) / FAILED (2 classes) [ran] [tree 376ab08715c8] (2026-10-20T14:33:19Z)
- (step 2) `python3 plugin/tests/run.py test_bench test_docs` → ✗ exit 1 · Ran 82 tests in 48.1s (23 classes, 16 at a time; slowest: Bench 48s, Judged 35s, Duel 26s) / FAILED (2 classes) [ran] [tree cd030d307a15] (2026-10-20T14:34:28Z)
- (step 2) `python3 plugin/tests/run.py test_bench test_docs` → ✗ exit 1 · Ran 82 tests in 26.8s (23 classes, 16 at a time; slowest: Bench 27s, Judged 15s, Duel 10s) / FAILED (1 classes) [ran] [tree 3c801b032cb8] (2026-10-20T14:35:31Z)
- (step 2) `python3 plugin/tests/run.py test_bench test_bench_family test_evolve test_docs` → exit 0 · Ran 91 tests in 27.5s (26 classes, 16 at a time; slowest: Bench 27s, Judged 15s, Evolve 12s) / OK [ran] [tree 4e899150714b] (2026-10-20T14:37:14Z)
- (ac 1) `python3 plugin/tests/run.py test_bench test_docs` → exit 0 · Ran 82 tests in 47.9s (23 classes, 16 at a time; slowest: Bench 48s, Judged 34s, Duel 22s) / OK [ran] [tree 8090f1136eb8] (2026-10-20T14:38:38Z)
- (step 1) `python3 plugin/tests/run.py test_bench test_bench_family test_evolve test_docs` → exit 0 · Ran 91 tests in 28.1s (26 classes, 16 at a time; slowest: Bench 28s, Judged 16s, Evolve 13s) / OK [ran] [tree 8090f1136eb8] (2026-10-20T14:38:38Z)
- (audit intent) `self review: stamp, carry-through and page line read against a stubbed run and a fixture state` → results from different Claude Code releases can now be told apart, on the page too; nothing is backfilled because an old run's version isn't known [tree 8090f1136eb8] (2026-10-20T14:38:38Z)
- (audit edge) `self review: stamp, carry-through and page line read against a stubbed run and a fixture state` → claude missing or printing no version gives None and the page says it wasn't recorded; a version line without a number is kept as given [tree 8090f1136eb8] (2026-10-20T14:38:38Z)
## Log
- 2026-10-20T14:01:16Z created
- 2026-10-20T14:16:50Z set scope=['plugin/lib/fmbench.py', 'site/stats.py', 'site/pages.py', 'plugin/tests/test_bench.py', 'plugin/tests/test_docs.py', 'CHANGELOG.md']
- 2026-10-20T14:31:48Z focused
- 2026-10-20T14:35:04Z set scope=['plugin/lib/fmbench.py', 'site/stats.py', 'site/pages.py', 'site/style.css', 'plugin/tests/test_bench.py', 'plugin/tests/test_docs.py', 'CHANGELOG.md']
- 2026-10-20T14:35:04Z scope: site/style.css for the version caption's style
- 2026-10-20T14:36:45Z set scope=['plugin/lib/fmbench.py', 'site/stats.py', 'site/pages.py', 'site/style.css', 'plugin/tests/test_bench.py', 'plugin/tests/test_bench_family.py', 'plugin/tests/test_evolve.py', 'plugin/tests/test_docs.py', 'CHANGELOG.md']
- 2026-10-20T14:36:46Z scope: the other bench stubs answer --version, which run_arm now calls
- 2026-10-20T14:39:35Z done
- 2026-10-20T14:39:36Z committed 692359cf (9 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1254 [FEATURE M, done, 2 steps] Benchmarks page: cost per fully-correct session (long sessions: Foreman's mean cost over i — lesson: Compare cost per correct result, n…
- research T-1242-review: Verdict: changes needed.** The acceptance criterion's published result is missing, and per-request passes aren't reported. [stale: plugin/lib/fmc…
- T-1220 [FEATURE L, done, 3 steps] Feature pages for the site: one page per Foreman capability, each with real graphs from Foreman's own history — lesson: A stdlib site g…
- decision 2026-10-20: [cites: research/brainstorm-20261020] Round 1 of the 2026-10-20 brainstorm builds T-1254 (cost per fully-correct session on the page), T-1255 (Claud…
- likely tests for the scope: plugin/tests/test_bench.py
## Lessons
- A new subprocess call in run_arm reaches every fake claude in the tests: each stub that logs its calls has to answer it without logging
## Plan gaps
- failed first: step 1 Failing tests: run_arm's result carries the version; stats.duel passes it on; the page names it
- failed first: step 2 Stamp it in fmbench.run_arm (fmeco.claude_version), carry it in site/stats.py, show it in site/page…
## Files touched
- plugin/tests/test_bench.py
- plugin/tests/test_docs.py
- plugin/lib/fmbench.py
- site/pages.py
- site/stats.py
- site/style.css
- plugin/tests/test_bench_family.py
- plugin/tests/test_evolve.py
- CHANGELOG.md
