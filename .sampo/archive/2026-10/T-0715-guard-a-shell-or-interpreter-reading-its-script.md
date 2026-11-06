---
id: T-0715
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T16:32:20Z
updated: 2026-10-09T16:34:23Z
base: 566e5e66ac15df285f69a894d39442e6bcd943e4
base_tree: ec9d64e4de6823500cc3fc1880eb2a72239cdcf3
verified: strong
---
# Guard: a shell or interpreter reading its script from a pipe is refused (echo 'rm -rf ~' | bash ran unread)
## Raw request
> Guard: a shell or interpreter reading its script from a pipe is refused (echo 'rm -rf ~' | bash ran unread)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a pipe into bash/sh/python/node/perl with no script, -c or -e is refused; -c, -m, a script file and a heredoc are unchanged — verify with `python3 plugin/tests/run.py -k PipeIntoShell`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: PipeIntoShell rows
2. [x] check_bash: _reads_stdin_code for a command after a pipe
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k PipeIntoShell` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: PipeIntoShell 0s) / FAILED (1 classes) [ran] [tree 815952696131] (2026-10-09T16:32:29Z)
- (step 2) `python3 plugin/tests/run.py -k PipeIntoShell -k AnyDownload` → exit 0 · Ran 2 tests in 0.2s (2 classes, 16 at a time; slowest: AnyDownload 0s, PipeIntoShell 0s) / OK [ran] [tree 206b5c1d8ac6] (2026-10-09T16:34:17Z)
- (step 1) `python3 plugin/tests/run.py -k PipeIntoShell` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: PipeIntoShell 0s) / OK [ran] [tree 206b5c1d8ac6] (2026-10-09T16:34:23Z)
- (ac 1) `python3 plugin/tests/run.py -k PipeIntoShell` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: PipeIntoShell 0s) / OK [ran] [tree 206b5c1d8ac6] (2026-10-09T16:34:23Z)
- (audit adversary) `self: PipeIntoShell rows red then green; guard, pipes and diff suites green; 30-day replay 0 newly blocked, 0 newly allowed (no real command pipes into a shell)` → shells (incl. busybox sh, -s, /dev/stdin), python/node/perl/ruby/php without inline code, and source /dev/stdin; a download piped in keeps the grantable pipe-shell category [tree 206b5c1d8ac6] (2026-10-09T16:34:23Z)
- (audit self) `self: PipeIntoShell rows red then green; guard, pipes and diff suites green; 30-day replay 0 newly blocked, 0 newly allowed (no real command pipes into a shell)` → no findings [tree 206b5c1d8ac6] (2026-10-09T16:34:23Z)
## Log
- 2026-10-09T16:32:20Z created
- 2026-10-09T16:32:20Z focused
- 2026-10-09T16:34:23Z done
- 2026-10-09T16:34:23Z committed da3071d (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0411-review: Verdict: changes needed.** I found three bypasses in `_expand_literal_loops`. I could not run bash (read-only), so each one is traced from the co…
- research T-0384-review: Changes needed.** I found four concrete bypasses by reading the code. I could not run bash or the tests, because I only had read tools. For each …
- T-0421 [SECURITY M, done, 3 steps] Guard: any download on the line counts when a shell reads a pipe — lesson: Check the property (a download reaches a shell; a word may …
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- similar past tasks were M: consider --tier M
## Lessons
- every way a shell gets its program (argument, -c, file, heredoc, here-string, pipe) needs a reading or a refusal; enumerate them once
## Files touched
- plugin/tests/test_guard_pipes.py
- plugin/lib/fmguard.py
- CHANGELOG.md
