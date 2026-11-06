---
id: T-2429
type: FIX
tier: M
status: done
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-10-31T17:02:52Z
updated: 2026-10-31T17:11:37Z
baseline: true
base: d9115041184e84f71dae29c618c09565e77651cd
base_tree: d455f974cdcc22a862b53350a56f677457297457
predict_minutes: 7
predict_attempts: 1
plan0_at: 2026-10-31T17:05:04Z
plan0_scope: []
verified: strong
---
# Baseline red:…
## Raw request
> Baseline red: `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py` fails test_doctor.ScanCache.test_an_append_within_the_hour_still_hits. Captured by fm check: the gates are red, so fix this before new work (it may not be this task's doing).
## Interpretation
Reading 1: test_doctor.ScanCache's grow() appended (resetting the mtime to now) and then added 60 s, so in an hour's last minute the mtime crossed into the next hour and both caches missed; the ship ran it at 11:59 CDT. Reading 2: the cache key itself is wrong. Ruled out: the key floors to the hour by design (T-2298), and the test means 'an append within the hour'.
## Assumptions (confidence)
## Acceptance criteria
- [x] ScanCache's append stays within the hour whatever the clock reads — verify with `python3 plugin/tests/run.py test_doctor -k ScanCache`
## Non-goals
## Approach (options → choice → why)
1) shift from the pre-append mtime in the helper; fails if: another caller relies on now+seconds (none: both callers set mid-hour first). 2) use what exists: pin time.time with mock; fails if: os.utime still reads the real clock on append. 3) do less: retry the test; fails if: it hides the bug. Choice 1 (90%): one line, the test's intent.
## Risks and rollback
## Execution prompt
## Steps
1. [x] grow() shifts from the mtime before the append
## Resume here
## Docs impact
none: a test helper
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_doctor -k ScanCache` → exit 0 · Ran 9 tests in 0.7s (1 classes, 16 at a time; slowest: ScanCache 0s) / OK [ran] [tree d455f974cdcc] (2026-10-31T17:05:18Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor -k ScanCache` → exit 0 · Ran 9 tests in 0.8s (1 classes, 16 at a time; slowest: ScanCache 0s) / OK [ran] [tree d455f974cdcc] (2026-10-31T17:05:20Z)
- (audit intent) `self-review: the helper's only callers set a mid-hour mtime first; the shift now starts from it, so the append can't move the hour` → the test means an append within the hour still hits; it now holds at any wall-clock minute [tree d455f974cdcc] (2026-10-31T17:05:20Z)
- (audit edge) `self-review: the helper's only callers set a mid-hour mtime first; the shift now starts from it, so the append can't move the hour` → the 2-hour default still crosses a boundary from mid-hour, as its other test needs [tree d455f974cdcc] (2026-10-31T17:05:20Z)
## Log
- 2026-10-31T17:02:52Z created
- 2026-10-31T17:05:02Z planned: it has criteria and steps
- 2026-10-31T17:05:03Z focused
- 2026-10-31T17:05:04Z predicted from its closes: 7 min, 1 attempt(s)
- 2026-10-31T17:05:25Z done
- 2026-10-31T17:05:38Z guard authorization added: publish
- 2026-10-31T17:11:37Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2286 [FIX M, dropped, 0 steps] Baseline red:…
- T-2309 [FIX S, done, 1 steps] Guard speed tests time CPU, not the wall clock, so a loaded host can't fail them — lesson: A complexity bar measures CPU (time.process_time…
- T-2305 [FIX S, done, 1 steps] Hooks import no glob: T-2297's leads-record prune lists the folder without a top-level import — lesson: A new top-level import in fmhooks c…
- decision 2026-10-31: [revisited: The Genesis frame may grow] [cites: the user's steer 2026-10-30 (sixth): the frame grows, never shrinks] [check: python3 plugin/tests/ru…
- similar finished tasks took 1–1 steps
- start here (files T-2309 touched): plugin/tests/test_guard.py
## Regression test
none: the failure needs the real clock in an hour's last minute (the append sets the mtime to the wall clock, which no mock reaches); the fix removes the dependence on the append's mtime, read in the diff
## Why not caught
none: it fails only in an hour's last minute; the ship's full run landed there at 11:59
## Lessons
- A test that appends then shifts an mtime is shifting from the wall clock: read the mtime before the write
