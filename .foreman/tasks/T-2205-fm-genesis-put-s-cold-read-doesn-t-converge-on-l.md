---
id: T-2205
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T19:54:14Z
updated: 2026-10-30T20:00:29Z
base: 9134ca177622ea74cc23bcc319f81e27a76aaa07
base_tree: 7026a61f53dedb9ddf0f197a4d5a7a93f4652773
plan0_at: 2026-10-30T19:55:32Z
plan0_scope: []
verified: strong
---
# fm genesis put's cold read doesn't converge on long tower files: 13 rounds to file…
## Raw request
> fm genesis put's cold read doesn't converge on long tower files: 13 rounds to file gen-1/mission-exam.md and 8+ on mission-genesis.md, each finding new points and some reversing an earlier round (status markers asked for, then objected to). Give the reader the previous round's findings and the writer's answer to each, so it checks those were met and still flags any new MUST/NEVER breach or metric gaming; never cap the rounds or narrow what it may fail
## Interpretation
Each fm genesis put cold read starts from nothing, so on a long file every round finds new points and some reverse an earlier round's ask; 13 rounds filed mission-exam.md, mission-genesis.md didn't converge in 8. The reader should see what earlier failed reads of the same file named.
## Assumptions (confidence)
## Acceptance criteria
- [x] a failed read's findings reach the next read of that file, fenced, and clear on a pass — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
Complete version: findings of failed reads kept per tower file name in p.dir/genesis-reads.json (newest 40, cleared on a pass), shown fenced as <previous-reads> in the next read's prompt, and READ_CHILD told to re-check each (unmet fails again, met isn't repeated, a line doing what an earlier read asked fails only on a gen-0/steer/intent breach) and still look for new problems. Options: cap rounds (rejected: narrows the guard), feed the writer's answers (rejected: untrusted, the file is the answer), a bigger model (cost, doesn't fix amnesia), carry findings (chosen). Build vs reuse: c.write_atomic, _fence, c.plain; no new verb.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: GenesisRead test for previous-reads carry, fence and clear
2. [x] fmgenesis: READS store, prompt block, READ_CHILD instruction; MASTER + CHANGELOG
## Resume here
## Docs impact
~/.claude/foreman/MASTER.md ~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 92 tests in 6.5s (13 classes, 16 at a time; slowest: GenesisCheck 6s, GenesisLive 5s, GenesisSweep 5s) / FAILED (1 classes) [ran] [tree ed194e1b0f1c] (2026-10-30T19:56:13Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 92 tests in 6.5s (13 classes, 16 at a time; slowest: GenesisCheck 6s, GenesisLive 5s, GenesisSweep 5s) / OK [ran] [tree 4d22bc2f138e] (2026-10-30T19:56:45Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_docs` → exit 0 · Ran 172 tests in 8.7s (34 classes, 16 at a time; slowest: Fences 8s, GenesisCheck 7s, GenesisLive 5s) / OK [ran] [tree bdcf6ee57e11] (2026-10-30T19:59:17Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 92 tests in 6.8s (13 classes, 16 at a time; slowest: GenesisCheck 7s, GenesisSweep 5s, GenesisLive 5s) / OK [ran] [tree bdcf6ee57e11] (2026-10-30T20:00:04Z)
- `python3 plugin/tests/run.py test_genesis test_docs` → exit 0 · Ran 172 tests in 8.6s (34 classes, 16 at a time; slowest: Fences 8s, GenesisCheck 6s, GenesisSweep 5s) / OK [ran] [tree bdcf6ee57e11] (2026-10-30T20:00:04Z)
- (audit intent) `one foreman:fm-reviewer pass over intent, adversary, edge, operator, maintainer (research T-2205-review): metric-gaming exception, concurrent-write loss, stray carry and dedupe fixed and tested` → a failed read's findings reach the next read fenced and clear on a pass; the reader can still fail metric gaming and any new breach [tree bdcf6ee57e11] (2026-10-30T20:00:04Z)
- (audit adversary) `one foreman:fm-reviewer pass over intent, adversary, edge, operator, maintainer (research T-2205-review): metric-gaming exception, concurrent-write loss, stray carry and dedupe fixed and tested` → carried text is plain'd, fenced (a why can't close the block) and named as data [tree bdcf6ee57e11] (2026-10-30T20:00:04Z)
- (audit edge) `one foreman:fm-reviewer pass over intent, adversary, edge, operator, maintainer (research T-2205-review): metric-gaming exception, concurrent-write loss, stray carry and dedupe fixed and tested` → strays not carried; one entry per line; reload before write keeps a concurrent put's findings [tree bdcf6ee57e11] (2026-10-30T20:00:04Z)
- (audit operator) `one foreman:fm-reviewer pass over intent, adversary, edge, operator, maintainer (research T-2205-review): metric-gaming exception, concurrent-write loss, stray carry and dedupe fixed and tested` → one small JSON per project, 40 entries max, no hook or loop [tree bdcf6ee57e11] (2026-10-30T20:00:04Z)
- (audit maintainer) `one foreman:fm-reviewer pass over intent, adversary, edge, operator, maintainer (research T-2205-review): metric-gaming exception, concurrent-write loss, stray carry and dedupe fixed and tested` → two helpers and one prompt block in fmgenesis, tests cover carry, fence, clear and dedupe [tree bdcf6ee57e11] (2026-10-30T20:00:04Z)
## Log
- 2026-10-30T19:54:14Z created
- 2026-10-30T19:55:31Z planned: it has criteria and steps
- 2026-10-30T19:55:31Z focused
- 2026-10-30T20:00:27Z done
- 2026-10-30T20:00:29Z committed da2761e4 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2078 [FEATURE M, done, 3 steps] fm genesis: the tower's home: init saves gen-0 verbatim and read-only, put files tower docs under research/genesis, status shows the to…
- decision 2026-10-30: [revisited: cold haiku fm second read] [cites: the user's steer 2026-10-30 (second): standing rule] [check: python3 plugin/tests/run.py test_genesis…
## Why not caught
T-2166 built the cold read for one-shot filings; no test put the same file through more than one failed round
## Lessons
- A model judge read from scratch every round doesn't converge on a long document: give it its earlier findings to verify, and keep its power to fail anything new
## Plan gaps
- failed first: step 1 red: GenesisRead test for previous-reads carry, fence and clear
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
