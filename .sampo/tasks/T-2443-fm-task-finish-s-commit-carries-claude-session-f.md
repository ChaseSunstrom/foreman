---
id: T-2443
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T21:39:54Z
updated: 2026-10-31T21:53:15Z
base: ec14edee42e9d8501afa12f5804bc3eae87aee1a
base_tree: 360d9075bc48e75b234eba13558bb98fe26a0843
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-10-31T21:39:55Z
plan0_scope: []
verified: strong
---
# fm task finish's commit carries Claude-Session from CLAUDE_CODE_BRIDGE_SESSION_ID
## Raw request
> fm task finish's commit carries Claude-Session from CLAUDE_CODE_BRIDGE_SESSION_ID
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a finish commit made with CLAUDE_CODE_BRIDGE_SESSION_ID=session_X carries Claude-Session: https://claude.ai/code/session_X, and none without it or with a malformed id — verify with `python3 plugin/tests/run.py test_bookkeeping -k session_trailer`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then the trailer in the finish commit
## Resume here
## Docs impact
none: commit trailer only; the rule lives in the session's attribution instructions
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bookkeeping -k session_trailer` → ✗ exit 1 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: SessionTrailer 1s) / FAILED (1 classes: test_bookkeeping.SessionTrailer) [ran] [tree f8cbd08d36d9] (2026-10-31T21:40:22Z)
- (step 1) `python3 plugin/tests/run.py test_bookkeeping -k session_trailer` → exit 0 · Ran 1 tests in 2.8s (1 classes, 16 at a time; slowest: SessionTrailer 2s) / OK [ran] [tree c42010247bbe] (2026-10-31T21:40:32Z)
- (ac 1) `python3 plugin/tests/run.py test_bookkeeping -k session_trailer` → exit 0 · Ran 1 tests in 2.9s (1 classes, 16 at a time; slowest: SessionTrailer 2s) / OK [ran] [tree c42010247bbe] (2026-10-31T21:40:36Z)
- `python3 plugin/tests/run.py test_bookkeeping -k session_trailer` → ✗ exit 1 · Ran 1 tests in 2.0s (1 classes, 16 at a time; slowest: SessionTrailer 1s) / FAILED (1 classes: test_bookkeeping.SessionTrailer) (start tree + this task's tests) [ran] [tree c42010247bbe] (2026-10-31T21:40:40Z)
- `python3 plugin/tests/run.py test_bookkeeping -k session_trailer` → exit 0 · Ran 1 tests in 1.6s (1 classes, 16 at a time; slowest: SessionTrailer 1s) / OK [ran] [tree c42010247bbe] (2026-10-31T21:40:40Z)
- (ac 1) `python3 plugin/tests/run.py test_bookkeeping -k session_trailer` → exit 0 · Ran 1 tests in 1.6s (1 classes, 16 at a time; slowest: SessionTrailer 1s) / OK [ran] [tree c42010247bbe] (2026-10-31T21:45:53Z)
- (audit adversary) `self-review: trailer read from CLAUDE_CODE_BRIDGE_SESSION_ID only when it fully matches session_[A-Za-z0-9]{1,64}; full fm check green` → a malformed or injected id (spaces, ;, newlines) never reaches git: fullmatch on a closed charset, passed as one --trailer argv item with no shell [tree c42010247bbe] (2026-10-31T21:45:53Z)
- (audit edge) `self-review: trailer read from CLAUDE_CODE_BRIDGE_SESSION_ID only when it fully matches session_[A-Za-z0-9]{1,64}; full fm check green` → no id, or a message that already has Claude-Session, adds nothing; test-made commits drop the live id via helpers [tree c42010247bbe] (2026-10-31T21:45:53Z)
- (audit self) `self-review: trailer read from CLAUDE_CODE_BRIDGE_SESSION_ID only when it fully matches session_[A-Za-z0-9]{1,64}; full fm check green` → no findings [tree c42010247bbe] (2026-10-31T21:45:53Z)
## Log
- 2026-10-31T21:39:54Z created
- 2026-10-31T21:39:54Z focused
- 2026-10-31T21:39:55Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-10-31T21:40:21Z criterion 1 verify: `python3 plugin/tests/run.py test_commit -k session` → `python3 plugin/tests/run.py test_bookkeeping -k session_trailer`
- 2026-10-31T21:45:51Z scope: plugin/tests/helpers.py drops CLAUDE_CODE_BRIDGE_SESSION_ID so test-made commits never carry the live session's link
- 2026-10-31T21:46:29Z done
- 2026-10-31T21:46:31Z committed 15175702 (3 files)
- 2026-10-31T21:46:38Z guard authorization added: publish
- 2026-10-31T21:53:15Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1523 [FEATURE M, done, 5 steps] Round 3 (T-1520): Playbooks drafted from finished runs and history: a draft from a proved — lesson: A brief is already a distilled tran…
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-1821 [FEATURE M, done, 3 steps] FEATURE: one panic command stops every run, frees locks and leases and writes a stop recor — lesson: Editing plugin/rules/foreman.md ne…
- decision 2026-10-30: [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] Long-horizon tier is the deciding end-of-run score for every ca…
## Lessons
- fm task finish's commits skipped the session trailer hand-made commits carried; read it from CLAUDE_CODE_BRIDGE_SESSION_ID
## Plan gaps
- failed first: step 1 red test, then the trailer in the finish commit
## Files touched
- plugin/tests/test_bookkeeping.py
- plugin/tests/helpers.py
- plugin/lib/fmcli.py
