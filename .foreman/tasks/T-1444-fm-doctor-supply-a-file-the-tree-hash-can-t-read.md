---
id: T-1444
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/lib/fmdoctor.py, plugin/lib/fmplugins.py, plugin/tests/test_supply_delta.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-21T22:52:18Z
updated: 2026-10-22T14:14:59Z
base: 5b09e03e5799de7b9b881ee9be9bca571a68442b
base_tree: c2cc3d971945b547338bf8768ec570c1b8f2f97c
plan0_at: 2026-10-22T14:01:02Z
plan0_scope: [plugin/lib/fmdoctor.py, plugin/lib/fmplugins.py, plugin/tests/test_supply_delta.py, CHANGELOG.md]
verified: strong
---
# Supply check holds a plugin file it can't read
## Raw request
> fm doctor supply: a file the tree hash can't read keeps the old baseline with only a WARN 'not checked', so a new unreadable SKILL.md is never held; and fmplugins.profile() lists only default component paths (custom plugin.json paths and nested commands are missing from names and token estimates) (T-1434 builder)
## Interpretation
_tree_hash opens every file; one unreadable file (chmod 000, a dangling permission) raises, _supply records the whole plugin in errors, and _check_supply keeps the OLD baseline with only a WARN 'not checked' — so planting one unreadable file hides every later change to that plugin. A component file the capability check needs (a SKILL.md or agent .md whose frontmatter may carry hooks) that can't be read must hold the plugin, like an unread hooks spec does. Second part: fmplugins.profile() globs only skills/*/SKILL.md, commands/*.md, agents/*.md, so plugin.json custom component paths (commands/agents/skills as a string or list) and nested commands/sub/x.md are missing from names and the token estimate.
## Assumptions (confidence)
## Acceptance criteria
- [x] a plugin with one unreadable file is still compared (a later change to another file shows) and an unreadable SKILL.md holds it (FAIL naming the file) — verify with `cd plugin/tests && python3 -m unittest test_supply_delta.SupplyDelta.test_an_unreadable_file_is_held_not_skipped`
- [x] profile() lists components from plugin.json custom paths and nested commands, confined to the plugin — verify with `cd plugin/tests && python3 -m unittest test_supply_delta.SupplyDelta.test_profile_reads_custom_component_paths`
## Non-goals
## Approach (options → choice → why)
_tree_hash: an unreadable file is named with a fixed 'unreadable' marker (the stand-in hash) instead of raising, so the rest of the plugin still compares; _frontmatter_hooks / profile: a component .md that can't be opened goes into caps['unread'] (existing FAIL path: 'can't read …'). profile(): also read plugin.json's commands/agents/skills entries (string or list, confined to the plugin root with _spec-style realpath checks) and commands/**/*.md. Keep each change minimal; reuse _spec_file's confinement idea.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] unreadable files named, component .md unread → held
3. [x] profile reads custom paths and nested commands
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_supply_delta` → exit 0 · Ran 38 tests in 1.978s / OK [ran] [tree e63aa5b414b4] (2026-10-22T14:01:56Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_supply_delta test_plugins test_doctor 2>&1 | grep -v Warning | grep -E "^(FAIL|ERROR|OK|Ran)"` → exit 0 · Ran 107 tests in 11.472s / OK [ran] [tree e3e49fb4df8c] (2026-10-22T14:06:00Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_supply_delta.SupplyDelta.test_an_unreadable_file_is_held_not_skipped` → exit 0 · Ran 1 test in 0.016s / OK [ran] [tree 93ccdcff0eaa] (2026-10-22T14:12:50Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_supply_delta.SupplyDelta.test_profile_reads_custom_component_paths` → exit 0 · Ran 1 test in 0.013s / OK [ran] [tree 93ccdcff0eaa] (2026-10-22T14:12:51Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_supply_delta.SupplyDelta.test_an_unreadable_file_is_held_not_skipped` → exit 0 · Ran 1 test in 0.019s / OK [ran] [tree 7e7825e58688] (2026-10-22T14:13:19Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_supply_delta.SupplyDelta.test_profile_reads_custom_component_paths` → exit 0 · Ran 1 test in 0.014s / OK [ran] [tree 7e7825e58688] (2026-10-22T14:13:19Z)
- (audit adversary) `builder (sonnet) test-first, red confirmed on the pre-fix tree in a scratch copy; fm-reviewer adversary/edge/maintainer pass (research T-1444-review): 1 HIGH, 1 MEDIUM, 4 LOW, all fixed on the branch and spot-checked; merged, suites green (test_supply_delta, test_plugins, test_doctor); live doctor supply PASS.` → unreadable files and unlistable folders are named with stand-ins (mode, size, mtime, ctime); markers can't be forged by content alone [tree 7e7825e58688] (2026-10-22T14:13:19Z)
- (audit edge) `builder (sonnet) test-first, red confirmed on the pre-fix tree in a scratch copy; fm-reviewer adversary/edge/maintainer pass (research T-1444-review): 1 HIGH, 1 MEDIUM, 4 LOW, all fixed on the branch and spot-checked; merged, suites green (test_supply_delta, test_plugins, test_doctor); live doctor supply PASS.` → a file vanishing mid-walk is named, not an error; tests skip chmod cases under root [tree 7e7825e58688] (2026-10-22T14:13:19Z)
- (audit maintainer) `builder (sonnet) test-first, red confirmed on the pre-fix tree in a scratch copy; fm-reviewer adversary/edge/maintainer pass (research T-1444-review): 1 HIGH, 1 MEDIUM, 4 LOW, all fixed on the branch and spot-checked; merged, suites green (test_supply_delta, test_plugins, test_doctor); live doctor supply PASS.` → _SUPPLY_SKIP (node_modules etc.) still unhashed — captured T-1459 [tree 7e7825e58688] (2026-10-22T14:13:19Z)
- (audit self) `builder (sonnet) test-first, red confirmed on the pre-fix tree in a scratch copy; fm-reviewer adversary/edge/maintainer pass (research T-1444-review): 1 HIGH, 1 MEDIUM, 4 LOW, all fixed on the branch and spot-checked; merged, suites green (test_supply_delta, test_plugins, test_doctor); live doctor supply PASS.` → no findings [tree 7e7825e58688] (2026-10-22T14:13:19Z)
## Log
- 2026-10-21T22:52:18Z created
- 2026-10-22T14:00:49Z planned from capture
- 2026-10-22T14:00:50Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1444.builder.md
- 2026-10-22T14:01:01Z focused
- 2026-10-22T14:12:38Z merged worktree-agent-a4253fb4342c1b5ce (3 file(s))
- 2026-10-22T14:12:38Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a4253fb4342c1b5ce
- 2026-10-22T14:12:39Z focused
- 2026-10-22T14:14:58Z done
- 2026-10-22T14:14:59Z committed affebffd (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1392-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict: changes needed.** The FAIL only fires for a narrow set of u…
- research T-1434-1417-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** T-1438 approve. T-1434 changes needed. T-1417 change…
- T-1434 [SECURITY M, done, 3 steps] fm doctor's supply check reads the rest of what a plugin runs: hooks in skill and agent frontmatter, LSP servers, linked and large fil…
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_doctor.py, plugin/tests/test_plugins.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, plugin/lib/fmdoctor.py, plugin/lib/fmplugins.py, plugin/tests/test_supply_delta.py; re-ground the plan against them before editing
## Files touched
- plugin/tests/test_supply_delta.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmplugins.py
- CHANGELOG.md
