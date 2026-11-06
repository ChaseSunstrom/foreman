---
id: T-1839
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-28T15:28:30Z
updated: 2026-10-28T15:39:20Z
base: f275832d027e350d814d5da0eac513492a3f7a49
base_tree: 9f2683ca334923e568ac871658ae7a97ed2de489
plan0_at: 2026-10-28T15:28:31Z
plan0_scope: []
verified: strong
---
# A pgrep -f/pkill -f whose pattern matches its own command is refused
## Raw request
> A pgrep -f/pkill -f whose pattern matches its own command is refused
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the pre-tool hook refuses pgrep -f/pkill -f whose pattern matches the command text, foreground or background, and names the fix — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_hooks.py, then the _self_match rule beside _wait_loop
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -4` → exit 0 · Ran 204 tests in 55.9s (26 classes, 16 at a time; slowest: Stop 55s, NoTaskGate 42s, PreToolUse 37s) / OK [ran] [tree ef598864a62d] (2026-10-28T15:30:45Z)
- (step 1) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -4` → exit 0 · Ran 204 tests in 55.9s (26 classes, 16 at a time; slowest: Stop 55s, NoTaskGate 42s, PreToolUse 37s) / OK [ran] [tree ef598864a62d] (2026-10-28T15:30:45Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks 2>&1 | grep -E "^FAIL|failures|^OK" | head -3` → ✗ exit 1 · FAILED (failures=1) / FAILED (1 classes) [ran] [tree 1a76788d395e] (2026-10-28T15:31:50Z)
- `python3 plugin/tests/run.py test_hooks` → ✗ exit 1 · Ran 204 tests in 40.8s (26 classes, 16 at a time; slowest: Stop 40s, NoTaskGate 27s, PreToolUse 22s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree f4b42285f9f9] (2026-10-28T15:34:54Z)
- `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 204 tests in 40.4s (26 classes, 16 at a time; slowest: Stop 40s, NoTaskGate 27s, PreToolUse 23s) / OK [ran] [tree f4b42285f9f9] (2026-10-28T15:34:54Z)
- (step 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 204 tests in 41.6s (26 classes, 16 at a time; slowest: Stop 41s, NoTaskGate 29s, PreToolUse 24s) / OK [ran] [tree 69933440133f] (2026-10-28T15:37:30Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 204 tests in 40.1s (26 classes, 16 at a time; slowest: Stop 40s, NoTaskGate 27s, PreToolUse 23s) / OK [ran] [tree 69933440133f] (2026-10-28T15:38:34Z)
- (audit intent) `self review of the diff: the rule runs only in command position, skips -x, a bracketed letter and a grep -v filter; replayed on 78,307 recorded commands, 224 denied, all self-matches; regex cost per Bash call is one finditer` → the user asked that a self-inflicted idle never recur; the hook now refuses the exact watcher and pkill that caused it, with the fix named [tree 69933440133f] (2026-10-28T15:38:34Z)
- (audit edge) `self review of the diff: the rule runs only in command position, skips -x, a bracketed letter and a grep -v filter; replayed on 78,307 recorded commands, 224 denied, all self-matches; regex cost per Bash call is one finditer` → multi-line commands (re.M), --full, -af combined flags, quoted and bare patterns, a mention inside a commit message passes, an invalid regex falls back to a substring test [tree 69933440133f] (2026-10-28T15:38:34Z)
- (audit operator) `self review of the diff: the rule runs only in command position, skips -x, a bracketed letter and a grep -v filter; replayed on 78,307 recorded commands, 224 denied, all self-matches; regex cost per Bash call is one finditer` → the refusal names three working forms, so a denied wait costs one retry, not a guess [tree 69933440133f] (2026-10-28T15:38:34Z)
- (audit self) `self review of the diff: the rule runs only in command position, skips -x, a bracketed letter and a grep -v filter; replayed on 78,307 recorded commands, 224 denied, all self-matches; regex cost per Bash call is one finditer` → no findings [tree 69933440133f] (2026-10-28T15:38:34Z)
## Log
- 2026-10-28T15:28:30Z created
- 2026-10-28T15:28:31Z focused
- 2026-10-28T15:37:53Z scope: CHANGELOG.md and MASTER.md document the new refusal
- 2026-10-28T15:39:18Z done
- 2026-10-28T15:39:20Z committed 502ed21c (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0369 [FIX M, done, 2 steps] Guard: pin the pipe proof's strictness (premise of a self-improvement finding was false) — lesson: Before widening a guard from a friction …
- research T-0978-small-models: Measured, not guessed. Sources: two recorded Sonnet demo sessions (T-0979; T-0983/T-0984 were written by them), one [stale: plugin/tests/ru…
- research rsi-pass-20261008: 1. **Answer.** I could ground one improvement fully (the pipe-shell false block) and one partly (state-direct from guessed variable targets).…
- decision 2026-10-22: T-1585: the guard refuses commands that name CLAUDECODE or CLAUDE_CODE_ENTRYPOINT to unset or override them, not a whole fresh environment (env -i, …
## Why not caught
T-0426's wait rule refused only foreground sleep loops and let background ones through, trusting the completion notice; a loop that matches its own shell never completes, so no notice came
## Lessons
- A background wait is only safe if it can end: a process match must not see its own command line
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
