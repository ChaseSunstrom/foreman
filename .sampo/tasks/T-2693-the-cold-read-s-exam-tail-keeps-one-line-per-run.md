---
id: T-2693
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T23:09:31Z
updated: 2026-11-02T23:12:21Z
base: 2c3010dfdb72a14dbe489741f41566ad594a2dbc
base_tree: 1dfc39b2016cd605807eb1efd8afcbb0799572b0
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T23:09:33Z
plan0_scope: []
verified: strong
---
# the cold read's exam tail keeps one line per run, agent and generation, so a later gen graded on a shared run no longer hides the earlier gen's line from the reader
## Raw request
> the cold read's exam tail keeps one line per run, agent and generation, so a later gen graded on a shared run no longer hides the earlier gen's line from the reader
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] two gens graded on one run show as two tail lines, each naming its gen and its closed count — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] key the tail by gen and name it
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 212 tests in 19.6s (24 classes, 16 at a time; slowest: GenesisRead 19s, GenerationReview 16s, GenesisCheck 15s) / OK [ran] [tree acb59415ce6b] [world 2f1906870a] (2026-11-02T23:10:49Z)
- `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 212 tests in 20.8s (24 classes, 16 at a time; slowest: GenesisRead 19s, GenerationReview 16s, ProofBeforePresentation 15s) / FAILED (1 classes: test_genesis.GenesisDraft) (start tree + this task's tests) [ran] [tree acb59415ce6b] [world 2f1906870a] (2026-11-02T23:11:31Z)
- `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 212 tests in 19.7s (24 classes, 16 at a time; slowest: GenesisRead 19s, GenerationReview 17s, GenesisCheck 15s) / OK [ran] [tree acb59415ce6b] [world 2f1906870a] (2026-11-02T23:11:31Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T23:11:31Z [ran] [tree acb59415ce6b] [world 2f1906870a] (2026-11-02T23:11:32Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T23:11:31Z [ran] [tree acb59415ce6b] [world 2f1906870a] (2026-11-02T23:11:32Z)
- (step 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T23:11:31Z [ran] [tree acb59415ce6b] [world 2f1906870a] (2026-11-02T23:11:32Z)
- (audit edge) `read _exam_tail: rows keyed by (run, agent, gen), the label names the gen when the line has one; lines without a gen keep their old label; the tail still keeps the newest k rows` → a regrade of the same gen on the same run still replaces its own earlier line (same key), as before [tree acb59415ce6b] (2026-11-02T23:11:32Z)
- (audit operator) `read _exam_tail: rows keyed by (run, agent, gen), the label names the gen when the line has one; lines without a gen keep their old label; the tail still keeps the newest k rows` → found when gen-3 select's lineage.md failed its cold read 3 times on a true gen-2 line; the reader's evidence showed only gen 3's grade for s32-015 [tree acb59415ce6b] (2026-11-02T23:11:32Z)
- (audit self) `read _exam_tail: rows keyed by (run, agent, gen), the label names the gen when the line has one; lines without a gen keep their old label; the tail still keeps the newest k rows` → no findings [tree acb59415ce6b] (2026-11-02T23:11:32Z)
## Log
- 2026-11-02T23:09:31Z created
- 2026-11-02T23:09:32Z focused
- 2026-11-02T23:09:33Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T23:10:29Z scope: CHANGELOG.md
- 2026-11-02T23:12:16Z done
- 2026-11-02T23:12:21Z committed 478e8d3b (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2568 [FEATURE M, done, 4 steps] fm tidy --apply prunes graded exam runs' work copies past 14 days, keeping the newest run per tier and agent, answers, grades and keys …
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2172 [FEATURE S, done, 2 steps] fm exam's surfaces: the exam scorecard isn't an MCP tool (so Desktop can't read it) and… — lesson: Put a new piece of state on the one …
- decision 2026-10-31: [costly] Tower filing waits for the user's call on the cold-read rule: Missions 5-8's files and the Mission 3-4 critiques stay unfiled after 4-12 pu…
## Why not caught
the tail's tests graded one gen per run; no test put two gens on one run
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
