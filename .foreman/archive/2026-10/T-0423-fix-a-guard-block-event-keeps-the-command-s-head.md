---
id: T-0423
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-09T14:00:49Z
updated: 2026-10-09T14:12:01Z
base: df9d352930915cf2cdde0429368def670e699d6e
base_tree: c91ec4130a62a0b43431262f5d8b02ea743c0e49
verified: strong
---
# A guard_block event keeps the part of the command that tripped it
## Raw request
> FIX: a guard_block event keeps the command's head (c.fit(cmd,160), fmhooks.py:770), not the part that tripped it: two $R blocks showed only a heredoc head and a gate pipe, so the digest can't explain them. Store a window around the blocked target in the event's cmd (done when a block on 'echo x; git -C $R reset' carries $R)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a block on 'echo x; git -C $R reset' records $R in the event's cmd — verify with `python3 plugin/tests/run.py -k test_block_event_keeps_the_tripping_part`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first, then a window around the blocked target in fmhooks' guard_block event
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_block_event_keeps_the_tripping_part` → ✗ exit 1 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: PreToolUse 0s) / FAILED (1 classes) [ran] [tree 5cbf67b48bcb] (2026-10-09T14:07:57Z)
- (step 1) `python3 plugin/tests/run.py -k test_block_event_keeps_the_tripping_part` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: PreToolUse 0s) / OK [ran] [tree 0efc4505ce46] (2026-10-09T14:08:19Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (29 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                34.1    43.1     150  [0] / SessionEnd                  31.5    36.0     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 13:13 UTC; python3 plugin/tests/run.py → exit 0 · Ran 967 tests in [ran] [tree 0efc4505ce46] (2026-10-09T14:11:11Z)
- (ac 1) `python3 plugin/tests/run.py -k test_block_event_keeps_the_tripping_part` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: PreToolUse 0s) / OK [ran] [tree e0ea593c021e] (2026-10-09T14:11:54Z)
- (audit edge) `builder branch read (one helper, _window, and its call); red→green recorded by the builder; merged; criterion rerun OK` → a known variable's detail names the path, so the window lands on the assignment, which still explains the block; the window is cut after redaction [tree e0ea593c021e] (2026-10-09T14:11:54Z)
- (audit self) `builder branch read (one helper, _window, and its call); red→green recorded by the builder; merged; criterion rerun OK` → no findings [tree e0ea593c021e] (2026-10-09T14:11:54Z)
- (audit adversary) `builder branch read (one helper, _window, and its call); red→green recorded by the builder; merged; criterion rerun OK` → this task changes only an event's logged text (after redaction); the guard files in its diff range are T-0414/T-0421/T-0422's commits, adversary-reviewed there [tree e0ea593c021e] (2026-10-09T14:12:01Z)
- (audit edge) `builder branch read (one helper, _window, and its call); red→green recorded by the builder; merged; criterion rerun OK` → a known variable's detail names the path, so the window lands on the assignment, which still explains the block [tree e0ea593c021e] (2026-10-09T14:12:01Z)
- (audit self) `builder branch read (one helper, _window, and its call); red→green recorded by the builder; merged; criterion rerun OK` → no findings [tree e0ea593c021e] (2026-10-09T14:12:01Z)
## Log
- 2026-10-09T14:00:49Z created
- 2026-10-09T14:06:05Z planned from capture
- 2026-10-09T14:06:22Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0423.builder.md
- 2026-10-09T14:06:37Z focused
- 2026-10-09T14:11:40Z merged worktree-agent-a42debe1df60bbe20 (2 file(s))
- 2026-10-09T14:11:40Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a42debe1df60bbe20
- 2026-10-09T14:11:53Z focused
- 2026-10-09T14:11:54Z paused: focus moved to T-0428
- 2026-10-09T14:12:01Z focused
- 2026-10-09T14:12:01Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-pass-20261009b: 1. **Answer.** I could ground three improvements. The biggest is that the guard-block log records the wrong part of the command. That made t…
- research rsi-pass-20261008: 1. **Answer.** I could ground one improvement fully (the pipe-shell false block) and one partly (state-direct from guessed variable targets).…
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
## Lessons
- Log what tripped the check, not what the line started with.
## Files touched
- .claude/worktrees/agent-a42debe1df60bbe20/plugin/tests/test_hooks.py
- .claude/worktrees/agent-a42debe1df60bbe20/plugin/lib/fmhooks.py
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
- plugin/lib/fmguard.py
- plugin/lib/fmhooks.py
- plugin/lib/fmlanes.py
- plugin/tests/test_builder.py
- plugin/tests/test_guard.py
- plugin/tests/test_guard_diff.py
- plugin/tests/test_guard_pipes.py
- plugin/tests/test_hooks.py
