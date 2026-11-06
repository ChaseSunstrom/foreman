---
id: T-0379
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmlanes.py, plugin/tests/test_builder.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-09T00:41:25Z
updated: 2026-10-09T00:43:48Z
base: f2c88b6057473b3738cf925d9553f040f2d3e5d8
base_tree: bfed826730d6bd85b95fd870c4f10635b722bceb
verified: strong
---
# Builder brief: start from the main checkout's commit; isolation refusals are reported for the main thread, not retried
## Raw request
> Builder lanes under Claude Code's worktree isolation: on JARVIS (2026-10-09) builders were refused 'this agent is isolated in the worktree … but this command runs make/gradle/expo/sed / is too complex' over and over. The builder brief should say: such a refusal is the harness, not a bug — don't retry or rephrase; run what it allows (unit tests in the worktree), commit, and list the refused verifications in the report so the main thread runs them after fm lane merge; and fm lane brief should mark criteria whose verify command needs a build tool as main-thread checks
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the builder brief names the base commit and the isolation rule — verify with `python3 plugin/tests/run.py -k test_the_brief_names_its_base_and_the_isolation_rule`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: base commit + isolation rule in the contract
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py -k test_the_brief_names_its_base_and_the_isolation_rule` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Brief 0s) / OK [ran] [tree 31e3958bbd28] (2026-10-09T00:43:41Z)
- (step 1) `python3 plugin/tests/run.py -k test_the_brief_names_its_base_and_the_isolation_rule` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Brief 0s) / OK [ran] [tree 31e3958bbd28] (2026-10-09T00:43:41Z)
- (audit self) `self: contract text only, plus the base sha read from the main checkout; the guard's confine still bounds the builder, and the fast-forward runs inside its own worktree` → no findings [tree 31e3958bbd28] (2026-10-09T00:43:41Z)
- `python3 plugin/tests/run.py -k test_the_brief_names_its_base_and_the_isolation_rule` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Brief 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 31e3958bbd28] (2026-10-09T00:43:48Z)
- `python3 plugin/tests/run.py -k test_the_brief_names_its_base_and_the_isolation_rule` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Brief 0s) / OK [ran] [tree 31e3958bbd28] (2026-10-09T00:43:48Z)
- (audit self) `self: contract text only, plus the base sha read from the main checkout; the guard's confine still bounds the builder, and the fast-forward runs inside its own worktree` → no findings [tree 31e3958bbd28] (2026-10-09T00:43:48Z)
## Log
- 2026-10-09T00:41:25Z created
- 2026-10-09T00:42:35Z also: Claude Code's isolation worktree starts from the default branch (local main), not the current branch, so a builder works on stale code when the session is on another branch; fm lane brief should tell the builder to check out the task's base first, or warn when HEAD isn't on the default branch
- 2026-10-09T00:43:11Z planned from capture
- 2026-10-09T00:43:11Z focused
- 2026-10-09T00:43:48Z done
- 2026-10-09T00:43:48Z committed 0bdff43 (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- research T-0134-review: Verdict: changes needed.** One finding is a real wrong-view bug and one is a real data-loss gap. The rest are lower. [stale: plugin/lib/fmcore.py…
- T-0260 [FEATURE M, dropped, 3 steps] Evidence quality: inconclusive runs, assumed vs verified facts, surprise log
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- likely tests for the scope: plugin/tests/test_lanes.py
## Lessons
- Watch the harness's own refusals too: 20+ 'isolated in the worktree' failures in an hour were builders retrying commands the harness will never allow
## Files touched
- plugin/tests/test_builder.py
- plugin/lib/fmlanes.py
- CHANGELOG.md
