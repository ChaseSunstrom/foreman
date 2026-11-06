---
id: T-2119
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T07:52:52Z
updated: 2026-10-30T08:06:36Z
base: 9b01b48ca1a2f97af3c214ebcf9634c2f18727fe
base_tree: b45b93ae6b4a14ac6e2418818e64b41f98dba62d
plan0_at: 2026-10-30T07:55:43Z
plan0_scope: []
verified: strong
---
# FIX S: fm genesis step reads a seed with no Missions table as a dry generation and jumps…
## Raw request
> FIX S: fm genesis step reads a seed with no Missions table as a dry generation and jumps to select, so G-tower's arm built nothing (0/3 fixed vs plain 3/3); require rows or an explicit 'no Missions this generation'
## Interpretation
G-tower's arm wrote a seed whose Missions weren't a table; step read it as a dry generation and named select, so nothing was built (0/3 fixed vs plain 3/3)
## Assumptions (confidence)
## Acceptance criteria
- [x] a seed with no Missions rows and no 'no Missions this generation' line is fatal, not a dry generation — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
Dry only when the seed says 'no Missions this generation' (the line fm genesis seed already writes); otherwise fatal with the row format.
## Risks and rollback
## Execution prompt
## Steps
1. [x] step(): no rows → fatal unless the seed says 'no Missions this generation'; tests for a bullet list and a header-only table
## Resume here
<!-- auto -->
- 2026-10-30T08:02:04Z steps 1/1 done
- git: foreman/build; 4 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py
- touched since last checkpoint: plugin/tests/test_genesis.py, CHANGELOG.md, MASTER.md
- failures met: indexerror: list index out of range
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_genesis 2>&1 | grep -E "^(FAIL|ERROR|AssertionError)|Error:" | head -20` → ✗ exit 1 · FAILED (failures=1) / FAILED (3 classes) [ran] [tree 9e19e43e41ba] (2026-10-30T07:56:25Z)
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 66 tests in 3.9s (11 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 8ecd5f784d5d] (2026-10-30T07:58:39Z)
- `python3 plugin/tests/run.py test_genesis.GenesisStep` → ✗ exit 1 · Ran 9 tests in 3.1s (1 classes, 16 at a time; slowest: GenesisStep 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 8ecd5f784d5d] (2026-10-30T08:04:00Z)
- `python3 plugin/tests/run.py test_genesis.GenesisStep` → exit 0 · Ran 9 tests in 2.3s (1 classes, 16 at a time; slowest: GenesisStep 2s) / OK [ran] [tree 8ecd5f784d5d] (2026-10-30T08:04:00Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 66 tests in 3.9s (11 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 3s, GenesisCheck 3s) / OK [ran] [tree 8ecd5f784d5d] (2026-10-30T08:04:08Z)
- (audit edge) `self-review: the only path that read as dry was rows==[]; now it needs the explicit phrase; 5 fixture seeds updated to say it; gates EXIT 0` → header-only table and bullet-list seeds both fatal; the seed verb's own dry text matches the phrase [tree 8ecd5f784d5d] (2026-10-30T08:04:08Z)
- (audit self) `self-review: the only path that read as dry was rows==[]; now it needs the explicit phrase; 5 fixture seeds updated to say it; gates EXIT 0` → no findings [tree 8ecd5f784d5d] (2026-10-30T08:04:08Z)
## Log
- 2026-10-30T07:52:52Z created
- 2026-10-30T07:55:34Z set type=FIX, tier=S
- 2026-10-30T07:55:42Z planned: it has criteria and steps
- 2026-10-30T07:55:42Z focused
- 2026-10-30T07:55:48Z focused
- 2026-10-30T08:04:10Z done
- 2026-10-30T08:04:12Z committed 2f8236c6 (4 files)
- 2026-10-30T08:04:18Z guard authorization added: publish
- 2026-10-30T08:06:36Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- decision 2026-10-30: T-2112: #13's draft kinds live in fmgenesis (fm genesis exam) reusing fmexam.draw/render and cover; G-tower is a 'genesis' session arm on fmexam's d…
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
