---
id: T-3277
type: FEATURE
tier: M
status: planned
priority: normal
scope: [plugin/lib/sampo/editverdict.py, plugin/tests/test_editverdict.py, plugin/lib/sampo/ambient.py, plugin/lib/sampo/cli.py, CHANGELOG.md]
depends_on: [T-3270]
source: user
created: 2026-11-06T02:28:07Z
updated: 2026-11-06T02:28:35Z
---
# Moon C-001115: rule keep/neutral/harmful on each edit's replay, at the edit
## Raw request
> Moon C-001115: rule keep/neutral/harmful on each edit's replay, at the edit
## Interpretation
Reading 1 (chosen): partial. Exists: ambient.py (T-0705) replays the affected tests after every edit but reports only a whole-run flip, and cli.py:2303 task_prove_hunks ablates hunks only when asked. Missing: a per-edit ruling (keep/neutral/harmful) recorded at the edit with the files named. This adds that ledger. Reading 2 (ruled out): a second model reading each diff; slow, costly, and the tests already give a neutral verdict for free.
## Assumptions (confidence)
## Acceptance criteria
- [ ] verdict(prev_exit, exit, edited_files, linked_tests) rules harmful when a pass turns red, keep when red turns green or a linked test passes, neutral when no test links the edited file — verify with `python3 plugin/tests/run.py test_editverdict`
- [ ] an ambient run records one ledger line per edited file with its verdict, and a harmful verdict's note names the edited files — verify with `python3 plugin/tests/run.py test_editverdict`
- [ ] sampo check ambient edits lists the last verdicts per file — verify with `python3 plugin/tests/run.py test_editverdict`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: reuse ambient.py's replay and its affected-test selection; new editverdict.py holds a pure verdict() plus a jsonl ledger, ambient.after_edit queues the path, _record rules each queued file. Likely outcome: bad edit flagged with file names in the next-tool note; ambient.py gets a small registration only.
2. Run prove --hunks (revert each hunk) after every edit. fails if: one check run per hunk per edit makes every edit minutes slow and starves lanes.
3. Rewrite ambient to run per-file tests separately. fails if: concurrent edits double test runs and the host strain gate skips them.
4. Do less: add edited file names to the existing flip note only. Likely outcome: harmful named but no neutral or keep ruling and no ledger.

Choice 1 (85%): reuses the existing replay, adds the ruling and ledger in a new module. Captured: none.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] write failing test_editverdict for verdict() and the ledger  <- CURRENT
2. [ ] add plugin/lib/sampo/editverdict.py (pure verdict + jsonl ledger + listing)
3. [ ] ambient.after_edit appends the path to ambient/pending; _record calls editverdict.record and names files in the flip note
4. [ ] register sampo check ambient edits; CHANGELOG
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T02:28:07Z created
- 2026-11-06T02:28:13Z set scope=['plugin/lib/sampo/editverdict.py', 'plugin/tests/test_editverdict.py', 'plugin/lib/sampo/ambient.py', 'plugin/lib/sampo/cli.py', 'CHANGELOG.md']
- 2026-11-06T02:28:35Z set depends_on=['T-3270']
## Follow-ups captured
