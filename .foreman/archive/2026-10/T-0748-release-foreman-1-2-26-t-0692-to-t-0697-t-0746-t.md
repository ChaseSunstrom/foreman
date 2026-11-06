---
id: T-0748
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T21:14:24Z
updated: 2026-10-09T21:16:16Z
base: 1cba0be7166a1bc31b5174c068ede5970b31864f
base_tree: 7508a4b585842991494f199d7654f2a652246869
verified: ok
---
# Release Foreman 1.2.26 (T-0692 to T-0697, T-0746, T-0747) to GitHub main and JARVIS
## Raw request
> Release Foreman 1.2.26 (T-0692 to T-0697, T-0746, T-0747) to GitHub main and JARVIS
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] 1.2.26 is on GitHub main — verify with `git fetch -q origin main && git log -1 --format=%s origin/main | grep -q 'Foreman 1.2.26'`
- [x] JARVIS runs 1.2.26 — verify with `ssh -o BatchMode=yes <user>@<host> 'grep -q 1.2.26 ~/.claude/foreman/plugin/.claude-plugin/plugin.json'`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] release.py 1.2.26 --push
2. [x] update JARVIS
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `git fetch -q origin main && git log -1 --format=%s origin/main | grep -q 'Foreman 1.2.26'` → exit 0 · (no output) [ran] [tree 55fc0c8653bc] (2026-10-09T21:16:16Z)
- (ac 2) `ssh -o BatchMode=yes <user>@<host> 'grep -q 1.2.26 ~/.claude/foreman/plugin/.claude-plugin/plugin.json'` → exit 0 · (no output) [ran] [tree 55fc0c8653bc] (2026-10-09T21:16:16Z)
- (step 1) `git fetch -q origin main && git log -1 --format=%s origin/main | grep -q 'Foreman 1.2.26'` → exit 0 · (no output) [ran] [tree 55fc0c8653bc] (2026-10-09T21:16:16Z)
- (step 2) `git fetch -q origin main && git log -1 --format=%s origin/main | grep -q 'Foreman 1.2.26'` → exit 0 · (no output) [ran] [tree 55fc0c8653bc] (2026-10-09T21:16:16Z)
- (audit self) `self: release.py's gates passed, pushed, JARVIS plugin updated` → no findings [tree 55fc0c8653bc] (2026-10-09T21:16:16Z)
## Log
- 2026-10-09T21:14:24Z created
- 2026-10-09T21:14:27Z focused
- 2026-10-09T21:16:16Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0745 [CLEAN S, done, 2 steps] Release Foreman 1.2.25 (T-0688 to T-0691) to GitHub main and JARVIS
- T-0407 [FIX S, done, 2 steps] Foreman 1.2.11: step evidence moves the current step (T-0406) to GitHub main and JARVIS
- T-0396 [FIX S, done, 2 steps] Foreman 1.2.6: the merge and pipe-shell refusal hints (T-0394, T-0395) to GitHub main and JARVIS
- decision 2026-10-09: [outward] Updating Foreman on JARVIS (merge to main, pull, plugin update, reload) as fixes land during the monitoring
- similar finished tasks took 2–2 steps
- start here (files T-0745 touched): .claude-plugin/marketplace.json, CHANGELOG.md, plugin/.claude-plugin/plugin.json
## Behaviour lock
release.py ran fm check (full suite, doctor, roundtrip, hook bench) on the release tree before tagging; the release changes only version strings and the changelog heading
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
