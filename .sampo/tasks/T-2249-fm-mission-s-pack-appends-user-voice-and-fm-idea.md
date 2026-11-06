---
id: T-2249
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T01:21:58Z
updated: 2026-10-31T01:59:35Z
base: c3fa40875a4086c102cf39b105f45737fa1ac939
base_tree: 9600c4e8a3867fe0dd6d9adea351896a55916d29
plan0_at: 2026-10-31T01:58:07Z
plan0_scope: []
verified: strong
---
# fm ideas adds the user's words once, even to a pack fm mission already gave them
## Raw request
> fm mission's pack appends user_voice and fm ideas appends it again, so a pack run through fm mission carries the user's words twice (fmmission.py:108, fmideas.py:811)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a pack from fm mission run through fm ideas carries the user-voice block once, and a plain pack still gets it — verify with `cd plugin/tests && python3 -m unittest -q test_mission test_ideas`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: fm mission's pack through fmideas' pack assembly holds the user-voice heading once; fmideas appends user_voice only when the pack lacks it
## Resume here
## Docs impact
none: internal; one prompt block no longer repeats
## Verification evidence
- `cd plugin/tests && python3 -m unittest -q test_ideas test_mission` → ✗ exit 1 · Ran 27 tests in 9.547s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 33db1ec4cb1c] (2026-10-31T01:58:37Z)
- `cd plugin/tests && python3 -m unittest -q test_ideas test_mission` → exit 0 · Ran 27 tests in 9.352s / OK [ran] [tree 33db1ec4cb1c] (2026-10-31T01:58:37Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_ideas test_mission` → exit 0 · Ran 27 tests in 9.329s / OK [ran] [tree 33db1ec4cb1c] (2026-10-31T01:58:54Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_mission test_ideas` → exit 0 · Ran 27 tests in 9.314s / OK [ran] [tree 33db1ec4cb1c] (2026-10-31T01:59:05Z)
- (audit edge) `self: fm ideas appends user_voice only when the pack doesn't already hold that block (fm mission's pack does); a plain pack still gets it; test_ideas test_mission 27 green, red-to-green proven` → an empty user voice appends nothing either way; a pack holding an older, different voice block gets the current one appended [tree 33db1ec4cb1c] (2026-10-31T01:59:05Z)
- (audit self) `self: fm ideas appends user_voice only when the pack doesn't already hold that block (fm mission's pack does); a plain pack still gets it; test_ideas test_mission 27 green, red-to-green proven` → no findings [tree 33db1ec4cb1c] (2026-10-31T01:59:05Z)
## Log
- 2026-10-31T01:21:58Z created
- 2026-10-31T01:39:30Z planned from capture
- 2026-10-31T01:39:30Z set approved=True
- 2026-10-31T01:58:06Z focused
- 2026-10-31T01:58:54Z scope: plugin/lib/fmideas.py (one line), plugin/tests/test_ideas.py
- 2026-10-31T01:59:27Z done
- 2026-10-31T01:59:28Z committed 9b944757 (2 files)
- 2026-10-31T01:59:35Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0375-review: Verdict:** approve with nits. I read the diff and the surrounding `fmideas.py`, `fmcore.py` and `test_ideas.py` code. I did not run the tests. [s…
- T-1549 [FEATURE M, done, 6 steps] Round 3 (T-1520): Session and release care: the user's own words once in the pack, a warni — lesson: A release's own artifacts (a new s…
- T-0375 [FEATURE L, done, 3 steps] fm mission: Foreman composes the full mission and brainstorm seeds itself for open-ended and exhaustive requests — lesson: When the use…
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (fifth): moonshot Mission from gen 2] [check: pending T-2187] Standing rule from gen 2 on: one Mission per gener…
## Lessons
- When two layers both enrich the same prompt, the later one checks for the earlier block before adding it
## Files touched
- plugin/tests/test_ideas.py
- plugin/lib/fmideas.py
