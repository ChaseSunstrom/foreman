---
id: T-1221
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T15:51:25Z
updated: 2026-10-16T15:58:37Z
base: 1bba1e37898fb0c276e2ca8f39b032563b1448bd
base_tree: 4ce19a767e20d5bd6eea53b3f0604d13a90d51f0
plan0_at: 2026-10-16T15:51:27Z
plan0_scope: []
verified: ok
---
# Release Foreman 1.2.36 so the feature pages deploy
## Raw request
> Release Foreman 1.2.36 so the feature pages deploy
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm release 1.2.36 --push finishes and origin/main's head is the 'Foreman 1.2.36' merge — verify with `git fetch -q origin main && git log -1 --format=%s origin/main`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm release 1.2.36 --push
## Resume here
## Docs impact
## Verification evidence
- (step 1) `git fetch -q origin main && git log -1 --format=%s origin/main && curl -s -o /dev/null -w 'features page %{http_code}' https://chasesunstrom.github.io/foreman/features/guard.html` → exit 0 · Foreman 1.2.36 / features page 200 [ran] [tree dd90fd94618f] (2026-10-16T15:57:45Z)
- (ac 1) `git fetch -q origin main && git log -1 --format=%s origin/main` → exit 0 · Foreman 1.2.36 [ran] [tree dd90fd94618f] (2026-10-16T15:57:47Z)
- (audit self) `self: origin/main is the Foreman 1.2.36 merge; the pages workflow for it succeeded and the landing and feature pages answer 200` → no findings [tree dd90fd94618f] (2026-10-16T15:57:47Z)
## Log
- 2026-10-16T15:51:25Z created
- 2026-10-16T15:51:26Z focused
- 2026-10-16T15:51:46Z user approved publish in Claude Code's permission prompt
- 2026-10-16T15:51:46Z undo point at this yes for publish: HEAD 1bba1e37898f
- 2026-10-16T15:56:25Z publish grant used by fm release --push
- 2026-10-16T15:58:37Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1220 [FEATURE L, planned, 3 steps] Feature pages for the site: one page per Foreman capability, each with real graphs from Foreman's own history
- T-1218 [CLEAN S, done, 1 steps] Release Foreman 1.2.35 and push to main so the Pages site publishes
- T-1206 [FEATURE M, done, 3 steps] A GitHub Pages site for Foreman: one modern page with the real demo, the loop, the guard and install — lesson: A marketing page for a d…
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- similar finished tasks took 1–3 steps
## Behaviour lock
Nothing changed by this task: it versions and publishes what T-1220 and earlier tasks closed; the release's gates (fm check, release-check) passed on the exact release commit before the push, and the Pages workflow deployed it (success on 6e14aa3f).
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
