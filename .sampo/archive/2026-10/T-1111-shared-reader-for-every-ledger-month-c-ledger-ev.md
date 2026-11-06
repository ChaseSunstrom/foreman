---
id: T-1111
type: CLEAN
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmoutcomes.py, plugin/tests/test_ledger_chain.py]
depends_on: []
source: user
created: 2026-10-16T05:34:59Z
updated: 2026-10-16T05:35:49Z
base: 342cc76287f62aee5aa7dc23c79b9ffe3e29c499
base_tree: a49406a7bdc7552124c7a85f8baaea4fdc38a466
verified: ok
---
# Shared reader for every ledger month: c.ledger_events(p, kinds, since) reads the archives and the live file; fmoutcomes uses it
## Raw request
> Shared reader for every ledger month: c.ledger_events(p, kinds, since) reads the archives and the live file; fmoutcomes uses it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] ledger_events returns matching events from archived months and the live file, oldest first, filtered by kind and since — verify with `python3 plugin/tests/run.py test_ledger_chain test_outcomes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test, then move fmoutcomes._events into fmcore.ledger_events with a since filter
## Resume here
## Docs impact
none: internal helper (docstring)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ledger_chain` → ✗ exit 1 · Ran 24 tests in 3.3s (2 classes, 16 at a time; slowest: Chain 3s, Receipt 1s) / FAILED (1 classes) [ran] [tree 32a3d68d5377] (2026-10-16T05:35:13Z)
- (step 1) `python3 plugin/tests/run.py test_ledger_chain test_outcomes` → exit 0 · Ran 39 tests in 9.1s (11 classes, 16 at a time; slowest: Survival 9s, Chain 3s, Receipt 2s) / OK [ran] [tree 6790c65645a4] (2026-10-16T05:35:35Z)
- (ac 1) `python3 plugin/tests/run.py test_ledger_chain test_outcomes` → exit 0 · Ran 39 tests in 9.1s (11 classes, 16 at a time; slowest: Survival 9s, Chain 3s, Receipt 2s) / OK [ran] [tree 6790c65645a4] (2026-10-16T05:35:48Z)
- (audit self) `self: reader tested over an archived month, a bad line, kind and since filters; fmoutcomes' tests unchanged` → no findings [tree 6790c65645a4] (2026-10-16T05:35:48Z)
## Log
- 2026-10-16T05:34:59Z created
- 2026-10-16T05:34:59Z focused
- 2026-10-16T05:35:49Z done
- 2026-10-16T05:35:49Z committed fc4d390 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- T-1099 [FIX S, done, 3 steps] Ledger roll takes the ledger lock and keeps time order: _roll_ledger keeps unparseable-ts — lesson: Rewriting a file other processes append…
- research wave1-plan-a306a171bb6861f90: === T-1044 [stale: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmcost.py changed since it was written]
- decision 2026-10-14: Keep the Read hook unscoped (T-0782 dropped)
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_core.py, plugin/tests/test_outcomes.py
## Behaviour lock
test_outcomes (15 tests, incl. the archived-ledger survival case) passes unchanged before and after: fmoutcomes reads the same events through c.ledger_events.
## Lessons
- When a second module needs a private reader, promote it to the core module before the third copy appears
## Plan gaps
- failed first: step 1 Test, then move fmoutcomes._events into fmcore.ledger_events with a since filter
## Files touched
- plugin/tests/test_ledger_chain.py
- plugin/lib/fmcore.py
- plugin/lib/fmoutcomes.py
