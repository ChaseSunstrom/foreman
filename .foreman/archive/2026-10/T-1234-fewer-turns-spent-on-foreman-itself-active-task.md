---
id: T-1234
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: [plugin/lib/**, plugin/tests/**, MASTER.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-16T17:34:14Z
updated: 2026-10-16T17:40:30Z
base: 2a43e90b29ba4419d73d793b16055bd24cbc76d8
base_tree: adc73768c05e38b0664332347a5092e19c94749a
plan0_at: 2026-10-16T17:38:49Z
plan0_scope: [plugin/lib/**, plugin/tests/**, MASTER.md, CHANGELOG.md]
verified: strong
---
# Fewer turns spent on Foreman itself: active-task default, either-side ac/step actions, --reason, correctable broken checks, S steps close on criteria, first task made for a one-request session; duel skips court cases, --runs/--jobs
## Raw request
> Fewer turns spent on Foreman itself: active-task default, either-side ac/step actions, --reason, correctable broken checks, S steps close on criteria, first task made for a one-request session; duel skips court cases, --runs/--jobs
## Interpretation
From T-1231's diagnosis: Foreman's extra cost in the duel was turns spent on its own commands; cut them without weakening any gate
## Assumptions (confidence)
## Acceptance criteria
- [x] The ergonomics, first-brief, approval and duel tests pass and the full suite is green — verify with `python3 plugin/tests/run.py test_task_ergonomics test_hooks test_board_posture test_bench test_bench_family test_round_i`
## Non-goals
## Approach (options → choice → why)
Fix each friction where all callers route through it (argv shaper at fm task entry, never_ran, finish's step proof, the brief refusal), keeping every lock that guards a failing check
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests from the duel transcripts and the review, then the changes
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_task_ergonomics test_hooks test_board_posture test_bench test_bench_family test_round_i` → exit 0 · Ran 224 tests in 41.9s (34 classes, 16 at a time; slowest: Stop 42s, PreToolUse 26s, Bench 24s) / OK [ran] [tree adc73768c05e] (2026-10-16T17:39:32Z)
- (ac 1) `python3 plugin/tests/run.py test_task_ergonomics test_hooks test_board_posture test_bench test_bench_family test_round_i` → exit 0 · Ran 224 tests in 42.1s (34 classes, 16 at a time; slowest: Stop 42s, PreToolUse 26s, Bench 24s) / OK [ran] [tree adc73768c05e] (2026-10-16T17:40:29Z)
- (audit adversary) `one fm-reviewer pass (adversary/edge/intent/operator/maintainer) on the diff; all findings fixed test-first: import-relabel limited to modules present in the repo with no other failures and no SyntaxError/'cannot import name'; first brief under a flock, with the session id, one work item only, tier S unless L-words or SECURITY; ids case-insensitive and after options; implicit add only for multi-word text; bench --jobs cancels queued sessions on interrupt; tail memo locked; spec lines kept in commit-case prompts` → a broken module under test (renamed function, deleted module, SyntaxError) keeps its failing check locked; an import gap can't mask another module's real failure; first brief only denies (the retry meets the whole guard) [tree adc73768c05e] (2026-10-16T17:40:29Z)
- (audit edge) `one fm-reviewer pass (adversary/edge/intent/operator/maintainer) on the diff; all findings fixed test-first: import-relabel limited to modules present in the repo with no other failures and no SyntaxError/'cannot import name'; first brief under a flock, with the session id, one work item only, tier S unless L-words or SECURITY; ids case-insensitive and after options; implicit add only for multi-word text; bench --jobs cancels queued sessions on interrupt; tail memo locked; spec lines kept in commit-case prompts` → lowercase and trailing ids, a one-word typo, two parallel first edits, Ctrl-C in a parallel duel, the summary line FAILED (errors=1) not counted as a real failure [tree adc73768c05e] (2026-10-16T17:40:29Z)
- (audit operator) `one fm-reviewer pass (adversary/edge/intent/operator/maintainer) on the diff; all findings fixed test-first: import-relabel limited to modules present in the repo with no other failures and no SyntaxError/'cannot import name'; first brief under a flock, with the session id, one work item only, tier S unless L-words or SECURITY; ids case-insensitive and after options; implicit add only for multi-word text; bench --jobs cancels queued sessions on interrupt; tail memo locked; spec lines kept in commit-case prompts` → commands without an id name the task they used on stderr; the first-brief note says how to finish and how to resize [tree adc73768c05e] (2026-10-16T17:40:29Z)
- (audit maintainer) `one fm-reviewer pass (adversary/edge/intent/operator/maintainer) on the diff; all findings fixed test-first: import-relabel limited to modules present in the repo with no other failures and no SyntaxError/'cannot import name'; first brief under a flock, with the session id, one work item only, tier S unless L-words or SECURITY; ids case-insensitive and after options; implicit add only for multi-word text; bench --jobs cancels queued sessions on interrupt; tail memo locked; spec lines kept in commit-case prompts` → one argv shaper at fm task entry instead of 32 optional ids; never_ran stays the single judge of a run that never reached its check [tree adc73768c05e] (2026-10-16T17:40:29Z)
- (audit intent) `one fm-reviewer pass (adversary/edge/intent/operator/maintainer) on the diff; all findings fixed test-first: import-relabel limited to modules present in the repo with no other failures and no SyntaxError/'cannot import name'; first brief under a flock, with the session id, one work item only, tier S unless L-words or SECURITY; ids case-insensitive and after options; implicit add only for multi-word text; bench --jobs cancels queued sessions on interrupt; tail memo locked; spec lines kept in commit-case prompts` → every cut removes a turn the duel's transcripts showed Foreman spending on itself, without loosening a gate on a failing check [tree adc73768c05e] (2026-10-16T17:40:29Z)
## Log
- 2026-10-16T17:34:14Z created
- 2026-10-16T17:38:49Z focused
- 2026-10-16T17:38:50Z scope: carries the T-1231 and T-1233 code edits made while T-1231 was focused (fmbench, fmcli, fmcore, fmhooks, helpers, test_bench, test_board_posture, test_hooks, test_task_ergonomics, MASTER.md)
- 2026-10-16T17:40:30Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- research T-0298-review-1: Findings
- T-0280 [FEATURE M, done, 5 steps] Bench family: judged cases, plugin duels, version replays, regression court, shadow-user soak — lesson: Git run after a bypass-mode ses…
- decision 2026-10-16: Drafts (fm draft) run headless claude with --permission-mode acceptEdits
- similar finished tasks took 5–5 steps
- start here (files T-1117 touched): plugin/tests/test_close_gates.py, plugin/lib/fmcli.py, CHANGELOG.md, MASTER.md, README.md
- likely tests for the scope: plugin/tests/test_agents.py, plugin/tests/test_ambient.py, plugin/tests/test_away.py, plugin/tests/test_backtest.py, plugin/tests/test_bench.py, plugin/tests/test_budget.py, plugin/tests/test_bus.py,…
## Measurements
Before (first duel transcripts, Foreman's own repo, sonnet): Foreman arm 23.5 turns per task on average vs 17 for Claude Code with the guard only; per case the Foreman arm spent 2 turns on the no-task refusal + fm task new, 3-4 on plan sections/--help/a refused state write, and in one case 6 on dropping and recreating a task whose check couldn't import its test module. After (neutral spec suite smoke, 2 tasks, 1 run each): the no-task refusal costs 1 turn (the task is made for the session), no drop/recreate, no argv errors; Foreman 8 and 12 turns vs 4 and 4 for Claude Code, both arms passing both tasks. The remaining gap is the bookkeeping turns themselves (finish, evidence), addressed next in T-1231.
## Lessons
- Measure an agent harness by reading its sessions turn by turn: the overhead was in friction with its own CLI, not in context size
