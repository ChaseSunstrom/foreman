---
id: T-0992
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py,plugin/tests/helpers.py,plugin/tests/test_ideas.py,plugin/tests/test_core.py,CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-15T23:36:05Z
updated: 2026-10-15T23:37:02Z
base: eb963e48b8cdd0bb412226ed4477e2decf580101
base_tree: c3c494b686f16f01240f816f9b266c283eedc5b3
verified: strong
---
# T-0990's ~/.local/bin fallback bypasses the tests' claude lockout when a test replaces PATH: test runs reached the paid binary
## Raw request
> T-0990's ~/.local/bin fallback bypasses the tests' claude lockout when a test replaces PATH: test runs reached the paid binary
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] under the test helpers no fm process finds a claude outside PATH; test_ideas' missing-claude case exits 1 — verify with `python3 plugin/tests/run.py test_ideas test_core`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing run
2. [x] fallback dir overridable; helpers point it at nothing
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ideas test_core` → ✗ exit 1 · Ran 87 tests in 25.9s (20 classes, 16 at a time; slowest: Ideas 26s, WritesAndLocks 2s, BoardIdeas 1s) / FAILED (1 classes) [ran] [tree c3c494b686f1] (2026-10-15T23:36:32Z)
- (step 2) `python3 plugin/tests/run.py test_ideas test_core` → exit 0 · Ran 87 tests in 4.5s (20 classes, 16 at a time; slowest: Ideas 4s, WritesAndLocks 2s, BoardIdeas 1s) / OK [ran] [tree c0967bdf9cc8] (2026-10-15T23:36:47Z)
- (ac 1) `python3 plugin/tests/run.py test_ideas test_core` → exit 0 · Ran 87 tests in 4.4s (20 classes, 16 at a time; slowest: Ideas 4s, WritesAndLocks 2s, BoardIdeas 1s) / OK [ran] [tree addfb6c9e80a] (2026-10-15T23:37:01Z)
- (audit edge) `self: the fallback folder comes from the env passed in (FOREMAN_NATIVE_BIN, else HOME's .local/bin); the test helpers set it to a folder that doesn't exist, next to the PATH lockout; test_ideas' missing-claude case is back to exit 1 without a session` → NativeClaude's own env dicts don't carry the variable, so they still test the HOME path [tree addfb6c9e80a] (2026-10-15T23:37:01Z)
- (audit adversary) `self: the fallback folder comes from the env passed in (FOREMAN_NATIVE_BIN, else HOME's .local/bin); the test helpers set it to a folder that doesn't exist, next to the PATH lockout; test_ideas' missing-claude case is back to exit 1 without a session` → the override only names where to look for the user's own install; a missing folder means no fallback [tree addfb6c9e80a] (2026-10-15T23:37:01Z)
- (audit self) `self: the fallback folder comes from the env passed in (FOREMAN_NATIVE_BIN, else HOME's .local/bin); the test helpers set it to a folder that doesn't exist, next to the PATH lockout; test_ideas' missing-claude case is back to exit 1 without a session` → no findings [tree addfb6c9e80a] (2026-10-15T23:37:01Z)
## Log
- 2026-10-15T23:36:05Z created
- 2026-10-15T23:36:05Z focused
- 2026-10-15T23:37:01Z done
- 2026-10-15T23:37:02Z committed 0f00ccf (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0283 [FIX S, done, 0 steps] Tests can never reach the real claude: a lockout claude after the stub dirs in helpers PAT
- T-0990 [FIX S, done, 2 steps] fm and its hooks can't find claude when only the native install (~/.local/bin/claude) exists and PATH lacks ~/.local/bin: roundtrip gate, d…
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- decision 2026-10-15: Update Claude Code with its native installer (claude install latest → ~/.local/bin, which updates itself without root) and put ~/.local/bin first on…
- similar finished tasks took 0–3 steps
- likely tests for the scope: plugin/tests/test_core.py
## Why not caught
the suite passed with the npm claude on PATH; the gap only showed once it was gone and a test replaced PATH
## Plan gaps
- failed first: step 1 failing run
## Files touched
- plugin/lib/fmcore.py
- plugin/tests/helpers.py
- CHANGELOG.md
