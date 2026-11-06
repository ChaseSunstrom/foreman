---
id: T-1449
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/lib/fmbus.py, plugin/tests/test_bus.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-22T05:50:55Z
updated: 2026-10-22T05:55:55Z
base: 0876c66b40b6351a1273bf38927d007aa67d621f
base_tree: 476c4804312512947437c352e9246aab51bc7c36
plan0_at: 2026-10-22T05:51:32Z
plan0_scope: [plugin/lib/fmhooks.py, plugin/lib/fmbus.py, plugin/tests/test_bus.py, CHANGELOG.md]
verified: strong
---
# Hook notes survive one failing builder
## Raw request
> Hook notes: one note builder raising (ENOSPC in fmbus.unread's mark write, fmbus.py:92 via _bus_note fmhooks.py:1908) drops every PreToolUse note for that call (one try around the list, fmhooks.py:1712-1720): isolate each builder so one failure loses one note (5 swallowed tracebacks 2026-10-22 04:00, disk full)
## Interpretation
PreToolUse builds its notes in one try; one raising builder (ENOSPC in fmbus.unread's mark) drops every note for that call. Isolate each builder; the bus mark write failing should still show the mail.
## Assumptions (confidence)
## Acceptance criteria
- [x] an out-of-scope note still shows when the bus mark write fails, and the mail itself shows — verify with `cd plugin/tests && python3 -m unittest test_bus.FailingMark`
## Non-goals
## Approach (options → choice → why)
Evaluate each note builder through a small helper that logs and skips a failure; unread() tolerates a failed mark write (mail shows again next call, better than lost).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: bus dir read-only, mail + scope note both show
2. [x] isolate builders in fmhooks, tolerate mark OSError in fmbus
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_bus.FailingMark` → ✗ exit 1 · Ran 1 test in 0.683s / FAILED (failures=1) [ran] [tree df9db1f1d68a] (2026-10-22T05:51:46Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_bus.FailingMark` → exit 0 · Ran 1 test in 0.715s / OK [ran] [tree ed1c16bc990f] (2026-10-22T05:54:34Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_bus.FailingMark` → exit 0 · Ran 1 test in 0.681s / OK [ran] [tree 6df4c2019461] (2026-10-22T05:54:44Z)
- (audit edge) `self: each PreToolUse note builder now runs through _each (logs + skips its own failure); fmbus.unread swallows only OSError on the seen-mark write. Test makes the bus dir read-only (same OSError path as ENOSPC) and asserts both the scope note and the mail show; test_bus + test_hooks green.` → mark failing repeats the mail next call (accepted: transient full disk; better than silent loss) [tree 6df4c2019461] (2026-10-22T05:54:44Z)
- (audit adversary) `self: each PreToolUse note builder now runs through _each (logs + skips its own failure); fmbus.unread swallows only OSError on the seen-mark write. Test makes the bus dir read-only (same OSError path as ENOSPC) and asserts both the scope note and the mail show; test_bus + test_hooks green.` → no guard decision moved — the blocks run before this try; only advisory notes are isolated [tree 6df4c2019461] (2026-10-22T05:54:44Z)
- (audit self) `self: each PreToolUse note builder now runs through _each (logs + skips its own failure); fmbus.unread swallows only OSError on the seen-mark write. Test makes the bus dir read-only (same OSError path as ENOSPC) and asserts both the scope note and the mail show; test_bus + test_hooks green.` → no findings [tree 6df4c2019461] (2026-10-22T05:54:44Z)
## Log
- 2026-10-22T05:50:55Z created
- 2026-10-22T05:51:32Z planned from capture
- 2026-10-22T05:51:32Z focused
- 2026-10-22T05:55:54Z done
- 2026-10-22T05:55:55Z committed 1aefd591 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0087-review: Verdict:** approve with nits. PreToolUse can never be paused, and the pause cannot get stuck or flap. The findings below are all MEDIUM or LOW. […
- T-0087 [FEATURE M, done, 4 steps] Hook circuit breaker: a hook failing 3 times in a row pauses for 10 minutes, shown in the band, dashboard and doctor; the guard never p…
- research T-1065-review: Verdict: changes needed.** Two MEDIUM findings, both about failures breaking normal use. I only read the code. This session had no shell, so I ra…
- decision 2026-10-05: Added Remote Control and worktree-meta facts to the queued isolation-bug feedback draft; marked the background-task cause unconfirmed
- similar past tasks were M: consider --tier M
- likely tests for the scope: plugin/tests/test_bus.py, plugin/tests/test_hooks.py
## Why not caught
no test exercised a failing note builder; the disk filled for the first time
## Lessons
- One try around a list of independent producers turns any one failure into total loss; isolate producers that don't depend on each other.
## Plan gaps
- failed first: step 1 failing test: bus dir read-only, mail + scope note both show
## Files touched
- plugin/tests/test_bus.py
- plugin/lib/fmbus.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
