---
id: T-1608
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmdojo.py, plugin/lib/fmcli.py, plugin/tests/test_guard_hardening.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T20:38:52Z
updated: 2026-10-23T10:35:09Z
base: 633e4693e184f170b378730389247e8bd8103c1e
base_tree: 07bd5d100c2cd676f854c64a1bbfbbf9c01b4170
plan0_at: 2026-10-23T10:31:54Z
plan0_scope: [plugin/lib/fmdojo.py, plugin/lib/fmcli.py, plugin/tests/test_guard_hardening.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# Dangerous-command dojo for people: a short interactive drill of commands the guard refuses
## Raw request
> Dangerous-command dojo for people: a short interactive drill of commands the guard refuses and why (from T-1553, deferred: lowest value of its parts)
## Interpretation
fm dojo: a short drill for people of commands the guard refuses and why. Rounds come from the guard's labelled corpus (about half refused), seeded so a drill can be repeated; each asks allow or refuse, then shows the guard's live verdict (as fm replay judges, no grants) and the case's reason; a score at the end. Off a terminal or with --json, the drill prints as a study sheet with the answers; --quiz asks with answers on stdin.
## Assumptions (confidence)
## Acceptance criteria
- [x] a seeded drill mixes refused and allowed commands, each with its reason and the guard's live verdict agreeing; a quiz with right answers scores 4/4 and stops when input ends — verify with `python3 plugin/tests/run.py test_guard_hardening.Dojo`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests, then fmdojo and the verb
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard_hardening.Dojo` → ✗ exit 1 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Dojo 0s) / FAILED (1 classes) [ran] [tree 19ef0b5a02ea] (2026-10-23T10:32:01Z)
- (step 1) `python3 plugin/tests/run.py test_guard_hardening.Dojo test_docs` → exit 0 · Ran 71 tests in 9.3s (18 classes, 16 at a time; slowest: Fences 9s, TaskLifecycle 3s, Dojo 2s) / OK [ran] [tree a2ca3e4b9283] (2026-10-23T10:33:42Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_hardening.Dojo` → exit 0 · Ran 2 tests in 0.8s (1 classes, 16 at a time; slowest: Dojo 1s) / OK [ran] [tree a2ca3e4b9283] (2026-10-23T10:33:43Z)
- (audit edge) `self review; test_guard_hardening, test_docs and test_cli green; a seeded study sheet read by eye` → rounds 0 or over 40 refused; input that ends stops the quiz with the score so far; the corpus's T-ids are dropped from the reasons; cases are judged in their resolved folders as fm replay judges them (a relative cwd had raised in the guard) [tree a2ca3e4b9283] (2026-10-23T10:33:43Z)
- (audit self) `self review; test_guard_hardening, test_docs and test_cli green; a seeded study sheet read by eye` → no findings [tree a2ca3e4b9283] (2026-10-23T10:33:43Z)
- (audit edge) `self review; test_guard_hardening, test_docs and test_cli green; a seeded study sheet read by eye` → rounds 0 or over 40 refused; input that ends stops the quiz with the score so far; the corpus's T-ids are dropped from the reasons; cases are judged in their resolved folders as fm replay judges them (a relative cwd had raised in the guard) [tree a2ca3e4b9283] (2026-10-23T10:34:21Z)
- (audit adversary) `self review; test_guard_hardening, test_docs and test_cli green; a seeded study sheet read by eye` → the dojo only reads the labelled corpus and asks the guard for verdicts (fmreplay.verdicts, no grants, nothing run); the dangerous commands are printed through c.plain, never executed; the guard's own rules and corpus are unchanged [tree a2ca3e4b9283] (2026-10-23T10:34:21Z)
- (audit self) `self review; test_guard_hardening, test_docs and test_cli green; a seeded study sheet read by eye` → no findings [tree a2ca3e4b9283] (2026-10-23T10:34:21Z)
## Log
- 2026-10-22T20:38:52Z created
- 2026-10-23T10:20:34Z set scope=['plugin/lib/fmdojo.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_guard_hardening.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-23T10:31:53Z focused
- 2026-10-23T10:35:06Z done
- 2026-10-23T10:35:09Z committed cf757494 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1553 [SECURITY M, done, 3 steps] Guard oracle: a stub-exec run agrees with the guard's reading — lesson: A tool that runs things to check them must treat 'didn't run' …
- research T-1606-review: Verdict: changes needed.** The core works, but the note's "logs keep it redacted" claim is false on one path, and the report-and-file flow puts t…
- research brainstorm-20261016-round4: 195 ideas, 46 clusters, each grounded against plugin/lib, hooks, skills, workflows, mods/foreman-ui and CHANGELOG.md. Paths are rela…
- decision 2026-10-22: T-1585: the guard refuses commands that name CLAUDECODE or CLAUDE_CODE_ENTRYPOINT to unset or override them, not a whole fresh environment (env -i, …
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/tests/test_guard_hardening.py; re-ground the plan against them before editing
## Plan gaps
- failed first: step 1 failing tests, then fmdojo and the verb
## Files touched
- plugin/lib/fmdojo.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/tests/test_guard_hardening.py
