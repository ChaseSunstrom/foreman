---
id: T-2782
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/doctor.py, plugin/tests/test_planning.py]
depends_on: []
source: discovered
created: 2026-11-03T05:05:27Z
updated: 2026-11-03T18:39:07Z
builder_model: sonnet
base: f99855d80b7312bff6b2af9edc76721581dad328
base_tree: 7dbd5e5442b3f9a603476cf4321e04816e9a9dc6
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-03T05:21:02Z
plan0_scope: [plugin/lib/sampo/doctor.py, plugin/tests/test_planning.py]
lane_stop: merged 2026-11-03T05:25:11Z
verified: strong
unproven: [docs]
---
# fm doctor's module-map check scans the sampo package: missing_modules lists plugin/lib/sampo/*.py (and fmguard.py) that MASTER.md never names, not the fm*.py shims
## Raw request
> FIX: doctor.missing_modules (doctor.py:1466) scans plugin/lib/fm*.py, now shims after T-2748, so a new plugin/lib/sampo/*.py module MASTER.md never names passes the self-docs check; scan lib/sampo/*.py (fmguard.py too) and update test_planning's fixture (T-2748 review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a new plugin/lib/sampo/foo.py that MASTER.md never names is listed, a shim fmX.py is not, and fmguard is still checked — verify with `python3 plugin/tests/run.py test_planning test_doctor`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: test_planning's fixture writes lib/sampo/new.py and a shim, expects ['new']; then scan lib/sampo/*.py plus fmguard.py; run test_planning and test_doctor
## Resume here
## Docs impact
MASTER.md: one line maps the moved modules to their sampo names
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_planning test_doctor 2>&1 | tail -5` → ✗ exit 1 · Ran 129 tests in 14.1s (50 classes, 16 at a time; slowest: CalibrationLedger 14s, ViewsRepair 7s, LockProbe 6s) / FAILED (2 classes: test_doctor.Checks, test_planning.SelfDocsModules) [ran] [tree 184bfc0762af] [world 2f1906870a] (2026-11-03T05:21:41Z)
- (ac 1) `python3 plugin/tests/run.py test_planning test_doctor 2>&1 | grep -B3 -A15 "^FAIL:" | head -60` → ✗ exit 1 · + [] / ---------------------------------------------------------------------- [ran] [tree 184bfc0762af] [world 2f1906870a] (2026-11-03T05:21:58Z)
- (ac 1) `python3 plugin/tests/run.py test_planning test_doctor 2>&1 | tail -3` → exit 0 · Ran 129 tests in 7.2s (50 classes, 16 at a time; slowest: CalibrationLedger 7s, ViewsRepair 4s, LockProbe 3s) / OK [ran] [tree e262c340ef82] [world 2f1906870a] (2026-11-03T05:22:19Z)
- (step 1) `python3 plugin/tests/run.py test_planning test_doctor 2>&1 | tail -3` → exit 0 · Ran 129 tests in 7.2s (50 classes, 16 at a time; slowest: CalibrationLedger 7s, ViewsRepair 4s, LockProbe 3s) / OK [ran] [tree e262c340ef82] [world 2f1906870a] (2026-11-03T05:22:19Z)
- (step 1) `python3 plugin/tests/run.py test_planning test_doctor` → exit 0 · Ran 129 tests in 7.4s (50 classes, 16 at a time; slowest: CalibrationLedger 7s, ViewsRepair 4s, LockProbe 3s) / OK [ran] [tree e262c340ef82] [world 2f1906870a] (2026-11-03T05:22:29Z)
- `python3 plugin/tests/run.py test_planning test_doctor` → ✗ exit 1 · Ran 129 tests in 9.0s (50 classes, 16 at a time; slowest: CalibrationLedger 8s, ViewsRepair 4s, LockProbe 4s) / FAILED (1 classes: test_planning.SelfDocsModules) (start tree + this task's tests) [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:19:53Z)
- `python3 plugin/tests/run.py test_planning test_doctor` → exit 0 · Ran 129 tests in 9.1s (50 classes, 16 at a time; slowest: CalibrationLedger 9s, ViewsRepair 4s, LockProbe 3s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:19:53Z)
- (ac 1) `python3 plugin/tests/run.py test_planning test_doctor` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T17:19:53Z [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:19:54Z)
- (audit intent) `self: read the diff; the module-map check scans the sampo package` → a new sampo module MASTER.md never names is reported; shims are skipped [tree 07445d19b39c] (2026-11-03T17:19:54Z)
- (audit edge) `self: read the diff; the module-map check scans the sampo package` → MASTER.md may name a module as fmX, sampo/X or sampo.X; fmguard is checked on its own [tree 07445d19b39c] (2026-11-03T17:19:54Z)
- (audit adversary) `self: read the diff; the module-map check scans the sampo package` → reads file names under plugin/lib only [tree 07445d19b39c] (2026-11-03T17:19:54Z)
- (audit self) `self: read the diff; the module-map check scans the sampo package` → no findings [tree 07445d19b39c] (2026-11-03T17:19:54Z)
- `python3 plugin/tests/run.py test_planning test_doctor` → ✗ exit 1 · Ran 129 tests in 8.4s (50 classes, 16 at a time; slowest: CalibrationLedger 7s, ViewsRepair 4s, LockProbe 3s) / FAILED (1 classes: test_planning.SelfDocsModules) (start tree + this task's tests) [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:20:34Z)
- `python3 plugin/tests/run.py test_planning test_doctor` → exit 0 · Ran 129 tests in 7.3s (50 classes, 16 at a time; slowest: CalibrationLedger 7s, ViewsRepair 4s, LockProbe 3s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:20:34Z)
- `python3 plugin/tests/run.py test_planning test_doctor` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T17:20:34Z [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:20:35Z)
- (audit intent) `self: read the diff; the module-map check scans the sampo package` → a new sampo module MASTER.md never names is reported; shims are skipped [tree 07445d19b39c] (2026-11-03T17:20:35Z)
- (audit edge) `self: read the diff; the module-map check scans the sampo package` → MASTER.md may name a module as fmX, sampo/X or sampo.X; fmguard is checked on its own [tree 07445d19b39c] (2026-11-03T17:20:35Z)
- (audit adversary) `self: read the diff; the module-map check scans the sampo package` → reads file names under plugin/lib only [tree 07445d19b39c] (2026-11-03T17:20:35Z)
- (audit self) `self: read the diff; the module-map check scans the sampo package` → no findings [tree 07445d19b39c] (2026-11-03T17:20:35Z)
- `python3 plugin/tests/run.py test_planning test_doctor` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T17:20:35Z [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T18:38:40Z)
- (audit intent) `self: read the diff; the module-map check scans the sampo package` → a new sampo module MASTER.md never names is reported; shims are skipped [tree 07445d19b39c] (2026-11-03T18:38:40Z)
- (audit edge) `self: read the diff; the module-map check scans the sampo package` → MASTER.md may name a module as fmX, sampo/X or sampo.X; fmguard is checked on its own [tree 07445d19b39c] (2026-11-03T18:38:40Z)
- (audit adversary) `self: read the diff; the module-map check scans the sampo package` → reads file names under plugin/lib only [tree 07445d19b39c] (2026-11-03T18:38:40Z)
- (audit self) `self: read the diff; the module-map check scans the sampo package` → no findings [tree 07445d19b39c] (2026-11-03T18:38:40Z)
## Log
- 2026-11-03T05:05:27Z created
- 2026-11-03T05:05:44Z planned from capture
- 2026-11-03T05:05:44Z set approved=True
- 2026-11-03T05:20:52Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2782.builder.md
- 2026-11-03T05:21:00Z focused
- 2026-11-03T05:21:02Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-03T05:25:11Z merged worktree-agent-a715598103f61d03d (3 file(s))
- 2026-11-03T05:25:26Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a715598103f61d03d
- 2026-11-03T15:07:41Z focused
- 2026-11-03T15:07:42Z paused: focus moved to T-2784
- 2026-11-03T17:05:11Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T17:05:11Z focused
- 2026-11-03T17:05:12Z paused: focus moved to T-2784
- 2026-11-03T17:19:33Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T17:19:33Z focused
- 2026-11-03T17:20:56Z paused: focus moved to T-2784
- 2026-11-03T17:21:01Z scope: MASTER.md's module map names the sampo modules; the doctor's module-map check reads it, so the doc and check move together
- 2026-11-03T18:38:37Z focused
- 2026-11-03T18:39:07Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2748 [CLEAN M, planned, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.p…
- research T-2748-review: Verdict:** changes needed. This is a narrow MEDIUM fix in the hook's fallback. The shim and rename work looks sound. I read the code but did not …
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- decision 2026-11-03: [cites: user steer: read SAMPO.md (RENAME, NOW)] [check: python3 plugin/tests/run.py test_rename_scan] Rename Foreman to Sampo per SAMPO.md: aliases…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_doctor.py
## Preflight
Changed in scope since this was planned (2026-11-03): plugin/lib/sampo/doctor.py, plugin/tests/test_planning.py; re-ground the plan against them before editing
## Lessons
- Point a check at where the code lives now
## Files touched
- plugin/tests/test_planning.py
- plugin/lib/sampo/doctor.py
- MASTER.md
