---
id: T-3400
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmrepro.py, CHANGELOG.md, .sampo/**]
depends_on: []
source: user
created: 2026-11-06T07:27:03Z
updated: 2026-11-06T07:28:55Z
base: cc0b40e222c2bc5b1093d488534f5e42ede73366
base_tree: 20429919737cbfeb7cf8c93bbdc4079cd13f97b9
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T07:27:05Z
plan0_scope: []
verified: ok
unproven: [meaning]
---
# fmrepro shim matches the shim template exactly (test_rename_aliases red after the T-3279 merge; the post-merge suite threatens its auto-revert)
## Raw request
> fmrepro shim matches the shim template exactly (test_rename_aliases red after the T-3279 merge; the post-merge suite threatens its auto-revert)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_rename_aliases passes on main — verify with `python3 plugin/tests/run.py test_rename_aliases`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] make plugin/lib/fmrepro.py byte-match the other shims
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_rename_aliases` → exit 0 · Ran 9 tests in 13.8s (9 jobs, 16 at a time; slowest: RenameAliases.test_nothing_but_the_shims_names_an_old_module 5s, RenameAliases.test_completion_and_help_teach_the_sampo_names 1s, RenameAliases.tes [ran] [tree 9393900f7cab] [world 2f1906870a] (2026-11-06T07:27:33Z)
- (ac 1) `python3 plugin/tests/run.py test_rename_aliases` → exit 0 · Ran 9 tests in 8.6s (1 jobs, 16 at a time; slowest: RenameAliases 6s) / OK [ran] [tree 9393900f7cab] [world 2f1906870a] (2026-11-06T07:27:42Z)
- (audit self) `one blank line removed from the fmrepro shim so it byte-matches the shim template; no behaviour change` → no findings [tree 2330361af108] (2026-11-06T07:27:50Z)
- (ac 1) `python3 plugin/tests/run.py test_rename_aliases` → exit 0 · Ran 9 tests in 9.6s (9 jobs, 16 at a time; slowest: RenameAliases.test_nothing_but_the_shims_names_an_old_module 5s, RenameAliases.test_completion_and_help_teach_the_sampo_names 1s, RenameAliases.test [ran] [tree 2330361af108] [world 2f1906870a] (2026-11-06T07:28:02Z)
- (audit self) `self: a one-blank-line shim fix` → no findings [tree 2330361af108] (2026-11-06T07:28:02Z)
## Log
- 2026-11-06T07:27:03Z created
- 2026-11-06T07:27:04Z focused
- 2026-11-06T07:27:05Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T07:27:11Z set scope=['plugin/lib/fmrepro.py', 'CHANGELOG.md', '.sampo/**']
- 2026-11-06T07:28:51Z done
- 2026-11-06T07:28:55Z committed e1b8d0c4c (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3216 [FIX S, done, 2 steps] Post-merge verify re-runs the red classes alone before reverting: a class red only inside the full suite (green alone) is a flake, logged, …
- T-3213 [FIX S, done, 2 steps] Post-merge verify blames the wrong merge: T-3189 landed on top of T-3160, T-3160 went… — lesson: blame a red on a merge only after the same…
- T-3141 [PERFORMANCE M, done, 2 steps] Fast merges part 3: land after the fast checks, run the full suite on the new main in the background, and on red revert that merge …
- decision 2026-10-30: [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] Coverage must be real: a coverage.md cell counts only when it n…
## Regression test
the existing test_rename_aliases.RenameAliases is the regression test: it failed on main at cc0b40e22 ('fmrepro' not exactly the shim, run before this change) and is the criterion's verify command
## Lessons
- a new module's shim must byte-match the template; test_rename_aliases checks it, so run it when adding a module
## Files touched
- plugin/lib/fmrepro.py
- CHANGELOG.md
