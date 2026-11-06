---
id: T-3405
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmtrain.py, CHANGELOG.md, .sampo/**, .fm-scratch/**]
depends_on: []
source: user
created: 2026-11-06T08:07:24Z
updated: 2026-11-06T08:08:16Z
base: 15ffb1b36a03f586edabf5258b282da64bd2a6de
base_tree: ef233f48fea6436d64da9d3129129ee5df77eca9
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T08:07:25Z
plan0_scope: []
verified: ok
unproven: [meaning]
---
# sampo.train gets its fmtrain.py import shim (test_rename_aliases red after the T-3380 merge)
## Raw request
> sampo.train gets its fmtrain.py import shim (test_rename_aliases red after the T-3380 merge)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_rename_aliases passes — verify with `python3 plugin/tests/run.py test_rename_aliases`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] add plugin/lib/fmtrain.py in the shim template
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_rename_aliases` → exit 0 · Ran 9 tests in 3.6s (1 jobs, 16 at a time; slowest: RenameAliases 3s) / OK [ran] [tree e4931ae37655] [world 2f1906870a] (2026-11-06T08:07:38Z)
- (ac 1) `python3 plugin/tests/run.py test_rename_aliases` → exit 0 · Ran 9 tests in 3.3s (1 jobs, 16 at a time; slowest: RenameAliases 3s) / OK [ran] [tree e4931ae37655] [world 2f1906870a] (2026-11-06T08:07:42Z)
- (audit self) `a four-line shim in the shared template; no behaviour change` → no findings [tree c05307db2871] (2026-11-06T08:07:43Z)
- (ac 1) `python3 plugin/tests/run.py test_rename_aliases` → exit 0 · Ran 9 tests in 3.8s (1 jobs, 16 at a time; slowest: RenameAliases 3s) / OK [ran] [tree c05307db2871] [world 2f1906870a] (2026-11-06T08:07:48Z)
- (audit self) `self: template shim` → no findings [tree c05307db2871] (2026-11-06T08:07:48Z)
## Log
- 2026-11-06T08:07:24Z created
- 2026-11-06T08:07:25Z focused
- 2026-11-06T08:07:25Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T08:07:26Z set scope=['plugin/lib/fmtrain.py', 'CHANGELOG.md', '.sampo/**', '.fm-scratch/**']
- 2026-11-06T08:08:12Z done
- 2026-11-06T08:08:16Z committed 9a9f67858 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2943 [FIX S, done, 1 steps] The fmmint and fmtraces shims match the exact old-path shim, so the rename alias test passes — lesson: A new sampo module's old-path shim m…
- T-2748 [CLEAN M, done, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.py s…
- T-3400 [FIX S, done, 1 steps] fmrepro shim matches the shim template exactly (test_rename_aliases red after the T-3279 merge; the post-merge suite threatens its auto-rev…
- decision 2026-11-03: [cites: user steer: read SAMPO.md (RENAME, NOW)] [check: python3 plugin/tests/run.py test_rename_scan] Rename Foreman to Sampo per SAMPO.md: aliases…
## Regression test
the existing test_rename_aliases.RenameAliases is the regression test: red on main at 15ffb1b36 ('sampo.train' has no shim), green after
## Lessons
- a new sampo module needs its fm shim; test_rename_aliases says so
## Files touched
- plugin/lib/fmtrain.py
- CHANGELOG.md
