---
id: T-1604
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmlib.py, plugin/tests/test_library.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T20:31:50Z
updated: 2026-10-23T08:49:09Z
base: b427b1a7b127b5390333443619b7094f45235b5e
base_tree: a9deb2a7a24f55a2842d060b0ab5a4bb0a26bee5
plan0_at: 2026-10-23T08:48:16Z
plan0_scope: [plugin/lib/fmlib.py, plugin/tests/test_library.py, CHANGELOG.md]
verified: strong
---
# fm lib check sorts its notes by a kind field, not by matching ': related ' in their text
## Raw request
> fm lib check` picks its related-names notes by matching the string `": related "` (fmlib.py:1235), so one more note type could be misfiled; a field on each note would be sturdier
> (noticed by an agent; research T-1519-review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] every fm lib lint note carries a kind (related or stale), and fm lib check counts related names by that kind, so a note whose words happen to include ': related ' isn't misfiled — verify with `python3 plugin/tests/run.py test_library`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, then a Note str subclass with .kind made in lint and read in check
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_library` → exit 0 · Ran 41 tests in 6.8s (9 classes, 16 at a time; slowest: LibSources 7s, LibraryAdmit 2s, LibrarySearch 1s) / OK [ran] [tree 2034543ce1c3] (2026-10-23T08:48:46Z)
- (audit self) `read the diff: Note is a str subclass, so every caller that prints, sorts, joins or json-dumps the notes sees plain text; only check reads .kind` → ok: lint's two note kinds tagged, related_notes filters by kind, a stale note quoting ': related ' is left out (test) [tree 2034543ce1c3] (2026-10-23T08:48:46Z)
- (ac 1) `python3 plugin/tests/run.py test_library` → exit 0 · Ran 41 tests in 6.5s (9 classes, 16 at a time; slowest: LibSources 6s, LibraryAdmit 2s, LibrarySearch 1s) / OK [ran] [tree 2034543ce1c3] (2026-10-23T08:48:57Z)
- (audit edge) `self review of the diff plus test_library` → a stale note whose words include ': related ' is not counted (test); Note prints and json-dumps as plain text [tree 2034543ce1c3] (2026-10-23T08:48:57Z)
- (audit self) `self review of the diff plus test_library` → no findings [tree 2034543ce1c3] (2026-10-23T08:48:57Z)
## Log
- 2026-10-22T20:31:50Z created
- 2026-10-23T08:44:25Z planned from capture
- 2026-10-23T08:44:25Z set scope=['plugin/lib/fmlib.py', 'plugin/tests/test_library.py', 'CHANGELOG.md']
- 2026-10-23T08:48:15Z focused
- 2026-10-23T08:49:08Z done
- 2026-10-23T08:49:09Z committed f8806754 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1519-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** changes needed. Two adversary findings, on `fm new check`…
- research T-1389-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** changes needed. The three criteria are met, but the quara…
- T-1303 [FIX S, done, 1 steps] fm ideas' near-T marks are spurious: an idea matched a done task by sharing two common words with its long request; a match now needs the t…
- decision 2026-10-21: fm code's no-setup default picks only a runner whose read-only mode is verified here (claude); codex/gemini plan only when named, with a note
- the similar finished task took 1 steps
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmlib.py, plugin/tests/test_library.py; re-ground the plan against them before editing
## Lessons
- none: a one-place classification fix
## Files touched
- plugin/lib/fmlib.py
- plugin/tests/test_library.py
- CHANGELOG.md
