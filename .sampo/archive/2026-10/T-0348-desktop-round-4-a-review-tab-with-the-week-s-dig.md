---
id: T-0348
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-06T03:46:21Z
updated: 2026-10-06T03:47:28Z
base: 2f0a8f9423a53820c36a850e0d9d0a0f6e90e92f
base_tree: 30501586cacd2a6ddadfb0965977d1be229adce3
verified: strong
---
# Desktop round 4: a Review tab with the week's digest and the friction since the last self-improvement pass
## Raw request
> Desktop round 4: a Review tab with the week's digest and the friction since the last self-improvement pass
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the app runs fm digest and fm friction read-only (friction with --json alone; --mark, --brief and --every refused) — verify with `bash -c 'cd ~/projects/foreman-desktop/src-tauri && cargo test --target-dir /tmp/claude-1000/-home-~--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target 2>&1 | grep -q "test result: ok. 9 passed"'`
- [x] the app type-checks — verify with `bash -c 'cd ~/projects/foreman-desktop && bun run check'`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] allow-list (red→green)
2. [x] Review tab, verified on screen
## Resume here
## Docs impact
CHANGELOG; app README
## Verification evidence
- (step 1) `bash -c 'cd ~/projects/foreman-desktop/src-tauri && cargo test --target-dir /tmp/claude-1000/-home-~--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target 2>&1 | grep -q "test result: ok. 9 passed"'` → ✗ exit 1 · (no output) [ran] [tree 30501586cacd] (2026-10-06T03:46:32Z)
- (step 1) `bash -c 'cd ~/projects/foreman-desktop/src-tauri && cargo test --target-dir /tmp/claude-1000/-home-~--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target 2>&1 | grep -q "test result: ok. 9 passed"'` → exit 0 · (no output) [ran] [tree ce7c72491bb2] (2026-10-06T03:47:21Z)
- (step 2) `bash -c 'cd ~/projects/foreman-desktop/src-tauri && cargo test --target-dir /tmp/claude-1000/-home-~--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target 2>&1 | grep -q "test result: ok. 9 passed"'` → exit 0 · (no output) [ran] [tree ce7c72491bb2] (2026-10-06T03:47:22Z)
- (ac 1) `bash -c 'cd ~/projects/foreman-desktop/src-tauri && cargo test --target-dir /tmp/claude-1000/-home-~--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target 2>&1 | grep -q "test result: ok. 9 passed"'` → exit 0 · (no output) [ran] [tree ce7c72491bb2] (2026-10-06T03:47:27Z)
- (ac 2) `bash -c 'cd ~/projects/foreman-desktop && bun run check'` → exit 0 · 1791258447771 START "~/projects/foreman-desktop" / 1791258447772 COMPLETED 200 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS [ran] [tree ce7c72491bb2] (2026-10-06T03:47:27Z)
- (audit self) `self-review: digest and friction are read-only in Foreman; the allow-list refuses friction --mark/--brief/--every (they move the self-improvement window); cargo tests 9/9, type-check clean, Review tab verified in a screenshot` → no findings [tree ce7c72491bb2] (2026-10-06T03:47:27Z)
## Log
- 2026-10-06T03:46:21Z created
- 2026-10-06T03:46:21Z focused
- 2026-10-06T03:47:25Z scope: app repo ~/projects/foreman-desktop
- 2026-10-06T03:47:27Z done
- 2026-10-06T03:47:28Z committed 1513cfb (1 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0187 [FEATURE M, done, 3 steps] Self-improvement scoreboard: the friction digest rechecks each earlier guard block with today's guard and shows the trend since the las…
- T-0125 [FEATURE M, done, 4 steps] Recursive self-improvement loop: fm friction digests Foreman's own friction since the last pass, fm next calls for a pass every N close…
- research brainstorm-20261003-round5: Quota brake (bold bets) → T-0198 economy mode: the mod reads session.usage rate limits; past 80% weekly / 90% 5-hour a prompt.compos…
- decision 2026-10-03: Self-improvement passes need N closed tasks AND 2 h since the last pass
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–4 steps
## Files touched
- CHANGELOG.md
