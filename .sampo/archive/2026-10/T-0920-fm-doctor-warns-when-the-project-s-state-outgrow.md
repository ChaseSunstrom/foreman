---
id: T-0920
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T19:25:19Z
updated: 2026-10-15T19:29:39Z
base: 347cdf2b9241bd43df6d5159363ce5624b0a2e4b
base_tree: 5510d19b20656deedbe115749399b8e682532f15
verified: strong
---
# fm doctor warns when the project's state outgrows a budget, naming fm tidy
## Raw request
> fm doctor warns when the project's state outgrows a budget, naming fm tidy
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] doctor WARNs past the budget with the size and 'fm tidy'; quiet under it — verify with `python3 plugin/tests/run.py -k DoctorStateSize`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, then check_state_size in fmdoctor
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k DoctorStateSize` → ✗ exit 1 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: DoctorStateSize 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree db12b55f49e9] (2026-10-15T19:29:37Z)
- `python3 plugin/tests/run.py -k DoctorStateSize` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: DoctorStateSize 0s) / OK [ran] [tree db12b55f49e9] (2026-10-15T19:29:37Z)
- (ac 1) `python3 plugin/tests/run.py -k DoctorStateSize` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: DoctorStateSize 0s) / OK [ran] [tree db12b55f49e9] (2026-10-15T19:29:38Z)
- (step 1) `python3 plugin/tests/run.py -k DoctorStateSize` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: DoctorStateSize 0s) / OK [ran] [tree db12b55f49e9] (2026-10-15T19:29:38Z)
- (audit edge) `self: per project, files under its state dir summed by top-level part; past 200 MB a WARN names the project, its size, its biggest part and fm tidy --apply; the largest project here is ~55 MB, so no warning today` → unreadable files are skipped; a project dir with files at its root counts each file as its own part [tree db12b55f49e9] (2026-10-15T19:29:38Z)
- (audit self) `self: per project, files under its state dir summed by top-level part; past 200 MB a WARN names the project, its size, its biggest part and fm tidy --apply; the largest project here is ~55 MB, so no warning today` → no findings [tree db12b55f49e9] (2026-10-15T19:29:38Z)
## Log
- 2026-10-15T19:25:19Z created
- 2026-10-15T19:28:34Z focused
- 2026-10-15T19:29:38Z done
- 2026-10-15T19:29:39Z committed ea43440 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-round7-20261015: Probe: `fm ideas` with reliability + delight, 2 rounds, past every earlier ideas.md (brainstorm-20261015-132957): 49 new titles, eac…
- T-0785 [FEATURE S, done, 2 steps] fm doctor names the Foreman features the installed Claude Code is too old for — lesson: a probe for a setting must look where Foreman w…
- decision 2026-10-15: Round 7 slate: 8 small reliability/delight builds (bare fm answers what now, close shows undo, demo ends in this repo, doctor state budget, night le…
- T-0855 [FIX M, done, 5 steps] A fresh install is clean and works from a shell: doctor passes and shows only problems, fm check finds the test runner,… — lesson: Walk thr…
## Files touched
- plugin/tests/test_doctor.py
- plugin/lib/fmdoctor.py
