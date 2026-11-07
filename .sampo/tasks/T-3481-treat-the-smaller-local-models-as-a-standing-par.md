---
id: T-3481
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T18:33:19Z
updated: 2026-11-06T18:33:19Z
steer_method_rate: 0.218
---
# Treat the smaller local models as a standing part of Sampo's development loop. Run real…
## Raw request
> and keep using the smaller local models, analyzing their behavior and keep improving Sampo to have their abilities match yours completely too
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Treat the smaller local models as a standing part of Sampo's development loop. Run real Sampo tasks through them routinely, not only when something breaks, and use the already-installed local models by default.
- Run the same task set through a local model and through the reference (Claude) model. Compare outcomes on pass rate, correctness of the final result, number of steps, tool-call validity, and whether the work was actually proven and finished.
- Analyze each local-model run for behavior, not just score. Read the traces for malformed tool calls, skipped verification, premature "done" claims, lost context, loops, plan drift, ignored instructions, and weak recovery from errors. Name the cause of each gap.
- Fix gaps in Sampo itself rather than in the task or the test. Candidate fixes include prompts, planning and decomposition, tool schemas and output parsing, retries and repair of bad output, context and memory handling, verification and finish gates, and guardrails. Prefer general mechanisms that li…
- Aim for the local models to reach the reference model's results through Sampo's scaffolding. Where a remaining gap comes from model capacity and not from the harness, say so plainly with evidence and don't claim parity.
- Don't game the measurement. Don't tune to specific eval tasks, loosen checks, or hide failures. Keep a held-out set of tasks the fixes were not tuned on.
- Every change needs a before/after re-run on the same tasks with the same models. Add a regression test or eval case for each fixed failure mode, and check that the strong model's results didn't get worse.
- Keep the surfaces consistent: update tests, evals, docs, and config defaults together with each behavior change. Keep a running log of runs, findings, changes, and the remaining gap per model.
- Repeat the loop continuously: run, analyze, fix, re-measure, and pick the biggest remaining gap next. Act on findings directly, and report results and open gaps faithfully, including failures and skipped steps.
- Keep all of this local and reversible by default. Get the user's grant before anything outward or irreversible: pushing or publishing, sending data to external services, downloading or installing new models or large dependencies, deleting or overwriting existing work, or spending past the stated bu…
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
- 2026-11-06T18:33:19Z created
## Follow-ups captured
