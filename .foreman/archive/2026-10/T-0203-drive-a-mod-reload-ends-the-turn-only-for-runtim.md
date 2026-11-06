---
id: T-0203
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-04T04:07:02Z
updated: 2026-10-04T04:16:30Z
base: ceb9fe6ef8efadbda58a3ae11d49219e887361bb
base_tree: 880cb93cfa98a0c7906100287f8bcf885f164a41
verified: strong
---
# Drive: a mod's tests and docs changing don't end the turn for a reload
## Raw request
> Drive: a mod reload ends the turn only for runtime mod files — _ui_changed (fmhooks.py:1416) counts tests/ and docs under dev-mods too
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a change under a mod's tests/ or to a .md file keeps the drive going; a hooks/ change still ends the turn — verify with `python3 plugin/tests/run.py -k test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test first, then skip tests/ and docs in _ui_changed
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k test_hooks` → ✗ exit 1 · Ran 121 tests in 13.4s (20 classes, 16 at a time; slowest: Stop 13s, Approvals 9s, PromptApprovals 7s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 6a4be9d1760a] (2026-10-04T04:15:16Z)
- `python3 plugin/tests/run.py -k test_hooks` → exit 0 · Ran 121 tests in 13.3s (20 classes, 16 at a time; slowest: Stop 13s, Approvals 9s, PromptApprovals 7s) / OK [ran] [tree 6a4be9d1760a] (2026-10-04T04:15:16Z)
- (step 1) `python3 plugin/tests/run.py -k test_hooks` → exit 0 · Ran 121 tests in 13.4s (20 classes, 16 at a time; slowest: Stop 13s, Approvals 9s, PromptApprovals 7s) / OK [ran] [tree 6a4be9d1760a] (2026-10-04T04:15:33Z)
- (ac 1) `python3 plugin/tests/run.py -k test_hooks` → exit 0 · Ran 121 tests in 13.3s (20 classes, 16 at a time; slowest: Stop 13s, Approvals 9s, PromptApprovals 7s) / OK [ran] [tree 6a4be9d1760a] (2026-10-04T04:16:27Z)
- (audit self) `self checklist` → pass [tree 6a4be9d1760a] (2026-10-04T04:16:27Z)
- (audit self) `self checklist` → pass [tree 6a4be9d1760a] (2026-10-04T04:16:29Z)
## Log
- 2026-10-04T04:07:02Z created
- 2026-10-04T04:14:41Z planned from capture
- 2026-10-04T04:14:41Z focused
- 2026-10-04T04:16:30Z done
- 2026-10-04T04:16:30Z committed 329d181 (2 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0145 [FEATURE M, done, 3 steps] UI changes reach the running session during a drive: the Stop hook ends the turn once when this session's dev-mods changed, and the rel…
- T-0147 [FIX S, done, 1 steps] Stop: a turn that ends on purpose for a mod reload isn't blocked by the evidence or question nudge — lesson: A gate meant to catch prematur…
- research brainstorm-20261003-round5: Quota brake (bold bets) → T-0198 economy mode: the mod reads session.usage rate limits; past 80% weekly / 90% 5-hour a prompt.compos…
- T-0121 [FIX M, done, 3 steps] A subagent that ended without its finish event stays 'running' for hours in the dashboard — lesson: Never derive 'still running' from the a…
## Measurements
turn ends for a reload after editing only a mod's tests/ or a .md: 1 → 0 per edit (test_hooks Reload case drives Stop after each touch)
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
