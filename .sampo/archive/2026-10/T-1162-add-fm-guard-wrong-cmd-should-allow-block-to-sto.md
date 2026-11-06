---
id: T-1162
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T10:45:53Z
updated: 2026-10-16T11:58:36Z
base: cf9972bfa70d489e071d98f35d5f3bffb2537e9d
base_tree: e1c98a17984f2222137be61f21da2a4d81b78f01
plan0_at: 2026-10-16T11:36:14Z
plan0_scope: []
verified: strong
---
# Add `fm guard wrong "<cmd>" --should allow|block` to store a labelled case that `fm replay
## Raw request
> FEATURE: Add `fm guard wrong "<cmd>" --should allow|block` to store a labelled case that `fm replay` and the guard tests load, and have `fm night` run the replay and capture a FIX when verdicts drift.
> DONE-WHEN: a test adds a wrong-verdict case, `fm replay` reports it against the current guard, and a seeded drift in `fm night` captures exactly one FIX brief
## Interpretation
A wrong guard verdict seen in practice should become a permanent labelled case, not a memory: fm guard wrong "CMD" --should allow|block [--cwd DIR] [--why TEXT] appends one case to a corpus in Foreman's repo (plugin/tests/fixtures/guard_cases.jsonl); the guard tests load every case and assert the labelled verdict; fm replay reports the corpus against the current guard; fm night runs that check and captures one FIX when a labelled case disagrees with the guard.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm guard wrong stores a labelled case; the guard test fails while the guard disagrees with a label and passes when they agree; fm night captures one FIX for a drifted case and none on a second run — verify with `python3 plugin/tests/run.py test_guard_cases`
## Non-goals
## Approach (options → choice → why)
Options: (a) a JSONL corpus in the repo's test fixtures, written by fm guard wrong (redacted: c.redact on the command; refuse a command that still holds a key-shaped literal), loaded by a new test and by fm replay --corpus; fm night calls the same checker; (b) store cases in project state (not shared through git; rejected); (c) only a docs convention (rejected: nothing enforces it). Choice: (a). Register as an action of the existing fm guard command (fm guard try exists in fmhooks.cmd_guard_try; add 'wrong' beside it). fm night: find where it runs its jobs (fmnight.py) and add one job that captures at most one FIX per drift, deduped by the case's hash.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (test_guard_cases.py): add a case; corpus loader asserts labels; night captures one FIX, deduped; key-shaped literals refused
2. [x] fm guard wrong, the corpus loader test, fm replay reporting the corpus, the night job
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard_cases` → ✗ exit 1 · Ran 5 tests in 1.1s (1 classes, 16 at a time; slowest: GuardCases 1s) / FAILED (1 classes) [ran] [tree aca807089c5f] (2026-10-16T11:36:49Z)
- (step 2) `python3 plugin/tests/run.py test_guard_cases` → exit 0 · Ran 5 tests in 3.5s (1 classes, 16 at a time; slowest: GuardCases 3s) / OK [ran] [tree f19083b167f0] (2026-10-16T11:38:47Z)
- (step 2) `python3 plugin/tests/run.py test_guard_cases test_night test_replay` → exit 0 · Ran 37 tests in 12.4s (12 classes, 16 at a time; slowest: Night 11s, NightGuards 8s, GuardCases 7s) / OK [ran] [tree a6bafc52eda2] (2026-10-16T11:51:13Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_cases test_night test_replay` → exit 0 · Ran 37 tests in 3.2s (12 classes, 16 at a time; slowest: Night 3s, Replay 3s, NightGuards 2s) / OK [ran] [tree 1a1c1d24633d] (2026-10-16T11:56:11Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_cases` → exit 0 · Ran 9 tests in 3.5s (1 classes, 16 at a time; slowest: GuardCases 3s) / OK [ran] [tree 0a3b335d7c2d] (2026-10-16T11:56:28Z)
- (audit intent) `reviewer: one fm-reviewer pass confirmed the corpus can't weaken the guard (nothing in fmguard reads it) and found a crash on bad lines, a vacuous pass via the env override, archived FIXes recaptured, the night job in every project, and a $HOME default cwd; builder fixed all six and seeded 6 cases verified against the guard (two seed labels were location-dependent and replaced)` → a wrong verdict becomes a permanent test, not a memory [tree 0a3b335d7c2d] (2026-10-16T11:56:28Z)
- (audit adversary) `reviewer: one fm-reviewer pass confirmed the corpus can't weaken the guard (nothing in fmguard reads it) and found a crash on bad lines, a vacuous pass via the env override, archived FIXes recaptured, the night job in every project, and a $HOME default cwd; builder fixed all six and seeded 6 cases verified against the guard (two seed labels were location-dependent and replaced)` → labels only reach tests; the repo test ignores FOREMAN_GUARD_CASES and fails on a missing or broken corpus; allow-drift FIX text forbids loosening without the user's yes [tree 0a3b335d7c2d] (2026-10-16T11:56:28Z)
- (audit edge) `reviewer: one fm-reviewer pass confirmed the corpus can't weaken the guard (nothing in fmguard reads it) and found a crash on bad lines, a vacuous pass via the env override, archived FIXes recaptured, the night job in every project, and a $HOME default cwd; builder fixed all six and seeded 6 cases verified against the guard (two seed labels were location-dependent and replaced)` → conflict markers and truncated lines are counted and fail the test; cwd stored repo-relative [tree 0a3b335d7c2d] (2026-10-16T11:56:28Z)
- (audit operator) `reviewer: one fm-reviewer pass confirmed the corpus can't weaken the guard (nothing in fmguard reads it) and found a crash on bad lines, a vacuous pass via the env override, archived FIXes recaptured, the night job in every project, and a $HOME default cwd; builder fixed all six and seeded 6 cases verified against the guard (two seed labels were location-dependent and replaced)` → fm replay --cases prints labelled/drifted/broken in one line [tree 0a3b335d7c2d] (2026-10-16T11:56:28Z)
- (audit maintainer) `reviewer: one fm-reviewer pass confirmed the corpus can't weaken the guard (nothing in fmguard reads it) and found a crash on bad lines, a vacuous pass via the env override, archived FIXes recaptured, the night job in every project, and a $HOME default cwd; builder fixed all six and seeded 6 cases verified against the guard (two seed labels were location-dependent and replaced)` → one JSONL fixture, one loader shared by the test, replay and night [tree 0a3b335d7c2d] (2026-10-16T11:56:28Z)
## Log
- 2026-10-16T10:45:53Z created
- 2026-10-16T11:36:02Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1162.builder.md
- 2026-10-16T11:36:14Z focused
- 2026-10-16T11:56:02Z merged worktree-agent-a3722d8a306e21060 (6 file(s))
- 2026-10-16T11:56:07Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a3722d8a306e21060
- 2026-10-16T11:56:08Z focused
- 2026-10-16T11:56:24Z scope: MASTER.md and CHANGELOG.md lines; corpus seeded with 6 cases checked against the real guard
- 2026-10-16T11:58:34Z done
- 2026-10-16T11:58:36Z committed f9916b2b (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0433 [SECURITY M, done, 3 steps] Guard fuzzer: mutated real-bash forms never run a dangerous call unblocked — lesson: A guard's own tests find what its authors imagine…
- T-0673 [FEATURE M, done, 7 steps] Milestone: Features — Multi-machine, multi-project and ecosystem — lesson: a capture into another project must not run that project's e…
- research brainstorm-20261016-round2: Format per cluster: ideas, grounding (code or fm command), Status (queued / done / partial / new / false), Score (value 1-5, effort …
- decision 2026-10-04: [costly] T-0308 closed on self-audit, hunk proofs and the replay corpus
- similar finished tasks took 3–7 steps
## Lessons
- a guard verdict can depend on where the checkout lives; label cases with an explicit cwd outside the repo
## Plan gaps
- failed first: step 1 Failing tests (test_guard_cases.py): add a case; corpus loader asserts labels; night captures one F…
## Files touched
- plugin/tests/test_guard_cases.py
- plugin/lib/fmreplay.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- plugin/lib/fmnight.py
- plugin/tests/fixtures/guard_cases.jsonl
- MASTER.md
- CHANGELOG.md
