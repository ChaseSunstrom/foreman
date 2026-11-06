---
id: T-3229
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/tests/run.py, plugin/tests/test_ci_annotations.py, plugin/tests/test_models.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-05T18:17:00Z
updated: 2026-11-05T18:40:47Z
base: ffff1a7fccd0c20ac93eb11d9479866abf125179
base_tree: 33f919f7d662bf0ee6ded44e14d0a559cf25ed66
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-05T18:34:30Z
plan0_scope: [plugin/tests/run.py, plugin/tests/test_ci_annotations.py, plugin/tests/test_models.py, CHANGELOG.md]
verified: strong
unproven: [meaning, red]
---
# The test runner hides local models from every class unless the caller says otherwise, so a run here sees what CI sees
## Raw request
> sampo check runs the model-touching tests (test_moons_scale, test_models, test_callcards, test_smith) once with FOREMAN_NO_LOCAL_MODELS=1, so a test that leans on this box's Ollama models fails here before CI (T-3220 lesson)
## Interpretation
Root cause, not an extra pass: run.py gives every test class FOREMAN_NO_LOCAL_MODELS=1 unless the caller set it, so a run here sees what CI sees (no local models); test_models' Base pops it, as its fakes stand in for discovery. T-3220's sweep showed only those discovery classes need it off.
## Assumptions (confidence)
## Acceptance criteria
- [x] run.py's child env hides local models unless the caller set the switch, and the whole suite stays green that way — verify with `python3 plugin/tests/run.py test_ci_annotations test_models test_moons_scale test_callcards test_code`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: the child env hides local models by default and keeps a caller's value
2. [x] child_env in run.py; test_models Base pops the switch
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ci_annotations` → ✗ exit 1 · Ran 7 tests in 1.2s (3 jobs, 16 at a time; slowest: ChildEnv 0s, Annotations 0s, SummaryNotes 0s) / FAILED (1 classes: test_ci_annotations.ChildEnv) [ran] [tree 5bf02d1a91f8] [world 2f1906870a] (2026-11-05T18:34:56Z)
- (step 2) `python3 plugin/tests/run.py test_ci_annotations test_models test_moons_scale test_callcards test_code` → exit 0 · Ran 777 tests in 127.8s (464 jobs, 16 at a time; slowest: Fuzz.test_any_event_stream_draws_at_any_size 38s, OutcomeEscalation.test_closes_made_under_another_harness_do_not_count 22s, FollowUp.test_the [ran] [tree 7b97404b87da] [world 2f1906870a] (2026-11-05T18:39:11Z)
- `python3 plugin/tests/run.py test_ci_annotations` → exit 0 · Ran 7 tests in 3.5s (3 jobs, 16 at a time; slowest: ChildEnv 0s, SummaryNotes 0s, Annotations 0s) / OK (start tree + this task's tests) [ran] [tree 9be9403b6693] [world 2f1906870a] (2026-11-05T18:39:17Z)
- `python3 plugin/tests/run.py test_ci_annotations` → exit 0 · Ran 7 tests in 1.0s (3 jobs, 16 at a time; slowest: ChildEnv 0s, SummaryNotes 0s, Annotations 0s) / OK [ran] [tree 9be9403b6693] [world 2f1906870a] (2026-11-05T18:39:17Z)
- (ac 1) `python3 plugin/tests/run.py test_ci_annotations test_models test_moons_scale test_callcards test_code` → exit 0 · Ran 777 tests in 53.8s (438 jobs, 16 at a time; slowest: Fuzz.test_any_event_stream_draws_at_any_size 19s, OutcomeEscalation.test_closes_made_under_another_harness_do_not_count 14s, CodeFakes.test_sil [ran] [tree 9be9403b6693] [world 2f1906870a] (2026-11-05T18:40:24Z)
- (audit intent) `self: child_env keeps every other variable and the caller's explicit value (empty string turns hiding off); test_models' Base pops and restores the switch through KEYS; T-3220's full sweep with the switch on showed only the discovery classes needed it off` → a test leaning on this box's Ollama fails here like on CI [tree 9be9403b6693] (2026-11-05T18:40:24Z)
- (audit edge) `self: child_env keeps every other variable and the caller's explicit value (empty string turns hiding off); test_models' Base pops and restores the switch through KEYS; T-3220's full sweep with the switch on showed only the discovery classes needed it off` → a caller's FOREMAN_NO_LOCAL_MODELS='' keeps local models visible; tests run outside run.py (python -m unittest) behave as before [tree 9be9403b6693] (2026-11-05T18:40:24Z)
- (audit operator) `self: child_env keeps every other variable and the caller's explicit value (empty string turns hiding off); test_models' Base pops and restores the switch through KEYS; T-3220's full sweep with the switch on showed only the discovery classes needed it off` → no change for users; only the test runner's child env [tree 9be9403b6693] (2026-11-05T18:40:24Z)
- (audit self) `self: child_env keeps every other variable and the caller's explicit value (empty string turns hiding off); test_models' Base pops and restores the switch through KEYS; T-3220's full sweep with the switch on showed only the discovery classes needed it off` → no findings [tree 9be9403b6693] (2026-11-05T18:40:24Z)
## Log
- 2026-11-05T18:17:00Z created
- 2026-11-05T18:34:23Z planned: it has criteria and steps
- 2026-11-05T18:34:24Z set scope=['plugin/tests/run.py', 'plugin/tests/test_ci_annotations.py', 'plugin/tests/test_models.py', 'CHANGELOG.md']
- 2026-11-05T18:34:25Z focused
- 2026-11-05T18:34:30Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-05T18:37:01Z set title=The test runner hides local models from every class unless the caller says otherwise, so a run here sees what CI sees
- 2026-11-05T18:40:45Z done
- 2026-11-05T18:40:47Z committed fc487f35 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3220 [FIX S, done, 2 steps] FIX: CI on main is red at fcf658d (tests) — lesson: a test that mocks a picker's fallback but not the picker itself passes only on boxes wi…
- T-3002 [FIX S, blocked, 1 steps] test_moons_scale fakes its embedder, so it passes the same with Ollama down or local models off
- T-2880 [FEATURE M, done, 3 steps] Local model runtime in Sampo's install: install.sh offers (opt-in) Ollama with pinned… — lesson: Discovery that probes a live server ne…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- similar finished tasks took 2–3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
## Regression test
ChildEnv.test_local_models_are_hidden_unless_the_caller_says: red before (step 1 evidence: AttributeError, run has no child_env), green after (step 2). sampo task prove can't split it: run.py lives in plugin/tests, so the start tree gets the new run.py with the tests.
## Why not caught
none: this is the gate T-3220's lesson asked for
## Lessons
- make the local test env match CI's by default instead of adding a second CI-like pass
## Plan gaps
- failed first: step 1 failing test: the child env hides local models by default and keeps a caller's value
## Files touched
- plugin/tests/test_ci_annotations.py
- plugin/tests/run.py
- plugin/tests/test_models.py
- CHANGELOG.md
