---
id: T-2556
type: RESEARCH
tier: M
status: done
priority: normal
scope: [state/projects/foreman-4a056f/research]
depends_on: []
source: genesis
created: 2026-11-02T06:47:31Z
updated: 2026-11-02T06:50:52Z
base_note: Calibration: this plan states Choice 80% where RESEARCH M closes (20) held on the first finish 100% of the time: 20 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
base: ec276a784bbe072a1f87e1950c7516217ef17311
base_tree: 9581b1432c1048d7d0630f9581ec1eafcad6bfd4
plan0_at: 2026-11-02T06:48:43Z
plan0_scope: [state/projects/foreman-4a056f/research]
verified: strong
---
# Diagnose the long tier's false dones: class every failed hidden check on l001 and l002 against what the goal stated
## Raw request
> RESEARCH: why long goals false-done: read fm exam long's l001 and l002 runs at zero tokens and class every failed hidden check (never planned, planned but not built, built but broken, out of the goal's reach) against each session's own plan and done-when; file it as research long-false-done
## Interpretation
Reading 1: find out why the foreman arm said done on 12 long goals whose hidden checks failed, by rerunning each failed check on the session's tree and classing its failure. Reading 2: rerun the long tier now to see if it's still 6 of 6. Chosen: 1; 2 is ruled out by the user's steer (session arms wait for the end-of-run exam) and would not say why.
## Assumptions (confidence)
## Acceptance criteria
- [x] research long-false-done classes every failed hidden check of the foreman arm on l001 and l002 (never planned, planned but not built, built but broken, out of the goal's reach: the check demands an interface or name the goal text never states), each with its evidence (the failure line from rerunning the check on the session's tree) — verify with `test -s state/projects/foreman-4a056f/research/long-false-done.md`
## Non-goals
## Approach (options → choice → why)
1) Rerun each hidden check on the kept work trees at zero tokens, overlaying the hidden test files as the grader does, and class each failure by its first error line and the goal text. Likely outcome: one or two classes dominate; fails if: the trees were cleaned. 2) use what exists: fmlong.grade's overlay (key src, target, test_files) gives the exact tree the grader checked; the rerun copies that recipe in a shell loop. Likely outcome: the same failures the grade counted. 3) Read the session transcripts for intent. Fails if: they were removed (T-2262 removes them). 4) do less: report the grade's per-goal counts only. Fails if: T-2557 then builds blind. Choice 1 (80%): the failure lines are the cheapest evidence that tells the classes apart.
## Risks and rollback
Rerunning checks executes the session-written code in its kept tree: these are Foreman's own exam trees under state, already run once by the grader; run with credentials stripped as the grader does. Rollback: a research file only.
## Execution prompt
## Steps
1. [x] for each goal of l001 and l002 (foreman arm): rerun its hidden checks on the session's work tree, keep each failure's first error line (ImportError/AttributeError/AssertionError), and the goal text
2. [x] class each failure, count the classes, and file research long-false-done; if the largest class is out of the goal's reach, name it for the final report (the keys are never rewritten by Foreman) and point T-2557 at the next class
## Resume here
## Docs impact
research long-false-done
## Verification evidence
- (step 1) `python3 -I /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/longdiag.py ~/.claude/foreman/state/projects/foreman-4a056f/exam/long foreman | grep -c FAIL` → exit 0 · 31 [ran] [tree 9581b1432c10] [world 2f1906870a] (2026-11-02T06:50:29Z)
- (step 2) `test -s state/projects/foreman-4a056f/research/long-false-done.md && grep -c '^- ' state/projects/foreman-4a056f/research/long-false-done.md` → exit 0 · 9 [ran] [tree 9581b1432c10] [world 2f1906870a] (2026-11-02T06:50:29Z)
- (ac 1) `test -s state/projects/foreman-4a056f/research/long-false-done.md` → exit 0 · (no output) [ran] [tree 9581b1432c10] [world 2f1906870a] (2026-11-02T06:50:38Z)
- (audit intent) `self-review: every failed check was rerun on the session's kept tree with the hidden files laid over a copy, the grader's recipe; classes assigned from the first error line and the goal text; raw output kept in the research file` → why the long tier reads 6 of 6 false dones is now known: 17 of 31 failures are the exam's reach (unstated interfaces), 14 are real misses; T-2557 targets the real misses and the keys go to the user [tree 9581b1432c10] (2026-11-02T06:50:38Z)
- (audit edge) `self-review: every failed check was rerun on the session's kept tree with the hidden files laid over a copy, the grader's recipe; classes assigned from the first error line and the goal text; raw output kept in the research file` → one goal's checks failed on an installed binding's API (environment, classed as reach); the misattributed T-2181 lines under T-2225 are counted where they printed [tree 9581b1432c10] (2026-11-02T06:50:38Z)
- (audit intent) `self-review: every failed check was rerun on the session's kept tree with the hidden files laid over a copy, the grader's recipe; classes assigned from the first error line and the goal text; raw output kept in the research file` → why the long tier reads 6 of 6 false dones is now known: 17 of 31 failures are the exam's reach (unstated interfaces), 14 are real misses; T-2557 targets the real misses and the keys go to the user [tree 9581b1432c10] (2026-11-02T06:50:49Z)
- (audit edge) `self-review: every failed check was rerun on the session's kept tree with the hidden files laid over a copy, the grader's recipe; classes assigned from the first error line and the goal text; raw output kept in the research file` → one goal's checks failed on an installed binding's API (environment, classed as reach); the misattributed T-2181 lines under T-2225 are counted where they printed [tree 9581b1432c10] (2026-11-02T06:50:49Z)
## Log
- 2026-11-02T06:47:31Z created
- 2026-11-02T06:48:12Z planned from capture
- 2026-11-02T06:48:22Z set approved=True
- 2026-11-02T06:48:41Z focused
- 2026-11-02T06:50:52Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-31: Long tier l001's foreman 0/6 is an exam defect, not a score: hidden checks need private names the goal never states (fmwatch._shown, fmlong.KILL_T) …
- T-2325 [FEATURE M, done, 2 steps] fm exam long keeps each session goal's activity summary, so a slow or false-done goal says where its time went — lesson: Measure where …
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
- T-2320 [FEATURE S, done, 1 steps] fm exam long grade gives partial credit: hidden checks passed per goal and in total — lesson: An all-or-nothing score on a hard tier re…
## Decision
Recommendation: build T-2557 (a goal session's done claim checks each stated Done-when line and requirement against the tree, or names it missing), the largest class Foreman owns (14 of 31); report the exam's reach class (17 of 31: unstated interfaces) to the user and leave the keys to the tool-less child author. Would change if: the end-of-run long tier shows false dones from stated requirements falling to zero while the totals barely move, which would make re-keying the bigger lever.
## Lessons
- a done-rate number mixes what the agent missed with what the exam never stated; rerun the failing checks and read the first error line before acting on the number
