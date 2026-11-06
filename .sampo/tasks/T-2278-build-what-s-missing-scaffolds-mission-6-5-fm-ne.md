---
id: T-2278
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T05:51:49Z
updated: 2026-10-31T06:26:18Z
base: db3db3bedec2ed4b1f8375b7ed6bb4f854886188
base_tree: 06209901d4b52716049fcc0c96581430f96dbaae
plan0_at: 2026-10-31T05:52:12Z
plan0_scope: []
verified: strong
---
# Build-what's-missing scaffolds (Mission 6, #5): fm new tool NAME (a stdlib script + its failing-first test) and fm new skill NAME (a project skill in the listing's format); the capability-miss note names fm new tool
## Raw request
> Build-what's-missing scaffolds (Mission 6, #5): fm new tool NAME (a stdlib script + its failing-first test) and fm new skill NAME (a project skill in the listing's format); the capability-miss note names fm new tool
## Interpretation
Gap map #5: 'build-test-use loop (3)' and 'skill new/script scaffold (3)'. When fm plugins find has nothing, building the missing tool is the other half of find-or-build, but nothing scaffolds a tool with its test or a project skill in the format the listing expects, so each build starts from nothing and often ships untested.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm new tool NAME [DIR] writes tools/NAME.py (argparse, --help, exit codes) and tests/test_NAME.py that fails until the tool does its job, and fm new check passes on it; fm new skill NAME writes .claude/skills/NAME/SKILL.md with frontmatter whose description starts 'Use whenever' under the per-skill cap; both refuse to overwrite; T-2270's note names fm new tool NAME; names are validated — verify with `python3 plugin/tests/run.py test_scaffold test_hooks`
## Non-goals
## Approach (options → choice → why)
1) two strict templates beside web/scene/panel in fm new: tool (tools/NAME.py with argparse, --help, exit codes 0/1/2, plus tests/test_NAME.py whose one test fails until the tool is written) and skill (.claude/skills/NAME/SKILL.md with 'Use whenever …' description under the 125-char cap and a body pointing at the verify step); fm new check validates them; T-2270's note says 'or build it: fm new tool NAME'. 2) generate the tool with a model — rejected: the build is the session's job; the scaffold makes the test exist first. 3) one generic template — rejected: a skill and a script have different contracts. Choice 1.
## Risks and rollback
Names are untrusted (they come from a failed command): [a-z0-9][a-z0-9_-]{0,40} only, never a path. Writes refuse to overwrite.
## Execution prompt
## Steps
1. [x] red tests: each template's files, the refusal to overwrite, a bad name refused, fm new check on the tool, the note text
2. [x] templates in plugin/templates and the fm new entries; the capability-miss note
3. [x] docs: MASTER fm new line, README, CHANGELOG
## Resume here
## Docs impact
MASTER.md, README.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_scaffold test_hooks` → exit 0 · Ran 228 tests in 84.4s (33 classes, 16 at a time; slowest: Stop 84s, NoTaskGate 49s, PreToolUse 43s) / OK [ran] [tree 3d1ef76510a8] (2026-10-31T05:56:43Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_away test_bench_family test_code_tui test_compact test_docs test_drive_side test_goal test_guard_evasions test_hooks test_library test_memory test_onwrite test_scaffold test_scene test_showpieces test_statusline_ui test_tool_taint && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [14.61s] [ran] [tree 3d1ef76510a8] (2026-10-31T05:59:55Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_away test_bench_family test_code_tui test_compact test_docs test_drive_side test_goal test_guard_evasions test_hooks test_library test_memory test_onwrite test_scaffold test_scene test_showpieces test_statusline_ui test_tool_taint && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [16.86s] [ran] [tree 3d1ef76510a8] (2026-10-31T06:00:17Z)
- (step 2) `python3 plugin/tests/run.py test_scaffold test_hooks test_docs 2>&1 | tail -6` → exit 0 · Ran 313 tests in 85.1s (54 classes, 16 at a time; slowest: Stop 84s, NoTaskGate 69s, PreToolUse 65s) / OK [ran] [tree 4c63ff88d608] (2026-10-31T06:15:04Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_away test_bench_family test_code_tui test_compact test_docs test_drive_side test_goal test_guard_evasions test_hooks test_library test_memory test_onwrite test_scaffold test_scene test_showpieces test_statusline_ui test_tool_taint && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [12.41s] [ran] [tree 4c63ff88d608] (2026-10-31T06:16:18Z)
- `python3 plugin/tests/run.py test_scaffold test_hooks test_docs` → ✗ exit 1 · Ran 314 tests in 35.9s (54 classes, 16 at a time; slowest: Stop 35s, NoTaskGate 24s, PreToolUse 19s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree 0c7e9aaa15fb] (2026-10-31T06:20:52Z)
- `python3 plugin/tests/run.py test_scaffold test_hooks test_docs` → exit 0 · Ran 314 tests in 35.0s (54 classes, 16 at a time; slowest: Stop 35s, NoTaskGate 24s, PreToolUse 19s) / OK [ran] [tree 0c7e9aaa15fb] (2026-10-31T06:20:52Z)
- (step 1) `python3 plugin/tests/run.py test_scaffold test_hooks test_docs` → exit 0 · Ran 314 tests in 35.0s (54 classes, 16 at a time; slowest: Stop 35s, NoTaskGate 24s, PreToolUse 19s) / OK [ran] [tree 0c7e9aaa15fb] (2026-10-31T06:21:27Z)
- (step 2) `python3 plugin/tests/run.py test_scaffold test_hooks test_docs` → exit 0 · Ran 314 tests in 35.0s (54 classes, 16 at a time; slowest: Stop 35s, NoTaskGate 24s, PreToolUse 19s) / OK [ran] [tree 0c7e9aaa15fb] (2026-10-31T06:22:02Z)
- (step 3) `python3 plugin/tests/run.py test_scaffold test_hooks test_docs` → exit 0 · Ran 314 tests in 35.0s (54 classes, 16 at a time; slowest: Stop 35s, NoTaskGate 24s, PreToolUse 19s) / OK [ran] [tree 0c7e9aaa15fb] (2026-10-31T06:22:38Z)
- (ac 1) `python3 plugin/tests/run.py test_scaffold test_hooks` → exit 0 · Ran 232 tests in 34.6s (33 classes, 16 at a time; slowest: Stop 34s, NoTaskGate 24s, PreToolUse 19s) / OK [ran] [tree 3d0c935f970f] (2026-10-31T06:25:10Z)
- (audit intent) `self + one fm-reviewer pass (2 medium: an unsandboxed tool check, an undo that left a file; 4 low; all fixed with tests)` → Mission 6's build half: a missing tool gets a scaffold whose test exists first, and a project skill in the listing's format (test_scaffold red-to-green) [tree 3d0c935f970f] (2026-10-31T06:25:10Z)
- (audit adversary) `self + one fm-reviewer pass (2 medium: an unsandboxed tool check, an undo that left a file; 4 low; all fixed with tests)` → fm new check runs a tool only with --run, through fmplaybooks._run (PATH-only env, temp HOME, limits, group kill); names validated, no stdlib names, no writes through a symlinked folder [tree 3d0c935f970f] (2026-10-31T06:25:10Z)
- (audit edge) `self + one fm-reviewer pass (2 medium: an unsandboxed tool check, an undo that left a file; 4 low; all fixed with tests)` → a half-written tool is undone whole; nothing overwritten; a quoted skill description survives a strict YAML parser [tree 3d0c935f970f] (2026-10-31T06:25:10Z)
## Log
- 2026-10-31T05:51:49Z created
- 2026-10-31T05:51:59Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2278.builder.md
- 2026-10-31T05:52:12Z focused
- 2026-10-31T06:17:11Z merged worktree-agent-a5c4d834ac659c205 (9 file(s))
- 2026-10-31T06:17:11Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a5c4d834ac659c205
- 2026-10-31T06:19:40Z focused
- 2026-10-31T06:23:03Z paused: focus moved to T-2277
- 2026-10-31T06:24:34Z focused
- 2026-10-31T06:24:35Z scope: plugin/lib/fmnew.py, plugin/lib/fmhooks.py (_capability_miss note), plugin/templates/scaffold/*.tmpl, plugin/tests/test_scaffold.py, plugin/tests/test_hooks.py, README.md, MASTER.md, CHANGELOG.md
- 2026-10-31T06:26:16Z done
- 2026-10-31T06:26:18Z committed 541838aa (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1397 [FEATURE M, done, 1 steps] Intake offer: fm code prints one line when an indexed skill matches the request (name, lic — lesson: Stack cards name tools (cargo) mor…
- T-2121 [FEATURE L, done, 2 steps] fm find: deterministic language-agnostic finders (untested, docs, deps, sql, slow, flaky, secrets, gates), zero on every clean render (…
- T-1838 [FEATURE M, done, 3 steps] Fm playbooks route: top-1 missed on 3 of 3 real task titles (e.g. a stop-hook bug → strate — lesson: bm25 in FTS5 scores 0 for a word i…
- decision 2026-10-31: While the Genesis tower waits on T-2221 (Mission 3's critique; the cold-read rule change is the user's steer-2 call, T-2246), build the gap map's Mi…
## Lessons
- A scaffold check that runs the scaffolded file is running untrusted code: reuse the sandboxed runner the other templates already use
## Files touched
- plugin/templates/scaffold/tool.py.tmpl
- plugin/templates/scaffold/tool_test.py.tmpl
- plugin/templates/scaffold/skill.md.tmpl
- plugin/tests/test_scaffold.py
- plugin/tests/test_hooks.py
- plugin/lib/fmnew.py
- plugin/lib/fmhooks.py
- MASTER.md
- README.md
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/lib/fmeco.py
- plugin/lib/fmfind.py
- plugin/lib/fmforesight.py
- plugin/lib/fmgraph.py
- plugin/lib/fmmcp.py
- plugin/lib/fmrecall.py
- plugin/lib/fmrepeats.py
- plugin/lib/fmtriggers.py
- plugin/tests/test_find.py
- plugin/tests/test_graph.py
- plugin/tests/test_mcp.py
- plugin/tests/test_triggers.py
