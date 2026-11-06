---
id: T-0591
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T15:16:39Z
updated: 2026-10-09T17:16:41Z
base: 1e0b573999ce578e86e1f6bd0956197a99a0c7fb
base_tree: 4ff27c2dc74eda5fff125e72322fb872e0bbabdc
verified: strong
---
# Fm pause gaps: fm session start, fm ideas, fm research ask, fm bench and the fmrelate spaw
## Raw request
> fm pause gaps: fm session start, fm ideas, fm research ask, fm bench and the fmrelate spawn still launch claude children while paused (T-0436 review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] while paused, fm session start, ideas, oracle, research ask, bench run and relate refuse with the pause note and launch nothing; the SessionStart relate spawn is skipped; Claude's own fm pause off is refused by the guard — verify with `python3 plugin/tests/run.py -p test_panic.py`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] the failing test first
2. [x] c.refuse_if_paused at each launcher's entry and its claude command builder; relate spawn skips
3. [x] guard: fm pause off is the user's (self-authorize)
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_panic.py` → ✗ exit 1 · Ran 4 tests in 3.5s (1 classes, 16 at a time; slowest: Panic 4s) / FAILED (1 classes) [ran] [tree cbc12b2d82ec] (2026-10-09T17:13:38Z)
- (step 2) `python3 plugin/tests/run.py -p test_panic.py` → exit 0 · Ran 4 tests in 2.5s (1 classes, 16 at a time; slowest: Panic 2s) / OK [ran] [tree ba46d775536d] (2026-10-09T17:16:35Z)
- (ac 1) `python3 plugin/tests/run.py -p test_panic.py` → exit 0 · Ran 4 tests in 2.5s (1 classes, 16 at a time; slowest: Panic 2s) / OK [ran] [tree ba46d775536d] (2026-10-09T17:16:40Z)
- (step 3) `python3 plugin/tests/run.py -p test_panic.py -p test_guard_pipes.py` → exit 0 · Ran 15 tests in 2.5s (11 classes, 16 at a time; slowest: Panic 3s, PipeIntoShell 0s, EvalVarsAndComputedNames 0s) / OK [ran] [tree ba46d775536d] (2026-10-09T17:16:40Z)
- (audit adversary) `self: listed every claude spawn (grep '"claude"' in lib: ideas, research, bench, session, serve, relate via ideas.run_child; plugins/doctor/tidy/setup only run claude plugin/--version, not sessions) and checked each at entry and builder` → fm pause off from Claude is self-authorize (never grantable); wrappers (env fm pause off, bash -c 'fm pause off') go through the same fm-subcommand check as --allow core; the user lifts it with ! fm pause off [tree ba46d775536d] (2026-10-09T17:16:40Z)
- (audit edge) `self: listed every claude spawn (grep '"claude"' in lib: ideas, research, bench, session, serve, relate via ideas.run_child; plugins/doctor/tidy/setup only run claude plugin/--version, not sessions) and checked each at entry and builder` → relate --no-child still runs (no claude); bench list/show/compare/models/build still work paused; 0 replay changes [tree ba46d775536d] (2026-10-09T17:16:40Z)
- (audit self) `self: listed every claude spawn (grep '"claude"' in lib: ideas, research, bench, session, serve, relate via ideas.run_child; plugins/doctor/tidy/setup only run claude plugin/--version, not sessions) and checked each at entry and builder` → no findings [tree ba46d775536d] (2026-10-09T17:16:40Z)
## Log
- 2026-10-09T15:16:39Z created
- 2026-10-09T17:13:23Z set type=SECURITY, tier=S
- 2026-10-09T17:13:23Z focused
- 2026-10-09T17:15:44Z hypothesis: refuse_if_paused at each launcher's entry and builder, a panicked() skip in relate spawn, and a self-authorize guard rule for fm pause off make the new panic test pass without breaking test_panic's resume test (it runs fm pause off through fm, not the hook)
- 2026-10-09T17:16:40Z done
- 2026-10-09T17:16:41Z committed 4181bac (9 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0436 [SECURITY M, done, 3 steps] fm pause: one flag stops everything Foreman runs unattended — lesson: a kill switch is one flag every launcher checks at its own entry…
- research T-0136-review: Verdict:** approve with nits. I found no data-loss or wrong-scope defect. These were traced by reading only. I ran nothing and did not read the d…
- research T-0383-review: Verdict: merge after fixes.** I found no CRITICAL or HIGH defects. I could not run anything, so the tests and the timing figures are unverified.
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
## Files touched
- plugin/tests/test_panic.py
- plugin/lib/fmcore.py
- plugin/lib/fmsession.py
- plugin/lib/fmideas.py
- plugin/lib/fmresearch.py
- plugin/lib/fmbench.py
- plugin/lib/fmrelate.py
- plugin/lib/fmguard.py
- CHANGELOG.md
