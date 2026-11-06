---
id: T-2566
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T07:39:22Z
updated: 2026-11-02T07:54:02Z
base: 5c549eebdd6d1a40f6267fed7a89bce5cda9d2d1
base_tree: 73e34c472cc93d3439b0a15294299ec02c8c9160
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T07:39:23Z
plan0_scope: []
verified: strong
---
# fm genesis select ignores exam lines answered only on the held-out split, so a run with no train answers never decides a keep or revert
## Raw request
> fm genesis select ignores exam lines answered only on the held-out split, so a run with no train answers never decides a keep or revert
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a line with split holdout never counts in select or confirm: gen n with only such lines asks for a train run; a parent with only such lines leaves gen n the baseline; a tie on train-empty lines no longer reverts — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_genesis
2. [x] filter in _compare
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisSelect` → ✗ exit 1 · Ran 20 tests in 3.8s (1 classes, 16 at a time; slowest: GenesisSelect 4s) / FAILED (1 classes: test_genesis.GenesisSelect) [ran] [tree c14cf61b05b1] [world 2f1906870a] (2026-11-02T07:39:44Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis 2>&1 | grep -E "^(ERROR|FAIL):|^OK|FAILED" | head -6` → exit 0 · OK [ran] [tree a61a04b65de8] [world 2f1906870a] (2026-11-02T07:40:09Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 209 tests in 16.0s (24 classes, 16 at a time; slowest: GenerationReview 14s, ProofBeforePresentation 13s, GenesisRead 12s) / OK [ran] [tree a61a04b65de8] [world 2f1906870a] (2026-11-02T07:40:37Z)
- `python3 plugin/tests/run.py test_genesis.GenesisSelect` → ✗ exit 1 · Ran 20 tests in 3.1s (1 classes, 16 at a time; slowest: GenesisSelect 2s) / FAILED (1 classes: test_genesis.GenesisSelect) (start tree + this task's tests) [ran] [tree 968f70c1c7a3] [world 2f1906870a] (2026-11-02T07:46:34Z)
- `python3 plugin/tests/run.py test_genesis.GenesisSelect` → exit 0 · Ran 20 tests in 2.1s (1 classes, 16 at a time; slowest: GenesisSelect 2s) / OK [ran] [tree 968f70c1c7a3] [world 2f1906870a] (2026-11-02T07:46:34Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 209 tests in 15.6s (24 classes, 16 at a time; slowest: GenerationReview 14s, ProofBeforePresentation 12s, GenesisRead 12s) / OK [ran] [tree 968f70c1c7a3] [world 2f1906870a] (2026-11-02T07:46:50Z)
- (audit intent) `self-review: the filter sits in _compare, which select and confirm share; holdout-split lines drop before kid/mom; legacy lines without a split stay counted; message names --split train` → a held-out-only line never decides select or confirm; gen n with only such lines is refused with the train-run ask; a parent with only such lines leaves gen n the baseline (test) [tree 968f70c1c7a3] (2026-11-02T07:46:50Z)
- (audit edge) `self-review: the filter sits in _compare, which select and confirm share; holdout-split lines drop before kid/mom; legacy lines without a split stay counted; message names --split train` → lines with no split field (pre-stamp) still count; split all counts; an empty filtered list raises the train-split message, which test_genesis pins with 'train' [tree 968f70c1c7a3] (2026-11-02T07:46:50Z)
- (audit self) `self-review: the filter sits in _compare, which select and confirm share; holdout-split lines drop before kid/mom; legacy lines without a split stay counted; message names --split train` → no findings [tree 968f70c1c7a3] (2026-11-02T07:46:50Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 99f6c41ab9b3] [world 2f1906870a] (2026-11-02T07:48:04Z)
## Log
- 2026-11-02T07:39:22Z created
- 2026-11-02T07:39:22Z focused
- 2026-11-02T07:39:23Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T07:47:20Z done
- 2026-11-02T07:47:22Z committed 8d8884ae (3 files)
- 2026-11-02T07:48:04Z guard authorization added: publish
- 2026-11-02T07:54:02Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- T-2158 [FEATURE M, done, 2 steps] Haiku scores are smoke signals only: fm exam scorecard, fm genesis select and the done… — lesson: A line that records what produced it …
- decision 2026-10-30: Genesis selection (fm genesis select) scores the exam's train split, never the held-out third; held-out only grades a capability done
- research T-2097-review: Verdict** — approve with nits. The scorecard logic is correct on the cases I traced. The real `fm genesis exam` path that feeds #13 has no test. …
- similar past tasks were M: consider --tier M
## Lessons
- A comparison that can only tie (both sides scored on a split that holds none of the counted items) must refuse, not decide: check the counted population is non-empty before reading a 0-0
## Plan gaps
- failed first: step 1 red test in test_genesis
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
