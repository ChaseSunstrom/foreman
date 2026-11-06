---
id: T-0346
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-06T03:39:39Z
updated: 2026-10-06T03:40:49Z
base: 702872930fddada42a58de7ed4d1ec8d3716289f
base_tree: e5d46227c353d9ab663eea8a1acf8dc1bdddc347
verified: strong
---
# Usage pace on each device: fm projects --json usage, a sidebar meter in the app
## Raw request
> Usage pace on each device: fm projects --json usage, a sidebar meter in the app
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm projects --json carries the device's usage (5-hour %, weekly %, share of the week gone) from the statusline snapshot, {} without one — verify with `python3 plugin/tests/run.py -k test_projects`
- [x] the app type-checks — verify with `bash -c 'cd ~/projects/foreman-desktop && bun run check'`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm: usage in projects (red→green)
2. [x] app: sidebar meter, verified on screen
## Resume here
## Docs impact
CHANGELOG; app README
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_projects.Usage` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Usage 0s) / FAILED (1 classes) [ran] [tree db697b99dd4a] (2026-10-06T03:39:44Z)
- (step 1) `python3 plugin/tests/run.py -k test_projects.Usage` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Usage 0s) / OK [ran] [tree a7c4b0d0325c] (2026-10-06T03:40:46Z)
- (step 2) `ls /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/r2-usage-crop.png` → exit 0 · /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/r2-usage-crop.png [ran] [tree a7c4b0d0325c] (2026-10-06T03:40:46Z)
- (ac 1) `python3 plugin/tests/run.py -k test_projects` → exit 0 · Ran 4 tests in 0.5s (3 classes, 16 at a time; slowest: Follow 0s, Projects 0s, Usage 0s) / OK [ran] [tree a7c4b0d0325c] (2026-10-06T03:40:49Z)
- (ac 2) `bash -c 'cd ~/projects/foreman-desktop && bun run check'` → exit 0 · 1791258049047 START "~/projects/foreman-desktop" / 1791258049047 COMPLETED 199 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS [ran] [tree a7c4b0d0325c] (2026-10-06T03:40:49Z)
- (audit self) `self-review: usage is read-only (fmbudget.rate_limits from the statusline snapshot), {} when absent; --follow refreshes it on its 30 s tick instead of watching the snapshot folder (which changes every statusline refresh); app type-check clean; meter verified in a screenshot (18% / 68% under pace)` → no findings [tree a7c4b0d0325c] (2026-10-06T03:40:49Z)
## Log
- 2026-10-06T03:39:39Z created
- 2026-10-06T03:39:39Z focused
- 2026-10-06T03:40:46Z scope: app repo ~/projects/foreman-desktop
- 2026-10-06T03:40:49Z done
- 2026-10-06T03:40:49Z committed 5f0e812 (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0322 [FEATURE M, done, 3 steps] fm projects --json and fm ui --follow: a device-wide read surface for the desktop app — lesson: A follow stream is the cheapest live AP…
- research T-0318-review: Verdict: changes needed.** There are no injection holes. The real problems are remote process leaks and silent failures in the session view.
- T-0320 [FEATURE M, done, 3 steps] Subagents budgeted by usage pace, not a daily token count — lesson: Budget by the real constraint: a proxy cap (tokens/day, with cache …
- decision 2026-10-06: Desktop app architecture: no daemon — the Tauri app drives fm --json locally or over ssh (Tailscale SSH) per device; agent sessions are supervised b…
## Files touched
- plugin/tests/test_projects.py
- plugin/lib/fmwatch.py
- CHANGELOG.md
