---
id: T-3284
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T02:32:23Z
updated: 2026-11-06T02:32:23Z
steer_method_rate: 0.218
---
# CPU is no longer a constraint. Run builds, test suites, linters, benchmarks, fuzzing,…
## Raw request
> you can use as much CPU as you want now, and you can run up to like 100 agents, i literally do not care
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- CPU is no longer a constraint. Run builds, test suites, linters, benchmarks, fuzzing, searches and verification at full parallelism, and don't ask before starting a heavy local job or throttle it to be polite.
- Up to about 100 agents may run concurrently. Treat 100 as a ceiling, not a target, and use as many as the work benefits from.
- Whenever work splits into independent pieces (per-file, per-module, per-test-shard, per-hypothesis, per-review-angle), fan it out to parallel agents and run independent tool calls in the same step.
- Use the extra capacity to prove the work, not only to speed it up. Run the full test matrix rather than a sample, review from several independent angles, and cross-check results.
- Keep parallel agents from colliding: give each a distinct scope, working directory or branch, don't let two write the same file, and merge and re-verify the combined result before reporting it done.
- This grant covers local compute and agent count only. Spending money, calls to paid or rate-limited external services, publishing, pushing, deleting, overwriting and other outward or irreversible actions still need the user's explicit go-ahead. The USD budget is unchanged.
- Report honestly how much parallelism was used and what the combined runs showed, including failures and skipped steps.
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T02:32:23Z created
## Follow-ups captured
