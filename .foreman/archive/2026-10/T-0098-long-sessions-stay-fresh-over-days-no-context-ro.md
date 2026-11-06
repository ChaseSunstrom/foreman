---
id: T-0098
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-02T20:09:43Z
updated: 2026-10-02T23:10:32Z
base: 88ff5afc4f0f9be70a77cb91fdd8ed62e0fd82d9
verified: strong
---
# Long sessions stay fresh: compact at task boundaries
## Raw request
> FEATURE: long sessions stay fresh over days: no context rot, out-of-date information or stale docs (compact at task boundaries, re-verify stale facts, docs freshness)
> CONTEXT: user report from a long-running Volt session; Foreman should keep driving the queue unattended
## Interpretation
User: 5-day sessions get context rot and out-of-date information; keep them fresh.
## Assumptions (confidence)
## Acceptance criteria
- [x] a task closing at ≥ threshold compacts once with Foreman's instructions; below it, or with the threshold 0, never — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
Options: (a) the mod compacts the session when a task closes and context ≥ a configurable threshold (default 40%), with instructions that keep standing requests/decisions and drop finished work, Foreman's checkpoint + resume note restoring the exact point; (b) a periodic /compact reminder. Choice: (a). Why: task boundaries are when old detail stops mattering, and it needs nobody to remember.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] freshen at task close + userConfig
3. [x] docs
## Resume here
## Docs impact
README.md, CHANGELOG.md
## Verification evidence
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 23 tests across 1 file. [0.75s] [ran] [tree 24ec6009de32] (2026-10-02T23:10:32Z)
- (step 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 23 tests across 1 file. [0.75s] [ran] [tree 24ec6009de32] (2026-10-02T23:10:32Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 23 tests across 1 file. [0.75s] [ran] [tree 24ec6009de32] (2026-10-02T23:10:32Z)
- (step 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 23 tests across 1 file. [0.75s] [ran] [tree 24ec6009de32] (2026-10-02T23:10:32Z)
- (audit intent) `self-review + mod tests with a mocked clock and usage` → multi-day sessions shed finished work at task boundaries automatically; configurable and off-able [tree 24ec6009de32] (2026-10-02T23:10:32Z)
- (audit edge) `self-review + mod tests with a mocked clock and usage` → compaction runs outside the refresh dispatch (clock.after), only on a task that was open and closed, once per close; usage errors and refusals caught; below threshold and freshAt 0 never compact (tested) [tree 24ec6009de32] (2026-10-02T23:10:32Z)
## Log
- 2026-10-02T20:09:43Z created
- 2026-10-02T23:09:59Z planned from capture
- 2026-10-02T23:09:59Z focused
- 2026-10-02T23:10:32Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0096 [FIX M, done, 3 steps] Drive resumes when background work finished mid-turn — lesson: A wait that depends on an event the hook might never see needs a second sign…
- T-0097 [PERFORMANCE M, done, 3 steps] Find and cut where Foreman's time goes — lesson: Measure from the ledgers before cutting: the bookkeeping round-trips, not the tool…
- T-0099 [FEATURE M, done, 3 steps] Brainstorms find more, wilder and unspoken ideas and build off categories — lesson: Feed brainstormers the user's own words and a yes-a…
- T-0013 [FEATURE L, done, 5 steps] Context rot and doc drift defenses
- similar finished tasks took 3–5 steps
## Lessons
- Compact at task boundaries, not on a timer: that's when old detail stops mattering.
## Files touched
- CHANGELOG.md
- README.md
- mods/foreman-ui/.claude-plugin/plugin.json
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
