---
id: T-3043
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-04T23:57:34Z
updated: 2026-11-04T23:57:34Z
steer_method_rate: 0.218
---
# The website shows live progress for every long-running task Sampo runs, such as model…
## Raw request
> also on the website i want to see progress of tasks, like training models, and such
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- The website shows live progress for every long-running task Sampo runs, such as model training, builds, test runs, data jobs, downloads and deploys. Training is one example of the pattern, not the whole scope.
- Each task has a visible state (queued, running, succeeded, failed, cancelled) and a start time and elapsed time. Where the task can report it, the page also shows a percent or step count, an ETA, and the current stage.
- Training runs also show epoch or step, loss and other key metrics (with a simple chart where useful), and the latest checkpoint.
- Updates arrive without a manual refresh, using streaming or polling at a sensible interval. The page stays correct after a reload or a reconnect, and after the task finishes.
- Task progress is recorded in a durable store, so finished and failed tasks stay visible as history with their final result, error message and log tail.
- Any task type that is added later must report progress through the same shared mechanism. Do this by adding one common progress-reporting interface that existing and new tasks call, instead of one-off pages.
- Failures, stalls and hung tasks are visible. A task with no heartbeat for a set time is flagged as stalled instead of displaying stale "running" status.
- Progress pages contain no secrets, tokens or private paths. Logs are filtered before display.
- Verify the work by running a real task, such as a short training run, and checking that the website shows its progress from start to finish, including a failure case. Add automated tests for the progress reporting and for the page's states.
- Update the docs to explain how to see progress and how to make a new task report it.
- Implement this directly in the existing website and codebase, following its current stack and conventions, rather than only proposing designs.
- Do not expose the progress view publicly, deploy it, or change hosting, access or auth settings without the user's explicit approval. Keep it local or behind the existing access controls by default.
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
- 2026-11-04T23:57:34Z created
## Follow-ups captured
