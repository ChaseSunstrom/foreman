---
id: T-1952
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T09:50:32Z
updated: 2026-10-29T10:05:38Z
base: 3931eea019e773140d4499977a6c6e9fb6e33b73
base_tree: 7690d45fe489d5de1bc8fe7808620cd13b970113
plan0_at: 2026-10-29T09:58:20Z
plan0_scope: []
verified: strong
---
# Fm task finish reads the 50000-line ledger tail twice (catch_rates, then the T-1947 prove
## Raw request
> PERF: fm task finish reads the 50000-line ledger tail twice (catch_rates, then the T-1947 prove scan); one pass can return both
> DONE-WHEN: the close reads the ledger once for the track record
## Interpretation
The close reads the 50000-line ledger tail twice: catch_rates, then T-1947's prove scan.
## Assumptions (confidence)
## Acceptance criteria
- [x] the close reads the ledger once for the track record and still skips the note after a red prove — verify with `python3 plugin/tests/run.py -k track_record`
## Non-goals
## Approach (options → choice → why)
catch_rates collects tasks whose prove went red then green in its own pass and returns them with the rates; its one caller uses that set. Rejected: caching ledger_tail (more state for one caller).
## Risks and rollback
## Execution prompt
## Steps
1. [x] catch_rates returns the proven tasks from its one pass
## Resume here
<!-- auto -->
- 2026-10-29T09:58:25Z step 1/1: catch_rates returns the proven tasks from its one pass
- git: foreman/build; 0 uncommitted
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_verifying 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|Ran|OK|FAILED)"` → exit 0 · Ran 9 tests in 1.0s (7 classes, 16 at a time; slowest: CatchRate 1s, Claims 1s, Verifier 1s) / OK [ran] [tree 6c3fa04fbfc5] (2026-10-29T10:00:08Z)
- (step 1) `python3 plugin/tests/run.py -k track_record` → exit 0 · Ran 2 tests in 2.6s (2 classes, 16 at a time; slowest: TrackRecord 2s, CatchRate 0s) / OK [ran] [tree 6c3fa04fbfc5] (2026-10-29T10:00:14Z)
- (ac 1) `python3 plugin/tests/run.py -k track_record` → exit 0 · Ran 2 tests in 2.6s (2 classes, 16 at a time; slowest: TrackRecord 2s, CatchRate 0s) / OK [ran] [tree 6c3fa04fbfc5] (2026-10-29T10:05:12Z)
- (audit edge) `self: the one-pass set holds the same tasks the old scan matched (a prove with red set and green unset); the prove branch still feeds the rates; catch_rates has one caller` → a prove without cmd still counts as proven, as before; tests in test_verifying and track_record pass [tree 6c3fa04fbfc5] (2026-10-29T10:05:12Z)
- (audit maintainer) `self: the one-pass set holds the same tasks the old scan matched (a prove with red set and green unset); the prove branch still feeds the rates; catch_rates has one caller` → the docstring names the tuple return [tree 6c3fa04fbfc5] (2026-10-29T10:05:12Z)
- (audit self) `self: the one-pass set holds the same tasks the old scan matched (a prove with red set and green unset); the prove branch still feeds the rates; catch_rates has one caller` → no findings [tree 6c3fa04fbfc5] (2026-10-29T10:05:12Z)
## Log
- 2026-10-29T09:50:32Z created
- 2026-10-29T09:50:37Z set tier=S
- 2026-10-29T09:58:19Z planned: it has criteria and steps
- 2026-10-29T09:58:20Z focused
- 2026-10-29T10:05:37Z done
- 2026-10-29T10:05:38Z committed 443d9271 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1065-review: Verdict: changes needed.** Two MEDIUM findings, both about failures breaking normal use. I only read the code. This session had no shell, so I ra…
- T-1947 [FIX S, done, 1 steps] Fm task finish says a check never failed (does it test the change?) even when this task's
- research T-1667-review: Verdict: changes needed.** One MEDIUM and one more MEDIUM-ish lead, both small to fix. I could only read files (no shell), so I did not run the t…
- decision 2026-09-26: User approved (AskUserQuestion, 2026-09-26): once everything is finished and all gates pass, fast-forward main to foreman/build and push both branch…
- the similar finished task took 1 steps
## Measurements
ledger passes per fm task finish track record: 2 → 1 (ledger 61238 lines; each pass is a 50000-row tail, the second a memo copy of 50000 dicts plus a scan)
## Files touched
- plugin/lib/fmcli.py
