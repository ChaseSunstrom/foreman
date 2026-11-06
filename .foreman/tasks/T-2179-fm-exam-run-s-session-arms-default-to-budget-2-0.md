---
id: T-2179
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T15:40:02Z
updated: 2026-10-30T18:34:44Z
base: 64a928757d33ed5ba3d5ee9df470f28c92bc033a
base_tree: 2d46c0b79c14335deba9a88c7c9f1a79f85db949
plan0_at: 2026-10-30T18:27:20Z
plan0_scope: []
verified: strong
---
# fm exam run's session arms default to --budget 2.0 USD a session: under gen-0's 'no…
## Raw request
> fm exam run's session arms default to --budget 2.0 USD a session: under gen-0's 'no spend cap on building and proving' that's a cap on proving; drop the dollar default for exam arms (keep the timeout as the runaway stop) or make it explicit per run (found by T-2166's cold read of mission-exam.md)
## Interpretation
gen-0: 'no spend cap on building and proving'. fm exam run passes --max-budget-usd 2 to every session arm by default, so a production-model (opus) foreman session on a hard scenario is cut off mid-proof and scored as errored: a cap on proving, and on the deciding end-of-run exam. Drop the dollar default for exam arms: no --max-budget-usd unless --budget is given; the 20-minute timeout stays the runaway stop; fm budget's own user-set cap (fmbudget.check) still guards, since that's the user's limit, not Genesis's.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam run's session arms pass no --max-budget-usd unless --budget is given, and pass it when it is — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
Options: (a) budget defaults to None for exam arms, fmbench._session omits --max-budget-usd when None, fmbudget.check estimates with the 0.5 fallback (chosen: removes the cap, keeps the runaway timeout and the user's own budget); (b) raise the default to $20 (rejected: still a cap, just a later one); (c) keep $2 and count budget-capped answers apart (rejected: the score still loses the proof). Same for every arm, so the comparison stays fair.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: the stub claude logs whether --max-budget-usd was passed; none by default, 1 with --budget 1
2. [x] implement: --budget default None for fm exam run, run_agent and _session_arm; fmbench._session omits the flag on None; MASTER, CHANGELOG
## Resume here
## Docs impact
~/.claude/foreman/MASTER.md ~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam` → ✗ exit 1 · Ran 27 tests in 21.5s (10 classes, 16 at a time; slowest: ExamGen 21s, ExamAuthors 13s, ExamRust 12s) / FAILED (1 classes) [ran] [tree 6b5d37c8d4ab] (2026-10-30T18:27:42Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_bench` → ✗ exit 1 · Ran 77 tests in 33.7s (28 classes, 16 at a time; slowest: Bench 33s, Judged 21s, ExamGen 21s) / FAILED (1 classes) [ran] [tree 5f4cea25a295] (2026-10-30T18:28:20Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_bench` → exit 0 · Ran 77 tests in 34.3s (28 classes, 16 at a time; slowest: Bench 34s, Judged 21s, ExamGen 21s) / OK [ran] [tree 5f0d7945541f] (2026-10-30T18:29:46Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 27 tests in 22.0s (10 classes, 16 at a time; slowest: ExamGen 22s, ExamAuthors 13s, ExamRust 12s) / OK [ran] [tree 30bcea453ab2] (2026-10-30T18:31:12Z)
- (step 1) `python3 plugin/tests/run.py test_exam test_bench` → exit 0 · Ran 77 tests in 34.7s (28 classes, 16 at a time; slowest: Bench 34s, Judged 22s, ExamGen 21s) / OK [ran] [tree 30bcea453ab2] (2026-10-30T18:31:12Z)
- (audit intent) `self-review of the 9-line diff over intent, edge and adversary (S tier); every fmbench._session caller but fm exam passes a number, unchanged` → an exam session runs uncapped unless --budget names a cap, the same for every arm, so the foreman-vs-plain comparison stays fair [tree 30bcea453ab2] (2026-10-30T18:31:12Z)
- (audit edge) `self-review of the 9-line diff over intent, edge and adversary (S tier); every fmbench._session caller but fm exam passes a number, unchanged` → budget None skips both the --max-budget-usd flag and the over-cap error check; --budget 0 still passes 0 as the user asked; fmbudget.estimate falls back to 0.5 a session [tree 30bcea453ab2] (2026-10-30T18:31:12Z)
- (audit adversary) `self-review of the 9-line diff over intent, edge and adversary (S tier); every fmbench._session caller but fm exam passes a number, unchanged` → spend stays bounded by the per-session timeout, the default 3-scenario limit and the user's fm budget cap (fmbudget.check runs before any session); no guard, grant or risk-budget weight touched [tree 30bcea453ab2] (2026-10-30T18:31:12Z)
- (audit self) `self-review of the 9-line diff over intent, edge and adversary (S tier); every fmbench._session caller but fm exam passes a number, unchanged` → no findings [tree 30bcea453ab2] (2026-10-30T18:31:12Z)
## Log
- 2026-10-30T15:40:02Z created
- 2026-10-30T18:23:48Z planned: it has criteria and steps
- 2026-10-30T18:25:38Z set tier=S
- 2026-10-30T18:27:20Z focused
- 2026-10-30T18:32:03Z done
- 2026-10-30T18:32:05Z committed cde43a89 (6 files)
- 2026-10-30T18:32:11Z guard authorization added: publish
- 2026-10-30T18:34:44Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research draft-mission-exam-gen1: Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- decision 2026-10-30: Recommendation: keep the free finders arm as the zero-token per-generation check for the find capabilities; on s0-001 it found 90/108 (held out 30/3…
- similar past tasks were M: consider --tier M
- similar finished tasks took 4–5 steps
## Why not caught
the $2 default predates gen-0's no-cap rule and every exam so far ran Haiku, which never reached it; T-2166's cold read of mission-exam.md caught it
## Lessons
- A default that caps a measurement biases the measurement: a dollar cap per exam session scored the costliest (production) model's cut-off proofs as errors. Runaway protection belongs to time and the user's own budget, not to a per-run dollar default.
## Plan gaps
- failed first: step 1 red test: the stub claude logs whether --max-budget-usd was passed; none by default, 1 with --budge…
- failed first: step 2 implement: --budget default None for fm exam run, run_agent and _session_arm; fmbench._session omit…
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/fmbench.py
- plugin/lib/fmcli.py
- plugin/lib/fmexam.py
- CHANGELOG.md
- MASTER.md
