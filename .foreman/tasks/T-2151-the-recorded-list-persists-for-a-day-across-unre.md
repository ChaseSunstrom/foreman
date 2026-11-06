---
id: T-2151
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T12:08:14Z
updated: 2026-10-30T12:35:39Z
base: 4eab1f8f9c684224f28f2249f0f1ead4d4b3ade4
base_tree: 9b1934d8ba3e06e484f63e1efe55aebd38a355f3
plan0_at: 2026-10-30T12:25:57Z
plan0_scope: []
verified: ok
---
# The recorded list persists for a day across unrelated later turns. Clearing it on a…
## Raw request
> the recorded list persists for a day across unrelated later turns. Clearing it on a non-multi-part, non-"yes" prompt would narrow that
> (noticed by an agent; research T-2146-review)
## Interpretation
Already bounded: the gate fires only on a done claim and T-2146 holds each clause once ever, so a stale list holds at most once per clause; clearing on a one-clause prompt would drop the gate on a mid-request steer (decision recorded). Left to do: the gate's docstring still says held once per set.
## Assumptions (confidence)
## Acceptance criteria
- [x] the clauses gate docstring says each clause holds once — verify with `grep -n 'held once per clause' plugin/lib/fmhooks.py`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fix the stale docstring
## Resume here
## Docs impact
## Verification evidence
- (step 1) `grep -n 'held once per clause' plugin/lib/fmhooks.py` → exit 0 · 3519:    """T-2138: a done claim while the last request has clauses no task covers, held once per clause (T-2146): a [ran] [tree 27cd27c9d30b] (2026-10-30T12:26:05Z)
- (ac 1) `grep -n 'held once per clause' plugin/lib/fmhooks.py` → exit 0 · 3519:    """T-2138: a done claim while the last request has clauses no task covers, held once per clause (T-2146): a [ran] [tree 27cd27c9d30b] (2026-10-30T12:26:05Z)
- (ac 1) `grep -n 'held once per clause' plugin/lib/fmhooks.py` → exit 0 · 3519:    """T-2138: a done claim while the last request has clauses no task covers, held once per clause (T-2146): a [ran] [tree 27cd27c9d30b] (2026-10-30T12:27:10Z)
- `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 210 tests in 54.9s (28 classes, 16 at a time; slowest: Stop 54s, NoTaskGate 39s, PreToolUse 33s) / OK [ran] [tree 27cd27c9d30b] (2026-10-30T12:27:10Z)
- (audit self) `self: docstring-only change; the gate's behaviour (done claim, hold once per clause) re-read at fmhooks.py:3518-3538` → no findings [tree 27cd27c9d30b] (2026-10-30T12:27:10Z)
## Log
- 2026-10-30T12:08:14Z created
- 2026-10-30T12:25:55Z set tier=S, type=CLEAN
- 2026-10-30T12:25:56Z planned: it has criteria and steps
- 2026-10-30T12:25:56Z focused
- 2026-10-30T12:26:14Z scope: one docstring in fmhooks.py
- 2026-10-30T12:28:19Z done
- 2026-10-30T12:28:22Z committed aa82235f (1 file)
- 2026-10-30T12:33:18Z guard authorization added: publish
- 2026-10-30T12:35:39Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2146-review: Changes needed. These are two small, cheap fixes, not a redesign. [stale: plugin/lib/fmhooks.py, plugin/lib/fmrecall.py, plugin/tests/test_hooks.…
- research T-2138-review: Verdict: approve with nits.** The gate does what the acceptance criterion says. I did not run the tests. The nits below are scope and test gaps, …
- decision 2026-10-30: [cites: T-2151] T-2151: no clearing of the recorded clause list on later prompts; T-2146's hold-once-per-clause already bounds a stale list to one h…
- decision 2026-10-30: T-2138 clauses gate staleness: a one-day window, not the current turn's start
## Lessons
- Before building a narrowing, check whether an earlier change already bounds the harm; T-2146's hold-once made this a doc fix
## Files touched
- plugin/lib/fmhooks.py
