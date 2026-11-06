---
id: T-1174
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-16T12:10:57Z
updated: 2026-10-16T12:38:49Z
base: a036c4fa71a897fc535d4fae5e0722eccde31e31
base_tree: f036102e04551cd54bb7dfdafe7aa3926ff08fef
plan0_at: 2026-10-16T12:14:34Z
plan0_scope: []
verified: strong
---
# Forever loop round 4: review what shipped since round 2, brainstorm past every earlier run
## Raw request
> Forever loop round 4: review what shipped since round 2, brainstorm past every earlier run, ground every idea, queue what's real
## Interpretation
Round 4 of the forever loop: review what shipped since round 2 as its user (review written into the pack), run fm ideas past every earlier brainstorm, cluster and ground every idea against the code, queue what is real and new, record the yield.
## Assumptions (confidence)
## Acceptance criteria
- [x] every idea of the round is grounded and either queued as a brief or marked with why not; fm loop yield recorded — verify with `fm loop status`
## Non-goals
## Approach (options → choice → why)
Options: (a) fm ideas (tool-less lenses, cheap) plus one grounding agent over the whole catalogue, as round 2 did (38 clusters in one pass); (b) the new /foreman:ideas workflow (code-reading lenses) — needs the user's opt-in to run a workflow, so not in an AFK run; (c) skip the brainstorm and build from the review only. Choice: (a), started after the release gates so the load doesn't flake them; the review findings go into the pack.
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm ideas on the round-4 pack (after the release gates)
2. [x] Cluster and ground (one agent over the catalogue); fm intake the build marks; fm research add the catalogue
3. [x] fm loop yield N
## Resume here
## Docs impact
none: research only
## Verification evidence
- (step 1) `test -s state/projects/foreman-4a056f/research/brainstorm-20261016-071416/ideas.md && grep -c '^- ' state/projects/foreman-4a056f/research/brainstorm-20261016-071416/ideas.md` → exit 0 · 324 [ran] [tree fcd8e2163dc7] (2026-10-16T12:20:37Z)
- (step 2) `test -s state/projects/foreman-4a056f/research/brainstorm-20261016-round4.md` → exit 0 · (no output) [ran] [tree f036102e0455] (2026-10-16T12:38:47Z)
- (step 3) `fm loop status` → exit 0 · Forever loop: on · round 4 [ran] [tree f036102e0455] (2026-10-16T12:38:47Z)
- (ac 1) `fm loop status` → exit 0 · Forever loop: on · round 4 [ran] [tree f036102e0455] (2026-10-16T12:38:48Z)
- (audit intent) `self: 195 ideas clustered into 46 clusters by one grounding agent (all placed, script-checked); spot-checked fm task list absent and the release ritual separate; 10 build marks, one skipped on security grounds and one narrowed to the existing replay gate; 9 intaken` → round past everything seen; every idea grounded and either queued or marked [tree f036102e0455] (2026-10-16T12:38:48Z)
- (audit adversary) `self: 195 ideas clustered into 46 clusters by one grounding agent (all placed, script-checked); spot-checked fm task list absent and the release ritual separate; 10 build marks, one skipped on security grounds and one narrowed to the existing replay gate; 9 intaken` → brainstorm text treated as data; the re-exec idea rejected because it would run unreviewed lane code against real state [tree f036102e0455] (2026-10-16T12:38:48Z)
- (audit edge) `self: 195 ideas clustered into 46 clusters by one grounding agent (all placed, script-checked); spot-checked fm task list absent and the release ritual separate; 10 build marks, one skipped on security grounds and one narrowed to the existing replay gate; 9 intaken` → 11 done and 3 false-premise clusters marked, not re-captured [tree f036102e0455] (2026-10-16T12:38:48Z)
- (audit operator) `self: 195 ideas clustered into 46 clusters by one grounding agent (all placed, script-checked); spot-checked fm task list absent and the release ritual separate; 10 build marks, one skipped on security grounds and one narrowed to the existing replay gate; 9 intaken` → catalogue filed under research/; 9 titles in the queue [tree f036102e0455] (2026-10-16T12:38:48Z)
- (audit maintainer) `self: 195 ideas clustered into 46 clusters by one grounding agent (all placed, script-checked); spot-checked fm task list absent and the release ritual separate; 10 build marks, one skipped on security grounds and one narrowed to the existing replay gate; 9 intaken` → yield 9 recorded; round 5 follows the builds [tree f036102e0455] (2026-10-16T12:38:48Z)
## Log
- 2026-10-16T12:10:57Z created
- 2026-10-16T12:11:32Z set status=planned
- 2026-10-16T12:14:34Z focused
- 2026-10-16T12:15:50Z paused: focus moved to T-1177
- 2026-10-16T12:38:24Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-16T12:38:24Z focused
- 2026-10-16T12:38:49Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1150 [RESEARCH M, done, 3 steps] Forever loop round 2: brainstorm past everything shipped through 1.2.32, ground every idea, queue what's real — lesson: one grounding …
- T-1057 [FEATURE M, done, 3 steps] Forever loop: fm loop on makes Foreman improve itself without end: when the queue and inbo — lesson: An invariant that ends a loop must…
- T-0818 [RESEARCH M, done, 3 steps] Round 2 brainstorm: improvements on top of round 1 (what shipped today), past every earlier idea — lesson: Round 2 of a recursive loop…
- decision 2026-10-16: Recommendation: build the 15 grounded items T-1155..T-1169 with up to 4 builders, then run round 3 against the improved tree; would change if: round…
## Decision
Recommendation: build the 9 grounded items T-1180..T-1188 with builders; the worktree-fm re-exec idea is skipped (unreviewed lane code would write real state); would change if: a round grounds fewer than 3 new valuable ideas (dry).
## Lessons
- check a brainstorm's 'make X automatic' ideas against what X would be allowed to do: automation that bypasses review is a skip
