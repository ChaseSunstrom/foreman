---
id: T-2408
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmforesight.py, plugin/lib/fmgraph.py]
depends_on: [T-2356]
source: user
created: 2026-10-31T14:33:37Z
updated: 2026-11-01T06:03:25Z
builder_model: sonnet
group: Mission 8 forecasting and watching
base: 7cb3bb1cd0d921c0be52d48baf7ca347aeb2c7b5
base_tree: a2d0ee62b17b5bf2336bb6fcc07520641bee4bff
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-01T05:44:36Z
plan0_scope: [plugin/lib/fmforesight.py, plugin/lib/fmgraph.py]
verified: strong
---
# fmforesight warns of breakage before it bites: dates about to pass, stale co-change partners, state growing toward its budget, each scored (Mission 8, #3)
## Raw request
> fmforesight warns of breakage before it bites: dates about to pass, stale co-change partners, state growing toward its budget, each scored (Mission 8, #3)
## Interpretation
Reading 1: zero-token detectors on the tick warn of breakage that has not happened: a date about to pass, a file changed without its usual co-change partner, state growing toward its budget, each scored by whether the failure or its fix landed in the window. Reading 2: a model reads the repo for risks. Rejected now: tokens per tick before cheap detectors are scored.
## Assumptions (confidence)
## Acceptance criteria
- [x] On the tick fmforesight files a warning, through the trigger table, for a literal date in tracked code, tests or config passing within 14 days, a commit that changed a file without its usual co-change partner, and state whose trend reaches its budget within 30 days; a clean repo files none — verify with `python3 plugin/tests/run.py test_foresight`
- [x] Each warning carries its window and is scored: a hit only when the failure is observed at the flagged target (a failed run naming the dated line or the stale partner, the state budget crossed) or a commit from a task not filed by this warning changes that target in the window; a fix filed from the warning itself counts as acted on, never as a hit; a miss when the window passes with neither; fm outcomes --predictions shows each kind's precision — verify with `python3 plugin/tests/run.py test_foresight`
## Non-goals
## Approach (options → choice → why)
1) Detectors on the tick (T-2356): literal dates in tracked code, tests and config that pass within 14 days; a commit that changed a file without its co-change partner (fm graph blast's history, 3+ past pairings); a state size whose 30-day trend reaches fmdoctor's state budget within 30 days; each files through the trigger table as foresight-KIND with its window; a warning is a hit when the predicted failure or a fix lands in the window; fm outcomes --predictions shows each kind's precision. Fails if: a detector is noisy, which scoring and the table's demotion handle. 2) Use what exists: fmforesight's current checks (CI red, changed versions, the blocked pile) and fm graph blast. Likely outcome: the gap is detectors that look forward, not new plumbing. 3) Do less: warn at session start only. Fails if: advice waits for a session. 4) A model reading the repo for risks. Breaks the token budget per tick. Choice 1 (80%): cheap detectors with a hit definition.
## Risks and rollback
Blast radius (fm graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/tests/test_graph.py, plugin/tests/test_foresight.py, plugin/lib/fmhooks.py; past FIXes T-1819.
## Execution prompt
## Steps
1. [x] blocked on T-2356 (the checks run on its tick); start once it is done
2. [x] red tests: each detector fires on a planted case and not on a clean twin; scoring by window
3. [x] the detectors in fmforesight; scoring in the book
4. [x] docs: MASTER, CHANGELOG
## Resume here
## Docs impact
MASTER.md (fmforesight T-2408), CHANGELOG.md Unreleased
## Verification evidence
- (step 1) `fm task show T-2356 --json | grep -o '"status": "[a-z]*"' | head -1` → exit 0 · "status": "done" [ran] [tree a2d0ee62b17b] (2026-11-01T05:44:38Z)
- (step 2) `python3 plugin/tests/run.py test_foresight -k BreakageWarnings` → ✗ exit 1 · Ran 5 tests in 0.6s (1 classes, 16 at a time; slowest: BreakageWarnings 0s) / FAILED (1 classes: test_foresight.BreakageWarnings) [ran] [tree e046be76c57c] (2026-11-01T05:44:44Z)
- (step 3) `python3 plugin/tests/run.py test_foresight test_outcomes test_serve` → exit 0 · Ran 117 tests in 15.9s (27 classes, 16 at a time; slowest: Run 16s, Survival 15s, ModelRouter 9s) / OK [ran] [tree 2651cc1e7fec] (2026-11-01T05:45:51Z)
- (step 3) `python3 plugin/tests/run.py test_foresight test_outcomes test_serve test_night` → exit 0 · Ran 152 tests in 16.8s (38 classes, 16 at a time; slowest: Run 17s, Survival 16s, ModelRouter 11s) / OK [ran] [tree 70397ccfa02f] (2026-11-01T05:46:51Z)
- (step 4) `python3 plugin/tests/run.py test_docs; grep -c 'breakage_tick' MASTER.md; grep -c 'Breakage warnings' CHANGELOG.md` → exit 0 · 1 / 1 [ran] [tree 071af625c50b] (2026-11-01T05:47:35Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 26 tests in 4.6s (6 classes, 16 at a time; slowest: PredictionBook 4s, DraftAhead 2s, BreakageWarnings 1s) / OK [ran] [tree 071af625c50b] (2026-11-01T05:47:40Z)
- (ac 2) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 26 tests in 4.6s (6 classes, 16 at a time; slowest: PredictionBook 4s, DraftAhead 2s, BreakageWarnings 1s) / OK [ran] [tree 071af625c50b] (2026-11-01T05:47:45Z)
- `python3 plugin/tests/run.py test_foresight -k BreakageWarnings` → ✗ exit 1 · Ran 5 tests in 1.6s (1 classes, 16 at a time; slowest: BreakageWarnings 0s) / FAILED (1 classes: test_foresight.BreakageWarnings) (start tree + this task's tests) [ran] [tree 071af625c50b] (2026-11-01T05:47:52Z)
- `python3 plugin/tests/run.py test_foresight -k BreakageWarnings` → exit 0 · Ran 5 tests in 0.8s (1 classes, 16 at a time; slowest: BreakageWarnings 1s) / OK [ran] [tree 071af625c50b] (2026-11-01T05:47:52Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 26 tests in 4.7s (6 classes, 16 at a time; slowest: PredictionBook 4s, DraftAhead 2s, BreakageWarnings 1s) / OK [ran] [tree 071af625c50b] (2026-11-01T05:54:30Z)
- (ac 2) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 26 tests in 4.7s (6 classes, 16 at a time; slowest: PredictionBook 4s, DraftAhead 2s, BreakageWarnings 1s) / OK [ran] [tree 071af625c50b] (2026-11-01T05:54:30Z)
- (audit intent) `fm check exit 0 (5511 tests); 5 red→green tests (clean repo none, a date in 14 days filed via the trigger table and a far one not, co-change with and without its partner, state trend, scoring hit/acted/miss by window); fm task prove proved; thresholds measured on Foreman's own last 20 commits` → three forward-looking detectors on the tick, each filed through the trigger table (route, mute, demotion) and scored by its window; fm outcomes --predictions shows precision per kind [tree 071af625c50b] (2026-11-01T05:54:30Z)
- (audit adversary) `fm check exit 0 (5511 tests); 5 red→green tests (clean repo none, a date in 14 days filed via the trigger table and a far one not, co-change with and without its partner, state trend, scoring hit/acted/miss by window); fm task prove proved; thresholds measured on Foreman's own last 20 commits` → git runs with list args under c._git (GIT_* stripped, no prompt); files are read as text only, symlinks and files over 512 KB skipped, nothing executed; the capture text is c.plain'd [tree 071af625c50b] (2026-11-01T05:54:30Z)
- (audit edge) `fm check exit 0 (5511 tests); 5 red→green tests (clean repo none, a date in 14 days filed via the trigger table and a far one not, co-change with and without its partner, state trend, scoring hit/acted/miss by window); fm task prove proved; thresholds measured on Foreman's own last 20 commits` → first run records HEAD only (no flood of historic co-change); a date of today never counts; state already over budget is fmdoctor's (no duplicate); a rewritten HEAD gives an empty rev-list; once a local day [tree 071af625c50b] (2026-11-01T05:54:30Z)
## Log
- 2026-10-31T14:33:37Z created
- 2026-10-31T16:08:16Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2408.builder.md
- 2026-10-31T16:08:16Z builder slot freed
- 2026-10-31T16:11:41Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2408.builder.md
- 2026-10-31T16:11:42Z builder slot freed
- 2026-11-01T05:44:35Z focused
- 2026-11-01T05:44:36Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-01T05:46:34Z decision: co-change thresholds 5 pairings / 80% (3/60% flagged 30 of the last 20 Foreman commits, 5/80% flags 4, each a module without its test); dates strictly after today (3 of today's test fixtures read as deadlines)
- 2026-11-01T05:47:52Z scope: plugin/tests/test_foresight.py (the tests), plugin/lib/fmnight.py (the tick calls breakage_tick), MASTER.md and CHANGELOG.md (docs); fmgraph untouched: git log's name lists suffice, its db can take seconds to build on a tick
- 2026-11-01T05:55:03Z done
- 2026-11-01T05:55:05Z committed 92d693cf (5 files)
- 2026-11-01T05:55:10Z guard authorization added: publish
- 2026-11-01T06:03:25Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2356 [FEATURE M, done, 3 steps] Watchers start work with no session: CI, issues and file events on a zero-token tick (Mission 8, #11) — lesson: Text from an outside tr…
- playbook Verify game logic without a window (fm playbooks show verify/game-logic)
- research T-1810-review: Verdict:** changes needed. The sweep never runs in a default project (finding 1), and its GitHub path has several failure modes (findings 2–5). […
- decision 2026-10-15: Round 7 slate: 8 small reliability/delight builds (bare fm answers what now, close shows undo, demo ends in this repo, doctor state budget, night le…
- the similar finished task took 3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_foresight.py, plugin/tests/test_graph.py
## Preflight
Changed in scope since this was planned (2026-10-31): plugin/lib/fmforesight.py; re-ground the plan against them before editing
## Lessons
- Measure a detector on the real history before setting its threshold: 3 pairings at 60% looked strict and flagged 30 of 20 commits; 5 at 80% flags 4, all real
## Plan gaps
- failed first: step 2 red tests: each detector fires on a planted case and not on a clean twin; scoring by window
## Files touched
- plugin/tests/test_foresight.py
- plugin/lib/fmforesight.py
- plugin/lib/fmnight.py
- CHANGELOG.md
- MASTER.md
