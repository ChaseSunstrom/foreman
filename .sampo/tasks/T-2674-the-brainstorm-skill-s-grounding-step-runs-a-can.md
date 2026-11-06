---
id: T-2674
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: genesis
created: 2026-11-02T21:30:41Z
updated: 2026-11-02T21:35:49Z
base: 2e6b1eeef531c3f28389a397b44f18f60ef5e7b0
base_tree: 3b6fbbf51909554659805218634798e69982b5a0
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T21:31:33Z
plan0_scope: []
verified: strong
---
# the brainstorm skill's grounding step runs a canary search for a term known to exist in the same scope before accepting any 'not found'
## Raw request
> FEATURE: the brainstorm skill's grounding step runs a canary search for a term known to exist in the same scope before it accepts any "not found", and test_brainstorm_skill asserts it
> CONTEXT: Genesis gen-3 Mission 6 (#2 exhaustive thinking), gen-3/mission-exhaustive-thinking.md
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] SKILL.md step 4 requires a canary search (a term known to exist, same tool and scope) before a 'not found' counts, and test_brainstorm_skill asserts it — verify with `python3 plugin/tests/run.py test_brainstorm_skill`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] the step 4 line
3. [x] CHANGELOG
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_brainstorm_skill` → red as expected (exit 1) · Ran 2 tests in 0.3s (2 classes, 16 at a time; slowest: Canary 0s, Grounding 0s) / FAILED (1 classes: test_brainstorm_skill.Canary) [ran] [tree e924527e9d40] [world 2f1906870a] (2026-11-02T21:31:45Z)
- (ac 1) `python3 plugin/tests/run.py test_brainstorm_skill 2>&1 | tail -1` → exit 0 · OK [ran] [tree fa980c9a2bed] [world 2f1906870a] (2026-11-02T21:31:49Z)
- (step 2) `python3 plugin/tests/run.py test_brainstorm_skill 2>&1 | tail -1` → exit 0 · OK [ran] [tree fa980c9a2bed] [world 2f1906870a] (2026-11-02T21:31:49Z)
- (step 2) `python3 plugin/tests/run.py test_brainstorm_skill` → exit 0 · Ran 2 tests in 0.5s (2 classes, 16 at a time; slowest: Grounding 0s, Canary 0s) / OK [ran] [tree 3f668e7c8b00] [world 2f1906870a] (2026-11-02T21:31:56Z)
- (step 3) `python3 plugin/tests/run.py test_brainstorm_skill` → exit 0 · Ran 2 tests in 0.6s (2 classes, 16 at a time; slowest: Canary 0s, Grounding 0s) / OK [ran] [tree 3f668e7c8b00] [world 2f1906870a] (2026-11-02T21:31:57Z)
- (ac 1) `python3 plugin/tests/run.py test_brainstorm_skill` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T21:31:57Z [ran] [tree 3f668e7c8b00] [world 2f1906870a] (2026-11-02T21:31:59Z)
- (audit edge) `self: one sentence in step 4 beside the T-2659 rule it completes; the verdict format (canary: <term> found) gives Mission 7's catalogue something to count` → the test checks the text only; use is measured on Mission 7's grounding, as Mission 6's Exam says [tree 3f668e7c8b00] (2026-11-02T21:31:59Z)
- (audit self) `self: one sentence in step 4 beside the T-2659 rule it completes; the verdict format (canary: <term> found) gives Mission 7's catalogue something to count` → no findings [tree 3f668e7c8b00] (2026-11-02T21:31:59Z)
## Log
- 2026-11-02T21:30:41Z created
- 2026-11-02T21:31:32Z planned from capture
- 2026-11-02T21:31:32Z focused
- 2026-11-02T21:31:33Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T21:35:44Z done
- 2026-11-02T21:35:49Z committed 525eb957 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-11-02: Recommendation: Mission 6 builds three gaps where Foreman drops part of a request's space silently (a grid lens, a count on every cut list, a canary…
- T-2672 [FEATURE S, active, 3 steps] a grid lens in fmideas.LENS_NOTES: cross the request's surfaces with its actors and failure modes, one idea per cell; selectable with…
- T-2666 [RESEARCH M, done, 3 steps] Genesis gen-3 Mission 5 (#12 staying lean and safe): ground the 525-idea brainstorm, record the catalogue, file the Mission and intake…
- T-2671 [RESEARCH M, done, 3 steps] Genesis gen-3 Mission 6 (#2 exhaustive thinking): brainstorm, ground every idea with spot checks on each claim a brief rests on, file …
## Files touched
- plugin/tests/test_brainstorm_skill.py
- plugin/skills/brainstorm/SKILL.md
- CHANGELOG.md
