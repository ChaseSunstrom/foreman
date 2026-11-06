---
id: T-1218
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T15:28:04Z
updated: 2026-10-16T15:42:56Z
base: 33ea5f472496f95fed462cc1724096cff14ac13d
base_tree: 77844eb5247025fc69899442afb2191cfa636825
plan0_at: 2026-10-16T15:28:05Z
plan0_scope: []
verified: ok
---
# Release Foreman 1.2.35 and push to main so the Pages site publishes
## Raw request
> Release Foreman 1.2.35 and push to main so the Pages site publishes
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm release 1.2.35 --ui 0.18.2 --push finishes and origin/main's head is the 'Foreman 1.2.35' merge — verify with `git fetch -q origin main && git log -1 --format=%s origin/main`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm release 1.2.35 --ui 0.18.2 --push
## Resume here
## Docs impact
## Verification evidence
- (step 1) `git fetch -q origin main && git log -1 --format=%s origin/main` → exit 0 · Foreman 1.2.35 [ran] [tree e5492fa89c45] (2026-10-16T15:42:12Z)
- (ac 1) `git fetch -q origin main && git log -1 --format=%s origin/main` → exit 0 · Foreman 1.2.35 [ran] [tree e5492fa89c45] (2026-10-16T15:42:14Z)
- (audit self) `self: origin/main is the Foreman 1.2.35 merge of the gated release commit; the first run stopped at the gate on a load flake, which T-1219 fixed and proved under 16 CPU burners before the resume` → no findings [tree e5492fa89c45] (2026-10-16T15:42:14Z)
## Log
- 2026-10-16T15:28:04Z created
- 2026-10-16T15:28:04Z focused
- 2026-10-16T15:28:19Z user approved publish in Claude Code's permission prompt
- 2026-10-16T15:28:19Z undo point at this yes for publish: HEAD 33ea5f472496
- 2026-10-16T15:32:59Z paused: focus moved to T-1219
- 2026-10-16T15:35:33Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-16T15:35:33Z focused
- 2026-10-16T15:35:40Z waiting: fm release 1.2.35 --resume is rerunning the full gates after the T-1219 flake fix; evidence is its exit and origin/main's head after the push
- 2026-10-16T15:38:23Z publish grant used by fm release --push
- 2026-10-16T15:42:56Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1206 [FEATURE M, done, 3 steps] A GitHub Pages site for Foreman: one modern page with the real demo, the loop, the guard and install — lesson: A marketing page for a d…
- T-1143 [CLEAN S, done, 2 steps] Release Foreman 1.2.32 (foreman-ui 0.18.0) and push to main (the user: 'push to main when you get a chance, and when you're done with eve…
- T-0953 [FEATURE S, done, 1 steps] Release 1.2.30 to GitHub main (user asked to push) — lesson: Run the full suite before release.py when a session changed hook wiring: t…
- decision 2026-10-15: Release as 1.2.28 via release.py --push, not a raw push
- similar finished tasks took 1–3 steps
## Behaviour lock
Nothing changed by this task: it versions and publishes what earlier tasks closed. The lock is the release's own gates on the release commit: fm check (2,114 tests, after T-1219 fixed the load flake) and fm release-check passed before the push merged that exact commit.
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- mods/foreman-ui/.claude-plugin/plugin.json
- plugin/.claude-plugin/plugin.json
