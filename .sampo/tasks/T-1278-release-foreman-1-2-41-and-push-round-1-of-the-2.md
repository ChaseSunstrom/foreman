---
id: T-1278
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-20T16:39:12Z
updated: 2026-10-20T16:58:07Z
base: 59bc96796cd5c2783b667e748761041910976785
base_tree: 1017b703b5affee1713a1a350bd06ef71cfee1b0
plan0_at: 2026-10-20T16:39:13Z
plan0_scope: []
verified: strong
---
# Release Foreman 1.2.41 and push (round 1 of the 2026-10-20 brainstorm, worker hardening, CI fix)
## Raw request
> Release Foreman 1.2.41 and push (round 1 of the 2026-10-20 brainstorm, worker hardening, CI fix)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] 1.2.41 on origin/main — verify with `git fetch -q origin && test "$(git log origin/main -1 --format=%s)" = 'Foreman 1.2.41'`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm release 1.2.41 --push (gates, version, changelog, tag, push)
## Resume here
## Docs impact
none: the release itself updated plugin.json, the marketplace entries and CHANGELOG's heading
## Verification evidence
- (ac 1) `git fetch -q origin && test "$(git log origin/main -1 --format=%s)" = 'Foreman 1.2.41'` → exit 0 · (no output) [ran] [tree c999e06fded0] (2026-10-20T16:56:03Z)
- (step 1) `git fetch -q origin && test "$(git log origin/main -1 --format=%s)" = 'Foreman 1.2.41'` → exit 0 · (no output) [ran] [tree c999e06fded0] (2026-10-20T16:56:03Z)
- (audit intent) `release gates (fm check, release-check) ran inside fm release; origin/main's head is the release commit` → the user asked to push to main as work lands and said releases need no sign-off; 1.2.41 carries round 1, the worker hardening and the CI fix [tree c999e06fded0] (2026-10-20T16:56:03Z)
- (audit self) `release gates (fm check, release-check) ran inside fm release; origin/main's head is the release commit` → no findings [tree c999e06fded0] (2026-10-20T16:56:03Z)
- `git fetch -q origin && test "$(git log origin/main -1 --format=%s)" = 'Foreman 1.2.41'` → exit 0 · (no output) [ran] [tree c999e06fded0] (2026-10-20T16:57:16Z)
- (audit intent) `release gates (fm check, release-check) ran inside fm release; origin/main's head is the release commit` → the user asked to push to main as work lands and said releases need no sign-off; 1.2.41 carries round 1, the worker hardening and the CI fix [tree c999e06fded0] (2026-10-20T16:57:16Z)
- (audit self) `release gates (fm check, release-check) ran inside fm release; origin/main's head is the release commit` → no findings [tree c999e06fded0] (2026-10-20T16:57:16Z)
## Log
- 2026-10-20T16:39:12Z created
- 2026-10-20T16:39:13Z focused
- 2026-10-20T16:48:56Z user approved publish in Claude Code's permission prompt
- 2026-10-20T16:48:56Z undo point at this yes for publish: HEAD 59bc96796cd5
- 2026-10-20T16:52:45Z publish grant used by fm release --push
- 2026-10-20T16:58:07Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1143 [CLEAN S, done, 2 steps] Release Foreman 1.2.32 (foreman-ui 0.18.0) and push to main (the user: 'push to main when you get a chance, and when you're done with eve…
- T-1243 [CLEAN S, done, 1 steps] Release 1.2.38 and push: Benchmarks page fixes
- T-0953 [FEATURE S, done, 1 steps] Release 1.2.30 to GitHub main (user asked to push) — lesson: Run the full suite before release.py when a session changed hook wiring: t…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
- similar finished tasks took 1–2 steps
## Behaviour lock
none: a release changes no behaviour; fm release ran the full gates (fm check, release-check) before its commit
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
