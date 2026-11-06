---
id: T-3084
type: RESEARCH
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T00:40:47Z
updated: 2026-11-05T00:41:00Z
harness_plan: code
base: 2760c2b4e776b766a446ed7ba606f5746ba419c0
base_tree: 50f6761c630f8a553673d0fba84b101bcbb9ebc7
plan0_at: 2026-11-05T00:40:48Z
plan0_scope: []
---
# Answer the multiplication question
## Raw request
> Reply with only the number: 17*23
## Interpretation
Reply with only the number: 17*23
## Assumptions (confidence)
## Acceptance criteria
- [ ] The answer to 17*23 is identified as 391 — verify with `test 391 -eq 391`
## Non-goals
## Approach (options → choice → why)
fm code (jarvis-nothink): 1) one free-form model run; 2) a human plan first; 3) the harness runs the stations. Choice 3: the model filled the plan and picks one action at a time
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Compute 17*23 to get 391  <- CURRENT
2. [ ] Confirm the arithmetic: 17 times 23 is 391
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `test 391 -eq 391` → exit 0 · (no output) [ran] [tree 50f6761c630f] [world 2f1906870a] (2026-11-05T00:40:50Z)
## Log
- 2026-11-05T00:40:47Z created
- 2026-11-05T00:40:48Z focused
- 2026-11-05T00:41:00Z dropped: a probe for T-3080 (sampo code on the 27B with a throwaway HOME), not work
- 2026-11-05T00:41:00Z work at drop saved: af7487e6d92e (restore: git -C ~/.claude/foreman restore --source=af7487e6d92e --worktree -- :/)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
- research T-2192-review: Verdict: changes needed.** The Stop-hook change and the exam re-ask look sound. The user's stated goal is not met, and the re-ask trigger is weak…
- T-2392 [FEATURE M, done, 4 steps] Unproven where the user sees it (Mission 7, #6): a reply claiming a measured number, accurate docs, a working migration, a rendered UI …
- T-1786 [FIX S, done, 1 steps] Guard: a multi-line double-quoted python3 -c string is read line by line as shell, so du.g — lesson: A name list that answers two questions…
