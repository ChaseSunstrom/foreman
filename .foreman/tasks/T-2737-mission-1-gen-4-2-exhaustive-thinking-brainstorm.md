---
id: T-2737
type: RESEARCH
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-03T00:34:58Z
updated: 2026-11-06T03:53:10Z
base: fc60bb351a236ab7e8ad5a2692bce16d2ceda040
base_tree: c6bfed3436adad4d339fabdf0bc1dad28093a670
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-03T00:35:14Z
plan0_scope: []
paused_tree: f2b13010631b406af0097b10497eba4708b0a803
---
# Mission 1 (gen 4, #2 exhaustive thinking): brainstorm, ground and file gen-4/mission-exhaustive-thinking.md with its briefs
## Raw request
> Mission 1 (gen 4, #2 exhaustive thinking): brainstorm, ground and file gen-4/mission-exhaustive-thinking.md with its briefs
## Interpretation
Reading 1 (chosen): the tower's Mission 1 for gen 4: brainstorm #2 Exhaustive thinking past the six earlier brainstorms, ground every cluster with canaries near the idea (T-2686), and file a Mission whose Exam gives each brief an outcome measure and a live-state reading (gen-3 critiques). Reading 2 (ruled out): skip the brainstorm and file the seed's carried gaps as briefs. Ruled out: the seed says a brainstorm is never skipped for pace.
## Assumptions (confidence)
## Acceptance criteria
- [ ] gen-4/mission-exhaustive-thinking.md is filed past its cold read — verify with `test -f state/projects/foreman-4a056f/research/genesis/gen-4/mission-exhaustive-thinking.md`
## Non-goals
## Approach (options → choice → why)
1. The gen-3 flow: fm mission, fm ideas --rounds 4 --deepen 3 --falsify --crossbreed --seen-latest 6 --lens grid, three fm-recon grounding passes over the clusters, a catalogue via fm research add, two spot checks, the Mission. Likely outcome: 3-4 S briefs, each with an outcome measure. Fails if: recon canaries repeat one term (now warned by fm research add).
2. Ground with one recon pass. Fails if: Mission 5's critique found one pass under-grounds (8 tool calls vs 100+).
3. Use what exists: fm mission, fm ideas, fm research add and the scratch scripts from Missions 5 to 7 (extract_json.py, build.py). Likely outcome: no new tooling; the run costs only its model calls.
4. Do less: brief the seed's carried gaps (dissents scored, canary quality) without a brainstorm. Fails if: it skips the grid's empty cells.
Choice 1 on 3 (80%).
## Risks and rollback
## Execution prompt
## Steps
1. [ ] fm mission and fm ideas (grid lens)  <- CURRENT
2. [ ] ground every cluster (three recon passes, canaries near the idea)
3. [ ] catalogue, spot checks, Mission file, intake
## Resume here
<!-- auto -->
- 2026-11-03T00:55:13Z step 1/3: fm mission and fm ideas (grid lens)
- git: foreman/build; 0 uncommitted
- failures met: 0
## Docs impact
## Verification evidence
## Log
- 2026-11-03T00:34:58Z created
- 2026-11-03T00:35:13Z focused
- 2026-11-03T00:35:14Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-03T00:36:22Z paused: focus moved to T-2738
- 2026-11-03T00:38:44Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-03T00:38:44Z focused
- 2026-11-03T00:39:55Z paused: focus moved to T-2736
- 2026-11-03T00:40:02Z focused
- 2026-11-03T00:44:26Z paused: focus moved to T-1344
- 2026-11-03T00:46:08Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-03T00:46:08Z focused
- 2026-11-03T00:49:10Z paused: focus moved to T-1476
- 2026-11-03T00:53:38Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T00:53:38Z focused
- 2026-11-03T00:53:39Z checkpoint (SAMPO.md rename, NOW): the brainstorm finished: research/brainstorm-20261102-183533 (grid only, 95 ideas, a mis-run: the Mission file passed as --pack) and the full run with the pack's lenses plus grid (newest research/brainstorm-*); resume at step 2: ground every cluster with g4m1/brief.md's near-the-idea canaries
- 2026-11-03T00:55:27Z paused: focus moved to T-2742
- 2026-11-03T01:00:24Z blocked: waits on T-2742 (SAMPO.md: finish the rename, then resume the tower and its Missions under the new names; checkpointed after the brainstorm, resume at step 2 grounding)
- 2026-11-06T03:53:10Z unblocked
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2666 [RESEARCH M, done, 3 steps] Genesis gen-3 Mission 5 (#12 staying lean and safe): ground the 525-idea brainstorm, record the catalogue, file the Mission and intake…
- T-2671 [RESEARCH M, done, 3 steps] Genesis gen-3 Mission 6 (#2 exhaustive thinking): brainstorm, ground every idea with spot checks on each claim a brief rests on, file …
- T-2078 [FEATURE M, done, 3 steps] fm genesis: the tower's home: init saves gen-0 verbatim and read-only, put files tower docs under research/genesis, status shows the to…
- decision 2026-11-02: Recommendation: Mission 6 builds three gaps where Foreman drops part of a request's space silently (a grid lens, a count on every cut list, a canary…
