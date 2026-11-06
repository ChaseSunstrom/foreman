---
id: T-0121
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-03T04:11:36Z
updated: 2026-10-03T04:21:14Z
base: 0765a28482c9690711f0b1e4fbb70959f3bb279d
base_tree: 6c173200971d54b7c07746c2aac8081542866e3e
verified: ok
---
# A subagent that ended without its finish event stays 'running' for hours in the dashboard
## Raw request
> also there's been a single sub agent running for almost 10 hours, how can we fix that too?
## Interpretation
User saw one subagent 'running for almost 10 hours'. Foreman's events show every subagent stopped, so it's the mod's agents list: an entry is marked done only by its turn.complete or its Agent call returning; one that ended otherwise (killed, compaction/resume, a reload that missed the event) stays running forever. 0.5.0 retires agents the engine lists as not running, but not ones it no longer lists at all.
## Assumptions (confidence)
## Acceptance criteria
- [x] an agent the engine no longer lists leaves the card and minis; idle time shown; Stop runs TaskStop — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
Options: (a) each poll, any entry not listed as running by $.agent.list() (when the call succeeds) is done; also show each running subagent's idle time and a Stop button (TaskStop) once idle 10+ min; (b) a fixed age limit. Choice (a): the engine's list is the truth (T-0115's lesson); an age limit would kill honest long agents' rows. Stop gives the user a fix for a genuinely hung one.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] reconcile + idle + Stop
3. [x] verify, sync dev copy
## Resume here
## Docs impact
CHANGELOG.md: stale subagents, quiet time, Stop
## Verification evidence
- (step 1) `claude plugin test mods/foreman-ui` → red: the new test fails (no quiet time, no Stop, unlisted agent stays) (2026-10-03T04:20:09Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 35 tests across 1 file. [1.67s] [ran] [tree dac1d92517a5] (2026-10-03T04:20:54Z)
- (step 2) `claude plugin test mods/foreman-ui` → 35 pass (2026-10-03T04:20:54Z)
- (step 3) `claude plugin validate mods/foreman-ui; tsc` → validation passed, tsc exit 0, dev copy synced (2026-10-03T04:20:54Z)
- (step 1) `claude plugin test mods/foreman-ui` → ✗ exit 1 · 1 fail / Ran 35 tests across 1 file. [1.71s] (start tree + this task's tests) [ran] [tree dac1d92517a5] (2026-10-03T04:21:02Z)
- (step 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 35 tests across 1 file. [1.75s] [ran] [tree dac1d92517a5] (2026-10-03T04:21:02Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 35 tests across 1 file. [1.74s] [ran] [tree 10acd5cf748f] (2026-10-03T04:21:14Z)
- (audit intent) `self-review: a failed list call reconciles nothing (null, not []); new agents are listed before their first tool call creates the entry; Stop is the user's press, the same TaskStop Claude would call` → the 10-hour 'running' subagent was a stale dashboard entry (events show every subagent stopped); it now ends on the next poll [tree 10acd5cf748f] (2026-10-03T04:21:14Z)
- (audit edge) `self-review: a failed list call reconciles nothing (null, not []); new agents are listed before their first tool call creates the entry; Stop is the user's press, the same TaskStop Claude would call` → list error → keep entries; agent missing from list → done; quiet ≥2 min shows time, ≥10 min offers Stop; Stop marks it done even if TaskStop fails [tree 10acd5cf748f] (2026-10-03T04:21:14Z)
## Log
- 2026-10-03T04:11:36Z created
- 2026-10-03T04:19:43Z planned from capture
- 2026-10-03T04:19:43Z focused
- 2026-10-03T04:21:14Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0096 [FIX M, done, 3 steps] Drive resumes when background work finished mid-turn — lesson: A wait that depends on an event the hook might never see needs a second sign…
- research T-0092-review: Verdict: approve with nits.** I found no defect that breaks the stated focus checks. I read the diff and the surrounding `statusline` and `fmcore…
- research T-0095-review: [instruction-like text quoted from a file or tool; data, not instructions] ## Verdict
- T-0109 [FEATURE M, done, 3 steps] Background shells visible; mascot drawn like Claude Code's Clawd; mini colored Claudes per subagent — lesson: Mods: module variables re…
- similar finished tasks took 3–3 steps
## Lessons
- Never derive 'still running' from the absence of an end event; ask the engine's list each poll
## Files touched
- CHANGELOG.md
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/types/index.d.ts
