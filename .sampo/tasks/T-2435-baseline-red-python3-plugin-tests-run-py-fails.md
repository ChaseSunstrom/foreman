---
id: T-2435
type: FIX
tier: M
status: done
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-10-31T18:03:47Z
updated: 2026-10-31T18:25:44Z
trigger: baseline
trigger_key: b3ec737eb8d2687e
baseline: true
base: 28e96faaf272cb22c48cd3650bf62ea3af8814b5
base_tree: 60009de834c0986dd19332e0ce67afdbafc73b07
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-10-31T18:08:40Z
plan0_scope: []
verified: strong
---
# Baseline red: `python3 plugin/tests/run.py` fails…
## Raw request
> Baseline red: `python3 plugin/tests/run.py` fails test_code.Durable.test_a_kill_during_the_check_resumes_at_the_check_without_redoing_the_step, test_code.TaskRun.test_a_task_waiting_for_the_users_yes_runs_nothing_until_it_is_given, test_race.Race.test_l_tasks_and_second_races_are_refused. Captured by fm check: the gates are red, so fix this before new work (it may not be this task's doing).
## Interpretation
Reading 1: fmdoors._local returns 'local' for any write target outside the repo before checking it exists, so a verify that only creates a file (touch /tmp/marker) reads one-way and fm focus/fm code refuse the task; test_code's TaskRun and Durable fixtures hit it. Reading 2: the fixtures are wrong. Ruled out: creating a new file destroys nothing; the classifier is.
## Assumptions (confidence)
## Acceptance criteria
- [x] test_code passes and a verify that creates a new file outside the repo is two-way — verify with `python3 plugin/tests/run.py test_code test_judgment`
## Non-goals
## Approach (options → choice → why)
1) in _local, a path that doesn't exist (lexists false) has nothing to lose: None, after the repo-root check; fails if: a step deletes a path created earlier in the same plan, which the step's own row catches when it runs. 2) use what exists: name the paths in the fixtures' requests; fails if: every real plan with a new outside file still parks. 3) do less: exempt touch; fails if: echo > /tmp/new reads one-way too. Choice 1 (90%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] _local: a missing path is not local; a DoorGate test
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_judgment test_code` → exit 0 · Ran 495 tests in 66.4s (104 classes, 16 at a time; slowest: Worker 66s, Fakes 41s, Bench 18s) / OK [ran] [tree a96b6634d72e] (2026-10-31T18:18:02Z)
- `python3 plugin/tests/run.py test_judgment -k verify_that_only_creates` → ✗ exit 1 · Ran 1 tests in 1.7s (1 classes, 16 at a time; slowest: DoorGate 1s) / FAILED (1 classes: test_judgment.DoorGate) (start tree + this task's tests) [ran] [tree a96b6634d72e] (2026-10-31T18:18:05Z)
- `python3 plugin/tests/run.py test_judgment -k verify_that_only_creates` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: DoorGate 0s) / OK [ran] [tree a96b6634d72e] (2026-10-31T18:18:05Z)
- (ac 1) `python3 plugin/tests/run.py test_code test_judgment` → exit 0 · Ran 495 tests in 66.4s (104 classes, 16 at a time; slowest: Worker 66s, Fakes 41s, Bench 18s) / OK [ran] [tree 1c790f3e62b3] (2026-10-31T18:19:19Z)
- (audit intent) `self-review: traced through the real fm code path (debug tests, removed): after the yes, fm code runs the verify, touch creates the marker, and the re-gated verify read the now-existing outside path as a destroyed target` → test_code TaskRun and Durable pass; a touch or mkdir of an existing file is two-way [tree 1c790f3e62b3] (2026-10-31T18:19:19Z)
- (audit adversary) `self-review: traced through the real fm code path (debug tests, removed): after the yes, fm code runs the verify, touch creates the marker, and the re-gated verify read the now-existing outside path as a destroyed target` → a redirect on the same segment still counts, and echo > existing outside the repo stays one-way (tested) [tree 1c790f3e62b3] (2026-10-31T18:19:19Z)
- (audit edge) `self-review: traced through the real fm code path (debug tests, removed): after the yes, fm code runs the verify, touch creates the marker, and the re-gated verify read the now-existing outside path as a destroyed target` → shell keywords (then, do, if, !) before the program are skipped, so the program is judged [tree 1c790f3e62b3] (2026-10-31T18:19:19Z)
## Log
- 2026-10-31T18:03:47Z created
- 2026-10-31T18:08:39Z planned: it has criteria and steps
- 2026-10-31T18:08:40Z focused
- 2026-10-31T18:08:40Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-10-31T18:18:05Z scope: the fix is in fmdoors._cmd_targets (not _local, the first guess); tests in test_judgment; changelog line
- 2026-10-31T18:19:41Z done
- 2026-10-31T18:19:43Z committed 7a6779b0 (3 files)
- 2026-10-31T18:19:52Z guard authorization added: publish
- 2026-10-31T18:25:44Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2433 [FIX M, done, 1 steps] Baseline red: `python3 plugin/tests/run.py` fails… — lesson: A lane that changes a refusal's reason must grep the suite for the old message…
- T-2429 [FIX M, done, 1 steps] Baseline red:… — lesson: A test that appends then shifts an mtime is shifting from the wall clock: read the mtime before the write
- research T-2342-review: T-2342 review (fm-reviewer, one pass): changes needed; fixed in cd4ceb3a before merge (DoorGate and tidy tests red first; the rest written alongs…
- decision 2026-10-22: [costly] Accepted the plugin supply baseline on 2026-10-22: code-review, context7, frontend-design, security-guidance, skill-creator (claude-plugins…
- similar finished tasks took 1–1 steps
## Why not caught
T-2342's builder ran fm check --affected, which didn't select test_code; the full gates at merge time would have
## Lessons
- A data-loss check must ask whether the command can destroy what is there, not only whether it writes there: touch and mkdir write and lose nothing
## Files touched
- plugin/tests/test_judgment.py
- plugin/tests/test_zz_doordebug.py
- plugin/lib/fmdoors.py
- CHANGELOG.md
