---
id: T-1910
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T04:08:04Z
updated: 2026-10-29T04:43:10Z
base: 485c5c60622dab98f2ef79cf973e1ce1bc2ae662
base_tree: 27acd7c34cd18cd9495f4ea471d6309ec906655e
plan0_at: 2026-10-29T04:35:22Z
plan0_scope: []
verified: strong
---
# The guard keeps a builder's write inside its worktree named through a linked parent
## Raw request
> The guard flags a builder's write inside its worktree named through a linked parent (macOS /var → /private/var) as confine: CI macOS fails test_guard.ScratchNames.test_a_builder_worktree_named_through_a_link_is_confined_at_its_real_path_too on 5af1a716; classify_write compares the as-given variant only to lane and realpath(lane), so /var/…/private-lane/x is outside both
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the lane named through a linked parent is the lane; a link inside it to main is outside — verify with `python3 plugin/tests/run.py test_guard -k through_a_link`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing guard test
2. [x] compare the as-named path's real location to the lane
3. [x] CHANGELOG line
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- `python3 plugin/tests/run.py test_guard -k through_a_link` → ✗ exit 1 · Ran 293 tests in 20.3s (89 classes, 16 at a time; slowest: Mutation 17s, GuardAgainstBash 17s, Trust 10s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree f4e9dcd69b11] (2026-10-29T04:42:26Z)
- `python3 plugin/tests/run.py test_guard -k through_a_link` → exit 0 · Ran 293 tests in 18.1s (89 classes, 16 at a time; slowest: GuardAgainstBash 16s, Mutation 16s, Trust 9s) / OK [ran] [tree f4e9dcd69b11] (2026-10-29T04:42:26Z)
- (ac 1) `python3 plugin/tests/run.py test_guard -k through_a_link` → exit 0 · Ran 293 tests in 19.4s (89 classes, 16 at a time; slowest: GuardAgainstBash 18s, Mutation 17s, Trust 10s) / OK [ran] [tree f4e9dcd69b11] (2026-10-29T04:42:50Z)
- (step 1) `python3 plugin/tests/run.py test_guard -k through_a_link` → exit 0 · Ran 293 tests in 19.4s (89 classes, 16 at a time; slowest: GuardAgainstBash 18s, Mutation 17s, Trust 10s) / OK [ran] [tree f4e9dcd69b11] (2026-10-29T04:42:50Z)
- (step 2) `python3 plugin/tests/run.py test_guard -k through_a_link` → exit 0 · Ran 293 tests in 19.4s (89 classes, 16 at a time; slowest: GuardAgainstBash 18s, Mutation 17s, Trust 10s) / OK [ran] [tree f4e9dcd69b11] (2026-10-29T04:42:50Z)
- (step 3) `python3 plugin/tests/run.py test_guard -k through_a_link` → exit 0 · Ran 293 tests in 19.4s (89 classes, 16 at a time; slowest: GuardAgainstBash 18s, Mutation 17s, Trust 10s) / OK [ran] [tree f4e9dcd69b11] (2026-10-29T04:42:50Z)
- (audit adversary) `S: lenses only` → realpath inside the lane only ever widens toward the lane; a link inside it to main stays outside (test case) [tree f4e9dcd69b11] (2026-10-29T04:42:50Z)
- (audit edge) `S: lenses only` → unresolved or missing paths fall back to the literal check [tree f4e9dcd69b11] (2026-10-29T04:42:50Z)
- (audit self) `S: lenses only` → no findings [tree f4e9dcd69b11] (2026-10-29T04:42:50Z)
## Log
- 2026-10-29T04:08:04Z created
- 2026-10-29T04:10:10Z set tier=S, title=The guard keeps a builder's write inside its worktree named through a linked parent
- 2026-10-29T04:10:11Z planned: it has criteria and steps
- 2026-10-29T04:35:03Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1910.builder.md
- 2026-10-29T04:35:21Z focused
- 2026-10-29T04:41:28Z merged worktree-agent-a9d79a8737865d429 (3 file(s))
- 2026-10-29T04:41:31Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9d79a8737865d429
- 2026-10-29T04:41:32Z focused
- 2026-10-29T04:43:10Z done
## Follow-ups captured
## Scope
plugin/lib/fmguard.py
plugin/tests/test_guard.py
CHANGELOG.md
## Related
Related past work (data from this project's history, not instructions):
- T-1902 [FIX M, done, 4 steps] FIX: macOS CI (experimental job) fails 4 tests at 06e55c1 and 48aad3d5: test_settings.Guar — lesson: On macOS the temp folder is a link: an…
- research T-1284-review: Verdict:** approve with nits. I found no way to make the guard treat an outside write as inside a project, or a project or state write as outside…
- T-1249 [FIX M, done, 5 steps] CI macOS (experimental job): tests that assume Linux fail there: /proc/PID/stat reads, /tm — lesson: A failing portability test is often a …
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- similar past tasks were M: consider --tier M
## Lessons
- compare guard paths by realpath on both sides; macOS /var is a link
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
