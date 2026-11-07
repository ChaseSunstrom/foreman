---
id: T-3470
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T17:00:25Z
updated: 2026-11-06T17:00:25Z
steer_method_rate: 0.218
---
# Focus on the plugin itself: push its AI capabilities to the limit, treating the plugin…
## Raw request
> I meant more of the plugin itself, pushing AI to the limits, also when everything gets mergecd, I want you to run a bunch of agents/reviewers on how we can speed up every process/make it more efficient, etc. so everything is much much faster
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Focus on the plugin itself: push its AI capabilities to the limit, treating the plugin as the primary target of improvement rather than surrounding or peripheral code.
- After every merge, automatically launch a batch of parallel agents/reviewers to audit the whole plugin and its workflows for speed and efficiency (build, test, CI, runtime, startup, agent orchestration, prompts and context size, tool calls, caching, docs/tooling).
- Cover every process end to end: each reviewer takes a distinct area, so no stage of the pipeline goes unexamined.
- Make the review measurable: record a baseline for each process (wall-clock time, token use, cost, tool-call counts), then re-measure after each change and report the before/after.
- Act on findings: implement the safe, clearly beneficial speedups directly, verify with tests and benchmarks that behavior is unchanged, and keep each optimization as its own reviewable change.
- Rank remaining findings by expected gain versus effort and risk, and report them with evidence rather than leaving vague advice.
- Run independent reviewers and independent tasks in parallel, and avoid redundant work such as re-deriving established facts or repeating completed steps.
- Keep the loop going: after each round of optimizations merges, repeat the review until gains fall below a stated threshold, and update docs, tests and configs to match each change.
- Require the user's explicit approval before outward-facing, destructive or irreversible actions (publishing releases, force-pushing, deleting data, spending beyond the budget, sending data to external services), and stay within the stated spend limit.
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
- 2026-11-06T17:00:25Z created
## Follow-ups captured
