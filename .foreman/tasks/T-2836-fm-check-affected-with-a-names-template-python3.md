---
id: T-2836
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-03T20:27:15Z
updated: 2026-11-03T20:34:05Z
base: 768b6aa3ba8ad355068b19268a0f4f2fa8f5b3d3
base_tree: 821d5ec174d711d006608ef8c44a29c39d754712
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-03T20:29:00Z
plan0_scope: []
verified: ok
unproven: [typed]
---
# fm check --affected with a {names} template (python3 plugin/tests/run.py {names}) hands…
## Raw request
> FIX: fm check --affected with a {names} template (python3 plugin/tests/run.py {names}) hands the runner every changed test_*.py by bare name, including plugin/templates/mcp-server/test_server.py, a template the runner can't find, so run.py fails 'no test matches test_server' and every close that touches a template's test is refused; cli.affected should keep only tests under the folder the template's runner path names (map.py:34 also links template tests as project tests)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with a {names} template whose runner is a file in the repo (python3 plugin/tests/run.py {names}), fm check --affected hands it only tests under the runner's folder; a changed test_*.py elsewhere (a template's) is left out, and a {tests} template is unchanged — verify with `python3 plugin/tests/run.py test_affected_hubs`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: a changed template test_server.py stays out of a {names} runner's command; tests/test_a.py stays in
2. [x] fix: cli.affected filters {names} groups to the runner's folder
## Resume here
<!-- auto -->
- 2026-11-03T20:32:42Z step 2/2: fix: cli.affected filters {names} groups to the runner's folder
- git: foreman/build; 2 uncommitted: plugin/lib/sampo/cli.py, plugin/tests/test_affected_hubs.py
- touched since last checkpoint: plugin/tests/test_affected_hubs.py, plugin/lib/sampo/cli.py, /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/directions-v2/12-forge-illustrated/_src/page.js
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_affected_hubs` → red: 'python3 tests/run.py test_server test_a' != 'python3 tests/run.py test_a' [tree 1ad625785c2f] (2026-11-03T20:29:34Z)
- (step 2) `python3 plugin/tests/run.py test_affected_hubs test_cli test_file_map_close test_subdir_matrix test_bookkeeping` → exit 0 · Ran 184 tests in 37.4s (57 classes, 16 at a time; slowest: TaskLifecycle 37s, CaptureAndIntake 13s, SubdirMatrix 12s) / OK [ran] [tree d99d817a3b05] [world 2f1906870a] (2026-11-03T20:33:10Z)
- `python3 plugin/tests/run.py test_affected_hubs` → ✗ exit 1 · Ran 4 tests in 4.7s (1 classes, 16 at a time; slowest: AffectedHubs 2s) / FAILED (1 classes: test_affected_hubs.AffectedHubs) (start tree + this task's tests) [ran] [tree d99d817a3b05] [world 2f1906870a] (2026-11-03T20:33:18Z)
- `python3 plugin/tests/run.py test_affected_hubs` → exit 0 · Ran 4 tests in 2.1s (1 classes, 16 at a time; slowest: AffectedHubs 2s) / OK [ran] [tree d99d817a3b05] [world 2f1906870a] (2026-11-03T20:33:18Z)
- (ac 1) `python3 plugin/tests/run.py test_affected_hubs` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T20:33:18Z [ran] [tree d99d817a3b05] [world 2f1906870a] (2026-11-03T20:33:25Z)
- (audit intent) `self: cli.affected's build() passes each group's tests through home(): a {names} template keeps only tests under its runner file's folder (first template word that is a file in the repo); {tests} templates and runners at the repo root are unchanged` → plugin/templates/mcp-server/test_server.py no longer reaches run.py by bare name, so closes touching templates aren't refused [tree d99d817a3b05] (2026-11-03T20:33:25Z)
- (audit edge) `self: cli.affected's build() passes each group's tests through home(): a {names} template keeps only tests under its runner file's folder (first template word that is a file in the repo); {tests} templates and runners at the repo root are unchanged` → a {names} runner with no file word (a module runner like -m unittest) keeps every test; subfolders under the runner's folder stay in; by-extension groups get the same filter [tree d99d817a3b05] (2026-11-03T20:33:25Z)
- (audit adversary) `self: cli.affected's build() passes each group's tests through home(): a {names} template keeps only tests under its runner file's folder (first template word that is a file in the repo); {tests} templates and runners at the repo root are unchanged` → only narrows what runs on --affected; the full fm check gates still run every test before ship [tree d99d817a3b05] (2026-11-03T20:33:25Z)
- (audit self) `self: cli.affected's build() passes each group's tests through home(): a {names} template keeps only tests under its runner file's folder (first template word that is a file in the repo); {tests} templates and runners at the repo root are unchanged` → no findings [tree d99d817a3b05] (2026-11-03T20:33:25Z)
## Log
- 2026-11-03T20:27:15Z created
- 2026-11-03T20:28:59Z planned: it has criteria and steps
- 2026-11-03T20:28:59Z set tier=S
- 2026-11-03T20:28:59Z focused
- 2026-11-03T20:29:00Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-03T20:34:03Z done
- 2026-11-03T20:34:05Z committed f491d6fd (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2086 [FIX S, done, 3 steps] T-2080's close passed its gates but fm ship's scratch-tree run failed…
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- decision 2026-10-30: [cites: user steer 2026-10-29: COVERAGE BY GRID, NOT BY LUCK] Genesis standing rule: coverage by grid — coverage.md (fm genesis put): rows = the 13 …
- similar finished tasks took 3–5 steps
## Why not caught
the template's test file was first touched by T-2818; no earlier close changed a test_*.py outside plugin/tests
## Lessons
- A bare-name test runner addresses only its own folder: filter changed test files by the runner's location before handing them over
## Files touched
- plugin/tests/test_affected_hubs.py
- plugin/lib/sampo/cli.py
