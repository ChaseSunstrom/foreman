---
id: T-2541
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-02T04:43:34Z
updated: 2026-11-02T05:08:35Z
base: bff2c77dcf43231f40a4d30bb3e3e0a687401abc
base_tree: 7e4e01da59288073d86400ee4d3dfbad9b6ad1cb
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T04:49:35Z
plan0_scope: [plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, CHANGELOG.md]
verified: strong
---
# fm genesis step carries a Mission task deferred with a revisit date (named, listed for the critique) instead of stalling on 'finish T-NNNN'
## Raw request
> fm genesis step: a Mission task deferred with an until date and a reason is carried (named in the step's output, listed for the critique), not 'finish T-NNNN'; the build gate counted deferred as open and stalled gen 2 on T-2533/T-2535
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a Mission whose Task line names a done task and a task deferred with --until moves to its critique step, and the step text names the deferred id as carried; a deferred task with no revisit date, or a planned one, still stalls the build — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_genesis: a mission with one done and one deferred (--until) task reaches the critique step naming it carried; without --until it stays 'finish T-…'
2. [x] fmgenesis step's build loop skips a deferred task with meta revisit, collecting it; the critique act's text names the carried ids
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 207 tests in 17.2s (23 classes, 16 at a time; slowest: GenesisRead 16s, GenerationReview 15s, GenesisCheck 14s) / FAILED (1 classes: test_genesis.GenesisStep) [ran] [tree 891d57a51706] [world 2f1906870a] (2026-11-02T04:50:01Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 207 tests in 17.3s (23 classes, 16 at a time; slowest: GenesisRead 16s, GenerationReview 14s, GenesisCheck 13s) / OK [ran] [tree 68ce90e771cd] [world 2f1906870a] (2026-11-02T04:50:40Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 207 tests in 12.2s (23 classes, 16 at a time; slowest: GenesisRead 12s, GenerationReview 10s, ProofBeforePresentation 9s) / OK [ran] [tree b4d27b50776a] [world 2f1906870a] (2026-11-02T04:57:14Z)
- (audit edge) `self-review: only status deferred with meta revisit is carried; every carried id is named in the critique action; other open statuses still stop the build` → a deferral without --until still says finish T-…; a blocked task still reads as blocked; a carried task that is later revived (planned) stops the build again on the next step [tree b4d27b50776a] (2026-11-02T04:57:14Z)
- (audit self) `self-review: only status deferred with meta revisit is carried; every carried id is named in the critique action; other open statuses still stop the build` → no findings [tree b4d27b50776a] (2026-11-02T04:57:14Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree a452a4909a68] [world 2f1906870a] (2026-11-02T05:08:35Z)
## Log
- 2026-11-02T04:43:34Z created
- 2026-11-02T04:43:50Z planned from capture
- 2026-11-02T04:49:34Z focused
- 2026-11-02T04:49:35Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T04:50:46Z scope: fmgenesis.step's build loop carries a deferred task with meta revisit; the critique act names the carried ids; test in test_genesis.GenesisStep
- 2026-11-02T04:57:40Z done
- 2026-11-02T04:57:43Z committed cba920d7 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-11-02: [costly] Genesis build stage: a deferred Mission task is carried, named, not a blocker
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- T-2172 [FEATURE S, done, 2 steps] fm exam's surfaces: the exam scorecard isn't an MCP tool (so Desktop can't read it) and… — lesson: Put a new piece of state on the one …
- T-2155 [SECURITY M, done, 3 steps] fm genesis put exam.jsonl can overwrite the exam record that fm genesis select and fm… — lesson: A gate's evidence file must be writab…
- similar finished tasks took 2–4 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_genesis.py
## Lessons
- a gate that only knows done and dropped forces a choice between building unmeasured work and hiding it; give the honest third state (deferred with a revive date) a named path through the gate
## Plan gaps
- failed first: step 1 red test in test_genesis: a mission with one done and one deferred (--until) task reaches the criti…
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
