---
id: T-2479
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: genesis
created: 2026-11-01T16:12:32Z
updated: 2026-11-01T16:16:36Z
genesis_sweep: 1:genesis check
base: 044632b5eafc791c229b8a1af3e94d128d1afb8a
base_tree: c91d3e9a9a80c034df5f046e350b66148f75774b
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-11-01T16:15:04Z
plan0_scope: []
verified: ok
---
# Genesis gen-1 sweep: genesis check is red — gen-1/mission-genesis.md: no cold-read pass for its current text: fm genesi…
## Raw request
> fm genesis sweep 1: ✗ genesis check: gen-1/mission-genesis.md: no cold-read pass for its current text: fm genesis put it again
> Done when the rerun's genesis check line is ✓.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] gen-1's tower files each have a cold-read pass for their current text — verify with `fm genesis check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] refile gen-1/mission-genesis.md through the cold read
## Resume here
## Docs impact
none: a tower file in state
## Verification evidence
- (step 1) `fm genesis check` → exit 0 · ✓ frame: 0 added categories / ✓ read [ran] [tree c91d3e9a9a80] (2026-11-01T16:15:23Z)
- (step 1) `fm genesis check` → exit 1 before the refile: ✗ read: gen-1/mission-genesis.md has no cold-read pass for its current text (the re-sweep's genesis check row, sweep3.txt; the refile changed that state, so it can't run again here) [tree c91d3e9a9a80] (2026-11-01T16:16:03Z)
- (step 1) `fm genesis check` → exit 0 · ✓ frame: 0 added categories / ✓ read [ran] [tree c91d3e9a9a80] (2026-11-01T16:16:04Z)
- (ac 1) `fm genesis check` → exit 0 · ✓ frame: 0 added categories / ✓ read [ran] [tree c91d3e9a9a80] (2026-11-01T16:16:34Z)
- (audit intent) `the sweep's red line was the red; refiled through the Sonnet-decided read after 3 grounded fixes; fm genesis check exits 0 with ✓ read; the regression check is the sweep's own read row` → the only red sweep line is green; the file now says the sweep runs steer checks and files fixes, the G-line grades standing-intent clauses, each rejected idea has its own reason [tree c91d3e9a9a80] (2026-11-01T16:16:34Z)
- (audit self) `the sweep's red line was the red; refiled through the Sonnet-decided read after 3 grounded fixes; fm genesis check exits 0 with ✓ read; the regression check is the sweep's own read row` → no findings [tree c91d3e9a9a80] (2026-11-01T16:16:34Z)
## Log
- 2026-11-01T16:12:32Z created
- 2026-11-01T16:15:03Z set tier=S
- 2026-11-01T16:15:03Z planned: it has criteria and steps
- 2026-11-01T16:15:03Z focused
- 2026-11-01T16:15:04Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-11-01T16:16:36Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- decision 2026-10-31: [revisited: Standing rule from gen 2 on: one Mission per generation is a moonshot] [cites: the user's steer 2026-10-30 (fifth): moonshot Mission fro…
## Regression test
The sweep's genesis check row runs read_check (T-2181), which fails any tower file whose current text has no cold-read pass; fm genesis check and every fm genesis sweep rerun it, so this can't come back unseen.
## Lessons
- A sweep fix task's regression test is the sweep row that filed it; file it with that section and an AC on the row so it closes without a typed red
