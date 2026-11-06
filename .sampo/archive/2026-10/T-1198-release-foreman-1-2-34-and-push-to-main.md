---
id: T-1198
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T13:55:45Z
updated: 2026-10-16T14:11:12Z
base: b8fa1cb1f783337bfe2243b5ccaac3b3e291959b
base_tree: 980ae68ee3165b77312049dd061b7a62f1a8550b
plan0_at: 2026-10-16T13:55:45Z
plan0_scope: []
verified: ok
---
# Release Foreman 1.2.34 and push to main
## Raw request
> Release Foreman 1.2.34 and push to main
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm release 1.2.34 --push finishes every step and origin/main's head is the 'Foreman 1.2.34' merge — verify with `git fetch -q origin main && git log -1 --format=%s origin/main`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm release 1.2.34 --push
## Resume here
## Docs impact
## Verification evidence
- (step 1) `git fetch -q origin main && git log -1 --format=%s origin/main && git merge-base --is-ancestor d0b47da0 origin/main && echo release-commit-on-main` → exit 0 · Foreman 1.2.34 / release-commit-on-main [ran] [tree 8929dc664b7e] (2026-10-16T14:09:46Z)
- (ac 1) `git fetch -q origin main && git log -1 --format=%s origin/main` → exit 0 · Foreman 1.2.34 [ran] [tree 8929dc664b7e] (2026-10-16T14:10:00Z)
- `git fetch -q origin main && git log -1 --format=%s origin/main && git merge-base --is-ancestor d0b47da0 origin/main && echo release-commit-on-main` → exit 0 · Foreman 1.2.34 / release-commit-on-main [ran] [tree 8929dc664b7e] (2026-10-16T14:10:00Z)
- (audit self) `self: origin/main head is the 'Foreman 1.2.34' merge of the gated release commit d0b47da0; the publish grant was spent by the push; T-1199 (committed after the release commit) is not in the push, as intended` → no findings [tree 8929dc664b7e] (2026-10-16T14:10:00Z)
## Log
- 2026-10-16T13:55:45Z created
- 2026-10-16T13:55:45Z focused
- 2026-10-16T13:55:56Z user approved publish in Claude Code's permission prompt
- 2026-10-16T13:55:56Z undo point at this yes for publish: HEAD b8fa1cb1f783
- 2026-10-16T13:58:58Z waiting: fm release 1.2.34 --push is running the full gates (started ~3 min ago under load ~25); evidence is its exit and origin/main's head after it ends
- 2026-10-16T14:05:08Z paused: focus moved to T-1199
- 2026-10-16T14:09:12Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-16T14:09:12Z focused
- 2026-10-16T14:09:18Z publish grant used by fm release --push
- 2026-10-16T14:11:12Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1143 [CLEAN S, done, 2 steps] Release Foreman 1.2.32 (foreman-ui 0.18.0) and push to main (the user: 'push to main when you get a chance, and when you're done with eve…
- T-0953 [FEATURE S, done, 1 steps] Release 1.2.30 to GitHub main (user asked to push) — lesson: Run the full suite before release.py when a session changed hook wiring: t…
- T-1091 [CLEAN S, done, 2 steps] Release Foreman 1.2.31 and push to main (the user: push to main when you get a chance)
- decision 2026-10-15: Release as 1.2.28 via release.py --push, not a raw push
- similar finished tasks took 1–2 steps
## Behaviour lock
No behaviour changed by this task: it versions and publishes what earlier tasks closed. The lock is the release's own gates on the release commit d0b47da0: fm check (full suite) passed at step 2 and fm release-check (doctor and demo in a temporary HOME) at step 6, both recorded done in release.json before the push merged that exact sha.
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
- plugin/lib/fmrelease.py
- plugin/tests/test_release.py
