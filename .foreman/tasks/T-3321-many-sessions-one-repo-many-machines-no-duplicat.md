---
id: T-3321
type: FEATURE
tier: M
status: planned
priority: normal
scope: [plugin/lib/sampo/claims.py, plugin/tests/test_claims_remote.py, plugin/lib/fmclaims.py, MASTER.md, docs/map]
depends_on: []
source: user
created: 2026-11-06T04:26:40Z
updated: 2026-11-06T04:31:54Z
---
# Fleet part 1: claims on git refs: take, renew, release and list claims under refs/sampo/<slug>/claim/<key> by atomic compare-and-swap push; leases expire and are taken over exactly once
## Raw request
> Many sessions, one repo, many machines, no duplicates or drift: run several Claude sessions in parallel on one repo (each working its own Kalevala towers or tasks) and on other machines via git, all managed as one. Exists: fm sync mirrors briefs/decisions/research in .foreman/ through git (local wins, theirs set aside), leases, lanes, bus, per-device fm session. Gaps: (1) task ids clash across machines (two machines both mint the next T-number; sync keeps one, sets the other aside); (2) no cross-machine claim, so two machines can start the same task or tower; a claim must travel before the work starts (a pushed ref like refs/sampo/claims/ID with an expiry), and a lost machine's claim must lapse; (3) focus is one active task per project, not per session; (4) Kalevala towers are not units any session or machine can claim, and Väinämöinen assumes one watcher; (5) drift: every session and machine must hold the same gen-0, mandate and steers, with a reconcile that names divergence; (6) a status view of who works what where. Must stay efficient: no polling storms, git as transport. User: 'the ability to have multiple sessions running in parallel on the same repo/recursive tower improvement... and even on different machines via git/changes/whatever, while still being managed entirely without duplications/drift'
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] two clones racing for one claim against a file:// bare remote (FOREMAN_CLAIMS_REMOTE) give exactly one winner; an expired claim (until + 5 min slack) is taken over exactly once by two racing clones; renew and release work; list shows holder machine (eco.machine()), until and the drift fingerprint field — verify with `python3 plugin/tests/run.py test_claims_remote`
- [ ] offline (remote unreachable) a claim attempt says so and the caller decides; no polling: renewals are batched into one --atomic push at most every 10 minutes — verify with `python3 plugin/tests/run.py test_claims_remote`
## Non-goals
## Approach (options → choice → why)
1) CAS on git refs: one winner guaranteed by the remote, no leader, works through any git remote including GitHub over ssh 443. 2) claims in the .foreman mirror: races show only later as merge conflicts. 3) a coordinator in sampo serve: a leader needing network reach. 4) Paxos/Raft between peers: needs direct links the machines may lack. Choice 1 (design: T-3321 plan).
## Risks and rollback
## Execution prompt
## Steps
1. [ ] race test against a temp bare remote, red  <- CURRENT
2. [ ] claims.py: empty-tree commit with JSON body, push --atomic --force-with-lease
3. [ ] expiry, takeover, renew batching, list
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T04:26:40Z created
- 2026-11-06T04:29:02Z steer: the user: 'manage all of that across sessions too, like a consensus thing... able to handle tasks like those recursive towers, kalevala, genesis stuff, even without direct access... not only one machine managing everything, but working together'. No leader machine: peers agree on claims, ids, tower ownership, keep/revert and births, watcher acts; git (any shared remote) is the only channel; a vanished peer never blocks the rest
- 2026-11-06T04:31:54Z planned from capture
## Follow-ups captured
