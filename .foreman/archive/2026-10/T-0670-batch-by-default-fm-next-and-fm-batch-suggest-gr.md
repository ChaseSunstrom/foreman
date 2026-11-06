---
id: T-0670
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:35:23Z
updated: 2026-10-09T15:39:51Z
base: 0a77ebeac88852c84318eee31c34e16ea7536a91
base_tree: ce7a7731b83162fde2809bcbfe327dcf9096b6fc
verified: strong
---
# Batch by default: fm next and fm batch --suggest group related items of any size; batch briefs verify per step with their own tests and run full gates once
## Raw request
> Batch by default: fm next and fm batch --suggest group related items of any size; batch briefs verify per step with their own tests and run full gates once
## Interpretation
User: 'instead of having a bunch of items, put them into one task/milestone, and not test every little change, to save time and tokens, but still able to verify it'. fm batch (T-0257) already makes one host task with one plan, gate run, review and commit, but fm next only offered it for 3+ small same-type captured items, so the guard escapes (L) and brainstorm items (M) were worked one by one, each with full suites and a replay.
## Assumptions (confidence)
## Acceptance criteria
- [x] related items group and unrelated ones don't; fm next offers the group for M items; --apply creates the batches — verify with `python3 plugin/tests/run.py -p test_batch.py`
## Non-goals
## Approach (options → choice → why)
Options: (a) a new milestone object above tasks — a second concept for what fm batch already is; (b) widen fm batch: relatedness by distinctive shared words (words in over a third of candidates are boilerplate) or shared scope, same type, any tier, ≤8 a group; fm next offers it; --suggest/--apply for the whole inbox; the batch brief and the rules state the verify rule (per step: that step's own new tests; full gates, replay and review once at close). Choice: (b).
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: suggest, next offer, apply
2. [x] fmcore.related(): IDF-filtered word overlap or shared scope, same type; next_for offers it; fm batch --suggest/--apply; batch brief + rules line state the verify-once rule
## Resume here
## Docs impact
CHANGELOG; rules line in plugin/rules/foreman.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_batch.py` → ✗ exit 1 · Ran 8 tests in 3.9s (2 classes, 16 at a time; slowest: Batch 4s, Related 2s) / FAILED (1 classes) [ran] [tree fb677cad052d] (2026-10-09T15:35:38Z)
- (step 2) `python3 plugin/tests/run.py -p test_batch.py -p test_hooks.py -p test_cli.py` → exit 0 · Ran 219 tests in 46.6s (36 classes, 16 at a time; slowest: Stop 47s, TaskLifecycle 36s, PreToolUse 28s) / OK [ran] [tree 93f725b649b5] (2026-10-09T15:39:33Z)
- (step 1) `python3 plugin/tests/run.py -k Related` → exit 0 · Ran 3 tests in 3.2s (1 classes, 16 at a time; slowest: Related 3s) / OK [ran] [tree 93f725b649b5] (2026-10-09T15:39:45Z)
- (ac 1) `python3 plugin/tests/run.py -p test_batch.py` → exit 0 · Ran 8 tests in 5.6s (2 classes, 16 at a time; slowest: Batch 6s, Related 3s) / OK [ran] [tree 93f725b649b5] (2026-10-09T15:39:51Z)
- (audit intent) `self: Related tests red then green (suggest groups related only; next offers the group for M items; apply makes batches whose brief states the verify rule); real inbox: 14 groups, 40 items, groups read sensibly (proof/verification; outcomes/learning; stuck/hypotheses); batch, hooks and cli suites green` → the user's batching ask is now Foreman's default path, not a command it has to remember [tree 93f725b649b5] (2026-10-09T15:39:51Z)
- (audit edge) `self: Related tests red then green (suggest groups related only; next offers the group for M items; apply makes batches whose brief states the verify rule); real inbox: 14 groups, 40 items, groups read sensibly (proof/verification; outcomes/learning; stuck/hypotheses); batch, hooks and cli suites green` → a small inbox keeps its shared words (boilerplate floor 8); a loose link can't chain the inbox (greedy, capped at 8); fm next computes one row of pairs per prompt [tree 93f725b649b5] (2026-10-09T15:39:51Z)
## Log
- 2026-10-09T15:35:23Z created
- 2026-10-09T15:35:23Z focused
- 2026-10-09T15:39:51Z done
- 2026-10-09T15:39:51Z committed a7b6b7e (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0257-review: MEDIUM** — `plugin/lib/fmcli.py:540` (host built by `_create`), with the gate at `plugin/lib/fmcore.py:1449`. An explore item (`TAG?:`) is meant …
- T-0257 [PERFORMANCE M, done, 2 steps] fm batch: several small requests worked as one task — one plan, one gate run, one review, one commit — and fm next suggests it — le…
- playbook Strategic Compact Skill (skills/playbooks/references/context/strategic-compact.md)
- decision 2026-10-04: Bench-family inbox items (T-0231 judge, T-0240 duels, T-0241 counterfactual, T-0242 regression court, T-0243 shadow-user soak) are built together as…
- the similar finished task took 2 steps
## Lessons
- an existing capability nobody is offered at the right moment is as good as missing; widen the trigger before building a new concept
## Files touched
- plugin/tests/test_batch.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/rules/foreman.md
- CHANGELOG.md
