---
id: T-2943
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmmint.py, plugin/lib/fmtraces.py, CHANGELOG.md]
depends_on: [T-2779]
source: discovered
created: 2026-11-04T08:52:47Z
updated: 2026-11-05T02:44:13Z
group: rename aliases and rename-scan test failures
base: 31cc0cc9258f3477fbb535b4851f0cca78b15a64
base_tree: 246d3ae54904516d706b2c2d91c9074cc9d151ef
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T02:42:58Z
plan0_scope: [plugin/lib/fmmint.py, plugin/lib/fmtraces.py, CHANGELOG.md]
verified: strong
unproven: [meaning]
---
# The fmmint and fmtraces shims match the exact old-path shim, so the rename alias test passes
## Raw request
> Re-verify failed for T-2779 (fb982e): python3 plugin/tests/run.py test_rename_scan… (now ✗ exit 1 · Ran 19 tests in 6.3s (2 classes, 16 at a time; slowest: RenameAliases 6s, RenameScan 6s) / FAILED (1 classes: test_rename_aliases.RenameAliases); queued by 3d1776cae… FEATURE: fm lane merge names changed text still found elsewhere, readers first, so a producer/reader split reaches the …)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] plugin/lib/fmmint.py and fmtraces.py are exactly the T-2742 shim (the standard docstring naming sampo.mint and sampo.traces), and every old import path is the same module object — verify with `python3 plugin/tests/run.py test_rename_scan test_rename_aliases`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] rewrite both shims to the standard text (the test is already red)
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_rename_scan test_rename_aliases` → exit 0 · Ran 19 tests in 7.3s (2 classes, 16 at a time; slowest: RenameAliases 7s, RenameScan 6s) / OK [ran] [tree 6a413ae7f6aa] [world 2f1906870a] (2026-11-05T02:43:23Z)
- (ac 1) `python3 plugin/tests/run.py test_rename_scan test_rename_aliases` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T02:43:23Z [ran] [tree 6a413ae7f6aa] [world 2f1906870a] (2026-11-05T02:43:31Z)
- (audit intent) `self: both shims are now the exact T-2742 text, so shims() reads them and the old import paths are the same module objects` → test_rename_aliases is green; the re-verify that filed this would pass [tree 6a413ae7f6aa] (2026-11-05T02:43:31Z)
- (audit edge) `self: both shims are now the exact T-2742 text, so shims() reads them and the old import paths are the same module objects` → no other fm*.py deviates (the test checks every one); the new sampo modules mint and traces keep their old-path shims [tree 6a413ae7f6aa] (2026-11-05T02:43:31Z)
- (audit self) `self: both shims are now the exact T-2742 text, so shims() reads them and the old import paths are the same module objects` → no findings [tree 6a413ae7f6aa] (2026-11-05T02:43:31Z)
## Log
- 2026-11-04T08:52:47Z created
- 2026-11-05T02:38:47Z planned from capture
- 2026-11-05T02:38:48Z set approved=True
- 2026-11-05T02:38:48Z set scope=['plugin/lib/fmmint.py', 'plugin/lib/fmtraces.py', 'CHANGELOG.md']
- 2026-11-05T02:42:56Z focused
- 2026-11-05T02:42:58Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T02:44:09Z done
- 2026-11-05T02:44:13Z committed 01efe2f4 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2944 [FIX S, blocked, 2 steps] A re-verify that times out is reported as inconclusive, not filed as a failed check
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2861 [FEATURE M, done, 3 steps] A rename-twin check for respelled literals: for each string fragment a branch respelled… — lesson: rank by either side: the changed sit…
- decision 2026-11-03: [cites: user steer: read SAMPO.md (RENAME, NOW)] [check: python3 plugin/tests/run.py test_rename_scan] Rename Foreman to Sampo per SAMPO.md: aliases…
- similar past tasks were L: consider --tier L
- similar finished tasks took 3–9 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_mint.py, plugin/tests/test_traces.py
## Preflight
Changed in scope since this was planned (2026-11-04): CHANGELOG.md, plugin/lib/fmmint.py, plugin/lib/fmtraces.py; re-ground the plan against them before editing
## Regression test
none new: test_rename_aliases already pinned it and was red before the edit (2026-11-05, 'Lists differ: [fmmint, fmtraces] != []' and the same-module subtests erroring); the fix only rewrites the two shims, so the existing test is the regression test
## Lessons
- A new sampo module's old-path shim must be the exact template (copy fmagents.py), not a paraphrase: the alias test reads shims by regex, and a T-number added to the docstring breaks it.
## Files touched
- plugin/lib/fmmint.py
- plugin/lib/fmtraces.py
