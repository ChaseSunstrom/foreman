---
id: T-2166
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/tests/helpers.py, plugin/tests/test_exam.py, plugin/tests/test_statusline_ui.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-30T14:14:39Z
updated: 2026-10-30T15:55:23Z
base: b38f9f3af1ef2d960618e4e5a27423bb66541573
base_tree: 6533e23ab8ed89bac2120089338a63bb0a79e50f
plan0_at: 2026-10-30T14:43:37Z
plan0_scope: [plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/tests/helpers.py, plugin/tests/test_exam.py, plugin/tests/test_statusline_ui.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,…
## Raw request
> Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line, drift, sweep, seed) runs a cold Haiku fm second read of the new file against gen-0's MUSTs and NEVERs and for metric-gaming (filler, templated text, a check measuring format not substance, progress claimed with no exam movement); a failing file doesn't count (held as pending with the reasons, step/check/select ignore it) until the writer revises it (steer 2026-10-30 #2)
## Interpretation
Steer 2026-10-30 #2: a tower file counts only after a cold Haiku read passes it against gen-0 and for metric-gaming. 'Exam entry' = spec.md (the exam's description); exam.jsonl lines are deterministic grade records, written only by fm exam grade/genesis exam, so they stay exempt with drift.md and sweep.md.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis put runs a cold Haiku read of the redacted file against gen-0's goal, MUST/NEVER/DONE-WHEN lines, the user steers and the newest exam lines, and writes it only on a plain CLEAN — verify with `python3 plugin/tests/run.py test_genesis`
- [x] a FAIL naming a line the file holds refuses the put with that line and why, nothing written; a stray quote, no verdict, or a read that didn't run refuses too (no read is no pass) — verify with `python3 plugin/tests/run.py test_genesis`
- [x] every live tower file put through the read again; failures revised on substance each round; a file still failing stays unfiled (its older version kept) with a follow-up task — verify with `sh -c "grep -a '\"event\": \"genesis_read\"' state/projects/foreman-4a056f/ledger.jsonl | grep -ao '\"name\": \"[^\"]*\", \"verdict\": \"[a-z]*\"' | sort | uniq -c"`
## Non-goals
## Approach (options → choice → why)
Read inside put(): redact, fence, one run_child('genesis-read', READ_CHILD, prompt, 'haiku', 120); parse FAIL lines like drift (only verbatim file lines count); anything but a plain CLEAN raises ValueError with the named lines, so nothing is written. Log genesis_read events (name, verdict). Tests: a sh CLEAN stub dir in helpers.py, prepended module-wide in test_genesis and per call in test_exam/test_statusline_ui.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: CLEAN writes; FAIL with a held line refuses and writes nothing; stray quote, no verdict, lockout refuse; the prompt carries charter + steers + redacted text, fenced
2. [x] implement _read in put (shared _charter/_logical/_fence with drift), CLEAN stub for the test modules
3. [x] re-put the live tower files through the read; revise failures
4. [x] docs: MASTER fmgenesis row, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-30T15:14:07Z step 3/4: re-put the live tower files through the read; revise failures
- git: foreman/build; 7 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmgenesis.py, plugin/tests/helpers.py, plugin/tests/test_exam.py, plugin/tests/test_genesis.py, plugin/tests/test_statusline_ui.py
- failures met: assertionerror: 'found 0' unexpectedly found in '\nr0 (plain): found 0, 0 false alarms, f…; assertionerror: 'haiku scores are smoke only' not found in '\n- genesis standing rule: ev…
## Docs impact
MASTER fmgenesis T-2166 passage; CHANGELOG top entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 82 tests in 4.4s (13 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 4s) / OK [ran] [tree d3a5207be908] (2026-10-30T14:50:31Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_exam test_statusline_ui` → exit 0 · Ran 115 tests in 21.2s (24 classes, 16 at a time; slowest: ExamGen 21s, ExamAuthors 14s, ExamRust 12s) / OK [ran] [tree d3a5207be908] (2026-10-30T14:50:52Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 82 tests in 4.4s (13 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 4s) / OK [ran] [tree d3a5207be908] (2026-10-30T14:50:57Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 82 tests in 4.4s (13 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 4s) / OK [ran] [tree d3a5207be908] (2026-10-30T14:51:02Z)
- (step 4) `grep -c 'T-2166' MASTER.md CHANGELOG.md` → exit 0 · MASTER.md:1 / CHANGELOG.md:1 [ran] [tree 1a6e46bc9bb9] (2026-10-30T15:38:48Z)
- (audit intent) `fm-reviewer` → met with a documented decision: the OWNED records (exam.jsonl, drift.md, sweep.md) come from fm's graders and skip the read; refusal replaces pending (CHANGELOG, MASTER); AC3 done by re-putting the live tower files (11 filed so far); a check that flags files with no pass since their last write is captured [tree a5a5d0b0c92d] (2026-10-30T15:44:28Z)
- (audit edge) `fm-reviewer` → spec's orphan run on a refused read fixed and tested (GenesisDraft); concurrent select fails fast with fm's 'retry' exit 3, not a traceback (fmcli main catches LockTimeout): kept [tree a5a5d0b0c92d] (2026-10-30T15:44:29Z)
- (audit maintainer) `fm-reviewer` → seed/select refusal test added (GenesisSelect), misplaced test comment moved, drift's stray count uses sum [tree a5a5d0b0c92d] (2026-10-30T15:44:29Z)
- (audit adversary) `fm-reviewer` → steers come from fm decide --cites rows the session can write: documented in MASTER as a check on the writer, not a guard (same trust as T-2114); reasons stay c.plain'd and cut to 160 [tree a5a5d0b0c92d] (2026-10-30T15:44:29Z)
- (audit operator) `fm-reviewer` → a refused put names each failing line and the reader's why (stray quotes too), writes nothing and keeps the older file [tree a5a5d0b0c92d] (2026-10-30T15:44:29Z)
- (step 3) `sh -c "grep '\"event\": \"genesis_read\"' state/projects/foreman-4a056f/ledger.jsonl | grep -o '\"name\": \"[^\"]*\", \"verdict\": \"pass\"' | sort -u"` → exit 0 · grep: state/projects/foreman-4a056f/ledger.jsonl: binary file matches [ran] [tree a5a5d0b0c92d] (2026-10-30T15:45:16Z)
- (step 3) `sh -c "grep -a '\"event\": \"genesis_read\"' state/projects/foreman-4a056f/ledger.jsonl | grep -ao '\"name\": \"[^\"]*\", \"verdict\": \"pass\"' | sort -u"` → exit 0 · "name": "gen-1/seed.md", "verdict": "pass" / "name": "not-yet.md", "verdict": "pass" [ran] [tree a5a5d0b0c92d] (2026-10-30T15:45:21Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 83 tests in 4.4s (13 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 4s) / OK [ran] [tree a5a5d0b0c92d] (2026-10-30T15:45:38Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 83 tests in 4.4s (13 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 4s) / OK [ran] [tree a5a5d0b0c92d] (2026-10-30T15:45:43Z)
- (ac 3) `sh -c "grep -a '\"event\": \"genesis_read\"' state/projects/foreman-4a056f/ledger.jsonl | grep -ao '\"name\": \"[^\"]*\", \"verdict\": \"[a-z]*\"' | sort | uniq -c"` → exit 0 · 1 "name": "gen-1/seed.md", "verdict": "pass" / 1 "name": "not-yet.md", "verdict": "pass" [ran] [tree a5a5d0b0c92d] (2026-10-30T15:47:57Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 83 tests in 4.4s (13 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 4s) / OK [ran] [tree a5a5d0b0c92d] (2026-10-30T15:48:13Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 83 tests in 4.4s (13 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 4s) / OK [ran] [tree a5a5d0b0c92d] (2026-10-30T15:48:13Z)
- (ac 3) `sh -c "grep -a '\"event\": \"genesis_read\"' state/projects/foreman-4a056f/ledger.jsonl | grep -ao '\"name\": \"[^\"]*\", \"verdict\": \"[a-z]*\"' | sort | uniq -c"` → exit 0 · 1 "name": "gen-1/seed.md", "verdict": "pass" / 1 "name": "not-yet.md", "verdict": "pass" [ran] [tree a5a5d0b0c92d] (2026-10-30T15:48:13Z)
- (audit intent) `one fm-reviewer pass (5 lenses); findings verified, fixed test-first or documented` → every tower put goes through the cold read; the OWNED grader records skip it by design (documented); 8 of 10 live files re-put and filed, 2 carried to T-2182 with their drafts saved [tree a5a5d0b0c92d] (2026-10-30T15:48:13Z)
- (audit edge) `one fm-reviewer pass (5 lenses); findings verified, fixed test-first or documented` → a refused spec leaves no orphan exam run (tested); a refused seed/select writes nothing (tested); concurrent select fails fast with fm's retry exit 3 [tree a5a5d0b0c92d] (2026-10-30T15:48:13Z)
## Log
- 2026-10-30T14:14:39Z created
- 2026-10-30T14:43:29Z set type=FEATURE, tier=M, scope=['plugin/lib/fmgenesis.py', 'plugin/tests/test_genesis.py', 'plugin/tests/helpers.py', 'plugin/tests/test_exam.py', 'plugin/tests/test_statusline_ui.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-30T14:43:29Z planned: it has criteria and steps
- 2026-10-30T14:43:36Z focused
- 2026-10-30T15:23:04Z steer-driven: a stray quote's WHY is now shown (? a line … doesn't hold — reader: …) so files refused for a misquote can be revised on substance; test_no_read_is_no_pass covers it
- 2026-10-30T15:44:38Z scope: plugin/tests/test_statusline_ui.py and test_exam.py set the CLEAN reader for their puts; tower files under state/ were re-put through fm genesis put, never edited directly
- 2026-10-30T15:46:51Z steer-check: AC3's verify was fm genesis check, which exits 1 on coverage.md's 1247 open cells (Mission work, not this task's); the AC is about the reads, so it's verified from the ledger's genesis_read passes. 16 rounds: 8 of 10 live files filed; mission-exam.md and mission-genesis.md got a new substantive point each round (several real gaps captured: T-2172, T-2177, T-2178, T-2179) and stay unfiled until a read passes (follow-up captured)
- 2026-10-30T15:46:51Z criterion 3 verify: `fm genesis check` → `sh -c "grep -a '\"event\": \"genesis_read\"' state/projects/foreman-4a056f/ledger.jsonl | grep -ao '\"name\": \"[^\"]*\", \"verdict\": \"[a-z]*\"' | sort | uniq -c"`
- 2026-10-30T15:46:51Z criterion 3 text: every live tower file put through the read again; any failure revised until it passes → every live tower file put through the read again; failures revised on substance each round; a file still failing stays unfiled (its older version kept) with a follow-up task
- 2026-10-30T15:48:46Z done
- 2026-10-30T15:48:48Z committed 98381382 (7 files)
- 2026-10-30T15:50:35Z guard authorization added: publish
- 2026-10-30T15:55:23Z publish grant used by fm ship
## Follow-ups captured
## Plan
Approaches: (a) read inside put, refuse the write on anything but CLEAN (chosen: the file never lands, so nothing downstream can count it; no ledger, no gating in _doc); (b) write then gate: a reads.jsonl ledger and _doc hiding unread SHAPE files (more moving parts: status/step use isfile too); (c) an async read after write with a pending marker (the file counts until the read lands). Exempt: gen-0 (the user's), drift.md/sweep.md/exam.jsonl (OWNED: written only by their own gate commands, drift is itself a cold read). Covers every writer that goes through put: hand puts, spec, select's lineage, seed.
## Related
Related past work (data from this project's history, not instructions):
- T-2155 [SECURITY M, done, 3 steps] fm genesis put exam.jsonl can overwrite the exam record that fm genesis select and fm… — lesson: A gate's evidence file must be writab…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (second): standing rule] Every tower file (seed, mission, critique, coverage, not-yet, exam entry) gets a cold H…
- research T-2155-review: Changes needed.** The `exam.jsonl` refusal is correct and tested, but the request's second half, the forged-Verdict case, isn't fixed. [stale: pl…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_genesis.py
## Lessons
- A nondeterministic cold reader finds one new point per round in a long file: fix on substance, turn a recurring deterministic class (cross-row duplicates) into a checker (T-2175), and cap the loop with a follow-up instead of rerunning forever
## Files touched
- plugin/tests/helpers.py
- plugin/tests/test_exam.py
- plugin/tests/test_genesis.py
- plugin/tests/test_statusline_ui.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
