---
id: T-1051
type: FEATURE
tier: S
status: dropped
priority: normal
scope: [plugin/lib/fmwatch.py, plugin/lib/fmcli.py, plugin/tests/test_ui.py]
depends_on: []
source: followup
created: 2026-10-16T03:42:11Z
updated: 2026-10-16T06:12:55Z
---
# Profile fm ui gather (the pane polls it every 2 s) and memoize what's slow; skip if it's u
## Raw request
> Profile fm ui gather (the pane polls it every 2 s) and memoize what's slow; skip if it's under 100 ms (T-1029 C7)
## Interpretation
Measure how long `fmwatch.gather` (fmwatch.py:47) and the full `view` (fmwatch.py:442) take, and memoize the slow parts. If the total is under 100 ms, say so and stop. Nothing times it today. The `view()` sections are already wrapped in `_guarded`.
## Assumptions (confidence)
## Acceptance criteria
- [ ] `fm ui --profile --json` returns ms for each section and a total — verify with `python3 plugin/tests/run.py test_ui`
- [ ] a memoized section recomputes only when its files change — verify with `python3 plugin/tests/run.py test_ui`
## Non-goals
## Approach (options → choice → why)
(a) cache whole `view` for 2 s; (b) time each section and cache only the slow ones, keyed by file mtimes; (c) do nothing. Choice (b): the pane starts a fresh `fm ui --json` process per poll, so an in-process cache is useless and the cache must live on disk or be skipped. Step 1 is `fm ui --profile`, printing ms per `view()` section and per `gather` part. Step 2 applies only if the measured total is ≥ 100 ms: wrap the slowest section in `_memo(key=(mtime, size of ledger.jsonl, tasks dir, meta.json))` stored in `p.dir/ui-cache.json`. `_tail_jsonl` of events.jsonl (256 KB) and `_closes_since` (the whole ledger) are the likely suspects. Both are inferred, not measured.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Failing tests: `--profile --json` has `sections` (name → ms) and `total_ms`. With a call counter on the slow function, two views with no change compute once; after a ledger append they compute again.  <- CURRENT
2. [ ] Add the `--profile` flag in cmd_ui (fmwatch.py:589) and the parser at fmcli `ui`.
3. [ ] Run it on a big fixture; memoize only what is over 100 ms, otherwise record "under 100 ms, skipped" in the task's insight.
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-16T03:42:11Z created
- 2026-10-16T05:00:59Z set scope=['plugin/lib/fmwatch.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_ui.py']
- 2026-10-16T05:01:00Z set tier=S
- 2026-10-16T06:12:55Z dropped: folded into T-1082: the profile is done there (brief parsing 0.49 s of fm ui's 1.2 s) and the memo is its fix
## Follow-ups captured
