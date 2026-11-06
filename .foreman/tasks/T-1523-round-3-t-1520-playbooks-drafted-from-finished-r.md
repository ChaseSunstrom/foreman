---
id: T-1523
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmplaybooks.py, plugin/lib/fmcli.py, plugin/tests/test_playbook_machinery.py, plugin/tests/test_playbook_draft.py, plugin/skills/playbooks/SKILL.md, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:43Z
updated: 2026-10-23T15:18:29Z
inferred_deps: [T-1520]
inferred_why: T-1520: named in its request
group: round 3 creative and playbook extras
base: 380c521f889e01a259782633a54c77fa9bf36fe5
base_tree: c6ab524dc17ebf8e52bee371fdcfe3f3c14e6ca8
plan0_at: 2026-10-23T15:09:46Z
plan0_scope: [plugin/lib/fmplaybooks.py, plugin/lib/fmcli.py, plugin/tests/test_playbook_machinery.py, plugin/skills/playbooks/SKILL.md, CHANGELOG.md, MASTER.md]
verified: strong
---
# Round 3 (T-1520): Playbooks drafted from finished runs and history: a draft from a proved
## Raw request
> Round 3 (T-1520): Playbooks drafted from finished runs and history: a draft from a proved task's transcript, recipes mined from the repo's git history, a counter-playbook of the repo's own failed fixes, and playbooks that re-rank their own steps from the session's failures (a082 a110 c156 b050 b054 c152). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Four fm playbooks verbs drafted from this repo's own work, all usable from Claude Code as fm verbs: draft ID (a done task's brief, the distilled transcript, as a draft in the library's shape), mine (files the history changes together), counter (reverted commits and tasks blocked or dropped with a reason), and show's re-rank: the steps the active task's failed runs point at, first. No model, browser or GPU needed.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm playbooks draft T-x writes a draft with Use-when, a numbered procedure and its source task; fm playbooks mine lists repeated fix patterns from git history — verify with `cd plugin/tests && python3 -m unittest test_playbook_draft`
- [x] draft, mine, counter and show's look-first block work as specified — verify with `python3 plugin/tests/run.py test_playbook_machinery`
## Non-goals
## Approach (options → choice → why)
Options: (a) parse session transcripts for the draft; (b) the brief (steps, run evidence, criteria, lessons, plan gaps), already the distilled transcript; (c) a model summarising the transcript. Choice: (b), deterministic and free; transcripts add noise the brief already filtered. Mine: per-file co-change shares over the last 400 non-merge commits, sweeps skipped (vs association-rule mining: more code, same answer here). Counter: git's revert line plus block/drop log reasons. Re-rank: a 'Look here first' block above the playbook (vs reordering its numbered steps, which would break the numbering the text refers to), by shared words with failed runs.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] draft from a task
3. [x] mine history and the counter-playbook
4. [x] red tests: draft, mine, counter, look-first
5. [x] fmplaybooks draft/mine/counter/look_first, the CLI choices, SKILL.md, CHANGELOG, MASTER
## Resume here
## Docs impact
~/.claude/foreman/plugin/skills/playbooks/SKILL.md (the verbs), ~/.claude/foreman/CHANGELOG.md, ~/.claude/foreman/MASTER.md (Playbooks from this repo's own work)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_playbook_machinery` → ✗ exit 1 · Ran 29 tests in 4.6s (6 classes, 16 at a time; slowest: Load 4s, FromThisRepo 3s, Verbs 3s) / FAILED (1 classes) [ran] [tree b032679b63a7] (2026-10-23T15:09:52Z)
- (step 1) `python3 plugin/tests/run.py test_playbook_machinery test_suite_hygiene test_cli` → exit 0 · Ran 156 tests in 23.3s (45 classes, 16 at a time; slowest: TaskLifecycle 23s, StateViews 8s, AuditPrep 8s) / OK [ran] [tree a7885543872d] (2026-10-23T15:11:55Z)
- (step 2) `python3 plugin/tests/run.py test_playbook_machinery test_suite_hygiene test_cli` → exit 0 · Ran 156 tests in 23.3s (45 classes, 16 at a time; slowest: TaskLifecycle 23s, StateViews 8s, AuditPrep 8s) / OK [ran] [tree a7885543872d] (2026-10-23T15:12:19Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_machinery` → exit 0 · Ran 29 tests in 4.0s (6 classes, 16 at a time; slowest: Load 4s, FromThisRepo 2s, Verbs 2s) / OK [ran] [tree a7885543872d] (2026-10-23T15:12:24Z)
- (step 3) `python3 plugin/tests/run.py test_playbook_machinery test_suite_hygiene test_cli` → exit 0 · Ran 156 tests in 23.2s (45 classes, 16 at a time; slowest: TaskLifecycle 23s, StateViews 8s, AuditPrep 8s) / OK [ran] [tree a7885543872d] (2026-10-23T15:12:59Z)
- (step 4) `python3 plugin/tests/run.py test_playbook_machinery test_suite_hygiene test_cli` → exit 0 · Ran 156 tests in 23.4s (45 classes, 16 at a time; slowest: TaskLifecycle 23s, StateViews 9s, AuditPrep 8s) / OK [ran] [tree a7885543872d] (2026-10-23T15:13:23Z)
- (step 5) `python3 plugin/tests/run.py test_playbook_machinery test_suite_hygiene test_cli` → exit 0 · Ran 156 tests in 23.1s (45 classes, 16 at a time; slowest: TaskLifecycle 23s, StateViews 8s, AuditPrep 8s) / OK [ran] [tree a7885543872d] (2026-10-23T15:13:47Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_playbook_draft` → ✗ exit 1 (never ran: no test_playbook_draft) · Ran 1 test in 0.000s / FAILED (errors=1) [ran] [tree a7885543872d] (2026-10-23T15:13:52Z)
- (ac 2) `python3 plugin/tests/run.py test_playbook_machinery` → exit 0 · Ran 29 tests in 3.9s (6 classes, 16 at a time; slowest: Load 4s, FromThisRepo 2s, Verbs 2s) / OK [ran] [tree a7885543872d] (2026-10-23T15:13:52Z)
- (step 1) `python3 plugin/tests/run.py test_playbook_machinery test_playbook_draft test_suite_hygiene test_cli` → exit 0 · Ran 156 tests in 41.8s (45 classes, 16 at a time; slowest: TaskLifecycle 42s, AuditPrep 19s, StateViews 19s) / OK [ran] [tree d42d751139a4] (2026-10-23T15:15:33Z)
- (step 2) `python3 plugin/tests/run.py test_playbook_machinery test_playbook_draft test_suite_hygiene test_cli` → exit 0 · Ran 156 tests in 41.9s (45 classes, 16 at a time; slowest: TaskLifecycle 42s, AuditPrep 19s, StateViews 18s) / OK [ran] [tree d42d751139a4] (2026-10-23T15:16:15Z)
- (step 3) `python3 plugin/tests/run.py test_playbook_machinery test_playbook_draft test_suite_hygiene test_cli` → exit 0 · Ran 156 tests in 36.3s (45 classes, 16 at a time; slowest: TaskLifecycle 36s, AuditPrep 17s, StateViews 17s) / OK [ran] [tree d42d751139a4] (2026-10-23T15:16:52Z)
- (step 4) `python3 plugin/tests/run.py test_playbook_machinery test_playbook_draft test_suite_hygiene test_cli` → exit 0 · Ran 156 tests in 27.2s (45 classes, 16 at a time; slowest: TaskLifecycle 27s, AuditPrep 12s, StateViews 12s) / OK [ran] [tree d42d751139a4] (2026-10-23T15:17:20Z)
- (step 5) `python3 plugin/tests/run.py test_playbook_machinery test_playbook_draft test_suite_hygiene test_cli` → exit 0 · Ran 156 tests in 24.3s (45 classes, 16 at a time; slowest: TaskLifecycle 24s, AuditPrep 10s, StateViews 10s) / OK [ran] [tree d42d751139a4] (2026-10-23T15:17:45Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_playbook_draft` → exit 0 · Ran 4 tests in 2.369s / OK [ran] [tree d42d751139a4] (2026-10-23T15:17:48Z)
- (ac 2) `python3 plugin/tests/run.py test_playbook_machinery test_playbook_draft` → exit 0 · Ran 29 tests in 3.9s (6 classes, 16 at a time; slowest: Load 4s, FromThisRepo 2s, Verbs 2s) / OK [ran] [tree d42d751139a4] (2026-10-23T15:17:52Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_playbook_draft` → exit 0 · Ran 4 tests in 2.344s / OK [ran] [tree d42d751139a4] (2026-10-23T15:18:02Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): draft reads a done brief only; mine and counter run git log through fmcore's one runner (no filters, GIT_* stripped) with fixed arguments; the look-first block shows the playbook's own lines and plain words from the active task's failed runs; tried on this repo: mine names fmcodetui/test_code_tui at 84-98%, counter lists blocked tasks with reasons, draft T-1377 gives a numbered procedure with its proving commands` → the four parts the request named — a draft from a proved task, recipes from history, a counter-playbook of failures, playbooks re-ranked by the session's failures — each an fm verb usable from Claude Code [tree d42d751139a4] (2026-10-23T15:18:02Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): draft reads a done brief only; mine and counter run git log through fmcore's one runner (no filters, GIT_* stripped) with fixed arguments; the look-first block shows the playbook's own lines and plain words from the active task's failed runs; tried on this repo: mine names fmcodetui/test_code_tui at 84-98%, counter lists blocked tasks with reasons, draft T-1377 gives a numbered procedure with its proving commands` → no git repo → a usage error; a done task with only typed evidence drafts steps without 'proved by'; sweeps of 30+ files are skipped so a rename-all commit doesn't pair everything; dropped tasks are left out of counter (mostly duplicates); a playbook's restarted numbering repeats n in look-first, which is shown as written [tree d42d751139a4] (2026-10-23T15:18:02Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): draft reads a done brief only; mine and counter run git log through fmcore's one runner (no filters, GIT_* stripped) with fixed arguments; the look-first block shows the playbook's own lines and plain words from the active task's failed runs; tried on this repo: mine names fmcodetui/test_code_tui at 84-98%, counter lists blocked tasks with reasons, draft T-1377 gives a numbered procedure with its proving commands` → the words lifted from failed runs into the look-first block are [a-z0-9_] tokens only and the lines shown are the playbook's own, so a run's output can't inject text into a loaded playbook; git gets no user-controlled option (counter's grep and mine's count are constants) [tree d42d751139a4] (2026-10-23T15:18:02Z)
## Log
- 2026-10-22T17:43:43Z created
- 2026-10-22T17:57:48Z set scope=['plugin/lib/fmplaybooks.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_playbook_draft.py', 'CHANGELOG.md']
- 2026-10-23T14:58:24Z set tier=M, scope=['plugin/lib/fmplaybooks.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_playbook_machinery.py', 'plugin/skills/playbooks/SKILL.md', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T15:09:45Z focused
- 2026-10-23T15:14:28Z set scope=['plugin/lib/fmplaybooks.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_playbook_machinery.py', 'plugin/tests/test_playbook_draft.py', 'plugin/skills/playbooks/SKILL.md', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T15:18:27Z done
- 2026-10-23T15:18:29Z committed a7058fa3 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1553 [SECURITY M, done, 3 steps] Guard oracle: a stub-exec run agrees with the guard's reading — lesson: A tool that runs things to check them must treat 'didn't run' …
- T-1539 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Looks gallery: a look book of one-file living specimens with 3-second po
- T-1542 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): 3D showpieces with the 3D playbook: the repo as a 3D city in fm page, ta
- decision 2026-10-22: T-1520: the user asked for every brainstorm idea and Claude Code plugin parity; the 206 skipped ideas became 35 round-3 tasks (T-1522..T-1556) and r…
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmplaybooks.py, plugin/skills/playbooks/SKILL.md, plugin/tests/test_playbook_machinery.py; re-ground the plan against them before editing
## Lessons
- A brief is already a distilled transcript: steps, the commands that proved them and the lessons are the playbook draft; no transcript parsing needed
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_playbook_machinery.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmplaybooks.py
- plugin/skills/playbooks/SKILL.md
- plugin/tests/test_playbook_draft.py
