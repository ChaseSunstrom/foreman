---
id: T-2941
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T08:51:17Z
updated: 2026-11-04T08:52:17Z
base: 3e1f4de06eebb87e51dd4a027ec14a0f966387f3
base_tree: c47f6b933a4b56d87a9bbbdeb110293aeb0bd0a0
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T08:51:19Z
plan0_scope: []
verified: strong
unproven: [docs]
---
# sampo.regen gets its old-name shim (plugin/lib/fmregen.py) and its MASTER bullet named fmregen, as every new sampo module has
## Raw request
> sampo.regen gets its old-name shim (plugin/lib/fmregen.py) and its MASTER bullet named fmregen, as every new sampo module has
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the rename alias test and the MASTER module list pass — verify with `python3 plugin/tests/run.py test_rename_aliases test_docs`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] shim and bullet
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_rename_aliases` → ✗ exit 1 · Ran 9 tests in 3.7s (1 classes, 16 at a time; slowest: RenameAliases 3s) / FAILED (1 classes: test_rename_aliases.RenameAliases) [ran] [tree c47f6b933a4b] [world 2f1906870a] (2026-11-04T08:51:29Z)
- (step 1) `python3 plugin/tests/run.py test_rename_aliases test_docs` → exit 0 · Ran 117 tests in 9.6s (27 classes, 16 at a time; slowest: Fences 9s, RenameAliases 4s, DocsProof 3s) / OK [ran] [tree 50be6491b62b] [world 2f1906870a] (2026-11-04T08:51:45Z)
- (ac 1) `python3 plugin/tests/run.py test_rename_aliases test_docs` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T08:51:45Z [ran] [tree 50be6491b62b] [world 2f1906870a] (2026-11-04T08:51:46Z)
- (audit edge) `test_rename_aliases red before, green after; test_docs green with the fmregen bullet` → the shim only aliases the import [tree 50be6491b62b] (2026-11-04T08:51:46Z)
- (audit intent) `test_rename_aliases red before, green after; test_docs green with the fmregen bullet` → the full check is green again after the regen merge [tree 50be6491b62b] (2026-11-04T08:51:46Z)
- (audit self) `test_rename_aliases red before, green after; test_docs green with the fmregen bullet` → no findings [tree 50be6491b62b] (2026-11-04T08:51:46Z)
## Log
- 2026-11-04T08:51:17Z created
- 2026-11-04T08:51:18Z focused
- 2026-11-04T08:51:19Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T08:52:15Z done
- 2026-11-04T08:52:17Z committed 9e9928ce (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2922 [FIX S, done, 1 steps] sampo.smallcards gets its old-name shim (plugin/lib/fmsmallcards.py) and its own MASTER bullet, as every sampo module has — lesson: a new s…
- T-2748 [CLEAN M, done, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.py s…
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- decision 2026-11-03: [cites: user steer: read SAMPO.md (RENAME, NOW)] [check: python3 plugin/tests/run.py test_rename_scan] Rename Foreman to Sampo per SAMPO.md: aliases…
## Regression test
none new: test_rename_aliases is the regression test; red on this tree before the shim (recorded), green after
## Why not caught
T-2918's lane ran test_docs but not test_rename_aliases
## Lessons
- the shim-and-bullet pair is now a pattern: a lane that adds a sampo module must add both (captured as a check)
## Plan gaps
- failed first: step 1 shim and bullet
## Files touched
- plugin/lib/fmregen.py
- MASTER.md
