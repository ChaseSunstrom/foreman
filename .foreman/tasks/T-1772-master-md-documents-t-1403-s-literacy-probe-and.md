---
id: T-1772
type: CLEAN
tier: S
status: done
priority: normal
scope: [MASTER.md]
depends_on: []
source: user
created: 2026-10-23T10:15:21Z
updated: 2026-10-23T10:15:50Z
base: 21b9d80a5f823158d136192e8df69639030b9d50
base_tree: c8a5f0e87649048edfd01f8984e2cc081afbffaa
plan0_at: 2026-10-23T10:15:22Z
plan0_scope: [MASTER.md]
verified: strong
---
# MASTER.md documents T-1403's literacy probe and bench prompt variants
## Raw request
> MASTER.md documents T-1403's literacy probe and bench prompt variants
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] MASTER.md names fm code runners --probe and bench --variants — verify with `grep -q 'runners --probe MODEL' MASTER.md`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] add the bullet
## Resume here
## Docs impact
## Verification evidence
- (step 1) `grep -q 'runners --probe MODEL' MASTER.md && python3 plugin/tests/run.py test_docs` → exit 0 · Ran 69 tests in 8.6s (17 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 39a05e33cecd] (2026-10-23T10:15:37Z)
- (ac 1) `grep -q 'runners --probe MODEL' MASTER.md` → exit 0 · (no output) [ran] [tree 39a05e33cecd] (2026-10-23T10:15:47Z)
- (audit edge) `self review; test_docs green` → the bullet sits before the Offers bullet, beside the other fm code features of this round [tree 39a05e33cecd] (2026-10-23T10:15:47Z)
- (audit self) `self review; test_docs green` → no findings [tree 39a05e33cecd] (2026-10-23T10:15:47Z)
## Log
- 2026-10-23T10:15:21Z created
- 2026-10-23T10:15:22Z focused
- 2026-10-23T10:15:49Z done
- 2026-10-23T10:15:50Z committed 2dc7938a (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1403 [FEATURE M, done, 1 steps] Model literacy probe: fm code runners --probe scores a model 0-10 on ten small graded prom — lesson: Grade a model's format literacy wi…
- T-0175 [SECURITY L, done, 3 steps] Guard: writes through a variable are checked — known NAME=literal values and $HOME resolve write, copy and cd targets (&& chains too);…
- T-0190 [FIX M, done, 3 steps] Guard: guesses never use a variable's own name; rm targets use literals set once before a branch — lesson: A replay gate turns a guard chan…
- decision 2026-10-15: Recommendation: close the gaps where a small model has to guess a command (done: T-0969, T-0985, T-0986, T-0987); no separate small-model mode or MC…
## Behaviour lock
none: a MASTER.md bullet only; no code changed (test_docs ran after it)
## Files touched
- MASTER.md
