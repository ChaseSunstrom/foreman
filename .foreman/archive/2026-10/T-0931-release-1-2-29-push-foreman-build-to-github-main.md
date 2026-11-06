---
id: T-0931
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T19:50:43Z
updated: 2026-10-15T19:53:11Z
base: 31d11710e524fe552115cb4e80d5315bae47ebbb
base_tree: 47a1f37804d819a69907f3d5638ce2804edde89b
verified: ok
---
# Release 1.2.29: push foreman/build to GitHub main (user said yes)
## Raw request
> Release 1.2.29: push foreman/build to GitHub main (user said yes)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] origin/main's tree equals HEAD as Foreman 1.2.29 — verify with `git fetch -q origin && git diff --quiet origin/main HEAD && git log -1 --format=%s origin/main`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] release.py 1.2.29 --push
## Resume here
## Docs impact
## Verification evidence
- (step 1) `git fetch -q origin && git diff --quiet origin/main HEAD && git log -1 --format=%s origin/main` → exit 0 · Foreman 1.2.29 [ran] [tree e27dd44b95fc] (2026-10-15T19:53:08Z)
- (ac 1) `git fetch -q origin && git diff --quiet origin/main HEAD && git log -1 --format=%s origin/main` → exit 0 · Foreman 1.2.29 [ran] [tree e27dd44b95fc] (2026-10-15T19:53:11Z)
- (audit self) `self: release.py bumped 1.2.28 → 1.2.29, fm check green inside it, --no-ff merge pushed; origin/main tree equals HEAD; outgoing diff had no home paths, names or e-mail` → no findings [tree e27dd44b95fc] (2026-10-15T19:53:11Z)
## Log
- 2026-10-15T19:50:43Z created
- 2026-10-15T19:50:43Z focused
- 2026-10-15T19:53:11Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0352 [FEATURE M, blocked, 3 steps] Publish Foreman Desktop on GitHub with CI and release pipelines
- T-0905 [FEATURE S, done, 1 steps] Release 1.2.28: push foreman/build to GitHub main (user asked)
- T-0388 [FIX S, done, 3 steps] Foreman 1.2.5: push 1.2.4 + fm relate, running-code check, fm status to GitHub main; fast-forward JARVIS
- decision 2026-09-26: Released: fast-forwarded main 924fe06 → bd86fd6 (43 commits: T-0018 rounds 1-10, T-0036, T-0038, T-0039) and pushed main + foreman/build to origin
- similar finished tasks took 1–3 steps
- start here (files T-0905 touched): .claude-plugin/marketplace.json, CHANGELOG.md, plugin/.claude-plugin/plugin.json
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
