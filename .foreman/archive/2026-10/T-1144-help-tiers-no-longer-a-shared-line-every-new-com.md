---
id: T-1144
type: CLEAN
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_help.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-16T10:08:42Z
updated: 2026-10-16T10:21:57Z
base: 8aeebcfcef5c328c6470d16ddd37051ce23bbbec
base_tree: 5184ce6d50a12574eba99751eb88ede9870bd492
plan0_at: 2026-10-16T10:11:08Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_help.py, CHANGELOG.md]
verified: strong
---
# Help tiers no longer a shared line every new command edits: each fm command declares its h
## Raw request
> Help tiers no longer a shared line every new command edits: each fm command declares its help tier where it is registered (add(..., tier=...)), so parallel builders adding commands stop conflicting on HELP_TIERS (T-1059/T-1062 conflicted on it twice on 2026-10-16)
## Interpretation
HELP_TIERS in fmcli.py is one table of space-separated command names per tier. Every new command adds its name to one of those long strings, so parallel builders adding commands conflict on the same line (T-1059 and T-1062 twice on 2026-10-16). Each command should declare its own tier where it is registered.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm help prints the same tiers before and after; adding a command needs no edit outside its own registration — verify with `python3 plugin/tests/run.py test_help test_cli`
## Non-goals
## Approach (options → choice → why)
The add() helper gains a tier= argument and HELP_TIERS is built from the registrations. A one-time migration moves every command's tier into its add() call. test_help keeps checking that every command has a tier and that the printed help is unchanged (a snapshot of fm help before and after). Options considered: one tier file per command (more files), or sorting the strings (still one line).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Snapshot fm help, then a test that every add() has a tier
2. [x] Move tiers into add() calls, build HELP_TIERS from them; the snapshot still matches
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_help` → ✗ exit 1 · Ran 5 tests in 0.9s (2 classes, 16 at a time; slowest: Help 1s, PromptApprovals 1s) / FAILED (1 classes) [ran] [tree c55f434b2737] (2026-10-16T10:11:56Z)
- (step 2) `python3 plugin/tests/run.py test_help test_cli test_doctor` → exit 0 · Ran 154 tests in 48.5s (47 classes, 16 at a time; slowest: Command 47s, TaskLifecycle 39s, ViewsRepair 35s) / OK [ran] [tree cb82c62e17d5] (2026-10-16T10:15:01Z)
- (step 1) `python3 plugin/tests/run.py test_help test_cli test_doctor` → exit 0 · Ran 154 tests in 35.8s (47 classes, 16 at a time; slowest: Command 35s, TaskLifecycle 24s, ViewsRepair 19s) / OK [ran] [tree 09c266c4d6c6] (2026-10-16T10:18:37Z)
- (ac 1) `python3 plugin/tests/run.py test_help test_cli` → exit 0 · Ran 107 tests in 42.2s (30 classes, 16 at a time; slowest: TaskLifecycle 42s, StateViews 18s, AuditPrep 16s) / OK [ran] [tree 16315f879933] (2026-10-16T10:19:33Z)
- `python3 plugin/tests/run.py test_help` → exit 0 · Ran 5 tests in 1.9s (2 classes, 16 at a time; slowest: Help 2s, PromptApprovals 1s) / OK [ran] [tree 16315f879933] (2026-10-16T10:19:33Z)
- (audit intent) `self review of the branch: add() requires tier=, so an untiered command fails at registration; ties keep registration order; byte-identical help verified by the builder; the next parallel commands touch only their own add() line` → no shared line for every new command [tree 16315f879933] (2026-10-16T10:19:33Z)
- (audit maintainer) `self review of the branch: add() requires tier=, so an untiered command fails at registration; ties keep registration order; byte-identical help verified by the builder; the next parallel commands touch only their own add() line` → one place to look when adding a command [tree 16315f879933] (2026-10-16T10:19:33Z)
## Log
- 2026-10-16T10:08:42Z created
- 2026-10-16T10:09:49Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_help.py', 'CHANGELOG.md']
- 2026-10-16T10:10:52Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1144.builder.md
- 2026-10-16T10:11:07Z focused
- 2026-10-16T10:17:52Z merged worktree-agent-aa0435a2a107b9a03 (3 file(s))
- 2026-10-16T10:17:56Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa0435a2a107b9a03
- 2026-10-16T10:17:56Z focused
- 2026-10-16T10:18:37Z scope: CHANGELOG.md — release note; plugin/tests/test_doctor.py — its HELP_TIERS mock now wraps build_parser
- 2026-10-16T10:18:48Z scope: MASTER.md — how tiers are declared
- 2026-10-16T10:21:57Z done
- 2026-10-16T10:21:57Z committed 48b0dfc (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research wave1-plan-a2475fc5d2263de06: === T-1049 [stale: plugin/lib/fmcli.py, plugin/lib/fmdeps.py, plugin/lib/fmhooks.py changed since it was written]
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- research wave2-plan-a4b64956d53d543cc: === T-1058 [stale: plugin/lib/fmbacktest.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py changed since it was written]
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Behaviour lock
fm help, fm help --json and fm help --all were byte-compared before and after the migration (identical); test_help checks every command has exactly one tier from its registration
## Lessons
- A registry every feature appends to is a merge-conflict magnet: let each entry carry its own registration
## Plan gaps
- failed first: step 1 Snapshot fm help, then a test that every add() has a tier
## Files touched
- plugin/tests/test_help.py
- plugin/lib/fmcli.py
- plugin/lib/fmdoctor.py
- plugin/tests/test_doctor.py
- CHANGELOG.md
- MASTER.md
