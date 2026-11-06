---
id: T-2155
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-30T13:50:59Z
updated: 2026-10-30T14:10:58Z
base: f75d900fd4f9102817e5ca5f50cbc6065eb4e839
base_tree: 2b3af7dd3a348dad7c118a98b1cffd87a57c9a52
plan0_at: 2026-10-30T13:57:46Z
plan0_scope: [plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# fm genesis put exam.jsonl can overwrite the exam record that fm genesis select and fm…
## Raw request
> fm genesis put exam.jsonl can overwrite the exam record that fm genesis select and fm exam scorecard gate on: refuse put on exam.jsonl (append only via exam_line) and fix the forged-Verdict case alongside (T-2097 review)
## Interpretation
exam.jsonl (the record fm genesis select and fm exam scorecard gate on) and gen-N/drift.md and sweep.md (the drift and sweep stages pass on their 'Verdict: clean') were all writable through fm genesis put, so a hand-written line or a forged verdict could pass a gate. Put refuses an OWNED name with a pointer to the writing command; drift() and sweep() write through the raw _file writer; SHAPE keeps the names so export still picks the docs; test fixtures write these files directly (tower_file).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis put exam.jsonl is refused and exam_line still appends — verify with `python3 plugin/tests/run.py test_genesis test_exam`
- [x] a forged 'Verdict: clean' through fm genesis put gen-N/drift.md or sweep.md is refused and fm genesis drift/sweep still write them — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
Remove exam.jsonl from SHAPE and the put error text (smallest; the guard already refuses direct state writes). Considered: a signed/hash-chained exam log (heavier, later if a writer outside fm appears); append-only put for .jsonl (still forgeable).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: put exam.jsonl refused; fixtures through exam_line
2. [x] drop exam.jsonl from SHAPE; MASTER, CHANGELOG
3. [x] widen to drift.md and sweep.md: OWNED regex refused by put, drift/sweep write via _file; MASTER, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-30T14:06:35Z steps 2/2 done
- git: foreman/build; 4 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py
- failures met: json.decoder.jsondecodeerror: expecting value: line 0 column 0 (char 0)
## Docs impact
MASTER fmgenesis row, CHANGELOG
## Verification evidence
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  version skew         uidemo-982f4c ran 1.2.29, lacks 317 (T-0275, T-0705, T-0787, T-0933 …) — restart their sessions on the new Foreman / fm doctor: OK (48 pass, 6 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                29.0    30.2     150  [0] / SessionEnd                  24.4    26.5     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/* [ran] [tree 2b3af7dd3a34] (2026-10-30T14:01:12Z)
- `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 78 tests in 5.1s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 20f2032636c6] (2026-10-30T14:02:17Z)
- `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 78 tests in 4.2s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 20f2032636c6] (2026-10-30T14:02:17Z)
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 78 tests in 4.3s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 20f2032636c6] (2026-10-30T14:02:27Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_exam test_docs` → exit 0 · Ran 184 tests in 20.1s (43 classes, 16 at a time; slowest: ExamGen 20s, ExamAuthors 14s, ExamRust 12s) / OK [ran] [tree 20f2032636c6] (2026-10-30T14:02:47Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis test_exam` → exit 0 · Ran 104 tests in 22.0s (22 classes, 16 at a time; slowest: ExamGen 22s, ExamAuthors 14s, ExamRust 12s) / OK [ran] [tree 20f2032636c6] (2026-10-30T14:03:09Z)
- `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 78 tests in 5.2s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / FAILED (3 classes) (start tree + this task's tests) [ran] [tree 423fb8f52e09] (2026-10-30T14:05:53Z)
- `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 78 tests in 4.3s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 423fb8f52e09] (2026-10-30T14:05:53Z)
- (step 3) `python3 plugin/tests/run.py test_genesis test_exam test_docs` → exit 0 · Ran 184 tests in 20.1s (43 classes, 16 at a time; slowest: ExamGen 20s, ExamAuthors 13s, ExamRust 12s) / OK [ran] [tree de28690094e6] (2026-10-30T14:09:21Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 78 tests in 4.4s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree de28690094e6] (2026-10-30T14:09:26Z)
- (audit intent) `fm-reviewer` → HIGH (raw request also asked to fix the forged-Verdict case; diff only refused exam.jsonl) fixed: put refuses gen-N/drift.md and sweep.md via OWNED; criterion 2 added [tree de28690094e6] (2026-10-30T14:09:36Z)
- (audit adversary) `fm-reviewer + self` → put on exam.jsonl, gen-N/drift.md, gen-N/sweep.md refused before any write (file absent after); SHAPE still validates other names; lineage.md heading forgery (MEDIUM) captured as T-2163 [tree de28690094e6] (2026-10-30T14:09:36Z)
- (audit edge) `self` → OWNED uses fullmatch so gen-10/drift.md and exam.jsonl are caught and a doc named e.g. gen-1/drift-notes.md is not a SHAPE name anyway; export still lists drift.md and sweep.md because SHAPE keeps them [tree de28690094e6] (2026-10-30T14:09:36Z)
- (audit maintainer) `self` → one raw writer _file shared by put, drift and sweep; tests use one tower_file helper; MASTER row names OWNED and _file [tree de28690094e6] (2026-10-30T14:09:36Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis test_exam` → exit 0 · Ran 104 tests in 21.8s (22 classes, 16 at a time; slowest: ExamGen 22s, ExamAuthors 14s, ExamRust 12s) / OK [ran] [tree de28690094e6] (2026-10-30T14:10:16Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 78 tests in 4.3s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree de28690094e6] (2026-10-30T14:10:16Z)
- (audit edge) `one fm-reviewer pass (intent/adversary/edge/maintainer); HIGH fixed, MEDIUM captured T-2163, LOW dropped` → OWNED fullmatch catches gen-10/drift.md; export still lists drift/sweep via SHAPE [tree de28690094e6] (2026-10-30T14:10:16Z)
- (audit adversary) `one fm-reviewer pass (intent/adversary/edge/maintainer); HIGH fixed, MEDIUM captured T-2163, LOW dropped` → forged exam.jsonl and Verdict: clean refused before any write [tree de28690094e6] (2026-10-30T14:10:16Z)
## Log
- 2026-10-30T13:50:59Z created
- 2026-10-30T13:51:13Z noticed by an agent (research T-2097-review): fm genesis put exam.jsonl` can rewrite the exam record that the selection and scorecard gates read (fmgenesis.py:72). That deserves its own task
- 2026-10-30T13:52:47Z set scope=['plugin/lib/fmgenesis.py', 'plugin/tests/test_genesis.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-30T13:52:48Z planned: it has criteria and steps
- 2026-10-30T13:57:45Z focused
- 2026-10-30T14:10:39Z done
- 2026-10-30T14:10:40Z committed 93cf6b98 (4 files)
- 2026-10-30T14:10:58Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2097-review: Verdict** — approve with nits. The scorecard logic is correct on the cases I traced. The real `fm genesis exam` path that feeds #13 has no test. …
- research T-2102-review: Verdict:** changes needed. Finding 1 is a MEDIUM that breaks the "seed N output passes step's seed-row rules (<= 8 rows)" MUST. I read the code a…
- T-2097 [FEATURE M, done, 3 steps] fm exam scorecard: per §2 capability, the held-out split's pass rate from graded runs,… — lesson: A gate that reads hand-written fixtur…
- decision 2026-10-30: T-2112: #13's draft kinds live in fmgenesis (fm genesis exam) reusing fmexam.draw/render and cover; G-tower is a 'genesis' session arm on fmexam's d…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_genesis.py
## Lessons
- A gate's evidence file must be writable only by the command that earns it: list every file a stage gate reads and refuse each in the generic writer, not just the one the finding named
## Plan gaps
- added late: widen to drift.md and sweep.md: OWNED regex refused by put, drift/sweep write via _file; MASTER, CHANGELOG
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
