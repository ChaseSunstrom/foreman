---
id: T-0921
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T19:25:19Z
updated: 2026-10-15T19:30:33Z
base: ea4344059af54d5926e0d177613e5ad95bba0e63
base_tree: db12b55f49e977f8e1290e20c7bd93eb52c4d642
verified: strong
---
# fm night holds a single-instance lease for its whole run
## Raw request
> fm night holds a single-instance lease for its whole run
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a second fm night while one runs exits at once saying one is running — verify with `python3 plugin/tests/run.py -k NightLease`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, then a non-blocking flock in cmd_night
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k NightLease` → ✗ exit 1 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: NightLease 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 1516cc256831] (2026-10-15T19:30:29Z)
- `python3 plugin/tests/run.py -k NightLease` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: NightLease 0s) / OK [ran] [tree 1516cc256831] (2026-10-15T19:30:29Z)
- (ac 1) `python3 plugin/tests/run.py -k NightLease` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: NightLease 0s) / OK [ran] [tree 1516cc256831] (2026-10-15T19:30:32Z)
- (step 1) `python3 plugin/tests/run.py -k Night` → exit 0 · Ran 10 tests in 1.9s (3 classes, 16 at a time; slowest: NightGuards 2s, Night 1s, NightLease 0s) / OK [ran] [tree 1516cc256831] (2026-10-15T19:30:32Z)
- (audit edge) `self: a non-dry fm night takes a non-blocking flock on <project>/night.lock right after resolving and holds it for the process; a second one exits with 'another fm night is already running'; a dry run plans only and takes none` → rebinding the module-level lease closes the earlier file first, so an in-process second call isn't locked out by itself [tree 1516cc256831] (2026-10-15T19:30:32Z)
- (audit self) `self: a non-dry fm night takes a non-blocking flock on <project>/night.lock right after resolving and holds it for the process; a second one exits with 'another fm night is already running'; a dry run plans only and takes none` → no findings [tree 1516cc256831] (2026-10-15T19:30:32Z)
## Log
- 2026-10-15T19:25:19Z created
- 2026-10-15T19:29:44Z focused
- 2026-10-15T19:30:32Z done
- 2026-10-15T19:30:33Z committed ca83b83 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-round7-20261015: Probe: `fm ideas` with reliability + delight, 2 rounds, past every earlier ideas.md (brainstorm-20261015-132957): 49 new titles, eac…
- decision 2026-10-15: Round 7 slate: 8 small reliability/delight builds (bare fm answers what now, close shows undo, demo ends in this repo, doctor state budget, night le…
- T-0708 [FEATURE M, done, 5 steps] Frontier 08 — Orchestrator control plane — lesson: Cross-session control fits in the hooks that already run: deliver on the next tool c…
- T-0489 [FEATURE M, done, 0 steps] Decisions, assumptions and promises (C052, value 3/5, effort M, risk low)
- similar past tasks were M: consider --tier M
- similar finished tasks took 0–5 steps
## Files touched
- plugin/tests/test_night.py
- plugin/lib/fmnight.py
