---
id: T-2529
type: FIX
tier: S
status: done
priority: urgent
scope: [plugin/lib/fmexam.py, plugin/tests/test_exam.py, CHANGELOG.md]
depends_on: []
source: baseline
created: 2026-11-02T03:34:15Z
updated: 2026-11-02T04:04:06Z
trigger: baseline
trigger_key: 2faa76057fcad088
baseline: true
base: f35484568f1590c2cdbd5165692a3b0f788c6e64
base_tree: bdb63e6c4453f12086c05912eb3d60094fd42654
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T03:41:39Z
plan0_scope: [plugin/lib/fmexam.py, plugin/tests/test_exam.py, CHANGELOG.md]
verified: strong
---
# The exam drops the package kind on a host whose Python has no setuptools, as its docstring promises
## Raw request
> Baseline red: `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py` fails test_exam.ExamGen.test_oracle_scores_full_and_empty_scores_zero, test_exam.ExamPython.test_planted_fails_hidden_checks_and_clean_passes, test_exam.ProofKinds.test_kind_package_installs_offline_and_runs_its_command_and_moves_no_beyond_item. Captured by fm check: the gates are red, so fix this before new work (it may not be this task's doing).
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] on a Python without setuptools (python3.12 from uv), the exam draws no package item and test_exam passes — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_exam`
- [x] the system python still draws and grades the package kind — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: with find_spec mocked to None, draw(…, ('package',), …) is empty; the package-grading test skips when package_backend() names a reason
2. [x] fmexam.draw skips PY_ONLY kinds when package_backend() names a reason
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam.ProofKinds` → ✗ exit 1 · Ran 6 tests in 22.9s (1 classes, 16 at a time; slowest: ProofKinds 22s) / FAILED (1 classes: test_exam.ProofKinds) [ran] [tree 7b4a8f58cec3] [world 2f1906870a] (2026-11-02T03:42:14Z)
- (step 2) `python3 plugin/tests/run.py test_exam && ~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_exam` → exit 0 · Ran 93 tests in 124.2s (23 classes, 16 at a time; slowest: LeanKind 123s, ExamAuthors 88s, JudgmentKinds 82s) / OK [ran] [tree 527bd0b146d8] [world 2f1906870a] (2026-11-02T03:45:52Z)
- `python3 plugin/tests/run.py test_exam.ProofKinds` → ✗ exit 1 · Ran 6 tests in 6.8s (1 classes, 16 at a time; slowest: ProofKinds 5s) / FAILED (1 classes: test_exam.ProofKinds) (start tree + this task's tests) [ran] [tree 527bd0b146d8] [world 2f1906870a] (2026-11-02T03:46:09Z)
- `python3 plugin/tests/run.py test_exam.ProofKinds` → exit 0 · Ran 6 tests in 5.6s (1 classes, 16 at a time; slowest: ProofKinds 5s) / OK [ran] [tree 527bd0b146d8] [world 2f1906870a] (2026-11-02T03:46:09Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_exam` → exit 0 · Ran 93 tests in 82.3s (23 classes, 16 at a time; slowest: LeanKind 82s, ExamAuthors 75s, JudgmentKinds 70s) / OK [ran] [tree 1e92bbea5d35] [world 2f1906870a] (2026-11-02T03:56:02Z)
- (ac 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 93 tests in 83.6s (23 classes, 16 at a time; slowest: LeanKind 83s, ExamAuthors 76s, JudgmentKinds 72s) / OK [ran] [tree 1e92bbea5d35] [world 2f1906870a] (2026-11-02T03:56:02Z)
- (audit edge) `self-review: the draw skip reuses package_backend(), the grader's own check, so draw and grading agree on one host test` → a host without setuptools draws no package item and the other kinds' ids are unchanged; the grading test skips there naming the reason; with setuptools nothing changes [tree 1e92bbea5d35] (2026-11-02T03:56:02Z)
- (audit self) `self-review: the draw skip reuses package_backend(), the grader's own check, so draw and grading agree on one host test` → no findings [tree 1e92bbea5d35] (2026-11-02T03:56:02Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 1e92bbea5d35] [world 2f1906870a] (2026-11-02T03:58:09Z)
## Log
- 2026-11-02T03:34:15Z created
- 2026-11-02T03:36:41Z planned from capture
- 2026-11-02T03:41:38Z focused
- 2026-11-02T03:41:39Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T03:46:20Z scope: fmexam.draw's PY_ONLY skip also checks package_backend(); test_exam gains a no-setuptools draw test and the grading test skips on such a host
- 2026-11-02T03:57:39Z done
- 2026-11-02T03:57:42Z committed 528be077 (3 files)
- 2026-11-02T03:58:09Z guard authorization added: publish
- 2026-11-02T04:04:06Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2286 [FIX M, dropped, 0 steps] Baseline red:…
- T-2436 [FIX M, dropped, 0 steps] Baseline red:…
- T-2309 [FIX S, done, 1 steps] Guard speed tests time CPU, not the wall clock, so a loaded host can't fail them — lesson: A complexity bar measures CPU (time.process_time…
- decision 2026-10-31: [revisited: The Genesis frame may grow] [cites: the user's steer 2026-10-30 (sixth): the frame grows, never shrinks] [check: python3 plugin/tests/ru…
- the similar finished task took 1 steps
- start here (files T-2309 touched): plugin/tests/test_guard.py
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_exam.py
## Why not caught
T-2524's gate ran on the system python, which has setuptools; fm ship tests with the remembered uv python3.12, which has none. The docstring promised gen drops the item, but only the grader checked the backend.
## Lessons
- a gate that runs on one interpreter can't vouch for a deliverable built with the host's packages; let the drawer and the grader share one capability check
## Plan gaps
- failed first: step 1 red test: with find_spec mocked to None, draw(…, ('package',), …) is empty; the package-grading tes…
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/fmexam.py
- CHANGELOG.md
