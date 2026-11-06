---
id: T-2292
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T07:16:58Z
updated: 2026-10-31T07:51:32Z
base: b122798c313874519552906dbf8fc6c122898f70
base_tree: d35a6a2633393fc14c85f70c3e9e04883901f74a
plan0_at: 2026-10-31T07:17:18Z
plan0_scope: []
paused_tree: e1ef079446e836a47446452f7518e5688a4a064b
verified: strong
---
# Parallel exam sessions: fm exam run and fm exam long run take --jobs N for the session arms (foreman, plain, genesis), so the end-of-run production exam finishes in hours, not days
## Raw request
> Parallel exam sessions: fm exam run and fm exam long run take --jobs N for the session arms (foreman, plain, genesis), so the end-of-run production exam finishes in hours, not days
## Interpretation
The end-of-run exam (steer 1) needs each capability graded in all six languages on the production model, about 90 held-out sessions per session arm plus the long tier; fmexam.run_agent and fmlong.run run sessions one at a time, so the exam would take most of a day of wall time.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam run RUN --agent foreman --jobs 4 runs up to 4 scenario sessions at once (each in its own temp copy and state dir, as today), grades the same as --jobs 1, keeps the spend check before each session and a combined budget, and writes answers without races; fm exam long run takes --jobs too; --jobs defaults to 1 — verify with `python3 plugin/tests/run.py test_exam test_long`
## Non-goals
## Approach (options → choice → why)
1) a bounded thread pool (--jobs N, default 1) over scenarios in run_agent and fmlong.run: each session already gets its own temp repo copy and state dir; answers are per-scenario dirs; the budget check runs before each session under a lock, and the model stamp is written once; 2) separate processes per scenario via fm run — rejected: more moving parts for the same isolation; 3) run fewer scenarios — rejected: the scorecard needs every language. Choice 1.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests with the stub claude: 4 jobs run concurrently (timestamps overlap), same grade as 1 job, budget checked per session
2. [x] a thread pool over scenarios in fmexam.run_agent and fmlong.run; per-scenario answer dirs keep writes apart
3. [x] docs lines in the report
## Resume here
<!-- auto -->
- 2026-10-31T07:49:31Z steps 3/3 done
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: .claude/worktrees/agent-abee9bcb7b8324607/plugin/tests/test_long.py, .claude/worktrees/agent-abee9bcb7b8324607/.fm-scratch/e1.json, .claude/worktrees/agent-abee9bcb7b8324607/plugin/tests/test_exam.py, .claude/worktrees/agent-abee9bcb7b8324607/plugin/lib/fmbudget.py, .claude/worktrees/agent-abee9bcb7b8324607/plugin/lib/fmexam.py, .claude/worktrees/agent-abee9bcb7b8324607/plugin/lib/fmcli.py, .claude/worktrees/agent-abee9bcb7b8324607/plugin/lib/fmlong.py
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_exam test_long 2>&1 | tail -15` → exit 0 · Ran 74 tests in 89.8s (18 classes, 16 at a time; slowest: ExamAuthors 89s, ExamGen 71s, Long 67s) / OK [ran] [tree 7cd3f47ca64b] (2026-10-31T07:21:57Z)
- (step 1) `python3 plugin/tests/run.py test_exam test_long 2>&1 | tail -15` → exit 0 · Ran 74 tests in 89.8s (18 classes, 16 at a time; slowest: ExamAuthors 89s, ExamGen 71s, Long 67s) / OK [ran] [tree 7cd3f47ca64b] (2026-10-31T07:21:57Z)
- (step 1) `python3 plugin/tests/run.py test_exam test_long` → exit 0 · Ran 74 tests in 90.7s (18 classes, 16 at a time; slowest: ExamAuthors 90s, ExamGen 73s, Long 71s) / OK [ran] [tree 7cd3f47ca64b] (2026-10-31T07:23:30Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_budget test_cli test_exam test_guard_cases test_long test_paused && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [12.19s] [ran] [tree 7cd3f47ca64b] (2026-10-31T07:25:17Z)
- `cd plugin/tests && python3 -m unittest -q test_exam test_long` → ✗ exit 1 · Ran 64 tests in 220.564s / FAILED (failures=1, errors=2) (start tree + this task's tests) [ran] [tree e1ef079446e8] (2026-10-31T07:45:10Z)
- `cd plugin/tests && python3 -m unittest -q test_exam test_long` → exit 0 · Ran 64 tests in 207.421s / OK [ran] [tree e1ef079446e8] (2026-10-31T07:45:10Z)
- (step 1) `python3 plugin/tests/run.py test_exam test_long` → exit 0 · Ran 74 tests in 70.8s (18 classes, 16 at a time; slowest: ExamAuthors 71s, ExamGen 55s, Long 30s) / OK [ran] [tree e1ef079446e8] (2026-10-31T07:46:21Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_long` → exit 0 · Ran 74 tests in 70.6s (18 classes, 16 at a time; slowest: ExamAuthors 70s, ExamGen 56s, Long 31s) / OK [ran] [tree e1ef079446e8] (2026-10-31T07:47:32Z)
- (step 3) `python3 plugin/tests/run.py test_exam test_long` → exit 0 · Ran 74 tests in 70.3s (18 classes, 16 at a time; slowest: ExamAuthors 70s, ExamGen 55s, Long 31s) / OK [ran] [tree e1ef079446e8] (2026-10-31T07:48:42Z)
- (ac 1) `python3 plugin/tests/run.py test_exam test_long` → exit 0 · Ran 74 tests in 76.7s (18 classes, 16 at a time; slowest: ExamAuthors 76s, ExamGen 60s, Long 31s) / OK [ran] [tree e1ef079446e8] (2026-10-31T07:50:00Z)
- (audit intent) `self-review of the diff: a bounded thread pool over scenarios; each session keeps its own temp copy and state dir; fmbudget.reserve checks est x (in-flight + 1) under a lock and record takes it too; the model stamp is written once before the pool; jobs 1 behaves as before but checks the budget per session` → the end-of-run production exam fits in hours (test_exam, test_long red-to-green) [tree e1ef079446e8] (2026-10-31T07:50:00Z)
- (audit adversary) `self-review of the diff: a bounded thread pool over scenarios; each session keeps its own temp copy and state dir; fmbudget.reserve checks est x (in-flight + 1) under a lock and record takes it too; the model stamp is written once before the pool; jobs 1 behaves as before but checks the budget per session` → no new spend path; the user's budget cap holds under concurrency (reserve counts sessions in flight) [tree e1ef079446e8] (2026-10-31T07:50:00Z)
- (audit edge) `self-review of the diff: a bounded thread pool over scenarios; each session keeps its own temp copy and state dir; fmbudget.reserve checks est x (in-flight + 1) under a lock and record takes it too; the model stamp is written once before the pool; jobs 1 behaves as before but checks the budget per session` → --jobs 0 refused; a budget stop mid-run lets in-flight sessions finish and record [tree e1ef079446e8] (2026-10-31T07:50:00Z)
## Log
- 2026-10-31T07:16:58Z created
- 2026-10-31T07:17:05Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2292.builder.md
- 2026-10-31T07:17:17Z focused
- 2026-10-31T07:27:15Z merged worktree-agent-abee9bcb7b8324607 (6 file(s))
- 2026-10-31T07:27:30Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-abee9bcb7b8324607
- 2026-10-31T07:38:01Z focused
- 2026-10-31T07:48:42Z scope: plugin/lib/fmbudget.py (reserve), plugin/lib/fmexam.py (run_agent jobs), plugin/lib/fmlong.py (run jobs), plugin/lib/fmcli.py (--jobs), plugin/tests/test_exam.py, test_long.py, MASTER.md, CHANGELOG.md
- 2026-10-31T07:49:32Z paused: focus moved to T-2230
- 2026-10-31T07:51:32Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- T-2158 [FEATURE M, done, 2 steps] Haiku scores are smoke signals only: fm exam scorecard, fm genesis select and the done… — lesson: A line that records what produced it …
- decision 2026-10-30: [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] Defer the full foreman-vs-plain exam and the long-horizon tier …
- decision 2026-10-30: [revisited: defer the full foreman-vs-plain exam] [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] [check: pendi…
## Lessons
- A spend check made before work starts must count the work already running, or N parallel workers each see an empty ledger
## Files touched
- plugin/tests/test_long.py
- .fm-scratch/e1.json
- plugin/tests/test_exam.py
- plugin/lib/fmbudget.py
- plugin/lib/fmexam.py
- plugin/lib/fmcli.py
- plugin/lib/fmlong.py
- CHANGELOG.md
- MASTER.md
