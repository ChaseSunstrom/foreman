---
id: T-3322
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T04:27:23Z
updated: 2026-11-06T04:27:23Z
steer_method_rate: 0.218
---
# Keep Sampo's working state (plan, task list and status, decisions with reasons, proof…
## Raw request
> And I want you to start syncing your state to git too, in this repo as well, etc.
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Keep Sampo's working state (plan, task list and status, decisions with reasons, proof and test evidence, open questions, handoff notes) in plain-text files in a dedicated tracked directory in each repo the user works in, including this one, and in any other place the user already syncs state to.
- Update those files as the work happens, not in a batch at the end. Update them at each milestone: plan agreed, step finished, check run, decision made, blocker hit, session ending.
- Commit the state files at each of those checkpoints with a clear message, e.g. `sampo-state: <what changed>`. Keep these commits separate from code commits, and never stage the user's unrelated or uncommitted changes in them.
- Make state files self-contained and current, so a fresh session can resume from them alone. Remove or mark stale entries rather than letting them contradict the code.
- Keep secrets, credentials, tokens, personal data such as the user's email, and raw logs that contain them out of state files. Check each state commit for them before committing.
- Before the first sync in a repo, check that it is a git repo and look at the existing state files, so nothing is overwritten. If the working directory is not a git repo, say so and ask before running `git init`.
- Commit locally without asking, but treat pushing to a remote as outward-facing. Push only to a remote and branch the user has explicitly approved, and treat that approval as covering only that remote and branch. Never force-push, rewrite history, or delete branches or state history without a specif…
- Report each sync briefly: which repo, which commit, and whether it was pushed. If a sync fails (conflict, hook rejection, no repo), say so plainly and do not claim it succeeded.
- Treat "etc." as covering every comparable surface: each repo or worktree touched in a session, and any state kept in memory or notes files that does not already exist in git.
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
- 2026-11-06T04:27:23Z created
## Follow-ups captured
