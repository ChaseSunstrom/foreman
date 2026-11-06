---
id: T-2333
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T13:53:30Z
updated: 2026-10-31T16:16:50Z
base: 6c18fc5197c4e10635fc1fb9b2e7255cd664e2f2
base_tree: bc7cf222347eaf94f23b9dbf795423a470a69c08
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-10-31T16:06:05Z
plan0_scope: []
verified: strong
---
# _VACUOUS` in plugin/lib/fmcore.py:4274 treats `ls`, `cat` and `date` as can't-fail, but…
## Raw request
> _VACUOUS` in plugin/lib/fmcore.py:4274 treats `ls`, `cat` and `date` as can't-fail, but `ls missing` and `cat missing` do fail. That makes a done-when like `ls dist` read as hollow. It is worth its o…
> (noticed by an agent; research T-2332-review)
## Interpretation
Reading 1: ls, cat and cd given a path can fail (a missing path exits non-zero), so with a path argument they are real checks and must not read as hollow. Reading 2: drop ls and cat from the set entirely; ruled out because a bare ls or cat with no path argument still can't fail on the behaviour.
## Assumptions (confidence)
## Acceptance criteria
- [x] a done-when or verify of ls, cat or cd with a path argument isn't called unable to fail; bare ls stays hollow — verify with `python3 plugin/tests/run.py test_goal`
## Non-goals
## Approach (options → choice → why)
1) use what exists: one _hollow(words) rule in fmcore that both lint_verify's first-word check and _masked use: vacuous unless ls, cat or cd carries a path argument, or exit carries a nonzero code; fails if: a path-like option is mistaken for a path (only non-dash arguments count). 2) do less: remove ls and cat from _VACUOUS; fails if: a bare ls or cat then passes as a check. 3) Run the done-when at item time to see if it can fail; fails if: slow and side-effecting at every fm goal item. Choice 1 (85%): one rule, both callers.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_goal (ls dist reads finished when dist exists; bare ls stays hollow), then one shared hollow-words rule in fmcore for lint_verify and _masked
## Resume here
<!-- auto -->
- 2026-10-31T16:13:18Z steps 1/1 done
- git: foreman/build; 2 uncommitted: plugin/lib/fmcore.py, plugin/tests/test_goal.py
- touched since last checkpoint: plugin/lib/fmcore.py, plugin/tests/test_goal.py
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_goal test_core test_diff_gates test_guard_diff test_guard` → exit 0 · Ran 464 tests in 27.6s (121 classes, 16 at a time; slowest: Mutation 24s, DiffGates 23s, GuardAgainstBash 22s) / OK [ran] [tree 1ea4e134dc55] (2026-10-31T16:08:57Z)
- `python3 plugin/tests/run.py test_goal -k done_vs_stopped` → ✗ exit 1 · Ran 1 tests in 8.8s (1 classes, 16 at a time; slowest: GoalReview 5s) / FAILED (1 classes: test_goal.GoalReview) (start tree + this task's tests) [ran] [tree 1ea4e134dc55] (2026-10-31T16:09:13Z)
- `python3 plugin/tests/run.py test_goal -k done_vs_stopped` → exit 0 · Ran 1 tests in 5.5s (1 classes, 16 at a time; slowest: GoalReview 5s) / OK [ran] [tree 1ea4e134dc55] (2026-10-31T16:09:13Z)
- (step 1) `python3 plugin/tests/run.py test_goal test_core` → exit 0 · Ran 148 tests in 5.1s (32 classes, 16 at a time; slowest: GoalReview 5s, GoalAcrossDays 5s, GoalEstimate 4s) / OK [ran] [tree 1d8fcebbc987] (2026-10-31T16:14:49Z)
- (ac 1) `python3 plugin/tests/run.py test_goal` → exit 0 · Ran 33 tests in 9.3s (7 classes, 16 at a time; slowest: GoalReview 9s, GoalAcrossDays 8s, GoalEstimate 7s) / OK [ran] [tree 8c24abb5b0fc] (2026-10-31T16:15:32Z)
- (audit intent) `fm-reviewer pass (intent, edge, maintainer); all 5 findings fixed and table-tested in test_goal` → ls/cat/cd with a path read as can-fail via lint_verify (done-when and verify) [tree 8c24abb5b0fc] (2026-10-31T16:15:32Z)
- (audit edge) `fm-reviewer pass (intent, edge, maintainer); all 5 findings fixed and table-tested in test_goal` → options, redirects (>/dev/null, 2>/dev/null), bare cat/cd, exit 0 vs 1, path fallbacks x || ls dist covered by 10 subTests [tree 8c24abb5b0fc] (2026-10-31T16:15:32Z)
- (audit maintainer) `fm-reviewer pass (intent, edge, maintainer); all 5 findings fixed and table-tested in test_goal` → one _hollow helper shared by lint_verify and _masked, pathed flag names the one difference [tree 8c24abb5b0fc] (2026-10-31T16:15:32Z)
## Log
- 2026-10-31T13:53:30Z created
- 2026-10-31T16:05:47Z planned: it has criteria and steps
- 2026-10-31T16:06:01Z focused
- 2026-10-31T16:06:05Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-10-31T16:09:21Z scope: plugin/lib/fmcore.py (_hollow, _PATHED), plugin/tests/test_goal.py
- 2026-10-31T16:16:47Z done
- 2026-10-31T16:16:50Z committed 93e1ec76 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2332-review: I found no HIGH issues. The change is small and the diff matches the two acceptance criteria. I read the code but did not run any tests. The adve…
- research T-1519-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** changes needed. Two adversary findings, on `fm new check`…
- research wave1-plan-a306a171bb6861f90: === T-1044 [stale: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmcost.py changed since it was written]
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
## Why not caught
none: the T-2332 tests only covered vacuous commands with no arguments
## Lessons
- A can't-fail list must separate 'can this command fail' from 'does this fallback mask the one before it': ls dist can fail alone yet still masks x in x || ls dist
## Files touched
- plugin/tests/test_goal.py
- plugin/lib/fmcore.py
- CHANGELOG.md
- MASTER.md
- README.md
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- plugin/lib/fmwhich.py
- plugin/tests/helpers.py
- plugin/tests/test_hooks.py
- plugin/tests/test_which.py
