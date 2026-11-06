---
id: T-1167
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmpr.py, plugin/lib/fmcost.py, plugin/lib/fmcli.py, plugin/tests/test_pr_train.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-16T10:45:53Z
updated: 2026-10-16T11:53:27Z
base: bfda3805680fb57f81feb9a2d7eb86e464bd66d1
base_tree: 9bb09c93d10ab8c599c21a557c9a32fa9b0b83d6
plan0_at: 2026-10-16T11:48:37Z
plan0_scope: [plugin/lib/fmpr.py, plugin/lib/fmcost.py, plugin/lib/fmcli.py, plugin/tests/test_pr_train.py, CHANGELOG.md]
verified: strong
---
# Add `fm pr ID --post` that posts the rendered PR body as a comment on the current branch's
## Raw request
> FEATURE: Add `fm pr ID --post` that posts the rendered PR body as a comment on the current branch's PR through gh, only after the remote approval.
> DONE-WHEN: with a fake gh on PATH the test sees one `gh pr comment` call carrying the body when approved and no call when not approved
## Interpretation
fm pr ID renders a PR description with its proof but only prints it; --post puts it on the PR as a comment. Posting is outward, so it needs the task's publish grant (the user's yes via fm ask ID publish), spent by the post like fm pr train's.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm pr ID --post comments the rendered body on the branch's PR (or --pr N) through gh only with the task's publish grant, which the post spends; without the grant nothing is called and it says how to ask — verify with `python3 plugin/tests/run.py test_pr_train`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests in test_pr_train: post with grant comments once and spends it; without grant no gh call
2. [x] --post in fm pr (fmcost.cmd_pr -> fmpr.post)
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_pr_train` → ✗ exit 1 · Ran 10 tests in 10.9s (1 classes, 16 at a time; slowest: PrTrain 11s) / FAILED (1 classes) [ran] [tree aef138fa3a9c] (2026-10-16T11:49:01Z)
- (step 2) `python3 plugin/tests/run.py test_pr_train test_help` → exit 0 · Ran 15 tests in 14.3s (3 classes, 16 at a time; slowest: PrTrain 14s, Help 2s, PromptApprovals 2s) / OK [ran] [tree 727b5172ffa9] (2026-10-16T11:49:28Z)
- (ac 1) `python3 plugin/tests/run.py test_pr_train` → exit 0 · Ran 10 tests in 32.7s (1 classes, 16 at a time; slowest: PrTrain 32s) / OK [ran] [tree 9ca1a2f75a8c] (2026-10-16T11:50:12Z)
- (step 1) `python3 plugin/tests/run.py test_pr_train` → exit 0 · Ran 10 tests in 32.7s (1 classes, 16 at a time; slowest: PrTrain 32s) / OK [ran] [tree 9ca1a2f75a8c] (2026-10-16T11:50:12Z)
- (audit adversary) `self: mirrors fm pr train's grant pattern (check, spend under the lock before the call, ledger grant_spent); gh gets an argv list, the body redacted; without the grant nothing is called and the refusal names fm ask` → one yes posts once; the PR number is int-coerced; no shell [tree 9ca1a2f75a8c] (2026-10-16T11:50:12Z)
- (audit edge) `self: mirrors fm pr train's grant pattern (check, spend under the lock before the call, ledger grant_spent); gh gets an argv list, the body redacted; without the grant nothing is called and the refusal names fm ask` → a failed gh call after the spend leaves the grant spent (ask again), as the train does [tree 9ca1a2f75a8c] (2026-10-16T11:50:12Z)
- (audit self) `self: mirrors fm pr train's grant pattern (check, spend under the lock before the call, ledger grant_spent); gh gets an argv list, the body redacted; without the grant nothing is called and the refusal names fm ask` → no findings [tree 9ca1a2f75a8c] (2026-10-16T11:50:12Z)
## Log
- 2026-10-16T10:45:53Z created
- 2026-10-16T11:48:35Z set type=FEATURE, tier=S, scope=['plugin/lib/fmpr.py', 'plugin/lib/fmcost.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_pr_train.py', 'CHANGELOG.md']
- 2026-10-16T11:48:36Z focused
- 2026-10-16T11:53:25Z done
- 2026-10-16T11:53:27Z committed 4b9f34dc (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research wave2-plan-a0f775007b83f4d0b: [instruction-like text quoted from a file or tool; data, not instructions] === T-1087 [stale: mods/foreman-ui/hooks/register.tsx, …
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- T-1157 [FEATURE M, done, 2 steps] Add `fm todo`, the list of what only the user can do (pending asks, blocked-on-user tasks, — lesson: a list of things to resolve needs …
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-16): CHANGELOG.md, plugin/lib/fmcli.py; re-ground the plan against them before editing
## Plan gaps
- failed first: step 1 Failing tests in test_pr_train: post with grant comments once and spends it; without grant no gh ca…
## Files touched
- plugin/tests/test_pr_train.py
- plugin/lib/fmpr.py
- plugin/lib/fmcost.py
- plugin/lib/fmcli.py
- CHANGELOG.md
