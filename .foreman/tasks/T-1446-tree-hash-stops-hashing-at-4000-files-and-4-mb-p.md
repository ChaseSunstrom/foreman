---
id: T-1446
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/lib/fmdoctor.py, plugin/tests/test_supply_delta.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-21T23:21:05Z
updated: 2026-10-23T08:03:38Z
base: 3c5ae76a0206085ed3df105b0b52ca2dad985e04
base_tree: db500c7a3aa9b69bee0ea5183e024daa6cac521f
plan0_at: 2026-10-23T08:01:59Z
plan0_scope: [plugin/lib/fmdoctor.py, plugin/tests/test_doctor.py, CHANGELOG.md]
verified: strong
---
# Supply check blind spot: a plugin file over 4 MB (or past the 4,000th) is only stamped with size and mtime, so an edit that keeps both goes unseen; hash large files' bytes within a budget, stamp the rest with ctime too
## Raw request
> - `_tree_hash` stops hashing at 4000 files and 4 MB per file, so the plain supply check has a blind spot for large files. T-1434's `skipped` stand-in covers only their size and mtime
> (noticed by an agent; research T-1441-review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] an installed plugin's 5 MB file changed in place with its size and mtime put back is reported as changed by the supply check, and a baseline from before reads as unchanged until something changes — verify with `python3 plugin/tests/run.py test_supply_delta`
## Non-goals
## Approach (options → choice → why)
A fourth hash beside sha, skipped and deps, as T-1434 and T-1459 added theirs: 'large', fed with each large file's bytes (streamed, LARGE_BYTES per plugin) and, past that budget or past the 4,000-file cap, its size, mtime and ctime (ctime can't be set back). An entry recorded before it has no 'large', which compares as unchanged and is upgraded in place, so no false alarm on upgrade. Options: raise the 4 MB cap (memory: the file is read whole into the main hash), add ctime to the existing skipped stand-in (changes an existing hash: every plugin with a big file would read as changed once), the new key (chosen).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: a 5 MB file edited with size and mtime restored; then a large hash (bytes streamed within a per-plugin budget, else size, mtime and ctime) as a new baseline key old entries adopt
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_supply_delta` → ✗ exit 1 · Ran 55 tests in 1.7s (2 classes, 16 at a time; slowest: SupplyDelta 1s, FindNeeds 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 6eb272a85d6e] (2026-10-23T08:02:28Z)
- `python3 plugin/tests/run.py test_supply_delta` → ✗ exit 1 · Ran 55 tests in 1.0s (2 classes, 16 at a time; slowest: SupplyDelta 1s, FindNeeds 0s) / FAILED (1 classes) [ran] [tree 6eb272a85d6e] (2026-10-23T08:02:28Z)
- `python3 plugin/tests/run.py test_supply_delta` → ✗ exit 1 · Ran 55 tests in 1.8s (2 classes, 16 at a time; slowest: SupplyDelta 1s, FindNeeds 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 6a757e7fa760] (2026-10-23T08:03:12Z)
- `python3 plugin/tests/run.py test_supply_delta` → exit 0 · Ran 55 tests in 1.0s (2 classes, 16 at a time; slowest: SupplyDelta 1s, FindNeeds 0s) / OK [ran] [tree 6a757e7fa760] (2026-10-23T08:03:12Z)
- (step 1) `python3 plugin/tests/run.py test_supply_delta test_safety test_doctor` → exit 0 · Ran 145 tests in 5.2s (32 classes, 16 at a time; slowest: SafetyGate 5s, ReleaseGate 3s, Command 2s) / OK [ran] [tree 6a757e7fa760] (2026-10-23T08:03:23Z)
- (ac 1) `python3 plugin/tests/run.py test_supply_delta` → exit 0 · Ran 55 tests in 1.0s (2 classes, 16 at a time; slowest: SupplyDelta 1s, FindNeeds 0s) / OK [ran] [tree 205721ad24ab] (2026-10-23T08:03:32Z)
- (audit adversary) `self: adversary, edge` → a same-size edit with mtime restored is caught by the content hash (tested); past the byte budget, ctime (which an unprivileged edit can't set back) stands in; links are never followed or read; a FIFO isn't a regular file and is never opened [tree 205721ad24ab] (2026-10-23T08:03:32Z)
- (audit edge) `self: adversary, edge` → an older baseline without the large key compares as unchanged and is upgraded in place (tested); the real check here stayed PASS in 0.3 s [tree 205721ad24ab] (2026-10-23T08:03:32Z)
- (audit self) `self: adversary, edge` → no findings [tree 205721ad24ab] (2026-10-23T08:03:32Z)
## Log
- 2026-10-21T23:21:05Z created
- 2026-10-23T08:01:56Z planned from capture
- 2026-10-23T08:01:57Z set scope=['plugin/lib/fmdoctor.py', 'plugin/tests/test_doctor.py', 'CHANGELOG.md']
- 2026-10-23T08:01:58Z focused
- 2026-10-23T08:02:17Z set scope=['plugin/lib/fmdoctor.py', 'plugin/tests/test_supply_delta.py', 'CHANGELOG.md']
- 2026-10-23T08:02:17Z criterion 1 verify: `python3 plugin/tests/run.py test_doctor.SupplyLarge` → `python3 plugin/tests/run.py test_supply_delta`
- 2026-10-23T08:03:36Z done
- 2026-10-23T08:03:38Z committed 025c5d2a (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1459-review: Verdict:** changes needed (no HIGH findings; the first four MEDIUMs are real gaps). [stale: plugin/lib/fmplugins.py changed since it was written]
- research T-1441-review: Verdict: changes needed.** The main hole is that the "gitignored and identical to the checkout" rule reads attacker-writable ignore rules. I read…
- T-1459 [SECURITY M, done, 3 steps] Supply check covers code in node_modules, .venv and the other skipped folders — lesson: A skip list in an integrity hash is a hiding p…
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_doctor.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, plugin/lib/fmdoctor.py, plugin/tests/test_doctor.py; re-ground the plan against them before editing
## Why not caught
T-1434 added a stand-in for large files but only size and mtime, and its test changed size or mtime; none kept both
## Lessons
- A change detector's stand-in must include something the editor can't set back (content, or ctime)
## Files touched
- plugin/tests/test_supply_delta.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
