---
id: T-2203
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T19:43:58Z
updated: 2026-10-30T20:17:03Z
base: f854209e67c7db8ade84b2b026ea375d9dd4e2db
base_tree: 31af1e803e79d6bbeb6a4f7b34242cc454aa144c
plan0_at: 2026-10-30T19:57:57Z
plan0_scope: []
verified: strong
---
# fm exam grade's test-first check puts back the whole planted file, so an arm that also…
## Raw request
> fm exam grade's test-first check puts back the whole planted file, so an arm that also edited other code in that file goes red for that and is credited test-first (which counts toward closing): put back only the defect's lines (the planted-vs-clean diff applied to the arm's file), and count no tf-first when that diff no longer applies
## Interpretation
fm exam grade credits a fix as test-first when the arm's suite is green on its fix and red with hidden/planted/<kind>'s whole files copied over the arm's work. An arm that also edited other code in those files (a helper its tests use) goes red for that loss, not the defect, and is credited; tf-first counts toward closing a scenario, so this inflates closed counts.
## Assumptions (confidence)
## Acceptance criteria
- [x] an arm that fixes the defect and also edits other code in that file gets tf-first only when its tests catch the defect's own lines put back; a region that no longer applies credits nothing — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
Complete version: put back only the defect: per file, the clean→planted line diff (hidden/clean vs hidden/planted/<kind>), each changed region with one line of context, applied to the arm's file only where that clean text occurs exactly once; any region that doesn't apply gives no tf-first credit (said in the grade). Options: whole-file overlay (today, over-credits), AST-level function swap (per-language parsers, heavier), git apply of a unified diff (needs git and fuzz rules; exact-once text replace is stricter and stdlib), exact-once region replace (chosen). Build vs reuse: difflib, the existing suite(key, target, overlay).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: test_exam case where the whole-file overlay over-credits
2. [x] fmexam: put back only the defect's regions; MASTER + CHANGELOG
## Resume here
## Docs impact
~/.claude/foreman/MASTER.md ~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam.ExamGen.test_test_first_puts_back_only_the_defects_lines` → ✗ exit 1 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: ExamGen 0s) / FAILED (1 classes) [ran] [tree 7bcd488d3c50] (2026-10-30T19:58:34Z)
- (step 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 28 tests in 22.6s (10 classes, 16 at a time; slowest: ExamGen 22s, ExamAuthors 13s, ExamRust 12s) / OK [ran] [tree ef9d6f3e3549] (2026-10-30T19:59:09Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_docs test_exam && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [12.68s] [ran] [tree 84fe19f866e7] (2026-10-30T19:59:54Z)
- (ac 1) `python3 plugin/tests/run.py test_exam 2>&1 | tail -6` → exit 0 · Ran 28 tests in 23.3s (10 classes, 16 at a time; slowest: ExamGen 23s, ExamAuthors 15s, ExamRust 12s) / OK [ran] [tree 808c39b7e361] (2026-10-30T20:02:18Z)
- (step 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 28 tests in 22.1s (10 classes, 16 at a time; slowest: ExamGen 22s, ExamAuthors 13s, ExamRust 12s) / OK [ran] [tree 3572af12aa03] (2026-10-30T20:02:47Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_docs test_exam && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.28s] [ran] [tree 3572af12aa03] (2026-10-30T20:03:22Z)
- (step 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 30 tests in 22.2s (10 classes, 16 at a time; slowest: ExamGen 22s, ExamAuthors 13s, ExamRust 12s) / OK [ran] [tree 550ace296ed0] (2026-10-30T20:14:30Z)
- `python3 plugin/tests/run.py test_exam` → ✗ exit 1 · Ran 30 tests in 23.0s (10 classes, 16 at a time; slowest: ExamGen 22s, ExamAuthors 13s, ExamRust 12s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 550ace296ed0] (2026-10-30T20:15:19Z)
- `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 30 tests in 22.2s (10 classes, 16 at a time; slowest: ExamGen 22s, ExamAuthors 13s, ExamRust 12s) / OK [ran] [tree 550ace296ed0] (2026-10-30T20:15:19Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 30 tests in 22.3s (10 classes, 16 at a time; slowest: ExamGen 22s, ExamAuthors 13s, ExamRust 12s) / OK [ran] [tree 550ace296ed0] (2026-10-30T20:16:24Z)
- (audit intent) `one foreman:fm-reviewer pass (intent, adversary, edge) on the lane diff: 2 MEDIUM + 1 LOW fixed test-first, a timeout-as-red LOW kept by design; research/T-2203-review.md` → only a red that isn't a load error credits tf-first; the oracle keeps full credit (tf_first == tf_keyed) [tree 550ace296ed0] (2026-10-30T20:16:24Z)
- (audit adversary) `one foreman:fm-reviewer pass (intent, adversary, edge) on the lane diff: 2 MEDIUM + 1 LOW fixed test-first, a timeout-as-red LOW kept by design; research/T-2203-review.md` → putback runs nothing and never writes through a link [tree 550ace296ed0] (2026-10-30T20:16:24Z)
- (audit edge) `one foreman:fm-reviewer pass (intent, adversary, edge) on the lane diff: 2 MEDIUM + 1 LOW fixed test-first, a timeout-as-red LOW kept by design; research/T-2203-review.md` → read-only file, end-of-file region, repeated anchor line, missing work dir all tested [tree 550ace296ed0] (2026-10-30T20:16:24Z)
## Log
- 2026-10-30T19:43:58Z created
- 2026-10-30T19:57:36Z planned: it has criteria and steps
- 2026-10-30T19:57:47Z set approved=True
- 2026-10-30T19:57:47Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2203.builder.md
- 2026-10-30T19:57:57Z focused
- 2026-10-30T20:13:49Z merged worktree-agent-a5faadedc25f340c9 (3 file(s))
- 2026-10-30T20:13:49Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a5faadedc25f340c9
- 2026-10-30T20:13:54Z focused
- 2026-10-30T20:17:01Z done
- 2026-10-30T20:17:03Z committed fc3ed759 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- research T-2120-review: Verdict:** changes needed. One MEDIUM finding: the exam-defect proof can be satisfied without any exam defect. [stale: plugin/lib/fmexam.py, plug…
- research draft-mission-exam-gen1: Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).
- decision 2026-10-30: T-2112: #13's draft kinds live in fmgenesis (fm genesis exam) reusing fmexam.draw/render and cover; G-tower is a 'genesis' session arm on fmexam's d…
- the similar finished task took 4 steps
## Why not caught
the oracle exam checked tf_first == tf_keyed only for arms whose work equals the clean tree, so a whole-file overlay looked right; no case had an arm with other edits in the defect's file
## Lessons
- A grade that puts code back must anchor on context, not byte-identical text, and must credit only a red the defect caused: a load error from a wiped name is the grader's damage, not the arm's catch
## Plan gaps
- failed first: step 1 red: test_exam case where the whole-file overlay over-credits
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/fmexam.py
- MASTER.md
- CHANGELOG.md
- README.md
- plugin/lib/fmgenesis.py
- plugin/lib/fmmcp.py
- plugin/tests/test_genesis.py
- plugin/tests/test_mcp.py
