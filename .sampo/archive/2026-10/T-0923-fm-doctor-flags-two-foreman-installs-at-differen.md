---
id: T-0923
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T19:25:20Z
updated: 2026-10-15T19:32:41Z
base: f3b66c7696e4795f981456f11ad44431ddb78235
base_tree: f5076ebe45249ed7ff399e2c67f51ffdcb4f7d04
verified: strong
---
# fm doctor flags two Foreman installs at different versions (marketplace and install.sh)
## Raw request
> fm doctor flags two Foreman installs at different versions (marketplace and install.sh)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] doctor WARNs when the marketplace foreman and the install.sh copy report different versions — verify with `python3 plugin/tests/run.py -k DoctorDualInstall`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, then a check in fmdoctor
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k DoctorDualInstall` → ✗ exit 1 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: DoctorDualInstall 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 48906f1a9121] (2026-10-15T19:32:39Z)
- `python3 plugin/tests/run.py -k DoctorDualInstall` → exit 0 · Ran 2 tests in 0.1s (1 classes, 16 at a time; slowest: DoctorDualInstall 0s) / OK [ran] [tree 48906f1a9121] (2026-10-15T19:32:39Z)
- (ac 1) `python3 plugin/tests/run.py -k DoctorDualInstall` → exit 0 · Ran 2 tests in 0.1s (1 classes, 16 at a time; slowest: DoctorDualInstall 0s) / OK [ran] [tree 48906f1a9121] (2026-10-15T19:32:40Z)
- (step 1) `python3 plugin/tests/run.py -k Doctor` → exit 0 · Ran 3 tests in 0.2s (2 classes, 16 at a time; slowest: DoctorStateSize 0s, DoctorDualInstall 0s) / OK [ran] [tree 48906f1a9121] (2026-10-15T19:32:40Z)
- (audit edge) `self: an installed foreman@foreman whose marketplace isn't this home (GitHub, another folder), beside this home's plugin/, at another version, warns with both versions and how to keep one; the marketplace being this home (this machine) passes; same version passes with a note` → no installed entry, or no plugin/ in this home, is one install; doctor reads the records only, never writes them [tree 48906f1a9121] (2026-10-15T19:32:40Z)
- (audit self) `self: an installed foreman@foreman whose marketplace isn't this home (GitHub, another folder), beside this home's plugin/, at another version, warns with both versions and how to keep one; the marketplace being this home (this machine) passes; same version passes with a note` → no findings [tree 48906f1a9121] (2026-10-15T19:32:40Z)
## Log
- 2026-10-15T19:25:20Z created
- 2026-10-15T19:31:33Z focused
- 2026-10-15T19:32:40Z done
- 2026-10-15T19:32:41Z committed 5e8acd5 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0391 [FEATURE S, done, 1 steps] FEATURE: show which Foreman code a session actually runs — SessionStart logs plugin root + — lesson: Compare versions by order, not equ…
- research brainstorm-round7-20261015: Probe: `fm ideas` with reliability + delight, 2 rounds, past every earlier ideas.md (brainstorm-20261015-132957): 49 new titles, eac…
- T-0785 [FEATURE S, done, 2 steps] fm doctor names the Foreman features the installed Claude Code is too old for — lesson: a probe for a setting must look where Foreman w…
- decision 2026-10-03: Round 4 slate: guard replay corpus (M) and a mod version check in fm doctor (S) first; four followups to the inbox
- similar finished tasks took 1–2 steps
## Files touched
- plugin/tests/test_doctor.py
- plugin/lib/fmdoctor.py
