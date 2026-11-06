---
id: T-2681
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: genesis
created: 2026-11-02T22:12:01Z
updated: 2026-11-02T22:31:51Z
builder_model: sonnet
base: 9ff9c5240d7b577230ffb1bbbd35348f8efa1bdf
base_tree: 3995584de8490c53b2226b763cd34ed51cb913ac
predict_minutes: 7
predict_attempts: 1
plan0_at: 2026-11-02T22:12:56Z
plan0_scope: []
lane_stop: merged 2026-11-02T22:28:56Z
verified: strong
---
# fmforesight.lines shows the newest unscored next-request prediction at session start while it beats its baseline and isn't muted, and the book records that it was shown
## Raw request
> FEATURE: fmforesight.lines shows the newest unscored next-request prediction (type and top paths) at session start only while prediction_kinds shows it beating its baseline and not muted, and the book records that it was shown
> CONTEXT: Genesis gen-3 Mission 7 (#3 anticipation), gen-3/mission-anticipation.md
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with a booked, unscored next-request row and the kind beating its baseline, fmforesight.lines returns one line naming the type and top paths with both hit rates, and the row gains shown: true; muted or trailing, no line — verify with `python3 plugin/tests/run.py test_foresight`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] the line and the shown mark
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_foresight 2>&1 | tail -15` → ✗ exit 1 · Ran 34 tests in 10.1s (8 classes, 16 at a time; slowest: PredictionBook 8s, DraftAhead 3s, BreakageWarnings 1s) / FAILED (1 classes: test_foresight.PredictionBook) [ran] [tree 96ccb19c9d38] [world 2f1906870a] (2026-11-02T22:13:23Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight 2>&1 | tail -8` → exit 0 · Ran 34 tests in 8.9s (8 classes, 16 at a time; slowest: PredictionBook 8s, DraftAhead 3s, BreakageWarnings 1s) / OK [ran] [tree 5ce5f0c0ee11] [world 2f1906870a] (2026-11-02T22:13:37Z)
- (step 1) `python3 plugin/tests/run.py test_foresight 2>&1 | tail -8` → exit 0 · Ran 34 tests in 8.9s (8 classes, 16 at a time; slowest: PredictionBook 8s, DraftAhead 3s, BreakageWarnings 1s) / OK [ran] [tree 5ce5f0c0ee11] [world 2f1906870a] (2026-11-02T22:13:37Z)
- (step 2) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 34 tests in 9.0s (8 classes, 16 at a time; slowest: PredictionBook 9s, DraftAhead 3s, BreakageWarnings 1s) / OK [ran] [tree 5ce5f0c0ee11] [world 2f1906870a] (2026-11-02T22:13:50Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_foresight && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [23.22s] [ran] [tree 5ce5f0c0ee11] [world 2f1906870a] (2026-11-02T22:14:25Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight 2>&1 | grep -B3 -A12 "^FAIL\|^ERROR" | head -40` → ✗ exit 1 · Ran 36 tests in 8.5s (8 classes, 16 at a time; slowest: PredictionBook 8s, DraftAhead 3s, BreakageWarnings 1s) / FAILED (1 classes: test_foresight.PredictionBook) [ran] [tree 71f816101f4e] [world 2f1906870a] (2026-11-02T22:30:05Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 36 tests in 8.5s (8 classes, 16 at a time; slowest: PredictionBook 8s, DraftAhead 3s, BreakageWarnings 1s) / OK [ran] [tree 7196ba088990] [world 2f1906870a] (2026-11-02T22:30:59Z)
- (step 3) `python3 plugin/tests/run.py test_foresight test_outcomes test_left_out` → exit 0 · Ran 105 tests in 23.0s (26 classes, 16 at a time; slowest: Survival 23s, ModelRouter 15s, CalibrationLedgerBets 14s) / OK [ran] [tree 7196ba088990] [world 2f1906870a] (2026-11-02T22:30:59Z)
- (audit edge) `read _next_line and the shown split: newest unscored row only, kind must beat its baseline over MUTE_MIN+ scored rows and not be muted, never sensitive; a shown row is appended once per prediction id; real book (23 scored, 52% vs 39%) shows the line` → one lucky score on a fresh book shows nothing (MUTE_MIN floor, tested at 19 then 20); a prediction with no paths prints just its type [tree 7196ba088990] (2026-11-02T22:30:59Z)
- (audit operator) `read _next_line and the shown split: newest unscored row only, kind must beat its baseline over MUTE_MIN+ scored rows and not be muted, never sensitive; a shown row is appended once per prediction id; real book (23 scored, 52% vs 39%) shows the line` → fm outcomes --predictions prints 'shown at session start: N scored, hit X%' so the Mission's week-later reading needs no new verb [tree 7196ba088990] (2026-11-02T22:30:59Z)
- (audit self) `read _next_line and the shown split: newest unscored row only, kind must beat its baseline over MUTE_MIN+ scored rows and not be muted, never sensitive; a shown row is appended once per prediction id; real book (23 scored, 52% vs 39%) shows the line` → no findings [tree 7196ba088990] (2026-11-02T22:30:59Z)
## Log
- 2026-11-02T22:12:01Z created
- 2026-11-02T22:12:36Z planned from capture
- 2026-11-02T22:12:38Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2681.builder.md
- 2026-11-02T22:12:55Z focused
- 2026-11-02T22:12:56Z predicted from its closes: 7 min, 1 attempt(s)
- 2026-11-02T22:28:56Z merged worktree-agent-a58fc814a21ba08c6 (2 file(s))
- 2026-11-02T22:28:56Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a58fc814a21ba08c6
- 2026-11-02T22:28:56Z focused
- 2026-11-02T22:30:24Z steer: added a MUTE_MIN (20 scored) floor before the line shows, c.joinmore on its paths (the left-out scan), and the shown-vs-all split in prediction_kinds and fm outcomes --predictions so the Mission's outcome measure can be read
- 2026-11-02T22:30:25Z scope: fmoutcomes.py (the --predictions line that reads shown guesses apart) and CHANGELOG.md
- 2026-11-02T22:31:46Z done
- 2026-11-02T22:31:51Z committed 1191a91c (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261102-m7: 393 ideas in 64 clusters, each grounded in the code: 34 built, 13 false-premise, 170 new, 176 partial. 16 clusters marked build.
- T-2406 [FEATURE M, done, 4 steps] Prediction book: Foreman predicts the user's next request from their own request stream and scores each against a naive baseline (Missi…
- T-2409 [FEATURE M, done, 4 steps] #3 exam kinds forecast and breakage: next-request prediction against a naive baseline, and breakage flagged before it bites (Mission 8,…
- decision 2026-11-02: Recommendation: Mission 7 builds four anticipation gaps where Foreman computes what the user will need but it never reaches them (the booked next-re…
## Files touched
- plugin/tests/test_foresight.py
- plugin/lib/fmforesight.py
- plugin/lib/fmoutcomes.py
- CHANGELOG.md
