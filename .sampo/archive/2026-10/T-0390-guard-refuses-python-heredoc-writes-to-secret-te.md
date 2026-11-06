---
id: T-0390
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T01:59:05Z
updated: 2026-10-09T02:13:38Z
base: 53230ae6c2e68187e39b7864d57a6a0e905ffcf9
base_tree: 46a74688ef61dd80c94de952af917145a7d0dbd7
verified: strong
---
# Guard refuses python-heredoc writes to secret templates (JARVIS T-0274: secrets.yaml.example 'written from interpreter code' after 1.2.4)
## Raw request
> Guard refuses python-heredoc writes to secret templates (JARVIS T-0274: secrets.yaml.example 'written from interpreter code' after 1.2.4)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a python heredoc that rewrites .env.example and config/secrets.yaml.example passes; one writing config/secrets.yaml is still refused — verify with `python3 plugin/tests/run.py -k test_interpreter_writes_to_secret_templates`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] reproduce with the JARVIS command, find the interpreter-write path, fix test-first
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_interpreter_writes_to_secret_templates` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: PreToolUse 0s) / OK [ran] [tree 1964906dbff8] (2026-10-09T02:12:50Z)
- (ac 1) `python3 plugin/tests/run.py -k test_interpreter_writes_to_secret_templates` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: PreToolUse 0s) / OK [ran] [tree 1964906dbff8] (2026-10-09T02:13:38Z)
- (audit intent) `self: reproduced on JARVIS with the hook's own guard context; 1.2.4 finds nothing; root cause was the deploy target, not the guard` → JARVIS's template rewrite passes on 1.2.4 (hook-path test); the deploy now targets the folder the session loads [tree 1964906dbff8] (2026-10-09T02:13:38Z)
- (audit edge) `self: reproduced on JARVIS with the hook's own guard context; 1.2.4 finds nothing; root cause was the deploy target, not the guard` → the real secrets.yaml stays credentials (test_guard ScratchNames); the hook harness's repo sits under scratch, so it can't assert that [tree 1964906dbff8] (2026-10-09T02:13:38Z)
- (audit self) `self: reproduced on JARVIS with the hook's own guard context; 1.2.4 finds nothing; root cause was the deploy target, not the guard` → no findings [tree 1964906dbff8] (2026-10-09T02:13:38Z)
## Log
- 2026-10-09T01:59:05Z created
- 2026-10-09T01:59:05Z focused
- 2026-10-09T02:12:44Z result: not a guard bug — 1.2.4's guard (hook context rebuilt on JARVIS, grant removed in memory) finds nothing in the exact command. Root cause: the JARVIS session runs Foreman from its Folder marketplace source ~/.claude/foreman (a clone at 1.2.3), not the cache folders I synced, so 1.2.4 never reached it; fixed by updating that folder at 02:12. The hook-path test locks the template case; capturing version visibility so a deploy can't miss the live folder again.
- 2026-10-09T02:13:38Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0386 [FIX S, done, 1 steps] FIX: the guard refuses writes to secret-name templates (jarvis-core/config/secrets.yaml.ex
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- T-0176 [FIX M, done, 3 steps] Guard: a python heredoc that provably writes only through open() counts only those files as written — lesson: Prove a relaxation by allowli…
- decision 2026-10-08: T-0368: entry points re-exec under a saved supported Python
- similar finished tasks took 1–3 steps
- start here (files T-0386 touched): plugin/tests/test_guard.py, plugin/lib/fmguard.py, CHANGELOG.md
## Regression test
test_interpreter_writes_to_secret_templates (test_hooks): the exact JARVIS command through the PreToolUse hook passes on 1.2.4. It was never red here: the refusal came from 1.2.3 code on JARVIS, not from this tree.
## Lessons
- Before saying a fix is live on another machine, prove the running session loads the folder you changed (a fresh bytecode rebuild there after its next tool call), not just that the folder holds the new code
## Files touched
- plugin/tests/test_hooks.py
