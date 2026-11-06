---
id: T-2559
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmideas.py, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_ideas.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-11-02T07:02:02Z
updated: 2026-11-02T07:23:13Z
base: b2c413301494a531d470794d27f0eb1481edf0f5
base_tree: ed326a5c1338131a61a59536ec50ac10102ecb51
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T07:02:27Z
plan0_scope: [plugin/lib/fmideas.py, plugin/lib/fmcli.py, plugin/tests/test_ideas.py, CHANGELOG.md]
verified: strong
---
# fm ideas --seen-latest N passes the newest N earlier runs' ideas.md without typing paths
## Raw request
> fm ideas --seen-latest N: pass the newest N earlier runs' ideas.md without typing paths; twice in one session a hand-typed --seen path for a run that didn't exist failed the brainstorm (Missions 7 and 8)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm ideas --seen-latest 2 reads the two newest research/brainstorm-*/ideas.md (by folder name, the run being made excluded) as if each were a --seen, beside any explicit --seen; runs with no ideas.md are skipped — verify with `python3 plugin/tests/run.py test_ideas`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_ideas: three earlier runs (one without ideas.md); --seen-latest 2 seeds the run with the two newest that have ideas.md
2. [x] fmideas: --seen-latest N extends args.seen with the newest N ideas.md before the --seen loop; fmcli flag
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ideas.Ideas.test_seen_latest_reads_the_newest_earlier_runs_without_typed_paths` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Ideas 0s) / FAILED (1 classes: test_ideas.Ideas) [ran] [tree 5543aa34c60b] [world 2f1906870a] (2026-11-02T07:02:57Z)
- (step 2) `python3 plugin/tests/run.py test_ideas` → exit 0 · Ran 26 tests in 8.6s (5 classes, 16 at a time; slowest: Ideas 8s, BoardIdeas 1s, DegradeOnPace 0s) / OK [ran] [tree 2ea1470c7009] [world 2f1906870a] (2026-11-02T07:03:19Z)
- (ac 1) `python3 plugin/tests/run.py test_ideas` → exit 0 · Ran 26 tests in 8.5s (5 classes, 16 at a time; slowest: Ideas 8s, BoardIdeas 1s, DegradeOnPace 0s) / OK [ran] [tree c3b3ddfa079e] [world 2f1906870a] (2026-11-02T07:10:04Z)
- (step 1) `python3 plugin/tests/run.py test_ideas.Ideas.test_seen_latest_reads_the_newest_earlier_runs_without_typed_paths` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Ideas 0s) / OK [ran] [tree c3b3ddfa079e] [world 2f1906870a] (2026-11-02T07:10:04Z)
- (audit edge) `self-review: --seen-latest globs research/brainstorm-*/ideas.md newest first by folder name, excludes this run's folder, adds them to any explicit --seen; the Genesis step's line uses it` → a run with no ideas.md is skipped (only ideas.md files are globbed); N larger than the runs available takes what exists; 0 or negative adds nothing [tree c3b3ddfa079e] (2026-11-02T07:10:04Z)
- (audit self) `self-review: --seen-latest globs research/brainstorm-*/ideas.md newest first by folder name, excludes this run's folder, adds them to any explicit --seen; the Genesis step's line uses it` → no findings [tree c3b3ddfa079e] (2026-11-02T07:10:04Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree fc83d19ddf47] [world 2f1906870a] (2026-11-02T07:23:13Z)
## Log
- 2026-11-02T07:02:02Z created
- 2026-11-02T07:02:25Z planned from capture
- 2026-11-02T07:02:26Z focused
- 2026-11-02T07:02:27Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T07:03:54Z set scope=['plugin/lib/fmideas.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmgenesis.py', 'plugin/tests/test_ideas.py', 'CHANGELOG.md']
- 2026-11-02T07:03:54Z scope: fmideas --seen-latest (newest ideas.md, this run excluded) and its fmcli flag; fmgenesis.IDEAS uses --seen-latest 6 (widened: the step told sessions to type paths); test_ideas; CHANGELOG
- 2026-11-02T07:10:42Z done
- 2026-11-02T07:10:45Z committed 699a3aea (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2527 [FEATURE M, done, 2 steps] fm ci-watch --last-ship watches the main commit the newest fm ship pushed — lesson: a falsy test on an optional CLI value turns a faile…
- T-1658 [FEATURE M, done, 5 steps] Settings extras: log, macro, duel, replay (what-breaks), words-to-diff, undo that adapts — lesson: CLI write tests need a pty: in_claud…
- T-1063 [FEATURE M, done, 2 steps] Steers compile to checkers: a steer or interrupt is typed (scope, style, safety, wrong app — lesson: Never let the agent create a restr…
- decision 2026-10-31: [revisited: Mission 4 brainstorm ran without --deepen] Mission 4's deepen rounds rerun now that the risk budget reset (fm ideas --rounds 1 --deepen …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_ideas.py
## Lessons
- a command that asks for paths the session must type invites guessed paths; let it find its own inputs
## Plan gaps
- failed first: step 1 red test in test_ideas: three earlier runs (one without ideas.md); --seen-latest 2 seeds the run wi…
## Files touched
- plugin/tests/test_ideas.py
- plugin/lib/fmcli.py
- plugin/lib/fmideas.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
