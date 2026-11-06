---
id: T-3321
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/claims.py, plugin/tests/test_claims_remote.py, plugin/lib/fmclaims.py, MASTER.md, docs/map]
depends_on: []
source: user
created: 2026-11-06T04:26:40Z
updated: 2026-11-06T06:12:58Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a3b6faa3c854c6eb7
lane_branch: worktree-agent-a3b6faa3c854c6eb7
base: 0e503eeeeb87000325d02673ba119e35ff08b7e8
base_tree: 5c2bb7b2f14ef72b4659b9d747b61d1c44bc9aca
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T05:55:03Z
plan0_scope: [plugin/lib/sampo/claims.py, plugin/tests/test_claims_remote.py, plugin/lib/fmclaims.py, MASTER.md, docs/map]
builder_returned: 2026-11-06T06:10:19Z
---
# Fleet part 1: claims on git refs: take, renew, release and list claims under refs/sampo/<slug>/claim/<key> by atomic compare-and-swap push; leases expire and are taken over exactly once
## Raw request
> Many sessions, one repo, many machines, no duplicates or drift: run several Claude sessions in parallel on one repo (each working its own Kalevala towers or tasks) and on other machines via git, all managed as one. Exists: fm sync mirrors briefs/decisions/research in .foreman/ through git (local wins, theirs set aside), leases, lanes, bus, per-device fm session. Gaps: (1) task ids clash across machines (two machines both mint the next T-number; sync keeps one, sets the other aside); (2) no cross-machine claim, so two machines can start the same task or tower; a claim must travel before the work starts (a pushed ref like refs/sampo/claims/ID with an expiry), and a lost machine's claim must lapse; (3) focus is one active task per project, not per session; (4) Kalevala towers are not units any session or machine can claim, and Väinämöinen assumes one watcher; (5) drift: every session and machine must hold the same gen-0, mandate and steers, with a reconcile that names divergence; (6) a status view of who works what where. Must stay efficient: no polling storms, git as transport. User: 'the ability to have multiple sessions running in parallel on the same repo/recursive tower improvement... and even on different machines via git/changes/whatever, while still being managed entirely without duplications/drift'
## Interpretation
Reading 1: only the claim primitive (take, renew, release, list) as a library over git refs. Reading 2: the whole fleet (ids, focus, towers, drift, status). Ruled out reading 2: later tasks T-3329/T-3330/T-3333/T-3334 build on this.
## Assumptions (confidence)
## Acceptance criteria
- [ ] two clones racing for one claim against a file:// bare remote (FOREMAN_CLAIMS_REMOTE) give exactly one winner; an expired claim (until + 5 min slack) is taken over exactly once by two racing clones; renew and release work; list shows holder machine (eco.machine()), until and the drift fingerprint field — verify with `python3 plugin/tests/run.py test_claims_remote`
- [ ] offline (remote unreachable) a claim attempt says so and the caller decides; no polling: renewals are batched into one --atomic push at most every 10 minutes — verify with `python3 plugin/tests/run.py test_claims_remote`
- [ ] other fleet gaps (id clash, per-session focus, towers, drift, status view) are later tasks T-3329/T-3330/T-3333/T-3334 — verify with `python3 plugin/tests/run.py test_claims_remote`
## Non-goals
Exists: fm sync mirrors briefs/decisions/research in .foreman/ through git (unchanged here); sync keeps one, sets the other aside (unchanged); ids clashing across machines, per-session focus, tower ownership, drift reconcile, status view: later tasks T-3329/T-3330/T-3333/T-3334. No polling storms beyond batched renewal.
## Approach (options → choice → why)
1) CAS on git refs (push --atomic --force-with-lease): one winner by the remote, works over any git remote; fails if the remote is unreachable (then take returns offline). 2) claims in the .foreman mirror: races show later as merge conflicts; likely outcome: duplicates. 3) a coordinator in sampo serve: a leader needing network reach; fails if it is down. 4) use what exists: fm sync and leases are local or merge-based; likely outcome: they cannot arbitrate a race. 5) do less: no claims, accept duplicate work; fails if the user wants no duplicates. Choice 1 (80%): the remote arbitrates exactly one winner.
## Risks and rollback
Blast radius (sampo graph blast): co-changes CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmexam.py; past FIXes T-1817, T-1828, T-1839, T-1865, T-1886.
## Execution prompt
## Steps
1. [x] race test against a temp bare remote, red
2. [x] claims.py: empty-tree commit with JSON body, push --atomic --force-with-lease
3. [x] expiry, takeover, renew batching, list
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_claims_remote` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 16.3s (1 jobs, 16 at a time; slowest: loader._FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) [ran] [tree 194deb837da1] [world 2f1906870a] (2026-11-06T05:56:03Z)
- (step 1) `python3 plugin/tests/run.py test_claims_remote` → exit 0 · Ran 9 tests in 159.4s (2 jobs, 16 at a time; slowest: Take 2s, Lifecycle 1s) / OK [ran] [tree 9e3b7a038f0f] [world 2f1906870a] (2026-11-06T06:08:50Z)
- (step 2) `python3 plugin/tests/run.py test_claims_remote` → exit 0 · Ran 9 tests in 154.0s (2 jobs, 16 at a time; slowest: Lifecycle 1s, Take 1s) / OK [ran] [tree 9e3b7a038f0f] [world 2f1906870a] (2026-11-06T06:11:26Z)
- (step 3) `python3 plugin/tests/run.py test_claims_remote` → exit 0 · Ran 9 tests in 90.4s (2 jobs, 16 at a time; slowest: Take 1s, Lifecycle 1s) / OK [ran] [tree 9e3b7a038f0f] [world 2f1906870a] (2026-11-06T06:12:58Z)
## Log
- 2026-11-06T04:26:40Z created
- 2026-11-06T04:29:02Z steer: the user: 'manage all of that across sessions too, like a consensus thing... able to handle tasks like those recursive towers, kalevala, genesis stuff, even without direct access... not only one machine managing everything, but working together'. No leader machine: peers agree on claims, ids, tower ownership, keep/revert and births, watcher acts; git (any shared remote) is the only channel; a vanished peer never blocks the rest
- 2026-11-06T04:31:54Z planned from capture
- 2026-11-06T05:55:02Z focused
- 2026-11-06T05:55:03Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3050 [FEATURE L, blocked, 6 steps] Kalevala: many Rune towers at once on every aspect of Sampo, overseen by Väinämöinen, and evolving its own setup
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- decision 2026-11-02: [costly] [reverses: queued and starts automatically once gen-0's DONE-WHEN holds] [cites: user steer 2026-11-02: Honestly integrate MOOMSHOT into ea…
- similar past tasks were L: consider --tier L
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_ambient.py, plugin/tests/test_board_export.py, plugin/tests/test_bookkeeping.py, plugin/tests/test_bus.py, plugin/tests/test_code.py, plug…
## Preflight
Changed in scope since this was planned (2026-11-06): docs/map/ops-1.md; re-ground the plan against them before editing
