---
id: T-2084
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-30T02:55:53Z
updated: 2026-10-30T13:27:22Z
base: 6270e090c364ddb211c11e92d7ed19e41ada4028
base_tree: d0c4073c01b01ac7e3531ee0183f9904caff3d79
plan0_at: 2026-10-30T13:20:04Z
plan0_scope: [plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, CHANGELOG.md]
verified: strong
---
# fm genesis export: stale .md files from an earlier export stay in DIR (removal skipped:…
## Raw request
> fm genesis export: stale .md files from an earlier export stay in DIR (removal skipped: deleting in a user-given dir); export() ~65 lines with inline import json
## Interpretation
fm genesis export writes each tower doc beside genesis.json; a doc gone from the tower stays in DIR forever. Remove only files the previous export listed in its own genesis.json docs, that match the tower's shape, are regular files (no symlinks) and are missing from this export. Anything else in DIR is the user's and stays.
## Assumptions (confidence)
## Acceptance criteria
- [x] Re-export drops a doc the tower lost, keeps a user's own file in DIR, and ignores a tampered key outside the tower shape — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
1) wipe DIR's .md files: deletes user files. 2) a separate manifest file: one more file. 3) the previous genesis.json's docs keys are already the manifest: chosen, zero new files; each key re-checked against SHAPE so a tampered json can't reach outside DIR.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: stale doc removed, user file and tampered key left alone
2. [x] export() removes stale docs listed by the previous genesis.json
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_genesis.GenesisExport.test_a_re_export_drops_docs_the_tower_lost_and_nothing_else` → ✗ exit 1 · Ran 1 tests in 1.5s (1 classes, 16 at a time; slowest: GenesisExport 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree a4732a0a6ecd] (2026-10-30T13:20:39Z)
- `python3 plugin/tests/run.py test_genesis.GenesisExport.test_a_re_export_drops_docs_the_tower_lost_and_nothing_else` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: GenesisExport 0s) / OK [ran] [tree a4732a0a6ecd] (2026-10-30T13:20:39Z)
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 77 tests in 4.2s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 7037d60a3905] (2026-10-30T13:20:53Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 77 tests in 4.3s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 7037d60a3905] (2026-10-30T13:20:58Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 77 tests in 4.3s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 7037d60a3905] (2026-10-30T13:21:02Z)
- (audit self) `read the diff: previous genesis.json docs keys minus this export's, each re-checked` → removes only regular files; a corrupt or non-dict genesis.json removes nothing; the inline import json stays (not worth a refactor) [tree 7037d60a3905] (2026-10-30T13:21:09Z)
- (audit adversary) `a tampered genesis.json in DIR: ../ keys, absolute keys, a symlinked file, a symlinked gen-N dir` → SHAPE.fullmatch rejects ../ and absolute keys; realpath must equal the normalized DIR/rel, so a symlinked file or dir is left alone; covered by the new test (../keep.md, symlinked critique) [tree 7037d60a3905] (2026-10-30T13:21:09Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 77 tests in 4.3s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 7037d60a3905] (2026-10-30T13:21:19Z)
- (audit edge) `self + adversary audits recorded; red→green on the new GenesisExport test; test_genesis green` → a corrupt, list or docs-less genesis.json removes nothing [tree 7037d60a3905] (2026-10-30T13:21:19Z)
- (audit adversary) `self + adversary audits recorded; red→green on the new GenesisExport test; test_genesis green` → ../ keys, a symlinked file and a symlinked dir are left alone [tree 7037d60a3905] (2026-10-30T13:21:19Z)
- (audit self) `self + adversary audits recorded; red→green on the new GenesisExport test; test_genesis green` → no findings [tree 7037d60a3905] (2026-10-30T13:21:19Z)
## Log
- 2026-10-30T02:55:53Z created
- 2026-10-30T13:19:21Z set type=FIX, tier=S
- 2026-10-30T13:19:22Z set scope=['plugin/lib/fmgenesis.py', 'plugin/tests/test_genesis.py', 'CHANGELOG.md']
- 2026-10-30T13:19:22Z planned: it has criteria and steps
- 2026-10-30T13:20:03Z focused
- 2026-10-30T13:21:09Z scope: raw request also named export()'s length and its inline import json; left as is, a refactor buys nothing here
- 2026-10-30T13:21:21Z done
- 2026-10-30T13:21:23Z committed 524ab58f (3 files)
- 2026-10-30T13:21:32Z guard authorization added: publish
- 2026-10-30T13:27:22Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2113 [FEATURE M, done, 3 steps] fm genesis charter seal + privilege diff (mission-genesis brief 8, tier 3): init seals… — lesson: A seal file beside the file it seals …
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- research T-2095-review: Verdict:** approve with nits. It meets the criteria as written. One resumability gap and one silent-skip case are worth fixing. I did not run `pl…
- decision 2026-10-30: T-2105: Genesis offers itself through fm scout (probe_genesis, once ever, ≥10 done tasks, no tower, nothing queued) as a confirm task, not a new fm …
- likely tests for the scope: plugin/tests/test_genesis.py
## Preflight
Changed in scope since this was planned (2026-10-30): CHANGELOG.md, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py; re-ground the plan against them before editing
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
