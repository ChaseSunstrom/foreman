---
id: T-1424
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmedit.py, plugin/tests/test_batch_edit.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-21T19:54:23Z
updated: 2026-10-22T15:30:21Z
base: fa212a676573b6659a0b8925ebd3c254c74ece0a
base_tree: c3809f0c45113a9a8cdde327f1565605fb1dcee4
plan0_at: 2026-10-22T15:27:23Z
plan0_scope: [plugin/lib/fmedit.py, plugin/tests/test_batch_edit.py, CHANGELOG.md]
verified: strong
---
# fm edit refuses NUL files and matches LF old text in a CRLF file
## Raw request
> fm edit (outside fm code) still edits a UTF-8 file containing NUL bytes, and when its old text is LF but the file is CRLF it only says 'not found' without naming the line endings (T-1408 builder)
## Interpretation
fm edit (fmedit.py) rewrites a UTF-8 file that holds NUL bytes (binary) and, when the old text has LF but the file is CRLF, says only 'old text not found'. fm code's edit path already refuses NUL files and converts endings (fmcode Run.existing/endings).
## Assumptions (confidence)
## Acceptance criteria
- [x] a NUL file is refused; LF old text in a CRLF file is applied keeping CRLF — verify with `cd plugin/tests && python3 -m unittest test_batch_edit.BatchEdit.test_nul_files_are_refused_and_lf_old_text_matches_crlf`
## Non-goals
## Approach (options → choice → why)
In the read loop: a text with \0 is a problem ('has NUL bytes: fm edit rewrites text files only'). In matching: no hit, the file mostly CRLF and the old text without \r → try old/new with CRLF endings (as fm code does), and say so in the summary; still no hit → the not-found line names the file's CRLF endings.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] NUL refusal and CRLF match in fmedit
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_batch_edit.BatchEdit.test_nul_files_are_refused_and_lf_old_text_matches_crlf` → ✗ exit 1 · Ran 1 test in 1.005s / FAILED (failures=1) [ran] [tree 8976d5433d45] (2026-10-22T15:27:25Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_batch_edit.BatchEdit.test_nul_files_are_refused_and_lf_old_text_matches_crlf` → exit 0 · Ran 1 test in 1.200s / OK [ran] [tree 26e4ea09fb82] (2026-10-22T15:27:28Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_batch_edit.BatchEdit.test_nul_files_are_refused_and_lf_old_text_matches_crlf` → exit 0 · Ran 1 test in 1.098s / OK [ran] [tree d9f8abdd5acf] (2026-10-22T15:28:08Z)
- (audit edge) `self: NUL check right after the read (the file is skipped, all-or-none keeps the batch unwritten); CRLF retry only when no hit, the file is mostly CRLF, and the old text has a newline and no CR; new text converted the same way. test_batch_edit green, incl. the existing CRLF-kept case.` → a mixed-ending file (under half CRLF) keeps the plain not-found; a single-line old text never needed the retry [tree d9f8abdd5acf] (2026-10-22T15:28:08Z)
- (audit adversary) `self: NUL check right after the read (the file is skipped, all-or-none keeps the batch unwritten); CRLF retry only when no hit, the file is mostly CRLF, and the old text has a newline and no CR; new text converted the same way. test_batch_edit green, incl. the existing CRLF-kept case.` → no new paths; the NUL refusal only narrows what fm edit writes [tree d9f8abdd5acf] (2026-10-22T15:28:08Z)
- (audit self) `self: NUL check right after the read (the file is skipped, all-or-none keeps the batch unwritten); CRLF retry only when no hit, the file is mostly CRLF, and the old text has a newline and no CR; new text converted the same way. test_batch_edit green, incl. the existing CRLF-kept case.` → no findings [tree d9f8abdd5acf] (2026-10-22T15:28:08Z)
## Log
- 2026-10-21T19:54:23Z created
- 2026-10-22T15:02:05Z planned from capture
- 2026-10-22T15:27:20Z focused
- 2026-10-22T15:30:19Z done
- 2026-10-22T15:30:21Z committed ff0d502d (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1089-review: Verdict: changes needed.** I found no guard bypass. I could not run anything, because this audit is read-only, so everything below is from readin…
- T-1408 [FIX M, done, 2 steps] fm code's write and edit keep a file's line endings and refuse a non-UTF-8 target; option-shaped paths are refused cleanly — lesson: A tool…
- T-1099 [FIX S, done, 3 steps] Ledger roll takes the ledger lock and keeps time order: _roll_ledger keeps unparseable-ts — lesson: Rewriting a file other processes append…
- decision 2026-10-21: T-1393: hold only the mcpServers entries of ~/.claude.json, not the whole file
- similar finished tasks took 2–3 steps
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md; re-ground the plan against them before editing
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/lib/fmedit.py
- plugin/tests/test_batch_edit.py
- CHANGELOG.md
