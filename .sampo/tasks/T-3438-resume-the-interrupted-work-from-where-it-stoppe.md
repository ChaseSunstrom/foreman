---
id: T-3438
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T14:35:12Z
updated: 2026-11-06T14:35:12Z
steer_method_rate: 0.218
---
# Resume the interrupted work from where it stopped, without restarting it or asking the…
## Raw request
> continue, why hasn't the github rpeo updated at all either
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Resume the interrupted work from where it stopped, without restarting it or asking the user to restate it. First state briefly what is done and what remains.
- Treat the GitHub repo as the record of progress. Completed, verified work gets committed in coherent units and pushed to the repo's configured remote and branch, so the repo never silently lags behind the working tree.
- When the user asks why the repo hasn't updated, investigate before explaining. Check whether a git repo and remote exist (the working directory here is not a git repository), the current branch, uncommitted or unpushed changes, auth and permission errors, and whether a push or CI step failed.
- Report the actual cause with evidence (command output, remote state), including if nothing was ever committed or pushed. Do not guess or reassure.
- Fix the cause when it is local and reversible: initialize or attach the repo, stage and commit the work, or repair the remote configuration. Do not just advise the user to do it.
- Before the first push to a remote, or any push to a new remote or branch, confirm the target with the user unless they have already authorized pushing there. A push publishes content that may be cached or indexed, so check the diff for secrets, credentials and unrelated files first.
- Never force-push, rewrite published history, delete branches, or overwrite remote content without explicit approval for that specific action.
- After pushing, verify that the remote head matches the local head and that the expected files and commits are visible. Say plainly what was pushed, or what failed and why.
- From then on, push at each natural checkpoint (a feature working, tests passing) under the grant given. Mention the push in the progress update so the user can see the repo is current.
- Keep commits honest. Messages describe the real change. Failing tests or skipped steps are stated in the report and not hidden by pushing as if complete.
- Update the docs, README and changelog affected by the pushed work in the same change, so the repo reflects the current state.
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
- 2026-11-06T14:35:12Z created
## Follow-ups captured
