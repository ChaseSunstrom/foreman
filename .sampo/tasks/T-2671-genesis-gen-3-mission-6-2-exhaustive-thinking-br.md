---
id: T-2671
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T21:11:33Z
updated: 2026-11-02T21:31:01Z
base: 34a2320825e3a9e148bed545dba08e37fd3ffee4
base_tree: 3b6fbbf51909554659805218634798e69982b5a0
plan0_at: 2026-11-02T21:11:35Z
plan0_scope: []
verified: strong
unproven: [research-uncited]
---
# Genesis gen-3 Mission 6 (#2 exhaustive thinking): brainstorm, ground every idea with spot checks on each claim a brief rests on, file the Mission and intake its briefs
## Raw request
> Genesis gen-3 Mission 6 (#2 exhaustive thinking): brainstorm, ground every idea with spot checks on each claim a brief rests on, file the Mission and intake its briefs
## Interpretation
1. (chosen) Follow the tower's step for Mission 6 as Mission 5 did, with its critique's changes: read the code path behind each baseline number, spot-check every claim a brief rests on.
2. Skip the brainstorm and pick from earlier catalogues. Rejected: the step asks for a fresh run with --seen-latest so it goes past them.
## Assumptions (confidence)
## Acceptance criteria
- [x] gen-3/mission-exhaustive-thinking.md is filed (its cold read passed) and its briefs are in the queue — verify with `fm genesis status`
## Non-goals
## Approach (options → choice → why)
1. fm mission, then fm ideas with the step's flags in the background; three recon passes ground it; I spot-check every claim the slate rests on. Likely outcome: a 2-4 brief slate. Fails if: the ideas repeat the earlier runs (--seen-latest 6 is there to stop that).
2. use what exists: take Mission 5's carried clusters. Fails if: they are #12's, not #2's.
3. do less: one recon pass over the top 100 ideas. Fails if: a whole cluster goes ungrounded, the T-0364 failure.
Choice 1 (88%): the same pipeline that found real gaps in Mission 5, with its lessons applied.
## Risks and rollback
## Execution prompt
## Steps
1. [x] brainstorm and catalogue (fm research add)
2. [x] Mission filed with fm genesis put
3. [x] briefs taken in with fm intake --source genesis
## Resume here
<!-- auto -->
- 2026-11-02T21:22:00Z step 1/3: brainstorm and catalogue (fm research add)
- git: foreman/build; 0 uncommitted
## Docs impact
none: the catalogue and Mission are Foreman state, not repo docs
## Verification evidence
- (step 1) `test -s state/projects/foreman-4a056f/research/brainstorm-20261102-m6.md` → exit 0 · (no output) [ran] [tree 3b6fbbf51909] [world 2f1906870a] (2026-11-02T21:27:33Z)
- (step 2) `test -s state/projects/foreman-4a056f/research/genesis/gen-3/mission-exhaustive-thinking.md` → exit 0 · (no output) [ran] [tree 3b6fbbf51909] [world 2f1906870a] (2026-11-02T21:30:57Z)
- (step 3) `fm task show T-2674` → exit 0 · - 2026-11-02T21:30:41Z created / ## Follow-ups captured [ran] [tree 3b6fbbf51909] [world 2f1906870a] (2026-11-02T21:30:58Z)
- (ac 1) `fm genesis status` → exit 0 · long-horizon (deciding): behind on 6 same goal(s): foreman 0/6 done, checks 4/20, false-done 6, regressions 0, resumes needed 0, unfinished 0, cost $13.08 vs plain 1/6 done, checks 4/20, false-done 5, [ran] [tree 3b6fbbf51909] [world 2f1906870a] (2026-11-02T21:30:59Z)
- (ac 1) `fm genesis status` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T21:30:59Z [ran] [tree 3b6fbbf51909] [world 2f1906870a] (2026-11-02T21:31:00Z)
- (audit intent) `self: every slate claim was spot-checked and one candidate (the citation check) was counted before choosing and found to clear 3 of 432; the Mission's cold read passed after four revisions` → the tower's step asked for the brainstorm, grounding, Mission and briefs; all exist, and the outcome measures go to Mission 7 and the critique [tree 3b6fbbf51909] (2026-11-02T21:31:00Z)
- (audit edge) `self: every slate claim was spot-checked and one candidate (the citation check) was counted before choosing and found to clear 3 of 432; the Mission's cold read passed after four revisions` → 397 ideas became 398 lines across chunks (one repeated); every cluster is in the catalogue with its mark [tree 3b6fbbf51909] (2026-11-02T21:31:00Z)
## Log
- 2026-11-02T21:11:33Z created
- 2026-11-02T21:11:34Z focused
- 2026-11-02T21:13:49Z paused: focus moved to T-2639
- 2026-11-02T21:21:35Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-02T21:21:35Z focused
- 2026-11-02T21:22:38Z paused: focus moved to T-2670
- 2026-11-02T21:30:56Z focused
- 2026-11-02T21:31:01Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2666 [RESEARCH M, done, 3 steps] Genesis gen-3 Mission 5 (#12 staying lean and safe): ground the 525-idea brainstorm, record the catalogue, file the Mission and intake…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2095 [FEATURE M, done, 3 steps] fm genesis step: the tower's next action from its files, resumable after any kill — lesson: A resumable state machine over files has to…
- decision 2026-11-01: [costly] Gen-2 Missions are written without fm ideas' four-round brainstorm while the account's weekly usage is past 80% (economy mode): each Missio…
## Decision
Recommendation: Mission 6 builds three gaps where Foreman drops part of a request's space silently (a grid lens, a count on every cut list, a canary before 'not found'), and carries the repeat-correction sweep, brief claim resolution and stop-reason codes to the next seed. Would change if: Mission 7's catalogue shows the grid lens yields no grounded idea, in which case the lens is removed.
## Lessons
- Recon passes told to grep per idea spent ~100 tool calls instead of ~8, and their claims held under spot checks; the depth instruction belongs in every grounding brief
