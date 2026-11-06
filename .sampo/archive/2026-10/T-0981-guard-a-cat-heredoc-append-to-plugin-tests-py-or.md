---
id: T-0981
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-15T22:26:15Z
updated: 2026-10-15T22:29:03Z
base: 70e4b37be070ccc08d25aa015d1c00261770506e
base_tree: 300fa0527f5d7179014bf0485d447240648bc3ad
verified: strong
---
# Guard: a cat >> heredoc append to plugin/tests/*.py (or a worktree's plugin/{lib,tests}) i
## Raw request
> Guard: a cat >> heredoc append to plugin/tests/*.py (or a worktree's plugin/{lib,tests}) is read as interpreter code driving Foreman (7 blocks this week); _writes_unrun_source (fmguard ~1273) should exempt test files and worktree copies, keeping the one-target rule; also accept <<"EOF"
## Interpretation
A quoted-heredoc append to a Foreman test file, or to a builder worktree's copy of plugin/lib or plugin/tests, is a source edit, not interpreter code driving Foreman; the guard blocked it 7 times this week.
## Assumptions (confidence)
## Acceptance criteria
- [x] cat >> plugin/tests/test_x.py <<'EOF', the same into a worktree's plugin/lib or plugin/tests, and <<"EOF" are not driving Foreman; running or importing what was written, and an unquoted marker, still are — verify with `python3 plugin/tests/run.py -k test_writing_a_foreman_source_file_is_not_driving_it`
## Non-goals
## Approach (options → choice → why)
Options: widen _writes_unrun_source to plugin/tests and to .claude/worktrees/*/plugin/{core dirs,tests}, and accept a double-quoted marker (chosen: the one-target rule and the unquoted-marker block stay); drop the driving check for heredocs (loses the T-0761 protection).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing cases in the T-0761 test
2. [x] Widen _writes_unrun_source; MASTER line
## Resume here
## Docs impact
none: guard internals; the T-0761 note in MASTER covers the rule
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_writing_a_foreman_source_file_is_not_driving_it` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / FAILED (1 classes) [ran] [tree d49dabfc6060] (2026-10-15T22:27:41Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_git test_guard_pipes` → exit 0 · Ran 104 tests in 4.9s (44 classes, 16 at a time; slowest: GuardAgainstBash 5s, Hook 2s, RuleIds 0s) / OK [ran] [tree 889d47aabefe] (2026-10-15T22:28:48Z)
- (ac 1) `python3 plugin/tests/run.py -k test_writing_a_foreman_source_file_is_not_driving_it` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / OK [ran] [tree 889d47aabefe] (2026-10-15T22:28:49Z)
- (step 1) `python3 plugin/tests/run.py -k test_writing_a_foreman_source_file_is_not_driving_it` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / OK [ran] [tree 889d47aabefe] (2026-10-15T22:28:49Z)
- (audit self) `self: red then green; the run-it, import-it, scratch-path and unquoted-marker cases still block` → quoted heredoc appends to plugin tests and worktree copies are source edits, not driving Foreman; the one-target rule stays [tree 889d47aabefe] (2026-10-15T22:28:49Z)
- `python3 plugin/tests/run.py -k test_writing_a_foreman_source_file_is_not_driving_it` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / OK [ran] [tree 889d47aabefe] (2026-10-15T22:29:02Z)
- (audit self) `self: red then green; the run-it, import-it, scratch-path and unquoted-marker cases still block` → quoted heredoc appends to plugin tests and worktree copies are source edits, not driving Foreman; the one-target rule stays [tree 889d47aabefe] (2026-10-15T22:29:02Z)
- (audit adversary) `self: red then green; the run-it, import-it, scratch-path and unquoted-marker cases still block` → the exemption only lifts the 'driving Foreman' block for a quoted (non-expanding) body written to one file that the command never names again; the path is a realpath under Foreman's home (no .. or symlink escape); writing a test then running the suite was already possible in two steps with the Write tool, and the suite runs in a throwaway FOREMAN_HOME; core-path write rules still apply to the main checkout [tree 889d47aabefe] (2026-10-15T22:29:02Z)
## Log
- 2026-10-15T22:26:15Z created
- 2026-10-15T22:27:33Z focused
- 2026-10-15T22:29:02Z done
- 2026-10-15T22:29:03Z committed d585092 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0940 [FIX M, done, 6 steps] Guard false blocks from the friction pass: cd; heredoc message, reset --soft, plugin update message, git fetch — lesson: Friction digests p…
- T-0761 [FIX S, dropped, 2 steps] Guard: a data heredoc that writes a Foreman source file isn't interpreter code driving Foreman
- T-0766 [FIX S, done, 2 steps] Guard: a data heredoc that writes a Foreman source file isn't interpreter code driving Foreman — lesson: a guard relaxation keyed on what a…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar finished tasks took 2–6 steps
## Plan gaps
- failed first: step 1 Failing cases in the T-0761 test
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
