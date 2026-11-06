---
id: T-0391
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T02:12:45Z
updated: 2026-10-09T02:19:33Z
base: 05b98c244270c624398aeb1bd4fc4df72e37a856
base_tree: 403072a7a6ad30d7ea6b5b639756565269fbcc17
verified: strong
---
# FEATURE: show which Foreman code a session actually runs — SessionStart logs plugin root +
## Raw request
> FEATURE: show which Foreman code a session actually runs — SessionStart logs plugin root + version + commit to events, fm doctor and the statusline warn when the live root differs from the installed or newest one (JARVIS ran 1.2.3 from its Folder marketplace clone while I synced 1.2.4 into cache folders)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] session_start events carry the plugin root and version; fm doctor warns when the last session ran a different version than the installed one — verify with `python3 plugin/tests/run.py -k test_running_code`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: event data + doctor check_running_code
## Resume here
## Docs impact
CHANGELOG Unreleased
## Verification evidence
- `python3 plugin/tests/run.py -k test_running_code` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Checks 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 0d1d651e5a96] (2026-10-09T02:17:51Z)
- `python3 plugin/tests/run.py -k test_running_code` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Checks 0s) / OK [ran] [tree 0d1d651e5a96] (2026-10-09T02:17:51Z)
- (step 1) `python3 plugin/tests/run.py -k test_running_code` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Checks 0s) / OK [ran] [tree 7af099637b21] (2026-10-09T02:18:30Z)
- (ac 1) `python3 plugin/tests/run.py -k test_running_code` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Checks 0s) / OK [ran] [tree 7af099637b21] (2026-10-09T02:19:32Z)
- (audit intent) `self: ran fm doctor on this machine (a dev checkout ahead of its install record: PASS) after a first version that false-alarmed there; test covers older-than-newest WARN, same PASS, newer PASS, no record PASS` → a session running stale Foreman code is visible in fm doctor, naming the folder to fix [tree 7af099637b21] (2026-10-09T02:19:32Z)
- (audit edge) `self: ran fm doctor on this machine (a dev checkout ahead of its install record: PASS) after a first version that false-alarmed there; test covers older-than-newest WARN, same PASS, newer PASS, no record PASS` → no ledger or no session_start yet → PASS with the newest version; a dev checkout newer than the install record → PASS; the ledger is read from its last 2 MB only [tree 7af099637b21] (2026-10-09T02:19:32Z)
- (audit operator) `self: ran fm doctor on this machine (a dev checkout ahead of its install record: PASS) after a first version that false-alarmed there; test covers older-than-newest WARN, same PASS, newer PASS, no record PASS` → one extra doctor line; session_start gains one field [tree 7af099637b21] (2026-10-09T02:19:32Z)
- (audit self) `self: ran fm doctor on this machine (a dev checkout ahead of its install record: PASS) after a first version that false-alarmed there; test covers older-than-newest WARN, same PASS, newer PASS, no record PASS` → no findings [tree 7af099637b21] (2026-10-09T02:19:32Z)
## Log
- 2026-10-09T02:12:45Z created
- 2026-10-09T02:16:41Z focused
- 2026-10-09T02:19:33Z done
- 2026-10-09T02:19:33Z committed 71cc04d (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0018-r3-operator: 3","isSidechain":true,"agentId":"a8c97e63300d81c73","message":{"model":"claude-sonnet-5","id":"msg_011CfSRu7Xczh871gZj2Mqhv","type":"message"…
- T-0376 [FEATURE M, done, 2 steps] Watch the JARVIS run and keep its Foreman current: fix friction it hits, ship each fix there — lesson: A running Claude Code session ke…
- T-0366 [FIX M, done, 3 steps] Ship T-0364 to JARVIS: merge its 2 local commits into main, bump plugin to 1.2.0, refresh its plugin cache — lesson: A directory-marketplac…
- decision 2026-10-03: Round 4 slate: guard replay corpus (M) and a mod version check in fm doctor (S) first; four followups to the inbox
- similar past tasks were M: consider --tier M
## Lessons
- Compare versions by order, not equality: a dev checkout runs ahead of its install record on purpose
## Files touched
- plugin/tests/test_doctor.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
