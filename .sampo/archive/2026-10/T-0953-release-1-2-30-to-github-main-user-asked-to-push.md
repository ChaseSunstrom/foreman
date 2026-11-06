---
id: T-0953
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T21:07:40Z
updated: 2026-10-15T21:13:56Z
base: 8a5e6fc063573603847490cb7c214d176bcb5bdc
base_tree: e71b6354828e00ab18e7e55a9b4af2b3698c52a2
verified: strong
---
# Release 1.2.30 to GitHub main (user asked to push)
## Raw request
> Release 1.2.30 to GitHub main (user asked to push)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] origin/main's tree equals the release commit — verify with `test "$(git rev-parse origin/main^{tree})" = "$(git rev-parse HEAD^{tree})"`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] CHANGELOG, mod 0.8.0, leftover practice cards; release.py 1.2.30 --push
## Resume here
## Docs impact
## Verification evidence
- (step 1) `git fetch -q origin && test "$(git rev-parse origin/main^{tree})" = "$(git rev-parse HEAD^{tree})"` → exit 0 · (no output) [ran] [tree b54c0e4328e7] (2026-10-15T21:13:55Z)
- (ac 1) `test "$(git rev-parse origin/main^{tree})" = "$(git rev-parse HEAD^{tree})"` → exit 0 · (no output) [ran] [tree b54c0e4328e7] (2026-10-15T21:13:56Z)
- (ac 1) `test "$(git rev-parse origin/main^{tree})" = "$(git rev-parse HEAD^{tree})"` → exit 0 · (no output) [ran] [tree b54c0e4328e7] (2026-10-15T21:13:56Z)
- (audit operator) `release.py ran the full gates (1,411 tests, mod suite, hook bench, guard replay) before the push` → ok: origin/main at Foreman 1.2.30, tree equal to HEAD [tree b54c0e4328e7] (2026-10-15T21:13:56Z)
- (audit self) `release.py ran the full gates (1,411 tests, mod suite, hook bench, guard replay) before the push` → no findings [tree b54c0e4328e7] (2026-10-15T21:13:56Z)
## Log
- 2026-10-15T21:07:40Z created
- 2026-10-15T21:07:40Z focused
- 2026-10-15T21:11:32Z focused
- 2026-10-15T21:11:33Z scope: test_round_g's syntax-note test now drives PostToolUseValidate (T-0947 moved the note there)
- 2026-10-15T21:13:56Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0905 [FEATURE S, done, 1 steps] Release 1.2.28: push foreman/build to GitHub main (user asked)
- T-0931 [FEATURE S, done, 1 steps] Release 1.2.29: push foreman/build to GitHub main (user said yes)
- T-0352 [FEATURE M, blocked, 3 steps] Publish Foreman Desktop on GitHub with CI and release pipelines
- decision 2026-10-15: Release as 1.2.28 via release.py --push, not a raw push
- similar finished tasks took 1–1 steps
- start here (files T-0905 touched): .claude-plugin/marketplace.json, CHANGELOG.md, plugin/.claude-plugin/plugin.json
## Lessons
- Run the full suite before release.py when a session changed hook wiring: the release gate caught a stale test the lanes' affected runs missed (now T-0952).
## Files touched
- .claude-plugin/marketplace.json
- mods/foreman-ui/.claude-plugin/plugin.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
- plugin/tests/test_round_g.py
