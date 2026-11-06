---
id: T-0114
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_queue_preview.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-03T03:05:24Z
updated: 2026-10-03T08:47:48Z
base: 102164a469269632436b79f7ae36bfca801151f5
base_tree: 95fff8b1d41023974adbc11d8df2602655e4f987
verified: ok
---
# fm queue --preview: usual time per item and what will need the user, gathered to answer at once
## Raw request
> Overnight dry run of the queue in a throwaway worktree
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm queue --preview lists queued and inbox items with this project's usual minutes for their type and size, and names what needs the user under the current autonomy (an L plan in standard; none in full), gathered in one list — verify with `python3 plugin/tests/run.py -k test_queue_preview`
- [x] All gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test
2. [x] Preview in fm queue
3. [x] MASTER and CHANGELOG
## Resume here
## Docs impact
MASTER (Queue preview) and CHANGELOG.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_queue_preview` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: QueuePreview 1s) / OK [ran] [tree b2606532a8bb] (2026-10-03T08:47:40Z)
- (step 2) `python3 plugin/tests/run.py -k test_queue_preview` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: QueuePreview 1s) / OK [ran] [tree b2606532a8bb] (2026-10-03T08:47:41Z)
- (step 3) `grep -q T-0114 MASTER.md && grep -q T-0114 CHANGELOG.md` → exit 0 · (no output) [ran] [tree b2606532a8bb] (2026-10-03T08:47:41Z)
- (ac 1) `python3 plugin/tests/run.py -k test_queue_preview` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: QueuePreview 1s) / OK [ran] [tree b2606532a8bb] (2026-10-03T08:47:48Z)
- (ac 2) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 08:47 UTC); cached (fm check --fresh reruns) [ran] [tree b2606532a8bb] (2026-10-03T08:47:48Z)
- (audit self) `self: the test covers usual minutes with and without history, an L plan needing a yes in standard and not in full, a plain S needing nothing, and the asks listed first; a core yes is predicted from scope with the guard's own classify_write and dropped when a standing yes exists; the active task is left out (it's being worked)` → no findings [tree b2606532a8bb] (2026-10-03T08:47:48Z)
## Log
- 2026-10-03T03:05:24Z created
- 2026-10-03T08:46:30Z planned from capture
- 2026-10-03T08:46:30Z focused
- 2026-10-03T08:47:48Z done
- 2026-10-03T08:47:48Z committed 70433f7 (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261002-super: 171 titles (6 lenses × 2 rounds + 3 deepen rounds: speed, gates, autonomy). Grounded against the code:
- research t0071-fg-review: Each piece does what it claims end-to-end (verified by reading each call site): the mtime union in `fm task done` (fmcli.py:219-226), `--fail-f…
- T-0134 [FEATURE L, done, 5 steps] Lanes: a git worktree is a lane of its project with its own active task — lesson: When a 'single X per project' rule becomes 'per lane'…
- research T-0134-review: Verdict: changes needed.** One finding is a real wrong-view bug and one is a real data-loss gap. The rest are lower.
- similar past tasks were L: consider --tier L
- the similar finished task took 5 steps
## Preflight
Changed in scope since this was planned (2026-10-03): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py; re-ground the plan against them before editing
## Lessons
- The brainstorm's 'overnight dry run' was really 'know what will need me before I leave': answer the need with existing data (typical times, waits_on_user, the guard's classifier) before building a simulator.
## Files touched
- plugin/tests/test_queue_preview.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
