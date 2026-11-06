---
id: T-0201
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-04T04:07:01Z
updated: 2026-10-04T04:14:11Z
base: 7727f9145fc3083f1632a6990218d74c303f1d3e
base_tree: 99cced0e67c2b757a19cb848b3902a6a318c4282
verified: strong
---
# Guard: refreshing a marketplace before one plugin update is one plugin change
## Raw request
> Guard: a marketplace update plus a plugin update from that same marketplace is one plugin change (fmguard.py:63 counts them as two; one yes should cover both, installs/adds still separate)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] marketplace update + one plugin update in one command is a single plugin change; install/enable after a marketplace update still blocks — verify with `python3 plugin/tests/run.py -k test_guard`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test first, then absorb marketplace-update findings beside exactly one plugin update in fmguard.check
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 58 tests in 1.2s (18 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, Core 0s) / OK [ran] [tree 880cb93cfa98] (2026-10-04T04:13:08Z)
- (ac 1) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 58 tests in 1.2s (18 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, Core 0s) / OK [ran] [tree 880cb93cfa98] (2026-10-04T04:14:06Z)
- (audit self) `self checklist + adversary thought: update was never pinned, so absorbing listing refreshes beside exactly one update can't skip a pin; install/enable, add, and two updates still block (tested); fm replay shows no newly allowed real command` → pass [tree 880cb93cfa98] (2026-10-04T04:14:06Z)
- `python3 plugin/tests/run.py -k test_guard` → ✗ exit 1 · Ran 58 tests in 1.3s (18 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, Core 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 880cb93cfa98] (2026-10-04T04:14:11Z)
- `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 58 tests in 1.2s (18 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, InterpreterWrites 0s) / OK [ran] [tree 880cb93cfa98] (2026-10-04T04:14:11Z)
- (audit adversary) `self checklist + adversary review` → update was never pinned, so absorbing listing refreshes beside exactly one update can't skip a pin; refresh+install, refresh+enable, add+update and two updates still block (tested); fm replay: no newly allowed real command [tree 880cb93cfa98] (2026-10-04T04:14:11Z)
- (audit self) `self checklist + adversary review` → pass [tree 880cb93cfa98] (2026-10-04T04:14:11Z)
## Log
- 2026-10-04T04:07:01Z created
- 2026-10-04T04:12:39Z planned from capture
- 2026-10-04T04:12:39Z focused
- 2026-10-04T04:13:07Z steer: criterion 1's verify corrected (run.py takes -k, not a positional)
- 2026-10-04T04:14:11Z done
- 2026-10-04T04:14:11Z committed ceb9fe6 (2 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0036-adversary: Confirmed: `check()` returns `Block` only when the category isn't in `ctx.allow`. Since `plugin` is in `ctx.allow` (from the earlier grant), `b…
- research t0036-adversary-recheck: All four call sites correctly updated to the 5-tuple. This confirms the pin plumbs through `_ask_prompt` (dialog) and `_grant_prompted`…
- T-0016 [FEATURE L, done, 4 steps] Approved plugin/marketplace installs on demand; conflict-free integration of plugins and skills
- research t0018-final-operator: Not directly related. I have sufficient evidence now. Let me finalize.
- similar past tasks were L: consider --tier L
- the similar finished task took 4 steps
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
