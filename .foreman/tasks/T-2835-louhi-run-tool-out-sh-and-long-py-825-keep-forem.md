---
id: T-2835
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-03T19:26:14Z
updated: 2026-11-03T20:22:56Z
base: 643a52e824af7f1a960692f1ae75e841e68f324a
base_tree: d2a16415edc5b92512eb8ba2337e9a031083bcd1
predict_minutes: 1
predict_attempts: 1
plan0_at: 2026-11-03T20:13:59Z
plan0_scope: []
verified: ok
unproven: [typed]
---
# louhi._run, _tool_out, _sh and long.py ~825 keep FOREMAN_* in model-written runs, so the…
## Raw request
> CLEAN: louhi._run, _tool_out, _sh and long.py ~825 keep FOREMAN_* in model-written runs, so the load gate can fire inside them the way it did in the sandboxes T-2822 fixed; decide per site whether it is a sandbox (route through c.sandbox_env) or a real run
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] louhi's _run, _tool_out, _sh and long's _recur_state run model-written code through c.sandbox_env: no FOREMAN_*, CLAUDE* or GIT_* inherited, the load gate off, credentials still stripped — verify with `python3 plugin/tests/run.py test_exam test_long`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: each site's env drops FOREMAN_HOME, CLAUDE_X, GIT_DIR and a credential, keeps PATH, sets FOREMAN_LOAD_GATE=0
2. [x] route the four sites through c.sandbox_env
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam.ModelRunEnv` → red: {'CLAUDE_X', 'FOREMAN_HOME', 'GIT_DIR'} reach model-written runs [tree 77c331e774e8] (2026-11-03T20:14:30Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_long` → exit 0 · Ran 157 tests in 136.3s (33 classes, 16 at a time; slowest: LeanKind 135s, ExamAuthors 96s, Long 94s) / OK [ran] [tree 0feb5b487ada] [world 2f1906870a] (2026-11-03T20:19:04Z)
- `python3 plugin/tests/run.py test_exam.ModelRunEnv` → ✗ exit 1 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: ModelRunEnv 0s) / FAILED (1 classes: test_exam.ModelRunEnv) (start tree + this task's tests) [ran] [tree 0feb5b487ada] [world 2f1906870a] (2026-11-03T20:19:28Z)
- `python3 plugin/tests/run.py test_exam.ModelRunEnv` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: ModelRunEnv 0s) / OK [ran] [tree 0feb5b487ada] [world 2f1906870a] (2026-11-03T20:19:28Z)
- (ac 1) `python3 plugin/tests/run.py test_exam test_long` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T20:19:04Z [ran] [tree 0feb5b487ada] [world 2f1906870a] (2026-11-03T20:19:29Z)
- `python3 plugin/tests/run.py test_exam.ModelRunEnv` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T20:19:28Z [ran] [tree 0feb5b487ada] [world 2f1906870a] (2026-11-03T20:19:29Z)
- (audit intent) `self: the four sites now share louhi._model_env / c.sandbox_env; credentials are still stripped first, ENV (PYTHONDONTWRITEBYTECODE, NODE_NO_WARNINGS) still added; callers (_run for suites and checks, _sh for venv/pip/docs blocks, _tool_out) need no FOREMAN_*, CLAUDE* or GIT_* var` → model-written code can no longer see FOREMAN_HOME or the session's GIT_DIR, and never waits on host load [tree 0feb5b487ada] (2026-11-03T20:19:29Z)
- (audit edge) `self: the four sites now share louhi._model_env / c.sandbox_env; credentials are still stripped first, ENV (PYTHONDONTWRITEBYTECODE, NODE_NO_WARNINGS) still added; callers (_run for suites and checks, _sh for venv/pip/docs blocks, _tool_out) need no FOREMAN_*, CLAUDE* or GIT_* var` → pip install --no-index and venv under _sh don't read GIT_* or FOREMAN_*; a target whose own tests set GIT_* still sets them itself [tree 0feb5b487ada] (2026-11-03T20:19:29Z)
- (audit adversary) `self: the four sites now share louhi._model_env / c.sandbox_env; credentials are still stripped first, ENV (PYTHONDONTWRITEBYTECODE, NODE_NO_WARNINGS) still added; callers (_run for suites and checks, _sh for venv/pip/docs blocks, _tool_out) need no FOREMAN_*, CLAUDE* or GIT_* var` → strictly narrows what untrusted code inherits; GIT_DIR leaking could have pointed a model's git at the real repo [tree 0feb5b487ada] (2026-11-03T20:19:29Z)
- (audit self) `self: the four sites now share louhi._model_env / c.sandbox_env; credentials are still stripped first, ENV (PYTHONDONTWRITEBYTECODE, NODE_NO_WARNINGS) still added; callers (_run for suites and checks, _sh for venv/pip/docs blocks, _tool_out) need no FOREMAN_*, CLAUDE* or GIT_* var` → no findings [tree 0feb5b487ada] (2026-11-03T20:19:29Z)
- `python3 plugin/tests/run.py test_exam.ModelRunEnv` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T20:19:29Z [ran] [tree 0feb5b487ada] [world 2f1906870a] (2026-11-03T20:21:14Z)
- (audit intent) `self: the four sites now share louhi._model_env / c.sandbox_env; credentials are still stripped first, ENV still added; callers (_run, _sh, _tool_out, _recur_state) need no FOREMAN_*, CLAUDE* or GIT_* var` → model-written code can no longer see FOREMAN_HOME or the session's GIT_DIR, and never waits on host load [tree 0feb5b487ada] (2026-11-03T20:21:14Z)
- (audit edge) `self: the four sites now share louhi._model_env / c.sandbox_env; credentials are still stripped first, ENV still added; callers (_run, _sh, _tool_out, _recur_state) need no FOREMAN_*, CLAUDE* or GIT_* var` → pip --no-index and venv under _sh don't read GIT_* or FOREMAN_*; a target whose tests need GIT_* sets them itself [tree 0feb5b487ada] (2026-11-03T20:21:14Z)
- (audit adversary) `self: the four sites now share louhi._model_env / c.sandbox_env; credentials are still stripped first, ENV still added; callers (_run, _sh, _tool_out, _recur_state) need no FOREMAN_*, CLAUDE* or GIT_* var` → strictly narrows what untrusted code inherits; a leaked GIT_DIR could point a model's git at the real repo [tree 0feb5b487ada] (2026-11-03T20:21:14Z)
- (audit self) `self: the four sites now share louhi._model_env / c.sandbox_env; credentials are still stripped first, ENV still added; callers (_run, _sh, _tool_out, _recur_state) need no FOREMAN_*, CLAUDE* or GIT_* var` → no findings [tree 0feb5b487ada] (2026-11-03T20:21:14Z)
## Log
- 2026-11-03T19:26:14Z created
- 2026-11-03T20:13:58Z planned: it has criteria and steps
- 2026-11-03T20:13:58Z set tier=S
- 2026-11-03T20:13:58Z focused
- 2026-11-03T20:13:59Z predicted from its closes: 1 min, 1 attempt(s)
- 2026-11-03T20:22:54Z done
- 2026-11-03T20:22:56Z committed 90879432 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2822 [FIX M, done, 3 steps] CI failed on this branch: run 41676727022 — lesson: A gate that reads the machine must be off inside the harness's own sandboxes: route eve…
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- decision 2026-10-21: T-1298: refusals for programs the guard couldn't read drop the --allow system route instead of keeping it
- similar past tasks were M: consider --tier M
## Behaviour lock
none: the lock is the regression test itself — ModelRunEnv was written and run red before the source edits (fm task prove shows it fails on the start tree), and the full test_exam + test_long suites (157 tests) ran green after; no behaviour other than the env passed to model runs changes
## Lessons
- Every subprocess that runs model-written code goes through c.sandbox_env, not a hand-rolled credential filter: the filter strips secrets but not state paths
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/sampo/louhi.py
- plugin/lib/sampo/long.py
