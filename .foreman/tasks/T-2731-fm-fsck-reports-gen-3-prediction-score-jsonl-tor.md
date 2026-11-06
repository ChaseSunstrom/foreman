---
id: T-2731
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-03T00:20:04Z
updated: 2026-11-03T00:25:25Z
base: 1949f2acfcd8bd63990ee4495a41dfa71d04883e
base_tree: 9348380af51e2410252b973cca2452d1dc2fe253
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-03T00:20:15Z
plan0_scope: []
verified: strong
---
# c.append_line ends a non-empty text with a newline, so no writer can leave a journal torn (gen-3/prediction-score.jsonl was, from fmgenesis.py:3695)
## Raw request
> fm fsck reports gen-3/prediction-score.jsonl torn: fmgenesis.py:3695 appends a row without its newline; c.append_line promises whole lines, so it should end a non-empty text with one (fixes every caller)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] append_line('x') leaves the file ending in a newline, append_line('') adds none, and fm fsck finds no torn journal after a prediction score is written — verify with `python3 plugin/tests/run.py test_core`
- [x] fm fsck --fix mends a non-ledger journal whose whole last record lacks only its newline, leaves a mid-record cut and the ledger alone, and says 'mended' — verify with `python3 plugin/tests/run.py test_reliability_tools`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] the newline in append_line
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_drill test_reliability_tools` → exit 0 · Ran 32 tests in 11.5s (5 classes, 16 at a time; slowest: Drill 11s, Fsck 7s, StateErrors 3s) / OK [ran] [tree 58493f86759d] [world 2f1906870a] (2026-11-03T00:22:59Z)
- (step 2) `python3 plugin/tests/run.py test_drill test_reliability_tools` → exit 0 · Ran 32 tests in 10.0s (5 classes, 16 at a time; slowest: Drill 10s, Fsck 6s, RestoreDrill 2s) / OK [ran] [tree 58493f86759d] [world 2f1906870a] (2026-11-03T00:23:09Z)
- (step 3) `python3 plugin/tests/run.py test_drill test_reliability_tools` → exit 0 · Ran 32 tests in 10.5s (5 classes, 16 at a time; slowest: Drill 10s, Fsck 7s, RestoreDrill 2s) / OK [ran] [tree 58493f86759d] [world 2f1906870a] (2026-11-03T00:23:21Z)
- `python3 plugin/tests/run.py test_drill test_reliability_tools` → ✗ exit 1 · Ran 32 tests in 11.4s (5 classes, 16 at a time; slowest: Drill 9s, Fsck 6s, StateErrors 3s) / FAILED (2 classes: test_reliability_tools.Fsck, test_drill.StateErrors) (start tree + this task's tests) [ran] [tree 58493f86759d] [world 2f1906870a] (2026-11-03T00:23:43Z)
- `python3 plugin/tests/run.py test_drill test_reliability_tools` → exit 0 · Ran 32 tests in 10.0s (5 classes, 16 at a time; slowest: Drill 10s, Fsck 6s, RestoreDrill 2s) / OK [ran] [tree 58493f86759d] [world 2f1906870a] (2026-11-03T00:23:43Z)
- (ac 1) `python3 plugin/tests/run.py test_core` → exit 0 · Ran 138 tests in 11.1s (28 classes, 16 at a time; slowest: ConfidenceRoutes 11s, BriefIndex 4s, RoundFirst 2s) / OK [ran] [tree 58493f86759d] [world 2f1906870a] (2026-11-03T00:24:25Z)
- (ac 2) `python3 plugin/tests/run.py test_reliability_tools` → exit 0 · Ran 19 tests in 7.8s (2 classes, 16 at a time; slowest: Fsck 7s, GateLock 1s) / OK [ran] [tree 58493f86759d] [world 2f1906870a] (2026-11-03T00:24:25Z)
- `python3 plugin/tests/run.py test_drill test_reliability_tools test_core` → exit 0 · Ran 170 tests in 15.4s (33 classes, 16 at a time; slowest: Drill 15s, ConfidenceRoutes 14s, Fsck 9s) / OK [ran] [tree 58493f86759d] [world 2f1906870a] (2026-11-03T00:24:25Z)
- (audit adversary) `append_line now ends non-empty text with a newline (fmdrill's append_line('') still adds nothing to a whole tail); fsck --fix mends only a non-ledger journal whose last record parses whole and lacks the newline, re-reading the tail; a mid-record cut and the ledger stay for a person; the live gen-3 prediction-score.jsonl was mended and fm fsck now reads OK` → the repair appends one newline and never rewrites; ledger.jsonl is excluded by name, so the hash chain is untouched (asserted) [tree 58493f86759d] (2026-11-03T00:24:25Z)
- (audit edge) `append_line now ends non-empty text with a newline (fmdrill's append_line('') still adds nothing to a whole tail); fsck --fix mends only a non-ledger journal whose last record parses whole and lacks the newline, re-reading the tail; a mid-record cut and the ledger stay for a person; the live gen-3 prediction-score.jsonl was mended and fm fsck now reads OK` → a file whose last record is JSON but is still being written (a writer mid-append) is mended only if it parses whole; append_line writes in one call, so a half record can't parse [tree 58493f86759d] (2026-11-03T00:24:25Z)
- (audit self) `append_line now ends non-empty text with a newline (fmdrill's append_line('') still adds nothing to a whole tail); fsck --fix mends only a non-ledger journal whose last record parses whole and lacks the newline, re-reading the tail; a mid-record cut and the ledger stay for a person; the live gen-3 prediction-score.jsonl was mended and fm fsck now reads OK` → no findings [tree 58493f86759d] (2026-11-03T00:24:25Z)
## Log
- 2026-11-03T00:20:04Z created
- 2026-11-03T00:20:13Z planned from capture
- 2026-11-03T00:20:14Z focused
- 2026-11-03T00:20:15Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-03T00:22:46Z scope: plugin/lib/fmdoctor.py (fsck_fix's newline repair and its wording), plugin/tests/test_reliability_tools.py, CHANGELOG.md; the live gen-3/prediction-score.jsonl mended by fm fsck --fix
- 2026-11-03T00:25:22Z done
- 2026-11-03T00:25:25Z committed f01818ae (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2155 [SECURITY M, done, 3 steps] fm genesis put exam.jsonl can overwrite the exam record that fm genesis select and fm… — lesson: A gate's evidence file must be writab…
- research T-1667-review: Verdict: changes needed.** One MEDIUM and one more MEDIUM-ish lead, both small to fix. I could only read files (no shell), so I did not run the t…
- T-1667 [FEATURE M, done, 3 steps] fm fsck: a read-only report of broken worktrees, stale locks and torn journals, --fix for the safe repairs — lesson: A dead-pid check i…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
## Why not caught
fmgenesis's prediction scorer was the only append_line caller without the newline, and nothing checked a journal's tail after a write in tests
## Files touched
- plugin/tests/test_drill.py
- plugin/lib/fmcore.py
- plugin/lib/fmdoctor.py
- plugin/tests/test_reliability_tools.py
- CHANGELOG.md
