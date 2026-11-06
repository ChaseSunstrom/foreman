---
id: T-3063
type: SECURITY
tier: M
status: planned
priority: low
scope: []
depends_on: []
source: genesis-review
created: 2026-11-05T00:31:10Z
updated: 2026-11-06T03:52:57Z
trigger: genesis-review
trigger_key: 36f91b6c445d6c61
---
# Browser steering on the live page (POST /api/act: drive, checkpoint, pause, notes) is proven safe: an origin and token check that holds against a forwarded port and a cross-site page, and an exam line for each act
## Raw request
> FIX: cross-cutting review gen-4 #7 (what grew without earning it): 1,704 lines of browser steering (drive, checkpoint, pause, notes via POST /api/act) landed with a hand-rolled CSRF wall and a stated hole (port forwards read as your uid) while no exam line measures it. [plugin/web/live/live.js]
> genesis-review 4:7
> (Filed at low priority: trigger genesis-review has precision 0.10 over its last 20 closed captures; fm triggers shows the record.)
## Interpretation
Reading 1 (chosen): gen-4's review: 1,704 lines of browser steering landed with a hand-rolled CSRF wall and a stated hole (a forwarded port reads as the user's uid) and no exam line measures it; prove each act needs the page's per-session token and a same-origin request, refuse a request through a forwarded port or another site's page, and add tests that attack each. Reading 2: remove browser steering; rejected, the user steers from the live page and the acts are small.
## Assumptions (confidence)
## Acceptance criteria
- [ ] POST /api/act refuses a request without the page's token, with a stale token, from another Origin, or with a Host other than the loopback address it is bound to; the page's own acts still work — verify with `python3 plugin/tests/run.py test_live`
- [ ] each act (drive, checkpoint, pause, note) has a test that an attacker's request is refused and the user's succeeds — verify with `python3 plugin/tests/run.py test_live`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: live.py's act route and its current token; add an Origin and Host check against the bound loopback address, a token bound to the page load, and attack tests (cross-site form post, a request with a forwarded Host, no token, a stale token); likely outcome: each attack refused, the page's own acts still work. 2. Do less: document the hole; fails if: a forwarded port lets anything on the network pause or steer the drive. 3. Move acts to the CLI only; fails if: the user loses steering from the page. Choice 1 (80%)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing attack tests  <- CURRENT
2. [ ] the origin, host and token checks
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T00:31:10Z created
- 2026-11-05T04:42:41Z planned from capture
- 2026-11-05T04:42:42Z set approved=True
- 2026-11-05T04:42:42Z blocked: approved; waits for a builder slot
- 2026-11-06T03:52:57Z unblocked
## Follow-ups captured
