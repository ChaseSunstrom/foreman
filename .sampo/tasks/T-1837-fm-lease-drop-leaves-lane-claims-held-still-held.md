---
id: T-1837
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T10:33:21Z
updated: 2026-10-28T15:52:54Z
base: 415be9e7a9a1ce66a90416339436609ef7c49c5a
base_tree: f0ed0e563b9688d847143b63db31de3cc17482b5
plan0_at: 2026-10-28T15:52:06Z
plan0_scope: []
verified: strong
---
# Fm lease drop leaves lane claims held ('still held: N lane claim(s)') after a builder fini
## Raw request
> fm lease drop leaves lane claims held ('still held: N lane claim(s)') after a builder finishes
## Interpretation
A builder's closing fm lease drop says 'still held: N lane claim(s)' and builders report it as unfinished work. Those are the lane's pre-claims, freed by fm lane merge/remove (fmbus.release). The line should say so, so no one chases them.
## Assumptions (confidence)
## Acceptance criteria
- [x] a bare drop with lane claims says they end when the lane merges or is removed — verify with `python3 plugin/tests/run.py test_bus`
## Non-goals
## Approach (options → choice → why)
Options: (1) say when they end in the drop line; (2) let a builder's drop release its lane's claims (wrong: the lane is not merged, a parallel session could then edit the files); (3) hide the line. Choice: 1, the claims are correct, only the line misleads.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_bus, then the drop line in fmbus
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bus` → exit 0 · Ran 21 tests in 6.8s (6 classes, 16 at a time; slowest: Watch 6s, Lease 4s, Approvals 4s) / OK [ran] [tree 860f7ab983ec] (2026-10-28T15:52:28Z)
- (ac 1) `python3 plugin/tests/run.py test_bus` → exit 0 · Ran 21 tests in 6.2s (6 classes, 16 at a time; slowest: Watch 6s, Lease 4s, Approvals 4s) / OK [ran] [tree 860f7ab983ec] (2026-10-28T15:52:41Z)
- (audit intent) `self: one line changed in fmbus lease drop; it names the task and says the claims end at lane merge/remove (fmbus.release callers in fmlanes: merge, remove, resume); act is non-null whenever lane>0, so act.id is safe` → a builder's closing drop no longer reads as unfinished work; the claims stay, which is right until the lane merges [tree 860f7ab983ec] (2026-10-28T15:52:41Z)
- (audit edge) `self: one line changed in fmbus lease drop; it names the task and says the claims end at lane merge/remove (fmbus.release callers in fmlanes: merge, remove, resume); act is non-null whenever lane>0, so act.id is safe` → lane is 0 without an active task, so the act.id branch never runs without one [tree 860f7ab983ec] (2026-10-28T15:52:41Z)
- (audit self) `self: one line changed in fmbus lease drop; it names the task and says the claims end at lane merge/remove (fmbus.release callers in fmlanes: merge, remove, resume); act is non-null whenever lane>0, so act.id is safe` → no findings [tree 860f7ab983ec] (2026-10-28T15:52:41Z)
## Log
- 2026-10-28T10:33:21Z created
- 2026-10-28T15:52:04Z set tier=S
- 2026-10-28T15:52:06Z focused
- 2026-10-28T15:52:53Z done
- 2026-10-28T15:52:54Z committed 52ba8c8f (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1731 [FIX M, done, 4 steps] Lane and close friction: finish --commit and shared files, CLEAN behaviour-lock in builder briefs, check --affected ski… — lesson: Skip a t…
- research T-1294-review: Verdict: approve with nits.** The diff file holds only the CHANGELOG hunk. I reviewed the real working-tree changes in `fmbus.py`, `fmcode.py` an…
- research wave2-plan-a4b64956d53d543cc: === T-1058 [stale: plugin/lib/fmbacktest.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py changed since it was written]
- decision 2026-10-16: T-1069 self-approved under full autonomy: a race clones the brief as a 'b' task so each builder works under its own id; pick merges the winner throu…
- similar past tasks were M: consider --tier M
## Files touched
- plugin/tests/test_bus.py
- plugin/lib/fmbus.py
