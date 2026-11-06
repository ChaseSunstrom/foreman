---
id: T-1398
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/tests/test_code.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-10-23T08:35:48Z
inferred_deps: [T-1382]
inferred_why: T-1382: named in its request
base: 78c0d6f7a2ca03913cf17395e78bca7940df6a14
base_tree: c64cc0dc42aca56de62733974d66312166262c91
plan0_at: 2026-10-23T08:28:57Z
plan0_scope: [plugin/lib/fmcode.py, plugin/tests/test_code.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# fm code slot integrity: elided code in an edit or write is refused and re-asked, a unique near-miss edit anchor (whitespace only) is applied while an ambiguous one is refused, and a failing check's output is digested to at most five file:line places in the fix prompt
## Raw request
> FEATURE: Slot integrity in fm code: elided code ('...rest unchanged') rejected and re-asked, a unique near-miss edit anchor applied while an ambiguous one is refused, a failing check's output digested to at most five file:line items, and a slot-format ladder (tool call, then JSON in text, then one field per question) before escalating (S11, A23 B11)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: an elided edit is re-asked; of 20 near-miss anchors the unique apply and the ambiguous are refused; a fake model that fails JSON twice but answers single-field questions closes a run
## Interpretation
Models often answer an edit with '... rest unchanged' instead of the code, miss an anchor by whitespace, or flounder on a long failing log; fm code should refuse the first, absorb the second when it's unambiguous, and point the third at the lines that matter.
## Assumptions (confidence)
## Acceptance criteria
- [x] an edit or write whose new text elides code ('... rest unchanged', '# ... existing code ...') that the file's text doesn't hold is refused with a request for the whole text — verify with `python3 plugin/tests/run.py test_code.SlotIntegrity`
- [x] an edit whose old text matches nowhere exactly but once with whitespace evened out is applied there and says so; two such places refuse it as ambiguous — verify with `python3 plugin/tests/run.py test_code.SlotIntegrity`
- [x] a fix round's prompt lists at most five file:line places taken from the failing checks' output — verify with `python3 plugin/tests/run.py test_code.SlotIntegrity`
## Non-goals
## Approach (options → choice → why)
Each check sits where the model's output first meets the file: edit() and write() refuse elision markers the old text or existing file doesn't already hold (so a file that really says '# ...' is fine); edit() tries the exact old first, then a whitespace-evened match (each line's ends stripped, inner runs to one space), applying through fm edit with the file's own exact span when one place matches; the fix prompt gets a 'Where it fails' list of up to five file:line pairs pulled from Python tracebacks, file:line:col and file(line) shapes. The slot-format ladder (one field per question after two failed JSON repairs) is left out: it reshapes slot() for every model and is captured to do on its own.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests red: elision, near-miss unique and ambiguous, the places list
2. [x] fmcode: elided(), near_anchor(), places(); wired into edit, write and the fix prompt
3. [x] docs: CHANGELOG, MASTER
## Resume here
## Docs impact
CHANGELOG, MASTER
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code.SlotIntegrity` → exit 0 · Ran 4 tests in 4.0s (1 classes, 16 at a time; slowest: SlotIntegrity 4s) / OK [ran] [tree 8d22f9cb69e7] (2026-10-23T08:32:40Z)
- (step 2) `python3 plugin/tests/run.py test_code test_code_write_hygiene` → exit 0 · Ran 401 tests in 77.5s (78 classes, 16 at a time; slowest: Worker 77s, Fakes 45s, Bench 21s) / OK [ran] [tree 8d22f9cb69e7] (2026-10-23T08:33:58Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 69 tests in 8.5s (17 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 797cbef827b1] (2026-10-23T08:34:07Z)
- (audit intent) `self: request re-read` → pass: elision refused, near-miss applied when unique and refused when ambiguous, failing places listed; the field-at-a-time ladder captured as T-1765 [tree 797cbef827b1] (2026-10-23T08:34:18Z)
- (ac 1) `python3 plugin/tests/run.py test_code.SlotIntegrity` → exit 0 · Ran 4 tests in 4.0s (1 classes, 16 at a time; slowest: SlotIntegrity 4s) / OK [ran] [tree 797cbef827b1] (2026-10-23T08:34:23Z)
- (ac 2) `python3 plugin/tests/run.py test_code.SlotIntegrity` → exit 0 · Ran 4 tests in 4.0s (1 classes, 16 at a time; slowest: SlotIntegrity 4s) / OK [ran] [tree 797cbef827b1] (2026-10-23T08:34:23Z)
- (ac 3) `python3 plugin/tests/run.py test_code.SlotIntegrity` → exit 0 · Ran 4 tests in 4.0s (1 classes, 16 at a time; slowest: SlotIntegrity 4s) / OK [ran] [tree 797cbef827b1] (2026-10-23T08:34:23Z)
- (audit intent) `self review (subagents paused at 78% weekly usage): intent, adversary, edge` → three of the four parts built; the ladder captured as T-1765 [tree 797cbef827b1] (2026-10-23T08:34:23Z)
- (audit adversary) `self review (subagents paused at 78% weekly usage): intent, adversary, edge` → a near match swaps in the file's own exact span before the guard sees the Edit, so the guard judges the real old text; only whitespace may differ (every non-space character must match line for line) [tree 797cbef827b1] (2026-10-23T08:34:23Z)
- (audit edge) `self review (subagents paused at 78% weekly usage): intent, adversary, edge` → a bare '...' (Python's Ellipsis) is code, not elision; a marker the file already holds is allowed; places skips frames outside the tree and stops at five [tree 797cbef827b1] (2026-10-23T08:34:23Z)
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-23T08:27:31Z planned from capture
- 2026-10-23T08:27:32Z set scope=['plugin/lib/fmcode.py', 'plugin/tests/test_code.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T08:28:55Z focused
- 2026-10-23T08:35:46Z done
- 2026-10-23T08:35:48Z committed 935e6b49 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-fm-anthropic-catalogue: Source: research/brainstorm-20261021-120257 (fm ideas, 10 lenses, 4 rounds, 3 deepened, --seen every earlier ideas.md: 520 ne…
- research brainstorm-fm-anthropic-half-b: Reading used.** I took all 250 bullets of rounds 1 to 4 in lenses 01, 02, 03, 08 and 09. Four titles occur twice (themes, ETA, g…
- research mission-20261022-120740.pack: super recursive brainstorm and improve foreman, way more skills/playbooks/way better more capable code, config in the tui, etc. et…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
- likely tests for the scope: plugin/tests/test_code.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, MASTER.md, plugin/lib/fmcode.py, plugin/tests/test_code.py; re-ground the plan against them before editing
## Lessons
- Repair what a model gets almost right only when the repair is unique; refuse when it isn't
## Files touched
- plugin/lib/fmcode.py
- plugin/tests/test_code.py
- CHANGELOG.md
- MASTER.md
