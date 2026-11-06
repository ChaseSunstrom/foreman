---
id: T-1525
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmplaybooks.py, plugin/lib/fmcli.py, plugin/tests/test_playbook_draft.py, plugin/tests/test_docs.py, plugin/skills/playbooks/SKILL.md, site/pages.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:44Z
updated: 2026-10-23T15:24:53Z
inferred_deps: [T-1520]
inferred_why: T-1520: named in its request
group: round 3 creative and playbook extras
base: a7058fa326873056efceaf831fd39bab6b58ffb8
base_tree: d42d751139a4481a97f2640ad90de281ca96486d
plan0_at: 2026-10-23T15:18:37Z
plan0_scope: [plugin/lib/fmplaybooks.py, plugin/lib/fmcli.py, plugin/tests/test_playbook_draft.py, plugin/tests/test_docs.py, plugin/skills/playbooks/SKILL.md, site/pages.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Round 3 (T-1520): Learning from playbooks: lessons, katas and a dojo that score a run agai
## Raw request
> Round 3 (T-1520): Learning from playbooks: lessons, katas and a dojo that score a run against a playbook, a five-minute lesson from a diff at the user's level, 'borrow from' analogy cards per craft playbook, and a browsable field guide on the site with live exemplars (b028 b053 b055 c154 c129 c157). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Learning from playbooks: a dojo (score NAME --task ID: which steps a run followed), katas (kata NAME: the held-out briefs as practice, --answer FILE scored by their checks), a five-minute lesson from a diff (lesson [RANGE]: commits, folders, what their tasks learned, the checklists to read it with) and a field-guide page on the site (every playbook by stage with its Use-when line). Analogy cards and live exemplars are left out (decided).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm playbooks lesson prints exercises with checks for a playbook; the site builds a field-guide page — verify with `python3 plugin/tests/run.py test_playbook_draft`
- [x] score, kata and lesson work as specified — verify with `python3 plugin/tests/run.py test_playbook_draft`
- [x] the site's Playbooks page lists every playbook by stage — verify with `python3 plugin/tests/run.py test_docs`
## Non-goals
## Approach (options → choice → why)
Options: (a) model-written lessons and scoring; (b) deterministic word overlap and the eval sets' own checks; (c) a separate fm learn verb family. Choice: (b) inside fm playbooks: no model, reuses passes(), load_briefs(), REVIEW_BY_EXT and T-1523's _sharing. The field guide is read from the library at site build, so it can't drift.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] lessons and katas
3. [x] field guide page
4. [x] red tests: score, kata, lesson, the field guide
5. [x] fmplaybooks score/kata/lesson, CLI, site page, SKILL.md, CHANGELOG, MASTER
## Resume here
## Docs impact
~/.claude/foreman/plugin/skills/playbooks/SKILL.md (score, kata, lesson), ~/.claude/foreman/site/pages.py (the Playbooks field guide page), ~/.claude/foreman/CHANGELOG.md, ~/.claude/foreman/MASTER.md (Learning from playbooks)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_playbook_draft test_docs` → ✗ exit 1 · Ran 79 tests in 8.5s (19 classes, 16 at a time; slowest: Fences 8s, FromThisRepo 3s, TaskLifecycle 1s) / FAILED (2 classes) [ran] [tree b7441e04a00e] (2026-10-23T15:18:47Z)
- (step 1) `python3 plugin/tests/run.py test_playbook_draft test_docs test_playbook_machinery test_suite_hygiene test_cli` → exit 0 · Ran 228 tests in 25.4s (60 classes, 16 at a time; slowest: TaskLifecycle 25s, StateViews 10s, AuditPrep 10s) / OK [ran] [tree 703e3997dde2] (2026-10-23T15:20:22Z)
- (step 2) `python3 plugin/tests/run.py test_playbook_draft test_docs test_playbook_machinery test_suite_hygiene test_cli` → exit 0 · Ran 228 tests in 26.4s (60 classes, 16 at a time; slowest: TaskLifecycle 26s, StateViews 11s, AuditPrep 11s) / OK [ran] [tree 703e3997dde2] (2026-10-23T15:20:49Z)
- (step 3) `python3 plugin/tests/run.py test_playbook_draft test_docs test_playbook_machinery test_suite_hygiene test_cli` → exit 0 · Ran 228 tests in 24.9s (60 classes, 16 at a time; slowest: TaskLifecycle 25s, AuditPrep 10s, StateViews 10s) / OK [ran] [tree 703e3997dde2] (2026-10-23T15:21:15Z)
- (step 4) `python3 plugin/tests/run.py test_playbook_draft test_docs test_playbook_machinery test_suite_hygiene test_cli` → exit 0 · Ran 228 tests in 24.8s (60 classes, 16 at a time; slowest: TaskLifecycle 25s, StateViews 10s, AuditPrep 10s) / OK [ran] [tree 703e3997dde2] (2026-10-23T15:21:41Z)
- (step 5) `python3 plugin/tests/run.py test_playbook_draft test_docs test_playbook_machinery test_suite_hygiene test_cli` → exit 0 · Ran 228 tests in 25.0s (60 classes, 16 at a time; slowest: TaskLifecycle 25s, AuditPrep 10s, StateViews 10s) / OK [ran] [tree 703e3997dde2] (2026-10-23T15:22:06Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_draft` → exit 0 · Ran 7 tests in 3.8s (1 classes, 16 at a time; slowest: FromThisRepo 4s) / OK [ran] [tree 703e3997dde2] (2026-10-23T15:22:23Z)
- (ac 2) `python3 plugin/tests/run.py test_playbook_draft` → exit 0 · Ran 7 tests in 3.8s (1 classes, 16 at a time; slowest: FromThisRepo 4s) / OK [ran] [tree 703e3997dde2] (2026-10-23T15:22:27Z)
- (ac 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 72 tests in 8.6s (18 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 703e3997dde2] (2026-10-23T15:22:36Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_draft` → exit 0 · Ran 7 tests in 3.8s (1 classes, 16 at a time; slowest: FromThisRepo 4s) / OK [ran] [tree 703e3997dde2] (2026-10-23T15:22:50Z)
- (ac 2) `python3 plugin/tests/run.py test_playbook_draft` → exit 0 · Ran 7 tests in 3.8s (1 classes, 16 at a time; slowest: FromThisRepo 4s) / OK [ran] [tree 703e3997dde2] (2026-10-23T15:22:50Z)
- (ac 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 72 tests in 8.5s (18 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 703e3997dde2] (2026-10-23T15:22:50Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): score counts only telling words (at most an eighth of the library uses them) after a first try matched 'files' and 'evidence'; kata reads the shipped eval sets through load_briefs (which already bounds regexes) and scores with passes(); lesson refuses a range starting with '-' and passes '--' to git; the field guide reads the library at site build and escapes every value` → the dojo, katas, a five-minute lesson from a diff and a browsable field guide, each an fm verb or site page; analogy cards and live exemplars left out by a recorded decision [tree 703e3997dde2] (2026-10-23T15:22:50Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): score counts only telling words (at most an eighth of the library uses them) after a first try matched 'files' and 'evidence'; kata reads the shipped eval sets through load_briefs (which already bounds regexes) and scores with passes(); lesson refuses a range starting with '-' and passes '--' to git; the field guide reads the library at site build and escapes every value` → a playbook with no eval set has no katas (a usage error naming the path); a one-commit range reads as that commit's change; a task with no Lessons gives none; a library of one playbook scores with a limit of 1, so tests and tiny overlays still match [tree 703e3997dde2] (2026-10-23T15:22:50Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): score counts only telling words (at most an eighth of the library uses them) after a first try matched 'files' and 'evidence'; kata reads the shipped eval sets through load_briefs (which already bounds regexes) and scores with passes(); lesson refuses a range starting with '-' and passes '--' to git; the field guide reads the library at site build and escapes every value` → lesson's RANGE is the only user string reaching git: one starting with '-' is refused before git runs and '--' ends options after it; the answer file is read as text and matched by the eval set's own checks, never run; the site page escapes playbook titles and Use-when lines [tree 703e3997dde2] (2026-10-23T15:22:50Z)
- (step 5) `python3 plugin/tests/run.py test_playbook_draft test_docs test_playbook_machinery test_playbook_check test_suite_hygiene test_cli` → exit 0 · Ran 263 tests in 24.3s (70 classes, 16 at a time; slowest: TaskLifecycle 24s, AuditPrep 9s, StateViews 9s) / OK [ran] [tree ac5efa8739f2] (2026-10-23T15:24:25Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): score counts only telling words (at most an eighth of the library uses them) after a first try matched 'files' and 'evidence'; kata reads the shipped eval sets through load_briefs (which already bounds regexes) and scores with passes(); lesson refuses a range starting with '-' and passes '--' to git; the field guide reads the library at site build and escapes every value; SKILL.md kept under its 10,000-character budget` → the dojo, katas, a five-minute lesson from a diff and a browsable field guide, each an fm verb or site page; analogy cards and live exemplars left out by a recorded decision [tree ac5efa8739f2] (2026-10-23T15:24:26Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): score counts only telling words (at most an eighth of the library uses them) after a first try matched 'files' and 'evidence'; kata reads the shipped eval sets through load_briefs (which already bounds regexes) and scores with passes(); lesson refuses a range starting with '-' and passes '--' to git; the field guide reads the library at site build and escapes every value; SKILL.md kept under its 10,000-character budget` → a playbook with no eval set has no katas (a usage error naming the path); a one-commit range reads as that commit's change; a task with no Lessons gives none; a library of one playbook scores with a limit of 1, so tests and tiny overlays still match [tree ac5efa8739f2] (2026-10-23T15:24:26Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): score counts only telling words (at most an eighth of the library uses them) after a first try matched 'files' and 'evidence'; kata reads the shipped eval sets through load_briefs (which already bounds regexes) and scores with passes(); lesson refuses a range starting with '-' and passes '--' to git; the field guide reads the library at site build and escapes every value; SKILL.md kept under its 10,000-character budget` → lesson's RANGE is the only user string reaching git: one starting with '-' is refused before git runs and '--' ends options after it; the answer file is read as text and matched by the eval set's own checks, never run; the site page escapes playbook titles and Use-when lines [tree ac5efa8739f2] (2026-10-23T15:24:26Z)
## Log
- 2026-10-22T17:43:44Z created
- 2026-10-22T17:57:54Z set scope=['plugin/lib/fmplaybooks.py', 'plugin/lib/fmcli.py', 'site', 'plugin/tests/test_playbook_lessons.py', 'CHANGELOG.md']
- 2026-10-23T14:58:26Z set tier=M, scope=['plugin/lib/fmplaybooks.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_playbook_machinery.py', 'plugin/tests/test_docs.py', 'plugin/skills/playbooks/SKILL.md', 'site/pages.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T15:14:50Z criterion 1 verify: `cd plugin/tests && python3 -m unittest test_playbook_lessons` → `python3 plugin/tests/run.py test_playbook_draft`
- 2026-10-23T15:14:50Z set scope=['plugin/lib/fmplaybooks.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_playbook_draft.py', 'plugin/tests/test_docs.py', 'plugin/skills/playbooks/SKILL.md', 'site/pages.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T15:18:37Z focused
- 2026-10-23T15:18:53Z criterion 2 verify: `python3 plugin/tests/run.py test_playbook_machinery` → `python3 plugin/tests/run.py test_playbook_draft`
- 2026-10-23T15:24:51Z done
- 2026-10-23T15:24:53Z committed 8457fa33 (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1523 [FEATURE M, done, 5 steps] Round 3 (T-1520): Playbooks drafted from finished runs and history: a draft from a proved — lesson: A brief is already a distilled tran…
- T-1553 [SECURITY M, done, 3 steps] Guard oracle: a stub-exec run agrees with the guard's reading — lesson: A tool that runs things to check them must treat 'didn't run' …
- T-1522 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Playbook evals: A/B each playbook against none on held-out briefs, ablat
- decision 2026-10-23: T-1525: leave out 'borrow from' analogy cards and live exemplars on the field guide
- similar finished tasks took 3–5 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmplaybooks.py, plugin/skills/playbooks/SKILL.md, plugin/tests/test_docs.py, plugin/tests/test_playbook_draft.py, site/pages.py; re-ground the plan against them before editing
## Lessons
- Word-overlap scoring needs document frequency: a word most of the library uses matches every run
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_docs.py
- plugin/tests/test_playbook_draft.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmplaybooks.py
- plugin/skills/playbooks/SKILL.md
- site/pages.py
