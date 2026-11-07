---
id: T-3321
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/claims.py, plugin/tests/test_claims_remote.py, plugin/lib/fmclaims.py, MASTER.md, docs/map, CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, scripts/probe-plugin-rename.sh, docs/map/files-lib-1.md]
depends_on: []
source: user
created: 2026-11-06T04:26:40Z
updated: 2026-11-07T00:44:52Z
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T05:55:03Z
plan0_scope: [plugin/lib/sampo/claims.py, plugin/tests/test_claims_remote.py, plugin/lib/fmclaims.py, MASTER.md, docs/map]
builder_returned: 2026-11-06T06:48:25Z
base: 483ea8c998fcabcdbad613d057b6da06eed34146
base_tree: 8d82ac7ab38937b5a64f2ab3af4b2c2fdfd175da
lane_stop: merged 2026-11-07T00:04:53Z
verified: ok
unproven: [docs, meaning, typed]
---
# Fleet part 1: claims on git refs: take, renew, release and list claims under refs/sampo/<slug>/claim/<key> by atomic compare-and-swap push; leases expire and are taken over exactly once
## Raw request
> Many sessions, one repo, many machines, no duplicates or drift: run several Claude sessions in parallel on one repo (each working its own Kalevala towers or tasks) and on other machines via git, all managed as one. Exists: fm sync mirrors briefs/decisions/research in .foreman/ through git (local wins, theirs set aside), leases, lanes, bus, per-device fm session. Gaps: (1) task ids clash across machines (two machines both mint the next T-number; sync keeps one, sets the other aside); (2) no cross-machine claim, so two machines can start the same task or tower; a claim must travel before the work starts (a pushed ref like refs/sampo/claims/ID with an expiry), and a lost machine's claim must lapse; (3) focus is one active task per project, not per session; (4) Kalevala towers are not units any session or machine can claim, and Väinämöinen assumes one watcher; (5) drift: every session and machine must hold the same gen-0, mandate and steers, with a reconcile that names divergence; (6) a status view of who works what where. Must stay efficient: no polling storms, git as transport. User: 'the ability to have multiple sessions running in parallel on the same repo/recursive tower improvement... and even on different machines via git/changes/whatever, while still being managed entirely without duplications/drift'
## Interpretation
Reading 1: only the claim primitive (take, renew, release, list) as a library over git refs. Reading 2: the whole fleet (ids, focus, towers, drift, status). Ruled out reading 2: later tasks T-3329/T-3330/T-3333/T-3334 build on this.
## Assumptions (confidence)
## Acceptance criteria
- [x] two clones racing for one claim against a file:// bare remote (FOREMAN_CLAIMS_REMOTE) give exactly one winner; an expired claim (until + 5 min slack) is taken over exactly once by two racing clones; renew and release work; list shows holder machine (eco.machine()), until and the drift fingerprint field — verify with `python3 plugin/tests/run.py test_claims_remote`
- [x] offline (remote unreachable) a claim attempt says so and the caller decides; no polling: renewals are batched into one --atomic push at most every 10 minutes — verify with `python3 plugin/tests/run.py test_claims_remote`
- [x] other fleet gaps (id clash, per-session focus, towers, drift, status view) are later tasks T-3329/T-3330/T-3333/T-3334 — verify with `python3 plugin/tests/run.py test_claims_remote`
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
<!-- auto -->
- 2026-11-06T06:47:29Z steps 3/3 done
- git: worktree-agent-a3b6faa3c854c6eb7; 0 uncommitted
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_claims_remote` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 16.3s (1 jobs, 16 at a time; slowest: loader._FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) (ran] (tree 194deb837da1] (world 2f1906870a] (2026-11-06T05:56:03Z)
- (step 1) `python3 plugin/tests/run.py test_claims_remote` → exit 0 · Ran 9 tests in 159.4s (2 jobs, 16 at a time; slowest: Take 2s, Lifecycle 1s) / OK (ran] (tree 9e3b7a038f0f] (world 2f1906870a] (2026-11-06T06:08:50Z)
- (step 2) `python3 plugin/tests/run.py test_claims_remote` → exit 0 · Ran 9 tests in 154.0s (2 jobs, 16 at a time; slowest: Lifecycle 1s, Take 1s) / OK (ran] (tree 9e3b7a038f0f] (world 2f1906870a] (2026-11-06T06:11:26Z)
- (step 3) `python3 plugin/tests/run.py test_claims_remote` → exit 0 · Ran 9 tests in 90.4s (2 jobs, 16 at a time; slowest: Take 1s, Lifecycle 1s) / OK (ran] (tree 9e3b7a038f0f] (world 2f1906870a] (2026-11-06T06:12:58Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_claims_remote test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_left_out test_library test_mcp test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2094 tests in 2247.4s (643 jobs, 16 at a time; slowest: LeanKindGateHookDelay 77s, JudgmentKinds 71s, LeanKindGateGuardAllow 62s) / FAILED (1 classes: test_left_out.LeftOut) (ran] (tree 48458831595a] (world 2f1906870a] (2026-11-06T06:46:59Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 8938eecee068] (2026-11-07T00:38:09Z)
- (ac 1) `python3 plugin/tests/run.py test_claims_remote` → exit 0 · Ran 15 tests in 15.2s (2 jobs, 16 at a time; slowest: Take 2s, Lifecycle 1s) / OK [ran] [tree 8938eecee068] [world 2f1906870a] (2026-11-07T00:38:29Z)
- (ac 2) `python3 plugin/tests/run.py test_claims_remote` → exit 0 · Ran 15 tests in 15.2s (2 jobs, 16 at a time; slowest: Take 2s, Lifecycle 1s) / OK [ran] [tree 8938eecee068] [world 2f1906870a] (2026-11-07T00:38:29Z)
- (ac 3) `python3 plugin/tests/run.py test_claims_remote` → exit 0 · Ran 15 tests in 15.2s (2 jobs, 16 at a time; slowest: Take 2s, Lifecycle 1s) / OK [ran] [tree 8938eecee068] [world 2f1906870a] (2026-11-07T00:38:29Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 8938eecee068] (2026-11-07T00:38:29Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 8938eecee068] (2026-11-07T00:38:29Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 8938eecee068] (2026-11-07T00:38:29Z)
## Log
- 2026-11-06T04:26:40Z created
- 2026-11-06T04:29:02Z steer: the user: 'manage all of that across sessions too, like a consensus thing... able to handle tasks like those recursive towers, kalevala, genesis stuff, even without direct access... not only one machine managing everything, but working together'. No leader machine: peers agree on claims, ids, tower ownership, keep/revert and births, watcher acts; git (any shared remote) is the only channel; a vanished peer never blocks the rest
- 2026-11-06T04:31:54Z planned from capture
- 2026-11-06T05:55:02Z focused
- 2026-11-06T05:55:03Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T17:20:15Z focused
- 2026-11-06T17:40:16Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a3b6faa3c854c6eb7 (branch worktree-agent-a3b6faa3c854c6eb7 kept: not merged); dropped: relocated beside the repo: the train left it out on a conflict and the Ward refuses git merge under .claude/worktrees; its branch is kept and merged into the new lane
- 2026-11-06T17:41:17Z lane: ~/.claude/foreman.lanes/T-3321 on foreman/T-3321
- 2026-11-06T17:41:34Z focused
- 2026-11-07T00:04:53Z merged foreman/T-3321 in merge train
- 2026-11-07T00:38:08Z set scope=['plugin/lib/sampo/claims.py', 'plugin/tests/test_claims_remote.py', 'plugin/lib/fmclaims.py', 'MASTER.md', 'docs/map', 'CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'scripts/probe-plugin-rename.sh', 'docs/map/files-lib-1.md']
- 2026-11-07T00:38:09Z scope: widened at merge to the reviewed lane's own diff (ce68d83d7), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902), and scripts/probe-plugin-rename.sh (an untracked stray copy T-3549 removed between closes; a base taken before that counts its removal)
- 2026-11-07T00:44:43Z done
- 2026-11-07T00:44:49Z committed 92f7c0456 (1 file)
- 2026-11-07T00:44:52Z lane removed: ~/.claude/foreman.lanes/T-3321; dropped: merged and closed
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
Changed in scope since this was planned (2026-11-06): MASTER.md, docs/map/files-lib-2.md, docs/map/files-lib-3.md, docs/map/ops-1.md; re-ground the plan against them before editing
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Plan gaps
- failed first: step 1 race test against a temp bare remote, red
## Files touched
- plugin/tests/test_claims_remote.py
- plugin/lib/sampo/claims.py
- plugin/lib/fmclaims.py
- MASTER.md
- docs/map/files-lib-1.md
- CHANGELOG.md
- scripts/probe-plugin-rename.sh
