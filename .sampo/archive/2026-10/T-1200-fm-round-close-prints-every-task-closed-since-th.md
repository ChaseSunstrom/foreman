---
id: T-1200
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T14:09:53Z
updated: 2026-10-16T14:44:04Z
base: b0f330c538eac6e1a8f8b81fc78c0b396c7daa05
base_tree: b35585d69fdb2045cbd0876f05d431ecac4b709f
plan0_at: 2026-10-16T14:34:54Z
plan0_scope: []
verified: strong
---
# fm round close lists the newest 20 closed tasks and a count of the rest
## Raw request
> fm round close prints every task closed since the last round tag; the first round (1.2.34) printed 744 lines into the release output: show the newest 20 and a count
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] round close with more than 20 closed tasks prints the newest 20 and one '… and N more (fm round --json lists all)' line; --json still lists every id — verify with `python3 plugin/tests/run.py test_board_verbs test_round_i`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: 25 closed tasks print 20 lines and the remainder count; json has all 25
2. [x] Cap the text listing in cmd_round
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k test_round_close` → ✗ exit 1 · Ran 2 tests in 4.2s (1 classes, 16 at a time; slowest: BoardVerbs 4s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 56a591dec9d2] (2026-10-16T14:35:28Z)
- `python3 plugin/tests/run.py -k test_round_close` → exit 0 · Ran 2 tests in 3.9s (1 classes, 16 at a time; slowest: BoardVerbs 4s) / OK [ran] [tree 56a591dec9d2] (2026-10-16T14:35:28Z)
- (step 1) `python3 plugin/tests/run.py -k test_round_close` → exit 0 · Ran 2 tests in 8.3s (1 classes, 16 at a time; slowest: BoardVerbs 8s) / OK [ran] [tree a4cafa459ce5] (2026-10-16T14:35:43Z)
- (step 2) `python3 plugin/tests/run.py -k test_round_close` → exit 0 · Ran 2 tests in 9.4s (1 classes, 16 at a time; slowest: BoardVerbs 9s) / OK [ran] [tree a4cafa459ce5] (2026-10-16T14:35:53Z)
- (ac 1) `python3 plugin/tests/run.py test_board_verbs test_round_i` → exit 0 · Ran 21 tests in 26.9s (2 classes, 16 at a time; slowest: BoardVerbs 27s, RoundI 14s) / OK [ran] [tree a4cafa459ce5] (2026-10-16T14:36:31Z)
- `python3 plugin/tests/run.py -k test_round_close` → exit 0 · Ran 2 tests in 9.2s (1 classes, 16 at a time; slowest: BoardVerbs 9s) / OK [ran] [tree a4cafa459ce5] (2026-10-16T14:36:31Z)
- (audit self) `self: text output capped at the newest 20 (load order is by id), one line for the rest; --json unchanged with every id; the tag itself is unaffected` → no findings [tree a4cafa459ce5] (2026-10-16T14:36:31Z)
- `python3 plugin/tests/run.py -k test_round_close` → exit 0 · Ran 2 tests in 4.9s (1 classes, 16 at a time; slowest: BoardVerbs 5s) / OK [ran] [tree a4cafa459ce5] (2026-10-16T14:43:59Z)
- (audit self) `self: text output capped at the newest 20 (load order is by id), one line for the rest; --json unchanged with every id; the tag itself is unaffected` → no findings [tree a4cafa459ce5] (2026-10-16T14:43:59Z)
## Log
- 2026-10-16T14:09:53Z created
- 2026-10-16T14:34:53Z planned from capture
- 2026-10-16T14:34:54Z focused
- 2026-10-16T14:35:54Z scope: CHANGELOG line
- 2026-10-16T14:44:00Z affected tests waived: the one failure was a foreman-ui mod test under load (~40); the mod suite then passed with 0 fail on a rerun, and this change touches only fm round close's text
- 2026-10-16T14:44:02Z done
- 2026-10-16T14:44:04Z committed bca4e1d0 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0960 [FEATURE M, done, 3 steps] New verbs: fm oops, fm round close, fm show, fm release-check, fm sensitive suggest, fm outcomes --readme — lesson: A restore verb's me…
- T-0802 [FEATURE S, done, 2 steps] fm research list and fm research show NAME — lesson: when users and criteria keep reaching for a command that doesn't exist, add it
- T-1188 [FEATURE M, done, 3 steps] `fm release VERSION` chains release-check, canary, the release.py steps and `fm round clos — lesson: A deferred step that acts on HEAD …
- decision 2026-10-03: Self-improvement passes need N closed tasks AND 2 h since the last pass
- similar finished tasks took 2–3 steps
## Files touched
- plugin/tests/test_board_verbs.py
- plugin/lib/fmcli.py
- CHANGELOG.md
