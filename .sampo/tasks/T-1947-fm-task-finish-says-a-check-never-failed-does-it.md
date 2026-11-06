---
id: T-1947
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T09:31:56Z
updated: 2026-10-29T09:39:10Z
base: eae4fd38db80b5d2f725cea45aa7bd43cf3473c3
base_tree: 3a9f2c759fe2f83aaddcb0f49f854bbdb4ac45e1
plan0_at: 2026-10-29T09:32:04Z
plan0_scope: []
verified: strong
---
# Fm task finish says a check never failed (does it test the change?) even when this task's
## Raw request
> FIX: fm task finish says a check never failed (does it test the change?) even when this task's own fm task prove recorded a red run first
> DONE-WHEN: a task with a red prove gets no 'does it test the change' note at the close
## Interpretation
The close's check track record warns a step's check never failed even when this task's own fm task prove recorded a red start-tree run: the proof already shows the check tests the change.
## Assumptions (confidence)
## Acceptance criteria
- [x] a task with a red prove gets no never-failed note at the close — verify with `python3 plugin/tests/run.py -k track_record`
## Non-goals
## Approach (options → choice → why)
In the finish track record, skip the never-failed note when the ledger holds a prove event for this task with red set.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then skip the note when the task proved red
## Resume here
<!-- auto -->
- 2026-10-29T09:32:12Z step 1/1: failing test, then skip the note when the task proved red
- git: foreman/build; 0 uncommitted
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k track_record` → ✗ exit 1 · Ran 2 tests in 5.0s (2 classes, 16 at a time; slowest: TrackRecord 3s, CatchRate 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 8580d1221144] (2026-10-29T09:34:13Z)
- `python3 plugin/tests/run.py -k track_record` → exit 0 · Ran 2 tests in 2.7s (2 classes, 16 at a time; slowest: TrackRecord 2s, CatchRate 0s) / OK [ran] [tree 8580d1221144] (2026-10-29T09:34:13Z)
- (step 1) `python3 plugin/tests/run.py -k track_record` → exit 0 · Ran 2 tests in 2.6s (2 classes, 16 at a time; slowest: TrackRecord 2s, CatchRate 0s) / OK [ran] [tree 8580d1221144] (2026-10-29T09:34:20Z)
- (ac 1) `python3 plugin/tests/run.py -k track_record` → exit 0 · Ran 2 tests in 2.5s (2 classes, 16 at a time; slowest: TrackRecord 2s, CatchRate 0s) / OK [ran] [tree 8580d1221144] (2026-10-29T09:38:43Z)
- (audit edge) `self-review of a 3-line change: the never-failed note now skips a task whose own prove went red then green; full gates green (4171 tests)` → a prove that failed on both trees (green nonzero) proves nothing, so the note stays; another task's prove has no effect [tree 8580d1221144] (2026-10-29T09:38:43Z)
- (audit adversary) `self-review of a 3-line change: the never-failed note now skips a task whose own prove went red then green; full gates green (4171 tests)` → a prove of an unrelated command that fails before and passes after silences the note; the note is advisory and the proof is still recorded in the brief for review [tree 8580d1221144] (2026-10-29T09:38:43Z)
- (audit self) `self-review of a 3-line change: the never-failed note now skips a task whose own prove went red then green; full gates green (4171 tests)` → no findings [tree 8580d1221144] (2026-10-29T09:38:43Z)
## Log
- 2026-10-29T09:31:56Z created
- 2026-10-29T09:32:02Z set tier=S
- 2026-10-29T09:32:03Z planned: it has criteria and steps
- 2026-10-29T09:32:04Z focused
- 2026-10-29T09:39:08Z done
- 2026-10-29T09:39:10Z committed c46d3330 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1906 [FIX S, done, 3 steps] Fm task finish checks a FIX's red-to-green proof before running its checks — lesson: A refusal known before the checks run must be said bef…
- T-1523 [FEATURE M, done, 5 steps] Round 3 (T-1520): Playbooks drafted from finished runs and history: a draft from a proved — lesson: A brief is already a distilled tran…
- T-1889 [FIX S, done, 3 steps] The fm check is piped note is given in full once per session — lesson: Record red and green with the same test command (or use fm task prov…
- decision 2026-10-15: Recommendation: close the gaps where a small model has to guess a command (done: T-0969, T-0985, T-0986, T-0987); no separate small-model mode or MC…
## Why not caught
T-0880 counted prove runs per exact command string; no test had a task whose prove ran a narrower command than its criterion
## Files touched
- plugin/tests/test_verifying.py
- plugin/lib/fmcli.py
