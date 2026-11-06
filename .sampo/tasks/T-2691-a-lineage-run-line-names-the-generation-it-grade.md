---
id: T-2691
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T23:03:33Z
updated: 2026-11-02T23:08:13Z
base: 7e93963bdfad7a7c2ac6f4b38afb466f53a1014a
base_tree: 0c10e7039628e95f503449a4a3a9be4480503f26
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T23:03:34Z
plan0_scope: []
verified: strong
---
# a lineage run line names the generation it grades (gen N, and gen N-1 for the parent), so a cold read never checks one gen's line against another gen's grade on a shared run
## Raw request
> a lineage run line names the generation it grades (gen N, and gen N-1 for the parent), so a cold read never checks one gen's line against another gen's grade on a shared run
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] select's lineage section says 'gen 3 closed 2 vs gen 2's 3' on a shared run — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] name the gens in select's run line
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_genesis 2>&1 | grep -A14 "^FAIL:\|^ERROR:" | grep -v "^ File\|^ " | head -24` → ✗ exit 1 · FAILED (failures=1) / Ran 212 tests in 23.6s (24 classes, 16 at a time; slowest: GenesisRead 23s, GenerationReview 20s, GenesisCheck 18s) [ran] [tree 58fc1e0ad160] [world 2f1906870a] (2026-11-02T23:05:16Z)
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 212 tests in 29.5s (24 classes, 16 at a time; slowest: GenesisRead 29s, GenerationReview 24s, GenesisCheck 21s) / OK [ran] [tree 1dfc39b2016c] [world 2f1906870a] (2026-11-02T23:06:29Z)
- `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 212 tests in 40.6s (24 classes, 16 at a time; slowest: GenesisRead 38s, ProofBeforePresentation 24s, GenerationReview 23s) / FAILED (1 classes: test_genesis.GenesisSelect) (start tree + this task's tests) [ran] [tree 1dfc39b2016c] [world 2f1906870a] (2026-11-02T23:07:38Z)
- `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 212 tests in 25.6s (24 classes, 16 at a time; slowest: GenesisRead 25s, GenerationReview 23s, GenesisCheck 22s) / OK [ran] [tree 1dfc39b2016c] [world 2f1906870a] (2026-11-02T23:07:38Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T23:07:38Z [ran] [tree 1dfc39b2016c] [world 2f1906870a] (2026-11-02T23:07:39Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T23:07:38Z [ran] [tree 1dfc39b2016c] [world 2f1906870a] (2026-11-02T23:07:39Z)
- (step 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T23:07:38Z [ran] [tree 1dfc39b2016c] [world 2f1906870a] (2026-11-02T23:07:39Z)
- (audit edge) `read both changed lines: select's lineage run line and confirm's lineage line now name gen N and gen N-1; confirm.md's labelled fields are unchanged; nothing parses the old 'train closed' wording (grep)` → a baseline section (no parent) prints only 'gen N closed K train'; old sections keep their wording until restated [tree 1dfc39b2016c] (2026-11-02T23:07:39Z)
- (audit self) `read both changed lines: select's lineage run line and confirm's lineage line now name gen N and gen N-1; confirm.md's labelled fields are unchanged; nothing parses the old 'train closed' wording (grep)` → no findings [tree 1dfc39b2016c] (2026-11-02T23:07:39Z)
## Log
- 2026-11-02T23:03:33Z created
- 2026-11-02T23:03:33Z focused
- 2026-11-02T23:03:34Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T23:05:59Z scope: CHANGELOG.md
- 2026-11-02T23:08:10Z done
- 2026-11-02T23:08:13Z committed 2c3010df (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (sixth): the frame may grow, never shrink] [check: pending T-2188] Standing rule from gen 2 on: the Genesis fram…
## Why not caught
select's tests asserted counts and the provisional line, never that the run line named its generation; the ambiguity shows only once two gens share a run
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
