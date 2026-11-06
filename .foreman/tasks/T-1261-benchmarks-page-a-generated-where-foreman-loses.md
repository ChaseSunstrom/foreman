---
id: T-1261
type: FEATURE
tier: M
status: done
priority: normal
scope: [site/pages.py, site/stats.py, plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/tests/test_docs.py, plugin/tests/test_bench_family.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-20T14:01:26Z
updated: 2026-10-23T12:46:32Z
base: 48fe899f0ea4438e9dcfc262432236437d0ca108
base_tree: f80f9864c7a8d7537e390be2adbfa47c5a7dea08
plan0_at: 2026-10-23T12:43:13Z
plan0_scope: [site/pages.py, site/stats.py, plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/tests/test_docs.py, plugin/tests/test_bench_family.py, CHANGELOG.md]
verified: strong
---
# Benchmarks page: a generated 'Where Foreman loses' section and fm bench repro to rerun one
## Raw request
> Benchmarks page: a generated 'Where Foreman loses' section and fm bench repro to rerun one row (brainstorm-20261020 C6)
## Interpretation
The benchmarks page gains a generated 'Where Foreman loses' section: every duel row where Claude Code passed and Foreman didn't, or Foreman cost or took 25% more, each with the command that reruns it. fm bench repro LABEL CASE reruns one row on both sides with the saved run's model, runs, budget, compaction window and marathon, printing then and now.
## Assumptions (confidence)
## Acceptance criteria
- [x] the page lists each losing row with its repro command (none: says so); fm bench repro reruns one row on both sides and refuses a wrong label or case — verify with `python3 plugin/tests/run.py test_docs test_bench_family`
## Non-goals
## Approach (options → choice → why)
Options: (1) the section computed in site/pages.py from stats.json's duels, which gain each run's label and case ids, plus a repro verb reading the saved results (chosen: the page and the charts read one source, and a row names its own rerun); (2) a hand-written losses list (rejected: drifts, the T-1246 lesson); (3) repro rerunning the whole duel (rejected: costs every case to check one).
## Risks and rollback
## Execution prompt
## Steps
1. [x] the generated section, the data it reads, and fm bench repro, test first
## Resume here
## Docs impact
The benchmarks page gains its generated section (site/pages.py); site/data/stats.json gains labels and case ids at its next build (site/stats.py), until then each row says its rerun wasn't recorded; CHANGELOG line.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_docs.Site test_bench_family.Repro` → ✗ exit 1 · Ran 18 tests in 2.9s (2 classes, 16 at a time; slowest: Repro 3s, Site 1s) / FAILED (2 classes) [ran] [tree 67830f95d3a2] (2026-10-23T12:43:22Z)
- (step 1) `python3 plugin/tests/run.py test_docs test_bench_family test_bench test_cli` → exit 0 · Ran 232 tests in 38.1s (64 classes, 16 at a time; slowest: Bench 38s, TaskLifecycle 27s, Judged 21s) / OK [ran] [tree cba7cf08f06a] (2026-10-23T12:45:17Z)
- (ac 1) `python3 plugin/tests/run.py test_docs test_bench_family` → exit 0 · Ran 87 tests in 15.7s (25 classes, 16 at a time; slowest: Judged 15s, Duel 10s, Marathon 9s) / OK [ran] [tree cba7cf08f06a] (2026-10-23T12:45:33Z)
- (ac 1) `python3 plugin/tests/run.py test_docs test_bench_family` → exit 0 · Ran 87 tests in 15.6s (25 classes, 16 at a time; slowest: Judged 15s, Duel 10s, Marathon 9s) / OK [ran] [tree cba7cf08f06a] (2026-10-23T12:45:49Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): the section reads the same duels the tables read; every cell escaped; repro checks the label's shape before building a path from it, reads both saved sides, and reruns through run_arm, so the guard and the budget check apply as in a duel` → the page shows where Foreman loses, not only where it wins, and each losing row can be rerun with one command [tree cba7cf08f06a] (2026-10-23T12:45:49Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): the section reads the same duels the tables read; every cell escaped; repro checks the label's shape before building a path from it, reads both saved sides, and reruns through run_arm, so the guard and the budget check apply as in a duel` → a run without labels (today's stats.json) lists its rows with 'not recorded with this run'; no losing row says so; a label that isn't a Foreman side's, a missing side or an unknown case is refused before any session; --budget defaults to the run's own [tree cba7cf08f06a] (2026-10-23T12:45:49Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): the section reads the same duels the tables read; every cell escaped; repro checks the label's shape before building a path from it, reads both saved sides, and reruns through run_arm, so the guard and the budget check apply as in a duel` → the label must match duel-none-foreman-[word chars, dot, dash], so no path can climb out of the results folder [tree cba7cf08f06a] (2026-10-23T12:45:49Z)
## Log
- 2026-10-20T14:01:26Z created
- 2026-10-23T12:43:05Z set tier=M, scope=['site/pages.py', 'site/stats.py', 'plugin/lib/fmbench.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_docs.py', 'plugin/tests/test_bench_family.py', 'CHANGELOG.md']
- 2026-10-23T12:43:12Z focused
- 2026-10-23T12:46:30Z done
- 2026-10-23T12:46:32Z committed 771938a0 (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1242-review: Verdict: changes needed.** The acceptance criterion's published result is missing, and per-request passes aren't reported. [stale: plugin/lib/fmb…
- T-1259 [FEATURE M, done, 1 steps] Compaction-storm soak in the bench (Haiku, forced compaction every few turns) and a measur — lesson: Build the paid experiment's harnes…
- research brainstorm-20261020: Run: `fm ideas` super mode, 9 lenses (user value, unspoken needs, delight, capability map, approaches, reliability,
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
- the similar finished task took 1 steps
- likely tests for the scope: plugin/tests/test_bench.py, plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-20): CHANGELOG.md, plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/tests/test_bench_family.py, plugin/tests/test_docs.py, site/pages.py, site/stats.py; re-ground the plan against them before editing
## Lessons
- A page that publishes results should generate its own losses from the same data as its wins
## Plan gaps
- failed first: step 1 the generated section, the data it reads, and fm bench repro, test first
## Files touched
- CHANGELOG.md
- plugin/lib/fmbench.py
- plugin/lib/fmcli.py
- plugin/tests/test_bench_family.py
- plugin/tests/test_docs.py
- site/pages.py
- site/stats.py
