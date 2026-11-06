---
id: T-1894
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_cli.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-29T02:18:37Z
updated: 2026-10-29T02:28:05Z
base: c36e8b06532c928dd94fdaf52ea67e1ec1ea4b7a
base_tree: 9c94a54c1f6a903883630b03285394d93a4f364d
plan0_at: 2026-10-29T02:18:38Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_cli.py, CHANGELOG.md]
verified: strong
---
# fm task set --section reads criteria and steps in the forms fm task new takes
## Raw request
> fm task set --section reads criteria and steps in the forms fm task new takes
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a criterion written 'X :: cmd' and a step '1. go' given with --section are parsed (verify command, unchecked step) — verify with `python3 plugin/tests/run.py test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: --section criteria and steps in task new forms
2. [x] Normalize them in task_set; green
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli.CaptureAndIntake` → red as expected (exit 1) · Ran 15 tests in 5.1s (1 classes, 16 at a time; slowest: CaptureAndIntake 5s) / FAILED (1 classes) [ran] [tree e7eefbf37a27] (2026-10-29T02:19:06Z)
- (step 2) `python3 plugin/tests/run.py test_cli.CaptureAndIntake` → exit 0 · Ran 15 tests in 5.2s (1 classes, 16 at a time; slowest: CaptureAndIntake 5s) / OK [ran] [tree c38dfaac880b] (2026-10-29T02:19:12Z)
- (step 3) `grep -c T-1894 CHANGELOG.md` → exit 0 · 1 [ran] [tree c38dfaac880b] (2026-10-29T02:19:12Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.4    41.9     150  [0] / SessionEnd                  35.3    37.3     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui [ran] [tree c38dfaac880b] (2026-10-29T02:23:17Z)
- (step 2) `python3 plugin/tests/run.py test_cli.CaptureAndIntake` → exit 0 · Ran 15 tests in 5.3s (1 classes, 16 at a time; slowest: CaptureAndIntake 5s) / OK [ran] [tree 6b9ebb9acb14] (2026-10-29T02:23:27Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.0    42.5     150  [0] / SessionEnd                  34.8    35.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui [ran] [tree 6b9ebb9acb14] (2026-10-29T02:27:28Z)
- (ac 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 126 tests in 22.7s (37 classes, 16 at a time; slowest: TaskLifecycle 22s, StateViews 8s, AuditPrep 8s) / OK [ran] [tree 6b9ebb9acb14] (2026-10-29T02:28:01Z)
- (audit intent) `self-review of the diff plus the lenses below; gates exit 0; the four real briefs (T-1875, T-1876, T-1881, T-1885) re-saved and now parse` → '- [ ] X :: cmd' and '1. step' given with --section are stored as '— verify with `cmd`' and '1. [ ] step', so fm focus accepts the task [tree 6b9ebb9acb14] (2026-10-29T02:28:01Z)
- (audit adversary) `self-review of the diff plus the lenses below; gates exit 0; the four real briefs (T-1875, T-1876, T-1881, T-1885) re-saved and now parse` → a criterion already carrying '— verify with' whose command holds ' :: ' is left as it is (tested); ' :: ' splits at the last one, as fm task new --ac does [tree 6b9ebb9acb14] (2026-10-29T02:28:01Z)
- (audit edge) `self-review of the diff plus the lenses below; gates exit 0; the four real briefs (T-1875, T-1876, T-1881, T-1885) re-saved and now parse` → checked steps and criteria keep their [x]; sections other than criteria and steps are untouched; a pytest node id (a.py::b) has no spaces so it never splits [tree 6b9ebb9acb14] (2026-10-29T02:28:01Z)
- (audit self) `self-review of the diff plus the lenses below; gates exit 0; the four real briefs (T-1875, T-1876, T-1881, T-1885) re-saved and now parse` → no findings [tree 6b9ebb9acb14] (2026-10-29T02:28:01Z)
## Log
- 2026-10-29T02:18:37Z created
- 2026-10-29T02:18:37Z focused
- 2026-10-29T02:28:03Z done
- 2026-10-29T02:28:05Z committed df225336 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1626 [FEATURE M, done, 5 steps] fm code's motion clock reads the project's Motion Score; fm motion compile --to lab: a page to play, scrub and edit each motion — lesso…
- T-1846 [FEATURE M, done, 2 steps] Fm scene: a fragment-shader subset fmraster can run per pixel (uniforms, a few built-ins), — lesson: a custom error that subclasses Val…
- T-1400 [FEATURE M, done, 1 steps] A standing mandate: a sweeping request becomes one record (its text, its clauses from fm c — lesson: parse_ts returns a datetime, not e…
- decision 2026-10-16: T-0275: a script over the guard's parse budget stays allowed after the literal scan, not refused
- similar past tasks were M: consider --tier M
- similar finished tasks took 1–5 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Lessons
- A writer that takes free text for a parsed section should accept the same shorthand the creating verb takes
## Files touched
- plugin/tests/test_cli.py
- CHANGELOG.md
- plugin/lib/fmcli.py
