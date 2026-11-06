---
id: T-2140
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T10:37:52Z
updated: 2026-10-30T11:18:16Z
base: a2bf4d88bb64cbdcae93fefe178fd9c6269401b5
base_tree: b71153f54940e943009d2693b59f6a3b768301dc
plan0_at: 2026-10-30T10:53:55Z
plan0_scope: []
verified: strong
---
# #4 exam: G-goal and G-resume kinds, child-authored contents keys, foreman vs plain, false done graded (Mission 4 brief 6)
## Raw request
> #4 exam: G-goal and G-resume kinds, child-authored contents keys, foreman vs plain, false done graded (Mission 4 brief 6)
## Interpretation
Two new fm exam kinds for gen-0 #4 (goal to finish). goal: the arm gets only a vague goal ('get these helpers to a finished state I could release'); the hidden key is the contents a finished version needs (a planted bug, an untested function, a README that disagrees with the code, plus a child-written missing piece). resume: the same, but PLAN.md on disk marks some items done and the arm gets only 'continue'. Graded: every key item met (fixed counts all items, so a done item that breaks is a regression), test-first for the open ones, and a false done when the reply says done while an item is unmet. Extra work is never a false alarm here.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam gen makes goal and resume scenarios with a hidden contents key a tool-less child writes; the oracle meets every key item, empty none and is never graded done — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
A. Chosen: two KINDS in fmexam reusing the defect machinery (render, _check_one, grade): goal = DEFECTS bug/vuln/untested/docs with the template goal request; resume = the same plus DONE items marked in PLAN.md and already applied in the repo. Child authoring through CHILD_KINDS/CHILD_DEFECTS as for bug/none. B. A separate contents-key format (free-form test bodies per item): a second grader for what the defect keys already express; not now. C. Multi-session resume (kill a real first session mid-run): costs a live arm per scenario; the static half-done repo tests the same reading of the plan. Captured as the relay-race spike.
## Risks and rollback
## Execution prompt
## Steps
1. [x] goal kind: child author prompt + key (tests and README patterns), render and grade, test-first with a stubbed child
2. [x] resume kind: half the key applied, a plan on disk, 'continue'; graded remaining met and none redone
3. [x] exam of the exam: every key test fails on base and passes on oracle in six languages; docs
## Resume here
<!-- auto -->
- 2026-10-30T11:02:28Z steps 3/3 done
- git: foreman/build; 4 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmexam.py, plugin/tests/test_exam.py
- touched since last checkpoint: /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2140-impl.edit, plugin/tests/test_exam.py, plugin/lib/fmexam.py, CHANGELOG.md, MASTER.md
## Docs impact
MASTER fmexam entry, CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam.ExamAuthors.test_finish_kinds_goal_and_resume` → exit 0 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: ExamAuthors 1s) / OK [ran] [tree dacf443f655b] (2026-10-30T11:01:38Z)
- (step 2) `python3 plugin/tests/run.py test_exam.ExamAuthors` → exit 0 · Ran 8 tests in 4.4s (1 classes, 16 at a time; slowest: ExamAuthors 4s) / OK [ran] [tree dacf443f655b] (2026-10-30T11:01:43Z)
- (step 3) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 24 tests in 20.2s (10 classes, 16 at a time; slowest: ExamGen 20s, ExamRust 12s, ExamC 11s) / OK [ran] [tree dacf443f655b] (2026-10-30T11:02:04Z)
- (step 3) `fm exam check s8-008` → exit 0 · s8-008: 36 scenarios checked, all sound [ran] [tree 35c8297912cb] (2026-10-30T11:07:07Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 24 tests in 20.3s (10 classes, 16 at a time; slowest: ExamGen 20s, ExamRust 12s, ExamC 11s) / OK [ran] [tree 35c8297912cb] (2026-10-30T11:07:44Z)
- (audit intent) `one fm-reviewer pass over five lenses (approve with nits); findings verified and fixed test-first; goal+resume fm exam check in all 6 languages` → child request optional for goal kinds (fixed, norequest stub test); child writes one key item, said in CHANGELOG, T-2149 captured [tree 35c8297912cb] (2026-10-30T11:07:44Z)
- (audit adversary) `one fm-reviewer pass over five lenses (approve with nits); findings verified and fixed test-first; goal+resume fm exam check in all 6 languages` → none; PLAN.md is plain text, static checks match by file name, key.json stays outside the repo [tree 35c8297912cb] (2026-10-30T11:07:44Z)
- (audit edge) `one fm-reviewer pass over five lenses (approve with nits); findings verified and fixed test-first; goal+resume fm exam check in all 6 languages` → missing work dir leaves broken 0 and done-claim is still false done; old keys grade unchanged [tree 35c8297912cb] (2026-10-30T11:07:44Z)
- (audit operator) `one fm-reviewer pass over five lenses (approve with nits); findings verified and fixed test-first; goal+resume fm exam check in all 6 languages` → default gen +18 scenarios accepted [tree 35c8297912cb] (2026-10-30T11:07:44Z)
- (audit maintainer) `one fm-reviewer pass over five lenses (approve with nits); findings verified and fixed test-first; goal+resume fm exam check in all 6 languages` → s7-007, s8-008, s9-009 all sound across python, js, ts, ruby, rust, c [tree 35c8297912cb] (2026-10-30T11:07:44Z)
## Log
- 2026-10-30T10:37:52Z created
- 2026-10-30T10:53:54Z focused
- 2026-10-30T11:01:14Z red first: test_finish_kinds_goal_and_resume failed (KINDS lacked goal/resume) before the fmexam change, then passed
- 2026-10-30T11:07:07Z review: approve with nits; fixed: child request optional for goal kinds (test: norequest stub), resume KIND_WORDS no longer matches 'continuous'; checked goal+resume in all 6 languages: s7-007, s8-008, s9-009 all sound; child-share wording in CHANGELOG; cost +18 scenarios per default gen accepted
- 2026-10-30T11:08:07Z done
- 2026-10-30T11:08:08Z committed e626873d (6 files)
- 2026-10-30T11:16:02Z guard authorization added: publish
- 2026-10-30T11:18:16Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- T-2126 [FEATURE M, done, 2 steps] #1 held-out exam: I-none, I-clean, I-rank child-authored kinds; finders, foreman and plain arms (Mission 3 brief 7) — lesson: a module-…
- T-2079 [FEATURE L, done, 6 steps] fm exam: generated multi-language exam with hidden keys, holdout third, finders and claude arms, scores to exam.jsonl — lesson: A claud…
- decision 2026-10-30: [cites: user steer 2026-10-30] Standing rule (user steer): weakness-finding uses signals Foreman didn't author — outcome survival (fm outcomes: reve…
## Lessons
- a regex on common words (continu) for kind mapping catches unrelated capabilities; anchor it on phrases
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/fmexam.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmgenesis.py
- plugin/tests/test_genesis.py
