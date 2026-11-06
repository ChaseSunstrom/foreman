---
id: T-2175
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T15:25:06Z
updated: 2026-10-31T07:14:19Z
group: genesis check gates on tower files
base: 8da84f2ce13e720a046d1e23a0042c5c37dcd77b
base_tree: af502a157c3c7638c09a2ad3f830532648984a7f
plan0_at: 2026-10-31T07:04:22Z
plan0_scope: []
verified: strong
---
# fm genesis check: flag one feature filled under two coverage areas (the same F: path…
## Raw request
> fm genesis check: flag one feature filled under two coverage areas (the same F: path with overlapping words in two rows), so the cold read stops catching these 5 at a time (T-2166 dropped 29 by hand)
## Interpretation
coverage.md fills each area's stage × surface cells with 'F: <path> — <what it does>'. One feature often gets filed under two cells (find × CLI and find × MCP naming fmfind.py with the same words), inflating the filled count; the cold read caught these a few at a time and T-2166 dropped 29 by hand. fm genesis check should flag them first.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis check flags two filled coverage cells naming the same F: path with descriptions sharing ≥60% of their significant words, counts only one as filled, and leaves the same path with different descriptions alone — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
1) in fmgenesis.coverage: for filled F: cells, group by the path; within a group, two cells whose descriptions share most significant words (Jaccard over 4+ letter words ≥ 0.6) are one feature in two cells: a problem naming both cells, and only one counts as filled; 2) one path may fill one cell only — rejected: a module legitimately serves CLI and MCP with different behaviour; 3) a model judge — rejected: tokens per check, and the rule is countable. Choice 1.
## Risks and rollback
A shared module described differently in two cells stays two cells (the words differ), as it should. The threshold is a constant with a test either side.
## Execution prompt
## Steps
1. [x] red tests: a duplicate pair flagged and counted once; the same path described differently kept
2. [x] the duplicate rule in fmgenesis.coverage
3. [x] docs: give MASTER and CHANGELOG lines in the report
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 155 tests in 13.1s (17 classes, 16 at a time; slowest: GenesisRead 13s, GenesisCheck 11s, GenesisDrift 10s) / OK [ran] [tree 4d7f1a0478bf] (2026-10-31T07:06:54Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_genesis && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [19.32s] [ran] [tree 4d7f1a0478bf] (2026-10-31T07:07:27Z)
- `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 155 tests in 8.8s (17 classes, 16 at a time; slowest: GenesisRead 8s, GenesisCheck 7s, GenesisDrift 6s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 299a06608b4d] (2026-10-31T07:12:55Z)
- `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 155 tests in 7.9s (17 classes, 16 at a time; slowest: GenesisRead 8s, GenesisCheck 7s, GenesisDrift 6s) / OK [ran] [tree 299a06608b4d] (2026-10-31T07:12:55Z)
- (step 1) `python3 plugin/tests/run.py test_genesis test_docs` → exit 0 · Ran 238 tests in 8.6s (39 classes, 16 at a time; slowest: Fences 8s, GenesisRead 8s, GenesisCheck 7s) / OK [ran] [tree 299a06608b4d] (2026-10-31T07:13:03Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_docs` → exit 0 · Ran 238 tests in 8.6s (39 classes, 16 at a time; slowest: Fences 8s, GenesisRead 8s, GenesisCheck 7s) / OK [ran] [tree 299a06608b4d] (2026-10-31T07:13:12Z)
- (step 3) `python3 plugin/tests/run.py test_genesis test_docs` → exit 0 · Ran 238 tests in 8.5s (39 classes, 16 at a time; slowest: Fences 8s, GenesisRead 8s, GenesisCheck 7s) / OK [ran] [tree 299a06608b4d] (2026-10-31T07:13:21Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 155 tests in 7.9s (17 classes, 16 at a time; slowest: GenesisRead 8s, GenesisCheck 7s, GenesisDrift 6s) / OK [ran] [tree 57131b67c730] (2026-10-31T07:13:39Z)
- (audit intent) `self-review of the diff: pairwise per F path, Jaccard over 4+ letter words at 0.6, cells already flagged as templated skipped; read-only; the live tower has 0 pairs today` → duplicates the cold read caught a few at a time are flagged by the check first, and the filled count stops inflating (test_genesis red-to-green) [tree 57131b67c730] (2026-10-31T07:13:39Z)
- (audit edge) `self-review of the diff: pairwise per F path, Jaccard over 4+ letter words at 0.6, cells already flagged as templated skipped; read-only; the live tower has 0 pairs today` → the same module described differently in two cells stays two cells; :NN and backticked paths normalized [tree 57131b67c730] (2026-10-31T07:13:39Z)
## Log
- 2026-10-30T15:25:06Z created
- 2026-10-31T07:04:10Z set tier=M
- 2026-10-31T07:04:11Z planned: it has criteria and steps
- 2026-10-31T07:04:11Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2175.builder.md
- 2026-10-31T07:04:22Z focused
- 2026-10-31T07:09:09Z merged worktree-agent-adb172cde70cfd7cf (2 file(s))
- 2026-10-31T07:12:31Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-adb172cde70cfd7cf
- 2026-10-31T07:12:37Z focused
- 2026-10-31T07:13:30Z scope: plugin/lib/fmgenesis.py (coverage duplicates), plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md
- 2026-10-31T07:14:02Z done
- 2026-10-31T07:14:03Z committed 43934c33 (2 files)
- 2026-10-31T07:14:19Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2159 [FEATURE M, done, 3 steps] Coverage must be real: reset coverage.md's templated cells (a shim to…, a site page to…,… — lesson: A templated-text detector has to co…
- research T-2159-review: Approve with nits. I read the diff, `coverage.md` and the callers, but ran no commands, so the two verify commands are unrun. [stale: plugin/lib/…
- research T-2223-review: MEDIUM, fixed: find × CLI (fmideas.py) said lens children read the code and mark ideas new/partial/built; they are tool-less and that marking liv…
- decision 2026-10-30: [cites: user steer 2026-10-29: COVERAGE BY GRID, NOT BY LUCK] Genesis standing rule: coverage by grid — coverage.md (fm genesis put): rows = the 13 …
## Lessons
- A count that a model reviewer keeps correcting by hand is a deterministic check waiting to be written
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
