# Execute loop (reference)

## Per step
1. `fm resume` if you are not sure where you are. Work only on the CURRENT step.
2. Do the work. Stay in scope; out-of-scope edits → widen scope with a logged reason or `fm capture`.
3. Verify with a fresh command (tests, build, lint, a reproduction). Read the whole output.
4. Record: `fm task step ID done N --evidence "<cmd>" "<result>"` (or `fm task evidence` first). fm refuses without evidence.
5. Acceptance criteria: `fm task ac ID check N --evidence "<cmd>" "<result>"`.

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
4. `/foreman:reflect` for M/L tasks or anything that caused back-and-forth.
5. Triage the inbox: expand captured items into briefs (intake §2), fold them into the queue.
6. Re-plan checkpoint after each phase group or structural change: re-read remaining briefs, update scope, approach and Execution prompts, re-order if dependencies changed (`fm queue --replan`), log what changed in each brief.
7. Show the queue in ≤ 10 lines and continue per autonomy (`/foreman:next`).

## Evidence quality
Evidence is a command plus its actual result. "Tests pass" needs the test command's output with 0 failures; "bug fixed" needs the original reproduction passing; "regression test works" needs the red-green cycle. See `verification.md`.
