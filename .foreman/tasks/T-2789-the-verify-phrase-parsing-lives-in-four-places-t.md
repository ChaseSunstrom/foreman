---
id: T-2789
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-03T05:35:24Z
updated: 2026-11-03T20:40:59Z
builder_model: sonnet
lane_branch: worktree-agent-a76e6d3ed974941d9
base: 083387495ebcb68379d6d58874da41570435295c
base_tree: ca561fc0097e26b6c1669a530e49bbb7dfe095dd
predict_minutes: 1
predict_attempts: 1
plan0_at: 2026-11-03T20:25:09Z
plan0_scope: []
lane_stop: merged 2026-11-03T20:38:05Z
verified: strong
---
# The verify-phrase parsing lives in four places (task new --ac, task ac add, task ac edit…
## Raw request
> CLEAN: the verify-phrase parsing lives in four places (task new --ac, task ac add, task ac edit after T-2786, core.edit_ac and task set --section's criteria parser); one helper core.split_verify(text) -> (text, cmd) would stop them drifting
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] one helper core.split_verify parses both typed verify forms (the double-colon form, split on its last separator, and the dash 'verify with' form); task new --ac, task ac add, task ac edit --text, fm batch's DONE-WHEN lines and task set --section's criteria all use it — verify with `python3 plugin/tests/run.py test_task_ergonomics test_cli test_batch`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests: each of the five entry points accepts both forms and splits on the last ' :: '
2. [x] core.split_verify, and the five sites call it
## Resume here
## Docs impact
none: behaviour unified, the documented forms unchanged
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_task_ergonomics test_cli test_batch` → exit 0 · Ran 219 tests in 50.3s (55 classes, 16 at a time; slowest: TaskLifecycle 50s, BatchEdit 34s, CaptureAndIntake 29s) / OK [ran] [tree e9902aaefb2e] [world 2f1906870a] (2026-11-03T20:30:19Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 2 of 6 failed: python3 plugin/tests/bench_hooks.py --runs 20 → ✗ exit 1 · Notification                36.2    38.8     150  [0] / SessionEnd                  25.7    26.8     150  [0] (flaky again (failed first in 3+ recent runs): treated as a failure; find the race); python3 plugin/tests/run.py → ✗ exit 1 · Ran 5958 tests in 374.0s (1279 classes, 16 at a time; slowest: Worker 134s, LeanKind 101s, ExamAuthors 88s) / FAILED (1 classes: test_core.SandboxEnv) [ran] [tree 0feb5b487ada] [world 2f1906870a] (2026-11-03T20:32:26Z)
- (step 2) `python3 plugin/tests/run.py test_task_ergonomics test_batch` → exit 0 · Ran 73 tests in 12.5s (11 classes, 16 at a time; slowest: BatchEdit 12s, SplitVerify 10s, Batch 9s) / OK [ran] [tree e9902aaefb2e] [world 2f1906870a] (2026-11-03T20:32:48Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_batch test_cli test_core test_task_ergonomics && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 361 tests in 35.1s (84 classes, 16 at a time; slowest: TaskLifecycle 35s, BatchEdit 25s, CaptureAndIntake 24s) / FAILED (1 classes: test_core.SandboxEnv) [ran] [tree e9902aaefb2e] [world 2f1906870a] (2026-11-03T20:33:25Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_batch test_cli test_core test_task_ergonomics && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 361 tests in 35.0s (84 classes, 16 at a time; slowest: TaskLifecycle 34s, BatchEdit 24s, CaptureAndIntake 23s) / FAILED (1 classes: test_core.SandboxEnv) [ran] [tree e9902aaefb2e] [world 2f1906870a] (2026-11-03T20:33:27Z)
- (ac 1) `CMD''; task new --ac, task ac add, task ac edit --text, fm batch's DONE-WHEN lines and task set --section's criteria all use it, and each accepts both forms — verify with 'python3 plugin/tests/run.py test_task_ergonomics test_cli test_batch` → ✗ exit 127 (never ran: command not found) · bash: command substitution: line 1: unexpected EOF while looking for matching `'' / bash: line 1: CMDpython3: command not found [ran] [tree f2da5f2502e1] [world 2f1906870a] (2026-11-03T20:38:43Z)
- (step 1) `python3 plugin/tests/run.py test_task_ergonomics test_cli test_batch test_core` → exit 0 · Ran 361 tests in 30.1s (84 classes, 16 at a time; slowest: TaskLifecycle 30s, BatchEdit 20s, CaptureAndIntake 19s) / OK [ran] [tree f2da5f2502e1] [world 2f1906870a] (2026-11-03T20:38:43Z)
- (ac 1) `python3 plugin/tests/run.py test_task_ergonomics test_cli test_batch` → exit 0 · Ran 219 tests in 26.0s (55 classes, 16 at a time; slowest: TaskLifecycle 26s, BatchEdit 13s, CaptureAndIntake 12s) / OK [ran] [tree f2da5f2502e1] [world 2f1906870a] (2026-11-03T20:39:20Z)
- `python3 plugin/tests/run.py test_task_ergonomics test_cli test_batch test_core` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T20:38:43Z [ran] [tree f2da5f2502e1] [world 2f1906870a] (2026-11-03T20:39:20Z)
- (audit intent) `self: read the branch diff — core.split_verify (dash form first, then the last ' :: '); five cli sites call it; the --section rewrite keeps checked boxes and converts both forms; stored briefs still read through verify_of` → one parser, so fm batch no longer splits on the first ' :: ' while every other entry point splits on the last [tree f2da5f2502e1] (2026-11-03T20:39:20Z)
- (audit edge) `self: read the branch diff — core.split_verify (dash form first, then the last ' :: '); five cli sites call it; the --section rewrite keeps checked boxes and converts both forms; stored briefs still read through verify_of` → a command containing ' :: ' inside the dash form stays whole; an empty dash command is no verify; ac add's --verify wins over a typed :: part [tree f2da5f2502e1] (2026-11-03T20:39:20Z)
- (audit adversary) `self: read the branch diff — core.split_verify (dash form first, then the last ' :: '); five cli sites call it; the --section rewrite keeps checked boxes and converts both forms; stored briefs still read through verify_of` → parsing only; the verify command still passes _refuse_unrunnable and _lint_verify as before [tree f2da5f2502e1] (2026-11-03T20:39:20Z)
- (audit self) `self: read the branch diff — core.split_verify (dash form first, then the last ' :: '); five cli sites call it; the --section rewrite keeps checked boxes and converts both forms; stored briefs still read through verify_of` → no findings [tree f2da5f2502e1] (2026-11-03T20:39:20Z)
- `python3 plugin/tests/run.py test_task_ergonomics test_cli test_batch test_core` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T20:39:20Z [ran] [tree f2da5f2502e1] [world 2f1906870a] (2026-11-03T20:40:13Z)
- (audit intent) `self: read the branch diff — core.split_verify (dash form first, then the last ' :: '); five cli sites call it; the --section rewrite keeps checked boxes and converts both forms; stored briefs still read through verify_of` → one parser, so fm batch no longer splits on the first ' :: ' while every other entry point splits on the last [tree f2da5f2502e1] (2026-11-03T20:40:13Z)
- (audit edge) `self: read the branch diff — core.split_verify (dash form first, then the last ' :: '); five cli sites call it; the --section rewrite keeps checked boxes and converts both forms; stored briefs still read through verify_of` → a command containing ' :: ' inside the dash form stays whole; an empty dash command is no verify; ac add's --verify wins over a typed :: part [tree f2da5f2502e1] (2026-11-03T20:40:13Z)
- (audit adversary) `self: read the branch diff — core.split_verify (dash form first, then the last ' :: '); five cli sites call it; the --section rewrite keeps checked boxes and converts both forms; stored briefs still read through verify_of` → parsing only; the verify command still passes _refuse_unrunnable and _lint_verify as before [tree f2da5f2502e1] (2026-11-03T20:40:13Z)
- (audit self) `self: read the branch diff — core.split_verify (dash form first, then the last ' :: '); five cli sites call it; the --section rewrite keeps checked boxes and converts both forms; stored briefs still read through verify_of` → no findings [tree f2da5f2502e1] (2026-11-03T20:40:13Z)
## Log
- 2026-11-03T05:35:24Z created
- 2026-11-03T05:36:59Z blocked: waits on T-2786's merge: the fourth copy of the parsing is in that lane
- 2026-11-03T20:24:55Z criterion 1 verify: `CMD`'; task new --ac, task ac add, task ac edit --text, fm batch's DONE-WHEN lines and task set --section's criteria all use it, and each accepts both forms — verify with `python3 plugin/tests/run.py test_task test_cli test_batch` → `python3 plugin/tests/run.py test_task_ergonomics test_cli test_batch`
- 2026-11-03T20:24:55Z criterion 1 text: one helper core.split_verify(text) -> (text, cmd|None) parses 'TEXT :: CMD' (last ' :: ') and 'TEXT → one helper core.split_verify(text) -> (text, cmd|None) parses 'TEXT :: CMD' (last ' :: ') and 'TEXT — verify with `CMD`'; task new --ac, task ac add, task ac edit --text, fm batch's DONE-WHEN lines and task set --section's criteria all use it, and each accepts both forms
- 2026-11-03T20:24:56Z set tier=S
- 2026-11-03T20:24:57Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2789.builder.md
- 2026-11-03T20:25:09Z focused
- 2026-11-03T20:25:09Z predicted from its closes: 1 min, 1 attempt(s)
- 2026-11-03T20:36:10Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a76e6d3ed974941d9 (branch worktree-agent-a76e6d3ed974941d9 kept: not merged)
- 2026-11-03T20:36:10Z focused
- 2026-11-03T20:38:05Z merged worktree-agent-a76e6d3ed974941d9 (4 file(s))
- 2026-11-03T20:38:10Z focused
- 2026-11-03T20:38:49Z criterion 1 verify: `CMD`'; task new --ac, task ac add, task ac edit --text, fm batch's DONE-WHEN lines and task set --section's criteria all use it, and each accepts both forms — verify with `python3 plugin/tests/run.py test_task_ergonomics test_cli test_batch` → `python3 plugin/tests/run.py test_task_ergonomics test_cli test_batch`
- 2026-11-03T20:38:49Z criterion 1 text: one helper core.split_verify(text) -> (text, cmd|None) parses 'TEXT :: CMD' (last ' :: ') and 'TEXT → one helper core.split_verify parses both typed verify forms (the double-colon form, split on its last separator, and the dash 'verify with' form); task new --ac, task ac add, task ac edit --text, fm batch's DONE-WHEN lines and task set --section's criteria all use it
- 2026-11-03T20:40:59Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2786 [FIX S, done, 1 steps] fm task ac ID edit N --text reads a verify command typed in the text: 'TEXT :: CMD' (as add and task new take it) or a trailing '— verify w…
- T-1905 [FIX M, done, 5 steps] CLI parsing: --section forms, a lone-word step, a capture's leading tag — lesson: When a parser accepts a shorthand, test the typo next to …
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- decision 2026-10-31: [revisited: Mission 4: the goal ledger grows fm mandate] Mission 4 as built: the goal ledger lives on fm mandate's record (one standing goal: text, …
## Behaviour lock
none: the builder's existing suites (test_task_ergonomics, test_cli, test_batch: 219 tests) pin the old behaviour and pass unchanged after the refactor; the new SplitVerify tests pin the unified one
## Files touched
- plugin/tests/test_task_ergonomics.py
- plugin/tests/test_batch.py
- plugin/lib/sampo/core.py
- plugin/lib/sampo/cli.py
