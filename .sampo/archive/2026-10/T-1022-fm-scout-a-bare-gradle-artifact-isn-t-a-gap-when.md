---
id: T-1022
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-16T01:41:32Z
updated: 2026-10-16T01:44:05Z
base: 09414b9d66ead2db0603a964bf8f36d715ce630c
base_tree: e51485e1e720448eb77127b75b1a6ff4f82c981f
verified: strong
---
# fm scout: a bare Gradle artifact isn't a gap when its group:artifact form is listed
## Raw request
> fm scout: a bare Gradle artifact isn't a gap when its group:artifact form is listed
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] probe_lib_gaps skips 'rules' when 'androidx.test:rules' is among the project's deps, and still reports an unqualified dep with no qualified twin — verify with `python3 plugin/tests/run.py test_scout`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] skip bare names with a qualified twin in the same project
3. [x] docs: CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_scout` → ✗ exit 1 · Ran 17 tests in 16.0s (3 classes, 16 at a time; slowest: Scout 16s, ScoutDrive 1s, ScoutProbes 1s) / FAILED (1 classes) [ran] [tree 35a39bba2f0a] (2026-10-16T01:41:57Z)
- (step 2) `python3 plugin/tests/run.py test_scout` → exit 0 · Ran 17 tests in 16.0s (3 classes, 16 at a time; slowest: Scout 16s, ScoutDrive 1s, ScoutProbes 1s) / OK [ran] [tree b11989d2df56] (2026-10-16T01:42:45Z)
- (step 3) `grep -q 'T-1022' CHANGELOG.md` → exit 0 · (no output) [ran] [tree 01b8e4bdd7a2] (2026-10-16T01:42:55Z)
- (ac 1) `python3 plugin/tests/run.py test_scout` → exit 0 · Ran 17 tests in 16.2s (3 classes, 16 at a time; slowest: Scout 16s, ScoutDrive 1s, ScoutProbes 1s) / OK [ran] [tree 01b8e4bdd7a2] (2026-10-16T01:43:12Z)
- `python3 plugin/tests/run.py test_scout` → ✗ exit 1 · Ran 17 tests in 16.4s (3 classes, 16 at a time; slowest: Scout 16s, ScoutDrive 1s, ScoutProbes 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 01b8e4bdd7a2] (2026-10-16T01:43:45Z)
- `python3 plugin/tests/run.py test_scout` → exit 0 · Ran 17 tests in 16.1s (3 classes, 16 at a time; slowest: Scout 16s, ScoutDrive 1s, ScoutProbes 1s) / OK [ran] [tree 01b8e4bdd7a2] (2026-10-16T01:43:45Z)
- (audit edge) `self` → ':' allowed in the data-only dep pattern (no spaces, newlines or quotes still); bare ids dropped only when their qualified twin is in the same project [tree 01b8e4bdd7a2] (2026-10-16T01:43:45Z)
- (ac 1) `python3 plugin/tests/run.py test_scout` → exit 0 · Ran 17 tests in 16.3s (3 classes, 16 at a time; slowest: Scout 16s, ScoutDrive 1s, ScoutProbes 1s) / OK [ran] [tree 01b8e4bdd7a2] (2026-10-16T01:44:01Z)
- (audit edge) `red→green` → npm/PyPI names unaffected (existing libgap test) [tree 01b8e4bdd7a2] (2026-10-16T01:44:01Z)
- (audit self) `red→green` → no findings [tree 01b8e4bdd7a2] (2026-10-16T01:44:01Z)
- `python3 plugin/tests/run.py test_scout` → ✗ exit 1 · Ran 17 tests in 16.5s (3 classes, 16 at a time; slowest: Scout 16s, ScoutDrive 2s, ScoutProbes 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 01b8e4bdd7a2] (2026-10-16T01:44:05Z)
- `python3 plugin/tests/run.py test_scout` → exit 0 · Ran 17 tests in 16.3s (3 classes, 16 at a time; slowest: Scout 16s, ScoutDrive 2s, ScoutProbes 1s) / OK [ran] [tree 01b8e4bdd7a2] (2026-10-16T01:44:05Z)
- (audit edge) `self` → ':' allowed in the data-only dep pattern (no spaces, newlines or quotes still); bare ids dropped only when their qualified twin is in the same project [tree 01b8e4bdd7a2] (2026-10-16T01:44:05Z)
## Log
- 2026-10-16T01:41:32Z created
- 2026-10-16T01:41:32Z focused
- 2026-10-16T01:44:02Z done
- 2026-10-16T01:44:03Z committed 2a28715 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0907 [FIX S, done, 1 steps] Stop claims gate: doc edits after a green run, unlisted runners (mvn, gradle, dotnet, deno, node --test, bats, make -jN) and list-form noti…
- T-0433 [SECURITY M, done, 3 steps] Guard fuzzer: mutated real-bash forms never run a dangerous call unblocked — lesson: A guard's own tests find what its authors imagine…
- research rsi-20261004-recon: 1. **Answer.** Four of the five findings are in the guard and the friction digest. The guard blocks most often on a heredoc that only writes…
- T-0301 [FIX S, done, 1 steps] Friction digest: say why tool calls failed; a wait on background work isn't friction — lesson: A digest that groups failures by target hide…
## Why not caught
no Gradle fixture in the scout tests
## Plan gaps
- failed first: step 1 red test
## Files touched
- plugin/tests/test_scout.py
- plugin/lib/fmscout.py
- CHANGELOG.md
