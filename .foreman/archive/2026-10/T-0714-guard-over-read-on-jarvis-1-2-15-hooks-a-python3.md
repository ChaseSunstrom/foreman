---
id: T-0714
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T16:28:22Z
updated: 2026-10-09T17:12:25Z
base: 26116343f9e3a04499f0e7192778e2beb4c8daff
base_tree: a2328bd4b18d21e981b392156951055875f9abe1
verified: strong
---
# Guard over-read on JARVIS (1.2.15 hooks): a python3 - <<'EOF' edit script whose strings me
## Raw request
> Guard over-read on JARVIS (1.2.15 hooks): a python3 - <<'EOF' edit script whose strings mention 'at' was refused as 'at schedules a command' (T-0143, jarvis-desktop/notifications.py); check the 1.2.16 guard on that shape and the python-strings-as-commands rule
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a line whose only shell or source reads a file (. .venv/bin/activate, bash script.sh) doesn't read the heredocs fed to python as shell; bash/sh -s/. /dev/stdin/bash -c 'source /dev/stdin' still do — verify with `python3 plugin/tests/run.py -p test_guard_pipes.py -k ShellStdin`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] the JARVIS command as a failing ShellStdin row
2. [x] _stdin_scripts counts only a shell or source that reads stdin as code (_reads_stdin_code)
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_guard_pipes.py -k ShellStdin` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: ShellStdin 0s) / OK [ran] [tree 31ff2ddd259f] (2026-10-09T17:11:11Z)
- (step 1) `python3 plugin/tests/run.py -p test_guard_pipes.py -k ShellStdin` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: ShellStdin 0s) / FAILED (1 classes) [ran] [tree b9c882370721] (2026-10-09T17:11:45Z)
- (step 2) `python3 plugin/tests/run.py -p test_guard_pipes.py -k ShellStdin` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: ShellStdin 0s) / OK [ran] [tree 0b5ed43d03f1] (2026-10-09T17:11:56Z)
- (ac 1) `python3 plugin/tests/run.py -p test_guard_pipes.py -k ShellStdin` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: ShellStdin 0s) / OK [ran] [tree 4ff27c2dc74e] (2026-10-09T17:12:24Z)
- (audit adversary) `self: _stdin_scripts' trigger now asks _reads_stdin_code (T-0716) instead of matching any shell/source name; JARVIS's exact command replayed → allow` → every T-0589/T-0590/T-0669 ShellStdin row still refused (bash, sh -s, bash -, bash /dev/stdin, { bash; }, busybox sh, . /dev/stdin, bash -c 'source /dev/stdin', env/exec/timeout wrappers, $X <<EOF); a file-reading shell (bash ./run.sh, . venv) now leaves python heredocs alone — what that file does with stdin is as unreadable as before [tree 4ff27c2dc74e] (2026-10-09T17:12:24Z)
- (audit edge) `self: _stdin_scripts' trigger now asks _reads_stdin_code (T-0716) instead of matching any shell/source name; JARVIS's exact command replayed → allow` → 0 newly blocked / 0 newly allowed over 5,000 real commands [tree 4ff27c2dc74e] (2026-10-09T17:12:24Z)
- (audit self) `self: _stdin_scripts' trigger now asks _reads_stdin_code (T-0716) instead of matching any shell/source name; JARVIS's exact command replayed → allow` → no findings [tree 4ff27c2dc74e] (2026-10-09T17:12:24Z)
## Log
- 2026-10-09T16:28:22Z created
- 2026-10-09T17:10:59Z set tier=S, type=FIX
- 2026-10-09T17:11:00Z focused
- 2026-10-09T17:12:24Z done
- 2026-10-09T17:12:25Z committed 1e0b573 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0282 [FIX S, done, 0 steps] Guard: parse 'cd DIR && python3 - <<EOF' heredocs like bare ones (an edit script whose str
- research mission-20261009-091631.pack: can you spawn a bunch of brainstorm agents to super recursive brainstorm on capabilities/features for foreman itself? not just sim…
- T-0170 [FIX M, done, 3 steps] Guard: 'driving Foreman's modules' reads real Python imports, not text that mentions them — lesson: Relax a guard by proving the safe case,…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar finished tasks took 0–3 steps
- start here (files T-0170 touched): plugin/tests/test_guard.py, plugin/lib/fmguard.py, CHANGELOG.md, MASTER.md
## Files touched
- plugin/tests/test_guard_pipes.py
- plugin/lib/fmguard.py
- CHANGELOG.md
