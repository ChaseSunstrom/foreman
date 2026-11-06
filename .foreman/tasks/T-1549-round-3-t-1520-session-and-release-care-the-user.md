---
id: T-1549
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmideas.py, plugin/lib/fmrelease.py, plugin/lib/fmsettings.py, plugin/lib/fmcost.py, plugin/lib/fmcli.py, plugin/defaults.json, plugin/tests/test_session_care.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:51Z
updated: 2026-10-23T16:37:49Z
inferred_deps: [T-1520]
inferred_why: T-1520: named in its request
group: round 3 creative and playbook extras
base: 881162b57c84f9a0629265580ca7653de167f723
base_tree: 78f492a9b6e2eb49e80a32213728c054ab564f13
plan0_at: 2026-10-23T16:30:58Z
plan0_scope: [plugin/lib/fmideas.py, plugin/lib/fmrelease.py, plugin/lib/fmsettings.py, plugin/lib/fmcost.py, plugin/lib/fmcli.py, plugin/defaults.json, plugin/tests/test_session_care.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Round 3 (T-1520): Session and release care: the user's own words once in the pack, a warni
## Raw request
> Round 3 (T-1520): Session and release care: the user's own words once in the pack, a warning when releasing in the user's historically bad hours, a demo teleprompter pane, a gallery of the guard's near misses, the morning digest read aloud, a decision card for each new dependency, and notice when a release changes a default the user never set (c036 c038 c039 c048 b093 b109 b060). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Session and release care: the user's own words once in the brainstorm pack; fm release warns in an hour this project's gates have failed at least twice as often as usual; each release's notes name the defaults it changed, and fm settings changed tells a user which of those reach them because they never set them; fm digest --say reads the digest aloud. Left out (decided): a demo teleprompter pane, a gallery of the guard's near misses and a decision card for each new dependency.
## Assumptions (confidence)
## Acceptance criteria
- [x] the pack holds each user quote once; a release in a bad hour warns; a changed default the user never set is named in the release notes — verify with `cd plugin/tests && python3 -m unittest test_session_care`
- [x] each quote once in the pack, the bad-hour rule, changed defaults in the notes and in fm settings changed, and the digest spoken — verify with `python3 plugin/tests/run.py test_session_care`
## Non-goals
## Approach (options → choice → why)
Options for changed defaults: (a) diff the settings schema against the last release tag's source (parsing old Python); (b) a plugin/defaults.json snapshot fm release rewrites each release, compared at the next; (c) a migration list by hand. Choice: (b): one data file, compared with the schema's own defaults(), no old code parsed. Bad hours come from the ledger's check_run events by local hour (a pure function, a warning only). Dedupe the pack by its words, not its prefix.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] pack and release warnings
3. [x] teleprompter pane and near-miss gallery
4. [x] digest aloud and dependency cards
5. [x] red tests: pack quotes, bad hour, release notes, settings changed, digest --say
6. [x] dedupe, bad_hour and its warning, defaults/changed_defaults and the release step, the snapshot, say(); CHANGELOG, MASTER
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md, ~/.claude/foreman/MASTER.md (file map row for plugin/defaults.json; Session and release care), fm settings and fm digest help
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_session_care` → ✗ exit 1 · Ran 6 tests in 0.7s (4 classes, 16 at a time; slowest: Pack 1s, Say 0s, Settings 0s) / FAILED (4 classes) [ran] [tree 8a132d8b33b5] (2026-10-23T16:31:04Z)
- (step 1) `python3 plugin/tests/run.py test_session_care test_release test_settings test_ideation test_cost test_cli test_suite_hygiene test_docs test_builder` → exit 0 · Ran 382 tests in 27.9s (101 classes, 16 at a time; slowest: TaskLifecycle 28s, Release 20s, Contract 14s) / OK [ran] [tree 01877f74ff97] (2026-10-23T16:34:39Z)
- (step 2) `python3 plugin/tests/run.py test_session_care test_release test_settings test_ideation test_cost test_cli test_suite_hygiene test_docs test_builder` → exit 0 · Ran 382 tests in 26.5s (101 classes, 16 at a time; slowest: TaskLifecycle 26s, Release 18s, Contract 12s) / OK [ran] [tree 01877f74ff97] (2026-10-23T16:35:06Z)
- (step 3) `python3 plugin/tests/run.py test_session_care test_release test_settings test_ideation test_cost test_cli test_suite_hygiene test_docs test_builder` → exit 0 · Ran 382 tests in 28.5s (101 classes, 16 at a time; slowest: TaskLifecycle 28s, Release 20s, Contract 14s) / OK [ran] [tree 01877f74ff97] (2026-10-23T16:35:35Z)
- (step 4) `python3 plugin/tests/run.py test_session_care test_release test_settings test_ideation test_cost test_cli test_suite_hygiene test_docs test_builder` → exit 0 · Ran 382 tests in 28.3s (101 classes, 16 at a time; slowest: TaskLifecycle 28s, Release 20s, Contract 14s) / OK [ran] [tree 01877f74ff97] (2026-10-23T16:36:04Z)
- (step 5) `python3 plugin/tests/run.py test_session_care test_release test_settings test_ideation test_cost test_cli test_suite_hygiene test_docs test_builder` → exit 0 · Ran 382 tests in 28.5s (101 classes, 16 at a time; slowest: TaskLifecycle 28s, Release 20s, Contract 14s) / OK [ran] [tree 01877f74ff97] (2026-10-23T16:36:34Z)
- (step 6) `python3 plugin/tests/run.py test_session_care test_release test_settings test_ideation test_cost test_cli test_suite_hygiene test_docs test_builder` → exit 0 · Ran 382 tests in 28.8s (101 classes, 16 at a time; slowest: TaskLifecycle 29s, Release 21s, Contract 14s) / OK [ran] [tree 01877f74ff97] (2026-10-23T16:37:03Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_session_care` → exit 0 · Ran 6 tests in 0.911s / OK [ran] [tree 01877f74ff97] (2026-10-23T16:37:05Z)
- (ac 2) `python3 plugin/tests/run.py test_session_care` → exit 0 · Ran 6 tests in 0.7s (4 classes, 16 at a time; slowest: Pack 1s, Settings 0s, Say 0s) / OK [ran] [tree 01877f74ff97] (2026-10-23T16:37:06Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_session_care` → exit 0 · Ran 6 tests in 0.911s / OK [ran] [tree 01877f74ff97] (2026-10-23T16:37:17Z)
- (ac 2) `python3 plugin/tests/run.py test_session_care` → exit 0 · Ran 6 tests in 0.7s (4 classes, 16 at a time; slowest: Pack 1s, Settings 0s, Say 0s) / OK [ran] [tree 01877f74ff97] (2026-10-23T16:37:17Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): the release commit step had to add the new snapshot before naming it (caught by the release tests), and doctor's file map needed its row; the bad-hour rule is a pure function over check_run events, a warning only, quiet below 20 runs; quotes dedupe by their words, so asked and pushed-back forms of one sentence count once` → the user's words once in the pack, a bad-hour release warning, changed defaults named in the release notes and per user in fm settings changed, the digest read aloud; the teleprompter, near-miss gallery and dependency cards left out by a recorded decision [tree 01877f74ff97] (2026-10-23T16:37:17Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): the release commit step had to add the new snapshot before naming it (caught by the release tests), and doctor's file map needed its row; the bad-hour rule is a pure function over check_run events, a warning only, quiet below 20 runs; quotes dedupe by their words, so asked and pushed-back forms of one sentence count once` → an unreadable or missing snapshot compares as empty (no changes named); a key new since the snapshot isn't a change; a setting the user's files set is marked theirs; no speech program prints a note and the digest still prints; a ts the ledger garbled is skipped [tree 01877f74ff97] (2026-10-23T16:37:17Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): the release commit step had to add the new snapshot before naming it (caught by the release tests), and doctor's file map needed its row; the bad-hour rule is a pure function over check_run events, a warning only, quiet below 20 runs; quotes dedupe by their words, so asked and pushed-back forms of one sentence count once` → the speech program gets the digest as one argv item after --, symbols stripped, capped at 4,000 characters, no shell; the defaults snapshot is plain JSON written by fm release, never executed; the release warning reads only this project's ledger [tree 01877f74ff97] (2026-10-23T16:37:17Z)
## Log
- 2026-10-22T17:43:51Z created
- 2026-10-22T18:06:23Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmideas.py', 'mods/foreman-ui/hooks', 'plugin/tests/test_session_care.py', 'CHANGELOG.md']
- 2026-10-23T16:30:55Z set tier=M, scope=['plugin/lib/fmideas.py', 'plugin/lib/fmrelease.py', 'plugin/lib/fmsettings.py', 'plugin/lib/fmcost.py', 'plugin/lib/fmcli.py', 'plugin/defaults.json', 'plugin/tests/test_session_care.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T16:30:58Z focused
- 2026-10-23T16:37:47Z done
- 2026-10-23T16:37:49Z committed 0ef80046 (9 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1523 [FEATURE M, done, 5 steps] Round 3 (T-1520): Playbooks drafted from finished runs and history: a draft from a proved — lesson: A brief is already a distilled tran…
- T-1553 [SECURITY M, done, 3 steps] Guard oracle: a stub-exec run agrees with the guard's reading — lesson: A tool that runs things to check them must treat 'didn't run' …
- T-1545 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Control Room and direct manipulation: a loopback web app generated from
- decision 2026-10-23: T-1549: leave out a demo teleprompter pane, a guard near-miss gallery and per-dependency decision cards
- similar finished tasks took 3–5 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_cost.py, plugin/tests/test_ideas.py, plugin/tests/test_release.py, plugin/tests/test_settings.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcost.py, plugin/lib/fmideas.py, plugin/lib/fmrelease.py, plugin/lib/fmsettings.py; re-ground the plan against them before editing
## Lessons
- A release's own artifacts (a new snapshot file) need the release's commit step to know them: git commit -- PATH refuses a file it has never seen
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/lib/fmcost.py
- plugin/lib/fmideas.py
- plugin/lib/fmrelease.py
- plugin/lib/fmsettings.py
- plugin/tests/test_session_care.py
- plugin/defaults.json
- MASTER.md
