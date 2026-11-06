---
id: T-2158
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T14:08:41Z
updated: 2026-10-30T18:27:07Z
base: 9f7875f39d6bb674faeef6f0ce48a834209533ba
base_tree: 74b5a50a447809e94dd28195921073cb3d516484
plan0_at: 2026-10-30T18:14:38Z
plan0_scope: []
verified: strong
---
# Haiku scores are smoke signals only: fm exam scorecard, fm genesis select and the done…
## Raw request
> Haiku scores are smoke signals only: fm exam scorecard, fm genesis select and the done gate ignore graded results from a non-production model (a Haiku smoke run of foreman vs plain on <=9 held-out scenarios), and say so in their output (steer 2026-10-30 rule 1)
## Interpretation
Steer 1: 'Haiku never decides'; the full foreman-vs-plain exam runs at the end on the production model. Exam lines don't record the model, so a Haiku smoke line (s31-006) reads like a production one. fm exam run stamps the session model in the answers dir (like request), grade copies it to the line as model; a line whose model names haiku is smoke. fm exam scorecard (the §8 / DONE-WHEN pass) skips smoke lines and says how many it skipped. fm genesis select may still read them (steer 1 rule 4: selection is provisional and rests on the Haiku smoke run), but its provisional line names the model. The s31-006 answers get their stamp and are regraded (zero tokens) so the old lines are marked.
## Assumptions (confidence)
## Acceptance criteria
- [x] an exam line records its session model; fm exam scorecard skips a Haiku line and says so; select's provisional line names the model — verify with `python3 plugin/tests/run.py test_exam test_genesis`
- [x] the s31-006 Haiku lines are stamped and regraded, and the live scorecard says it skipped them — verify with `sh -c 'fm exam scorecard | grep -F "4 Haiku smoke lines not counted"'`
## Non-goals
## Approach (options → choice → why)
Options: (a) stamp the model at run time, copy to the line, a smoke() test (model names haiku), scorecard skips and counts smoke, select names it (chosen: the line says what produced it, each reader decides); (b) a --smoke flag on fm exam run (rejected: a label the runner can forget; the model is the fact); (c) a separate smoke.jsonl (rejected: two files every reader must join). Free-arm gaps (free_beats) keep reading smoke lines: a gap is a building signal, not a decision (steer 3 found its gap on a smoke run).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: model on the line, scorecard skips smoke, select names the model
2. [x] implement stamp/copy/smoke/scorecard/select; stamp and regrade s31-006; docs
## Resume here
## Docs impact
~/.claude/foreman/MASTER.md ~/.claude/foreman/CHANGELOG.md ~/.claude/foreman/site/genesis/genesis.js
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam test_genesis` → ✗ exit 1 · Ran 117 tests in 21.9s (23 classes, 16 at a time; slowest: ExamGen 22s, ExamAuthors 14s, GenesisCheck 13s) / FAILED (3 classes) [ran] [tree 3d1ece1eb181] (2026-10-30T18:15:06Z)
- (step 1) `python3 plugin/tests/run.py test_exam.ExamAuthors` → ✗ exit 1 · Ran 9 tests in 6.6s (1 classes, 16 at a time; slowest: ExamAuthors 6s) / FAILED (1 classes) [ran] [tree 370f510bfb9a] (2026-10-30T18:16:33Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisScorecard` → ✗ exit 1 · run.py: no test matches test_genesis.GenesisScorecard [ran] [tree 91384b853368] (2026-10-30T18:17:44Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisDraft` → ✗ exit 1 · Ran 12 tests in 2.5s (1 classes, 16 at a time; slowest: GenesisDraft 2s) / FAILED (1 classes) [ran] [tree 91384b853368] (2026-10-30T18:17:56Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 117 tests in 21.2s (23 classes, 16 at a time; slowest: ExamGen 21s, ExamAuthors 15s, GenesisCheck 13s) / OK [ran] [tree 460856856fbd] (2026-10-30T18:19:08Z)
- (step 2) `python3 plugin/tests/run.py test_genesis.GenesisDraft` → ✗ exit 1 · Ran 12 tests in 2.5s (1 classes, 16 at a time; slowest: GenesisDraft 2s) / FAILED (1 classes) [ran] [tree 03a13d0e7e82] (2026-10-30T18:19:54Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 117 tests in 21.5s (23 classes, 16 at a time; slowest: ExamGen 21s, ExamAuthors 15s, GenesisCheck 13s) / OK [ran] [tree 34b6ee281fdd] (2026-10-30T18:20:19Z)
- (step 2) `python3 plugin/tests/run.py test_exam.ExamAuthors test_genesis.GenesisDraft` → ✗ exit 1 · Ran 21 tests in 6.7s (2 classes, 16 at a time; slowest: ExamAuthors 6s, GenesisDraft 2s) / FAILED (2 classes) [ran] [tree 12ab61db765f] (2026-10-30T18:21:57Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 117 tests in 21.3s (23 classes, 16 at a time; slowest: ExamGen 21s, ExamAuthors 15s, GenesisCheck 13s) / OK [ran] [tree 7389e506de4e] (2026-10-30T18:22:23Z)
- (ac 1) `python3 plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 117 tests in 21.5s (23 classes, 16 at a time; slowest: ExamGen 21s, ExamAuthors 15s, GenesisCheck 13s) / OK [ran] [tree 2d46c0b79c14] (2026-10-30T18:23:50Z)
- (ac 2) `sh -c 'fm exam scorecard | grep -F "4 Haiku smoke lines not counted"'` → exit 0 · scorecard (foreman, held out, bar 80%): 0/13 pass · 4 Haiku smoke lines not counted (Haiku never decides) [ran] [tree 2d46c0b79c14] (2026-10-30T18:23:50Z)
- (step 1) `python3 plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 117 tests in 21.5s (23 classes, 16 at a time; slowest: ExamGen 21s, ExamAuthors 15s, GenesisCheck 13s) / OK [ran] [tree 2d46c0b79c14] (2026-10-30T18:23:50Z)
- (audit intent) `one foreman:fm-reviewer pass over five lenses (research T-2158-review); 2 MEDIUM + 4 LOW, all fixed test-first` → scorecard skips Haiku and counts it; top gaps from a Haiku line say so; select still reads them by steer 1 rule 4, recorded with fm decide [tree 2d46c0b79c14] (2026-10-30T18:23:50Z)
- (audit edge) `one foreman:fm-reviewer pass over five lenses (research T-2158-review); 2 MEDIUM + 4 LOW, all fixed test-first` → grade --model fills an unstamped or default stamp, refuses a named one and a non-session agent; an older unstamped line takes its run's later stamp [tree 2d46c0b79c14] (2026-10-30T18:23:50Z)
- (audit adversary) `one foreman:fm-reviewer pass over five lenses (research T-2158-review); 2 MEDIUM + 4 LOW, all fixed test-first` → model strings are c.plain'd and cut to 60/40 chars before answers files, lineage.md, the tail and the site; the site escapes nothing new (a fixed label) [tree 2d46c0b79c14] (2026-10-30T18:23:50Z)
## Log
- 2026-10-30T14:08:41Z created
- 2026-10-30T16:05:37Z needs first: exam lines don't record the session model (fmexam writes none), so record it on each run/grade line before select/scorecard can ignore Haiku-graded ones (from T-2183)
- 2026-10-30T18:05:07Z planned: it has criteria and steps
- 2026-10-30T18:14:37Z focused
- 2026-10-30T18:18:46Z criterion 2 verify: `fm exam scorecard` → `sh -c 'fm exam scorecard | grep -F "4 Haiku smoke lines not counted"'`
- 2026-10-30T18:24:26Z done
- 2026-10-30T18:24:28Z committed 64a92875 (7 files)
- 2026-10-30T18:24:41Z guard authorization added: publish
- 2026-10-30T18:27:07Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
- T-2184 [FEATURE M, done, 5 steps] Foreman sessions use fm find by default (steer 2026-10-30 #3): the exam shows a Foreman… — lesson: a capability the session never hears…
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- decision 2026-10-30: [revisited: testing cadence] [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] [check: pending T-2158] Testing ca…
## Why not caught
exam lines never recorded the model, so nothing could tell a Haiku smoke line from a production one; the steer named the rule before any line said which model answered
## Lessons
- A line that records what produced it lets each reader decide; a label the runner must remember (a --smoke flag) is forgotten. Backfill old lines at read time from a later stamp of the same run instead of rewriting history.
## Plan gaps
- failed first: step 1 red tests: model on the line, scorecard skips smoke, select names the model
## Files touched
- plugin/tests/test_exam.py
- plugin/tests/test_genesis.py
- plugin/lib/fmexam.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
- site/genesis/genesis.js
