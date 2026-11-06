---
id: T-1238
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T19:21:58Z
updated: 2026-10-16T19:38:17Z
base: ae7654a9fb07c27e1c0afe7c509d652811f2b410
base_tree: cb561f105f941c6d1e42463f2e1efd3565f5a39a
plan0_at: 2026-10-16T19:21:59Z
plan0_scope: []
verified: ok
---
# Release 1.2.37: guard credential reads, approval binding, fm code, cheaper Foreman turns, neutral benchmark suites and the Benchmarks page
## Raw request
> Release 1.2.37: guard credential reads, approval binding, fm code, cheaper Foreman turns, neutral benchmark suites and the Benchmarks page
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] 1.2.37 is on origin's main and the Pages deploy serves the Benchmarks page — verify with `git ls-remote origin main`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm release 1.2.37 --push
## Resume here
## Docs impact
## Verification evidence
- (step 1) `fm release 1.2.37 --push` → Foreman 1.2.37 released: pushed; origin main at ee620f4d; canary: 3 other projects report their own failing checks [tree 37a7c412ced0] (2026-10-16T19:37:28Z)
- (ac 1) `git ls-remote origin main` → exit 0 · ee620f4d161409a1f8252c9363161ccf55506660	refs/heads/main [ran] [tree 37a7c412ced0] (2026-10-16T19:37:30Z)
- (audit self) `self: release ritual ran all 9 steps (gates, release-check, push under the publish grant, round tag, canary)` → no findings [tree 37a7c412ced0] (2026-10-16T19:37:30Z)
## Log
- 2026-10-16T19:21:58Z created
- 2026-10-16T19:21:59Z focused
- 2026-10-16T19:24:41Z user approved publish in Claude Code's permission prompt
- 2026-10-16T19:24:41Z undo point at this yes for publish: HEAD ae7654a9fb07
- 2026-10-16T19:25:11Z publish grant used by fm release --push
- 2026-10-16T19:38:17Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1220 [FEATURE L, planned, 3 steps] Feature pages for the site: one page per Foreman capability, each with real graphs from Foreman's own history
- T-1232 [FEATURE M, done, 3 steps] Spec suite: a neutral toy repo of fully specified tasks with hidden tests, for fm bench duel — lesson: A benchmark's hidden tests must …
- T-0702 [FEATURE M, dropped, 3 steps] Frontier 02 — Context firewall and cheap reader
- decision 2026-10-16: T-1231 L plan approval under standard autonomy: the user's explicit request ('I want foreman to be better than CC though, and cheaper/faster') is th…
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
