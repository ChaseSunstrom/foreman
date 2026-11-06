---
id: T-2525
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_proof.py, plugin/tests/test_core.py]
depends_on: []
source: user
created: 2026-11-02T02:36:32Z
updated: 2026-11-02T02:50:39Z
base: 2fb3b24ca7a17cce7dba83c495e81e54f976a097
base_tree: b0b274a59e5a8299074b141e68f7590d9f08bbc4
predict_minutes: 7
predict_attempts: 1
plan0_at: 2026-11-02T02:36:34Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_proof.py, plugin/tests/test_core.py]
verified: strong
---
# T-2334's late start point applies only to open tasks, and the docs-unknown proof test keeps its no-start-commit premise
## Raw request
> T-2334's late start point applies only to open tasks, and the docs-unknown proof test keeps its no-start-commit premise
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] evidence on a done or dropped task records no late start point (one after its commit would give it an empty diff); test_proof's docs-unknown case builds its brief without fm's evidence writer, so it has no start commit; the full suite passes — verify with `python3 plugin/tests/run.py test_proof test_core`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: fm task evidence on a done task with no base leaves base unset; the full test_proof.Proof is red now (the regression)
2. [x] fmcli evidence: late only when the brief's status isn't closed; test_proof: the docs-unknown task uses lines= (written as fm's runs, no late record)
## Resume here
## Docs impact
none: corrects T-2334 before it shipped
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_core.StartPoint test_proof.Proof` → ✗ exit 1 · Ran 33 tests in 17.7s (2 classes, 16 at a time; slowest: Proof 17s, StartPoint 1s) / FAILED (2 classes: test_proof.Proof, test_core.StartPoint) [ran] [tree c7357767f551] [world 2f1906870a] (2026-11-02T02:37:19Z)
- (step 1) `python3 plugin/tests/run.py test_core.StartPoint test_proof.Proof` → exit 0 · Ran 33 tests in 17.7s (2 classes, 16 at a time; slowest: Proof 17s, StartPoint 1s) / OK [ran] [tree 3b9d40624dc2] [world 2f1906870a] (2026-11-02T02:38:22Z)
- (step 2) `python3 plugin/tests/run.py test_core test_proof test_cli` → exit 0 · Ran 320 tests in 21.5s (80 classes, 16 at a time; slowest: TaskLifecycle 21s, Proof 20s, StateViews 10s) / OK [ran] [tree 3b9d40624dc2] [world 2f1906870a] (2026-11-02T02:38:44Z)
- `python3 plugin/tests/run.py test_core.StartPoint` → ✗ exit 1 · Ran 4 tests in 1.8s (1 classes, 16 at a time; slowest: StartPoint 1s) / FAILED (1 classes: test_core.StartPoint) (start tree + this task's tests) [ran] [tree 3b9d40624dc2] [world 2f1906870a] (2026-11-02T02:38:47Z)
- `python3 plugin/tests/run.py test_core.StartPoint` → exit 0 · Ran 4 tests in 0.8s (1 classes, 16 at a time; slowest: StartPoint 1s) / OK [ran] [tree 3b9d40624dc2] [world 2f1906870a] (2026-11-02T02:38:47Z)
- (ac 1) `python3 plugin/tests/run.py test_proof test_core` → exit 0 · Ran 177 tests in 17.9s (36 classes, 16 at a time; slowest: Proof 18s, ConfidenceRoutes 6s, BriefIndex 2s) / OK [ran] [tree 3b9d40624dc2] [world 2f1906870a] (2026-11-02T02:44:32Z)
- (audit edge) `self-review: the late start point now needs an open brief (status not closed) as well as no base and a git repo; the docs-unknown proof test builds its brief through lines= (fm's own runs written directly), so it keeps no start commit; the full suite passed on this tree` → evidence on a done task leaves base unset; an open task with no base still gets HEAD; a task with a base keeps it [tree 3b9d40624dc2] (2026-11-02T02:44:32Z)
- (audit self) `self-review: the late start point now needs an open brief (status not closed) as well as no base and a git repo; the docs-unknown proof test builds its brief through lines= (fm's own runs written directly), so it keeps no start commit; the full suite passed on this tree` → no findings [tree 3b9d40624dc2] (2026-11-02T02:44:32Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 3b9d40624dc2] [world 2f1906870a] (2026-11-02T02:45:39Z)
## Log
- 2026-11-02T02:36:32Z created
- 2026-11-02T02:36:32Z focused
- 2026-11-02T02:36:34Z predicted from its closes: 7 min, 1 attempt(s)
- 2026-11-02T02:45:09Z done
- 2026-11-02T02:45:12Z committed 048da03e (3 files)
- 2026-11-02T02:45:39Z guard authorization added: publish
- 2026-11-02T02:50:39Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2334 [FIX M, done, 2 steps] A task always gets a start point: a git timeout at focus or at finish is retried, never read as no start commit — lesson: A timeout is not …
- T-1907 [FIX S, done, 3 steps] Fm task finish asks for the adversary lens before its checks run — lesson: A refusal done makes late should run where finish gathers its ga…
- T-1906 [FIX S, done, 3 steps] Fm task finish checks a FIX's red-to-green proof before running its checks — lesson: A refusal known before the checks run must be said bef…
- decision 2026-10-31: [revisited: Parallel Missions 5-8] [check: python3 plugin/tests/run.py test_lanes] Parallel Missions 5-8 still holds: an L stays in the main thread,…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py
## Why not caught
T-2334 closed on its criterion's tests (test_core, test_cli) while its full gate was red in test_proof, which fm task finish doesn't run; the docs-unknown test's premise (no start commit) is exactly what T-2334's late record removes.
## Lessons
- Read the full gate's verdict on its own before closing; a close chained after the read runs whatever it says
## Plan gaps
- failed first: step 1 red test: fm task evidence on a done task with no base leaves base unset; the full test_proof.Proof…
## Files touched
- plugin/tests/test_core.py
- plugin/lib/fmcli.py
- plugin/tests/test_proof.py
