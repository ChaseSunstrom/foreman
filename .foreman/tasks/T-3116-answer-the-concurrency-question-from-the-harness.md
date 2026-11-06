---
id: T-3116
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-05T03:10:58Z
updated: 2026-11-05T03:10:58Z
steer_method_rate: 0.218
---
# Answer the concurrency question from the harness itself: report the real maximum number…
## Raw request
> how many different builders can you have running at the same time on independant things? also, have you tried using the local models for tasks with you? like the qwen 3.8 27b model for tasks? so you can see its output and help improve sampo to make sure its genuinely better
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Answer the concurrency question from the harness itself: report the real maximum number of builders that can run at once on independent work, and how that limit is set. Don't guess a number.
- Run work in parallel builders whenever the pieces are independent (no shared files, no ordering dependency, no shared state). Keep dependent pieces sequential, and say which pieces were treated as independent and why.
- Give each parallel builder its own scope, such as its own files, worktree, or directory, so concurrent runs can't overwrite each other. Check for conflicts before merging results.
- Use the locally installed models (the Qwen ~27B model named, whatever its exact installed tag is) as workers on real Sampo tasks. First check what is installed and runnable locally, and use that exact model rather than assuming a name or version.
- For each local-model task, capture the full output and read it. Judge it against a concrete bar: tests pass, the diff is correct, the spec is met, and no needed step was skipped.
- Compare local-model results with the current default path on the same task and inputs. Record the quality, correctness, failure modes, time, and cost of each, so "genuinely better" rests on measured before/after evidence rather than impressions.
- Turn the failures and weak spots found into specific Sampo improvements, covering prompts, task decomposition, tool handling, verification steps, retries, and docs. Make those changes directly, then re-run the same tasks to confirm the change helped and nothing else regressed.
- Add or update tests and an evaluation set for each issue found, so the improvement is repeatable and the gain can be re-checked later.
- Report results plainly: what ran, how many builders at once, what the local model got right and wrong, what changed in Sampo, and what the measured difference was. If a run failed or was skipped, say so with the output.
- Keep local-model work local. Don't send task content, code, or logs to any outside service to run or score these comparisons.
- Ask first before anything outward-facing or hard to reverse: publishing or pushing changes, deleting or overwriting existing configs or models, installing or downloading large models, or spending beyond the stated budget.
- Treat this as standing practice: keep dogfooding local models on tasks as Sampo changes, and re-measure after each significant change.
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
- 2026-11-05T03:10:58Z created
## Follow-ups captured
