---
id: T-2642
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmrelease.py, plugin/tests/test_ship.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-02T19:21:26Z
updated: 2026-11-02T19:47:57Z
builder_model: haiku
route_probe: 1
base: 5e774fa681fa2ddc664b971ea0eae6b305a9f94f
base_tree: 438611fcbac3512ce25f913611e59331fa7e6a2e
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T19:35:18Z
plan0_scope: [plugin/lib/fmrelease.py, plugin/tests/test_ship.py, CHANGELOG.md]
lane_stop: merged 2026-11-02T19:40:39Z
verified: strong
---
# fm ship refuses to push when the tree it would push isn't the tree its tests ran on (an edit or checkout between the gates and the push)
## Raw request
> FEATURE: fm ship asserts the pushed tree hash equals the tree its tests ran against (c09: Self-change rollout, bisect and benchmarks; value 3, effort S, risk low)
> CONTEXT: from the 2 November brainstorm (research/brainstorm-20261102.md, 552 ideas grounded in 59 clusters); each line is a cluster Claude marked build; the user's ticks on the Foreman Idea Triage page re-order them.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a file changed after fm ship's tests pass and before its push makes it refuse with both tree hashes, pushing nothing; an untouched tree ships as before — verify with `python3 plugin/tests/run.py test_ship`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] record HEAD's tree at the gates, compare before the push
3. [x] CHANGELOG
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_ship 2>&1 | tail -15` → exit 0 · Ran 37 tests in 43.0s (1 classes, 16 at a time; slowest: Ship 42s) / OK [ran] [tree f77ecc90561b] [world 2f1906870a] (2026-11-02T19:36:17Z)
- (step 1) `python3 plugin/tests/run.py test_ship 2>&1 | tail -15` → exit 0 · Ran 37 tests in 43.0s (1 classes, 16 at a time; slowest: Ship 42s) / OK [ran] [tree f77ecc90561b] [world 2f1906870a] (2026-11-02T19:36:17Z)
- (step 1) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 37 tests in 39.4s (1 classes, 16 at a time; slowest: Ship 39s) / OK [ran] [tree f77ecc90561b] [world 2f1906870a] (2026-11-02T19:36:59Z)
- (step 2) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 37 tests in 30.2s (1 classes, 16 at a time; slowest: Ship 30s) / OK [ran] [tree f77ecc90561b] [world 2f1906870a] (2026-11-02T19:37:29Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 103 tests in 9.7s (24 classes, 16 at a time; slowest: Fences 9s, DocsProof 3s, TaskLifecycle 2s) / OK [ran] [tree 1c68dd523ead] [world 2f1906870a] (2026-11-02T19:46:00Z)
- (ac 1) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 37 tests in 44.2s (1 classes, 16 at a time; slowest: Ship 44s) / OK [ran] [tree 1c68dd523ead] [world 2f1906870a] (2026-11-02T19:46:46Z)
- (audit edge) `self: builder diff read: the tested tree is HEAD^{tree} of the scratch worktree before the tests and is compared before the fetch and push loop; a re-pick onto a moved main legitimately changes it, so the check sits before that loop` → a test command that commits in the scratch tree is refused with both hashes and the grant kept; uncommitted scratch edits never reach the push [tree 1c68dd523ead] (2026-11-02T19:46:46Z)
- (audit self) `self: builder diff read: the tested tree is HEAD^{tree} of the scratch worktree before the tests and is compared before the fetch and push loop; a re-pick onto a moved main legitimately changes it, so the check sits before that loop` → no findings [tree 1c68dd523ead] (2026-11-02T19:46:46Z)
## Log
- 2026-11-02T19:21:26Z created
- 2026-11-02T19:35:05Z planned from capture
- 2026-11-02T19:35:09Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2642.builder.md
- 2026-11-02T19:35:18Z focused
- 2026-11-02T19:35:18Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T19:40:39Z merged worktree-agent-a221ce413f025f15d (2 file(s))
- 2026-11-02T19:41:58Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a221ce413f025f15d
- 2026-11-02T19:45:48Z focused
- 2026-11-02T19:47:57Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2643 [FEATURE S, planned, 3 steps] fm doctor checks, at most once a day, that each model name Foreman pins (fmgenesis.REVIEW_MODELS, the exam and steer defaults) still…
- T-2657 [FEATURE S, active, 3 steps] flakes.json counts each flaky test's fails and passes; fm doctor lists the three worst by fail rate with the command that flakes them
- T-2641 [FEATURE S, active, 3 steps] A removed fm verb or flag prints its tombstone (what replaced it and the task that removed it) instead of argparse's bare error; firs…
- decision 2026-11-02: brainstorm-20261102 slate: all 552 ideas grounded into 59 clusters (104 built, 249 partial, 197 new, 2 premise-false); the 24 clusters marked build …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_release.py
## Lessons
- Gate on the artifact you ship, not on a step that ran earlier: compare the tree hash the tests saw with the one being pushed
## Files touched
- plugin/tests/test_ship.py
- plugin/lib/fmrelease.py
- CHANGELOG.md
