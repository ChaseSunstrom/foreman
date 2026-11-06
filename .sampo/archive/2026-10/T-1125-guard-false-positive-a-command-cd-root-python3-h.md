---
id: T-1125
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py]
depends_on: []
source: discovered
created: 2026-10-16T06:57:51Z
updated: 2026-10-16T07:51:58Z
base: d6de8f02f8bf2db98b0d32812edcda115c8b0e84
base_tree: 168cc5744727f494121d09acf10eeb888ad3c90d
plan0_at: 2026-10-16T07:48:59Z
plan0_scope: []
verified: strong
---
# Guard false positive: a command 'cd ROOT && python3 heredoc writing CHANGELOG.md (relative
## Raw request
> Guard false positive: a command 'cd ROOT && python3 heredoc writing CHANGELOG.md (relative) ... && fm task finish ... --run "python3 ... && cd mods/foreman-ui && ..."' was refused as a write to ROOT/state/CHANGELOG.md; the quoted cd inside an argument (or the heredoc's relative path) is resolved against the wrong directory
## Interpretation
A command that cds to the Foreman root, edits CHANGELOG.md through a python heredoc with a relative path, then runs fm task finish with a quoted --run holding another cd, was refused as a write to ROOT/state/CHANGELOG.md. The relative path resolves against the wrong directory.
## Assumptions (confidence)
## Acceptance criteria
- [x] the reported shape (cd ROOT && python3 heredoc writing relative CHANGELOG.md, then fm task finish --run quoting a cd) is allowed; the same heredoc writing state/x.json still refused — verify with `python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
Reproduce in a GuardCase test, find where the cwd for heredoc path resolution comes from, and resolve relative heredoc paths against the cwd the shell has when the interpreter starts (the cd before it, never a cd quoted inside a later argument).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Repro test, then fix the cwd used for heredoc paths
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 113 tests in 6.0s (49 classes, 16 at a time; slowest: GuardAgainstBash 6s, Hook 2s, Proxy 1s) / OK [ran] [tree 49c2dc4f3911] (2026-10-16T07:51:05Z)
- `python3 plugin/tests/run.py test_guard` → ✗ exit 1 · Ran 113 tests in 5.3s (49 classes, 16 at a time; slowest: GuardAgainstBash 5s, Hook 2s, Proxy 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 49c2dc4f3911] (2026-10-16T07:51:24Z)
- `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 113 tests in 5.0s (49 classes, 16 at a time; slowest: GuardAgainstBash 5s, Hook 2s, Proxy 1s) / OK [ran] [tree 49c2dc4f3911] (2026-10-16T07:51:24Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 113 tests in 5.0s (49 classes, 16 at a time; slowest: GuardAgainstBash 5s, Hook 2s, Proxy 1s) / OK [ran] [tree f6a34924c730] (2026-10-16T07:51:29Z)
- (audit adversary) `self + adversary: replaying the reported command through the real hook from the repo root, mods/foreman-ui and plugin/tests allows it; from state/ it is refused because the relative path really is state/CHANGELOG.md. So the block was correct and only the message changes: nothing is loosened` → message-only change; the decision path (_interpreter_writes, classify_write) is untouched, guard suite 113/113 [tree f6a34924c730] (2026-10-16T07:51:29Z)
- (audit self) `self + adversary: replaying the reported command through the real hook from the repo root, mods/foreman-ui and plugin/tests allows it; from state/ it is refused because the relative path really is state/CHANGELOG.md. So the block was correct and only the message changes: nothing is loosened` → no findings [tree f6a34924c730] (2026-10-16T07:51:29Z)
## Log
- 2026-10-16T06:57:51Z created
- 2026-10-16T07:48:58Z focused
- 2026-10-16T07:50:59Z set scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py']
- 2026-10-16T07:51:24Z scope: CHANGELOG.md — release note
- 2026-10-16T07:51:58Z done
- 2026-10-16T07:51:58Z committed 1e5f230 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0774 [FIX S, done, 2 steps] Guard: heredoc python started by 'cd DIR && python3 -' resolves its relative open() targets in DIR only — lesson: a guard relaxation that t…
- T-0698 [FIX M, done, 4 steps] Friction batch 2026-10-09: IFS false block from heredoc data, an undefined-name gate, MASTER.md read hint, builder refused-command list — l…
- T-0175 [SECURITY L, done, 3 steps] Guard: writes through a variable are checked — known NAME=literal values and $HOME resolve write, copy and cd targets (&& chains too);…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar finished tasks took 2–4 steps
- start here (files T-0774 touched): plugin/tests/test_guard.py, plugin/lib/fmguard.py
## Lessons
- Before calling a guard block a false positive, replay it through the real hook with the shell's real cwd
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
