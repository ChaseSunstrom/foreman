---
id: T-2608
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-11-02T12:45:26Z
updated: 2026-11-02T13:15:43Z
base: 76455d87379aeb483de882a5945c7628ec251f2b
base_tree: 2179cc30bb3ce0a29cc49781e6659a9db22c3f1e
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-02T12:56:02Z
plan0_scope: []
verified: strong
---
# The watch exam kind's blind variant: a stream whose setup has no watch yes for issues expects no work from its issue events and 'issues' named blind
## Raw request
> FEATURE: the watch exam kind gains blind variants (gen-3 Mission 1, T-2607's exam): a stream whose setup has no watch yes for issues, a sensitive repo, or no network; the hidden key expects no work started from the unseen source and started.json naming it blind with the reason; _stream, the key and _watch_score read it
## Interpretation
Reading 1 (chosen): grade, in the replayed stream, the one blind reason a replay can show: the setup has no watch yes for issues. 'Sensitive' and 'no network' are runtime conditions of the tick, covered by T-2607's unit tests; the Mission's 'a variant per reason' narrows to this one. Reading 2: a separate exam kind for blindness. Rejected: the watch kind already replays the stream and grades what starts.
## Assumptions (confidence)
## Acceptance criteria
- [x] about a third of watch scenarios (by their seed) have setup watch [] for issues; their hidden key drops the issue events' starts and sets blind ['issues']; the scenario's instructions ask for a blind list in started.json — verify with `python3 plugin/tests/run.py test_exam`
- [x] _watch_score and the grade count a blind variant closed only when the issue events started nothing and started.json names issues blind; a normal scenario ignores blind — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
1) Variant inside _stream: by the scenario's hash a third set setup watch [] and the key's starts drop the issue events, with blind ['issues']; _watch_score returns whether blind was named; the grade needs both. Likely outcome: the exam sees whether a session notices an unwatched source. Fails if: a child-authored stream lacks the setup line (the variant applies only to the template's stream). 2) use what exists: grade blindness only by the absence of issue starts. Fails if: an arm that started nothing at all passes without noticing anything. 3) do less: leave the exam alone and rely on T-2607's unit tests. Fails if: the Mission's exam line stays empty. Choice 1 (80%): one branch in the template, one field in the key and the score.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests in test_exam (the key of a blind variant; the grade of a right and a wrong answer)
2. [x] variant in _stream and the key; instructions
3. [x] blind in _watch_score and the grade
4. [x] CHANGELOG
## Resume here
<!-- auto -->
- 2026-11-02T13:06:37Z steps 4/4 done
- git: foreman/build; 3 uncommitted: CHANGELOG.md, plugin/lib/fmexam.py, plugin/tests/test_exam.py
- touched since last checkpoint: plugin/tests/test_exam.py, plugin/lib/fmexam.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/critique3-1.md
## Docs impact
CHANGELOG (Unreleased); the kind's description is unchanged in shape (the events that should start work didn't, or work started from ones that shouldn't).
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam.ExamGen` → exit 0 · Ran 21 tests in 52.5s (1 classes, 16 at a time; slowest: ExamGen 52s) / OK [ran] [tree cad5b02620e7] [world 2f1906870a] (2026-11-02T12:58:06Z)
- (step 1) `python3 plugin/tests/run.py test_exam.WatchKind` → ✗ exit 1 · Ran 4 tests in 3.4s (1 classes, 16 at a time; slowest: WatchKind 3s) / FAILED (1 classes: test_exam.WatchKind) [ran] [tree 89d9a4ffb24f] [world 2f1906870a] (2026-11-02T12:58:22Z)
- (step 2) `python3 plugin/tests/run.py test_exam.WatchKind` → exit 0 · Ran 4 tests in 3.5s (1 classes, 16 at a time; slowest: WatchKind 3s) / OK [ran] [tree 75621cc6f3f1] [world 2f1906870a] (2026-11-02T12:59:00Z)
- (step 3) `python3 plugin/tests/run.py test_exam.WatchKind` → exit 0 · Ran 4 tests in 3.5s (1 classes, 16 at a time; slowest: WatchKind 3s) / OK [ran] [tree 75621cc6f3f1] [world 2f1906870a] (2026-11-02T12:59:04Z)
- (step 4) `head -4 CHANGELOG.md` → exit 0 · # Changelog / ## Unreleased [ran] [tree fbf742c28bdb] [world 2f1906870a] (2026-11-02T12:59:04Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 97 tests in 83.8s (23 classes, 16 at a time; slowest: LeanKind 84s, ExamAuthors 77s, JudgmentKinds 71s) / OK [ran] [tree fbf742c28bdb] [world 2f1906870a] (2026-11-02T13:06:02Z)
- (ac 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 97 tests in 83.8s (23 classes, 16 at a time; slowest: LeanKind 84s, ExamAuthors 77s, JudgmentKinds 71s) / OK [ran] [tree fbf742c28bdb] [world 2f1906870a] (2026-11-02T13:06:02Z)
- (audit intent) `self-review: _stream makes a third of scenarios (by hash) blind to issues: setup watch [], no starts from issue events, key blind ['issues']; the triggers runner copies the real tick's tick-blind.json kinds into started.json; the grade needs _watch_blind; normal scenarios have no blind key, so their grade is unchanged; the clean render carries the key's blind` → about a third of 30 streams are blind variants with no issue starts and blind ['issues']; the grade passes when issues is named and fails when not (test); the real-tick replay test passes [tree fbf742c28bdb] (2026-11-02T13:06:02Z)
- (audit edge) `self-review: _stream makes a third of scenarios (by hash) blind to issues: setup watch [], no starts from issue events, key blind ['issues']; the triggers runner copies the real tick's tick-blind.json kinds into started.json; the grade needs _watch_blind; normal scenarios have no blind key, so their grade is unchanged; the clean render carries the key's blind` → CI is also blind in every replay (no --watch-ci staged), and the check is a superset, so naming CI too is fine; a child-authored stream keeps the template's setup, so the variant applies to it as well [tree fbf742c28bdb] (2026-11-02T13:06:02Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-2/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree fbf742c28bdb] [world 2f1906870a] (2026-11-02T13:09:33Z)
## Log
- 2026-11-02T12:45:26Z created
- 2026-11-02T12:49:31Z planned from capture
- 2026-11-02T12:56:02Z set approved=True
- 2026-11-02T12:56:02Z focused
- 2026-11-02T12:56:02Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-02T13:07:53Z done
- 2026-11-02T13:07:56Z committed c5fbfafc (3 files)
- 2026-11-02T13:09:34Z guard authorization added: publish
- 2026-11-02T13:15:43Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2607 [FEATURE M, done, 4 steps] The tick names what it could not watch: each trigger kind it skipped (CI, issues) with the reason, in fm doctor and the session's Watch…
- T-2360 [FEATURE M, done, 3 steps] #11 exam kind watch: a zero-token trigger arm on replayed event streams with a hidden key (Mission 8, #11) — lesson: An exam kind for u…
- T-2524 [FEATURE M, done, 2 steps] Beyond exam kind: an offline-package deliverable, built and run with no network — lesson: an exam kind tied to one ecosystem must be fi…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
## Lessons
- An exam variant is cheapest where the harness already runs the real code: the replay ran the real tick, so the variant only had to change the setup and read what the tick said
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/fmexam.py
- CHANGELOG.md
