---
id: T-2100
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T05:24:52Z
updated: 2026-10-30T11:49:20Z
base: cf6037b1585b9c90847ad2ceaf243365cf14da8e
base_tree: 9ab101e0418d11c37de50393dd494611e8c3e51d
plan0_at: 2026-10-30T11:40:57Z
plan0_scope: []
verified: strong
---
# fm genesis step: in gen 1 name fm genesis spec when spec.md is missing (after gen-0,…
## Raw request
> fm genesis step: in gen 1 name fm genesis spec when spec.md is missing (after gen-0, before the seed), keeping the T-2095 stage tests
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis step names fm genesis spec after gen-0 when spec.md is missing and gen-0 §2 maps to exam kinds; no mappable cap goes straight to seed — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] step(): spec stage before seed when spec.md is missing and a §2 cap maps to a kind; tests updated
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisStep test_genesis.GenesisDraft` → red as expected (exit 1) · Ran 21 tests in 2.2s (2 classes, 16 at a time; slowest: GenesisDraft 2s, GenesisStep 1s) / FAILED (2 classes) [ran] [tree 9ecd8be5f1dc] (2026-10-30T11:41:28Z)
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 71 tests in 4.0s (11 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree b3dc3eb694e2] (2026-10-30T11:41:52Z)
- `python3 plugin/tests/run.py test_genesis.GenesisStep test_genesis.GenesisDraft` → ✗ exit 1 · Ran 21 tests in 3.0s (2 classes, 16 at a time; slowest: GenesisDraft 2s, GenesisStep 2s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree 8f48207adb31] (2026-10-30T11:43:05Z)
- `python3 plugin/tests/run.py test_genesis.GenesisStep test_genesis.GenesisDraft` → exit 0 · Ran 21 tests in 2.5s (2 classes, 16 at a time; slowest: GenesisStep 2s, GenesisDraft 2s) / OK [ran] [tree 8f48207adb31] (2026-10-30T11:43:05Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 71 tests in 3.9s (11 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 8f48207adb31] (2026-10-30T11:43:18Z)
- (audit edge) `self: read the diff; the spec stage only fires at gen 0 with no spec.md and uses spec()'s own mapping test (any §2 cap with a kind), so fm genesis spec never gets named where it would refuse; later-gen seed stages untouched (n>0 tests green)` → gen-0 with no mappable cap goes straight to seed (new test); empty §2 → seed as before; a rerun gives the same action (at() checks) [tree 8f48207adb31] (2026-10-30T11:43:18Z)
- (audit self) `self: read the diff; the spec stage only fires at gen 0 with no spec.md and uses spec()'s own mapping test (any §2 cap with a kind), so fm genesis spec never gets named where it would refuse; later-gen seed stages untouched (n>0 tests green)` → no findings [tree 8f48207adb31] (2026-10-30T11:43:18Z)
## Log
- 2026-10-30T05:24:52Z created
- 2026-10-30T11:40:56Z set tier=S, type=FIX
- 2026-10-30T11:40:57Z planned: it has criteria and steps
- 2026-10-30T11:40:57Z focused
- 2026-10-30T11:43:20Z done
- 2026-10-30T11:43:22Z committed 1a1d9d5d (5 files)
- 2026-10-30T11:47:00Z guard authorization added: publish
- 2026-10-30T11:49:20Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2099 [FEATURE M, done, 5 steps] fm genesis draft/spec — gen-0 from a line or nothing; per-project spec with a held-out… — lesson: cover() tag words counted as shared w…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2114 [FIX S, done, 2 steps] FIX S: genesis drift's cold read flags the seed's user-steer section (gen-0 doesn't name… — lesson: A seed that paraphrases gen-0 drifts: q…
- decision 2026-10-30: [outward] [cites: gen-0 MUST line 11] T-2076's push and any later push of Genesis work wait for a publish grant: they go in the final report
- similar finished tasks took 2–5 steps
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/genesis/SKILL.md
