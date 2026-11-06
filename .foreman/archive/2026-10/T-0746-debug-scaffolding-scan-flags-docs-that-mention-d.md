---
id: T-0746
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_execution.py]
depends_on: []
source: user
created: 2026-10-09T21:01:53Z
updated: 2026-10-09T21:02:11Z
base: 4b7cea3f8b05815b8f0561a31ce10d39cd30440e
base_tree: 4f39b47277dab8f133d7ffcfbd675530846900f2
verified: strong
---
# Debug-scaffolding scan flags docs that mention debug calls (CHANGELOG.md:10 at T-0695's close)
## Raw request
> Debug-scaffolding scan flags docs that mention debug calls (CHANGELOG.md:10 at T-0695's close)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a markdown line naming breakpoint() isn't flagged — verify with `python3 plugin/tests/run.py -p test_execution.py -k Scaffold`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: a .md line with breakpoint() stays quiet; skip prose files in the scan
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_execution.py -k Scaffold` → ✗ exit 1 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Scaffold 0s) / FAILED (1 classes) [ran] [tree 121d52b06721] (2026-10-09T21:02:00Z)
- (step 1) `python3 plugin/tests/run.py -p test_execution.py -k Scaffold` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Scaffold 0s) / OK [ran] [tree 669f9136eebb] (2026-10-09T21:02:06Z)
- (ac 1) `python3 plugin/tests/run.py -p test_execution.py -k Scaffold` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Scaffold 0s) / OK [ran] [tree 669f9136eebb] (2026-10-09T21:02:11Z)
- `python3 plugin/tests/run.py -p test_execution.py` → exit 0 · Ran 7 tests in 0.5s (6 classes, 16 at a time; slowest: Tried 0s, Scaffold 0s, ResumeCheck 0s) / OK [ran] [tree 669f9136eebb] (2026-10-09T21:02:11Z)
- (audit self) `self: the scan now skips prose files; code files are scanned as before (the existing Scaffold test still flags breakpoint() in x.py)` → no findings [tree 669f9136eebb] (2026-10-09T21:02:11Z)
## Log
- 2026-10-09T21:01:53Z created
- 2026-10-09T21:01:53Z focused
- 2026-10-09T21:02:11Z done
- 2026-10-09T21:02:11Z committed 8106b40 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0650 [FEATURE M, done, 0 steps] Keep steps in scope (I047, value 3/5, effort M, risk low)
- research T-0264-review-1: All three reviews are below. Only fmhooks, fmcore, fmcli, fmplugins and fmevolve were read. I did not run the tests or the PreToolUse hook. [st…
- T-0161 [SECURITY M, done, 3 steps] Guard: rm variable resolution fails closed on every way bash changes a variable (security review of T-0151) — lesson: Fail-closed mean…
- decision 2026-10-04: T-0224 (L) self-approved under full autonomy: tool-less mutation child, candidate on an evolve branch outside the live plugin, merge stays the user'…
- similar past tasks were M: consider --tier M
- similar finished tasks took 0–3 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Why not caught
none: the T-0695 tests only fed code files; the first real close (its own CHANGELOG) showed it — the new prose test now covers it
## Plan gaps
- failed first: step 1 test: a .md line with breakpoint() stays quiet; skip prose files in the scan
## Files touched
- plugin/tests/test_execution.py
- plugin/lib/fmcli.py
