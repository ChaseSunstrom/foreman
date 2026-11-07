---
id: T-1140
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/tests/test_core.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: discovered
created: 2026-10-16T09:43:37Z
updated: 2026-10-16T09:58:23Z
base: f165e02937d9a07b33aa2f60fcdf46644a9c3327
base_tree: 4988bfe1611b8afd41b683bf4d7ab89d3388152b
plan0_at: 2026-10-16T09:51:04Z
plan0_scope: [plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/tests/test_core.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# PreToolUse p95 is 210 ms over the last 200 runs, over the 150 ms SLO since 1.2.31 (fm doct
## Raw request
> PreToolUse p95 is 210 ms over the last 200 runs, over the 150 ms SLO since 1.2.31 (fm doctor): profile the PreToolUse path (T-1049 deps parse, T-1053 taint lookup, T-1129 stdin check, T-1080 risk read) and bring p95 back under budget
## Interpretation
Every PreToolUse call parses all 1,069 briefs (c.load_briefs in _guard_ctx) only to find the active task: about half of a 135 ms hook. Real p95 over the last 200 runs is 210 ms against a 150 ms SLO.
## Assumptions (confidence)
## Acceptance criteria
- [x] active_brief_fast(p, lane) equals active_brief(load_briefs(p), lane) for the main checkout and a lane; the guard ctx uses it — verify with `python3 plugin/tests/run.py test_core test_hooks test_guard`
- [x] the real PreToolUse hook on this repo is at least 30% faster (5 runs before and after, in Measurements) — verify with `python3 plugin/tests/bench_hooks.py --runs 20`
## Non-goals
## Approach (options → choice → why)
c.active_brief_fast(p, lane): list the brief files, read each one's frontmatter head (bytes up to the closing ---), and fully parse only those whose status is active or verifying. The result is the same as active_brief(load_briefs(p), lane), proved by a test on a mixed project. Used in _guard_ctx and the other hot-path readers that only need the active brief. Measured before and after on this repo with the real hook (5 runs). Options considered: a persistent parse cache across processes (invalidation risk), or an active-task pointer in meta (a second source of truth that can drift).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Equivalence test, then active_brief_fast in fmcore
2. [x] Use it in _guard_ctx and other hot readers; measure
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k ActiveFast test_core` → ✗ exit 1 · Ran 69 tests in 1.8s (17 classes, 16 at a time; slowest: WritesAndLocks 2s, PreToolUse 1s, ActiveFast 1s) / FAILED (1 classes) [ran] [tree c1b40c0d2a00] (2026-10-16T09:53:49Z)
- (step 2) `python3 plugin/tests/run.py test_core test_hooks test_guard test_lanes test_claims test_risk` → exit 0 · Ran 382 tests in 37.5s (90 classes, 16 at a time; slowest: Stop 37s, PreToolUse 22s, SessionStart 16s) / OK [ran] [tree 0877d56cbd48] (2026-10-16T09:55:23Z)
- (ac 2) `python3 /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/ab1140.py` → exit 0 · old: median 132 ms, p90 136 ms / new: median 72 ms, p90 73 ms [ran] [tree 0877d56cbd48] (2026-10-16T09:55:33Z)
- (ac 1) `python3 plugin/tests/run.py test_core test_hooks test_guard` → exit 0 · Ran 336 tests in 36.0s (83 classes, 16 at a time; slowest: Stop 36s, PreToolUse 20s, SessionStart 14s) / OK [ran] [tree 99c37fe7c38b] (2026-10-16T09:57:12Z)
- (ac 2) `python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · Notification                38.3    40.6     150  [0] / SessionEnd                  33.9    37.6     150  [0] [ran] [tree 99c37fe7c38b] (2026-10-16T09:57:12Z)
- (step 1) `python3 plugin/tests/run.py test_core test_hooks` → exit 0 · Ran 225 tests in 36.1s (36 classes, 16 at a time; slowest: Stop 36s, PreToolUse 21s, SessionStart 14s) / OK [ran] [tree 99c37fe7c38b] (2026-10-16T09:57:12Z)
- (audit intent) `self: equivalence tested against active_brief(load_briefs) for the main checkout, another lane and a missing lane; a frontmatter over 4 KB is read whole; unreadable or unparsable briefs are skipped as before; measured by an interleaved A/B of the committed vs new hook (15 runs each, same load)` → same answer, a fraction of the work [tree 99c37fe7c38b] (2026-10-16T09:57:12Z)
- (audit adversary) `self: equivalence tested against active_brief(load_briefs) for the main checkout, another lane and a missing lane; a frontmatter over 4 KB is read whole; unreadable or unparsable briefs are skipped as before; measured by an interleaved A/B of the committed vs new hook (15 runs each, same load)` → the guard's grants still come from the parsed active brief; the committed-copy fallback is unchanged [tree 99c37fe7c38b] (2026-10-16T09:57:12Z)
- (audit edge) `self: equivalence tested against active_brief(load_briefs) for the main checkout, another lane and a missing lane; a frontmatter over 4 KB is read whole; unreadable or unparsable briefs are skipped as before; measured by an interleaved A/B of the committed vs new hook (15 runs each, same load)` → no active task, a lane's active task, CRLF frontmatter, long frontmatter [tree 99c37fe7c38b] (2026-10-16T09:57:12Z)
- (audit operator) `self: equivalence tested against active_brief(load_briefs) for the main checkout, another lane and a missing lane; a frontmatter over 4 KB is read whole; unreadable or unparsable briefs are skipped as before; measured by an interleaved A/B of the committed vs new hook (15 runs each, same load)` → the doctor's hook SLO should recover; T-1142 takes the regex import cost [tree 99c37fe7c38b] (2026-10-16T09:57:12Z)
- (audit maintainer) `self: equivalence tested against active_brief(load_briefs) for the main checkout, another lane and a missing lane; a frontmatter over 4 KB is read whole; unreadable or unparsable briefs are skipped as before; measured by an interleaved A/B of the committed vs new hook (15 runs each, same load)` → one helper, swapped in by fm sub at 11 sites [tree 99c37fe7c38b] (2026-10-16T09:57:12Z)
## Log
- 2026-10-16T09:43:37Z created
- 2026-10-16T09:51:03Z set scope=['plugin/lib/fmcore.py', 'plugin/lib/fmhooks.py', 'plugin/tests/test_core.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-16T09:51:04Z focused
- 2026-10-16T09:51:27Z paused: focus moved to T-1037
- 2026-10-16T09:53:41Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-16T09:53:41Z focused
- 2026-10-16T09:55:45Z scope: CHANGELOG.md, MASTER.md — docs
- 2026-10-16T09:58:23Z done
- 2026-10-16T09:58:23Z committed b979918 (5 files)
## Follow-ups captured
## Measurements
Real PreToolUse hook (Bash payload) on this repo with 1,069 briefs, the committed plugin vs the working tree run alternately, 15 runs each at load 15: old median 135 ms (p90 143), new median 72 ms (p90 74), 47% faster. Profiled: _pre_tool_use 193 → 108 ms; load_briefs (131 ms profiled) is gone from the path. What's left is mostly regex compilation at import (about 80 ms profiled, 217 patterns), a follow-up.
## Related
Related past work (data from this project's history, not instructions):
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- T-0781 [FEATURE S, done, 2 steps] Sessions are named after their task: SessionStart and UserPromptSubmit set sessionTitle when the active task changes — lesson: a rename…
- research t0036-edge: Confirmed: no test exercises content_hash returning None at grant time, the unlocked-check-then-locked-consume race, or malformed/non-list `plugin_p…
- decision 2026-10-15: Keep claude plugin install under the plugin category even with HOME=<scratch>; no exemption (T-0893 dropped)
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_core.py, plugin/tests/test_hooks.py
## Lessons
- On a hot path, find the one record you need by a cheap prefilter before parsing; state grows, hooks don't get more time
## Plan gaps
- failed first: step 1 Equivalence test, then active_brief_fast in fmcore
## Files touched
- plugin/tests/test_core.py
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmlib.py
- plugin/lib/fmscout.py
- plugin/tests/test_library.py
