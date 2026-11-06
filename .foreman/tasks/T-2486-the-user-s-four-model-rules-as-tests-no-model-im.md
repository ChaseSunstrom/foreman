---
id: T-2486
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-01T17:10:19Z
updated: 2026-11-01T17:46:59Z
base: 5e4f5355305f818df147aeab81fc242bf81b182f
base_tree: f11fe5a0cdceb6a55eadcd43c1c95f9a8e926438
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-01T17:34:07Z
plan0_scope: []
verified: strong
---
# The user's four model rules as tests: no model import in fmguard or the evidence gates,…
## Raw request
> FEATURE: the user's four model rules as tests: no model import in fmguard or the evidence gates, sensitive repos resolve local backends only, backends and downloads only through fm ask --later, no live use without an fm decide row citing its exam
## Interpretation
Readings: (a) each of the user's four model rules gets a check that fails if the rule breaks: a source test that no guard or evidence-gate code calls the model layer; decide() and fm code resolve only local backends for a sensitive project; the model layer has no download or install path of its own (installs go through fm ask --later); a use goes live only by a decision row naming it with its exam numbers, read by one live(p, use) function the uses must call; (b) prose rules in the docs. (a): the user asked for rules a run can't drift from, and each steer becomes a rule plus an automatic check.
## Assumptions (confidence)
## Acceptance criteria
- [x] each of the four model rules has a check that fails when it breaks — verify with `python3 plugin/tests/run.py test_models`
## Non-goals
## Approach (options → choice → why)
1) A test module of rule checks: an AST scan that fmguard.py and fmcore.py never import fmmodels and that fmcli's gate commands (check, gates, task finish and done) never reach decide(); a sensitive-project test for decide() and fm code's backend choice; a scan that fmmodels holds no download, pull or package-install call; fmmodels.live(p, use) true only for a decision row tagged [model-live: USE] that cites exam numbers, with a test. Fails if: a gate gains a model call through an indirect import (the scan follows the gate functions' direct calls only; ponytail: the upgrade is an import-graph walk). 2) Runtime asserts inside the guard. Fails if: it puts model-layer code in the guard, the thing the rule forbids. 3) Use what exists: fm decide rows and their tags (the live switch reads them, as steer checks do), fmcore.read_meta's sensitive flag, test_docs-style source scans. Likely outcome: one test module, one small function. 4) Do less: document the rules. Fails if: nothing fails when one breaks. Choice 1 on 3 (85%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests for the four rules
2. [x] fmmodels.live(p, use) and fm code's sensitive backend choice
3. [x] docs
## Resume here
## Docs impact
MASTER (fmmodels entry), CHANGELOG Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k ModelRules test_models` → ✗ exit 1 · Ran 3 tests in 0.6s (1 classes, 16 at a time; slowest: ModelRules 0s) / FAILED (1 classes: test_models.ModelRules) [ran] [tree 39ff3302d988] (2026-11-01T17:34:37Z)
- `python3 plugin/tests/run.py -k ModelRules test_models` → ✗ exit 1 · Ran 3 tests in 1.5s (1 classes, 16 at a time; slowest: ModelRules 0s) / FAILED (1 classes: test_models.ModelRules) (start tree + this task's tests) [ran] [tree 197d0357112a] (2026-11-01T17:34:58Z)
- `python3 plugin/tests/run.py -k ModelRules test_models` → exit 0 · Ran 3 tests in 0.5s (1 classes, 16 at a time; slowest: ModelRules 0s) / OK [ran] [tree 197d0357112a] (2026-11-01T17:34:58Z)
- (step 2) `python3 plugin/tests/run.py test_models test_code` → exit 0 · Ran 517 tests in 66.8s (107 classes, 16 at a time; slowest: Worker 67s, Fakes 41s, Bench 18s) / OK [ran] [tree 197d0357112a] (2026-11-01T17:36:06Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 103 tests in 8.3s (24 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree 51167e2cd152] (2026-11-01T17:36:21Z)
- (ac 1) `python3 plugin/tests/run.py test_models` → exit 0 · Ran 63 tests in 2.3s (10 classes, 16 at a time; slowest: Bench 2s, RunRoute 1s, OpenAIShape 1s) / OK [ran] [tree 51167e2cd152] (2026-11-01T17:36:24Z)
- (ac 1) `python3 plugin/tests/run.py test_models` → exit 0 · Ran 63 tests in 2.2s (10 classes, 16 at a time; slowest: Bench 2s, RunRoute 1s, OpenAIShape 1s) / OK [ran] [tree 51167e2cd152] (2026-11-01T17:41:42Z)
- (audit intent) `main-thread lens pass over live(), the registry's is_loopback reuse and the three ModelRules tests` → each of the user's four rules now fails a test when broken: no guard or evidence gate reaches the model layer, sensitive projects stay local (decide's test; fm code's T-0784 refusal), the layer downloads nothing, and a use is live only by a decision row citing its exam run [tree 51167e2cd152] (2026-11-01T17:41:42Z)
- (audit adversary) `main-thread lens pass over live(), the registry's is_loopback reuse and the three ModelRules tests` → a 'model-live' row with no exam run id keeps the use in shadow; the newest row wins, so a later 'model-shadow' reverts it; the registry and fm code now share one loopback test [tree 51167e2cd152] (2026-11-01T17:41:42Z)
- (audit edge) `main-thread lens pass over live(), the registry's is_loopback reuse and the three ModelRules tests` → the gate scan follows the gate functions' direct calls only (marked ponytail: an import-graph walk is the upgrade) [tree 51167e2cd152] (2026-11-01T17:41:42Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm ask: text in a file; a run of a documented command proves it (--yes-run) / · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a f [ran] [tree 51167e2cd152] (2026-11-01T17:42:35Z)
## Log
- 2026-11-01T17:10:19Z created
- 2026-11-01T17:23:51Z planned: it has criteria and steps
- 2026-11-01T17:23:51Z set approved=True
- 2026-11-01T17:34:07Z focused
- 2026-11-01T17:34:07Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-01T17:36:21Z scope: plugin/lib/fmmodels.py (live, registry reuses is_loopback), plugin/tests/test_models.py, MASTER.md, CHANGELOG.md
- 2026-11-01T17:42:04Z done
- 2026-11-01T17:42:07Z committed d59dd455 (4 files)
- 2026-11-01T17:42:35Z guard authorization added: publish
- 2026-11-01T17:46:59Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2437 [FEATURE L, done, 5 steps] Gen 2: a model layer (user steer 2026-10-31, start after round 1). (1) A… — lesson: A user's next-generation request has to reach the n…
- T-2471 [FEATURE L, done, 3 steps] Cold read made reliable: Haiku first and Sonnet decides on a non-pass, a FAIL counts only with the quoted line and the MUST/NEVER or st…
- research mission-20261101-105530.pack: (none given: improve the project in every way that matters to its user)
- decision 2026-10-31: Standing rule (user steer 2026-10-31): gen 2 builds a model layer, small specialist models wherever a decision, ranking or lookup is the job, backen…
- similar past tasks were L: consider --tier L
- similar finished tasks took 3–5 steps
## Lessons
- A rule is only standing when a test fails the moment it breaks; prose rules drift
## Plan gaps
- failed first: step 1 red tests for the four rules
## Files touched
- plugin/lib/fmmodels.py
- plugin/tests/test_models.py
- CHANGELOG.md
- MASTER.md
