---
id: T-0727
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T17:22:16Z
updated: 2026-10-09T17:27:08Z
base: 056b373937dd1a38101c867e4a90771428b1f8a0
base_tree: 5fc14ccb16bd71e12f7fe9c08992ace6188ed77a
verified: strong
---
# Release 1.2.18: JARVIS at fix, pause holds every launcher, close-out friction, observability and performance milestones
## Raw request
> Release 1.2.18: JARVIS at fix, pause holds every launcher, close-out friction, observability and performance milestones
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] gates pass on the release tree — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] bump versions and changelog, gates, push to GitHub main, update JARVIS
## Resume here
<!-- auto -->
- 2026-10-09T17:24:07Z steps 1/1 done
- git: foreman/build; 3 uncommitted: .claude-plugin/marketplace.json, CHANGELOG.md, plugin/.claude-plugin/plugin.json
- touched since last checkpoint: .claude-plugin/marketplace.json, CHANGELOG.md, plugin/.claude-plugin/plugin.json
## Docs impact
## Verification evidence
- (step 1) `fm check` → exit 0 · ✓ python3 plugin/tests/run.py → exit 0 · Ran 1082 tests in 54.3s (279 classes, 16 at a time; slowest: Stop 42s, TaskLifecycle 26s, Bench 24s) / OK (54.3 s) / ✓ fm replay → exit 0 · 0 newly allowed (po [ran] [tree 6df5259f73c3] (2026-10-09T17:23:54Z)
- (step 1) `fm check` → exit 0 · ✓ python3 plugin/tests/run.py → exit 0 · Ran 1083 tests in 53.4s (279 classes, 16 at a time; slowest: Stop 43s, TaskLifecycle 28s, Bench 26s) / OK (53.4 s) / ✓ fm replay → exit 0 · skipped: nothing un [ran] [tree 303c3f375c6c] (2026-10-09T17:27:07Z)
- (ac 1) `fm check` → exit 0 · ✓ all 6 gates passed on this exact tree already (run at 17:27 UTC); cached (fm check --fresh reruns) [ran] [tree 303c3f375c6c] (2026-10-09T17:27:07Z)
- (audit operator) `self: version bump in plugin.json and both marketplace entries, changelog heading in the 1.2.17 layout; full gates passed on this tree` → JARVIS picks it up with git pull in its folder marketplace, marketplace update and plugin update [tree 303c3f375c6c] (2026-10-09T17:27:07Z)
- (audit self) `self: version bump in plugin.json and both marketplace entries, changelog heading in the 1.2.17 layout; full gates passed on this tree` → no findings [tree 303c3f375c6c] (2026-10-09T17:27:07Z)
## Log
- 2026-10-09T17:22:16Z created
- 2026-10-09T17:22:17Z focused
- 2026-10-09T17:24:07Z paused: focus moved to T-0728
- 2026-10-09T17:25:14Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-09T17:25:14Z focused
- 2026-10-09T17:25:18Z paused: focus moved to T-0728
- 2026-10-09T17:25:43Z focused
- 2026-10-09T17:27:07Z done
- 2026-10-09T17:27:08Z committed 6933ae7 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0436 [SECURITY M, done, 3 steps] fm pause: one flag stops everything Foreman runs unattended — lesson: a kill switch is one flag every launcher checks at its own entry…
- T-0591 [SECURITY S, done, 3 steps] Fm pause gaps: fm session start, fm ideas, fm research ask, fm bench and the fmrelate spaw
- T-0678 [FEATURE M, planned, 2 steps] Milestone: Features — Releases and delivery
- decision 2026-10-04: Friction pass deferred to the next day
- similar finished tasks took 3–3 steps
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
- plugin/lib/fmrecall.py
- plugin/tests/test_trust.py
