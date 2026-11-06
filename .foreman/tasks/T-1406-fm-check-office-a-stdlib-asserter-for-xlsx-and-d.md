---
id: T-1406
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmoffice.py, plugin/lib/fmcli.py, plugin/tests/test_office.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-10-23T09:30:01Z
inferred_deps: [T-1382]
inferred_why: T-1382: named in its request
base: 0b6b03d083052beafb434fe9803db0389891bb56
base_tree: 45d29b6815aebcabb35bd46cf29f3753c75a7510
plan0_at: 2026-10-23T09:27:16Z
plan0_scope: [plugin/lib/fmoffice.py, plugin/lib/fmcli.py, plugin/tests/test_office.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# Fm check office: a stdlib asserter for xlsx and docx deliverables (cell values, sheet coun
## Raw request
> FEATURE: fm check office: a stdlib asserter for xlsx and docx deliverables (cell values, sheet count, no error cells) usable as a verify command (S19, A21)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: a workbook with #REF! fails and a clean one passes; --cell Sheet1!B7=42 checks a value
## Interpretation
fm check office FILE: a stdlib asserter for .xlsx/.xlsm and .docx deliverables, usable as a criterion's verify command. Workbook: no error cells (cached t=e values such as #REF!), --sheets N, --cell 'Sheet!REF=VALUE' (numbers compare as numbers, quoted sheet names, $ refs). Document: no broken-field text, --contains TEXT. Exit 0/1/2 (holds / a check fails / can't read). Untrusted files: members over 64 MB unpacked are refused and any DTD is refused as expat meets it, so no entity is declared or fetched.
## Assumptions (confidence)
## Acceptance criteria
- [x] a workbook with #REF! fails and a clean one passes; --cell Sheet1!B7=42 checks a value; a docx broken field fails; a DTD in any encoding, a non-zip and an unsupported extension exit 2 — verify with `python3 plugin/tests/run.py test_office`
## Non-goals
## Approach (options → choice → why)
Options: openpyxl/python-docx (not stdlib; never installed silently); LibreOffice headless recalculation (heavy, optional at best); zipfile + expat over the OOXML parts, cached values only. Choice: the last; ElementTree's own parser can't refuse a DTD in a non-UTF-8 encoding by byte search, so expat's StartDoctypeDeclHandler raises and a TreeBuilder builds the tree.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests, then fmoffice and the check action
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_office` → ✗ exit 1 · Ran 4 tests in 0.6s (1 classes, 16 at a time; slowest: Office 0s) / FAILED (1 classes) [ran] [tree 36862a22b9bf] (2026-10-23T09:27:21Z)
- (step 1) `python3 plugin/tests/run.py test_office test_cli` → exit 0 · Ran 122 tests in 40.1s (36 classes, 16 at a time; slowest: TaskLifecycle 40s, AuditPrep 17s, StateViews 17s) / OK [ran] [tree f9c312bd7749] (2026-10-23T09:28:56Z)
- (ac 1) `python3 plugin/tests/run.py test_office` → exit 0 · Ran 4 tests in 2.9s (1 classes, 16 at a time; slowest: Office 3s) / OK [ran] [tree f9c312bd7749] (2026-10-23T09:29:00Z)
- (audit intent) `self review; test_office, test_cli, test_docs green; tried on scratch workbooks and documents` → a workbook with #REF! fails and a clean one passes; --cell Sheet1!B7=42 checks a value; a docx's broken field fails; usable as a verify (exit 0/1/2) [tree f9c312bd7749] (2026-10-23T09:29:00Z)
- (audit adversary) `self review; test_office, test_cli, test_docs green; tried on scratch workbooks and documents` → untrusted OOXML: a UTF-16 member with a DOCTYPE and entity is refused as expat meets the doctype (no entity declared or expanded); members over 64 MB unpacked are refused before reading; a non-zip, a .xls and a wrong-kind flag exit 2; nothing is executed or recalculated [tree f9c312bd7749] (2026-10-23T09:29:00Z)
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-23T09:20:11Z set tier=M, scope=['plugin/lib/fmoffice.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_office.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-23T09:27:15Z focused
- 2026-10-23T09:29:58Z done
- 2026-10-23T09:30:01Z committed eea3069e (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-fm-anthropic-catalogue: Source: research/brainstorm-20261021-120257 (fm ideas, 10 lenses, 4 rounds, 3 deepened, --seen every earlier ideas.md: 520 ne…
- T-1405 [FIX M, done, 4 steps] Crash hygiene: stack dumps for hung verbs, safe stale index.lock removal, a lock probe in doctor — lesson: A safety rule written as 'unknow…
- T-1760 [FEATURE M, done, 3 steps] fm code diagnostics: fm code why explains a run, piped stdin is the request's context, and the start event and the app … — lesson: Read…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py; re-ground the plan against them before editing
## Lessons
- ElementTree's C parser exposes no doctype hook; for untrusted XML use expat directly with StartDoctypeDeclHandler raising and a TreeBuilder, rather than a byte search for <!DOCTYPE that UTF-16 slips past
## Plan gaps
- failed first: step 1 failing tests, then fmoffice and the check action
## Files touched
- plugin/tests/test_office.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmoffice.py
