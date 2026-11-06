---
id: T-1912
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmrecall.py, plugin/tests/test_nudges.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-29T04:22:49Z
updated: 2026-10-29T04:58:56Z
base: 03e0f7a1d34fb71f7713d4b10a55a063e2d43bd2
base_tree: 4fa80d0638a7b43813f59dee76fe2c358930151a
plan0_at: 2026-10-29T04:35:57Z
plan0_scope: [plugin/lib/fmrecall.py, plugin/tests/test_nudges.py, CHANGELOG.md]
verified: strong
---
# Fmrecall.covered() indexes only top-level fm commands, so capture's 'already exists' warni
## Raw request
> fmrecall.covered() indexes only top-level fm commands, so capture's 'already exists' warning misses fm task subcommands now that verb_docs walks them (T-1908 review)
## Interpretation
covered() walks only top-level verbs; reuse verb_docs() so a request restating a subcommand (fm task prove) is warned as already existing.
## Assumptions (confidence)
## Acceptance criteria
- [x] A request restating fm task prove's help is covered as 'task prove' — verify with `python3 plugin/tests/run.py test_nudges`
## Non-goals
## Approach (options → choice → why)
Reuse verb_docs() (already walks nested subparsers) in covered(). Alternatives: duplicate the walk (more code), index only task subcommands (misses others).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: a subcommand restated
2. [x] covered() reads verb_docs(); CHANGELOG; green
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_nudges test_recall test_which` → exit 0 · Ran 49 tests in 16.9s (14 classes, 16 at a time; slowest: Recall 17s, OtherProjects 6s, Consolidate 4s) / OK [ran] [tree 44b8c809dba0] (2026-10-29T04:58:26Z)
- (ac 1) `python3 plugin/tests/run.py test_nudges` → exit 0 · Ran 12 tests in 2.6s (3 classes, 16 at a time; slowest: Revisit 2s, QuietHints 2s, Covered 0s) / OK [ran] [tree 44b8c809dba0] (2026-10-29T04:58:34Z)
- (step 2) `python3 plugin/tests/run.py test_nudges` → exit 0 · Ran 12 tests in 2.6s (3 classes, 16 at a time; slowest: Revisit 2s, QuietHints 2s, Covered 0s) / OK [ran] [tree 44b8c809dba0] (2026-10-29T04:58:34Z)
- (audit edge) `main-thread read of the builder diff: covered() reuses verb_docs, same thresholds` → a long paste still isn't a match (existing threshold kept); subcommand help now counted [tree 44b8c809dba0] (2026-10-29T04:58:34Z)
- (audit maintainer) `main-thread read of the builder diff: covered() reuses verb_docs, same thresholds` → one command index (verb_docs) behind fm which, fm help and capture's warning [tree 44b8c809dba0] (2026-10-29T04:58:34Z)
- (audit self) `main-thread read of the builder diff: covered() reuses verb_docs, same thresholds` → no findings [tree 44b8c809dba0] (2026-10-29T04:58:34Z)
## Log
- 2026-10-29T04:22:49Z created
- 2026-10-29T04:34:31Z set tier=S, scope=['plugin/lib/fmrecall.py', 'plugin/tests/test_nudges.py', 'CHANGELOG.md']
- 2026-10-29T04:34:35Z planned: it has criteria and steps
- 2026-10-29T04:35:37Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1912.builder.md
- 2026-10-29T04:35:55Z focused
- 2026-10-29T04:58:01Z merged worktree-agent-a43e4d89de8f3db3c (2 file(s))
- 2026-10-29T04:58:03Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a43e4d89de8f3db3c
- 2026-10-29T04:58:04Z focused
- 2026-10-29T04:58:54Z done
- 2026-10-29T04:58:56Z committed a2638229 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1908 [FIX M, done, 6 steps] FIX: fm which misses subcommands and the rules' own phrases: 'drop a task', 'defer a task' — lesson: an index built from top-level verbs mi…
- research wave1-plan-a2475fc5d2263de06: === T-1049 [stale: plugin/lib/fmcli.py, plugin/lib/fmdeps.py, plugin/lib/fmhooks.py changed since it was written]
- T-1303 [FIX S, done, 1 steps] fm ideas' near-T marks are spurious: an idea matched a done task by sharing two common words with its long request; a match now needs the t…
- decision 2026-10-23: T-1779: 'a stop line' read as the s key; --all-projects left out
- similar finished tasks took 1–6 steps
- likely tests for the scope: plugin/tests/test_recall.py
## Lessons
- Reuse the one command index instead of re-walking the parser
## Files touched
- plugin/tests/test_nudges.py
- plugin/lib/fmrecall.py
- CHANGELOG.md
