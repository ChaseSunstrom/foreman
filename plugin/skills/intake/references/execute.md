# Execute loop (reference)

## Per step
0. M/L FEATURE or FIX, before reading the code for the tests: `fm oracle ID` (T-0226) writes behaviour examples and ambiguities from the request alone into the brief's Oracle section. Write the tests from those examples, so they check what was asked rather than mirror what you build; settle each ambiguity with `fm decide` first.
1. `fm resume` if you are not sure where you are. Work only on the CURRENT step.
2. Do the work. Stay in scope; out-of-scope edits → widen scope (`fm task set ID scope=…`) or log why (`fm task log ID "scope: <why>"`; `fm task done` asks for one), or `fm capture`. Big file: `fm outline PATH`, then Read only the range you need.
3. Verify with a fresh command (tests, build, lint, a reproduction). Read the whole output.
4. Record: `fm task step ID done N --evidence "<cmd>" "<result>"` (or `fm task evidence` first). fm refuses without evidence.
5. Acceptance criteria: `fm task ac ID check N --evidence "<cmd>" "<result>"`.

## Batches (T-0257)
Small related requests (the same type, nearby files) are faster as one: `fm batch ID ID …` makes one host task with every member's criteria and one step each. Plan its verify commands, work the steps, run `fm check` once for the whole batch, one review pass, one commit; the members close done in the host. `fm next` suggests it when three or more small items of one type lead the inbox.

## Checkpoints and git
- `fm checkpoint --note "<exact resume point>"` before switching tasks, before risky or destructive-but-authorized steps, and at natural pauses. PreCompact does an automatic checkpoint; a note is better.
- Commit in small conventional commits on the task branch. Before a destructive-but-authorized step, commit or stash (`git stash push -m foreman/T-NNNN`) so git and rewind both cover it.

## Loop cap
3 failed verification attempts on the same step → stop. Write a diagnosis in the brief (what was tried, what was observed, hypotheses) with `fm task set ID --section "Resume here" --text …`, `fm task block ID "<reason>"`, move to the next unblocked task, and report.

## Preemption and pause
- `NOW:` / `TAG!:` / emergency → `fm checkpoint --note …`, `fm capture` or intake the new item, `fm focus NEW`, and offer to resume the old one afterwards.
- PAUSE → `fm checkpoint --note …` and wait (drive pauses automatically).

## End of task
1. FINAL checks for this task: full test suite / build, not just the new test. Record evidence.
2. Audit (`audit.md`): S = self checklist; M = intent + the riskiest other lens; L = all five lenses via `foreman:fm-reviewer`. Verify every finding, fix or capture it, `fm task audit ID <lens> "<how>" "<result>"`.
3. `fm task done ID` (fm lists anything missing, including audits older than the last edit).
4. `/foreman:reflect` for M/L tasks or anything that caused back-and-forth. Anything you did by hand again (`fm repeats` lists what recurs across tasks) → capture an S task to make it a project tool (below).
5. Triage the inbox: expand captured items into briefs (intake §2), fold them into the queue.
6. Re-plan checkpoint after each phase group or structural change: re-read remaining briefs, update scope, approach and Execution prompts, re-order if dependencies changed (`fm queue --replan`), log what changed in each brief.
7. Show the queue in ≤ 10 lines and continue per autonomy (`/foreman:next`).

## Project tools (for work that repeats)
`fm repeats` reports commands run 3+ times in 2+ tasks and steps that recur in 3+ tasks, each with a suggestion. Make the smallest tool that removes the repetition, in the project repo, as its own S task, then `fm repeats dismiss "<shape or step>"` (also for one that isn't worth a tool). A new skill, agent or command file is always-on context, so creating one needs the user's yes (`fm ask ID plugin`; editing an existing one doesn't):
- A gate (tests, lint, build, a benchmark with a budget) → `fm check add "<cmd>"`; `fm check` then runs every gate at once.
- A multi-command sequence → a script in the repo (`scripts/<name>`), then use it in evidence (`--run`) or as a gate.
- A procedure with judgement (how this repo does releases, migrations, fixture updates) → a project skill, `.claude/skills/<name>/SKILL.md`: frontmatter `name` and a one-line `description` saying when to use it (it is always-on context in this repo, so keep it short), then the steps, commands and pitfalls. Sessions and subagents in the repo load it when it applies.
- The same delegation brief sent again and again → a project agent, `.claude/agents/<name>.md`, with only the tools it needs.

## Evidence quality
Evidence is a command plus its actual result. "Tests pass" needs the test command's output with 0 failures; "bug fixed" needs the original reproduction passing; "regression test works" needs the red-green cycle: `fm task prove ID --run "<test cmd>"` runs it on the start tree with only your test files (must fail) and on the current tree (must pass), recording both. PERFORMANCE tasks record numbers (`--section "Measurements"`: before → after); CLEAN tasks run the tests before their first edit (behaviour lock). `fm task done` prints a verification grade (strong: every check ran through fm, plus red→green or an independent lens). `fm sentinel` re-runs the checks recent finished tasks passed (FINAL VERIFY). See `verification.md`.
