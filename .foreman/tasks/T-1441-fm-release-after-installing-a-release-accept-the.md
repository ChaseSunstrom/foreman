---
id: T-1441
type: SECURITY
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T22:33:06Z
updated: 2026-10-21T23:21:06Z
base: d4aa947b10d4dcd0bbf8fa003c2afa500462c934
base_tree: a85c83409adf8c3eb7142abd577058ef1dd555cf
plan0_at: 2026-10-21T22:53:14Z
plan0_scope: []
---
# fm doctor accepts Foreman's own plugins when their installed files match this checkout's source, so a release never holds itself
## Raw request
> fm release: after installing a release, accept the supply entries of Foreman's own plugins (foreman, foreman-ui) it just shipped, so its own update never holds the next release's gate; third-party plugins stay held
## Interpretation
Release 1.2.49's gate held foreman-ui after T-1434 renamed its hooks module and its cache updated: Foreman's own UI mod, holding Foreman's own release. The supply check exists to catch third-party updates; an installed copy that is byte-for-byte the code this checkout ships needs no human review beyond the release itself.
## Assumptions (confidence)
## Acceptance criteria
- [ ] with a fixture where foreman-ui's installed tree equals mods/foreman-ui at HEAD (file for file), a capability change there is accepted on its own and named as 'matches this checkout'; one differing file keeps the hold; third-party plugins are never auto-accepted — verify with `python3 plugin/tests/run.py test_supply_delta`
## Non-goals
## Approach (options → choice → why)
Options: (A) auto-accept only Foreman's two ids, and only when the installed tree equals the checkout's tracked source file for file (chosen: provable, no trust in names alone; a tampered cache still holds); (B) accept by plugin id (a renamed or replaced cache would pass); (C) skip Foreman's plugins in the check (blind to tampering of the very code that guards everything). A dev setup whose installed copy is older than HEAD keeps the hold, which is correct: it isn't what's being released.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests in plugin/tests/test_supply_delta.py with a fake Foreman home (FOREMAN_HOME) holding plugin/ and mods/foreman-ui, and installed copies that match or differ
2. [x] in fmdoctor._check_supply: for ids foreman@foreman and foreman-ui@foreman only, when every file in the install path has the same bytes as the tracked file at the same relative path under the checkout's plugin/ or mods/foreman-ui (git ls-files, regular files only, no extras), record its new entry and say so; anything else keeps today's hold
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_supply_delta 2>&1 | tail -30` → ✗ exit 1 · Ran 43 tests in 8.7s (3 classes, 16 at a time; slowest: SupplyDelta 2s, OwnPlugins 1s, FindNeeds 1s) / FAILED (1 classes) [ran] [tree b1d008d5d450] (2026-10-21T22:56:07Z)
- (step 1) `python3 plugin/tests/run.py test_supply_delta` → ✗ exit 1 · Ran 43 tests in 2.3s (3 classes, 16 at a time; slowest: SupplyDelta 2s, FindNeeds 1s, OwnPlugins 1s) / FAILED (1 classes) [ran] [tree b1d008d5d450] (2026-10-21T22:56:13Z)
- (ac 1) `python3 plugin/tests/run.py test_supply_delta 2>&1 | tail -4` → exit 0 · Ran 43 tests in 2.0s (3 classes, 16 at a time; slowest: SupplyDelta 2s, OwnPlugins 1s, FindNeeds 1s) / OK [ran] [tree 962b11fee5f4] (2026-10-21T22:57:43Z)
- (step 2) `python3 plugin/tests/run.py test_supply_delta` → exit 0 · Ran 43 tests in 2.5s (3 classes, 16 at a time; slowest: SupplyDelta 2s, OwnPlugins 1s, FindNeeds 1s) / OK [ran] [tree 962b11fee5f4] (2026-10-21T22:57:50Z)
- (ac 1) `python3 plugin/tests/run.py test_supply_delta 2>&1 | grep -E "^(FAIL|ERROR|OK|Ran)"` → ✗ exit 1 · Ran 48 tests in 2.3s (3 classes, 16 at a time; slowest: SupplyDelta 1s, OwnPlugins 1s, FindNeeds 1s) / FAILED (1 classes) [ran] [tree e8dd829935f0] (2026-10-21T22:59:22Z)
- (step 2) `python3 plugin/tests/run.py test_supply_delta` → ✗ exit 1 · Ran 48 tests in 2.3s (3 classes, 16 at a time; slowest: SupplyDelta 2s, OwnPlugins 1s, FindNeeds 1s) / FAILED (1 classes) [ran] [tree e8dd829935f0] (2026-10-21T22:59:30Z)
- (ac 1) `python3 plugin/tests/run.py test_supply_delta 2>&1 | grep -B2 -A12 "^FAIL:" | tail -12` → ✗ exit 1 · Ran 13 tests in 0.945s / FAILED (failures=1) [ran] [tree 9b3869cc17e6] (2026-10-21T22:59:59Z)
- (ac 1) `python3 plugin/tests/run.py test_supply_delta 2>&1 | grep -E "^(FAIL|ERROR|OK|Ran)"` → exit 0 · Ran 48 tests in 1.9s (3 classes, 16 at a time; slowest: SupplyDelta 1s, OwnPlugins 1s, FindNeeds 1s) / OK [ran] [tree 849b60dcb92f] (2026-10-21T23:00:29Z)
- (step 2) `python3 plugin/tests/run.py test_supply_delta` → exit 0 · Ran 48 tests in 2.0s (3 classes, 16 at a time; slowest: SupplyDelta 1s, OwnPlugins 1s, FindNeeds 1s) / OK [ran] [tree bb009c289766] (2026-10-21T23:00:42Z)
- (step 1) `python3 plugin/tests/run.py test_supply_delta test_doctor` → exit 0 · Ran 102 tests in 6.2s (21 classes, 16 at a time; slowest: ViewsRepair 5s, Command 5s, Checks 2s) / OK [ran] [tree 7f62d7df2726] (2026-10-21T23:07:30Z)
- (step 2) `python3 plugin/tests/run.py test_supply_delta test_doctor` → exit 0 · Ran 102 tests in 4.6s (21 classes, 16 at a time; slowest: Command 4s, ViewsRepair 4s, Fix 2s) / OK [ran] [tree 7f62d7df2726] (2026-10-21T23:07:35Z)
## Log
- 2026-10-21T22:33:06Z created
- 2026-10-21T22:52:56Z planned from capture
- 2026-10-21T22:52:57Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1441.builder.md
- 2026-10-21T22:53:13Z focused
- 2026-10-21T23:07:10Z merged worktree-agent-ab1be492cffa2682f (2 file(s))
- 2026-10-21T23:07:10Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab1be492cffa2682f
- 2026-10-21T23:07:22Z focused
- 2026-10-21T23:08:50Z paused: focus moved to T-1417
- 2026-10-21T23:20:40Z focused
- 2026-10-21T23:21:06Z dropped: reverted (11ed8e10) after review: auto-accepting own plugins trusted plantable gitignored files and an unreviewed HEAD; the human fm doctor --accept-supply step stays (research T-1441-review, decision recorded)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1396 [SECURITY M, done, 3 steps] Hostile skills and plugins can't get past the indexer: a 25+ item corpus quarantined with reasons, the Agent Skills spec checked, over…
- research brainstorm-fm-anthropic-half-a: Grounded against `plugin/lib` at HEAD (branch foreman/build; fmcli.py and test_cli.py have uncommitted edits).
- T-1392 [SECURITY M, done, 3 steps] A plugin update that adds a hook event, MCP server or script is held with that exact delta until fm doctor --accept-supply; fm plugins…
- decision 2026-10-21: Accept foreman-ui's supply entry after T-1434 named its hooks module
- similar finished tasks took 3–3 steps
