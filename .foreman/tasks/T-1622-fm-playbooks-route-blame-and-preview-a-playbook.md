---
id: T-1622
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmplaybooks.py, plugin/lib/fmcli.py, plugin/skills/playbooks/SKILL.md, plugin/tests/test_playbook_machinery.py, CHANGELOG.md]
depends_on: [T-1621]
source: user
created: 2026-10-22T20:57:04Z
updated: 2026-10-23T01:51:08Z
base: c37cd0a11ccc09acca8f19a8512d1ed84bb742b8
base_tree: 17e7e55b1f3e67d0519f053262ddcceb6fb328b3
plan0_at: 2026-10-22T23:41:44Z
plan0_scope: [plugin/lib/fmplaybooks.py, plugin/lib/fmcli.py, plugin/skills/playbooks/SKILL.md, plugin/tests/test_playbook_machinery.py, CHANGELOG.md]
verified: strong
---
# fm playbooks route, blame and preview: a playbook per stage, lines to the tasks that wrote them, the checks a load adds
## Raw request
> fm playbooks route, blame and preview: a playbook per stage, lines to the tasks that wrote them, the checks a load adds
## Interpretation
Three verbs over playbooks: fm playbooks route STAGE names the playbook(s) for a stage from the stage table; fm playbooks blame NAME maps each line to the task that last changed it (git blame plus task ids in commit messages); fm playbooks preview NAME lists the checks loading it adds (its runnable fences and named verify commands). The playbooks SKILL.md gets one line naming them.
## Assumptions (confidence)
## Acceptance criteria
- [x] route names a playbook per stage; blame maps lines to tasks through git; preview lists checks — verify with `python3 plugin/tests/run.py test_playbook_machinery.Verbs`
## Non-goals
## Approach (options → choice → why)
Options: one combined report (hard to read); separate verbs reusing fmplaybooks' parser and git; nothing new (people grep). Choice: three small verbs: each answers one question people ask, reusing what exists.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests per verb
2. [x] router from the stage table, blame from git blame and task ids
3. [x] SKILL.md note
## Resume here
## Docs impact
plugin/skills/playbooks/SKILL.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_playbook_machinery.Verbs` → exit 0 · Ran 4 tests in 2.0s (1 classes, 16 at a time; slowest: Verbs 2s) / OK [ran] [tree 3d919bc2c705] (2026-10-23T01:27:22Z)
- (step 2) `python3 plugin/tests/run.py test_playbook_machinery` → exit 0 · Ran 23 tests in 6.7s (5 classes, 16 at a time; slowest: Load 7s, Verbs 2s, Count 0s) / OK [ran] [tree 3d919bc2c705] (2026-10-23T01:27:30Z)
- (step 3) `python3 plugin/bin/fm check playbooks` → exit 0 · ✓ playbooks: 76 checked, 0 problem(s) / unread in 60 days (the event log covers 6.6): 32 of 76: build/cpp-build, build/csharp-build, build/go-build, build/jvm-build, build/rust-build, build/shell-buil [ran] [tree 3d919bc2c705] (2026-10-23T01:27:36Z)
- (step 2) `python3 plugin/tests/run.py test_playbook_machinery` → exit 0 · Ran 25 tests in 31.2s (5 classes, 16 at a time; slowest: Load 31s, Verbs 16s, Count 1s) / OK [ran] [tree 5729b098c7ec] (2026-10-23T01:45:44Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_machinery test_docs` → exit 0 · Ran 90 tests in 17.9s (20 classes, 16 at a time; slowest: Load 17s, Fences 17s, Verbs 13s) / OK [ran] [tree 4a8946dc8313] (2026-10-23T01:50:08Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_machinery.Verbs` → exit 0 · Ran 6 tests in 2.6s (1 classes, 16 at a time; slowest: Verbs 2s) / OK [ran] [tree 4a8946dc8313] (2026-10-23T01:50:18Z)
- (audit intent) `fm-reviewer pass (shared with T-1627); fixed test-first: blame runs git with --no-textconv and no signature checks, and workers may not run blame (a hostile repo's textconv/gpg test); bytes-decoded blame lines; summary-line task id wins over body mentions; verify commands only inside quotes/backticks; route test no longer pins FIX's playbook` → route names a stage's playbooks from SKILL_FOR, blame maps each line to the task whose commit wrote it, preview lists the checks loading a playbook adds [tree 4a8946dc8313] (2026-10-23T01:50:18Z)
- (audit adversary) `fm-reviewer pass (shared with T-1627); fixed test-first: blame runs git with --no-textconv and no signature checks, and workers may not run blame (a hostile repo's textconv/gpg test); bytes-decoded blame lines; summary-line task id wins over body mentions; verify commands only inside quotes/backticks; route test no longer pins FIX's playbook` → git is argv-only with -- and a timeout; textconv and gpg can't run from a repo's config; workers can't blame [tree 4a8946dc8313] (2026-10-23T01:50:18Z)
- (audit edge) `fm-reviewer pass (shared with T-1627); fixed test-first: blame runs git with --no-textconv and no signature checks, and workers may not run blame (a hostile repo's textconv/gpg test); bytes-decoded blame lines; summary-line task id wins over body mentions; verify commands only inside quotes/backticks; route test no longer pins FIX's playbook` → uncommitted lines say so; \r in a line doesn't shift numbers; an unknown stage lists the valid ones [tree 4a8946dc8313] (2026-10-23T01:50:18Z)
- (audit maintainer) `fm-reviewer pass (shared with T-1627); fixed test-first: blame runs git with --no-textconv and no signature checks, and workers may not run blame (a hostile repo's textconv/gpg test); bytes-decoded blame lines; summary-line task id wins over body mentions; verify commands only inside quotes/backticks; route test no longer pins FIX's playbook` → one shared runnable() fence finder for fm check playbooks and preview [tree 4a8946dc8313] (2026-10-23T01:50:18Z)
## Log
- 2026-10-22T20:57:04Z created
- 2026-10-22T20:57:05Z set scope=['plugin/lib/fmplaybooks.py', 'plugin/lib/fmcli.py', 'plugin/skills/playbooks/SKILL.md', 'plugin/tests/test_playbook_machinery.py', 'CHANGELOG.md']
- 2026-10-22T20:57:06Z split from T-1524 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T20:57:07Z set depends_on=['T-1621']
- 2026-10-22T21:29:49Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_playbook_machinery.Verbs`
- 2026-10-22T21:30:13Z criterion 1 text: route names a playbook per stage; blame maps lines to tasks through git; preview lists checks — verify with python3 plugin/tests/run.py test_playbook_machinery.Verbs → route names a playbook per stage; blame maps lines to tasks through git; preview lists checks
- 2026-10-22T23:41:21Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1622.builder.md
- 2026-10-22T23:41:42Z focused
- 2026-10-23T01:49:30Z merged worktree-agent-ad3f7821a638f21a4 (6 file(s))
- 2026-10-23T01:49:31Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad3f7821a638f21a4
- 2026-10-23T01:49:45Z focused
- 2026-10-23T01:50:14Z scope: MASTER.md and plugin/skills/playbooks/SKILL.md name the new actions (CC plugin parity)
- 2026-10-23T01:51:08Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1524 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Playbook machinery: live project facts injected at load, inheritance and
- research brainstorm-skills-20261022: The cause is mostly structural. Claude Code skills trigger on user words, while Foreman's hooks and rules already hand the model the…
- T-1519 [FEATURE M, done, 4 steps] Brainstorm T-1479 round 2 (cluster 24): strict-by-default templates for web, 3D and fm cod — lesson: A check that runs user code in-pro…
- decision 2026-10-21: fm code's no-setup default picks only a runner whose read-only mode is verified here (claude); codex/gemini plan only when named, with a note
- the similar finished task took 4 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmplaybooks.py, plugin/skills/playbooks/SKILL.md, plugin/tests/test_playbook_machinery.py; re-ground the plan against them before editing
## Lessons
- git blame and log can run commands from a repo's own config (textconv, gpg): pass --no-textconv and keep them out of workers' reach
## Files touched
- plugin/tests/test_playbook_machinery.py
- plugin/lib/fmplaybooks.py
- plugin/lib/fmcli.py
- plugin/skills/playbooks/SKILL.md
- MASTER.md
- CHANGELOG.md
