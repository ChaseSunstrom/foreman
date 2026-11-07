---
id: T-2969
type: FIX
tier: M
status: planned
priority: normal
scope: []
depends_on: [T-3002]
source: discovered
created: 2026-11-04T13:53:41Z
updated: 2026-11-06T09:09:00Z
trigger: ci-red
trigger_key: 09aeed4b8bce88fb
rival_at: 2026-11-06T08:56:02Z
rival_split: true
---
# CI on main is green again: test_moons_scale stops needing a live embedder (T-3002) and test_ui_replay's timeout kills claude's own child on Linux
## Raw request
> FIX: CI on main is red at d1901b5 (tests)
> CONTEXT: found by the session-start sweep (T-1810): https://github.com/ChaseSunstrom/sampo/commit/d1901b57f2bd762970a78c245b9cced032e55795
> CI-red: d1901b57f2bd762970a78c245b9cced032e55795
## Interpretation
Reading 1 (chosen): CI on main has been red since d1901b5 (2026-11-04 13:22, two pushes): on ubuntu test_ui_replay.Run ('claude's own child outlived the timeout') and test_moons_scale.Families; on macOS test_moons_scale.Families and .Promote ('- Family: F-000003 (1 variant)' not found). The moons classes fail where no Ollama embedder answers (CI), which T-3002 fixes with a fake embedder; the ui_replay one is a child process that survives the replay's timeout kill on Linux. Reading 2: mark the classes skip on CI; rejected, CI would stop testing them.
## Assumptions (confidence)
## Acceptance criteria
- [ ] test_moons_scale passes with FOREMAN_NO_LOCAL_MODELS=1 (no embedder), as on CI — verify with `FOREMAN_NO_LOCAL_MODELS=1 python3 plugin/tests/run.py test_moons_scale`
- [ ] test_ui_replay.Run's timeout leaves no child of claude running: the replay starts claude in its own process group and kills the group on timeout — verify with `python3 plugin/tests/run.py test_ui_replay`
- [ ] the tests workflow on main passes on the next push — verify with `gh run list --branch main --workflow tests --limit 1 | grep -q success`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: T-3002's fake embedder for the moons classes; for ui_replay, kill the whole process group the replay starts (start_new_session and os.killpg on timeout), as Sampo's other runners do; likely outcome: both pass on CI. 2. Do less: raise the timeout; fails if: the child outlives any timeout because nothing kills it. 3. Skip on CI; fails if: CI stops testing them. Choice 1 (80%)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] T-3002's fake embedder (depends on it)  <- CURRENT
2. [ ] failing test: a fake claude that forks a sleeping child; after the timeout no child remains
3. [ ] the process-group kill in the replay runner
4. [ ] push through sampo ship and read CI
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-04T13:53:41Z created
- 2026-11-05T03:49:19Z planned from capture
- 2026-11-05T03:49:23Z set approved=True
- 2026-11-05T03:49:24Z set depends_on=['T-3002']
- 2026-11-05T03:49:24Z blocked: after T-3002 (the moons classes); the ui_replay part waits for a builder slot
- 2026-11-06T03:52:45Z unblocked
- 2026-11-06T09:09:00Z builder 2026-11-06: every CI failure visible on main (run 42186952825) is already fixed on foreman/build: test_bench_hooks cleanup (T-3241), macOS Landlock skips (T-3238), /proc skip (T-3240), moons embedder (T-3220); test_ui_replay passes; no code change; the 'next push is green' criterion waits on the push
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- The commit d1901b5 broke the Python test suite (`python3 plugin/tests/run.py`), and the fix is a targeted repair of whichever test or source file that commit touched. This is the likeliest reading: the title says "(tests)" and the gate list has one runner for this.
- The failure is a stale or flaky test, not a source bug. A test such as `plugin/tests/test_genesis.py` (a frequently changed file) may assert on behaviour that has since moved, so the repair belongs in the test and not the source.
- The red CI comes from a different gate that is also labeled "tests", such as `claude plugin test mods/foreman-ui` (`mods/foreman-ui/tests/foreman-ui.test.tsx`, which reads `bench/` and `docs/`) or `plugin/tests/e2e/roundtrip.py`, and not from `run.py`.
- The failure is already gone at HEAD 3d1fb1b, because the map is built from 3d1fb1b and not d1901b5. The right move is then to confirm that and report it, with no code change.
Approaches:
- Reproduce first. The working directory is not a git repo, so locate the checkout and run `python3 plugin/tests/run.py` there. Pull the CI log for d1901b5 from the GitHub commit page. Take the first failing test name and traceback, then diff d1901b5 against its parent for the files that test maps to…
- Bisect between d1901b5 and HEAD 3d1fb1b. Run the failing test at both commits. If it passes at HEAD, report "already fixed by <commit>" and stop. If it fails at both, fix at HEAD, not at d1901b5.
- Fix the root cause in the mapped source module (for example `plugin/lib/fmcore.py`, `fmhooks.py`, `fmguard.py` or `plugin/lib/sampo/cli.py`) if the test encodes intended behaviour. Update the test only if the commit deliberately changed the contract, and check `CHANGELOG.md` for that intent.
- Rerun every gate in the map after the fix (`fm doctor`, `roundtrip.py`, `bench_hooks.py --runs 20`, `run.py`, `fm replay`), because the hooks and core modules are shared by many tests.
Failure modes:
- Fixing the wrong gate: the CI-red report says only "tests", so repairing `run.py` failures while the actual red job is `mods/foreman-ui` or `roundtrip.py` leaves CI red.
- Working in a directory that is not a git checkout, so there is no way to diff or bisect. Guessing from the map alone would patch an unrelated file among the 15088 files, most of which are `.foreman/` and `.sampo/` state.
- Making the test pass by loosening an assertion or skipping it in `plugin/tests/test_*.py`, which hides a real regression in `fmhooks.py` or `fmcore.py`.
- A fix that passes locally but not in CI because of environment drift (a Python version, a missing fixture under `plugin/tests/fixtures/`, or a timing-sensitive `bench_hooks.py` threshold), so the log has to be read before the fix is trusted.
## Dissent
- [ ] rival reading: The commit d1901b5 broke the Python test suite (`python3 plugin/tests/run.py`), and the fix is a targeted repair of whichever test or source file that commit touched. This is the likeliest reading: the title says "(tests)" and the gate list has one runner for this.
- [ ] rival reading: The failure is a stale or flaky test, not a source bug. A test such as `plugin/tests/test_genesis.py` (a frequently changed file) may assert on behaviour that has since moved, so the repair belongs in the test and not the source.
- [ ] rival reading: The red CI comes from a different gate that is also labeled "tests", such as `claude plugin test mods/foreman-ui` (`mods/foreman-ui/tests/foreman-ui.test.tsx`, which reads `bench/` and `docs/`) or `plugin/tests/e2e/roundtrip.py`, and not from `run.py`.
- [ ] rival reading: The failure is already gone at HEAD 3d1fb1b, because the map is built from 3d1fb1b and not d1901b5. The right move is then to confirm that and report it, with no code change.
- [ ] rival approach: Reproduce first. The working directory is not a git repo, so locate the checkout and run `python3 plugin/tests/run.py` there. Pull the CI log for d1901b5 from the GitHub commit page. Take the first failing test name and traceback, then diff d1901b5 against its parent for the files that test maps to…
- [ ] rival approach: Bisect between d1901b5 and HEAD 3d1fb1b. Run the failing test at both commits. If it passes at HEAD, report "already fixed by <commit>" and stop. If it fails at both, fix at HEAD, not at d1901b5.
- [ ] rival approach: Fix the root cause in the mapped source module (for example `plugin/lib/fmcore.py`, `fmhooks.py`, `fmguard.py` or `plugin/lib/sampo/cli.py`) if the test encodes intended behaviour. Update the test only if the commit deliberately changed the contract, and check `CHANGELOG.md` for that intent.
- [ ] rival approach: Rerun every gate in the map after the fix (`fm doctor`, `roundtrip.py`, `bench_hooks.py --runs 20`, `run.py`, `fm replay`), because the hooks and core modules are shared by many tests.
