---
id: T-0986
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py,plugin/tests/test_board_export.py,CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-15T23:08:00Z
updated: 2026-10-15T23:08:50Z
base: 9a87d192973bb6847fcb291afb18b3a07bde5f82
base_tree: c864863b937cde0c0d1f3d9bc2aeed57511efb89
verified: strong
---
# fm next's due-back line for a 'when PATH changes' deferral suggests --until <date>; name the file trigger
## Raw request
> fm next's due-back line for a 'when PATH changes' deferral suggests --until <date>; name the file trigger
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a due-back file-trigger deferral's fm next line says --until "when PATH changes", not <date> — verify with `python3 plugin/tests/run.py test_board_export`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test (from the T-0978 Haiku probe)
2. [x] strip the @hash and keep the trigger
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_board_export` → ✗ exit 1 · Ran 4 tests in 8.2s (1 classes, 16 at a time; slowest: BoardExport 8s) / FAILED (1 classes) [ran] [tree 40029b04afa9] (2026-10-15T23:08:20Z)
- (step 2) `python3 plugin/tests/run.py test_board_export` → exit 0 · Ran 4 tests in 8.2s (1 classes, 16 at a time; slowest: BoardExport 8s) / OK [ran] [tree 14fc9285b938] (2026-10-15T23:08:37Z)
- (ac 1) `python3 plugin/tests/run.py test_board_export` → exit 0 · Ran 4 tests in 4.8s (1 classes, 16 at a time; slowest: BoardExport 5s) / OK [ran] [tree 9086caa53cfc] (2026-10-15T23:08:49Z)
- (audit edge) `self: one-line change in next_for; the test extends the existing T-0958 due-back test; a date revisit still says <date>` → a date revisit keeps --until <date>; a when-trigger drops only a trailing @hash [tree 9086caa53cfc] (2026-10-15T23:08:49Z)
- (audit self) `self: one-line change in next_for; the test extends the existing T-0958 due-back test; a date revisit still says <date>` → no findings [tree 9086caa53cfc] (2026-10-15T23:08:49Z)
## Log
- 2026-10-15T23:08:00Z created
- 2026-10-15T23:08:00Z focused
- 2026-10-15T23:08:49Z done
- 2026-10-15T23:08:50Z committed b6158b6 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0802 [FEATURE S, done, 2 steps] fm research list and fm research show NAME — lesson: when users and criteria keep reaching for a command that doesn't exist, add it
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- T-0958 [FEATURE M, done, 3 steps] Knowledge out: lessons as native rules, decisions as ADRs, deferrals that wake when a file changes — lesson: Exporting to a natively lo…
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_core.py
## Plan gaps
- failed first: step 1 failing test (from the T-0978 Haiku probe)
## Files touched
- plugin/tests/test_board_export.py
- plugin/lib/fmcore.py
- CHANGELOG.md
