---
id: T-3342
type: CLEAN
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo, plugin/tests, README.md, plugin/skills]
depends_on: []
source: user
created: 2026-11-06T05:09:41Z
updated: 2026-11-06T06:08:17Z
lane: ~/.claude/foreman/.claude/worktrees/agent-ad87d1e22878ac6e5
lane_branch: worktree-agent-ad87d1e22878ac6e5
base: 0e503eeeeb87000325d02673ba119e35ff08b7e8
base_tree: 5c2bb7b2f14ef72b4659b9d747b61d1c44bc9aca
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T06:08:17Z
plan0_scope: [plugin/lib/sampo, plugin/tests, README.md, plugin/skills]
---
# Mirror folder .foreman/ becomes .sampo/: one constant (core.MIRROR/MIRRORS/MIRROR_DIRS) every site reads, the old folder still read, sync.move renames it once with git mv in one logged commit at a CLI export (never from a hook), the guard and verify-lint cover .sampo, and the rename scan allows .foreman only as an alias
## Raw request
> The repo mirror is still named .foreman/ (sync.DIR, sync.py:23) and ~36 code sites name it (core mirror_ignored and audit pathspecs, hooks, playbooks, smith, stack, change, fixes); the product is Sampo. Rename the mirror to .sampo/ with one constant every caller reads (core.MIRROR); a repo that already has .foreman/ keeps working: sync reads it, and moves it to .sampo/ with git mv on the next export (one commit, logged), never two mirrors at once; the guard's state-direct rule covers both names. Also sweep every other user-visible 'foreman' name the rename left behind (FOREMAN_* env vars shown in docs, refs/foreman/*, the foreman/build branch name in messages, .foreman-state.json) with the rename scan, keeping old names as read-only aliases. User: 'How come the state is still called .foreman?'
## Interpretation
Reading 1: rename the mirror folder to .sampo/ with one constant, old folder still read, moved once. Reading 2 (ruled out): rename every foreman name now; env vars, refs and branch prefix are separate alias tasks.
## Assumptions (confidence)
## Acceptance criteria
- [ ] no .foreman literal left in the library except the constant, and the listed tests pass — verify with `python3 plugin/tests/run.py test_sync test_fixes test_parallel test_secrets test_ui test_playbook_machinery test_code_tui test_execution test_guard test_guard_sampo test_board_posture test_rename_scan`
- [ ] a tracked .foreman becomes one logged rename commit; ignored, both-folders, mid-merge and failed-commit cases tested — verify with `python3 plugin/tests/run.py test_sync`
- [ ] the user-visible mirror folder is .sampo/ (the product's name), and sync status and the README name it — verify with `python3 plugin/tests/run.py test_sync`
- [ ] the guard's state-direct rule and verify-lint cover both .sampo and .foreman — verify with `python3 plugin/tests/run.py test_guard test_guard_sampo test_board_posture`
- [ ] the user asks why state is still called .foreman: fresh sync writes .sampo/ and status names it — verify with `python3 plugin/tests/run.py test_sync`
## Non-goals
Renaming refs/foreman/*, the foreman/<id> lane branch prefix, .foreman-state.json and FOREMAN_* env vars: their own alias tasks (T-3369 for env vars). Running the move on this repo: the main thread does it last, alone.
## Approach (options → choice → why)
1) one constant (core.MIRROR/MIRRORS/MIRROR_DIRS) read by every site, .foreman read while .sampo is absent, sync.move git mv at a CLI export: likely outcome one logged commit; fails if a hook triggers it or both folders exist. 2) opt-in sampo sync move plus doctor nudge: fails if .foreman lingers forever. 3) rename on disk, next task commits it: fails with 6000 renames in an unrelated commit. 4) use what exists: sync.mirror(p) already picks the folder, extend it; likely outcome small diff. 5) do less: alias only, no move; fails the user complaint. Choice 1 (80%): matches the ask.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py; past FIXes T-2061, T-2846.
## Execution prompt
## Steps
1. [ ] constant and every site  <- CURRENT
2. [ ] sync.move with its cases
3. [ ] guard/verify-lint and rename-scan checks
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T05:09:41Z created
- 2026-11-06T06:00:08Z planned from capture
- 2026-11-06T06:08:12Z focused
- 2026-11-06T06:08:17Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2748 [CLEAN M, done, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.py s…
- decision 2026-11-03: [cites: user steer: read SAMPO.md (RENAME, NOW)] [check: python3 plugin/tests/run.py test_rename_scan] Rename Foreman to Sampo per SAMPO.md: aliases…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_agents.py, plugin/tests/test_ambient.py, plugin/tests/test_anergy.py, plugin/tests/test_audit.py, plugin/tests/test_away.py, plugin/tests/…
