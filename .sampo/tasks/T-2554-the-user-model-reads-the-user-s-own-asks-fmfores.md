---
id: T-2554
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmforesight.py, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/lib/fmexam.py, plugin/tests/test_foresight.py, plugin/tests/test_cli.py, plugin/tests/test_genesis.py, plugin/tests/test_exam.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-11-02T06:11:12Z
updated: 2026-11-02T06:48:17Z
base: 1c7e9227a0b72fb5f5b7c96ff80346e1411e93d9
base_tree: 3d1bbcebcaa0d049f77dc4aec636971fa2d383a5
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-02T06:15:26Z
plan0_scope: [plugin/lib/fmforesight.py, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/lib/fmexam.py, plugin/tests/test_foresight.py, plugin/tests/test_cli.py, plugin/tests/test_genesis.py, plugin/tests/test_exam.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# The user model reads only the user's own asks: Mission briefs and mistaken captures left out of fmforesight._requests; fm intake --source genesis
## Raw request
> FEATURE: the user model reads the user's own asks: fmforesight._requests leaves out briefs a Genesis Mission's Task line names and briefs dropped as captured by mistake; fm intake --source genesis files the tower's briefs as its own and the Genesis step's intake line uses it; a walk-forward replay of the prediction book on both streams must not score lower with the cleaned one
## Interpretation
Reading 1: the next-request predictor and the lane plan learn only from requests the user made: Genesis Mission briefs (Foreman-written, filed by fm intake) and captures dropped as mistakes are left out, and new Mission briefs are filed under their own source. Reading 2: relabel every old brief's source in place. Chosen: 1; 2 rewrites 1,164 briefs for what one reader can filter.
## Assumptions (confidence)
## Acceptance criteria
- [x] fmforesight._requests leaves out a brief a Genesis Mission's Task line names and a brief dropped as captured by mistake; clean=False keeps the old stream — verify with `python3 plugin/tests/run.py test_foresight`
- [x] fm intake --source genesis files its briefs with source genesis, and fm genesis step's intake line says --source genesis — verify with `python3 plugin/tests/run.py test_cli test_genesis`
- [x] fmexam.replay_forecast reports the cleaned stream and the raw one side by side; the walk-forward result on this project is recorded in the task log and the cleaned stream's type hit rate is not lower — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
1. Filter at the one reader: _requests(p, clean=True) leaves out ids from every Mission's Task paragraph (fmgenesis.TASKS) and briefs whose drop note says by mistake/accident; fm intake --source; the Genesis intake line uses --source genesis. Likely outcome: the replay's type hit rate holds or rises on a stream of real asks; fails if: a Mission brief the user adopted drops out (the user's own words still come through capture). 2. use what exists: TASKS, drop notes and replay_forecast (T-2409) are there; 1 wires them. Likely outcome: same as 1, built this way. 3. Relabel sources in place. Fails if: a large irreversible edit to briefs other tools read. 4. do less: only --source for new intakes. Fails if: 40-plus old Mission briefs and 72 mistakes keep polluting. Choice 1 (80%).
## Risks and rollback
Scanning every Mission file on each _requests call costs a few file reads, only in the tick, the exam and fmdraft (never a hook path; fmhooks:754 calls a different _requests). Rollback: clean=False restores the old stream; the flag is additive.
Blast radius (fm graph blast): co-changes plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/lib/fmguard.py, README.md, plugin/tests/test_guard.py; past FIXes T-0875, T-0876, T-0880, T-0908, T-0926.
## Execution prompt
## Steps
1. [x] red tests: test_foresight (Mission-named and mistake-dropped briefs left out; clean=False keeps them), test_cli (intake --source), test_genesis (the intake line), test_exam (replay raw beside clean)
2. [x] fmforesight._requests(p, clean=True): leave out ids from every gen-*/mission-*.md Task paragraph (fmgenesis.TASKS) and briefs whose drop note says by mistake/by accident; fm intake --source; fmgenesis intake act names --source genesis; replay_forecast returns raw beside clean
3. [x] walk-forward on this project: fm exam run --agent foresight's forecast replay, both streams; log the numbers
## Resume here
## Docs impact
MASTER (fmforesight entry), CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_foresight.OwnAsks test_cli.CaptureAndIntake.test_intake_source_files_the_briefs_under_it` → ✗ exit 1 · Ran 2 tests in 0.7s (2 classes, 16 at a time; slowest: OwnAsks 0s, CaptureAndIntake 0s) / FAILED (2 classes: test_cli.CaptureAndIntake, test_foresight.OwnAsks) [ran] [tree 9f855b335e9b] [world 2f1906870a] (2026-11-02T06:15:42Z)
- (step 2) `python3 plugin/tests/run.py test_foresight test_cli` → exit 0 · Ran 176 tests in 20.9s (52 classes, 16 at a time; slowest: TaskLifecycle 21s, CaptureAndIntake 9s, StateViews 9s) / OK [ran] [tree 6be8ae6fa74c] [world 2f1906870a] (2026-11-02T06:16:33Z)
- (step 2) `python3 plugin/tests/run.py test_foresight test_cli test_genesis test_exam` → exit 0 · Ran 477 tests in 157.4s (97 classes, 16 at a time; slowest: LeanKind 138s, ExamAuthors 87s, JudgmentKinds 85s) / OK [ran] [tree 52230df0c1ee] [world 2f1906870a] (2026-11-02T06:19:44Z)
- (step 3) `fm exam run s0-014 --agent foresight --json | python3 -c "import json,sys; d=json.load(sys.stdin); a,b=d['forecast_replay'],d['forecast_replay_raw']; print('clean',a); print('raw',b); assert a['held']==b['held'] and a['type_hit']>=b['type_hit'] and a['overlap']>=b['overlap']"` → exit 0 · clean {'held': 331, 'type_hit': 201, 'base_type_hit': 196, 'overlap': 0.118, 'base_overlap': 0.116} / raw {'held': 331, 'type_hit': 201, 'base_type_hit': 196, 'overlap': 0.113, 'base_overlap': 0.113} [ran] [tree 59f1fa28d6f8] [world 2f1906870a] (2026-11-02T06:20:53Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 31 tests in 8.4s (8 classes, 16 at a time; slowest: PredictionBook 8s, DraftAhead 3s, BreakageWarnings 1s) / OK [ran] [tree e57180086acc] [world 2f1906870a] (2026-11-02T06:30:25Z)
- (ac 2) `python3 plugin/tests/run.py test_cli test_genesis` → exit 0 · Ran 352 tests in 27.1s (67 classes, 16 at a time; slowest: TaskLifecycle 27s, GenesisRead 19s, GenerationReview 17s) / OK [ran] [tree e57180086acc] [world 2f1906870a] (2026-11-02T06:30:25Z)
- (ac 3) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 94 tests in 117.5s (23 classes, 16 at a time; slowest: LeanKind 117s, ExamAuthors 97s, JudgmentKinds 78s) / OK [ran] [tree e57180086acc] [world 2f1906870a] (2026-11-02T06:30:25Z)
- (step 1) `python3 plugin/tests/run.py test_foresight.OwnAsks test_cli.CaptureAndIntake.test_intake_source_files_the_briefs_under_it` → exit 0 · Ran 2 tests in 1.2s (2 classes, 16 at a time; slowest: OwnAsks 1s, CaptureAndIntake 0s) / OK [ran] [tree e57180086acc] [world 2f1906870a] (2026-11-02T06:30:25Z)
- (audit intent) `self-review: the filter sits at fmforesight._requests, the one reader the prediction book, the lane plan and fmdraft share; clean=False is the old stream; the replay scores both histories on the same held-out user asks` → the user model learns the user's own asks; the tower's Mission briefs and mistaken captures no longer read as the user's habits, and new Mission briefs are filed as genesis [tree e57180086acc] (2026-11-02T06:30:25Z)
- (audit edge) `self-review: the filter sits at fmforesight._requests, the one reader the prediction book, the lane plan and fmdraft share; clean=False is the old stream; the replay scores both histories on the same held-out user asks` → a project with no genesis folder pays no fmgenesis import; a brief dropped for another reason (not a mistake) stays in; a Mission naming an id twice is one skip; the first replay compared different held-out sets and was rebuilt before the verdict [tree e57180086acc] (2026-11-02T06:30:25Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 9581b1432c10] [world 2f1906870a] (2026-11-02T06:48:17Z)
## Log
- 2026-11-02T06:11:12Z created
- 2026-11-02T06:12:09Z planned from capture
- 2026-11-02T06:12:19Z set approved=True
- 2026-11-02T06:15:25Z focused
- 2026-11-02T06:15:26Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-02T06:20:53Z backtest (fm exam run s0-014 --agent foresight, both histories on the same 331 held-out user asks): type hits clean 201 vs raw 201 (baseline 196 both); path overlap clean 0.118 vs raw 0.113 (baselines 0.116 / 0.113). An earlier comparison on different held-out sets (331 vs 388) was not the Mission's test and was replaced
- 2026-11-02T06:21:08Z scope: fmforesight._requests clean + _tower_ids/_SLIP; fmcli intake --source; fmgenesis intake act; fmexam.replay_forecast same held-out asks for both histories and forecast_replay_raw; tests in test_foresight, test_cli, test_genesis, test_exam; MASTER fmforesight entry; CHANGELOG
- 2026-11-02T06:33:47Z done
- 2026-11-02T06:33:56Z committed d9c20ac2 (10 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2409 [FEATURE M, done, 4 steps] #3 exam kinds forecast and breakage: next-request prediction against a naive baseline, and breakage flagged before it bites (Mission 8,…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2471 [FEATURE L, done, 3 steps] Cold read made reliable: Haiku first and Sonnet decides on a non-pass, a FAIL counts only with the quoted line and the MUST/NEVER or st…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_exam.py, plugin/tests/test_foresight.py, plugin/tests/test_genesis.py
## Lessons
- compare two variants of a predictor on the same evaluation set, fixed before either runs; different held-out sets made the polluted stream look 10 points better
## Plan gaps
- failed first: step 1 red tests: test_foresight (Mission-named and mistake-dropped briefs left out; clean=False keeps the…
## Files touched
- plugin/tests/test_cli.py
- plugin/tests/test_foresight.py
- plugin/lib/fmcli.py
- plugin/lib/fmforesight.py
- plugin/lib/fmexam.py
- plugin/lib/fmgenesis.py
- plugin/tests/test_genesis.py
- plugin/tests/test_exam.py
- CHANGELOG.md
- MASTER.md
