---
id: T-2993
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T17:46:53Z
updated: 2026-11-04T17:52:48Z
base: a61fe5db51bae390e7e051d7d52ccabfe872e178
base_tree: ce2cddbe1c20c8c8f20c92fbdf74196425badf8e
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T17:46:54Z
plan0_scope: []
verified: strong
unproven: [data, docs]
---
# The close verifier advises and never blocks a close: models advise, proof decides
## Raw request
> The close verifier advises and never blocks a close: models advise, proof decides
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a live low verifier score prints its ask as advice and the close still lands; task_finish reaches no model layer — verify with `python3 plugin/tests/run.py test_verifier test_models`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] flip the live test to advice-and-close, then route the score through a helper that only prints
## Resume here
## Docs impact
CHANGELOG and files-lib-3 wording
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_verifier test_models` → ✗ exit 1 · Ran 93 tests in 8.5s (18 classes, 16 at a time; slowest: Lake2 8s, Bench 2s, Shadow 2s) / FAILED (2 classes: test_models.ModelRules, test_verifier.Shadow) [ran] [tree 143c19fc9577] [world 2f1906870a] (2026-11-04T17:47:10Z)
- (step 1) `python3 plugin/tests/run.py test_verifier test_models test_bookkeeping` → exit 0 · Ran 115 tests in 9.1s (28 classes, 16 at a time; slowest: Lake2 9s, FinishGaps 5s, CommitOwnFiles 4s) / OK [ran] [tree ca1450979ae9] [world 2f1906870a] (2026-11-04T17:47:44Z)
- `python3 plugin/tests/run.py test_verifier test_models` → ✗ exit 1 · Ran 93 tests in 9.7s (18 classes, 16 at a time; slowest: Lake2 8s, Bench 2s, Shadow 2s) / FAILED (2 classes: test_models.ModelRules, test_verifier.Shadow) (start tree + this task's tests) [ran] [tree 37ca9cffa40a] [world 2f1906870a] (2026-11-04T17:48:26Z)
- `python3 plugin/tests/run.py test_verifier test_models` → exit 0 · Ran 93 tests in 8.6s (18 classes, 16 at a time; slowest: Lake2 8s, Bench 2s, Shadow 2s) / OK [ran] [tree 37ca9cffa40a] [world 2f1906870a] (2026-11-04T17:48:26Z)
- (ac 1) `python3 plugin/tests/run.py test_verifier test_models` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T17:48:26Z [ran] [tree 37ca9cffa40a] [world 2f1906870a] (2026-11-04T17:48:27Z)
- (audit intent) `diff read: _close_advice prints and never raises; the rule test (models advise, proof decides) and the flipped verifier test green; prove red on the start tree, green now` → the standing rule wins over T-2977's original criterion: a model can only advise a close, never stop it [tree 37ca9cffa40a] (2026-11-04T17:48:27Z)
- (audit self) `diff read: _close_advice prints and never raises; the rule test (models advise, proof decides) and the flipped verifier test green; prove red on the start tree, green now` → no findings [tree 37ca9cffa40a] (2026-11-04T17:48:27Z)
## Log
- 2026-11-04T17:46:53Z created
- 2026-11-04T17:46:54Z focused
- 2026-11-04T17:46:54Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T17:52:46Z done
- 2026-11-04T17:52:48Z committed 3f0b0b28 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2489 [FEATURE M, done, 3 steps] Model layer surfaces: MCP decide tool, fm doctor backend health, the site's Model layer… — lesson: README has a 2000-word visible budge…
- T-2395 [FEATURE M, done, 4 steps] Proof surfaces (Mission 7, #6/#10): the rollup by kind on MCP, the pane, fm code, the AGENTS.md block, Desktop through MCP and a site p…
- research brainstorm-20261104-model: Request (T-2973): "should we/could we train a model to fit sampo better? like a better kev/whatever to do more things and more than j…
- decision 2026-11-04: Recommendation: build Sampo's own model family generic across every Sampo project in this order — the training lake (T-2974), a retrieval baseline d…
## Lessons
- A builder brief must carry the standing rules: the verifier was specified to block a close, against 'models advise, proof decides', and only a rule test after the merge caught it
## Plan gaps
- failed first: step 1 flip the live test to advice-and-close, then route the score through a helper that only prints
## Files touched
- plugin/tests/test_verifier.py
- plugin/lib/sampo/cli.py
- CHANGELOG.md
- docs/map/files-lib-3.md
- research/models/bench.jsonl
