---
id: T-1129
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/lib/fmguard.py, plugin/tests/test_hooks.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: discovered
created: 2026-10-16T07:56:21Z
updated: 2026-10-16T08:24:38Z
base: f6cdaaf1a89eb76018f6cf9b908cfef824c67f5d
base_tree: b36127c8b3450d0f4f59911712488d2eb712349e
plan0_at: 2026-10-16T08:14:16Z
plan0_scope: [plugin/lib/fmhooks.py, plugin/lib/fmguard.py, plugin/tests/test_hooks.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Builders report a 'python3 - <<EOF' heredoc hanging the shell tool until timeout (T-1047 a
## Raw request
> Builders report a 'python3 - <<EOF' heredoc hanging the shell tool until timeout (T-1047 and T-1067 lanes, 2026-10-16): find the shape (empty body? delimiter never matched? stdin held open?) and have the guard or a hint stop it before it hangs
## Interpretation
Both builders' hangs were a bare stdin reader: 'cat > /tmp/x' and 'cat > /dev/null' with nothing feeding them. The Bash tool's stdin never closes, so the call waits until its 120 s timeout and is then backgrounded forever.
## Assumptions (confidence)
## Acceptance criteria
- [x] a bare 'cat > f', 'python3 -' or 'bash' with nothing on stdin is denied naming how to feed it; fed, piped, redirected, filed and compound forms pass — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
A PreToolUse check beside _wait_loop: a top-level cat (no file operand, or '-'), tee, python (no script, -c or -m), or a shell (no script or -c) that has no pipe, heredoc, here-string or < redirect is denied with how to feed it. Compound commands (while/for/{ }/( )) are skipped, because their input redirect sits on the closing word. The guard's tokenizer records '<' as Cmd.stdin.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test, then the stdin check in PreToolUse
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks test_guard` → exit 0 · Ran 269 tests in 35.7s (68 classes, 16 at a time; slowest: Stop 36s, PreToolUse 21s, SessionStart 15s) / OK [ran] [tree 546c803d35a1] (2026-10-16T08:21:53Z)
- `python3 plugin/tests/run.py test_hooks` → ✗ exit 1 · Ran 157 tests in 34.5s (20 classes, 16 at a time; slowest: Stop 34s, PreToolUse 19s, SessionStart 13s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 546c803d35a1] (2026-10-16T08:23:02Z)
- `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 157 tests in 34.2s (20 classes, 16 at a time; slowest: Stop 34s, PreToolUse 19s, SessionStart 13s) / OK [ran] [tree 546c803d35a1] (2026-10-16T08:23:02Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 157 tests in 35.1s (20 classes, 16 at a time; slowest: Stop 35s, PreToolUse 20s, SessionStart 14s) / OK [ran] [tree 4d419ef7d248] (2026-10-16T08:23:38Z)
- (audit adversary) `self + adversary + replay: a week of recorded Bash commands (30,507 across all projects and subagents) replayed through _stdin_hang: 22 denied, every one a real stdin hang (cat > /tmp/x, cat >> /dev/null, python3 - with no heredoc); the false positives found on the way (2>/dev/null's fd read as a file, python3 --version) are fixed and pinned in the test. Guard change is one attribute (Cmd.stdin from <), no decision path reads it but this check` → only a deny that saves a hang; it can't allow anything the guard refuses (it runs after the guard in the chain) [tree 4d419ef7d248] (2026-10-16T08:23:38Z)
- (audit self) `self + adversary + replay: a week of recorded Bash commands (30,507 across all projects and subagents) replayed through _stdin_hang: 22 denied, every one a real stdin hang (cat > /tmp/x, cat >> /dev/null, python3 - with no heredoc); the false positives found on the way (2>/dev/null's fd read as a file, python3 --version) are fixed and pinned in the test. Guard change is one attribute (Cmd.stdin from <), no decision path reads it but this check` → no findings [tree 4d419ef7d248] (2026-10-16T08:23:38Z)
## Log
- 2026-10-16T07:56:21Z created
- 2026-10-16T08:14:15Z set scope=['plugin/lib/fmhooks.py', 'plugin/lib/fmguard.py', 'plugin/tests/test_hooks.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-16T08:14:16Z focused
- 2026-10-16T08:23:03Z scope: CHANGELOG.md, MASTER.md — docs
- 2026-10-16T08:24:37Z done
- 2026-10-16T08:24:38Z committed 8dda9ee (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0369 [FIX M, done, 2 steps] Guard: pin the pipe proof's strictness (premise of a self-improvement finding was false) — lesson: Before widening a guard from a friction …
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- research T-0384-review: Changes needed.** I found four concrete bypasses by reading the code. I could not run bash or the tests, because I only had read tools. For each …
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar past tasks were M: consider --tier M
- the similar finished task took 2 steps
- likely tests for the scope: plugin/tests/test_guard.py, plugin/tests/test_hooks.py
## Lessons
- Validate a new pre-run check by replaying real recorded commands through it before trusting a hand-made test list
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmguard.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
