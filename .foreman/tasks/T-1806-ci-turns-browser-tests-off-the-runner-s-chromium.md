---
id: T-1806
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-28T02:28:10Z
updated: 2026-10-28T02:38:53Z
base: b4c1e45f07e6664d5ca11b35ce394dbe4b13b06d
base_tree: a7bb882d4687602dd1c9a5d3349d8ba133dc23de
plan0_at: 2026-10-28T02:28:11Z
plan0_scope: []
verified: strong
---
# CI turns browser tests off: the runner's chromium crashes under parallel load
## Raw request
> CI turns browser tests off: the runner's chromium crashes under parallel load
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] FOREMAN_CHROME=none makes headless_chrome() None and CI sets it — verify with `FOREMAN_CHROME=none python3 -c 'import sys; sys.path[:0]=["plugin/tests","plugin/lib"]; import helpers; assert helpers.headless_chrome() is None' && grep -q 'FOREMAN_CHROME: none' .github/workflows/test.yml`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] helpers honors FOREMAN_CHROME=none; test.yml sets it
## Resume here
<!-- auto -->
- 2026-10-28T02:31:38Z step 1/1: helpers honors FOREMAN_CHROME=none; test.yml sets it
- git: foreman/build; 3 uncommitted: .github/workflows/test.yml, plugin/lib/fmshot.py, plugin/tests/helpers.py
- touched since last checkpoint: .github/workflows/test.yml, plugin/tests/helpers.py, plugin/lib/fmshot.py
## Docs impact
## Verification evidence
- `cd plugin/tests && python3 -m unittest -q test_fmshot` → ✗ exit 1 · Ran 30 tests in 42.360s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 80c74128f069] (2026-10-28T02:34:13Z)
- `cd plugin/tests && python3 -m unittest -q test_fmshot` → exit 0 · Ran 30 tests in 42.155s / OK [ran] [tree 80c74128f069] (2026-10-28T02:34:13Z)
- (step 1) `FOREMAN_CHROME=none python3 -c 'import sys; sys.path[:0]=["plugin/tests","plugin/lib"]; import helpers, fmshot; assert helpers.headless_chrome() is None and fmshot.chrome() is None' && grep -q 'FOREMAN_CHROME: none' .github/workflows/test.yml` → exit 0 · (no output) [ran] [tree 80c74128f069] (2026-10-28T02:34:19Z)
- (ac 1) `FOREMAN_CHROME=none python3 -c 'import sys; sys.path[:0]=["plugin/tests","plugin/lib"]; import helpers; assert helpers.headless_chrome() is None' && grep -q 'FOREMAN_CHROME: none' .github/workflows/test.yml` → exit 0 · (no output) [ran] [tree 80c74128f069] (2026-10-28T02:38:05Z)
- (audit edge) `self-review: the switch only returns None early in the two browser finders; every browser test already skips on None; local gates keep running them` → FOREMAN_CHROME unset or a path keeps the old search; only the literal 'none' turns it off [tree 80c74128f069] (2026-10-28T02:38:05Z)
- (audit intent) `self-review: the switch only returns None early in the two browser finders; every browser test already skips on None; local gates keep running them` → CI's ubuntu job stops failing on browser crashes while browser coverage stays in local gates [tree 80c74128f069] (2026-10-28T02:38:05Z)
- (audit self) `self-review: the switch only returns None early in the two browser finders; every browser test already skips on None; local gates keep running them` → no findings [tree 80c74128f069] (2026-10-28T02:38:05Z)
## Log
- 2026-10-28T02:28:10Z created
- 2026-10-28T02:28:11Z focused
- 2026-10-28T02:34:19Z scope: plugin/lib/fmshot.py chrome() honors FOREMAN_CHROME=none too, so fm shot and the tests agree; test_fmshot.py gets the regression test
- 2026-10-28T02:38:52Z done
- 2026-10-28T02:38:53Z committed d678abcf (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1799 [FIX M, done, 3 steps] CI green on ubuntu: runner-specific test failures fixed — lesson: marshal.dumps sets ref flags from refcounts: compare two code objects onl…
- T-1356 [FEATURE M, done, 3 steps] fm code limits and failover: a worker turn's failure is sorted (usage limit with its reset, sign-in, crash, timeout); a limit within th…
- T-1636 [FEATURE M, done, 3 steps] fm shot: viewport and frame captures and a poster frame per animated page, or a stated reason without a browser — lesson: Headless Chro…
- decision 2026-10-23: Edit the main checkout while a background fm check runs under heavy builder load
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–3 steps
## Why not caught
local gates run with a working browser; only CI's snap chromium crashes under the 16-way parallel suite
## Lessons
- a browser that starts can still crash under load: CI gets an explicit off switch rather than probes that race
## Files touched
- .github/workflows/test.yml
- plugin/tests/helpers.py
- plugin/lib/fmshot.py
- plugin/tests/test_fmshot.py
