---
id: T-1452
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-22T05:50:56Z
updated: 2026-10-22T14:23:17Z
base: 218fdc78f0588649abe379227e619a87c3ee3377
base_tree: 6a3af19f1fdd243268876319fad8f4b096ef40b4
plan0_at: 2026-10-22T14:21:16Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
verified: strong
---
# Brief refusal of a CHANGELOG edit says where the line goes
## Raw request
> The brief guard's refusal of a CHANGELOG.md edit with no active task says only the generic text (fmguard.py:220-223): name the way on (edit it before fm task finish, or fm task new … --focus); 3× this window
## Interpretation
A CHANGELOG.md edit with no active task gets the generic 'start a task' text; the line belongs to the task it describes (3 blocks this window, mine, after a close).
## Assumptions (confidence)
## Acceptance criteria
- [x] a CHANGELOG.md edit with no active task is refused naming fm task finish and fm focus — verify with `cd plugin/tests && python3 -m unittest test_guard.BriefChangelog`
## Non-goals
## Approach (options → choice → why)
In the brief refusal, when the path is a CHANGELOG.md, add: a changelog line belongs to its task: add it before fm task finish, or fm focus that task again; fm release writes the release header itself.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] hint in the brief refusal
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_guard.BriefChangelog` → ✗ exit 1 · Ran 1 test in 0.079s / FAILED (failures=1) [ran] [tree fa9b580c6b8c] (2026-10-22T14:21:18Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_guard.BriefChangelog` → exit 0 · Ran 1 test in 0.080s / OK [ran] [tree abeb02046821] (2026-10-22T14:21:20Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard.BriefChangelog` → exit 0 · Ran 1 test in 0.089s / OK [ran] [tree 455c1d1060b1] (2026-10-22T14:21:32Z)
- (audit adversary) `self: one hint in _hint for category brief when the path's basename is CHANGELOG.md; test checks the hint and that another file doesn't get it; test_guard.BriefChangelog green.` → message text only; no decision changes [tree 455c1d1060b1] (2026-10-22T14:21:32Z)
- (audit self) `self: one hint in _hint for category brief when the path's basename is CHANGELOG.md; test checks the hint and that another file doesn't get it; test_guard.BriefChangelog green.` → no findings [tree 455c1d1060b1] (2026-10-22T14:21:32Z)
## Log
- 2026-10-22T05:50:56Z created
- 2026-10-22T14:19:51Z planned from capture
- 2026-10-22T14:21:15Z focused
- 2026-10-22T14:23:16Z done
- 2026-10-22T14:23:17Z committed dea9379b (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- T-1074 [FEATURE M, done, 3 steps] Hotspots in plans: files that keep getting fixed after edits are flagged in the plan and a — lesson: A history signal needs a cap on sw…
- decision 2026-10-15: Recommendation: close the gaps where a small model has to guess a command (done: T-0969, T-0985, T-0986, T-0987); no separate small-model mode or MC…
- likely tests for the scope: plugin/tests/test_guard.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md; re-ground the plan against them before editing
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/lib/fmguard.py
- plugin/tests/test_guard.py
- CHANGELOG.md
