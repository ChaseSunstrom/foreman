---
id: T-1043
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcost.py, plugin/lib/fmcli.py, plugin/tests/test_export.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-16T03:42:07Z
updated: 2026-10-16T08:28:43Z
base: 8dda9ee13fbd40f72c942eabfd8bc4f7f8f90c82
base_tree: 4d419ef7d24821fa3fa2f85974212400aba103e9
plan0_at: 2026-10-16T08:12:42Z
plan0_scope: [plugin/lib/fmcost.py, plugin/lib/fmcli.py, plugin/tests/test_export.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# Export the learned brain to Cursor (.cursor/rules) and Gemini (GEMINI.md), and include kno
## Raw request
> Export the learned brain to Cursor (.cursor/rules) and Gemini (GEMINI.md), and include known fixes in fm export agents (T-1029 C4)
## Interpretation
fm export writes AGENTS.md only. Add 'cursor' (.cursor/rules/foreman.mdc, Cursor's project-rule format with frontmatter description + alwaysApply: true) and 'gemini' (GEMINI.md at the root) targets with the same body, and a 'Known fixes' section (trusted fixes only, from fmfixes.known, redacted and defanged, bounded) in every target.
## Assumptions (confidence)
## Acceptance criteria
- [x] `fm export cursor|gemini` write their files with the mark, corrections and a "Known fixes" section — verify with `python3 plugin/tests/run.py test_fixes test_cli`
- [x] fm export cursor writes .cursor/rules/foreman.mdc with frontmatter (alwaysApply: true) and fm export gemini writes GEMINI.md, each with the AGENTS.md body, and refuse to replace a file they didn't write without --force — verify with `python3 plugin/tests/run.py test_export`
- [x] every export target has a Known fixes section listing only trusted fixes (an untrusted repo fix never appears), none in a sensitive project — verify with `python3 plugin/tests/run.py test_export`
## Non-goals
## Approach (options → choice → why)
Options: (a) one body builder agents_md(p) reused with a per-target header — chosen, smallest; (b) separate renderers per tool — duplicate; (c) symlinks to AGENTS.md — Cursor needs .mdc frontmatter, symlinks break on Windows. Each target keeps its own mark so a hand-written GEMINI.md or .mdc is never overwritten without --force; .cursor/rules is created; all the existing path checks (inside the project, not .git/.claude, no symlink) apply.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (plugin/tests/test_export.py): after `fm fix add "boom" --do "retry"`, `fm export agents` contains "Known fixes" and "boom"; `export cursor` creates `.cursor/rules/foreman.mdc` starting with "---" and alwaysApply: true; `export gemini` creates GEMINI.md; a non-fm-written file is refused without `--force`; a repo-sourced untrusted fix is left out; a sensitive project lists no fixes.
2. [x] In `agents_md(p, target="agents")` add the fixes section from `fmfixes.known(p)` (trusted only, redacted, defanged, ≤15) and the front matter for cursor; extend `choices` and `cmd_export`'s default path; MASTER.md and CHANGELOG lines.
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_export` → exit 0 · Ran 9 tests in 2.0s (3 classes, 16 at a time; slowest: Export 2s, Sync 1s, SessionStart 0s) / OK [ran] [tree 280cc615a964] (2026-10-16T08:13:58Z)
- (step 2) `python3 plugin/tests/run.py test_export test_fixes test_cli test_handoff` → exit 0 · Ran 132 tests in 22.0s (35 classes, 16 at a time; slowest: TaskLifecycle 22s, StateViews 9s, AuditPrep 8s) / OK [ran] [tree 280cc615a964] (2026-10-16T08:14:20Z)
- (step 1) `python3 plugin/tests/run.py test_export test_fixes test_cli test_handoff` → exit 0 · Ran 132 tests in 41.3s (35 classes, 16 at a time; slowest: TaskLifecycle 41s, StateViews 18s, AuditPrep 15s) / OK [ran] [tree 4f4411ec1a61] (2026-10-16T08:26:02Z)
- (ac 1) `python3 plugin/tests/run.py test_fixes test_cli` → exit 0 · Ran 114 tests in 45.2s (29 classes, 16 at a time; slowest: TaskLifecycle 45s, StateViews 20s, AuditPrep 17s) / OK [ran] [tree 8f9858f26094] (2026-10-16T08:27:11Z)
- (ac 2) `python3 plugin/tests/run.py test_export` → exit 0 · Ran 9 tests in 7.0s (3 classes, 16 at a time; slowest: Export 7s, Sync 3s, SessionStart 0s) / OK [ran] [tree 8f9858f26094] (2026-10-16T08:27:11Z)
- (ac 3) `python3 plugin/tests/run.py test_export` → exit 0 · Ran 9 tests in 7.0s (3 classes, 16 at a time; slowest: Export 7s, Sync 3s, SessionStart 0s) / OK [ran] [tree 8f9858f26094] (2026-10-16T08:27:11Z)
- (audit intent) `self review of the diff: targets share agents_md with a per-target mark and the Cursor front matter; the existing path checks (inside the project via realpath, not under .git/.claude, no symlink) apply to .cursor/rules too (a symlinked .cursor resolves outside and is refused); only trusted fixes are exported (a repo-only fix is a hint), defanged and redacted; a sensitive project exports none` → Cursor and Gemini get the same brain as AGENTS.md, plus known fixes [tree 8f9858f26094] (2026-10-16T08:27:11Z)
- (audit adversary) `self review of the diff: targets share agents_md with a per-target mark and the Cursor front matter; the existing path checks (inside the project via realpath, not under .git/.claude, no symlink) apply to .cursor/rules too (a symlinked .cursor resolves outside and is refused); only trusted fixes are exported (a repo-only fix is a hint), defanged and redacted; a sensitive project exports none` → a repo's own untrusted fix text never reaches an exported instruction file [tree 8f9858f26094] (2026-10-16T08:27:11Z)
- (audit edge) `self review of the diff: targets share agents_md with a per-target mark and the Cursor front matter; the existing path checks (inside the project via realpath, not under .git/.claude, no symlink) apply to .cursor/rules too (a symlinked .cursor resolves outside and is refused); only trusted fixes are exported (a repo-only fix is a hint), defanged and redacted; a sensitive project exports none` → hand-written GEMINI.md/.mdc refused without --force; missing .cursor/rules created [tree 8f9858f26094] (2026-10-16T08:27:11Z)
- (audit operator) `self review of the diff: targets share agents_md with a per-target mark and the Cursor front matter; the existing path checks (inside the project via realpath, not under .git/.claude, no symlink) apply to .cursor/rules too (a symlinked .cursor resolves outside and is refused); only trusted fixes are exported (a repo-only fix is a hint), defanged and redacted; a sensitive project exports none` → one verb, three targets [tree 8f9858f26094] (2026-10-16T08:27:11Z)
- (audit maintainer) `self review of the diff: targets share agents_md with a per-target mark and the Cursor front matter; the existing path checks (inside the project via realpath, not under .git/.claude, no symlink) apply to .cursor/rules too (a symlinked .cursor resolves outside and is refused); only trusted fixes are exported (a repo-only fix is a hint), defanged and redacted; a sensitive project exports none` → EXPORTS table, one body builder [tree 8f9858f26094] (2026-10-16T08:27:11Z)
## Log
- 2026-10-16T03:42:07Z created
- 2026-10-16T04:22:54Z set scope=['plugin/lib/fmcost.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_fixes.py']
- 2026-10-16T04:22:54Z set tier=M
- 2026-10-16T07:52:45Z set scope=['plugin/lib/fmcost.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_export.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-16T08:12:30Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1043.builder.md
- 2026-10-16T08:12:41Z focused
- 2026-10-16T08:25:16Z merged worktree-agent-adab34b63de0dca87 (4 file(s))
- 2026-10-16T08:25:19Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-adab34b63de0dca87
- 2026-10-16T08:25:20Z focused
- 2026-10-16T08:26:12Z scope: CHANGELOG.md — release note
- 2026-10-16T08:28:42Z done
- 2026-10-16T08:28:43Z committed b85fed8 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research wave1-plan-a4e57ddf98089606d: === T-1074 [stale: plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py changed since it was written]
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- T-0263 [FEATURE M, done, 4 steps] Handoff: diff tour, proof sections in fm pr, AGENTS.md export — lesson: Anything written for other people or tools (AGENTS.md, PR bodie…
- decision 2026-10-16: Recommendation: build the slate T-1042..T-1053 plus T-1028 widened (recorded in research brainstorm-20261016-catalogue); the user then asked for eve…
- similar finished tasks took 4–6 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-16): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcost.py, plugin/tests/test_export.py; re-ground the plan against them before editing
## Lessons
- Exports of learned state carry only what this machine trusts; hints stay local
## Files touched
- plugin/tests/test_export.py
- plugin/lib/fmcli.py
- plugin/lib/fmcost.py
- MASTER.md
- CHANGELOG.md
