---
id: T-0749
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_verifying.py]
depends_on: []
source: user
created: 2026-10-09T21:28:02Z
updated: 2026-10-09T21:28:28Z
base: ec9c63c49634c9d7a0640fb0d302f4cd3ec2a886
base_tree: 26fb9d7d1c1d41c0d6f7b7e102828a5bc58024db
verified: strong
---
# Check track record misses failures recorded by fm task finish (said the full suite never failed)
## Raw request
> Check track record misses failures recorded by fm task finish (said the full suite never failed)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a check that failed in a finish run counts as having caught a failure — verify with `python3 plugin/tests/run.py -p test_verifying.py -k CatchRate`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: a finish-recorded failure then pass counts; finish logs which commands failed
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_verifying.py -k CatchRate` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: CatchRate 0s) / FAILED (1 classes) [ran] [tree 781ef0704bf6] (2026-10-09T21:28:15Z)
- (step 1) `python3 plugin/tests/run.py -p test_verifying.py -k CatchRate` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: CatchRate 0s) / OK [ran] [tree a7b61a747f74] (2026-10-09T21:28:21Z)
- (ac 1) `python3 plugin/tests/run.py -p test_verifying.py -k CatchRate` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: CatchRate 0s) / OK [ran] [tree a7b61a747f74] (2026-10-09T21:28:27Z)
- `python3 plugin/tests/run.py -p test_verifying.py` → exit 0 · Ran 8 tests in 0.5s (7 classes, 16 at a time; slowest: Claims 0s, Verifier 0s, Stale 0s) / OK [ran] [tree a7b61a747f74] (2026-10-09T21:28:27Z)
- (audit self) `self: finish now logs each command it ran with its exit code, and catch rates read those beside evidence events; older finish events carry no commands, so history before today still undercounts (the hint never gates)` → no findings [tree a7b61a747f74] (2026-10-09T21:28:27Z)
## Log
- 2026-10-09T21:28:02Z created
- 2026-10-09T21:28:03Z focused
- 2026-10-09T21:28:27Z done
- 2026-10-09T21:28:28Z committed f59c73d (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0174 [FIX M, done, 4 steps] Parallel runs clean up after a failure, re-check main before merging; task commits take paths literally — lesson: A cleanup that covers onl…
- T-0370 [FIX M, done, 2 steps] Guard: a $(…) substitution no longer turns off variable tracking, so a literal S=/tmp/… stays known — lesson: Before widening what the guar…
- T-0736 [FIX S, done, 2 steps] Not-verified warning at finish fires even when the full suite ran (T-0703: fm check-free r
- decision 2026-09-26: Full autonomy never asks mid-run but still can't grant itself core or run destructive/irreversible guard categories: those are recorded with fm ask …
- similar finished tasks took 2–4 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Why not caught
none: T-0697's test fed only evidence events; the first real close showed the suite's failures live in finish events
## Plan gaps
- failed first: step 1 test: a finish-recorded failure then pass counts; finish logs which commands failed
## Files touched
- plugin/tests/test_verifying.py
- plugin/lib/fmcli.py
