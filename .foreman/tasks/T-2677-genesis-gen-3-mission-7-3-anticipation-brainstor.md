---
id: T-2677
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T21:51:50Z
updated: 2026-11-02T22:12:23Z
base: 6a4e4a506c481f9b3d962c77382a90a5e0344f3d
base_tree: 37c80f3d08ed6a0467af181a91ae9b09c862dc51
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-02T21:51:52Z
plan0_scope: []
verified: strong
unproven: [research-uncited]
---
# Genesis gen-3 Mission 7 (#3 anticipation): brainstorm with the grid lens, ground with canaries, report Mission 6's two use counts, file the Mission and intake its briefs
## Raw request
> Genesis gen-3 Mission 7 (#3 anticipation): brainstorm with the grid lens, ground with canaries, report Mission 6's two use counts, file the Mission and intake its briefs
## Interpretation
1. (chosen) Follow the tower's step for Mission 7 as for Missions 5 and 6, and also carry Mission 6's two outcome measures: the brainstorm runs the grid lens and the grounding passes record canaries, and the catalogue counts both.
2. Measure Mission 6 separately. Rejected: Mission 6's Done when names Mission 7's grounding as its measure.
## Assumptions (confidence)
## Acceptance criteria
- [x] gen-3/mission-anticipation.md is filed and its catalogue reports grid cells that yielded a grounded idea and 'new' verdicts carrying a canary — verify with `fm genesis status`
## Non-goals
## Approach (options → choice → why)
1. fm mission, fm ideas with the step's flags plus --lens grid, three recon passes told to record a canary per 'new' verdict, spot checks on every slate claim. Likely outcome: a 2-3 brief slate and both counts. Fails if: the recon passes skip the canary, which the count then shows as a gap.
2. use what exists: Mission 5 and 6 catalogues. Fails if: they hold #12 and #2 ideas, not #3.
3. do less: skip the grid lens. Fails if: Mission 6's brief 1 then goes unmeasured.
Choice 1 (88%): the same pipeline with Mission 6's measures built in.
## Risks and rollback
## Execution prompt
## Steps
1. [x] brainstorm (with --lens grid) and canary-checked grounding; catalogue with both counts
2. [x] Mission filed
3. [x] briefs taken in with fm intake --source genesis
## Resume here
<!-- auto -->
- 2026-11-02T22:06:54Z step 1/3: brainstorm (with --lens grid) and canary-checked grounding; catalogue with both counts
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/m7/mission.md
## Docs impact
none: the catalogue and Mission are Foreman state, not repo docs
## Verification evidence
- (step 1) `test -s state/projects/foreman-4a056f/research/brainstorm-20261102-m7.md` → exit 0 · (no output) [ran] [tree 37c80f3d08ed] [world 2f1906870a] (2026-11-02T22:12:10Z)
- (step 2) `test -s state/projects/foreman-4a056f/research/genesis/gen-3/mission-anticipation.md` → exit 0 · (no output) [ran] [tree 37c80f3d08ed] [world 2f1906870a] (2026-11-02T22:12:11Z)
- (step 3) `fm task show T-2684` → exit 0 · - 2026-11-02T22:12:01Z created / ## Follow-ups captured [ran] [tree 37c80f3d08ed] [world 2f1906870a] (2026-11-02T22:12:11Z)
- (ac 1) `fm genesis status` → exit 0 · long-horizon (deciding): behind on 6 same goal(s): foreman 0/6 done, checks 4/20, false-done 6, regressions 0, resumes needed 0, unfinished 0, cost $13.08 vs plain 1/6 done, checks 4/20, false-done 5, [ran] [tree 37c80f3d08ed] [world 2f1906870a] (2026-11-02T22:12:13Z)
- (ac 1) `fm genesis status` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T22:12:13Z [ran] [tree 37c80f3d08ed] [world 2f1906870a] (2026-11-02T22:12:20Z)
- (audit intent) `self: every slate claim was spot-checked (four true), Mission 6's two measures were counted from this catalogue, and the Mission passed its cold read after brief 2 became an action under the push grant` → the tower's step for Mission 7 plus Mission 6's carried measures; both are in the catalogue and the Mission [tree 37c80f3d08ed] (2026-11-02T22:12:20Z)
- (audit edge) `self: every slate claim was spot-checked (four true), Mission 6's two measures were counted from this catalogue, and the Mission passed its cold read after brief 2 became an action under the push grant` → one 'new' verdict of 170 lacks a canary; the grid count reads ideas tagged with a cell, so an untagged grid idea is missed (a lower bound) [tree 37c80f3d08ed] (2026-11-02T22:12:20Z)
## Log
- 2026-11-02T21:51:50Z created
- 2026-11-02T21:51:52Z focused
- 2026-11-02T21:51:52Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-02T21:52:04Z paused: focus moved to T-2678
- 2026-11-02T22:02:03Z focused
- 2026-11-02T22:12:23Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2666 [RESEARCH M, done, 3 steps] Genesis gen-3 Mission 5 (#12 staying lean and safe): ground the 525-idea brainstorm, record the catalogue, file the Mission and intake…
- T-2671 [RESEARCH M, done, 3 steps] Genesis gen-3 Mission 6 (#2 exhaustive thinking): brainstorm, ground every idea with spot checks on each claim a brief rests on, file …
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- decision 2026-11-02: Recommendation: Mission 6 builds three gaps where Foreman drops part of a request's space silently (a grid lens, a count on every cut list, a canary…
## Decision
Recommendation: Mission 7 builds four anticipation gaps where Foreman computes what the user will need but it never reaches them (the booked next-request guess, unshipped work under the push grant, the action that frees the blocked pile, a notify channel that fails silently), and carries the hook-error line, draft-ahead stamps, capture-time closest task and conditional reminders. Mission 6's measures came out positive: 169 of 170 'new' verdicts carried a canary, and 27 of 41 grid-cell ideas grounded as real gaps. Would change if: brief 1's shown guesses hit less often than its unshown ones, in which case the line comes back off.
## Lessons
- When the user has granted an action, a foreseen need becomes the action, not a line asking for it: the cold reader caught an offer-to-ship that should have been a ship
