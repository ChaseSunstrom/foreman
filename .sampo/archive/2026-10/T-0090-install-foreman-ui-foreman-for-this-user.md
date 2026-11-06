---
id: T-0090
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-02T19:05:06Z
updated: 2026-10-02T19:09:12Z
base: 994a4aa912590170d992e89c24c3fc45429e824c
verified: ok
---
# Install foreman-ui@foreman for this user
## Raw request
> Install foreman-ui@foreman for this user
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] claude plugin list shows foreman-ui — verify with `claude plugin list`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] install from the local foreman marketplace
## Resume here
<!-- auto -->
- 2026-10-02T19:05:47Z step 1/1: install from the local foreman marketplace
- git: foreman/build; 0 uncommitted
## Docs impact
## Verification evidence
- (step 1) `claude plugin list` → exit 0 · Path: ~/.claude/plugins/synced/5c6dfa37-93dd-4629-b988-4c203bfcc1c6_1c4f9a98-efaa-4a14-b5b3-7852713bd772/figma~g2 / Status: ✘ disabled [ran] [tree d724667519e7] (2026-10-02T19:09:11Z)
- (ac 1) `claude plugin list` → exit 0 · Path: ~/.claude/plugins/synced/5c6dfa37-93dd-4629-b988-4c203bfcc1c6_1c4f9a98-efaa-4a14-b5b3-7852713bd772/figma~g2 / Status: ✘ disabled [ran] [tree d724667519e7] (2026-10-02T19:09:12Z)
- (step 1) `claude plugin list` → exit 0 · Path: ~/.claude/plugins/synced/5c6dfa37-93dd-4629-b988-4c203bfcc1c6_1c4f9a98-efaa-4a14-b5b3-7852713bd772/figma~g2 / Status: ✘ disabled [ran] [tree d724667519e7] (2026-10-02T19:09:12Z)
- (audit self) `plugin list shows foreman-ui@foreman installed at user scope from the pinned local marketplace; the dev-mods copy is the same code` → no findings [tree d724667519e7] (2026-10-02T19:09:12Z)
## Log
- 2026-10-02T19:05:06Z created
- 2026-10-02T19:05:06Z focused
- 2026-10-02T19:05:22Z user approved plugin in Claude Code's permission prompt
- 2026-10-02T19:05:47Z paused: focus moved to T-0089
- 2026-10-02T19:08:51Z focused
- 2026-10-02T19:09:06Z user approved plugin in Claude Code's permission prompt
- 2026-10-02T19:09:08Z plugin grant used for: fm plugins install changes Claude Code's plugins [plugin foreman-ui@foreman]
- 2026-10-02T19:09:12Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0003 [FEATURE L, done, 5 steps] Phase 5: integration — install-user wiring, plugin decisions, CLAUDE.md, rules symlink, deny rules
- research t0036-operator: The implementation matches its documented contract and is well tested. Findings below are minor.
- T-0016 [FEATURE L, done, 4 steps] Approved plugin/marketplace installs on demand; conflict-free integration of plugins and skills
- research t0016-edge: 901a8c8-aa34-4df7-8164-6500197eb1c7","version":"2.1.280","gitBranch":"foreman/build","slug":"starry-petting-quasar"}
- similar past tasks were L: consider --tier L
- similar finished tasks took 4–5 steps
## Files touched
- plugin/lib/fmplugins.py
- plugin/tests/test_plugins.py
