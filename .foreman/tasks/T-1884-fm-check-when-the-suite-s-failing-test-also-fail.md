---
id: T-1884
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T00:17:06Z
updated: 2026-10-29T00:46:01Z
base: 2db04662ce6bd1f13402fe2d655df35a88a94fb0
base_tree: 590f48ba080d58d2d4d37361219f5a85ea8c9bed
plan0_at: 2026-10-29T00:35:47Z
plan0_scope: []
verified: strong
---
# Fm check: when the suite's failing test also fails its rerun, the ✗ summary shows only bla
## Raw request
> fm check: when the suite's failing test also fails its rerun, the ✗ summary shows only blank lines and 'Ran 1 test … FAILED' — name the failing test (FAIL: line) so nobody reruns 210 s of suite to find it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a failed gate names its failing tests and shows how the first one failed — verify with `python3 plugin/tests/run.py -k failed_gate_names test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: a gate whose failure is followed by summary noise
2. [x] the failing: line and the first test's excerpt replace the raw tail; green
## Resume here
<!-- auto -->
- 2026-10-29T00:36:36Z step 2/2: the failing: line and the first test's excerpt replace the raw tail; green
- git: foreman/build; 2 uncommitted: plugin/lib/fmcli.py, plugin/tests/test_cli.py
- touched since last checkpoint: plugin/tests/test_cli.py, plugin/lib/fmcli.py
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k failed_gate_names test_cli` → red as expected (exit 1) · Ran 122 tests in 41.5s (37 classes, 16 at a time; slowest: TaskLifecycle 41s, AuditPrep 17s, StateViews 17s) / FAILED (1 classes) [ran] [tree 4ed3f91b5488] (2026-10-29T00:36:31Z)
- (step 2) `python3 plugin/tests/run.py -k failed_gate_names test_cli` → exit 0 · Ran 124 tests in 42.2s (37 classes, 16 at a time; slowest: TaskLifecycle 42s, Checks 16s, AuditPrep 16s) / OK [ran] [tree 47215a9bfe7b] (2026-10-29T00:38:22Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                42.6    51.8     150  [0] / SessionEnd                  36.7    40.4     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui [ran] [tree 94f4bb31eb50] (2026-10-29T00:43:36Z)
- (ac 1) `python3 plugin/tests/run.py -k failed_gate_names test_cli` → exit 0 · Ran 124 tests in 23.7s (37 classes, 16 at a time; slowest: TaskLifecycle 23s, StateViews 8s, AuditPrep 8s) / OK [ran] [tree 94f4bb31eb50] (2026-10-29T00:44:15Z)
- (audit intent) `S task: lenses only; the new test drives a real failed gate and checks the failing: line and excerpt` → a failed gate now names the failing tests and shows the first one's failure instead of the summary tail [tree 94f4bb31eb50] (2026-10-29T00:44:15Z)
- (audit adversary) `S task: lenses only; the new test drives a real failed gate and checks the failing: line and excerpt` → output with no parsable test name falls back to the old last-10-lines tail, so nothing is hidden [tree 94f4bb31eb50] (2026-10-29T00:44:15Z)
- (audit edge) `S task: lenses only; the new test drives a real failed gate and checks the failing: line and excerpt` → more than 5 failures say +N more; the excerpt is capped at 600 chars and 10 lines [tree 94f4bb31eb50] (2026-10-29T00:44:15Z)
- (audit self) `S task: lenses only; the new test drives a real failed gate and checks the failing: line and excerpt` → no findings [tree 94f4bb31eb50] (2026-10-29T00:44:15Z)
- `python3 plugin/tests/run.py -k failed_gate_names test_cli` → ✗ exit 1 · Ran 122 tests in 24.1s (37 classes, 16 at a time; slowest: TaskLifecycle 23s, StateViews 8s, AuditPrep 8s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 94f4bb31eb50] (2026-10-29T00:45:34Z)
- `python3 plugin/tests/run.py -k failed_gate_names test_cli` → exit 0 · Ran 124 tests in 23.4s (37 classes, 16 at a time; slowest: TaskLifecycle 23s, StateViews 8s, AuditPrep 8s) / OK [ran] [tree 94f4bb31eb50] (2026-10-29T00:45:34Z)
- (audit intent) `S task: lenses only; the new test drives a real failed gate and checks the failing: line and excerpt` → a failed gate now names the failing tests and shows the first one's failure instead of the summary tail [tree 94f4bb31eb50] (2026-10-29T00:45:35Z)
- (audit adversary) `S task: lenses only; the new test drives a real failed gate and checks the failing: line and excerpt` → output with no parsable test name falls back to the old last-10-lines tail, so nothing is hidden [tree 94f4bb31eb50] (2026-10-29T00:45:35Z)
- (audit edge) `S task: lenses only; the new test drives a real failed gate and checks the failing: line and excerpt` → more than 5 failures say +N more; the excerpt is capped at 600 chars and 10 lines [tree 94f4bb31eb50] (2026-10-29T00:45:35Z)
- (audit self) `S task: lenses only; the new test drives a real failed gate and checks the failing: line and excerpt` → no findings [tree 94f4bb31eb50] (2026-10-29T00:45:35Z)
## Log
- 2026-10-29T00:17:06Z created
- 2026-10-29T00:23:51Z set type=FIX, tier=S
- 2026-10-29T00:35:47Z focused
- 2026-10-29T00:46:00Z done
- 2026-10-29T00:46:01Z committed 349e83bc (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1678 [FIX S, done, 1 steps] A slow gate's one failure in a load spike opens an urgent baseline task: rerun just its failing tests first
- T-1377 [FEATURE M, done, 3 steps] A false-done benchmark: impossible tasks where the only right outcome is saying it can't b — lesson: A benchmark of honesty needs an ob…
- T-1805 [FEATURE S, done, 2 steps] Before a push to main or a release, run the suite once under the oldest supported Python w — lesson: A flag that re-runs a command unde…
- decision 2026-10-23: A broken code.toml: fm code config falls back to defaults and names the line; runs keep refusing it
- similar finished tasks took 1–3 steps
## Lessons
- A failure summary's tail is the runner's footer; name the failing test and show its own excerpt
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- CHANGELOG.md
