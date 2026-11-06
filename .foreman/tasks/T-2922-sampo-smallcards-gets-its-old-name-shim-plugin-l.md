---
id: T-2922
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T07:42:25Z
updated: 2026-11-04T07:43:18Z
base: 833236bd1ba7d023f181c82fba608d77824ebc88
base_tree: 862dd64ebfeca44ce755d7f8042d8be8a632a279
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T07:42:26Z
plan0_scope: []
verified: strong
unproven: [docs]
---
# sampo.smallcards gets its old-name shim (plugin/lib/fmsmallcards.py) and its own MASTER bullet, as every sampo module has
## Raw request
> sampo.smallcards gets its old-name shim (plugin/lib/fmsmallcards.py) and its own MASTER bullet, as every sampo module has
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
- (step 1) `python3 plugin/tests/run.py test_rename_aliases test_docs` → exit 0 · Ran 117 tests in 9.3s (27 classes, 16 at a time; slowest: Fences 9s, RenameAliases 4s, DocsProof 3s) / OK [ran] [tree d23240f475a2] [world 2f1906870a] (2026-11-04T07:42:45Z)
- (ac 1) `python3 plugin/tests/run.py test_rename_aliases test_docs` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T07:42:45Z [ran] [tree d23240f475a2] [world 2f1906870a] (2026-11-04T07:42:51Z)
- (audit edge) `test_rename_aliases red before, green after; test_docs green with the module's own bullet` → the shim only aliases the import; the bullet moved out of fmplaybooks, so MASTER names the module once [tree d23240f475a2] (2026-11-04T07:42:51Z)
- (audit intent) `test_rename_aliases red before, green after; test_docs green with the module's own bullet` → the baseline is green again after the cards merge [tree d23240f475a2] (2026-11-04T07:42:51Z)
- (audit self) `test_rename_aliases red before, green after; test_docs green with the module's own bullet` → no findings [tree d23240f475a2] (2026-11-04T07:42:51Z)
## Log
- 2026-11-04T07:42:25Z created
- 2026-11-04T07:42:25Z focused
- 2026-11-04T07:42:26Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T07:43:16Z done
- 2026-11-04T07:43:18Z committed cac58adc (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2748 [CLEAN M, done, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.py s…
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- research T-2748-review: Verdict:** changes needed. This is a narrow MEDIUM fix in the hook's fallback. The shim and rename work looks sound. I read the code but did not …
- decision 2026-11-03: [cites: user steer: read SAMPO.md (RENAME, NOW)] [check: python3 plugin/tests/run.py test_rename_scan] Rename Foreman to Sampo per SAMPO.md: aliases…
## Regression test
none new: test_rename_aliases is the regression test; it was red on this tree before the shim (seen in this session's run) and is green now
## Why not caught
T-2909's close ran its affected tests, which didn't include test_rename_aliases
## Lessons
- a new sampo module needs the old-name shim and its own MASTER bullet in the same commit; the docs test and the alias test check opposite sides of the same pair
## Files touched
- plugin/lib/fmsmallcards.py
- MASTER.md
