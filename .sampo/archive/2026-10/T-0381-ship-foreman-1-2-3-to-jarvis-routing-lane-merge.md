---
id: T-0381
type: CLEAN
tier: S
status: done
priority: normal
scope: [.claude-plugin/marketplace.json, plugin/.claude-plugin/plugin.json, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-09T00:43:56Z
updated: 2026-10-09T00:45:28Z
base: 0bdff43e14cf1aae116ae48d0ea580c7ad81d655
base_tree: 31e3958bbd2889c15ddf200134db35cbc08a3b51
verified: ok
---
# Ship Foreman 1.2.3 to JARVIS (routing, lane merge, fail-closed guard, builder briefs)
## Raw request
> Ship Foreman 1.2.3 to JARVIS (routing, lane merge, fail-closed guard, builder briefs)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] JARVIS has 1.2.3 installed and its live cache synced — verify with `ssh -o BatchMode=yes <host> 'grep -c "base=base" ~/.claude/plugins/cache/foreman/foreman/1.2.2/lib/fmlanes.py'`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] gate, bump, merge to main, update JARVIS, sync its live cache
## Resume here
## Docs impact
## Verification evidence
- (step 1) `ssh -o BatchMode=yes <host> 'grep -c "base=base" ~/.claude/plugins/cache/foreman/foreman/1.2.2/lib/fmlanes.py'` → exit 0 · 1 [ran] [tree 3ed35f8b6b2b] (2026-10-09T00:45:27Z)
- (ac 1) `ssh -o BatchMode=yes <host> 'grep -c "base=base" ~/.claude/plugins/cache/foreman/foreman/1.2.2/lib/fmlanes.py'` → exit 0 · 1 [ran] [tree 3ed35f8b6b2b] (2026-10-09T00:45:28Z)
- (audit self) `self: gate green (901 tests, doctor, roundtrip, hooks bench, mod tests, replay) before the bump; merged in a scratch clone; JARVIS fast-forwarded, plugin 1.2.3 installed, live cache synced with cp (no rsync there)` → no findings [tree 3ed35f8b6b2b] (2026-10-09T00:45:28Z)
## Log
- 2026-10-09T00:43:56Z created
- 2026-10-09T00:43:56Z focused
- 2026-10-09T00:45:28Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0366 [FIX M, done, 3 steps] Ship T-0364 to JARVIS: merge its 2 local commits into main, bump plugin to 1.2.0, refresh its plugin cache — lesson: A directory-marketplac…
- T-0371 [SECURITY S, done, 1 steps] Guard hook fails closed in Claude Code itself: onFailure: "block" on the PreToolUse hook (Claude Code ≥2.1.295) — lesson: A Sonnet bui…
- T-0376 [FEATURE M, done, 2 steps] Watch the JARVIS run and keep its Foreman current: fix friction it hits, ship each fix there — lesson: A running Claude Code session ke…
- decision 2026-10-09: [outward] Updating Foreman on JARVIS (merge to main, pull, plugin update, reload) as fixes land during the monitoring
- similar finished tasks took 1–3 steps
## Behaviour lock
none: a release (version bump + merge + install); each change it ships has its own tests (T-0371, T-0373, T-0377, T-0379); full fm check green before the bump
## Lessons
- JARVIS has no rsync: use cp -a for cache syncs
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
