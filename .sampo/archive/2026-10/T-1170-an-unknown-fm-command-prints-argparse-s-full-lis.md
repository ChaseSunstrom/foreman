---
id: T-1170
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_gate_friction.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-16T10:45:57Z
updated: 2026-10-16T10:57:46Z
base: 67393bbcb080ce50080abaf964893d5abced5847
base_tree: 40a85aa2fb17ec9df302b1995b4cabe2d0e0c5b1
plan0_at: 2026-10-16T10:54:18Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_gate_friction.py, CHANGELOG.md]
verified: strong
---
# An unknown fm command prints argparse's full list of 170 choices (and a poor 'did you mean
## Raw request
> An unknown fm command prints argparse's full list of 170 choices (and a poor 'did you mean'); print only the close matches and point at fm help
## Interpretation
An unknown command costs ~2 KB of choices in the output; the nearest match and a pointer to fm help are what help.
## Assumptions (confidence)
## Acceptance criteria
- [x] an unknown fm command names the nearest match and fm help, not argparse's list of every command; a short choice list (a subcommand's few actions) is still shown — verify with `python3 plugin/tests/run.py test_gate_friction`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test in test_gate_friction Typos
2. [x] _Parser.error drops a long choose-from list
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_gate_friction` → ✗ exit 1 · Ran 7 tests in 1.4s (2 classes, 16 at a time; slowest: Flakes 1s, Typos 1s) / FAILED (1 classes) [ran] [tree ff581e770773] (2026-10-16T10:54:25Z)
- (step 2) `python3 plugin/tests/run.py test_gate_friction` → exit 0 · Ran 7 tests in 3.3s (2 classes, 16 at a time; slowest: Flakes 3s, Typos 1s) / OK [ran] [tree b9ae4ff5f3ab] (2026-10-16T10:54:35Z)
- `python3 plugin/tests/run.py test_gate_friction` → ✗ exit 1 · Ran 7 tests in 3.6s (2 classes, 16 at a time; slowest: Flakes 3s, Typos 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree b50c98be814f] (2026-10-16T10:54:49Z)
- `python3 plugin/tests/run.py test_gate_friction` → exit 0 · Ran 7 tests in 3.2s (2 classes, 16 at a time; slowest: Flakes 3s, Typos 1s) / OK [ran] [tree b50c98be814f] (2026-10-16T10:54:49Z)
- (ac 1) `python3 plugin/tests/run.py test_gate_friction` → exit 0 · Ran 7 tests in 3.0s (2 classes, 16 at a time; slowest: Flakes 3s, Typos 2s) / OK [ran] [tree b50c98be814f] (2026-10-16T10:55:30Z)
- `python3 plugin/tests/run.py test_gate_friction test_cli` → exit 0 · Ran 109 tests in 37.5s (30 classes, 16 at a time; slowest: TaskLifecycle 37s, StateViews 14s, AuditPrep 12s) / OK [ran] [tree b50c98be814f] (2026-10-16T10:55:30Z)
- (audit edge) `self: only argparse's invalid-choice text is rewritten and only when it lists more than 12 choices; did-you-mean unchanged; short subcommand lists keep their choices` → a choice list of exactly 12 or fewer is unchanged; a flag typo path untouched [tree b50c98be814f] (2026-10-16T10:55:30Z)
- (audit self) `self: only argparse's invalid-choice text is rewritten and only when it lists more than 12 choices; did-you-mean unchanged; short subcommand lists keep their choices` → no findings [tree b50c98be814f] (2026-10-16T10:55:30Z)
## Log
- 2026-10-16T10:45:57Z created
- 2026-10-16T10:54:17Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_gate_friction.py', 'CHANGELOG.md']
- 2026-10-16T10:54:18Z focused
- 2026-10-16T10:57:45Z done
- 2026-10-16T10:57:46Z committed bb0a8d6 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- T-0854 [FIX M, done, 5 steps] A newcomer's first fm commands make sense: short --help, task new shows its values and an example, init/status say what… — lesson: The firs…
- T-0274 [FEATURE M, done, 3 steps] Gate and CLI friction: flake ledger in fm check, nearest-command help on fm typos — lesson: Before adding a mechanism, read how the cod…
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
- likely tests for the scope: plugin/tests/test_cli.py
## Plan gaps
- failed first: step 1 Failing test in test_gate_friction Typos
## Files touched
- plugin/tests/test_gate_friction.py
- plugin/lib/fmcli.py
- CHANGELOG.md
