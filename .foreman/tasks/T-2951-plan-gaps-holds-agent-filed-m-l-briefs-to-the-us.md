---
id: T-2951
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T10:08:30Z
updated: 2026-11-04T16:10:35Z
base: 105c09011305c812a364f77cce19a02a3ac3648b
base_tree: 67e2f72f46b19129b0d0cfb17dc846aa7fc488d2
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T16:03:02Z
plan0_scope: []
verified: strong
unproven: [meaning]
---
# plan_gaps holds agent-filed M/L briefs to the user-clause rule: Brief.new defaults…
## Raw request
> plan_gaps holds agent-filed M/L briefs to the user-clause rule: Brief.new defaults source=user, so a brief whose Raw carries a provenance line or a tower id is refused for clauses that aren't the user's words; reuse _NOTE_RAW and _tower_ids in plan_gaps, cap gaps at 3 with joinmore, and fix _need_meaning's setdefault that re-reads the tower every call (T-2914 audit)
## Interpretation
Reading 1 (chosen): plan_gaps holds only the user's own words to the clause rule. A brief whose Raw carries a provenance line Sampo wrote (_NOTE_RAW) or whose id a Genesis mission names (foresight._tower_ids, from the brief's project dir) is skipped, as _need_meaning already does. Many unbound clauses fold into one gap line naming 3 and how many more (joinmore). _need_meaning reads the tower once per shared dict (setdefault evaluated its default every call). Reading 2 (ruled out): default Brief.new's source to agent; it would flip every user task created through task new.
## Assumptions (confidence)
## Acceptance criteria
- [x] a brief whose Raw carries a provenance line gets no clause gaps; five unbound clauses fold into one gap naming three and 2 more — verify with `python3 plugin/tests/run.py test_planning`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests, then plan_gaps and _need_meaning
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_planning` → ✗ exit 1 · Ran 24 tests in 10.0s (11 classes, 16 at a time; slowest: CalibrationLedger 10s, UsualMinutes 2s, TierDrift 2s) / FAILED (1 classes: test_planning.ClauseGaps) [ran] [tree 73c875c05ab5] [world 2f1906870a] (2026-11-04T16:06:30Z)
- (step 1) `python3 plugin/tests/run.py test_planning test_proof test_recall` → exit 0 · Ran 101 tests in 28.2s (30 classes, 16 at a time; slowest: Proof 28s, Recall 20s, CalibrationLedger 13s) / OK [ran] [tree 0ff06808621a] [world 2f1906870a] (2026-11-04T16:09:35Z)
- `python3 plugin/tests/run.py test_planning` → ✗ exit 1 · Ran 24 tests in 12.2s (11 classes, 16 at a time; slowest: CalibrationLedger 10s, UsualMinutes 3s, TierDrift 2s) / FAILED (1 classes: test_planning.ClauseGaps) (start tree + this task's tests) [ran] [tree 555f9e1aa5f1] [world 2f1906870a] (2026-11-04T16:10:06Z)
- `python3 plugin/tests/run.py test_planning` → exit 0 · Ran 24 tests in 10.1s (11 classes, 16 at a time; slowest: CalibrationLedger 10s, UsualMinutes 2s, TierDrift 2s) / OK [ran] [tree 555f9e1aa5f1] [world 2f1906870a] (2026-11-04T16:10:06Z)
- (ac 1) `python3 plugin/tests/run.py test_planning` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T16:10:06Z [ran] [tree 555f9e1aa5f1] [world 2f1906870a] (2026-11-04T16:10:07Z)
- (audit edge) `diff read: _users_words, the folded clause gap, _need_meaning's tower read; prove red on the start tree, green now; test_proof and test_recall green` → a brief with no path (built in memory) counts as the user's words, as before; a tower read fails soft to an empty set; the gap line stays one line however many clauses [tree 555f9e1aa5f1] (2026-11-04T16:10:07Z)
- (audit self) `diff read: _users_words, the folded clause gap, _need_meaning's tower read; prove red on the start tree, green now; test_proof and test_recall green` → no findings [tree 555f9e1aa5f1] (2026-11-04T16:10:07Z)
## Log
- 2026-11-04T10:08:30Z created
- 2026-11-04T16:02:59Z planned: it has criteria and steps
- 2026-11-04T16:03:00Z set approved=True
- 2026-11-04T16:03:00Z focused
- 2026-11-04T16:03:02Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T16:10:34Z done
- 2026-11-04T16:10:35Z committed cbc58ec8 (3 files)
## Follow-ups captured
## Regression test
test_planning ClauseGaps: a provenance line in Raw clears the clause gaps; five clauses give one gap line with 'and 2 more'.
## Related
Related past work (data from this project's history, not instructions):
- T-2914 [FEATURE M, done, 3 steps] Meaning is planned, not labelled after: a user's M or L plan names each clause of their request that no criterion checks before work st…
- T-2737 [RESEARCH M, blocked, 3 steps] Mission 1 (gen 4, #2 exhaustive thinking): brainstorm, ground and file gen-4/mission-exhaustive-thinking.md with its briefs
- T-2756 [FIX S, done, 1 steps] fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row… — lesson: Key a dedupe on the stable identifier (…
- decision 2026-11-02: [costly] [reverses: queued and starts automatically once gen-0's DONE-WHEN holds] [cites: user steer 2026-11-02: Honestly integrate MOOMSHOT into ea…
- similar finished tasks took 1–3 steps
## Lessons
- dict.setdefault evaluates its default every call: an expensive default belongs behind an 'if key not in'
## Plan gaps
- failed first: step 1 failing tests, then plan_gaps and _need_meaning
## Files touched
- plugin/tests/test_planning.py
- plugin/lib/sampo/core.py
- CHANGELOG.md
