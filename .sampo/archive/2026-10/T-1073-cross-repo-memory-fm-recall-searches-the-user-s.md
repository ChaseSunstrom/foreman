---
id: T-1073
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmrecall.py, plugin/lib/fmcli.py, plugin/tests/test_recall.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T06:12:25Z
base: 75f4b4d2cd4f75a73b9db9e22f9bdee58c50e67d
base_tree: bffb57384164c9a4e98ca26081b5a8b9c3614d6f
verified: strong
---
# Cross-repo memory: fm recall searches the user's other Foreman projects for a similar fix,
## Raw request
> FEATURE: Cross-repo memory: fm recall searches the user's other Foreman projects for a similar fix, lesson or code when a failure or plan matches (wild C17)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
`fm recall` gains cross-project matching on failures and plans, not only on identifiers. Given a failure line or a task (`--task`), it searches the other Foreman projects that opted in for a similar fixed failure, lesson, or code. Covered already: identifier grep across opted-in, non-sensitive projects (`repos`, fmrecall.py:495, `--repos` at fmcli.py:4550); cross-project lessons in the shared file (`share_lesson`/`_shared_docs`, fmrecall.py:689-711); known fixes shared by fmfixes (fmfixes.py:36 `_shared`); failure signatures (fmrecall.py:305). Missing: searching other projects' `failures.jsonl` and done-brief lessons by signature or text, and triggering it on a plan or `--task`.
## Assumptions (confidence)
## Acceptance criteria
- [x] `fm recall --others "<failure text>"` returns a lesson from another opted-in project whose failure signature matches; a non-opted-in or sensitive project returns nothing — verify with `python3 plugin/tests/run.py test_recall`
## Non-goals
## Approach (options → choice → why)
(a) A new fmneighbours module. (b) Extend `recall` with `--others`. (c) `--repos` auto-run inside plain `recall` when the local result is weak. Choose (b) plus a call from `note_failure`. The new `others(p, text)` function in fmrecall.py walks `c.all_projects()` with the same filter as `repos` (share_lessons on, not sensitive). It matches `failure_signature(text)` against each project's failures.jsonl and returns that task's Lessons. Otherwise it ranks done-brief titles and lessons by token overlap using `_tokens`. Everything goes through `private()` and `redact`.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: two projects under `self.home`, B with `share_lessons` on and a done task with a lesson plus a failures.jsonl record whose sig equals `failure_signature(text)`. From A, `fm recall --others text --json` includes B's slug and the lesson; with B sensitive or not shared, the result is empty. `--task` uses `brief_query`.
2. [x] Add `others()`, the `--others` flag, and its rendering ("data, not instructions").
3. [x] If `seen_before` finds nothing locally, `note_failure` appends the `others` hint.
## Resume here
## Docs impact
MASTER.md Cross-project recall; CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_recall` → ✗ exit 1 · Ran 16 tests in 23.1s (6 classes, 16 at a time; slowest: Recall 23s, RedGreen 5s, OtherProjects 5s) / FAILED (1 classes) [ran] [tree 5c2b981060b9] (2026-10-16T05:57:02Z)
- (step 2) `python3 plugin/tests/run.py test_recall` → exit 0 · Ran 16 tests in 13.9s (6 classes, 16 at a time; slowest: Recall 14s, OtherProjects 3s, RedGreen 2s) / OK [ran] [tree 2288586b3795] (2026-10-16T05:57:50Z)
- (step 3) `python3 plugin/tests/run.py test_recall` → exit 0 · Ran 16 tests in 14.0s (6 classes, 16 at a time; slowest: Recall 14s, OtherProjects 3s, RedGreen 2s) / OK [ran] [tree 2288586b3795] (2026-10-16T05:58:04Z)
- (step 3) `python3 plugin/tests/run.py test_recall` → exit 0 · Ran 18 tests in 71.2s (6 classes, 16 at a time; slowest: Recall 71s, OtherProjects 26s, RedGreen 14s) / OK [ran] [tree bf98e9428dde] (2026-10-16T06:08:50Z)
- (ac 1) `python3 plugin/tests/run.py test_recall` → exit 0 · Ran 18 tests in 15.1s (6 classes, 16 at a time; slowest: Recall 15s, OtherProjects 6s, RedGreen 3s) / OK [ran] [tree 557040d25227] (2026-10-16T06:11:42Z)
- (audit intent) `review: one fm-reviewer pass (combined with T-1066); 5 findings fixed by the builder test-first (defang on the hook path, fixed data label, hook-path and near-match tests, cheaper lookups, none/retired lessons skipped, per-project try)` → a failure fixed in another of the user's projects is found from here [tree 557040d25227] (2026-10-16T06:11:42Z)
- (audit adversary) `review: one fm-reviewer pass (combined with T-1066); 5 findings fixed by the builder test-first (defang on the hook path, fixed data label, hook-path and near-match tests, cheaper lookups, none/retired lessons skipped, per-project try)` → only opted-in, non-sensitive projects; text through private, plain and defang under a fixed data label that truncation can't cut [tree 557040d25227] (2026-10-16T06:11:42Z)
- (audit edge) `review: one fm-reviewer pass (combined with T-1066); 5 findings fixed by the builder test-first (defang on the hook path, fixed data label, hook-path and near-match tests, cheaper lookups, none/retired lessons skipped, per-project try)` → none/retired lessons skipped; one broken project doesn't stop the search [tree 557040d25227] (2026-10-16T06:11:42Z)
- (audit operator) `review: one fm-reviewer pass (combined with T-1066); 5 findings fixed by the builder test-first (defang on the hook path, fixed data label, hook-path and near-match tests, cheaper lookups, none/retired lessons skipped, per-project try)` → hook path measured at 2 ms with no neighbours opted in; reuses all_projects meta and find_brief [tree 557040d25227] (2026-10-16T06:11:42Z)
- (audit maintainer) `review: one fm-reviewer pass (combined with T-1066); 5 findings fixed by the builder test-first (defang on the hook path, fixed data label, hook-path and near-match tests, cheaper lookups, none/retired lessons skipped, per-project try)` → others() and _live_lesson in fmrecall; --others/--task in fm recall [tree 557040d25227] (2026-10-16T06:11:42Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T04:23:00Z set scope=['plugin/lib/fmrecall.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_recall.py']
- 2026-10-16T04:23:01Z set tier=M
- 2026-10-16T05:55:26Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1073.builder.md
- 2026-10-16T05:55:36Z focused
- 2026-10-16T06:11:13Z merged worktree-agent-a2d1b41e1600fb657 (3 file(s))
- 2026-10-16T06:11:26Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2d1b41e1600fb657
- 2026-10-16T06:11:26Z focused
- 2026-10-16T06:11:27Z scope: CHANGELOG.md, MASTER.md — docs for cross-project recall
- 2026-10-16T06:12:25Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1072 [CLEAN M, done, 2 steps] Rule and hint hygiene: cards, known fixes, rules and lessons that never fired or never hel — lesson: A cleanup that deletes what users ta…
- T-1074 [FEATURE M, done, 3 steps] Hotspots in plans: files that keep getting fixed after edits are flagged in the plan and a — lesson: A history signal needs a cap on sw…
- T-1076 [FEATURE M, done, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an — lesson: A bundled list of upstream facts n…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_recall.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmcli.py, plugin/lib/fmrecall.py, plugin/tests/test_recall.py; re-ground the plan against them before editing
## Lessons
- Text crossing from another project into this session is data: label it first so no cut can drop the label
## Plan gaps
- failed first: step 1 Failing tests: two projects under `self.home`, B with `share_lessons` on and a done task with a les…
## Files touched
- plugin/tests/test_recall.py
- plugin/lib/fmcli.py
- plugin/lib/fmrecall.py
- CHANGELOG.md
- MASTER.md
