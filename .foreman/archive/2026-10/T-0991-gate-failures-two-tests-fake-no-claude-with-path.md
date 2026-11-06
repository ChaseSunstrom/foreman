---
id: T-0991
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/tests/test_research_rigor.py,plugin/tests/test_second.py,plugin/tests/test_onwrite.py]
depends_on: []
source: user
created: 2026-10-15T23:28:08Z
updated: 2026-10-15T23:29:27Z
base: c61d072a04315819197f68e494c7b0fb7890be8b
base_tree: 0410d08e470de16fdbf84735e1a15caec1b0972c
verified: strong
---
# Gate failures: two tests fake 'no claude' with PATH alone (T-0990 now finds ~/.local/bin), and the PostToolUseValidate matcher test predates T-0972
## Raw request
> Gate failures: two tests fake 'no claude' with PATH alone (T-0990 now finds ~/.local/bin), and the PostToolUseValidate matcher test predates T-0972
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the three tests pass and fm check is green — verify with `python3 plugin/tests/run.py -k Cache -k Second -k OnWrite`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fix the tests
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k Cache -k OnWrite` → ✗ exit 1 · Ran 14 tests in 30.9s (2 classes, 16 at a time; slowest: Cache 31s, OnWrite 7s) / FAILED (2 classes) [ran] [tree 0410d08e470d] (2026-10-15T23:28:40Z)
- (step 1) `python3 plugin/tests/run.py -k Cache -k Second -k OnWrite` → exit 0 · Ran 14 tests in 6.9s (2 classes, 16 at a time; slowest: OnWrite 7s, Cache 1s) / OK [ran] [tree c2eed7c52e55] (2026-10-15T23:28:52Z)
- (ac 1) `python3 plugin/tests/run.py -k Cache -k Second -k OnWrite` → exit 0 · Ran 14 tests in 6.9s (2 classes, 16 at a time; slowest: OnWrite 7s, Cache 1s) / OK [ran] [tree c2eed7c52e55] (2026-10-15T23:29:13Z)
- `python3 plugin/tests/run.py test_second test_research_rigor test_onwrite` → exit 0 · Ran 35 tests in 7.0s (11 classes, 16 at a time; slowest: OnWrite 7s, Session 2s, Cross 1s) / OK [ran] [tree c2eed7c52e55] (2026-10-15T23:29:13Z)
- (audit edge) `self: test-only changes; the two tests now fake 'no claude' with an empty HOME as well as PATH, so T-0990's ~/.local/bin lookup can't reach a real claude; the matcher test names T-0972's outside-text tools` → test_second's no-claude path still exits without a session [tree c2eed7c52e55] (2026-10-15T23:29:13Z)
- (audit self) `self: test-only changes; the two tests now fake 'no claude' with an empty HOME as well as PATH, so T-0990's ~/.local/bin lookup can't reach a real claude; the matcher test names T-0972's outside-text tools` → no findings [tree c2eed7c52e55] (2026-10-15T23:29:13Z)
- `python3 plugin/tests/run.py test_second test_research_rigor test_onwrite` → exit 0 · Ran 35 tests in 7.0s (11 classes, 16 at a time; slowest: OnWrite 7s, Session 2s, Cross 1s) / OK [ran] [tree c2eed7c52e55] (2026-10-15T23:29:25Z)
- (audit edge) `self: test-only changes; the two tests now fake 'no claude' with an empty HOME as well as PATH, so T-0990's ~/.local/bin lookup can't reach a real claude; the matcher test names T-0972's outside-text tools` → test_second's no-claude path still exits without a session [tree c2eed7c52e55] (2026-10-15T23:29:25Z)
- (audit self) `self: test-only changes; the two tests now fake 'no claude' with an empty HOME as well as PATH, so T-0990's ~/.local/bin lookup can't reach a real claude; the matcher test names T-0972's outside-text tools` → no findings [tree c2eed7c52e55] (2026-10-15T23:29:25Z)
## Log
- 2026-10-15T23:28:08Z created
- 2026-10-15T23:28:08Z focused
- 2026-10-15T23:29:26Z done
- 2026-10-15T23:29:27Z committed eb963e4 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- T-0990 [FIX S, done, 2 steps] fm and its hooks can't find claude when only the native install (~/.local/bin/claude) exists and PATH lacks ~/.local/bin: roundtrip gate, d…
- T-0855 [FIX M, done, 5 steps] A fresh install is clean and works from a shell: doctor passes and shows only problems, fm check finds the test runner,… — lesson: Walk thr…
- decision 2026-10-15: Update Claude Code with its native installer (claude install latest → ~/.local/bin, which updates itself without root) and put ~/.local/bin first on…
## Regression test
none: the fix is to the tests themselves; red (Cache, OnWrite failing) and green recorded with -k Cache -k OnWrite (+Second)
## Plan gaps
- failed first: step 1 fix the tests
## Files touched
- plugin/tests/test_onwrite.py
- plugin/tests/test_research_rigor.py
- plugin/tests/test_second.py
