---
id: T-2409
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmexam.py, plugin/lib/fmgenesis.py]
depends_on: [T-2356, T-2406, T-2408]
source: user
created: 2026-10-31T14:33:39Z
updated: 2026-11-01T06:22:12Z
builder_model: sonnet
group: Mission 8 forecasting and watching
base: 92d693cfab4a012475063fd3df89954014b0eca2
base_tree: 071af625c50b6876509276367adf7a248dc442b4
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-01T05:55:26Z
plan0_scope: [plugin/lib/fmexam.py, plugin/lib/fmgenesis.py]
verified: strong
---
# #3 exam kinds forecast and breakage: next-request prediction against a naive baseline, and breakage flagged before it bites (Mission 8, #3)
## Raw request
> #3 exam kinds forecast and breakage: next-request prediction against a naive baseline, and breakage flagged before it bites (Mission 8, #3)
## Interpretation
Reading 1: two #3 exam kinds, forecast (next-request prediction beside a naive baseline) and breakage (a planted future failure flagged before a fake clock reaches it, with a clean twin). Reading 2: grade only the user's own request stream. Rejected: one stream and no child-authored held-out third.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam gen renders forecast scenarios (9, 3 held out; the child writes the stream and the hidden next request) graded on type hit and path overlap beside the naive baseline's, and a zero-token replay of the user's own request stream with its last third held out; oracle 100%, empty 0 — verify with `python3 plugin/tests/run.py test_exam`
- [x] fm exam gen renders breakage scenarios (9, 3 held out) with a planted future failure and a clean twin, graded on flagged before a fake clock reaches it and on false alarms on the twin; oracle 100%, empty 0 — verify with `python3 plugin/tests/run.py test_exam`
- [x] The scorecard maps #3 to forecast and breakage, not bug — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
1) forecast: the child writes a request stream (12-20 requests with a pattern) and the hidden next request; the arm sees the prefix and predicts; graded on type hit and path overlap beside the baseline's; a zero-token replay arm also runs the user's own stream in time order with its last third held out. breakage: a repo with a planted future failure (a date-bound check, a stale co-change partner, a growing file nearing a limit) and a clean twin; graded on flagged before the fake clock reaches it and on false alarms on the twin. Fails if: the child's pattern is too easy, which the baseline column exposes. 2) Use what exists: the user's own stream only, replayed through the tick's predictor. Likely outcome: no held-out child-authored set. 3) Do less: forecast only. Fails if: breakage warnings, half of #3, stay ungraded. 4) Grade the prose quality of the prediction. Breaks as proof: it is a format check. Choice 1 (80%): two keys and a baseline.
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md, plugin/tests/test_exam.py, plugin/lib/fmcli.py; past FIXes T-2083, T-2084, T-2100, T-2101, T-2103.
## Execution prompt
## Steps
1. [x] blocked on T-2356 (the replay arm runs the tick's predictor and detectors) and on briefs 18 and 20; start once they are done
2. [x] red tests: both renders and keys; baseline beside the arm; fake clock; oracle and empty; scorecard row
3. [x] the two kinds and the replay arm in fmexam; the mapping
4. [x] docs: MASTER exam line, CHANGELOG
## Resume here
## Docs impact
MASTER.md (fmexam T-2409), CHANGELOG.md Unreleased
## Verification evidence
- (step 1) `for t in T-2356 T-2406 T-2408; do fm task show $t --json | grep -o '"status": "[a-z]*"' | head -1; done` → exit 0 · "status": "done" / "status": "done" [ran] [tree 071af625c50b] (2026-11-01T05:55:29Z)
- (step 2) `python3 plugin/tests/run.py test_exam -k ForecastKind -k BreakageKind test_genesis -k test_anticipation_maps` → ✗ exit 1 · Ran 8 tests in 2.1s (3 classes, 16 at a time; slowest: ForecastKind 2s, BreakageKind 1s, GenesisDraft 0s) / FAILED (3 classes: test_exam.ForecastKind, test_exam.BreakageKind, test_genesis.GenesisDraft [ran] [tree 564dffffbe1c] (2026-11-01T05:55:53Z)
- (step 3) `python3 plugin/tests/run.py test_exam test_genesis test_foresight` → exit 0 · Ran 290 tests in 140.9s (46 classes, 16 at a time; slowest: LeanKind 125s, ExamAuthors 91s, JudgmentKinds 83s) / OK [ran] [tree cddad9c9310c] (2026-11-01T06:00:53Z)
- (step 4) `python3 plugin/tests/run.py test_docs; grep -c 'T-2409 (#3)' MASTER.md; grep -c 'exam kinds forecast and breakage' CHANGELOG.md` → exit 0 · 1 / 1 [ran] [tree ffd00b3231ff] (2026-11-01T06:02:50Z)
- (ac 1) `python3 plugin/tests/run.py test_exam -k ForecastKind` → exit 0 · Ran 4 tests in 6.8s (1 classes, 16 at a time; slowest: ForecastKind 6s) / OK [ran] [tree ffd00b3231ff] (2026-11-01T06:02:58Z)
- (ac 2) `python3 plugin/tests/run.py test_exam -k BreakageKind` → exit 0 · Ran 3 tests in 4.5s (1 classes, 16 at a time; slowest: BreakageKind 4s) / OK [ran] [tree ffd00b3231ff] (2026-11-01T06:03:03Z)
- (ac 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 176 tests in 10.7s (18 classes, 16 at a time; slowest: GenesisRead 10s, GenesisCheck 8s, GenesisSweep 8s) / OK [ran] [tree ffd00b3231ff] (2026-11-01T06:03:14Z)
- `python3 plugin/tests/run.py test_exam -k ForecastKind -k BreakageKind` → ✗ exit 1 · Ran 7 tests in 2.3s (2 classes, 16 at a time; slowest: ForecastKind 1s, BreakageKind 0s) / FAILED (2 classes: test_exam.ForecastKind, test_exam.BreakageKind) (start tree + this task's tests) [ran] [tree ffd00b3231ff] (2026-11-01T06:03:25Z)
- `python3 plugin/tests/run.py test_exam -k ForecastKind -k BreakageKind` → exit 0 · Ran 7 tests in 3.3s (2 classes, 16 at a time; slowest: ForecastKind 3s, BreakageKind 3s) / OK [ran] [tree ffd00b3231ff] (2026-11-01T06:03:25Z)
- (step 3) `python3 plugin/tests/run.py test_exam test_genesis test_foresight test_find` → exit 0 · Ran 411 tests in 115.3s (66 classes, 16 at a time; slowest: ExamAuthors 91s, JudgmentKinds 90s, LeanKind 89s) / OK [ran] [tree 9004f7a4ac05] (2026-11-01T06:11:31Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 88 tests in 78.9s (22 classes, 16 at a time; slowest: LeanKind 79s, ExamAuthors 78s, JudgmentKinds 71s) / OK [ran] [tree 9004f7a4ac05] (2026-11-01T06:18:38Z)
- (ac 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 88 tests in 78.9s (22 classes, 16 at a time; slowest: LeanKind 79s, ExamAuthors 78s, JudgmentKinds 71s) / OK [ran] [tree 9004f7a4ac05] (2026-11-01T06:18:38Z)
- (ac 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 176 tests in 9.4s (18 classes, 16 at a time; slowest: GenesisRead 9s, GenesisSweep 8s, GenesisCheck 7s) / OK [ran] [tree 9004f7a4ac05] (2026-11-01T06:18:38Z)
- (step 2) `python3 plugin/tests/run.py test_exam -k ForecastKind -k BreakageKind test_genesis -k test_anticipation_maps` → exit 0 · Ran 8 tests in 3.2s (3 classes, 16 at a time; slowest: ForecastKind 3s, BreakageKind 3s, GenesisDraft 0s) / OK [ran] [tree 9004f7a4ac05] (2026-11-01T06:18:38Z)
- (audit intent) `fm check exit 0 (5519 tests); 8 red→green tests (both renders and their keys, 9/3 held out, every language, oracle closes, empty doesn't, the foresight arm through Foreman's own tick, child streams and lines with their drops, the replay with its last third held out, the scorecard row); fm task prove proved; a real zero-token run s11-012: forecast type 8/9 vs the baseline's 0/9 (the miss was PERF vs PERFORMANCE, fixed), breakage 9/9 flagged early, 0 false alarms; replay of this user's 376 held-out requests: type 259 vs 256, paths 0.052 vs 0.086 (captured T-2449)` → #3 now has its own held-out exam kinds graded beside a naive baseline, a zero-token arm that runs the tick's predictor and detectors, and the user's own stream replayed; the scorecard maps #3 to them [tree 9004f7a4ac05] (2026-11-01T06:18:38Z)
- (audit adversary) `fm check exit 0 (5519 tests); 8 red→green tests (both renders and their keys, 9/3 held out, every language, oracle closes, empty doesn't, the foresight arm through Foreman's own tick, child streams and lines with their drops, the replay with its last third held out, the scorecard row); fm task prove proved; a real zero-token run s11-012: forecast type 8/9 vs the baseline's 0/9 (the miss was PERF vs PERFORMANCE, fixed), breakage 9/9 flagged early, 0 false alarms; replay of this user's 376 held-out requests: type 259 vs 256, paths 0.052 vs 0.086 (captured T-2449)` → child text is c.plain'd with @ stripped, paths must be relative without .., config names are a fixed pattern; the replay arm strips credentials (fmbench.CREDENTIALS), runs in a throwaway home with FOREMAN_NO_NET; hidden keys stay outside repo/ and the clean render [tree 9004f7a4ac05] (2026-11-01T06:18:38Z)
- (audit edge) `fm check exit 0 (5519 tests); 8 red→green tests (both renders and their keys, 9/3 held out, every language, oracle closes, empty doesn't, the foresight arm through Foreman's own tick, child streams and lines with their drops, the replay with its last third held out, the scorecard row); fm task prove proved; a real zero-token run s11-012: forecast type 8/9 vs the baseline's 0/9 (the miss was PERF vs PERFORMANCE, fixed), breakage 9/9 flagged early, 0 false alarms; replay of this user's 376 held-out requests: type 259 vs 256, paths 0.052 vs 0.086 (captured T-2449)` → a child stream whose next type has no transition out of the last is dropped; a line with its own date is dropped; a warning without a day counts as today; the twin flagged is a false alarm; fm find's secrets finder no longer sees the template's planted key as a credential (captured T-2450) [tree 9004f7a4ac05] (2026-11-01T06:18:38Z)
- (ac 2) `python3 plugin/tests/run.py test_exam -k BreakageKind` → exit 0 · Ran 3 tests in 3.0s (1 classes, 16 at a time; slowest: BreakageKind 3s) / OK [ran] [tree 21a1ceae8531] (2026-11-01T06:20:28Z)
- (audit intent) `fm check exit 0 (5519 tests; the stub's key rename after it re-ran BreakageKind green); 8 red→green tests (both renders and keys, 9/3 held out, every language, oracle closes, empty doesn't, the foresight arm through Foreman's own tick, child streams and lines with their drops, the replay with its last third held out, the scorecard row); fm task prove proved; real zero-token run s11-012: forecast type 8/9 vs the baseline's 0/9 (the miss was PERF vs PERFORMANCE, fixed), breakage 9/9 flagged early, 0 false alarms; replay of this user's 376 held-out requests: type 259 vs 256, paths 0.052 vs 0.086 (captured T-2449)` → #3 now has its own held-out exam kinds graded beside a naive baseline, a zero-token arm that runs the tick's predictor and detectors, and the user's own stream replayed; the scorecard maps #3 to them [tree 21a1ceae8531] (2026-11-01T06:20:30Z)
- (audit adversary) `fm check exit 0 (5519 tests; the stub's key rename after it re-ran BreakageKind green); 8 red→green tests (both renders and keys, 9/3 held out, every language, oracle closes, empty doesn't, the foresight arm through Foreman's own tick, child streams and lines with their drops, the replay with its last third held out, the scorecard row); fm task prove proved; real zero-token run s11-012: forecast type 8/9 vs the baseline's 0/9 (the miss was PERF vs PERFORMANCE, fixed), breakage 9/9 flagged early, 0 false alarms; replay of this user's 376 held-out requests: type 259 vs 256, paths 0.052 vs 0.086 (captured T-2449)` → child text is c.plain'd with @ stripped, paths must be relative without .., config names a fixed pattern; the replay arm strips credentials (fmbench.CREDENTIALS) and runs in a throwaway home with FOREMAN_NO_NET; hidden keys stay outside repo/ and the clean render [tree 21a1ceae8531] (2026-11-01T06:20:30Z)
- (audit edge) `fm check exit 0 (5519 tests; the stub's key rename after it re-ran BreakageKind green); 8 red→green tests (both renders and keys, 9/3 held out, every language, oracle closes, empty doesn't, the foresight arm through Foreman's own tick, child streams and lines with their drops, the replay with its last third held out, the scorecard row); fm task prove proved; real zero-token run s11-012: forecast type 8/9 vs the baseline's 0/9 (the miss was PERF vs PERFORMANCE, fixed), breakage 9/9 flagged early, 0 false alarms; replay of this user's 376 held-out requests: type 259 vs 256, paths 0.052 vs 0.086 (captured T-2449)` → a child stream whose next type has no transition out of the last is dropped; a line with its own date is dropped; a warning without a day counts as today; the twin flagged is a false alarm; a date under a secret-like key read as a credential by fm find and the credential check (captured T-2450) [tree 21a1ceae8531] (2026-11-01T06:20:30Z)
## Log
- 2026-10-31T14:33:39Z created
- 2026-10-31T16:08:17Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2409.builder.md
- 2026-10-31T16:08:18Z builder slot freed
- 2026-10-31T16:11:43Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2409.builder.md
- 2026-10-31T16:11:43Z builder slot freed
- 2026-11-01T05:55:25Z focused
- 2026-11-01T05:55:26Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-01T06:01:54Z hypothesis: the one forecast miss (got PERFORMANCE, want PERF) is fm task new normalizing PERF; the exam's type list must be c.TYPES. Rules out a predictor error: the stream was a clean 3-cycle
- 2026-11-01T06:03:26Z scope: plugin/tests/test_exam.py and test_genesis.py (tests and the child stub), plugin/lib/fmforesight.py (predict() shared by the tick and the replay; breakage_tick honours FOREMAN_TODAY for the replay's fake clock), MASTER.md and CHANGELOG.md (docs)
- 2026-11-01T06:09:36Z fix: fm find's secrets finder read the template's token_expires = "<date>" as a credential, so the clean breakage render wasn't clean (test_find.FindRenders); the planted key is licence_expires, and the child prompt asks for a name that isn't a token, key or password
- 2026-11-01T06:20:24Z scope: plugin/tests/test_exam.py and test_genesis.py (tests and the child stub; the stub's key renamed cert_expires so the credential check doesn't read a date as a secret, T-2450), plugin/lib/fmforesight.py (predict() shared by the tick and the replay; breakage_tick honours FOREMAN_TODAY), MASTER.md and CHANGELOG.md (docs)
- 2026-11-01T06:22:10Z done
- 2026-11-01T06:22:12Z committed 08ff330f (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2406 [FEATURE M, done, 4 steps] Prediction book: Foreman predicts the user's next request from their own request stream and scores each against a naive baseline (Missi…
- research T-2126-review: Changes needed. The new exam code works as tested. But adding two kinds to `fmexam.KINDS` changes an existing Genesis exam in fmgenesis.py, which…
- T-2126 [FEATURE M, done, 2 steps] #1 held-out exam: I-none, I-clean, I-rank child-authored kinds; finders, foreman and plain arms (Mission 3 brief 7) — lesson: a module-…
- decision 2026-10-30: [cites: user steer 2026-10-30] Standing rule (user steer): weakness-finding uses signals Foreman didn't author — outcome survival (fm outcomes: reve…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_exam.py, plugin/tests/test_genesis.py
## Preflight
Changed in scope since this was planned (2026-10-31): plugin/lib/fmexam.py, plugin/lib/fmgenesis.py; re-ground the plan against them before editing
## Lessons
- Replay a predictor on the user's own history before trusting its scores: template streams passed 8/9 while the real stream showed the path guess trailing the naive baseline
## Plan gaps
- failed first: step 2 red tests: both renders and keys; baseline beside the arm; fake clock; oracle and empty; scorecard …
## Files touched
- plugin/tests/test_exam.py
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- plugin/lib/fmforesight.py
- plugin/lib/fmexam.py
- CHANGELOG.md
- MASTER.md
