---
id: T-1501
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/lib/fmauditrun.py, plugin/skills/intake/references/audit.md, plugin/agents/fm-reviewer.md, plugin/tests/test_audit.py, plugin/tests/test_audit_run.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:14Z
updated: 2026-10-22T19:46:04Z
base: d3fef34bc300e4085f5f092c797f6629c75d195f
base_tree: ffd5f3ceadfa9c1227503f98cd2c9b95512df0c7
plan0_at: 2026-10-22T18:42:59Z
plan0_scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/lib/fmauditrun.py, plugin/skills/intake/references/audit.md, plugin/agents/fm-reviewer.md, plugin/tests/test_audit.py, plugin/tests/test_audit_run.py, CHANGELOG.md]
verified: strong
---
# fm-reviewer: a design lens with three personas
## Raw request
> fm-reviewer: a design lens with three personas
## Interpretation
Brainstorm T-1479 cluster 9: a UI diff gets a design read: an art director (is there a point of view, is it generic), an accessibility reviewer (contrast, focus, motion), and a first-time user (can I tell what to do). The reviewer agent and the audit brief gain a 'design' lens used when the diff touches UI files, reading screenshots when the task has them.
## Assumptions (confidence)
## Acceptance criteria
- [x] the reviewer prompt defines the design lens with the three personas and fm audit prep names it for a UI diff — verify with `cd plugin/tests && python3 -m unittest test_audit.DesignLens`
- [x] fm audit run runs the design reviewer only when the prepared brief has a design section; a non-UI diff costs nothing extra — verify with `python3 plugin/tests/run.py test_audit_run`
## Non-goals
## Approach (options → choice → why)
Grounded: lenses are fmcore.AUDIT_LENSES (1094, also validates fm task audit/--lens/fmlanes _LENS_HEAD); fm audit prep (fmcli ~4491) adds adversary to any tier when fmcore.sensitive(files) and otherwise uses AUDIT_LENSES minus self; templates come from skills/intake/references/audit.md (**name** — context: …\n> prompt); fmauditrun.py:55 runs one headless reviewer per AUDIT_LENSES entry. Options: (1) chosen: design joins AUDIT_LENSES (so it can be recorded) but not the default set: a DEFAULT_LENSES tuple (intent, adversary, edge, operator, maintainer) replaces 'AUDIT_LENSES minus self' in prep and audit run; prep adds design, like adversary, when fmcore.ui_paths(files) finds UI files (html/css/scss/less/tsx/jsx/vue/svelte/astro, mods/*/hooks, *tui*.py, templates/); audit run runs design only when the prepared brief has a design section; the design section lists screenshots the brief names (existing .png/.jpg/.webp paths) so the reviewer reads them; the audit.md template has the three personas: art director (a point of view, or generic tells: fm design lint names them), accessibility reviewer (contrast, focus order and visibility, reduced motion, target size), first-time user (what can I do here, what happened after I did it). Not required by REQUIRED_AUDITS: advisory, like a stack card checklist. (2) design in the default set: rejected, every backend diff would pay for it. (3) a separate fm design review command: rejected, two review paths drift. Claude Code parity: the lens lives in the plugin's fm-reviewer agent and fm audit prep, which /foreman:review and the fm code app both use.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] lens in plugin/agents/fm-reviewer.md and the audit brief
3. [x] review fixes: ui_paths shares design lint's skips, anchored lens headings, no dot-dir screenshots
## Resume here
## Docs impact
plugin/skills/intake/references/audit.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_audit test_audit_run` → ✗ exit 1 · Ran 31 tests in 6.5s (17 classes, 16 at a time; slowest: AuditRun 6s, ImportCards 3s, TaskLifecycle 2s) / FAILED (2 classes) [ran] [tree d6d7c8a3ce60] (2026-10-22T18:46:15Z)
- (step 2) `python3 plugin/tests/run.py -k test_docs -k test_cli -k test_edit_cards -k test_core -k test_lanes 2>&1 | tail -4` → exit 0 · Ran 275 tests in 47.9s (67 classes, 16 at a time; slowest: TaskLifecycle 48s, Lanes 37s, ImportCards 28s) / OK [ran] [tree 2a95b96f0e47] (2026-10-22T18:51:23Z)
- (step 2) `python3 plugin/tests/run.py test_audit test_audit_run` → exit 0 · Ran 31 tests in 7.0s (17 classes, 16 at a time; slowest: AuditRun 7s, DesignLens 3s, ImportCards 3s) / OK [ran] [tree 2a95b96f0e47] (2026-10-22T18:51:52Z)
- (step 3) `python3 plugin/tests/run.py -k DesignLens` → ✗ exit 1 · Ran 8 tests in 3.9s (1 classes, 16 at a time; slowest: DesignLens 4s) / FAILED (1 classes) [ran] [tree e25c3edcb695] (2026-10-22T19:02:05Z)
- (step 3) `python3 plugin/tests/run.py -k DesignLens -k AuditRun` → exit 0 · Ran 14 tests in 5.6s (2 classes, 16 at a time; slowest: AuditRun 5s, DesignLens 4s) / OK [ran] [tree 0f54b8f24d58] (2026-10-22T19:03:09Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_audit.DesignLens` → exit 0 · Ran 8 tests in 7.544s / OK [ran] [tree cfbf58df6882] (2026-10-22T19:42:09Z)
- (ac 2) `python3 plugin/tests/run.py test_audit_run` → exit 0 · Ran 7 tests in 11.7s (1 classes, 16 at a time; slowest: AuditRun 11s) / OK [ran] [tree cfbf58df6882] (2026-10-22T19:42:22Z)
- (step 1) `python3 plugin/tests/run.py test_audit test_audit_run test_lanes` → exit 0 · Ran 65 tests in 26.7s (22 classes, 16 at a time; slowest: Lanes 26s, AuditRun 15s, DesignLens 10s) / OK [ran] [tree cfbf58df6882] (2026-10-22T19:43:00Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_audit.DesignLens` → exit 0 · Ran 8 tests in 7.599s / OK [ran] [tree a79582f55ff1] (2026-10-22T19:43:27Z)
- (ac 2) `python3 plugin/tests/run.py test_audit_run` → exit 0 · Ran 7 tests in 18.0s (1 classes, 16 at a time; slowest: AuditRun 18s) / OK [ran] [tree a79582f55ff1] (2026-10-22T19:43:27Z)
- (audit intent) `one fm-reviewer pass: approve with nits; 1 MEDIUM (ui_paths too broad) and 4 LOW fixed in 2f10d1b8` → a design lens with three personas, named by fm audit prep for UI diffs, run by fm audit run only then [tree a79582f55ff1] (2026-10-22T19:43:27Z)
- (audit adversary) `one fm-reviewer pass: approve with nits; 1 MEDIUM (ui_paths too broad) and 4 LOW fixed in 2f10d1b8` → brief text can't trigger the design reviewer (fm audit run reads the header fm writes); screenshots under dot-directories aren't listed [tree a79582f55ff1] (2026-10-22T19:43:27Z)
- (audit edge) `one fm-reviewer pass: approve with nits; 1 MEDIUM (ui_paths too broad) and 4 LOW fixed in 2f10d1b8` → dist/, node_modules/, vendor/, build/, *.min.* and coverage html aren't UI; statusline scripts are [tree a79582f55ff1] (2026-10-22T19:43:27Z)
- (audit maintainer) `one fm-reviewer pass: approve with nits; 1 MEDIUM (ui_paths too broad) and 4 LOW fixed in 2f10d1b8` → DesignLens and AuditRun tests red first; lens headings anchored for every lens [tree a79582f55ff1] (2026-10-22T19:43:27Z)
## Log
- 2026-10-22T17:36:14Z created
- 2026-10-22T17:58:59Z set scope=['plugin/agents/fm-reviewer.md', 'plugin/lib/fmauditrun.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_audit.py', 'CHANGELOG.md']
- 2026-10-22T18:28:37Z set tier=M
- 2026-10-22T18:28:38Z set scope=['plugin/lib/fmcore.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmauditrun.py', 'plugin/skills/intake/references/audit.md', 'plugin/agents/fm-reviewer.md', 'plugin/tests/test_audit.py', 'plugin/tests/test_audit_run.py', 'CHANGELOG.md']
- 2026-10-22T18:42:43Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1501.builder.md
- 2026-10-22T18:42:57Z focused
- 2026-10-22T19:20:04Z merged worktree-agent-ae98cfe521c8e9669 (11 file(s))
- 2026-10-22T19:20:10Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae98cfe521c8e9669
- 2026-10-22T19:42:00Z focused
- 2026-10-22T19:43:00Z scope: fmlanes.py and fmdesign.py were changed at the review's request (lens headings, shared skip dirs); other files changed through other tasks' merges after T-1501's base
- 2026-10-22T19:46:02Z done
- 2026-10-22T19:46:04Z committed 74007f13 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1074 [FEATURE M, done, 3 steps] Hotspots in plans: files that keep getting fixed after edits are flagged in the plan and a — lesson: A history signal needs a cap on sw…
- T-1488 [FEATURE M, done, 2 steps] UI playbook: design direction before pixels — lesson: A playbook's acceptance check proves headings, not quality: pair every writing ta…
- T-0780 [FEATURE S, done, 2 steps] Audit findings reach the host's review UI: fm audit prep asks for ReportFindings fields and tells the main thread to report them — less…
- decision 2026-10-22: T-1479 brainstorm: 548 ideas grounded into 26 capabilities; round 1 (19 tasks: UI design, motion and 3D playbooks and template, fm design lint, TUI …
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/agents/fm-reviewer.md, plugin/lib/fmauditrun.py, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/skills/intake/references/audit.md, plugin/tests/test_audit.py, plugin/tests/tes…; re-ground the plan against them before editing
## Why not caught
lens-heading parsing was built from AUDIT_LENSES by a loose regex, so a new name widened what it matched
## Lessons
- Adding a value to a list other code iterates (AUDIT_LENSES) changes every consumer: grep each use before adding, and keep defaults as their own tuple
## Plan gaps
- added late: review fixes: ui_paths shares design lint's skips, anchored lens headings, no dot-dir screenshots
- failed first: step 1 failing test
- failed first: step 3 review fixes: ui_paths shares design lint's skips, anchored lens headings, no dot-dir screenshots
## Files touched
- plugin/tests/test_audit.py
- plugin/tests/test_audit_run.py
- plugin/lib/fmcore.py
- plugin/lib/fmdesign.py
- plugin/lib/fmcli.py
- plugin/lib/fmauditrun.py
- plugin/skills/intake/references/audit.md
- plugin/agents/fm-reviewer.md
- MASTER.md
- README.md
- plugin/lib/fmlanes.py
- CHANGELOG.md
- plugin/README.md
- plugin/commands/settings.md
- plugin/lib/fmguard.py
- plugin/lib/fmhooks.py
- plugin/lib/fmplaybooks.py
- plugin/lib/fmsettings.py
- plugin/skills/brainstorm/SKILL.md
- plugin/skills/directions/SKILL.md
- plugin/skills/directions/references/cards.md
- plugin/skills/doctor/SKILL.md
- plugin/skills/improve/SKILL.md
- plugin/skills/intake/SKILL.md
- plugin/skills/library/SKILL.md
- plugin/skills/next/SKILL.md
- plugin/skills/playbooks/ratchet.json
- plugin/skills/playbooks/references/clean/code-simplifier.md
- plugin/skills/playbooks/references/clean/repo-sweep.md
- plugin/skills/playbooks/references/context/context-budget.md
