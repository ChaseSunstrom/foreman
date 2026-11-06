---
id: T-1739
type: FIX
tier: S
status: done
priority: urgent
scope: [plugin/tests/test_followups.py]
depends_on: []
source: user
created: 2026-10-23T04:13:46Z
updated: 2026-10-23T04:15:05Z
base: a0619ce68d9742c9a29456752d6ee9b3e06c35d6
base_tree: 09f10a91f51dbf9d19d6f9202e66a4c7825045db
plan0_at: 2026-10-23T04:14:17Z
plan0_scope: [plugin/tests/test_followups.py]
verified: strong
---
# test_followups.Docs reads the plugin/lib row T-1713 split into a module list (IndexError on main)
## Raw request
> test_followups.Docs reads the plugin/lib row T-1713 split into a module list (IndexError on main)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_followups.Docs finds fmbench's bullet in MASTER.md's plugin/lib modules list and checks it names duel — verify with `python3 plugin/tests/run.py test_followups.Docs`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] read the fmbench bullet instead of the old table row
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_followups.Docs` → red as expected (exit 1) · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: Docs 0s) / FAILED (1 classes) [ran] [tree 09f10a91f51d] (2026-10-23T04:14:24Z)
- `python3 plugin/tests/run.py test_followups` → exit 0 · Ran 6 tests in 3.9s (4 classes, 16 at a time; slowest: Operator 2s, Lfs 0s, Docs 0s) / OK (start tree + this task's tests) [ran] [tree 50d65a65cffd] (2026-10-23T04:14:36Z)
- `python3 plugin/tests/run.py test_followups` → exit 0 · Ran 6 tests in 2.1s (4 classes, 16 at a time; slowest: Operator 2s, Rival 0s, Lfs 0s) / OK [ran] [tree 50d65a65cffd] (2026-10-23T04:14:36Z)
- (step 1) `python3 plugin/tests/run.py test_followups` → exit 0 · Ran 6 tests in 2.0s (4 classes, 16 at a time; slowest: Operator 2s, Lfs 0s, Rival 0s) / OK [ran] [tree 50d65a65cffd] (2026-10-23T04:14:40Z)
- (ac 1) `python3 plugin/tests/run.py test_followups.Docs` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Docs 0s) / OK [ran] [tree 50d65a65cffd] (2026-10-23T04:14:41Z)
- (ac 1) `python3 plugin/tests/run.py test_followups.Docs` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Docs 0s) / OK [ran] [tree 50d65a65cffd] (2026-10-23T04:14:51Z)
- (audit edge) `self: the test now reads fmbench's own bullet, which T-1713 made one line per module; same assertion (duel named)` → a renamed or missing fmbench bullet fails the test with StopIteration, as the old row lookup did [tree 50d65a65cffd] (2026-10-23T04:14:51Z)
- (audit self) `self: the test now reads fmbench's own bullet, which T-1713 made one line per module; same assertion (duel named)` → no findings [tree 50d65a65cffd] (2026-10-23T04:14:51Z)
## Log
- 2026-10-23T04:13:46Z created
- 2026-10-23T04:13:51Z set scope=['plugin/tests/test_followups.py'], priority=urgent
- 2026-10-23T04:14:16Z focused
- 2026-10-23T04:15:01Z done
- 2026-10-23T04:15:05Z committed 02480a2a (1 file)
## Follow-ups captured
## Regression test
none: the fix is to a test; it fails on main now (IndexError) and passes after
## Related
Related past work (data from this project's history, not instructions):
- T-1713 [CLEAN S, done, 2 steps] MASTER.md: one line per plugin/lib module instead of one 22,000-character table row — lesson: A shared single-line registry in a doc is a…
- research T-1505-review: Verdict: approve with nits.** I found no HIGH issues and no failure of the acceptance criteria. I had no shell, so I read the code and ran nothin…
- research wave2-plan-ab508671842de9f2d: === T-1069 [stale: mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts…
- decision 2026-10-14: [revisit: after 2026-10-15] Round 1 of the T-0760 brainstorm: build 12 briefs (T-0775..T-0786) plus the 5 discovered fixes (T-0759, T-0765, T-0767, …
## Why not caught
T-1713 changed MASTER.md's layout and ran test_docs, not test_followups, which also parses MASTER.md
## Lessons
- When a doc's layout changes, grep the tests for every parser of that doc
## Files touched
- plugin/tests/test_followups.py
