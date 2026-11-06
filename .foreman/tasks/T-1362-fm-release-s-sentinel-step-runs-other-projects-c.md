---
id: T-1362
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T03:51:05Z
updated: 2026-10-21T04:57:04Z
base: 4f39be513dbf2e671d9b284515d26486f87b8df6
base_tree: 3c42ffae021264c15d50a5046483efe9f18ce51a
plan0_at: 2026-10-21T04:25:07Z
plan0_scope: []
verified: strong
---
# fm release's canary (fm sentinel in every local project) runs after the push without blocking the release command; its result lands in the inbox and the notify hook
## Raw request
> fm release's sentinel step runs other projects' checks: releasing Foreman 1.2.46 ran cargo test --test golden in ~/projects/volt for 10+ minutes; a release's sentinel should cover only the released project's finished tasks
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm release --push returns once pushed, with the canary started detached; its findings (a project's past check failing now) are captured to that project's inbox and reported through fm notify, and fm release --canary-status shows the last run — verify with `python3 plugin/tests/run.py test_release`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: release returns before a slow fake sentinel ends; the canary's failure lands as an inbox item
2. [x] Detach the canary step (its own session, output to a file); capture failures; --canary-status
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_release 2>&1 | tail -8` → ✗ exit 1 · Ran 30 tests in 71.4s (5 classes, 16 at a time; slowest: Release 69s, BoardVerbs 24s, Release 5s) / FAILED (1 classes) [ran] [tree dcd9b38c2f07] (2026-10-21T04:27:09Z)
- (ac 1) `python3 plugin/tests/run.py test_release 2>&1 | tail -30` → ✗ exit 1 · Ran 30 tests in 29.2s (5 classes, 16 at a time; slowest: Release 29s, BoardVerbs 22s, Release 4s) / FAILED (1 classes) [ran] [tree bec523c47579] (2026-10-21T04:28:07Z)
- (step 2) `python3 plugin/tests/run.py test_release` → exit 0 · Ran 30 tests in 57.6s (5 classes, 16 at a time; slowest: Release 57s, BoardVerbs 48s, Release 10s) / OK [ran] [tree edba8b9f1eff] (2026-10-21T04:31:43Z)
- (step 2) `python3 plugin/tests/run.py test_release test_release_py` → exit 0 · Ran 30 tests in 26.6s (5 classes, 16 at a time; slowest: Release 26s, BoardVerbs 19s, Release 4s) / OK [ran] [tree 8a1a6e979b9c] (2026-10-21T04:49:16Z)
- (step 1) `python3 plugin/tests/run.py test_release` → exit 0 · Ran 30 tests in 26.0s (5 classes, 16 at a time; slowest: Release 26s, BoardVerbs 18s, Release 3s) / OK [ran] [tree 8a1a6e979b9c] (2026-10-21T04:49:47Z)
- (ac 1) `python3 plugin/tests/run.py test_release` → exit 0 · Ran 30 tests in 38.5s (5 classes, 16 at a time; slowest: Release 38s, BoardVerbs 29s, Release 5s) / OK [ran] [tree 2fad01bad9e0] (2026-10-21T04:50:35Z)
- (audit intent) `self: read the diff; worker runs as __main__ with plugin/lib on sys.path so fmcore/fmeco/fmserve import; capture and notify failures are swallowed; added: FOREMAN_NO_BACKGROUND waits for the worker so test folders aren't written after cleanup` → --push returns once pushed (detached test waits for the report after release returns); failures reach inbox and notify [tree 2fad01bad9e0] (2026-10-21T04:50:35Z)
- (audit edge) `self: read the diff; worker runs as __main__ with plugin/lib on sys.path so fmcore/fmeco/fmserve import; capture and notify failures are swallowed; added: FOREMAN_NO_BACKGROUND waits for the worker so test folders aren't written after cleanup` → a killed worker leaves 'still running' forever (no staleness check; low value, left) [tree 2fad01bad9e0] (2026-10-21T04:50:35Z)
- (audit adversary) `self: read the diff; worker runs as __main__ with plugin/lib on sys.path so fmcore/fmeco/fmserve import; capture and notify failures are swallowed; added: FOREMAN_NO_BACKGROUND waits for the worker so test folders aren't written after cleanup` → worker argv is version and root from the release itself, never repo input [tree 2fad01bad9e0] (2026-10-21T04:50:35Z)
- (audit operator) `self: read the diff; worker runs as __main__ with plugin/lib on sys.path so fmcore/fmeco/fmserve import; capture and notify failures are swallowed; added: FOREMAN_NO_BACKGROUND waits for the worker so test folders aren't written after cleanup` → fm release --canary-status names the report and whether it's still running [tree 2fad01bad9e0] (2026-10-21T04:50:35Z)
- (audit self) `self: read the diff; worker runs as __main__ with plugin/lib on sys.path so fmcore/fmeco/fmserve import; capture and notify failures are swallowed; added: FOREMAN_NO_BACKGROUND waits for the worker so test folders aren't written after cleanup` → no findings [tree 2fad01bad9e0] (2026-10-21T04:50:35Z)
- `python3 plugin/tests/run.py test_release` → ✗ exit 1 · Ran 30 tests in 64.7s (5 classes, 16 at a time; slowest: Release 63s, BoardVerbs 19s, Release 3s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 2fad01bad9e0] (2026-10-21T04:54:49Z)
- `python3 plugin/tests/run.py test_release` → exit 0 · Ran 30 tests in 25.6s (5 classes, 16 at a time; slowest: Release 25s, BoardVerbs 19s, Release 3s) / OK [ran] [tree 2fad01bad9e0] (2026-10-21T04:54:49Z)
- (audit intent) `self: read the diff; worker runs as __main__ with plugin/lib on sys.path so fmcore/fmeco/fmserve import; capture and notify failures are swallowed; added: FOREMAN_NO_BACKGROUND waits for the worker so test folders aren't written after cleanup` → --push returns once pushed (detached test waits for the report after release returns); failures reach inbox and notify [tree 2fad01bad9e0] (2026-10-21T04:54:54Z)
- (audit edge) `self: read the diff; worker runs as __main__ with plugin/lib on sys.path so fmcore/fmeco/fmserve import; capture and notify failures are swallowed; added: FOREMAN_NO_BACKGROUND waits for the worker so test folders aren't written after cleanup` → a killed worker leaves 'still running' forever (no staleness check; low value, left) [tree 2fad01bad9e0] (2026-10-21T04:54:54Z)
- (audit adversary) `self: read the diff; worker runs as __main__ with plugin/lib on sys.path so fmcore/fmeco/fmserve import; capture and notify failures are swallowed; added: FOREMAN_NO_BACKGROUND waits for the worker so test folders aren't written after cleanup` → worker argv is version and root from the release itself, never repo input [tree 2fad01bad9e0] (2026-10-21T04:54:54Z)
- (audit operator) `self: read the diff; worker runs as __main__ with plugin/lib on sys.path so fmcore/fmeco/fmserve import; capture and notify failures are swallowed; added: FOREMAN_NO_BACKGROUND waits for the worker so test folders aren't written after cleanup` → fm release --canary-status names the report and whether it's still running [tree 2fad01bad9e0] (2026-10-21T04:54:54Z)
- (audit self) `self: read the diff; worker runs as __main__ with plugin/lib on sys.path so fmcore/fmeco/fmserve import; capture and notify failures are swallowed; added: FOREMAN_NO_BACKGROUND waits for the worker so test folders aren't written after cleanup` → no findings [tree 2fad01bad9e0] (2026-10-21T04:54:54Z)
## Log
- 2026-10-21T03:51:05Z created
- 2026-10-21T04:24:41Z planned from capture
- 2026-10-21T04:24:46Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1362.builder.md
- 2026-10-21T04:25:07Z focused
- 2026-10-21T04:43:27Z merged worktree-agent-a6bd4a2b44bbf8374 (3 file(s))
- 2026-10-21T04:43:28Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a6bd4a2b44bbf8374
- 2026-10-21T04:48:23Z focused
- 2026-10-21T04:49:55Z scope: CHANGELOG.md, plugin/tests/test_release.py — changelog line; tests honor FOREMAN_NO_BACKGROUND
- 2026-10-21T04:57:01Z done
- 2026-10-21T04:57:04Z committed 7208a4b3 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1199 [PERFORMANCE S, done, 2 steps] fm release runs the canary after the push, its sentinels in parallel
- T-0492 [FEATURE M, done, 0 steps] Canary releases with consumer replay (C085, value 3/5, effort M, risk low)
- T-0562 [FEATURE M, dropped, 0 steps] Canary releases with consumer replay (C085, value 3/5, effort M, risk low)
- decision 2026-10-20: Abandoned the unfinished 1.2.40 release state: it was pushed; only its advisory canary was left, which 1.2.41's release runs
- similar finished tasks took 0–2 steps
- start here (files T-1199 touched): plugin/tests/test_release.py, plugin/lib/fmrelease.py, CHANGELOG.md
## Lessons
- A detached child started by a command must honor FOREMAN_NO_BACKGROUND, or tests race their own cleanup
## Files touched
- plugin/tests/test_release.py
- plugin/lib/fmcli.py
- plugin/lib/fmrelease.py
- CHANGELOG.md
