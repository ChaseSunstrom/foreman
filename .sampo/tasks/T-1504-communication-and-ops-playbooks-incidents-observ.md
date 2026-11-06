---
id: T-1504
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/playbooks/references, plugin/skills/playbooks/SKILL.md, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:16Z
updated: 2026-10-22T18:43:46Z
base: f210f73f4b817ce2eea17ae2b77faa4989fb8214
base_tree: b755e46e23ad37ca419ad4e4168f08ff609ab7a5
plan0_at: 2026-10-22T18:20:13Z
plan0_scope: [plugin/skills/playbooks/references]
verified: strong
---
# Communication and ops playbooks: incidents, observability, data-viz, docs, decks, scrollytelling, demos, sound
## Raw request
> Communication and ops playbooks: incidents, observability, data-viz, docs, decks, scrollytelling, demos, sound
## Interpretation
Brainstorm T-1479 cluster 10: incident (triage, mitigate, timeline, follow-ups), observability (logs, metrics, traces worth having), data-viz (form by job, colour by role, one axis), docs (task-first pages, examples that run), decks-and-reports, scrollytelling (step triggers, reduced motion), demo-production (scripted, seeded, short), sound-design (off by default, earcons, volume caps), stdlib-python (reach for the standard library first). Foreman's own original writing (no third-party text copied); every rule checkable (a reader can say pass or fail); link the library cards it builds on (fm lib show NAME); do not edit plugin/skills/playbooks/SKILL.md, put the one index line in your report.
## Assumptions (confidence)
## Acceptance criteria
- [x] the nine playbooks exist with a 'Use when' line and a numbered procedure — verify with `for f in ops/incident ops/observability ui/data-viz context/docs context/decks-and-reports ui/scrollytelling release/demo-production ui/sound-design lang/stdlib-python; do python3 -c "t=open('plugin/skills/playbooks/references/$f.md').read(); miss=[s for s in ['Use when','1.',] if s not in t]; assert not miss, miss" || exit 1; done`
## Non-goals
## Approach (options → choice → why)
Options: one communication playbook (mixes unrelated jobs); chosen: nine short original playbooks in their stages (ops/incident, ops/observability, ui/data-viz, context/docs, context/decks-and-reports, ui/scrollytelling, release/demo-production, ui/sound-design, lang/stdlib-python), each a Use-when line and a numbered procedure with checks; ui entries go in references/ui/INDEX.md, a new ops stage gets its own INDEX.md named once in SKILL.md.
## Risks and rollback
## Execution prompt
## Steps
1. [x] write the nine playbooks
## Resume here
## Docs impact
plugin/skills/playbooks/SKILL.md
## Verification evidence
- (step 1) `python3 -m unittest discover -s plugin/tests -p test_docs.py` → exit 0 · Ran 36 tests in 0.521s / OK [ran] [tree 8e94dcde085c] (2026-10-22T18:28:28Z)
- (step 1) `python3 .t1504/run_examples.py plugin/skills/playbooks/references/ops/observability.md plugin/skills/playbooks/references/context/docs.md` → exit 0 · (no output) [ran] [tree 8e94dcde085c] (2026-10-22T18:28:31Z)
- (step 1) `for f in ops/incident ops/observability ui/data-viz context/docs context/decks-and-reports ui/scrollytelling release/demo-production ui/sound-design lang/stdlib-python; do python3 -c "t=open('plugin/skills/playbooks/references/$f.md').read(); miss=[s for s in ['Use when','1.',] if s not in t]; assert not miss, miss" || exit 1; done` → exit 0 · (no output) [ran] [tree 8e94dcde085c] (2026-10-22T18:28:36Z)
- (step 1) `node .t1504/steps.test.mjs` → exit 0 · steps ok [ran] [tree 8e94dcde085c] (2026-10-22T18:28:39Z)
- (step 1) `python3 .t1504/sound_test.py` → exit 0 · sound ok [ran] [tree 8e94dcde085c] (2026-10-22T18:28:40Z)
- (step 1) `python3 .t1504/cards.py` → exit 0 · 54 missing: [] [ran] [tree 8e94dcde085c] (2026-10-22T18:28:40Z)
- (step 1) `python3 .t1504/runner_test.py` → exit 0 · runner ok 7 [ran] [tree 7143a866db19] (2026-10-22T18:42:30Z)
- (step 1) `node .t1504/steps.test.mjs` → exit 0 · steps ok [ran] [tree 7143a866db19] (2026-10-22T18:42:31Z)
- (step 1) `python3 .t1504/sound_test.py` → exit 0 · sound ok [ran] [tree 7143a866db19] (2026-10-22T18:42:31Z)
- (step 1) `python3 .t1504/run_examples.py plugin/skills/playbooks/references/ops/observability.md plugin/skills/playbooks/references/context/docs.md` → exit 0 · (no output) [ran] [tree 7143a866db19] (2026-10-22T18:42:32Z)
- (step 1) `python3 -m unittest discover -s plugin/tests -p test_docs.py` → exit 0 · Ran 36 tests in 0.828s / OK [ran] [tree 7143a866db19] (2026-10-22T18:42:33Z)
- (step 1) `for f in ops/incident ops/observability ui/data-viz context/docs context/decks-and-reports ui/scrollytelling release/demo-production ui/sound-design lang/stdlib-python; do python3 -c "t=open('plugin/skills/playbooks/references/$f.md').read(); miss=[s for s in ['Use when','1.',] if s not in t]; assert not miss, miss" || exit 1; done` → exit 0 · (no output) [ran] [tree 7143a866db19] (2026-10-22T18:42:38Z)
- (ac 1) `for f in ops/incident ops/observability ui/data-viz context/docs context/decks-and-reports ui/scrollytelling release/demo-production ui/sound-design lang/stdlib-python; do python3 -c "t=open('plugin/skills/playbooks/references/$f.md').read(); miss=[s for s in ['Use when','1.',] if s not in t]; assert not miss, miss" || exit 1; done` → exit 0 · (no output) [ran] [tree 3ea9e8f8c5f0] (2026-10-22T18:43:29Z)
- (step 1) `python3 plugin/tests/run.py test_docs test_doctor` → exit 0 · Ran 106 tests in 4.2s (31 classes, 16 at a time; slowest: Command 4s, TaskLifecycle 3s, ViewsRepair 3s) / OK [ran] [tree 3ea9e8f8c5f0] (2026-10-22T18:43:34Z)
- (ac 1) `for f in ops/incident ops/observability ui/data-viz context/docs context/decks-and-reports ui/scrollytelling release/demo-production ui/sound-design lang/stdlib-python; do python3 -c "t=open('plugin/skills/playbooks/references/$f.md').read(); miss=[s for s in ['Use when','1.',] if s not in t]; assert not miss, miss" || exit 1; done` → exit 0 · (no output) [ran] [tree c4ecb3673932] (2026-10-22T18:43:43Z)
- (audit intent) `one fm-reviewer pass: 1 HIGH (runner passed silent failures), 3 MEDIUM, 5 LOW, all fixed in 3aeab777 with a 7-case runner self-check` → nine playbooks with Use when and numbered procedures, reachable through stage INDEX.md files [tree c4ecb3673932] (2026-10-22T18:43:43Z)
- (audit adversary) `one fm-reviewer pass: 1 HIGH (runner passed silent failures), 3 MEDIUM, 5 LOW, all fixed in 3aeab777 with a 7-case runner self-check` → run_examples.py says trusted docs only, PATH-only env, stdin closed; incidents preserve evidence before rollback [tree c4ecb3673932] (2026-10-22T18:43:43Z)
- (audit edge) `one fm-reviewer pass: 1 HIGH (runner passed silent failures), 3 MEDIUM, 5 LOW, all fixed in 3aeab777 with a 7-case runner self-check` → cold #step-N deep link renders; sys.stdlib_module_names and tarfile filter version notes; sound check uses RMS spread too [tree c4ecb3673932] (2026-10-22T18:43:43Z)
- (audit maintainer) `one fm-reviewer pass: 1 HIGH (runner passed silent failures), 3 MEDIUM, 5 LOW, all fixed in 3aeab777 with a 7-case runner self-check` → test_docs and test_doctor pass; SKILL.md 9,830 of 10,000 chars [tree c4ecb3673932] (2026-10-22T18:43:43Z)
## Log
- 2026-10-22T17:36:16Z created
- 2026-10-22T18:19:57Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1504.builder.md
- 2026-10-22T18:20:13Z focused
- 2026-10-22T18:43:11Z merged worktree-agent-a763e54b4573998f4 (15 file(s))
- 2026-10-22T18:43:15Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a763e54b4573998f4
- 2026-10-22T18:43:17Z focused
- 2026-10-22T18:43:35Z set scope=['plugin/skills/playbooks/references', 'plugin/skills/playbooks/SKILL.md', 'CHANGELOG.md']
- 2026-10-22T18:43:35Z scope: SKILL.md names the new stage indexes (ops, context, release, lang); CHANGELOG line
- 2026-10-22T18:43:44Z done
- 2026-10-22T18:43:46Z committed d8b2e25c (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1493 [FEATURE S, done, 1 steps] Motion playbook: game feel with intensity caps — lesson: Asserts in an embedded snippet should check the playbook's table, not the snip…
- T-1489 [FEATURE M, done, 2 steps] UI playbook: type and colour — lesson: Embedded scripts in a playbook should be run by the writer against the playbook's own example; i…
- T-1500 [FEATURE S, done, 1 steps] UI playbook: visual QA with screenshots and receipts — lesson: A playbook that ships a script should be run against a clean and a broke…
- decision 2026-10-22: T-1422: dropped the plan reach lint (hosts/paths in a planner's plan → refuse). Two reviews (research T-1422-review, -review2) showed it either refu…
## Preflight
Changed in scope since this was planned (2026-10-22): plugin/skills/playbooks/references/build/INDEX.md, plugin/skills/playbooks/references/build/csharp-build.md, plugin/skills/playbooks/references/build/go-build.md, plugin/skills/playbooks/references/b…; re-ground the plan against them before editing
## Why not caught
the runner's self-check had only failures that print a traceback
## Lessons
- A runner that reports failure from stderr alone passes every silent crash: judge by exit status, show stderr as the reason
## Files touched
- plugin/skills/playbooks/references/ops/INDEX.md
- plugin/skills/playbooks/references/ops/incident.md
- plugin/skills/playbooks/references/ops/observability.md
- plugin/skills/playbooks/references/context/docs.md
- .t1504/extract.py
- .t1504/run_examples.py
- .t1504/bad.md
- plugin/skills/playbooks/references/ui/data-viz.md
- .t1504/src/charts/Two.jsx
- .t1504/src/charts/One.jsx
- .t1504/src/plot.py
- plugin/skills/playbooks/references/ui/scrollytelling.md
- .t1504/steps.test.mjs
- .t1504/steps.mjs
- plugin/skills/playbooks/references/ui/sound-design.md
- .t1504/sound_test.py
- .t1504/sound_check.py
- .t1504/wav/junk.wav
- .t1504/wav/long.wav
- .t1504/wav/loud.wav
- .t1504/wav/ok1.wav
- .t1504/wav/ok2.wav
- .t1504/wav/quiet.wav
- .t1504/wav/wide.wav
- plugin/skills/playbooks/references/context/decks-and-reports.md
- plugin/skills/playbooks/references/release/demo-production.md
- plugin/skills/playbooks/references/lang/stdlib-python.md
- plugin/skills/playbooks/references/ui/INDEX.md
- plugin/skills/playbooks/references/context/INDEX.md
- plugin/skills/playbooks/references/release/INDEX.md
