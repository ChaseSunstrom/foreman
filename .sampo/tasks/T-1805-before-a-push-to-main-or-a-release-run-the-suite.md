---
id: T-1805
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-28T01:52:05Z
updated: 2026-10-28T09:45:40Z
group: CI and release pipeline gates
base: c2b93e94a0c6a2303c334535b402cc09ceaead55
base_tree: c9faca75124642fee97a979797a167ec12322031
plan0_at: 2026-10-28T09:38:35Z
plan0_scope: []
verified: strong
---
# Before a push to main or a release, run the suite once under the oldest supported Python w
## Raw request
> Before a push to main or a release, run the suite once under the oldest supported Python when one is installed (uv python find 3.12); every fm check would double gate time, so not there (T-1799's why-not-caught)
## Interpretation
fm check --python oldest|VER runs the gates with that interpreter first on PATH as python3/python (oldest = the lowest Foreman supports, fmpy.NAMES[-1], found on PATH or by uv python find), so a push to main or a release catches 3.12-only breaks (T-1799) without doubling every fm check. The release skill's gate step and MASTER name it.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm check --python VER runs gates under that interpreter; a VER not on the machine is refused — verify with `cd plugin/tests && python3 -m unittest -q test_check_paths.CheckPython`
## Non-goals
## Approach (options → choice → why)
(a) --python on fm check: a temp shim dir prepended to PATH; env_id already keys the gate cache on PATH, so the 3.12 pass is its own cache entry. (b) a separate fm verb: a second gate runner to keep in step. (c) a pre-push git hook: Foreman doesn't install git hooks; a hook in every repo is cost at scale. → (a), plus the release skill line.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then --python on fm check, release skill and MASTER
2. [x] gates and review
## Resume here
<!-- auto -->
- 2026-10-28T09:41:44Z step 2/2: gates and review
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmpy.py, plugin/skills/release/SKILL.md, plugin/tests/test_check_paths.py
- touched since last checkpoint: plugin/lib/fmpy.py, plugin/skills/release/SKILL.md, CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/tests/test_check_paths.py
## Docs impact
CHANGELOG.md MASTER.md plugin/skills/release/SKILL.md
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest -q test_check_paths.CheckPython` → red as expected (exit 1) · Ran 1 test in 0.454s / FAILED (failures=1) [ran] [tree 3773424e4b1b] (2026-10-28T09:38:55Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_check_paths` → exit 0 · Ran 11 tests in 21.615s / OK [ran] [tree 211f024590e9] (2026-10-28T09:40:13Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_check_paths test_docs` → exit 0 · Ran 69 tests in 34.545s / OK [ran] [tree 80339aaa4cf7] (2026-10-28T09:41:13Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmpy.py — commit it through a task, or git checkout it back / fm doctor: OK (48 pass, 6 warn, 0 ; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · SessionEnd                  35.9    37.2     150  [0] / machine busy (load 1.2 per core): judged by each hook's CPU time, not wall time (T-0805); claude plugin test mods/foreman-ui [ran] [tree 80339aaa4cf7] (2026-10-28T09:45:01Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_check_paths.CheckPython` → exit 0 · Ran 1 test in 0.323s / OK [ran] [tree 80339aaa4cf7] (2026-10-28T09:45:14Z)
- (audit intent) `self-review of a ~40-line diff: fmpy.find gained names/uv filters, cmd_check --python re-enters itself with a PATH shim; the test stubs a 3.12 that answers fmpy's probe and marks its runs` → fm check --python oldest runs the gates with the lowest supported python as python3; the release skill and push note name it [tree 80339aaa4cf7] (2026-10-28T09:45:14Z)
- (audit edge) `self-review of a ~40-line diff: fmpy.find gained names/uv filters, cmd_check --python re-enters itself with a PATH shim; the test stubs a 3.12 that answers fmpy's probe and marks its runs` → VER must match 3.N before it reaches a path or glob; oldest is NAMES[-1]; the 'gates under' line goes to stderr so --json stays one document; the shim is removed in finally and PATH restored [tree 80339aaa4cf7] (2026-10-28T09:45:14Z)
- (audit adversary) `self-review of a ~40-line diff: fmpy.find gained names/uv filters, cmd_check --python re-enters itself with a PATH shim; the test stubs a 3.12 that answers fmpy's probe and marks its runs` → VER is regex-checked before any filesystem use; mkdtemp is 0700, so nobody else can plant a python3 in the shim [tree 80339aaa4cf7] (2026-10-28T09:45:14Z)
- (audit operator) `self-review of a ~40-line diff: fmpy.find gained names/uv filters, cmd_check --python re-enters itself with a PATH shim; the test stubs a 3.12 that answers fmpy's probe and marks its runs` → zero cost unless the flag is passed; one version probe per candidate; env_id keys the gate cache on PATH, so the 3.12 pass never reuses the 3.14 one [tree 80339aaa4cf7] (2026-10-28T09:45:14Z)
- (audit self) `self-review of a ~40-line diff: fmpy.find gained names/uv filters, cmd_check --python re-enters itself with a PATH shim; the test stubs a 3.12 that answers fmpy's probe and marks its runs` → no findings [tree 80339aaa4cf7] (2026-10-28T09:45:14Z)
## Log
- 2026-10-28T01:52:05Z created
- 2026-10-28T09:34:30Z set type=FEATURE, tier=S
- 2026-10-28T09:38:31Z criterion 1 verify: `cd plugin/tests && python3 -m unittest -q test_check_python` → `cd plugin/tests && python3 -m unittest -q test_check_paths.CheckPython`
- 2026-10-28T09:38:35Z focused
- 2026-10-28T09:39:51Z criterion 1 text: fm check --python VER runs gates under that interpreter; unknown VER exits 2 → fm check --python VER runs gates under that interpreter; a VER not on the machine is refused
- 2026-10-28T09:45:38Z done
- 2026-10-28T09:45:40Z committed b734071b (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0953 [FEATURE S, done, 1 steps] Release 1.2.30 to GitHub main (user asked to push) — lesson: Run the full suite before release.py when a session changed hook wiring: t…
- T-1440 [FEATURE S, done, 1 steps] Release Foreman 1.2.49 (foreman-ui 0.18.3) and push to main — lesson: A new machine-state check can block the release gate on its first…
- T-0368 [FIX M, done, 3 steps] fm and the hooks re-run under a supported Python when python3 is below 3.12.7 — lesson: Check the interpreter a remote Foreman really runs …
- decision 2026-10-21: Revert and drop T-1441 (auto-accepting Foreman's own plugins in the supply check)
- similar finished tasks took 1–3 steps
## Lessons
- A flag that re-runs a command under another interpreter is a PATH shim plus re-entry: the gate cache already keys on PATH, so no new cache field was needed
## Files touched
- plugin/tests/test_check_paths.py
- plugin/lib/fmpy.py
- plugin/lib/fmcli.py
- plugin/skills/release/SKILL.md
- CHANGELOG.md
- MASTER.md
