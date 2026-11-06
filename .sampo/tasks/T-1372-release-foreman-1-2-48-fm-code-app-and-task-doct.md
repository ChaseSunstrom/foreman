---
id: T-1372
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T13:37:22Z
updated: 2026-10-21T16:31:37Z
base: 070e9e9fe5acf0de52c8c8b1bf029b84f870192b
base_tree: 4d0bf8b785b36301e92ba6c3e62e2a276aa63ed9
plan0_at: 2026-10-21T13:37:23Z
plan0_scope: []
verified: strong
---
# Release Foreman 1.2.48 (fm code app and --task, doctor fm link, --events replay, task --from fix)
## Raw request
> Release Foreman 1.2.48 (fm code app and --task, doctor fm link, --events replay, task --from fix)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] Foreman 1.2.48 is released and pushed to origin's main — verify with `git log origin/main -1 --format=%s | grep -q 'Foreman 1.2.48'`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm release 1.2.48 --push
## Resume here
<!-- auto -->
- 2026-10-21T13:47:37Z step 1/1: fm release 1.2.48 --push
- git: foreman/build; 0 uncommitted
- failures met: failed (0 classes); posttoolusefailure 0.0 0.0 0 [0] over budget
## Docs impact
## Verification evidence
- (step 1) `git log origin/main -1 --format=%s | grep 'Foreman 1.2.48'` → exit 0 · Foreman 1.2.48 [ran] [tree fd55e9e77d93] (2026-10-21T16:28:20Z)
- (ac 1) `git log origin/main -1 --format=%s | grep -q 'Foreman 1.2.48'` → exit 0 · (no output) [ran] [tree fd55e9e77d93] (2026-10-21T16:28:21Z)
- (audit intent) `self: fm release 1.2.48 --push passed every gate on the third try (the first two stopped on load-sensitive flakes, captured as T-1378 and T-1379), committed, merged into origin main and pushed; canary detached` → released and pushed; origin/main's head is Foreman 1.2.48 [tree fd55e9e77d93] (2026-10-21T16:28:21Z)
- (audit self) `self: fm release 1.2.48 --push passed every gate on the third try (the first two stopped on load-sensitive flakes, captured as T-1378 and T-1379), committed, merged into origin main and pushed; canary detached` → no findings [tree fd55e9e77d93] (2026-10-21T16:28:21Z)
## Log
- 2026-10-21T13:37:22Z created
- 2026-10-21T13:37:22Z focused
- 2026-10-21T13:37:26Z guard authorization added: publish
- 2026-10-21T13:39:41Z step 1 evidence waits on the running release (fm release 1.2.48 --push, background job, at step 2/9 check); recorded when it lands
- 2026-10-21T13:47:37Z release check stopped at step 2 on the known flaky test_hooks NoTaskGate test (load ~30 with two builders running); cause read and captured as T-1378; resume (fm release 1.2.48 --resume) when the builders finish
- 2026-10-21T13:47:38Z paused: focus moved to T-1354
- 2026-10-21T15:26:42Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-21T15:26:42Z focused
- 2026-10-21T15:35:06Z attempt 2 stopped at check on known flakes test_breaker (Breaker three failures) and test_scout (fm scout dry run), both pass alone; load ~40 from the background full gates T-1354's finish started. Attempt 3 waits for that check (pid 517317) to end, then resumes
- 2026-10-21T16:28:08Z publish grant used by fm release --push
- 2026-10-21T16:31:37Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1321 [FEATURE S, done, 1 steps] Release 1.2.46: fm code takes any request, real examples on the site, linked state folders
- research mission-20261020-222446: Request: super improve fm code, make it genuinely amazing: launch it as an app like claude (fm code with no request), able to manage AN…
- research mission-20261020-222446.pack: super improve fm code, make it genuinely amazing: launch it as an app like claude (fm code with no request), able to manage ANY CL…
- decision 2026-10-21: T-1330 approved by self-critique (full autonomy): the app is views inside fm code tui's existing App; --task works a planned brief with a per-task l…
- the similar finished task took 1 steps
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
