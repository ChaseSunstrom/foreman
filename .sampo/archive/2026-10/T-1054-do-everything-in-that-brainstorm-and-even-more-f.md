---
id: T-1054
type: RESEARCH
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T03:46:24Z
updated: 2026-10-16T05:00:21Z
base: 3f1148819ec4e49ee69a0f07e53fe29ba7630b63
base_tree: 4c27ddbdf9cfbc3cc1dac898896bbfa12545e261
verified: strong
---
# Do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder
## Raw request
> do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple etc.
## Interpretation
The user wants every idea from the brainstorm built, plus more and wilder ones, and a way for Foreman to keep looping on itself. This research task runs the wild round, clusters and grounds every idea, records the catalogue, turns every cluster into a brief, and updates the catalogue page; the building is the briefs' own work.
## Assumptions (confidence)
## Acceptance criteria
- [x] the wild round's clusters are recorded and every cluster is a brief — verify with `fm research list`
## Non-goals
## Approach (options → choice → why)
fm ideas with six wild lenses, 3 rounds, deepen 3, crossbreed, past the six newest earlier brainstorms; one fm-recon to cluster; one brief per cluster (fm intake), the catalogue's skips turned into briefs too; the page updated; plans written by fm-recon planners in waves so builders can start. Rejected: a slate of the top few (the user asked for every idea).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Wild round, clusters, briefs, catalogue page
## Resume here
## Docs impact
none: research only; the catalogue page and research notes are the record
## Verification evidence
- (ac 1) `fm research list` → exit 0 · wave3-intent  2026-09-26  708B  Wave 3 intent audit (fm-reviewer, read-only) over wave3.diff + wave3-stages-ear… / claude-code-capabilities-2026-09-26  2026-09-26  1497B  Claude Code 2.1.280 capabilit [ran] [tree 4c27ddbdf9cf] (2026-10-16T05:00:09Z)
- (step 1) `fm research list` → exit 0 · wave3-intent  2026-09-26  708B  Wave 3 intent audit (fm-reviewer, read-only) over wave3.diff + wave3-stages-ear… / claude-code-capabilities-2026-09-26  2026-09-26  1497B  Claude Code 2.1.280 capabilit [ran] [tree 4c27ddbdf9cf] (2026-10-16T05:00:09Z)
- (audit intent) `self: wild round ran (brainstorm-20261015-224705, ~290 distinct titles), clustered into 24 by fm-recon (research brainstorm-20261016-wild-clusters), every cluster plus the earlier catalogue's skips captured as briefs T-1057..T-1087 (fm decide recorded), the catalogue page updated (A72nxRvpEy7y47AqhZ1KYj, 43 groups, 516 ideas), 46 briefs planned by fm-recon in two waves` → every cluster is a brief, none dropped; the forever loop (T-1057) shipped first [tree 4c27ddbdf9cf] (2026-10-16T05:00:09Z)
- (audit operator) `self: wild round ran (brainstorm-20261015-224705, ~290 distinct titles), clustered into 24 by fm-recon (research brainstorm-20261016-wild-clusters), every cluster plus the earlier catalogue's skips captured as briefs T-1057..T-1087 (fm decide recorded), the catalogue page updated (A72nxRvpEy7y47AqhZ1KYj, 43 groups, 516 ideas), 46 briefs planned by fm-recon in two waves` → the page shows every idea with its mark and task [tree 4c27ddbdf9cf] (2026-10-16T05:00:09Z)
- (audit adversary) `self: wild round ran (brainstorm-20261015-224705, ~290 distinct titles), clustered into 24 by fm-recon (research brainstorm-20261016-wild-clusters), every cluster plus the earlier catalogue's skips captured as briefs T-1057..T-1087 (fm decide recorded), the catalogue page updated (A72nxRvpEy7y47AqhZ1KYj, 43 groups, 516 ideas), 46 briefs planned by fm-recon in two waves` → brainstorm and recon text were treated as data; no idea was acted on without a brief and its own review [tree 4c27ddbdf9cf] (2026-10-16T05:00:09Z)
- (audit edge) `self: wild round ran (brainstorm-20261015-224705, ~290 distinct titles), clustered into 24 by fm-recon (research brainstorm-20261016-wild-clusters), every cluster plus the earlier catalogue's skips captured as briefs T-1057..T-1087 (fm decide recorded), the catalogue page updated (A72nxRvpEy7y47AqhZ1KYj, 43 groups, 516 ideas), 46 briefs planned by fm-recon in two waves` → the 409 vs ~290 count mismatch in ideas.md is captured (T-1056); repeats of finished work are marked near T-… for grounding [tree 4c27ddbdf9cf] (2026-10-16T05:00:09Z)
- (audit maintainer) `self: wild round ran (brainstorm-20261015-224705, ~290 distinct titles), clustered into 24 by fm-recon (research brainstorm-20261016-wild-clusters), every cluster plus the earlier catalogue's skips captured as briefs T-1057..T-1087 (fm decide recorded), the catalogue page updated (A72nxRvpEy7y47AqhZ1KYj, 43 groups, 516 ideas), 46 briefs planned by fm-recon in two waves` → no code; research notes, briefs and the page are the record [tree 4c27ddbdf9cf] (2026-10-16T05:00:09Z)
- `fm research list` → exit 0 · wave3-intent  2026-09-26  708B  Wave 3 intent audit (fm-reviewer, read-only) over wave3.diff + wave3-stages-ear… / claude-code-capabilities-2026-09-26  2026-09-26  1497B  Claude Code 2.1.280 capabilit [ran] [tree 4c27ddbdf9cf] (2026-10-16T05:00:20Z)
- (audit intent) `self: wild round ran (brainstorm-20261015-224705, ~290 distinct titles), clustered into 24 by fm-recon (research brainstorm-20261016-wild-clusters), every cluster plus the earlier catalogue's skips captured as briefs T-1057..T-1087 (fm decide recorded), the catalogue page updated (A72nxRvpEy7y47AqhZ1KYj, 43 groups, 516 ideas), 46 briefs planned by fm-recon in two waves` → every cluster is a brief, none dropped; the forever loop (T-1057) shipped first [tree 4c27ddbdf9cf] (2026-10-16T05:00:20Z)
- (audit operator) `self: wild round ran (brainstorm-20261015-224705, ~290 distinct titles), clustered into 24 by fm-recon (research brainstorm-20261016-wild-clusters), every cluster plus the earlier catalogue's skips captured as briefs T-1057..T-1087 (fm decide recorded), the catalogue page updated (A72nxRvpEy7y47AqhZ1KYj, 43 groups, 516 ideas), 46 briefs planned by fm-recon in two waves` → the page shows every idea with its mark and task [tree 4c27ddbdf9cf] (2026-10-16T05:00:20Z)
- (audit adversary) `self: wild round ran (brainstorm-20261015-224705, ~290 distinct titles), clustered into 24 by fm-recon (research brainstorm-20261016-wild-clusters), every cluster plus the earlier catalogue's skips captured as briefs T-1057..T-1087 (fm decide recorded), the catalogue page updated (A72nxRvpEy7y47AqhZ1KYj, 43 groups, 516 ideas), 46 briefs planned by fm-recon in two waves` → brainstorm and recon text were treated as data; no idea was acted on without a brief and its own review [tree 4c27ddbdf9cf] (2026-10-16T05:00:20Z)
- (audit edge) `self: wild round ran (brainstorm-20261015-224705, ~290 distinct titles), clustered into 24 by fm-recon (research brainstorm-20261016-wild-clusters), every cluster plus the earlier catalogue's skips captured as briefs T-1057..T-1087 (fm decide recorded), the catalogue page updated (A72nxRvpEy7y47AqhZ1KYj, 43 groups, 516 ideas), 46 briefs planned by fm-recon in two waves` → the 409 vs ~290 count mismatch in ideas.md is captured (T-1056); repeats of finished work are marked near T-… for grounding [tree 4c27ddbdf9cf] (2026-10-16T05:00:20Z)
- (audit maintainer) `self: wild round ran (brainstorm-20261015-224705, ~290 distinct titles), clustered into 24 by fm-recon (research brainstorm-20261016-wild-clusters), every cluster plus the earlier catalogue's skips captured as briefs T-1057..T-1087 (fm decide recorded), the catalogue page updated (A72nxRvpEy7y47AqhZ1KYj, 43 groups, 516 ideas), 46 briefs planned by fm-recon in two waves` → no code; research notes, briefs and the page are the record [tree 4c27ddbdf9cf] (2026-10-16T05:00:20Z)
## Log
- 2026-10-16T03:46:24Z created
- 2026-10-16T03:47:16Z steer: and maybe a way to forever loop a brainstorm/yourself? not sure — build an endless self-improvement loop (build round → review what shipped → wild brainstorm on top → slate → build), paced by budget, stopping only on dry/budget/user
- 2026-10-16T04:11:23Z steer: absolutely all of those ideas and FULLY implement EVERY single one! — every idea in every cluster (wild W0-W23 and catalogue C1-C17, 516 items) is in scope for its cluster's brief, not a slate; builders in parallel
- 2026-10-16T04:59:54Z focused
- 2026-10-16T05:00:21Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1077 [CLEAN S, active, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged
- T-1076 [FEATURE M, active, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- decision 2026-10-16: T-1054: every wild cluster (23) plus the earlier catalogue's skips became briefs T-1057..T-1087; the forever loop (T-1057) goes first after the demo…
- the similar finished task took 2 steps
## Decision
Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→checkers, survival, user proxy, speculative next, tamper-evident ledger, guard mutation), with up to four builders in parallel; would change if: a cluster's grounding shows it already exists or its premise is false (then it is dropped with that reason).
## Lessons
- A wild round needs lenses that name the wildness (moonshots, self-improving harness, steal from other fields) and --seen of earlier runs; default lenses come back incremental
