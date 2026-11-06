---
id: T-1554
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmnew.py, plugin/lib/fmcodemod.py, plugin/lib/fmcli.py, plugin/tests/test_scaffold.py, plugin/skills/playbooks/references/clean/deprecation.md, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:53Z
updated: 2026-10-23T16:45:55Z
inferred_deps: [T-1520]
inferred_why: T-1520: named in its request
group: round 3 creative and playbook extras
base: 0ef800461b4b9b1d689ebf2b5577b7c2a031072e
base_tree: 01877f74ff9709e58c9ffcb5c17610c1f6c14f98
plan0_at: 2026-10-23T16:40:30Z
plan0_scope: [plugin/lib/fmnew.py, plugin/lib/fmcodemod.py, plugin/lib/fmcli.py, plugin/tests/test_scaffold.py, plugin/skills/playbooks/references/clean/deprecation.md, CHANGELOG.md, MASTER.md]
verified: strong
---
# Round 3 (T-1520): Scaffolding and dev loop: fm new for projects born proven, fm dev as a w
## Raw request
> Round 3 (T-1520): Scaffolding and dev loop: fm new for projects born proven, fm dev as a watch loop for contributors, and an fm codemod family with migration playbooks (b070 b114 a171). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Scaffolding and dev loop: fm new NAME DIR in a new folder makes a project born proven (git init, fm init, the template's own check as its gate, a first commit, a passing fm check); fm dev, the contributor's watch loop running fm check --affected when a tracked file changes; fm codemod rename/sub, a mechanical rewrite across tracked text files previewed as a diff before --apply writes it, with the deprecation playbook saying when to use it.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm new web demo creates a project whose own check passes; fm codemod previews a rewrite before applying — verify with `cd plugin/tests && python3 -m unittest test_scaffold`
- [x] a new web project is born green; codemod previews then applies; fm dev --once runs the affected check — verify with `python3 plugin/tests/run.py test_scaffold`
## Non-goals
## Approach (options → choice → why)
Options for codemod: (a) an AST rewriter per language; (b) identifier-boundary rename and regex sub over git-tracked UTF-8 text files, preview first; (c) shelling out to sed. Choice: (b): language-neutral, stdlib, and the preview is the safety (a diff the user reads before --apply); binary, non-UTF-8, symlinked and large files are left alone. Born proven chains existing verbs (git init, fm init, fm check add, fm check) rather than new state; fm dev is a polling loop over git ls-files mtimes calling fm check --affected.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] fm new
3. [x] fm dev
4. [x] fm codemod
5. [x] red tests: born proven, codemod preview/apply, dev --once
6. [x] fmnew.born and cmd_dev, fmcodemod, the parsers, the deprecation playbook's step; CHANGELOG, MASTER
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md, ~/.claude/foreman/MASTER.md (fmcodemod module line; Scaffolding and dev loop), ~/.claude/foreman/plugin/skills/playbooks/references/clean/deprecation.md (step 1 points renames at fm codemod)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_scaffold` → ✗ exit 1 · Ran 5 tests in 0.6s (3 classes, 16 at a time; slowest: Dev 0s, Codemod 0s, Born 0s) / FAILED (3 classes) [ran] [tree 810baf6005f6] (2026-10-23T16:40:37Z)
- (step 1) `python3 plugin/tests/run.py test_scaffold test_playbook_check test_cli test_suite_hygiene test_docs` → exit 0 · Ran 236 tests in 25.5s (67 classes, 16 at a time; slowest: TaskLifecycle 25s, StateViews 10s, Fences 10s) / OK [ran] [tree c1813d933ea3] (2026-10-23T16:42:58Z)
- (step 2) `python3 plugin/tests/run.py test_scaffold test_playbook_check test_cli test_suite_hygiene test_docs` → exit 0 · Ran 236 tests in 26.3s (67 classes, 16 at a time; slowest: TaskLifecycle 26s, AuditPrep 11s, StateViews 11s) / OK [ran] [tree c1813d933ea3] (2026-10-23T16:43:25Z)
- (step 3) `python3 plugin/tests/run.py test_scaffold test_playbook_check test_cli test_suite_hygiene test_docs` → exit 0 · Ran 236 tests in 25.6s (67 classes, 16 at a time; slowest: TaskLifecycle 25s, Fences 10s, AuditPrep 10s) / OK [ran] [tree c1813d933ea3] (2026-10-23T16:43:51Z)
- (step 4) `python3 plugin/tests/run.py test_scaffold test_playbook_check test_cli test_suite_hygiene test_docs` → exit 0 · Ran 236 tests in 25.8s (67 classes, 16 at a time; slowest: TaskLifecycle 26s, Fences 10s, StateViews 10s) / OK [ran] [tree c1813d933ea3] (2026-10-23T16:44:18Z)
- (step 5) `python3 plugin/tests/run.py test_scaffold test_playbook_check test_cli test_suite_hygiene test_docs` → exit 0 · Ran 236 tests in 25.9s (67 classes, 16 at a time; slowest: TaskLifecycle 26s, Fences 10s, StateViews 10s) / OK [ran] [tree c1813d933ea3] (2026-10-23T16:44:44Z)
- (step 6) `python3 plugin/tests/run.py test_scaffold test_playbook_check test_cli test_suite_hygiene test_docs` → exit 0 · Ran 236 tests in 25.9s (67 classes, 16 at a time; slowest: TaskLifecycle 26s, AuditPrep 10s, Fences 10s) / OK [ran] [tree c1813d933ea3] (2026-10-23T16:45:11Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_scaffold` → exit 0 · Ran 5 tests in 1.573s / OK [ran] [tree c1813d933ea3] (2026-10-23T16:45:13Z)
- (ac 2) `python3 plugin/tests/run.py test_scaffold` → exit 0 · Ran 5 tests in 0.9s (3 classes, 16 at a time; slowest: Born 1s, Codemod 1s, Dev 0s) / OK [ran] [tree c1813d933ea3] (2026-10-23T16:45:15Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_scaffold` → exit 0 · Ran 5 tests in 1.572s / OK [ran] [tree c1813d933ea3] (2026-10-23T16:45:27Z)
- (ac 2) `python3 plugin/tests/run.py test_scaffold` → exit 0 · Ran 5 tests in 0.9s (3 classes, 16 at a time; slowest: Born 1s, Codemod 1s, Dev 0s) / OK [ran] [tree c1813d933ea3] (2026-10-23T16:45:27Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): born proven chains existing verbs in the new folder and reports each step, never failing the copy; codemod reads only git-tracked UTF-8 text files of 1 MB or less, previews by default and writes whole files with write_atomic only on --apply; fm dev polls tracked mtimes once a second and calls fm check --affected; help positions made unique after the registry test caught a clash` → fm new for projects born proven, fm dev as a contributor watch loop, an fm codemod family pointed at by the deprecation (migration) playbook, all fm verbs usable from Claude Code [tree c1813d933ea3] (2026-10-23T16:45:27Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): born proven chains existing verbs in the new folder and reports each step, never failing the copy; codemod reads only git-tracked UTF-8 text files of 1 MB or less, previews by default and writes whole files with write_atomic only on --apply; fm dev polls tracked mtimes once a second and calls fm check --affected; help positions made unique after the registry test caught a clash` → an existing folder only gets the file (no git init over someone's work); a commit with no git identity marks the first-commit step failed and the rest still run; a rename refuses anything but identifiers; a bad regex is a usage error; symlinks, binaries and non-UTF-8 files are skipped; paths narrow the rewrite [tree c1813d933ea3] (2026-10-23T16:45:27Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): born proven chains existing verbs in the new folder and reports each step, never failing the copy; codemod reads only git-tracked UTF-8 text files of 1 MB or less, previews by default and writes whole files with write_atomic only on --apply; fm dev polls tracked mtimes once a second and calls fm check --affected; help positions made unique after the registry test caught a clash` → codemod never follows a symlink out of the repo (skipped), writes only files git tracks inside the repo root, and an --apply is the user's explicit choice after a preview; born runs only git and this checkout's fm with fixed arguments in the folder it just created [tree c1813d933ea3] (2026-10-23T16:45:27Z)
## Log
- 2026-10-22T17:43:53Z created
- 2026-10-22T18:06:36Z set scope=['plugin/lib/fmcli.py', 'plugin/templates', 'plugin/tests/test_scaffold.py', 'CHANGELOG.md']
- 2026-10-23T16:40:27Z set tier=M, scope=['plugin/lib/fmnew.py', 'plugin/lib/fmcodemod.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_scaffold.py', 'plugin/skills/playbooks/references/clean/deprecation.md', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T16:40:29Z focused
- 2026-10-23T16:45:53Z done
- 2026-10-23T16:45:55Z committed 66e6b3da (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1523 [FEATURE M, done, 5 steps] Round 3 (T-1520): Playbooks drafted from finished runs and history: a draft from a proved — lesson: A brief is already a distilled tran…
- T-1553 [SECURITY M, done, 3 steps] Guard oracle: a stub-exec run agrees with the guard's reading — lesson: A tool that runs things to check them must treat 'didn't run' …
- T-1524 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Playbook machinery: live project facts injected at load, inheritance and
- decision 2026-10-22: T-1520: the user asked for every brainstorm idea and Claude Code plugin parity; the 206 skipped ideas became 35 round-3 tasks (T-1522..T-1556) and r…
- similar finished tasks took 3–5 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmnew.py, plugin/skills/playbooks/references/clean/deprecation.md; re-ground the plan against them before editing
## Lessons
- Make a scaffold prove itself at birth: chain the existing verbs (init, check add, check) instead of inventing a project state
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/lib/fmcli.py
- plugin/lib/fmnew.py
- plugin/lib/fmcodemod.py
- plugin/tests/test_scaffold.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/playbooks/references/clean/deprecation.md
