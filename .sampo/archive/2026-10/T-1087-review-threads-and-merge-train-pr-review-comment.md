---
id: T-1087
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T09:08:10Z
base: bd613efcaddb5435396223f0b36bd9b8b845f51e
base_tree: 5658384086dfaff3a2d4a42cfdab1360c5c84ea6
plan0_at: 2026-10-16T08:45:14Z
plan0_scope: []
verified: strong
---
# Review threads and merge train: PR review comments become task steps; approved branches me
## Raw request
> FEATURE: Review threads and merge train: PR review comments become task steps; approved branches merge in order with a re-test each (catalogue C11)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
Two PR verbs through gh. 'fm pr threads ID' turns a task's PR unresolved review comments into task steps (quoted as data, each once). 'fm pr train' merges approved PRs in order, re-running the gates on each rebased head first; it stops at the first red and never merges a PR that isn't approved with green checks.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm pr threads T-x adds each unresolved review comment once as a step quoted as data; a second run adds none — verify with `python3 plugin/tests/run.py test_pr_train`
- [x] fm pr train merges approved, green PRs in order after a passing re-test, stops at the first red re-test, and never merges an unapproved PR — verify with `python3 plugin/tests/run.py test_pr_train`
## Non-goals
## Approach (options → choice → why)
Extend fmcli's pr command with an action (threads, train). The gh calls are 'gh pr view --json reviews,reviewDecision,statusCheckRollup' and 'gh api' for review comments. The train merges with 'gh pr merge --merge' only after a local fm check on the PR head in a scratch worktree. Merging is outward: the train asks once per run (fm ask ID merge) unless the standing yes covers it. Tests use a fake gh. Options considered: the GitHub merge queue (needs repo settings), or comments as captured tasks (they belong to the PR's task).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests with a fake gh: threads (comments to steps, idempotent, injection quoted), train (order, stop at red, skip unapproved)
2. [x] Implement threads and train in the pr command; the merge needs fm ask merge; docs
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_pr_train` → ✗ exit 1 · Ran 4 tests in 4.5s (1 classes, 16 at a time; slowest: PrTrain 4s) / FAILED (1 classes) [ran] [tree d43d2af319bf] (2026-10-16T08:46:44Z)
- (step 2) `python3 plugin/tests/run.py test_pr_train` → exit 0 · Ran 4 tests in 10.4s (1 classes, 16 at a time; slowest: PrTrain 10s) / OK [ran] [tree 06ae2bf61bc9] (2026-10-16T08:47:27Z)
- (step 1) `python3 plugin/tests/run.py test_pr_train` → ✗ exit 1 · Ran 9 tests in 3.8s (1 classes, 16 at a time; slowest: PrTrain 4s) / FAILED (1 classes) [ran] [tree 2e9c0d8541bc] (2026-10-16T08:54:52Z)
- (step 2) `python3 plugin/tests/run.py test_pr_train` → exit 0 · Ran 9 tests in 26.7s (1 classes, 16 at a time; slowest: PrTrain 26s) / OK [ran] [tree 68972c004db9] (2026-10-16T08:56:19Z)
- (step 1) `python3 plugin/tests/run.py test_pr_train test_ci_watch test_help` → exit 0 · Ran 17 tests in 4.0s (4 classes, 16 at a time; slowest: PrTrain 4s, CiWatch 1s, Help 1s) / OK [ran] [tree a05fabab4237] (2026-10-16T09:07:23Z)
- (ac 1) `python3 plugin/tests/run.py test_pr_train` → exit 0 · Ran 9 tests in 4.0s (1 classes, 16 at a time; slowest: PrTrain 4s) / OK [ran] [tree a05fabab4237] (2026-10-16T09:07:27Z)
- (ac 2) `python3 plugin/tests/run.py test_pr_train` → exit 0 · Ran 9 tests in 4.0s (1 classes, 16 at a time; slowest: PrTrain 4s) / OK [ran] [tree a05fabab4237] (2026-10-16T09:07:27Z)
- (audit intent) `fm-reviewer (intent, adversary, edge, operator, maintainer): the merge didn't pin the tested commit → --match-head-commit <tested sha>; PR code runs during the re-test → documented (trusted PRs only); a standing publish grant authorized every train → spent per run; comment path not defanged and a quoting comment could hide another → same pipeline, exact prefix; empty rollup counted green, drafts merged, mid-train failure lost the merged list → fixed, all tested on the builder's branch` → review comments become steps; approved green PRs merge in order after a re-test [tree a05fabab4237] (2026-10-16T09:07:27Z)
- (audit adversary) `fm-reviewer (intent, adversary, edge, operator, maintainer): the merge didn't pin the tested commit → --match-head-commit <tested sha>; PR code runs during the re-test → documented (trusted PRs only); a standing publish grant authorized every train → spent per run; comment path not defanged and a quoting comment could hide another → same pipeline, exact prefix; empty rollup counted green, drafts merged, mid-train failure lost the merged list → fixed, all tested on the builder's branch` → comment text is data; merges pin the tested sha; one grant, one train [tree a05fabab4237] (2026-10-16T09:07:27Z)
- (audit edge) `fm-reviewer (intent, adversary, edge, operator, maintainer): the merge didn't pin the tested commit → --match-head-commit <tested sha>; PR code runs during the re-test → documented (trusted PRs only); a standing publish grant authorized every train → spent per run; comment path not defanged and a quoting comment could hide another → same pipeline, exact prefix; empty rollup counted green, drafts merged, mid-train failure lost the merged list → fixed, all tested on the builder's branch` → empty rollup, draft, pending check, merge failure after a merge [tree a05fabab4237] (2026-10-16T09:07:27Z)
- (audit operator) `fm-reviewer (intent, adversary, edge, operator, maintainer): the merge didn't pin the tested commit → --match-head-commit <tested sha>; PR code runs during the re-test → documented (trusted PRs only); a standing publish grant authorized every train → spent per run; comment path not defanged and a quoting comment could hide another → same pipeline, exact prefix; empty rollup counted green, drafts merged, mid-train failure lost the merged list → fixed, all tested on the builder's branch` → the merged list is always printed; a red stops the train [tree a05fabab4237] (2026-10-16T09:07:27Z)
- (audit maintainer) `fm-reviewer (intent, adversary, edge, operator, maintainer): the merge didn't pin the tested commit → --match-head-commit <tested sha>; PR code runs during the re-test → documented (trusted PRs only); a standing publish grant authorized every train → spent per run; comment path not defanged and a quoting comment could hide another → same pipeline, exact prefix; empty rollup counted green, drafts merged, mid-train failure lost the merged list → fixed, all tested on the builder's branch` → fmpr.py shares fmci's gh helper and c._git [tree a05fabab4237] (2026-10-16T09:07:28Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T08:45:02Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1087.builder.md
- 2026-10-16T08:45:13Z focused
- 2026-10-16T09:05:05Z merged worktree-agent-ab36a2eb87e0a4dfc (6 file(s))
- 2026-10-16T09:05:05Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab36a2eb87e0a4dfc
- 2026-10-16T09:07:18Z focused
- 2026-10-16T09:07:23Z scope: CHANGELOG.md, MASTER.md lines committed with T-1058's close; plugin/lib/fmci.py — the shared gh helper's message is generic now
- 2026-10-16T09:08:10Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1079 [PERFORMANCE S, done, 2 steps] Unexplained spend alarm: spend with no Foreman task or turn to explain it is flagged in fm — lesson: Window reports read every ledg…
- T-1076 [FEATURE M, done, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an — lesson: A bundled list of upstream facts n…
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
## Lessons
- Merge what you tested: pin the sha the gates saw
## Plan gaps
- failed first: step 1 Failing tests with a fake gh: threads (comments to steps, idempotent, injection quoted), train (ord…
## Files touched
- plugin/tests/test_pr_train.py
- plugin/lib/fmpr.py
- plugin/lib/fmcli.py
- plugin/lib/fmcost.py
- MASTER.md
- plugin/lib/fmci.py
- CHANGELOG.md
