---
id: T-2729
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-03T00:17:37Z
updated: 2026-11-03T00:18:40Z
base: 1949f2acfcd8bd63990ee4495a41dfa71d04883e
base_tree: 9348380af51e2410252b973cca2452d1dc2fe253
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-03T00:17:38Z
plan0_scope: []
verified: strong
---
# gen-4 seed: the selection rule says what gen-0 §3 says of #13 (a first working version in generation 1, then ranked like any area), so the Missions table no longer contradicts it
## Raw request
> gen-4 seed: the selection rule says what gen-0 §3 says of #13 (a first working version in generation 1, then ranked like any area), so the Missions table no longer contradicts it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] gen-4/seed.md is filed past its cold read — verify with `test -f state/projects/foreman-4a056f/research/genesis/gen-4/seed.md`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] revise the draft's rule and the waiting-cells line, then put it
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `test -f state/projects/foreman-4a056f/research/genesis/gen-4/seed.md` → exit 0 · (no output) [ran] [tree 9348380af51e] [world 2f1906870a] (2026-11-03T00:18:37Z)
- (step 1) `test -f state/projects/foreman-4a056f/research/genesis/gen-4/seed.md` → exit 0 · (no output) [ran] [tree 9348380af51e] [world 2f1906870a] (2026-11-03T00:18:37Z)
- (ac 1) `test -f state/projects/foreman-4a056f/research/genesis/gen-4/seed.md` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T00:18:37Z [ran] [tree 9348380af51e] [world 2f1906870a] (2026-11-03T00:18:38Z)
- (audit intent) `the draft's selection rule claimed '#13 included (gen-0 §3)', but gen-0 §3 puts #13 in generation 1 only; restated it and said the waiting areas rank below the seven by value; the put passed its cold read over two rounds (12 sections a round)` → the Missions table wasn't changed to fit the text; the text was wrong about gen-0 [tree 9348380af51e] (2026-11-03T00:18:38Z)
- (audit self) `the draft's selection rule claimed '#13 included (gen-0 §3)', but gen-0 §3 puts #13 in generation 1 only; restated it and said the waiting areas rank below the seven by value; the put passed its cold read over two rounds (12 sections a round)` → no findings [tree 9348380af51e] (2026-11-03T00:18:38Z)
## Log
- 2026-11-03T00:17:37Z created
- 2026-11-03T00:17:38Z focused
- 2026-11-03T00:17:38Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-03T00:18:40Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- T-2119 [FIX S, done, 1 steps] FIX S: fm genesis step reads a seed with no Missions table as a dry generation and jumps…
- research T-2102-review: Verdict:** changes needed. Finding 1 is a MEDIUM that breaks the "seed N output passes step's seed-row rules (<= 8 rows)" MUST. I read the code a…
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (sixth): the frame may grow, never shrink] [check: pending T-2188] Standing rule from gen 2 on: the Genesis fram…
- similar finished tasks took 1–5 steps
## Regression test
none: a tower file; its cold read is the check
