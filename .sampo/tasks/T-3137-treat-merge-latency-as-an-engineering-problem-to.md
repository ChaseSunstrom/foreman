---
id: T-3137
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-05T04:52:25Z
updated: 2026-11-05T04:52:25Z
steer_method_rate: 0.218
---
# Treat merge latency as an engineering problem to solve: when Sampo's merge path takes…
## Raw request
> feel free to invent/make new tech to make it so merges can happen very very quickly without the almost hour of verifications and such, but still making sure everything works, and multiple merges at the same time, etc.
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Treat merge latency as an engineering problem to solve: when Sampo's merge path takes long (the ~hour of verification), measure where the time goes (queue wait, build, test, lint, integration, deploy checks) and cut it, rather than accepting it as fixed.
- Invent or build new tooling where existing options fall short: e.g. affected-only test selection from a dependency graph, content-addressed build/test caching, incremental and parallel verification, sharded test runners, speculative pre-verification of the likely merge result, and flaky-test quaran…
- Support many merges in flight concurrently: use a merge queue that speculatively verifies stacked or batched candidates in parallel, bisects automatically on failure to isolate the culprit, and detects conflicts, both textual and semantic, between simultaneous merges.
- Never trade correctness for speed: every merge must still be proven to work against the exact tree that lands (the post-merge result, not just the branch tip). Any shortcut (skipped test, cache hit, selective run) must be shown sound, with a fallback to full verification when soundness can't be est…
- Make the speedup measurable and checked: record baseline vs. new merge time (p50/p95), cache hit rate, and the rate of escaped defects, and add tests for the new tooling itself (including cache invalidation, concurrent-merge races, and failure/bisect paths) and a periodic full-verification audit th…
- Cover every surface the merge path touches: CI configuration, local pre-merge hooks, the merge queue/bot, build and test scripts, branch protection or required-check settings, and docs/runbooks describing the process, updating all of them consistently.
- Roll out safely and reversibly: ship the fast path behind a flag or alongside the existing path, compare results in shadow mode first, keep a one-step rollback, and keep failures loud, never silently passing.
- Act on this by implementing and verifying within the work, not just proposing designs. Changes that are outward-facing or hard to reverse (altering protected-branch rules or required checks on the remote, pushing, force-merging, changing shared CI infrastructure, or spending beyond the budget) stil…
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
- 2026-11-05T04:52:25Z created
## Follow-ups captured
