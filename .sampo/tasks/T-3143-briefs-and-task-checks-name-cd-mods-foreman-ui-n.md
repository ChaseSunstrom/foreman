---
id: T-3143
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T05:11:31Z
updated: 2026-11-05T11:17:43Z
builder_model: haiku
base: 9ff3d8619e5a678a4cb33bdba1990f5ab9ea5a5d
base_tree: 6ca08f40dcb206b6de69dd19a8447080612d4f1b
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T09:56:17Z
plan0_scope: []
builder_returned: 2026-11-05T10:01:12Z
lane_stop: merged 2026-11-05T11:02:04Z
verified: strong
unproven: [docs]
---
# Briefs, criteria templates and playbooks name 'claude plugin test mods/foreman-ui' for the UI mod, never 'cd mods/foreman-ui && npx vitest run' (which can't run here and refused T-3113's merge)
## Raw request
> briefs and task checks name 'cd mods/foreman-ui && npx vitest run' for the UI mod, which can't run here ('Cannot find package claude-code/testing'); the mod's test command is 'claude plugin test mods/foreman-ui'; fix the T-3113 criteria pattern and any playbook or brief template that names vitest for the mod
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] no brief template, playbook, skill or criteria suggestion under plugin/ names npx vitest for mods/foreman-ui, and the UI mod's test command Sampo suggests is claude plugin test mods/foreman-ui — verify with `python3 plugin/tests/run.py test_docs test_lanes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] find each place, test, replace
## Resume here
<!-- auto -->
- 2026-11-05T11:04:51Z step 1/1: find each place, test, replace
- git: foreman/build; 2 uncommitted: CHANGELOG.md, scripts/
- touched since last checkpoint: CHANGELOG.md
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_docs test_lanes` → exit 0 · Ran 277 tests in 103.5s (42 classes, 16 at a time; slowest: Lanes 102s, LaneRecovery 69s, RaceEvidence 42s) / OK [ran] [tree bdfbdc0e00e1] [world 2f1906870a] (2026-11-05T10:00:47Z)
- (step 1) `python3 plugin/tests/run.py test_docs test_lanes` → ✗ exit 1 · Ran 277 tests in 78.3s (42 classes, 16 at a time; slowest: Lanes 78s, LaneRecovery 57s, RaceEvidence 35s) / FAILED (1 classes: test_lanes.SelfChangeGate) [ran] [tree 92b27fab0a86] [world 2f1906870a] (2026-11-05T11:03:35Z)
- `python3 plugin/tests/run.py test_docs.UiModTestCommand` → ✗ exit 1 · Ran 2 tests in 3.5s (1 classes, 16 at a time; slowest: UiModTestCommand 0s) / FAILED (1 classes: test_docs.UiModTestCommand) (start tree + this task's tests) [ran] [tree 92b27fab0a86] [world 2f1906870a] (2026-11-05T11:03:42Z)
- `python3 plugin/tests/run.py test_docs.UiModTestCommand` → exit 0 · Ran 2 tests in 1.7s (1 classes, 16 at a time; slowest: UiModTestCommand 0s) / OK [ran] [tree 92b27fab0a86] [world 2f1906870a] (2026-11-05T11:03:42Z)
- (step 1) `python3 plugin/tests/run.py test_docs test_lanes` → exit 0 · Ran 277 tests in 141.8s (42 classes, 16 at a time; slowest: Lanes 141s, LaneRecovery 67s, RaceEvidence 43s) / OK [ran] [tree 1aa4dec9a3a5] [world 2f1906870a] (2026-11-05T11:13:26Z)
- (ac 1) `python3 plugin/tests/run.py test_docs test_lanes` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T11:13:26Z [ran] [tree 1aa4dec9a3a5] [world 2f1906870a] (2026-11-05T11:13:41Z)
- (audit edge) `self: read the merged diff (the cc-mod-testing card names claude plugin test mods/foreman-ui; test_docs.UiModTestCommand sweeps plugin/ briefs, templates, playbooks and skills for npx vitest aimed at the mod); proved red on the start tree; test_docs + test_lanes 277 green` → npx vitest stays allowed where a project has its own package.json (only the foreman-ui mod pairing is refused); T-3189 adds the general warning for any verify command that can't run in a fresh lane [tree 1aa4dec9a3a5] (2026-11-05T11:13:41Z)
- (audit self) `self: read the merged diff (the cc-mod-testing card names claude plugin test mods/foreman-ui; test_docs.UiModTestCommand sweeps plugin/ briefs, templates, playbooks and skills for npx vitest aimed at the mod); proved red on the start tree; test_docs + test_lanes 277 green` → no findings [tree 1aa4dec9a3a5] (2026-11-05T11:13:41Z)
## Log
- 2026-11-05T05:11:31Z created
- 2026-11-05T09:55:53Z planned from capture
- 2026-11-05T09:55:55Z set approved=True
- 2026-11-05T09:55:59Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3143.builder.md
- 2026-11-05T09:56:17Z focused
- 2026-11-05T09:56:17Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-05T11:02:04Z merged worktree-agent-a2f8fbd4f56147ddc (2 file(s))
- 2026-11-05T11:02:05Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2f8fbd4f56147ddc
- 2026-11-05T11:02:08Z focused
- 2026-11-05T11:04:52Z paused: focus moved to T-3195
- 2026-11-05T11:10:55Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-05T11:10:55Z focused
- 2026-11-05T11:17:38Z done
- 2026-11-05T11:17:43Z committed 8156d1f7 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2049-review: Changes needed. The lint logic is sound and the AC-named test looks right. One MEDIUM finding is on the card-admission path. I had no shell, so I…
- research T-1534-review: Verdict:** changes needed (one MEDIUM, easy to fix). The data-not-code question comes out clean. [stale: plugin/tests/test_ui_replay.py changed s…
- research T-2044-review: Not checked:** I read about 25 cards in full and ran grep across the rest. I had no network and could not run any command, so package and flag cl…
- decision 2026-10-31: Mission 6 (tools, #5) approach A: wire the parts Foreman has into one loop on the active task (T-2270's hook notices the miss; fm which, fm lib and …
## Files touched
- plugin/tests/test_docs.py
- plugin/skills/library/cards/claude-code/cc-mod-testing.md
- CHANGELOG.md
