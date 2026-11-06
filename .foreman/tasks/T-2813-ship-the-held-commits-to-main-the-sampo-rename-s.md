---
id: T-2813
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-03T16:09:22Z
updated: 2026-11-03T20:54:26Z
base: 5872d04f2fac5d63aaa1e77365b71ed6b180d995
base_tree: f2da5f2502e13a2d0b971402bc857ebb09b22530
predict_minutes: 1
predict_attempts: 1
plan0_at: 2026-11-03T20:41:22Z
plan0_scope: []
verified: strong
---
# Ship the held commits to main: the Sampo rename steps 4-5, the closes and fixes landed on foreman/build since the last push (user: 'feel free to push to main at any time')
## Raw request
> Ship the held commits to main: the Sampo rename steps 4-5, the closes and fixes landed on foreman/build since the last push (user: 'feel free to push to main at any time')
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] origin/main has every landed commit (fm ship --check exits 0) — verify with `fm ship --check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm ship after the full gate is green
## Resume here
## Docs impact
none: a ship
## Verification evidence
- (ac 1) `fm ship --check` → exit 0 · nothing to ship: origin main already has HEAD's changes after the last shipped commit 5872d04f [ran] [tree f2da5f2502e1] [world 2f1906870a] (2026-11-03T20:54:24Z)
- (step 1) `fm ship --check` → exit 0 · nothing to ship: origin main already has HEAD's changes after the last shipped commit 5872d04f [ran] [tree f2da5f2502e1] [world 2f1906870a] (2026-11-03T20:54:24Z)
- (audit intent) `self: fm ship ran the full gates (6 of 6 on this exact tree) and pushed 6 commits to origin main at bc543b55 under the T-2813 publish grant; CI for 55ee23fd was green` → the user's standing 'push to main any time' is honoured; nothing landed is left local [tree f2da5f2502e1] (2026-11-03T20:54:24Z)
- (audit edge) `self: fm ship ran the full gates (6 of 6 on this exact tree) and pushed 6 commits to origin main at bc543b55 under the T-2813 publish grant; CI for 55ee23fd was green` → the commit held for T-2742 stays on foreman/build only where fm ship holds it [tree f2da5f2502e1] (2026-11-03T20:54:24Z)
- (audit adversary) `self: fm ship ran the full gates (6 of 6 on this exact tree) and pushed 6 commits to origin main at bc543b55 under the T-2813 publish grant; CI for 55ee23fd was green` → pushed only through fm ship with a spent single-use grant; no force push [tree f2da5f2502e1] (2026-11-03T20:54:24Z)
- (audit self) `self: fm ship ran the full gates (6 of 6 on this exact tree) and pushed 6 commits to origin main at bc543b55 under the T-2813 publish grant; CI for 55ee23fd was green` → no findings [tree f2da5f2502e1] (2026-11-03T20:54:24Z)
## Log
- 2026-11-03T16:09:22Z created
- 2026-11-03T16:09:25Z guard authorization added: publish
- 2026-11-03T16:41:09Z publish grant used by fm ship
- 2026-11-03T16:41:16Z guard authorization added: publish
- 2026-11-03T17:06:58Z guard authorization added: publish
- 2026-11-03T20:02:18Z guard authorization added: publish
- 2026-11-03T20:09:56Z publish grant used by fm ship
- 2026-11-03T20:41:21Z focused
- 2026-11-03T20:41:22Z predicted from its closes: 1 min, 1 attempt(s)
- 2026-11-03T20:46:46Z guard authorization added: publish
- 2026-11-03T20:54:11Z publish grant used by fm ship
- 2026-11-03T20:54:26Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-2527 [FEATURE M, done, 2 steps] fm ci-watch --last-ship watches the main commit the newest fm ship pushed — lesson: a falsy test on an optional CLI value turns a faile…
- decision 2026-10-30: [revisited: feel free to push to main] [cites: user steer 2026-10-29: push to main without asking] [check: python3 plugin/tests/run.py test_ship.Shi…
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
