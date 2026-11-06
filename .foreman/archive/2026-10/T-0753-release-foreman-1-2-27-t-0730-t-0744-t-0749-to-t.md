---
id: T-0753
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T21:43:11Z
updated: 2026-10-09T21:45:17Z
base: b6168e79f378624fe87a31d28a9e63705f831e36
base_tree: e5a74fd0c41147c6b28c44439499f05877915398
verified: ok
---
# Release Foreman 1.2.27 (T-0730, T-0744, T-0749 to T-0752) to GitHub main and JARVIS
## Raw request
> Release Foreman 1.2.27 (T-0730, T-0744, T-0749 to T-0752) to GitHub main and JARVIS
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] 1.2.27 is on GitHub main — verify with `git fetch -q origin main && git log -1 --format=%s origin/main | grep -q 'Foreman 1.2.27'`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] release.py 1.2.27 --push
2. [x] update JARVIS
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `git fetch -q origin main && git log -1 --format=%s origin/main | grep -q 'Foreman 1.2.27'` → exit 0 · (no output) [ran] [tree d587bc0ede02] (2026-10-09T21:45:16Z)
- (step 1) `git fetch -q origin main && git log -1 --format=%s origin/main | grep -q 'Foreman 1.2.27'` → exit 0 · (no output) [ran] [tree d587bc0ede02] (2026-10-09T21:45:16Z)
- (step 2) `git fetch -q origin main && git log -1 --format=%s origin/main | grep -q 'Foreman 1.2.27'` → exit 0 · (no output) [ran] [tree d587bc0ede02] (2026-10-09T21:45:16Z)
- (audit self) `self: release.py's gates passed, pushed, JARVIS plugin updated to 1.2.27` → no findings [tree d587bc0ede02] (2026-10-09T21:45:16Z)
## Log
- 2026-10-09T21:43:11Z created
- 2026-10-09T21:43:13Z focused
- 2026-10-09T21:45:17Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0748 [CLEAN S, done, 2 steps] Release Foreman 1.2.26 (T-0692 to T-0697, T-0746, T-0747) to GitHub main and JARVIS
- T-0745 [CLEAN S, done, 2 steps] Release Foreman 1.2.25 (T-0688 to T-0691) to GitHub main and JARVIS
- T-0407 [FIX S, done, 2 steps] Foreman 1.2.11: step evidence moves the current step (T-0406) to GitHub main and JARVIS
- decision 2026-10-09: [outward] Updating Foreman on JARVIS (merge to main, pull, plugin update, reload) as fixes land during the monitoring
- similar finished tasks took 2–2 steps
- start here (files T-0748 touched): .claude-plugin/marketplace.json, CHANGELOG.md, plugin/.claude-plugin/plugin.json
## Behaviour lock
release.py ran fm check (full suite, doctor, roundtrip, hook bench) on the release tree before tagging; the release changes only version strings and the changelog heading
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
