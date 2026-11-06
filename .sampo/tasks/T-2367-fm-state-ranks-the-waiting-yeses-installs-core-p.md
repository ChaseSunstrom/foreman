---
id: T-2367
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T14:01:20Z
updated: 2026-11-01T22:29:33Z
group: Mission 8 surfaces
base: ad98d29af6cecf1b0315ef29e840a8d96c4e7991
base_tree: 665546f7b6a493d63ac6f15c94fbb9493b402827
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-11-01T22:17:24Z
plan0_scope: []
verified: strong
---
# fm state ranks the waiting yeses by the open work each one unblocks
## Raw request
> fm state ranks the waiting yeses (installs, core, plugins) by the work each one unlocks (Mission 8 inbox, tier 2)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fmgrants.line and fm todo list queued grants most-unblocking first (the task plus the open tasks waiting on it, transitively), oldest first on a tie — verify with `python3 plugin/tests/run.py test_tool_queue`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: two queued grants, the newer one unblocks two waiting tasks, so it lists first in fm state's line and fm todo
2. [x] fmgrants.ranked(p, briefs) sorts queued() by unblocked count; line() and cmd_todo use it
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_tool_queue.GrantQueue.test_the_waiting_yeses_rank_by_the_open_work_each_unblocks` → ✗ exit 1 · Ran 1 tests in 2.8s (1 classes, 16 at a time; slowest: GrantQueue 2s) / FAILED (1 classes: test_tool_queue.GrantQueue) [ran] [tree ad557d133bb8] (2026-11-01T22:17:58Z)
- (step 1) `python3 plugin/tests/run.py test_tool_queue.GrantQueue.test_the_waiting_yeses_rank_by_the_open_work_each_unblocks` → exit 0 · Ran 1 tests in 3.3s (1 classes, 16 at a time; slowest: GrantQueue 3s) / OK [ran] [tree e54036e46bed] (2026-11-01T22:18:48Z)
- (step 2) `python3 plugin/tests/run.py test_tool_queue test_mcp` → exit 0 · Ran 49 tests in 16.8s (16 classes, 16 at a time; slowest: GrantQueue 16s, McpNew 4s, McpTools 3s) / OK [ran] [tree e54036e46bed] (2026-11-01T22:19:05Z)
- (ac 1) `python3 plugin/tests/run.py test_tool_queue` → exit 0 · Ran 20 tests in 13.9s (1 classes, 16 at a time; slowest: GrantQueue 14s) / OK [ran] [tree 5892e7eddd20] (2026-11-01T22:28:54Z)
- (audit edge) `self-review: ranked() is a stable sort of queued() (already oldest first) by the size of _freed, so ties keep the oldest first; _freed walks open briefs' depends_on (stored as a list: LIST_FIELDS) with a seen set, so a dependency cycle ends; closed waiters don't count; fm todo, the waiting line and the MCP list now share one order, and queued()'s other callers (counts in fmtriggers) are unchanged` → a cycle A↔B terminates; a closed waiter is not counted; two grants on one task both rank with it; ties stay oldest first [tree 5892e7eddd20] (2026-11-01T22:28:54Z)
- (audit self) `self-review: ranked() is a stable sort of queued() (already oldest first) by the size of _freed, so ties keep the oldest first; _freed walks open briefs' depends_on (stored as a list: LIST_FIELDS) with a seen set, so a dependency cycle ends; closed waiters don't count; fm todo, the waiting line and the MCP list now share one order, and queued()'s other callers (counts in fmtriggers) are unchanged` → no findings [tree 5892e7eddd20] (2026-11-01T22:28:54Z)
## Log
- 2026-10-31T14:01:20Z created
- 2026-11-01T19:15:50Z planned from capture
- 2026-11-01T22:17:24Z focused
- 2026-11-01T22:17:24Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-11-01T22:17:44Z criterion 1 verify: `python3 plugin/tests/run.py test_grants` → `python3 plugin/tests/run.py test_tool_queue`
- 2026-11-01T22:19:05Z scope: fmmcp's waiting-yeses list ranks too (one word), so every surface lists the same order
- 2026-11-01T22:29:31Z done
- 2026-11-01T22:29:33Z committed 24fef522 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2357 [FEATURE M, done, 3 steps] Installs are queued for one yes: night and tick timers staged, asked once, installed only after the user's yes (Mission 8, #11) — lesso…
- T-2347 [FEATURE S, done, 2 steps] Price a parked door: the final report (fm decide --review) lists each task parked at a one-way step with the days it has waited and the…
- T-2364 [FEATURE M, done, 3 steps] Mission 8 surfaces: triggers, waiting installs, lane recoveries and self-fix verdicts on every surface (Mission 8, #7 #9 #11 #12) — les…
- decision 2026-11-01: [revisited: T-2450 (the secrets finder reads a date as a credential)] [cites: user steer 2026-10-31: finish round 1 completely, in order; no new mai…
## Lessons
- Rank a user's queue by what each answer frees, counted transitively, and keep age as the tiebreak so nothing starves silently
## Plan gaps
- failed first: step 1 red test: two queued grants, the newer one unblocks two waiting tasks, so it lists first in fm stat…
## Files touched
- plugin/tests/test_tool_queue.py
- plugin/lib/fmgrants.py
- plugin/lib/fmcli.py
- plugin/lib/fmmcp.py
- CHANGELOG.md
