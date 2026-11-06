---
id: T-1766
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_speed.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-23T08:55:19Z
updated: 2026-10-23T08:57:31Z
base: b9c60a4caffa741c42b332a908824c97ee0e67ad
base_tree: f19db8d6b125df1ff8ed043fe98205d0356a9dfd
plan0_at: 2026-10-23T08:55:30Z
plan0_scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_speed.py, CHANGELOG.md]
verified: strong
---
# fm quiet runs its command with no stdin, so a heredoc script fed to it does nothing and reports exit 0
## Raw request
> fm quiet runs its command with no stdin, so a heredoc script fed to it does nothing and reports exit 0
## Interpretation
fm quiet runs commands through run_command, which gives the child /dev/null as stdin (so a command never waits on an agent's pipe that may never close). A script fed by heredoc (fm quiet -- python3 - <<EOF) then runs nothing and reports ✓ exit 0: found when T-1765's changelog line silently didn't land. Pass fm quiet's own stdin through when it is a regular file or a pipe with data or EOF ready now; anything else (a terminal, /dev/null, an idle open pipe) keeps /dev/null.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm quiet passes its own stdin when it is a file or a pipe with data waiting (a heredoc), and an idle open pipe still never blocks the command — verify with `python3 plugin/tests/run.py test_speed`
## Non-goals
## Approach (options → choice → why)
Options: refuse a command that names '-' (misses cat, bash -s); always inherit stdin (an idle agent pipe would block a reader until the timeout); pass stdin only when it's a file or a ready pipe (select, 50 ms). Choice: the last; run_command gains a stdin parameter, default /dev/null, so every other caller is unchanged.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: heredoc reaches the command; idle pipe doesn't hang
2. [x] run_command stdin param; fm quiet passes a ready stdin; CHANGELOG (also T-1765's missed line)
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_speed` → ✗ exit 1 · Ran 10 tests in 3.7s (1 classes, 16 at a time; slowest: Speed 3s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree b0cb28a834d8] (2026-10-23T08:55:58Z)
- `python3 plugin/tests/run.py test_speed` → ✗ exit 1 · Ran 10 tests in 3.0s (1 classes, 16 at a time; slowest: Speed 3s) / FAILED (1 classes) [ran] [tree b0cb28a834d8] (2026-10-23T08:55:58Z)
- `python3 plugin/tests/run.py test_speed` → ✗ exit 1 · Ran 10 tests in 3.8s (1 classes, 16 at a time; slowest: Speed 3s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree b954fcc3e775] (2026-10-23T08:56:18Z)
- `python3 plugin/tests/run.py test_speed` → exit 0 · Ran 10 tests in 3.1s (1 classes, 16 at a time; slowest: Speed 3s) / OK [ran] [tree b954fcc3e775] (2026-10-23T08:56:18Z)
- (step 1) `python3 plugin/tests/run.py test_speed` → exit 0 · Ran 10 tests in 5.3s (1 classes, 16 at a time; slowest: Speed 5s) / OK [ran] [tree 9eb210c6747e] (2026-10-23T08:56:32Z)
- (step 2) `python3 plugin/tests/run.py test_speed test_verify_strength test_doctor` → exit 0 · Ran 92 tests in 15.2s (25 classes, 16 at a time; slowest: VerifyStrength 15s, Repeat 8s, Speed 4s) / OK [ran] [tree 9eb210c6747e] (2026-10-23T08:56:48Z)
- (ac 1) `python3 plugin/tests/run.py test_speed` → exit 0 · Ran 10 tests in 5.0s (1 classes, 16 at a time; slowest: Speed 5s) / OK [ran] [tree 9eb210c6747e] (2026-10-23T08:57:00Z)
- (audit edge) `self review; live: a file on stdin runs the script, a bare fm quiet -- cat ends at once; test_speed, test_verify_strength, test_doctor green` → an idle open pipe (the test keeps one open) still gets /dev/null, so cat ends; a terminal or /dev/null stdin is never read [tree 9eb210c6747e] (2026-10-23T08:57:00Z)
- (audit self) `self review; live: a file on stdin runs the script, a bare fm quiet -- cat ends at once; test_speed, test_verify_strength, test_doctor green` → no findings [tree 9eb210c6747e] (2026-10-23T08:57:00Z)
## Log
- 2026-10-23T08:55:19Z created
- 2026-10-23T08:55:26Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmcore.py', 'plugin/tests/test_speed.py', 'CHANGELOG.md']
- 2026-10-23T08:55:29Z focused
- 2026-10-23T08:56:55Z scope: CHANGELOG also takes T-1765's line, which its fm quiet heredoc never wrote (this bug)
- 2026-10-23T08:57:29Z done
- 2026-10-23T08:57:31Z committed 19689171 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0369 [FIX M, done, 2 steps] Guard: pin the pipe proof's strictness (premise of a self-improvement finding was false) — lesson: Before widening a guard from a friction …
- T-1129 [FIX S, done, 1 steps] Builders report a 'python3 - <<EOF' heredoc hanging the shell tool until timeout (T-1047 a — lesson: Validate a new pre-run check by replay…
- playbook Terminal and mod UI (fm playbooks show ui/terminal-ui)
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar finished tasks took 1–2 steps
- start here (files T-0369 touched): plugin/tests/test_guard.py, plugin/lib/fmguard.py
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py
## Why not caught
no test fed fm quiet a stdin: every caller passed a command, never a script on stdin
## Lessons
- A wrapper that swaps stdin for /dev/null must say so or pass a ready stdin through: a script read from stdin then succeeds by doing nothing
## Files touched
- plugin/tests/test_speed.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- CHANGELOG.md
