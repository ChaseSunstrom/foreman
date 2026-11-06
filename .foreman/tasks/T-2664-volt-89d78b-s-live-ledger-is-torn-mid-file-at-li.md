---
id: T-2664
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-02T20:18:41Z
updated: 2026-11-02T20:23:21Z
base: 49f21d01d32771184e4ce9deec33b1a5103515cf
base_tree: df6a155e410c19014e937bb2feba159e578e4245
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T20:21:17Z
plan0_scope: []
verified: strong
---
# fm verify-ledger --accept-damage covers a line a crash cut short mid-file (chained on both sides); a cut last line stays broken
## Raw request
> volt-89d78b's live ledger is torn mid-file at line 24329 (a 2026-10-23 crash cut the line short; later appends start fresh lines), found by fm drill --restore. fm verify-ledger --accept-damage covers only zeroed lines, fm fsck sees only a torn tail, and fm doctor checks no other project's chain, so it went unreported for 10 days. Let --accept-damage record a cut-short mid-file line as a known gap when the next line starts whole, and have fsck name it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a chained line cut short at write time and followed by a chained line reads as crash damage that --accept-damage records once, after which verify passes and still names it; a cut last line stays broken — verify with `python3 plugin/tests/run.py test_ledger_chain`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] chain() takes a cut-short chained line as damage once a later line pins its bytes
3. [x] accept volt's line, CHANGELOG
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ledger_chain` → red as expected (exit 1) · Ran 36 tests in 4.5s (2 classes, 16 at a time; slowest: Chain 4s, Receipt 2s) / FAILED (1 classes: test_ledger_chain.Chain) [ran] [tree 15c014ef967e] [world 2f1906870a] (2026-11-02T20:21:35Z)
- (step 2) `python3 plugin/tests/run.py test_ledger_chain test_drill` → exit 0 · Ran 49 tests in 6.5s (5 classes, 16 at a time; slowest: Drill 6s, Chain 5s, Receipt 2s) / OK [ran] [tree b4e37733ad36] [world 2f1906870a] (2026-11-02T20:22:54Z)
- (step 3) `fm verify-ledger -p volt-89d78b` → exit 0 · Crash damage (accepted; the events written just before each were lost): ledger.jsonl:24329 (cut short at 96 bytes), ledger.jsonl:26529 (197 zero bytes) / 2 unchained line(s) after the start (an older [ran] [tree b4e37733ad36] [world 2f1906870a] (2026-11-02T20:22:54Z)
- (ac 1) `python3 plugin/tests/run.py test_ledger_chain` → exit 0 · Ran 36 tests in 4.7s (2 classes, 16 at a time; slowest: Chain 4s, Receipt 2s) / OK [ran] [tree b4e37733ad36] [world 2f1906870a] (2026-11-02T20:23:00Z)
- (audit edge) `self: the cut line must be chained (its prev checked) and a later chained line must hash-match it before it counts as damage, so an edit after the fact still breaks the next line's prev; a cut newest line stays broken (tested); keys use the same prev:hash scheme, so an ack can't cover a later cut` → a cut newest line is not acceptable (tested); an unchained non-JSON line still breaks; the zeroed path is unchanged (its 3 tests pass) [tree b4e37733ad36] (2026-11-02T20:23:00Z)
- (audit adversary) `self: the cut line must be chained (its prev checked) and a later chained line must hash-match it before it counts as damage, so an edit after the fact still breaks the next line's prev; a cut newest line stays broken (tested); keys use the same prev:hash scheme, so an ack can't cover a later cut` → truncating a mid-file line changes its hash, so the next line's prev no longer matches and verify says 'doesn't follow'; only bytes the next write chained to are accepted [tree b4e37733ad36] (2026-11-02T20:23:00Z)
- (audit self) `self: the cut line must be chained (its prev checked) and a later chained line must hash-match it before it counts as damage, so an edit after the fact still breaks the next line's prev; a cut newest line stays broken (tested); keys use the same prev:hash scheme, so an ack can't cover a later cut` → no findings [tree b4e37733ad36] (2026-11-02T20:23:00Z)
## Log
- 2026-11-02T20:18:41Z created
- 2026-11-02T20:21:16Z planned from capture
- 2026-11-02T20:21:17Z focused
- 2026-11-02T20:21:17Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T20:22:55Z scope: CHANGELOG.md
- 2026-11-02T20:23:19Z done
- 2026-11-02T20:23:21Z committed 20487138 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1456 [SECURITY M, done, 3 steps] Ledger names crash damage and accepts it once — lesson: A tamper-evident chain needs a defined, explicit path through accidental damag…
- T-1669 [FEATURE M, done, 4 steps] Fm drill: compound fault days in a temp home, promotion by false-positive rate (from T-155 — lesson: A corrupt meta.json hides its proj…
- research T-1456-review: Verdict: changes needed.** One HIGH adversary finding. I could not run code (read-only, no shell), so each finding is proved by tracing `fmledger…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
## Files touched
- plugin/tests/test_ledger_chain.py
- plugin/lib/fmledger.py
- CHANGELOG.md
