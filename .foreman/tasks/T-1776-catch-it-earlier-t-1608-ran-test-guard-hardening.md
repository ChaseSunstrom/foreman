---
id: T-1776
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/tests/test_help.py, plugin/tests/test_cli.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-23T10:41:53Z
updated: 2026-10-23T11:28:07Z
base: 843a67f97b79096adca8fbf03cfd15d791d75744
base_tree: 4557f6bfa73ee123fd66889a9cc62f942c7becfe
plan0_at: 2026-10-23T11:24:50Z
plan0_scope: [plugin/tests/test_help.py, plugin/tests/test_cli.py, CHANGELOG.md]
verified: strong
---
# Catch it earlier: T-1608 ran test_guard_hardening, test_docs and test_cli; the help-positi
## Raw request
> T-1775 (fm dojo shares help position 306 with another command, so test_help fails) wasn't caught before it shipped: T-1608 ran test_guard_hardening, test_docs and test_cli; the help-position test lives in test_help, which only the full suite ran
## Interpretation
The help-position check (and the tiers-from-registrations check) test fmcli.py's command registrations but live in test_help, which nothing links to fmcli.py: fm map links tests by name, and fmcli.py co-changes with so many tests that its pairs are dropped (T-1467). So a task editing fmcli.py runs test_cli, never test_help, and T-1608 shipped a shared position.
## Assumptions (confidence)
## Acceptance criteria
- [x] test_cli holds the help-position and tiers checks, so an fmcli.py change runs them; test_help keeps the help-output tests — verify with `python3 plugin/tests/run.py test_cli.HelpRegistrations test_help`
## Non-goals
## Approach (options → choice → why)
Options: (1) move the two registration tests into test_cli (chosen: the file every fmcli.py change already runs; no new mechanism); (2) refuse a shared position when the parser is built (rejected: a slip would break every fm call, hooks included, mid-task); (3) a covers: line test files declare for fm map (rejected for now: a new mechanism for one case; capture if a second appears).
## Risks and rollback
## Execution prompt
## Steps
1. [x] move the two registration tests into test_cli
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli.HelpRegistrations` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: HelpRegistrations 0s) / OK [ran] [tree 1c0d70a9a59f] (2026-10-23T11:27:29Z)
- (ac 1) `python3 plugin/tests/run.py test_cli.HelpRegistrations test_help` → exit 0 · Ran 7 tests in 0.9s (4 classes, 16 at a time; slowest: Help 1s, PromptApprovals 1s, Rules 0s) / OK [ran] [tree 6e2fd31b70fb] (2026-10-23T11:27:39Z)
- (ac 1) `python3 plugin/tests/run.py test_cli.HelpRegistrations test_help` → exit 0 · Ran 7 tests in 0.9s (4 classes, 16 at a time; slowest: Help 1s, PromptApprovals 1s, Rules 0s) / OK [ran] [tree 6e2fd31b70fb] (2026-10-23T11:27:41Z)
- (audit edge) `self: a move, not a change: the two tests are byte-for-byte the same checks (fmcli imported at test_cli's top instead of inside each), and test_help keeps its help-output tests with all its imports still used` → a shared position or a command missing from the tiers now fails test_cli, which fm map links to fmcli.py, so the affected run of any fmcli.py change (and the ambient runner) catches it before the full suite [tree 6e2fd31b70fb] (2026-10-23T11:27:41Z)
- (audit self) `self: a move, not a change: the two tests are byte-for-byte the same checks (fmcli imported at test_cli's top instead of inside each), and test_help keeps its help-output tests with all its imports still used` → no findings [tree 6e2fd31b70fb] (2026-10-23T11:27:41Z)
## Log
- 2026-10-23T10:41:53Z created
- 2026-10-23T11:20:08Z set tier=S, scope=['plugin/tests/test_help.py', 'plugin/tests/test_cli.py', 'CHANGELOG.md']
- 2026-10-23T11:24:50Z focused
- 2026-10-23T11:28:05Z done
- 2026-10-23T11:28:07Z committed 819a6dde (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0952 [FEATURE S, done, 1 steps] --affected also runs tests that historically change together with the edited files (the map's co-change pairs), so a hooks.json edit ru…
- T-1775 [FIX S, done, 1 steps] fm dojo shares help position 306 with another command, so test_help fails
- T-1179 [FEATURE S, done, 2 steps] Catch it earlier: T-0787 ran test_workflows only; the doctor's file-map rule is checked by
- decision 2026-10-04: Drop T-0305 (edit a criterion in place)
- similar finished tasks took 1–2 steps
- start here (files T-0952 touched): plugin/tests/test_cli.py, plugin/lib/fmcli.py
## Lessons
- A test of a file's own contents belongs in the test file named after it: fm map links by name, and a hub file's co-change pairs are dropped
## Files touched
- plugin/tests/test_cli.py
- CHANGELOG.md
- plugin/tests/test_help.py
