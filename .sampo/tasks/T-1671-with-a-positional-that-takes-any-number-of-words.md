---
id: T-1671
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_cli.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T21:03:44Z
updated: 2026-10-23T09:10:29Z
base: b78ed61b8e4a56aa92615b08e20a891b1c525079
base_tree: 6282256d51ab9d7f2ef95b973badcbb9096e15d8
plan0_at: 2026-10-23T09:08:56Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_cli.py, CHANGELOG.md]
verified: strong
---
# A flag among a command's path words strands the paths after it (fm new check --run PATH)
## Raw request
> - With a positional that takes any number of words, argparse rejects a flag placed between those words. `fm new check --run PATH` hits this, and other `fm` verbs with word lists likely do too
> (noticed by an agent; research T-1519-review-2)
## Interpretation
argparse ends a variadic positional's run at an option, so the words after it are 'unrecognized' (fm new check --run PATH). For commands whose words are paths (positional dest paths/targets or a metavar naming PATH, FILE or URL), move the command's own options and their values in front of the words before parsing. Free-text words (fm code's request, session messages, capture) are left as typed so a flag inside them stays an error, as T-0332's review asked.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm new check --run PATH and fm img diff A --tol 3 B parse as meant; unknown flags, free text and anything after -- are left as typed — verify with `python3 plugin/tests/run.py test_cli.FlagsAmongPaths`
## Non-goals
## Approach (options → choice → why)
Options: parse_intermixed_args (doesn't take subparsers); retry on 'unrecognized arguments' by appending the leftovers to the variadic (silently eats flags inside free text); move known options in front for path-list commands only. Choice: the last, beside T-0332's _options_first.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then _flags_before_paths from _options_first
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_cli.FlagsAmongPaths` → ✗ exit 1 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: FlagsAmongPaths 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 14914f7239ee] (2026-10-23T09:08:58Z)
- `python3 plugin/tests/run.py test_cli.FlagsAmongPaths` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: FlagsAmongPaths 0s) / FAILED (1 classes) [ran] [tree 14914f7239ee] (2026-10-23T09:08:58Z)
- `python3 plugin/tests/run.py test_cli.FlagsAmongPaths` → ✗ exit 1 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: FlagsAmongPaths 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree c0322f62ceaf] (2026-10-23T09:09:04Z)
- `python3 plugin/tests/run.py test_cli.FlagsAmongPaths` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: FlagsAmongPaths 0s) / OK [ran] [tree c0322f62ceaf] (2026-10-23T09:09:04Z)
- (step 1) `python3 plugin/tests/run.py test_cli test_session test_raster test_design_lint` → exit 0 · Ran 195 tests in 23.5s (57 classes, 16 at a time; slowest: TaskLifecycle 23s, StateViews 9s, AuditPrep 9s) / OK [ran] [tree c0322f62ceaf] (2026-10-23T09:10:03Z)
- (ac 1) `python3 plugin/tests/run.py test_cli.FlagsAmongPaths` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: FlagsAmongPaths 0s) / OK [ran] [tree c0322f62ceaf] (2026-10-23T09:10:03Z)
- (audit edge) `self review; the parser-touching suites green; fm new check --run PATH now reaches the command` → an unknown flag, a '?'/'*' option, free text (fm code, session send) and anything past -- are left as typed (test); --opt=value moves as one token; -p PROJECT before the command is kept [tree c0322f62ceaf] (2026-10-23T09:10:03Z)
- (audit self) `self review; the parser-touching suites green; fm new check --run PATH now reaches the command` → no findings [tree c0322f62ceaf] (2026-10-23T09:10:03Z)
## Log
- 2026-10-22T21:03:44Z created
- 2026-10-23T09:06:33Z set type=FIX, tier=S, scope=['plugin/lib/fmcli.py', 'plugin/tests/test_cli.py', 'CHANGELOG.md']
- 2026-10-23T09:06:34Z set title=A flag among a command's path words strands the paths after it (fm new check --run PATH)
- 2026-10-23T09:08:55Z focused
- 2026-10-23T09:10:27Z done
- 2026-10-23T09:10:29Z committed 5dcfbf72 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1519-review-2: All six review points are fixed test-first, in one commit on top of a clean `foreman/build` merge. The 12 tests in `test_docs` (Fences, HelpAns…
- research T-0338-review: Changes needed. I could not run anything (no execution tool), so each finding comes from tracing the code by hand. The two HIGH findings are bypa…
- research T-0323-review: Changes needed. No path-traversal hole found. Stop, hand-off and the message path have real defects. [stale: plugin/lib/fmcli.py, plugin/lib/fmse…
- decision 2026-10-22: T-1585: the guard refuses commands that name CLAUDECODE or CLAUDE_CODE_ENTRYPOINT to unset or override them, not a whole fresh environment (env -i, …
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/tests/test_cli.py; re-ground the plan against them before editing
## Why not caught
no test put a flag between a command's path words; argparse's run-ends-at-an-option rule only shows with that order
## Files touched
- plugin/tests/test_cli.py
- CHANGELOG.md
- plugin/lib/fmcli.py
