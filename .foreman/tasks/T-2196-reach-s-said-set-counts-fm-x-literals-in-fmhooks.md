---
id: T-2196
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T17:47:39Z
updated: 2026-10-30T18:42:10Z
base: cde43a898b6902dcdcc1c8988ddc6325beb16bef
base_tree: 30bcea453ab269243f55a15ac11edf032145dfdd
plan0_at: 2026-10-30T18:34:58Z
plan0_scope: []
verified: strong
---
# Reach's said set counts fm x literals in fmhooks.py that a session never sees
## Raw request
> reach's said set counts fm x literals in fmhooks.py that a session never sees
> (noticed by an agent; research T-2186-review)
## Interpretation
reach (T-2186) counts a verb as said when any string literal in fmhooks.py names it. Two kinds a session never sees unasked: a cmd_* function's strings (fmhooks.cmd_guard_try prints 'fm replay', 'fm guard try' only to a session that already ran fm guard) and set displays used as matchers (STATUS_WORDS holds 'fm status' to match the user's words, never printed). _literals skips both, so reach measures what a session is shown.
## Assumptions (confidence)
## Acceptance criteria
- [x] _literals skips strings in a cmd_* function body and in a set display — verify with `python3 plugin/tests/run.py test_genesis`
- [x] live reach still reports every gen-1 verb reached, or names the ones that fall out — verify with `sh -c 'fm genesis check | grep -F "reach"'`
## Non-goals
## Approach (options → choice → why)
Options: (a) _literals skips constants under a cmd_* FunctionDef and under an ast.Set (chosen: two ast rules, no list of strings to keep in sync); (b) a hand list of fmhooks functions whose output reaches a session (rejected: rots as hooks change); (c) trace print/return data flow from hook entry points (rejected: large for two false-positive kinds). Truth over self-image: a reach that counts unseen strings measures wording, not use.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: _literals on a cmd_ body and a set display
2. [x] implement in _literals; run live fm genesis check; MASTER, CHANGELOG
## Resume here
## Docs impact
~/.claude/foreman/MASTER.md ~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 90 tests in 6.5s (13 classes, 16 at a time; slowest: GenesisCheck 6s, GenesisLive 5s, GenesisSweep 5s) / FAILED (1 classes) [ran] [tree af4534e7fd5e] (2026-10-30T18:35:05Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 90 tests in 6.2s (13 classes, 16 at a time; slowest: GenesisCheck 6s, GenesisLive 5s, GenesisSweep 4s) / OK [ran] [tree 6d4dbeb1efa7] (2026-10-30T18:35:15Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 90 tests in 6.4s (13 classes, 16 at a time; slowest: GenesisCheck 6s, GenesisLive 5s, GenesisSweep 5s) / OK [ran] [tree 5085187e5f68] (2026-10-30T18:35:45Z)
- (ac 2) `sh -c 'fm genesis check | grep -F "reach"'` → exit 0 · ✓ reach: 27 fm verb(s) the missions name, each on a session path [ran] [tree 5085187e5f68] (2026-10-30T18:35:45Z)
- (audit intent) `self-review of the 4-line _literals change over intent, edge, adversary (S tier); live fm genesis check reach still 27/27` → reach measures what a session is shown unasked; STATUS_WORDS ('fm status' to match the user's words) and cmd_guard_try's output no longer count [tree 5085187e5f68] (2026-10-30T18:35:45Z)
- (audit edge) `self-review of the 4-line _literals change over intent, edge, adversary (S tier); live fm genesis check reach still 27/27` → a set display anywhere and any FunctionDef named cmd_* drop all strings under them, nested f-string parts too; dict and list literals still count, since hooks build notes from them; _next_for has neither, so fm next's text is unchanged [tree 5085187e5f68] (2026-10-30T18:35:45Z)
- (audit adversary) `self-review of the 4-line _literals change over intent, edge, adversary (S tier); live fm genesis check reach still 27/27` → the change can only shrink the said set, so reach gets stricter, never looser; ast.parse on Foreman's own source, nothing untrusted [tree 5085187e5f68] (2026-10-30T18:35:45Z)
- (audit self) `self-review of the 4-line _literals change over intent, edge, adversary (S tier); live fm genesis check reach still 27/27` → no findings [tree 5085187e5f68] (2026-10-30T18:35:45Z)
## Log
- 2026-10-30T17:47:39Z created
- 2026-10-30T18:25:31Z planned: it has criteria and steps
- 2026-10-30T18:25:37Z set tier=S
- 2026-10-30T18:34:57Z focused
- 2026-10-30T18:36:09Z done
- 2026-10-30T18:36:11Z committed c8f64f80 (4 files)
- 2026-10-30T18:36:25Z guard authorization added: publish
- 2026-10-30T18:42:10Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2186-review: Verdict: changes needed (3 MEDIUM, all addressed)
- research T-2184-review: Verdict: changes needed.** Two MEDIUM defects, plus acceptance criteria 4 and 5 still open. [stale: plugin/lib/fmgenesis.py, plugin/lib/fmhooks.p…
- T-2186 [FIX M, done, 3 steps] Wire the four verbs gen-1's missions name that no session path calls (fm genesis check's… — lesson: A reach check that reads words fails bo…
- decision 2026-10-22: T-1422: dropped the plan reach lint (hosts/paths in a planner's plan → refuse). Two reviews (research T-1422-review, -review2) showed it either refu…
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
## Why not caught
T-2186's test covered comments and docstrings only; the reviewer of T-2186 noticed fmhooks literals that no session sees
## Lessons
- A metric over source text needs the same scoping as the reader it stands for: a string a session never sees (a matcher, a verb's own reply) is wording, not reach.
## Plan gaps
- failed first: step 1 red test: _literals on a cmd_ body and a set display
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
