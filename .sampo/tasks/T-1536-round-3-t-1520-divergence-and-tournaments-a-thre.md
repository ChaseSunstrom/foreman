---
id: T-1536
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmtaste.py, plugin/lib/fmdesign.py, plugin/lib/fmcli.py, plugin/tests/test_taste_ledger.py, plugin/tests/test_design_diverge.py, plugin/commands/looks.md, plugin/skills/directions/SKILL.md, plugin/skills/directions/references/idioms.md, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:47Z
updated: 2026-10-23T15:49:10Z
inferred_deps: [T-1520]
inferred_why: T-1520: named in its request
group: round 3 creative and playbook extras
base: aa08d77b71eee0e5a7ed985eb47e88ebc8c9b2a9
base_tree: cd04b7d6d6019cc1ba0d74bd21238eed1abfca96
plan0_at: 2026-10-23T15:44:20Z
plan0_scope: [plugin/lib/fmtaste.py, plugin/lib/fmcli.py, plugin/tests/test_taste_ledger.py, plugin/commands/looks.md, plugin/skills/directions/SKILL.md, plugin/skills/directions/references/idioms.md, CHANGELOG.md, MASTER.md]
verified: strong
---
# Round 3 (T-1520): Divergence and tournaments: a three-variant round for UI tasks, a four-l
## Raw request
> Round 3 (T-1520): Divergence and tournaments: a three-variant round for UI tasks, a four-look tournament, a taste duel, opposite day, a lookbook of N directions, five historical idioms of one layout, and a blind multi-runner taste panel (a054 a086 a098 a159 a137 a048 c079 c077). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Divergence before a UI look converges: a taste duel and a four-look tournament the user answers (fm looks tournament, recorded in the taste ledger), opposite day (fm looks opposite LOOK), a lookbook of N directions (fm looks book), a three-variant round (the directions skill: three lanes) and five historical idioms of one layout (a directions reference). The blind multi-runner taste panel is left out (decided).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm design diverge 3 writes three variant briefs from distinct directions; a pick is recorded — verify with `cd plugin/tests && python3 -m unittest test_design_diverge`
- [x] tournament, opposite and book work and the skill and command offer them — verify with `python3 plugin/tests/run.py test_taste_ledger`
## Non-goals
## Approach (options → choice → why)
Options: (a) a new fm diverge verb family; (b) extend fm looks (the taste ledger already ranks looks and scores A-or-B picks) and the directions skill; (c) model-judged panels. Choice: (b): a tournament is calibration's A-or-B with a bracket, so its matches reuse the ledger's scoring; stateless (the cumulative answers replay the bracket), so Claude Code and fm code ask it the same way; (c) spends paid runs to guess what the user's own picks say.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] divergence and idioms
3. [x] duel and tournament page
4. [x] blind panel and opposite day
5. [x] red tests: tournament, opposite, book, the skill and command
6. [x] fmtaste bracket/opposite/book and the CLI; looks.md, directions SKILL.md and idioms.md; CHANGELOG, MASTER
## Resume here
## Docs impact
~/.claude/foreman/plugin/skills/directions/SKILL.md (diverge before you converge), ~/.claude/foreman/plugin/skills/directions/references/idioms.md (new), ~/.claude/foreman/plugin/commands/looks.md (tournament, opposite, book), ~/.claude/foreman/CHANGELOG.md, ~/.claude/foreman/MASTER.md (Divergence)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_taste_ledger test_design_diverge` → ✗ exit 1 · Ran 18 tests in 1.1s (7 classes, 16 at a time; slowest: Ledger 1s, Calibration 1s, Sources 0s) / FAILED (2 classes) [ran] [tree 5495ec914ab1] (2026-10-23T15:44:27Z)
- (step 1) `python3 plugin/tests/run.py test_taste_ledger test_design_diverge test_taste test_looks_gallery test_suite_hygiene test_cli` → exit 0 · Ran 169 tests in 23.5s (52 classes, 16 at a time; slowest: TaskLifecycle 23s, StateViews 9s, AuditPrep 9s) / OK [ran] [tree 44e2d628e9b4] (2026-10-23T15:45:37Z)
- (step 2) `python3 plugin/tests/run.py test_taste_ledger test_design_diverge test_taste test_looks_gallery test_suite_hygiene test_cli` → exit 0 · Ran 169 tests in 23.8s (52 classes, 16 at a time; slowest: TaskLifecycle 24s, StateViews 9s, AuditPrep 9s) / OK [ran] [tree 44e2d628e9b4] (2026-10-23T15:46:02Z)
- (step 3) `python3 plugin/tests/run.py test_taste_ledger test_design_diverge test_taste test_looks_gallery test_suite_hygiene test_cli` → exit 0 · Ran 169 tests in 23.6s (52 classes, 16 at a time; slowest: TaskLifecycle 23s, StateViews 9s, AuditPrep 9s) / OK [ran] [tree 44e2d628e9b4] (2026-10-23T15:46:26Z)
- (step 4) `python3 plugin/tests/run.py test_taste_ledger test_design_diverge test_taste test_looks_gallery test_suite_hygiene test_cli` → exit 0 · Ran 169 tests in 24.0s (52 classes, 16 at a time; slowest: TaskLifecycle 24s, AuditPrep 9s, StateViews 9s) / OK [ran] [tree 44e2d628e9b4] (2026-10-23T15:46:51Z)
- (step 5) `python3 plugin/tests/run.py test_taste_ledger test_design_diverge test_taste test_looks_gallery test_suite_hygiene test_cli` → exit 0 · Ran 169 tests in 23.5s (52 classes, 16 at a time; slowest: TaskLifecycle 23s, AuditPrep 9s, StateViews 9s) / OK [ran] [tree 44e2d628e9b4] (2026-10-23T15:47:15Z)
- (step 6) `python3 plugin/tests/run.py test_taste_ledger test_design_diverge test_taste test_looks_gallery test_suite_hygiene test_cli` → exit 0 · Ran 169 tests in 23.8s (52 classes, 16 at a time; slowest: TaskLifecycle 24s, StateViews 9s, AuditPrep 9s) / OK [ran] [tree 44e2d628e9b4] (2026-10-23T15:47:39Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_design_diverge` → exit 0 · Ran 2 tests in 0.456s / OK [ran] [tree 44e2d628e9b4] (2026-10-23T15:47:41Z)
- (ac 2) `python3 plugin/tests/run.py test_taste_ledger` → exit 0 · Ran 16 tests in 1.2s (6 classes, 16 at a time; slowest: Ledger 1s, Divergence 1s, Calibration 1s) / OK [ran] [tree 44e2d628e9b4] (2026-10-23T15:47:42Z)
- (step 6) `python3 plugin/tests/run.py test_taste_ledger test_design_diverge test_docs test_suite_hygiene test_cli` → exit 0 · Ran 214 tests in 23.2s (61 classes, 16 at a time; slowest: TaskLifecycle 23s, Fences 9s, StateViews 8s) / OK [ran] [tree 3dd82b2b1a67] (2026-10-23T15:48:41Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_design_diverge` → exit 0 · Ran 2 tests in 0.466s / OK [ran] [tree 3dd82b2b1a67] (2026-10-23T15:48:43Z)
- (ac 2) `python3 plugin/tests/run.py test_taste_ledger` → exit 0 · Ran 16 tests in 1.2s (6 classes, 16 at a time; slowest: Ledger 1s, Divergence 1s, Calibration 1s) / OK [ran] [tree 3dd82b2b1a67] (2026-10-23T15:48:43Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): a tournament is calibration's A-or-B with a bracket, stateless (cumulative answers replay it, the seeds printed in the continue command), recorded once at the champion and scored like calibration; opposite and diverge share one distance; tried opposite lido on the real cards (Shipping manifest, Night market, Observatory: plausible opposites); the lookbook page has no script and escapes every value` → duel and four-look tournament, opposite day, a lookbook, a three-variant round (fm design diverge) and five historical idioms, each from Claude Code (fm verbs, /foreman:looks, the directions skill); the blind panel left out by a recorded decision [tree 3dd82b2b1a67] (2026-10-23T15:48:43Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): a tournament is calibration's A-or-B with a bracket, stateless (cumulative answers replay it, the seeds printed in the continue command), recorded once at the champion and scored like calibration; opposite and diverge share one distance; tried opposite lido on the real cards (Shipping manifest, Night market, Observatory: plausible opposites); the lookbook page has no script and escapes every value` → a bracket needs 2, 4 or 8 different looks; answers past the last match, or anything but a/b, are refused; nothing is recorded until a champion, so an abandoned tournament leaves the ledger as it was; diverge takes 2-6 and pick needs a look; a look with no palette or tags gets the middle distance [tree 3dd82b2b1a67] (2026-10-23T15:48:43Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): a tournament is calibration's A-or-B with a bracket, stateless (cumulative answers replay it, the seeds printed in the continue command), recorded once at the champion and scored like calibration; opposite and diverge share one distance; tried opposite lido on the real cards (Shipping manifest, Night market, Observatory: plausible opposites); the lookbook page has no script and escapes every value` → the lookbook's titles, lines and tags come from the shipped cards and are HTML-escaped, its colours are parsed hex only; tournament seeds go through name_of, so a made-up look is refused; the /foreman:looks steps pass only answers a or b, which fm validates [tree 3dd82b2b1a67] (2026-10-23T15:48:43Z)
## Log
- 2026-10-22T17:43:47Z created
- 2026-10-22T17:58:28Z set scope=['plugin/lib/fmdesign.py', 'plugin/lib/fmcli.py', 'plugin/skills/directions/SKILL.md', 'plugin/tests/test_design_diverge.py', 'CHANGELOG.md']
- 2026-10-23T15:37:45Z set tier=M, scope=['plugin/lib/fmtaste.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_taste_ledger.py', 'plugin/commands/looks.md', 'plugin/skills/directions/SKILL.md', 'plugin/skills/directions/references/idioms.md', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T15:44:19Z focused
- 2026-10-23T15:44:26Z set scope=['plugin/lib/fmtaste.py', 'plugin/lib/fmdesign.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_taste_ledger.py', 'plugin/tests/test_design_diverge.py', 'plugin/commands/looks.md', 'plugin/skills/directions/SKILL.md', 'plugin/skills/directions/references/idioms.md', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T15:48:17Z scope: MASTER.md line 140 (T-1530's) held a literal triple backtick that the self-docs check read as an open fence; reworded
- 2026-10-23T15:49:08Z done
- 2026-10-23T15:49:10Z committed 3c3038c8 (10 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1523 [FEATURE M, done, 5 steps] Round 3 (T-1520): Playbooks drafted from finished runs and history: a draft from a proved — lesson: A brief is already a distilled tran…
- T-1553 [SECURITY M, done, 3 steps] Guard oracle: a stub-exec run agrees with the guard's reading — lesson: A tool that runs things to check them must treat 'didn't run' …
- T-1537 [FEATURE M, done, 4 steps] Round 3 (T-1520): Taste ledger: learn from what the user keeps and from 'not like that', a — lesson: Any score fed by a bulk input (a g…
- decision 2026-10-22: T-1520: the user asked for every brainstorm idea and Claude Code plugin parity; the 206 skipped ideas became 35 round-3 tasks (T-1522..T-1556) and r…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_taste.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/commands/looks.md, plugin/lib/fmcli.py, plugin/lib/fmtaste.py, plugin/skills/directions/SKILL.md, plugin/tests/test_taste_ledger.py; re-ground the plan against them before editing
## Lessons
- A preference round that's stateless (cumulative answers replay the bracket) works the same from a chat question flow and a terminal
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_taste_ledger.py
- plugin/tests/test_design_diverge.py
- CHANGELOG.md
- MASTER.md
- plugin/commands/looks.md
- plugin/lib/fmcli.py
- plugin/lib/fmdesign.py
- plugin/lib/fmtaste.py
- plugin/skills/directions/SKILL.md
- plugin/skills/directions/references/idioms.md
