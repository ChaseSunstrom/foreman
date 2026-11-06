---
id: T-2398
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmdoctor.py, plugin/tests/test_core.py, plugin/tests/test_doctor.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-31T14:03:48Z
updated: 2026-11-02T00:18:16Z
group: Mission 7 proof inbox
base: 18abf4089d0514ef77c5278b889dab7b954ead50
base_tree: 5475ce09eee84764b1623be3be4fad398b1fa2b1
predict_minutes: 7
predict_attempts: 1
plan0_at: 2026-11-02T00:07:04Z
plan0_scope: [plugin/lib/fmcore.py, plugin/lib/fmdoctor.py, plugin/tests/test_core.py, plugin/tests/test_doctor.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# Each proof run records the world it leaned on; fm doctor names done tasks whose world moved since
## Raw request
> FEATURE: each proof run records the world it leaned on (interpreter and tool versions, lockfile hash) and fm doctor names proofs whose world moved since (Mission 7 inbox, tier 2)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] an fm-run evidence line carries [world H]: a short hash of the interpreter version and the repo-root lockfiles (uv.lock, package-lock.json, poetry.lock, requirements*.txt, Cargo.lock, go.sum, Gemfile.lock), the parts kept once in the project's worlds.json; fm doctor WARNs with the done tasks of the last 30 days whose newest world differs from today's and names what moved — verify with `python3 plugin/tests/run.py test_core test_doctor`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: fm task evidence --run writes [world H]; changing uv.lock gives a new H; fm doctor's world check names the task and 'uv.lock changed'; with no change it passes
2. [x] fmcore.world(root) (stat-cached hashes) and the mark in add_evidence for ran lines; worlds.json write once per H; fmdoctor.check_worlds; MASTER and CHANGELOG
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_doctor.ProofWorlds test_core.Briefs` → ✗ exit 1 · Ran 19 tests in 1.2s (2 classes, 16 at a time; slowest: ProofWorlds 1s, Briefs 0s) / FAILED (2 classes: test_core.Briefs, test_doctor.ProofWorlds) [ran] [tree af0ec4ab0895] (2026-11-02T00:07:43Z)
- (step 1) `python3 plugin/tests/run.py test_doctor.ProofWorlds test_core.Briefs` → exit 0 · Ran 19 tests in 1.1s (2 classes, 16 at a time; slowest: ProofWorlds 1s, Briefs 0s) / OK [ran] [tree 388278656ec5] [world 2f1906870a] (2026-11-02T00:09:30Z)
- (step 2) `python3 plugin/tests/run.py test_doctor test_core` → exit 0 · Ran 236 tests in 11.4s (60 classes, 16 at a time; slowest: ConfidenceRoutes 11s, ViewsRepair 6s, LockProbe 6s) / OK [ran] [tree 388278656ec5] [world 2f1906870a] (2026-11-02T00:09:43Z)
- (step 2) `fm doctor` → exit 0 · WARN  version skew         uidemo-982f4c ran 1.2.29, lacks 317 (T-0275, T-0705, T-0787, T-0933 …) — restart their sessions on the new Foreman / fm doctor: OK (54 pass, 8 warn, 0 fail) [ran] [tree 388278656ec5] [world 2f1906870a] (2026-11-02T00:09:59Z)
- (ac 1) `python3 plugin/tests/run.py test_core test_doctor` → exit 0 · Ran 236 tests in 6.5s (60 classes, 16 at a time; slowest: ConfidenceRoutes 6s, ViewsRepair 4s, LockProbe 3s) / OK [ran] [tree 013df9f6be3c] [world 2f1906870a] (2026-11-02T00:17:50Z)
- (audit adversary) `self-review: world_here runs only for fm-run evidence, walks up from cwd to the nearest .git, stats 11 lockfile names and hashes the ones present (stat-keyed cache per process), keeps each new world's parts once in state/worlds.json under the state lock, and returns None on any error so a run never fails for its mark; (world is added to the marks typed text can't forge; check_worlds reads done briefs closed in 30 days and compares their newest (world H] with today's, naming changed parts from worlds.json` → typed evidence with '(world x]' is unmarked to '(world x'; a forged H only makes doctor say 'not on record' [tree 013df9f6be3c] (2026-11-02T00:17:50Z)
- (audit edge) `self-review: world_here runs only for fm-run evidence, walks up from cwd to the nearest .git, stats 11 lockfile names and hashes the ones present (stat-keyed cache per process), keeps each new world's parts once in state/worlds.json under the state lock, and returns None on any error so a run never fails for its mark; (world is added to the marks typed text can't forge; check_worlds reads done briefs closed in 30 days and compares their newest (world H] with today's, naming changed parts from worlds.json` → no lockfiles → python only; a lockfile edit changes H; a task with no world mark is skipped; a world not in worlds.json says not on record [tree 013df9f6be3c] (2026-11-02T00:17:50Z)
- (audit self) `self-review: world_here runs only for fm-run evidence, walks up from cwd to the nearest .git, stats 11 lockfile names and hashes the ones present (stat-keyed cache per process), keeps each new world's parts once in state/worlds.json under the state lock, and returns None on any error so a run never fails for its mark; (world is added to the marks typed text can't forge; check_worlds reads done briefs closed in 30 days and compares their newest (world H] with today's, naming changed parts from worlds.json` → no findings [tree 013df9f6be3c] (2026-11-02T00:17:50Z)
## Log
- 2026-10-31T14:03:48Z created
- 2026-11-01T23:43:46Z planned from capture
- 2026-11-02T00:07:03Z focused
- 2026-11-02T00:07:04Z predicted from its closes: 7 min, 1 attempt(s)
- 2026-11-02T00:18:14Z done
- 2026-11-02T00:18:16Z committed 32b1a015 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2396 [FEATURE S, done, 2 steps] ui-unshot counts terminal UIs (TUI screens, statuslines, the pane's hooks) by ui_paths — lesson: When a proof's tool can't reach a surf…
- T-2397 [FEATURE S, done, 3 steps] Research claims say how they were learned (ran, read, recalled); fm prove labels a Decision resting only on recalled ones — lesson: Bef…
- T-2489 [FEATURE M, done, 3 steps] Model layer surfaces: MCP decide tool, fm doctor backend health, the site's Model layer… — lesson: README has a 2000-word visible budge…
- decision 2026-10-30: [revisit: when plugin/lib/fmexam.py changes @ecf3a72d8dff] Exam baseline: the finders arm (fmdocs.scan + fmsecrets, no session) scores 0/108 on s0-0…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_core.py, plugin/tests/test_doctor.py
## Preflight
Changed in scope since this was planned (2026-10-31): CHANGELOG.md, MASTER.md, plugin/lib/fmcore.py, plugin/lib/fmdoctor.py, plugin/tests/test_core.py, plugin/tests/test_doctor.py; re-ground the plan against them before editing
## Lessons
- Record what a proof leaned on next to the proof itself; a green from a world that has since moved is a claim nobody re-checked
## Plan gaps
- failed first: step 1 red tests: fm task evidence --run writes [world H]; changing uv.lock gives a new H; fm doctor's wor…
## Files touched
- plugin/tests/test_doctor.py
- plugin/tests/test_core.py
- plugin/lib/fmcore.py
- plugin/lib/fmdoctor.py
- MASTER.md
- CHANGELOG.md
