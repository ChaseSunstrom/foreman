---
id: T-2686
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-02T22:38:04Z
updated: 2026-11-02T22:55:14Z
base: 1ed400df5850bef9e34e5ba0bbf015a85a721cbc
base_tree: 2b5234f4b834752b9b047e651469218f1e63dc91
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T22:52:14Z
plan0_scope: []
verified: strong
---
# a brainstorm canary must be a built feature near the idea, and fm research add warns when one canary term covers most of a catalogue's 'not found' verdicts
## Raw request
> brainstorm skill step 4: a canary must be a built feature near the idea (same nouns or module), not a generic term; the catalogue counts distinct canary terms (Mission 7: 156 of 169 canaries were 'def main')
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_brainstorm_skill: step 4 names a near-neighbour canary, and fmideas.canary_spread flags a catalogue where one term covers over half of 10+ canaries while passing varied ones — verify with `python3 plugin/tests/run.py test_brainstorm_skill`
- [x] fm research add prints the canary warning for such a catalogue — verify with `python3 plugin/tests/run.py test_brainstorm_skill`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] canary_spread in fmideas, the warning in fm research add, the step 4 sentence
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_brainstorm_skill` → exit 0 · Ran 5 tests in 0.7s (3 classes, 16 at a time; slowest: CanaryWarning 0s, Canary 0s, Grounding 0s) / OK [ran] [tree 519b1bfc8a0e] [world 2f1906870a] (2026-11-02T22:52:55Z)
- `python3 plugin/tests/run.py test_brainstorm_skill` → ✗ exit 1 · Ran 5 tests in 2.4s (3 classes, 16 at a time; slowest: CanaryWarning 0s, Canary 0s, Grounding 0s) / FAILED (2 classes: test_brainstorm_skill.Canary, test_brainstorm_skill.CanaryWarning) (start tree + this task's tests) [ran] [tree 519b1bfc8a0e] [world 2f1906870a] (2026-11-02T22:52:59Z)
- `python3 plugin/tests/run.py test_brainstorm_skill` → exit 0 · Ran 5 tests in 0.7s (3 classes, 16 at a time; slowest: CanaryWarning 0s, Canary 0s, Grounding 0s) / OK [ran] [tree 519b1bfc8a0e] [world 2f1906870a] (2026-11-02T22:52:59Z)
- (ac 1) `python3 plugin/tests/run.py test_brainstorm_skill` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T22:52:59Z [ran] [tree 519b1bfc8a0e] [world 2f1906870a] (2026-11-02T22:53:04Z)
- (ac 2) `python3 plugin/tests/run.py test_brainstorm_skill` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T22:52:59Z [ran] [tree 519b1bfc8a0e] [world 2f1906870a] (2026-11-02T22:53:04Z)
- (step 2) `python3 plugin/tests/run.py test_brainstorm_skill test_left_out test_research` → exit 0 · Ran 36 tests in 2.5s (16 classes, 16 at a time; slowest: DriveSide 2s, DecisionsResearchSelf 2s, Cross 2s) / OK [ran] [tree 519b1bfc8a0e] [world 2f1906870a] (2026-11-02T22:53:04Z)
- (step 3) `python3 plugin/tests/run.py test_brainstorm_skill test_left_out test_research` → exit 0 · Ran 36 tests in 2.5s (16 classes, 16 at a time; slowest: DriveSide 2s, DecisionsResearchSelf 2s, Cross 2s) / OK [ran] [tree 519b1bfc8a0e] [world 2f1906870a] (2026-11-02T22:53:04Z)
- (audit edge) `read canary_spread and the research add line: 10+ canaries and one term over half triggers it; Mission 7's catalogue (156 'def main' among its canaries) would have warned; varied canaries and small catalogues pass` → a catalogue with 9 canaries never warns (too few to judge); the term is shown through c.plain and cut at 40 characters [tree 519b1bfc8a0e] (2026-11-02T22:53:04Z)
- (audit intent) `read canary_spread and the research add line: 10+ canaries and one term over half triggers it; Mission 7's catalogue (156 'def main' among its canaries) would have warned; varied canaries and small catalogues pass` → Mission 7's critique asked for a check, not only skill text; the warning fires where the catalogue is filed [tree 519b1bfc8a0e] (2026-11-02T22:53:04Z)
- (audit self) `read canary_spread and the research add line: 10+ canaries and one term over half triggers it; Mission 7's catalogue (156 'def main' among its canaries) would have warned; varied canaries and small catalogues pass` → no findings [tree 519b1bfc8a0e] (2026-11-02T22:53:04Z)
## Log
- 2026-11-02T22:38:04Z created
- 2026-11-02T22:52:13Z planned from capture
- 2026-11-02T22:52:13Z focused
- 2026-11-02T22:52:14Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T22:52:54Z scope: fmcli.py (the warning in fm research add), fmideas.py (canary_spread), CHANGELOG.md
- 2026-11-02T22:55:10Z done
- 2026-11-02T22:55:14Z committed cdcd3339 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261102-m7: 393 ideas in 64 clusters, each grounded in the code: 34 built, 13 false-premise, 170 new, 176 partial. 16 clusters marked build.
- T-2187 [FEATURE L, done, 4 steps] Moonshot Mission each generation from gen 2 (steer 2026-10-30 #5): fm genesis seed N (N… — lesson: A rule over model marks must treat a…
- T-2674 [FEATURE S, done, 3 steps] the brainstorm skill's grounding step runs a canary search for a term known to exist in the same scope before accepting any 'not found'
- decision 2026-11-02: Recommendation: Mission 6 builds three gaps where Foreman drops part of a request's space silently (a grid lens, a count on every cut list, a canary…
- similar finished tasks took 3–4 steps
## Why not caught
T-2674 checked that each 'new' verdict carried a canary, never what the canary was
## Files touched
- plugin/tests/test_brainstorm_skill.py
- plugin/lib/fmideas.py
- plugin/lib/fmcli.py
- plugin/skills/brainstorm/SKILL.md
- CHANGELOG.md
