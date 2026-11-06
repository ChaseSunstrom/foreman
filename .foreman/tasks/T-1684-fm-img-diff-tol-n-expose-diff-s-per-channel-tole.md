---
id: T-1684
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmimg.py, plugin/tests/test_raster.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T21:51:00Z
updated: 2026-10-23T09:02:47Z
base: 19689171678d1432d168d7c1987366da181c40df
base_tree: 9eb210c6747e6e11fbe0a26739786afc89723205
plan0_at: 2026-10-23T09:01:46Z
plan0_scope: [plugin/lib/fmcli.py, plugin/lib/fmimg.py, plugin/tests/test_raster.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# Fm img diff --tol N: expose diff()'s per-channel tolerance on the command line (T-1630 not
## Raw request
> fm img diff --tol N: expose diff()'s per-channel tolerance on the command line (T-1630 noticed)
## Interpretation
fm img diff gains --tol N (0 to 255), passed to diff()'s existing per-channel tolerance; the text says 'within N a channel' and the JSON carries tol. Out of range exits 2.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm img diff --tol N treats a pixel within N on every channel as unchanged, refuses N outside 0 to 255 with exit 2, and reports the tolerance — verify with `python3 plugin/tests/run.py test_raster`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, then the flag, the check and the report
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_raster` → exit 0 · Ran 21 tests in 2.0s (2 classes, 16 at a time; slowest: Img 2s, Cube 0s) / OK [ran] [tree 6d1b89befd09] (2026-10-23T09:02:11Z)
- (audit self) `read the diff; ran the new test alone (not skipped) and the raster suite` → ok: --tol reaches diff(); -1 and 256 exit 2 with the range; the text and JSON name the tolerance; tol 0 output unchanged [tree 6d1b89befd09] (2026-10-23T09:02:12Z)
- (ac 1) `python3 plugin/tests/run.py test_raster` → exit 0 · Ran 21 tests in 2.0s (2 classes, 16 at a time; slowest: Img 2s, Cube 0s) / OK [ran] [tree 6d1b89befd09] (2026-10-23T09:02:17Z)
- (audit edge) `self review; the new test runs without Pillow; test_raster green` → --tol -1 and 256 exit 2 naming 0 to 255; --tol 0 keeps the old text; the JSON carries tol [tree 6d1b89befd09] (2026-10-23T09:02:17Z)
- (audit self) `self review; the new test runs without Pillow; test_raster green` → no findings [tree 6d1b89befd09] (2026-10-23T09:02:17Z)
## Log
- 2026-10-22T21:51:00Z created
- 2026-10-23T08:58:59Z set tier=S, scope=['plugin/lib/fmcli.py', 'plugin/lib/fmimg.py', 'plugin/tests/test_raster.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-23T09:01:45Z focused
- 2026-10-23T09:02:46Z done
- 2026-10-23T09:02:47Z committed 26a7bc68 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1630-review: Verdict:** approve with nits. No HIGH findings. I read the diff and the dispatcher code only. I did not run anything, so the timing, memory and t…
- T-1630 [FEATURE M, done, 3 steps] fm img: stdlib PNG encode/decode and a pixel diff with a changed-pixel count — lesson: A bomb test must fail without the cap it protect…
- T-1339 [FEATURE M, done, 4 steps] fm code run friction: a blocked, stalled or killed run, or one that fails before its task exists, counts as friction with fm code in Fo…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/tests/test_raster.py; re-ground the plan against them before editing
## Files touched
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmimg.py
- plugin/tests/test_raster.py
