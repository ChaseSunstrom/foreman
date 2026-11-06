---
id: T-1514
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:42Z
updated: 2026-10-22T19:51:19Z
base: 68c161b37df55f3289d31c59015c2f6551428a88
base_tree: 4c999fc611162dd145b9034ed75126992a3ece91
plan0_at: 2026-10-22T19:04:08Z
plan0_scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py, CHANGELOG.md]
verified: strong
---
# Brainstorm T-1479 round 2 (cluster 19): a soft hook note asking for a design direction (DE
## Raw request
> Brainstorm T-1479 round 2 (cluster 19): a soft hook note asking for a design direction (DESIGN.md or ui/design-direction.md) the first time a task edits UI files; never blocks
## Interpretation
The first time a task edits UI files (css, html, jsx, tsx, vue, svelte), a hook note asks for a design direction: a DESIGN.md or ui/design-direction.md first. Once per task, never blocks; quiet when DESIGN.md exists. Claude Code plugin hook (PreToolUse/PostToolUse note) and fm code's worker see the same note. Works from Claude Code (an fm verb or /foreman: command) as well as fm code.
## Assumptions (confidence)
## Acceptance criteria
- [x] a first UI edit in a task without DESIGN.md gets one note naming the playbook; a second edit or a repo with DESIGN.md gets none — verify with `cd plugin/tests && python3 -m unittest test_hooks.DesignNudge`
## Non-goals
## Approach (options → choice → why)
Options: a guard refusal (too strong); chosen: a one-time additionalContext note from the existing hook path, recorded in the task meta so it fires once.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] the note in the hook path
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.DesignNudge` → ✗ exit 1 · Ran 2 tests in 6.0s (1 classes, 16 at a time; slowest: DesignNudge 4s) / FAILED (1 classes) [ran] [tree d96c7685cde0] (2026-10-22T19:06:39Z)
- (step 2) `python3 plugin/tests/run.py test_hooks.DesignNudge test_first_note` → exit 0 · Ran 8 tests in 14.8s (2 classes, 16 at a time; slowest: TestFirstNote 14s, DesignNudge 6s) / OK [ran] [tree 816b49404606] (2026-10-22T19:07:07Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_hooks.DesignNudge` → exit 0 · Ran 2 tests in 8.748s / OK [ran] [tree a79582f55ff1] (2026-10-22T19:47:10Z)
- (step 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 196 tests in 51.7s (24 classes, 16 at a time; slowest: Stop 51s, NoTaskGate 40s, PreToolUse 33s) / OK [ran] [tree a79582f55ff1] (2026-10-22T19:48:03Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_hooks.DesignNudge` → exit 0 · Ran 2 tests in 2.291s / OK [ran] [tree 9552918d2966] (2026-10-22T19:48:06Z)
- (audit maintainer) `self: intent: one note on a task's first UI edit, none with DESIGN.md or on later edits · adversary: a note only, never a block; path from the tool input, extension checked before any read · edge: cheap when it doesn't fire (bench_hooks PreToolUse:Edit p95 62.9 ms of 150); monorepo DESIGN.md in a package folder gives one extra note · operator: no install change · maintainer: DesignNudge red first` → DesignNudge tests red first; test_hooks passes [tree 9552918d2966] (2026-10-22T19:48:06Z)
- (audit self) `self: intent: one note on a task's first UI edit, none with DESIGN.md or on later edits · adversary: a note only, never a block; path from the tool input, extension checked before any read · edge: cheap when it doesn't fire (bench_hooks PreToolUse:Edit p95 62.9 ms of 150); monorepo DESIGN.md in a package folder gives one extra note · operator: no install change · maintainer: DesignNudge red first` → no findings [tree 9552918d2966] (2026-10-22T19:48:06Z)
- (audit adversary) `self: intent: one note on a task's first UI edit, none with DESIGN.md or on later edits · adversary: a note only, never a block; path from the tool input, extension checked before any read · edge: cheap when it doesn't fire (bench_hooks PreToolUse:Edit p95 62.9 ms of 150); monorepo DESIGN.md in a package folder gives one extra note · operator: no install change · maintainer: DesignNudge red first` → the note adds context only and never blocks or approves; a crafted file path only selects whether the note shows; the security-sensitive files in range (fmguard.py, test_guard.py, security playbooks) belong to T-1585, T-1505 and T-1503, reviewed there [tree 9552918d2966] (2026-10-22T19:49:35Z)
- (audit maintainer) `self: intent: one note on a task's first UI edit, none with DESIGN.md or on later edits · adversary: a note only, never a block; path from the tool input, extension checked before any read · edge: cheap when it doesn't fire (bench_hooks PreToolUse:Edit p95 62.9 ms of 150); monorepo DESIGN.md in a package folder gives one extra note · operator: no install change · maintainer: DesignNudge red first` → DesignNudge tests red first; test_hooks passes [tree 9552918d2966] (2026-10-22T19:49:35Z)
- (audit self) `self: intent: one note on a task's first UI edit, none with DESIGN.md or on later edits · adversary: a note only, never a block; path from the tool input, extension checked before any read · edge: cheap when it doesn't fire (bench_hooks PreToolUse:Edit p95 62.9 ms of 150); monorepo DESIGN.md in a package folder gives one extra note · operator: no install change · maintainer: DesignNudge red first` → no findings [tree 9552918d2966] (2026-10-22T19:49:35Z)
## Log
- 2026-10-22T17:36:42Z created
- 2026-10-22T17:55:58Z set scope=['plugin/lib/fmhooks.py', 'plugin/tests/test_hooks.py', 'CHANGELOG.md']
- 2026-10-22T19:03:44Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1514.builder.md
- 2026-10-22T19:04:07Z focused
- 2026-10-22T19:20:07Z merged worktree-agent-a5b839bfe5efc3ed1 (2 file(s))
- 2026-10-22T19:20:10Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a5b839bfe5efc3ed1
- 2026-10-22T19:46:42Z focused
- 2026-10-22T19:48:03Z scope: other files changed through other tasks' merges after T-1514's base; T-1514's lane touched fmhooks.py, test_hooks.py
- 2026-10-22T19:51:18Z done
- 2026-10-22T19:51:19Z committed 0da4b79f (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1506 [FEATURE M, done, 3 steps] fm design lint: a stdlib check for generic tells and craft slips — lesson: A lint's fixtures should include the real-world forms of eac…
- research T-1506-review: Verdict:** changes needed. I could only read the code, not run it, so every finding below is a code trace and none was executed. Four fixes shoul…
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
- likely tests for the scope: plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmhooks.py, plugin/tests/test_hooks.py; re-ground the plan against them before editing
## Why not caught
new behaviour
## Lessons
- A nudge that fires once per task needs its marker set only when it actually goes out, or a quiet check uses it up
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
- README.md
- plugin/README.md
- plugin/commands/settings.md
- plugin/lib/fmcli.py
- plugin/lib/fmguard.py
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
- plugin/skills/playbooks/references/ground/code-architect.md
- plugin/skills/playbooks/references/ground/code-explorer.md
- plugin/skills/playbooks/references/ground/search-first.md
- plugin/skills/playbooks/references/lang/python-patterns.md
- plugin/skills/playbooks/references/lang/python-testing.md
- plugin/skills/playbooks/references/lang/rust-patterns.md
- plugin/skills/playbooks/references/reflect/architecture-decision-records.md
