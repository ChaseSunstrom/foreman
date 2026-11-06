---
id: T-2521
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/tests/test_second.py]
depends_on: []
source: discovered
created: 2026-11-02T01:35:34Z
updated: 2026-11-02T01:57:08Z
base: f73bef7553f7b77641ba193a9fbce187025823e1
base_tree: 1396a158a16f947dd5fab2d3c437ac0c357c33e6
predict_minutes: 7
predict_attempts: 1
plan0_at: 2026-11-02T01:44:26Z
plan0_scope: [plugin/lib/fmcore.py, plugin/tests/test_second.py]
verified: strong
---
# The one-way step check skips a delete or drop whose object is a code symbol
## Raw request
> The one-way step detector reads 'delete _CONF_RE' (a code edit in a tracked file, undone by git) as a one-way door and demands a rival read; a delete/remove of a symbol in a tracked source file isn't one-way: scope the verb check to untracked data or paths outside git
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a step 'delete _CONF_RE' or 'drop the unused fmcore._x helper' (the verb's object is a code identifier: snake_case with _, dotted, backticked or with ()) isn't a one-way step; 'delete data/old.csv', 'drop the users table', 'delete the release branch' still are — verify with `python3 plugin/tests/run.py test_second`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: _one_way on briefs with each step: the two code-symbol steps give '', the three data steps give their verb
2. [x] fmcore._one_way: after a delete/drop match, skip it when the next word is a code identifier (CODE_OBJ pattern); Why not caught
## Resume here
## Docs impact
none: planning-gate wording only
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_second.OneWayVerb` → ✗ exit 1 · run.py: no test matches test_second.OneWayVerb [ran] [tree c6b81ebe54cc] [world 2f1906870a] (2026-11-02T01:44:39Z)
- (step 1) `python3 plugin/tests/run.py test_second.OneWayVerb` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: OneWayVerb 0s) / FAILED (1 classes: test_second.OneWayVerb) [ran] [tree 091c2aeb4ead] [world 2f1906870a] (2026-11-02T01:44:45Z)
- (step 1) `python3 plugin/tests/run.py test_second.OneWayVerb` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: OneWayVerb 0s) / OK [ran] [tree b6a2d639b2ed] [world 2f1906870a] (2026-11-02T01:45:42Z)
- (step 2) `python3 plugin/tests/run.py test_second test_judgment` → exit 0 · Ran 100 tests in 11.0s (33 classes, 16 at a time; slowest: Rival 11s, DoorPark 9s, DoorGate 5s) / OK [ran] [tree b6a2d639b2ed] [world 2f1906870a] (2026-11-02T01:45:53Z)
- `python3 plugin/tests/run.py test_second.OneWayVerb` → ✗ exit 1 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: OneWayVerb 0s) / FAILED (1 classes: test_second.OneWayVerb) (start tree + this task's tests) [ran] [tree b6a2d639b2ed] [world 2f1906870a] (2026-11-02T01:45:56Z)
- `python3 plugin/tests/run.py test_second.OneWayVerb` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: OneWayVerb 0s) / OK [ran] [tree b6a2d639b2ed] [world 2f1906870a] (2026-11-02T01:45:56Z)
- (ac 1) `python3 plugin/tests/run.py test_second` → exit 0 · Ran 37 tests in 10.1s (13 classes, 16 at a time; slowest: Rival 10s, RivalSplit 2s, Session 1s) / OK [ran] [tree b6a2d639b2ed] [world 2f1906870a] (2026-11-02T01:51:43Z)
- (audit adversary) `self-review: _one_way skips a delete or drop only when the text right after the verb is a code identifier (backticked, snake_case word not followed by a dot, a dotted name whose last part has an underscore, or a call); a file name (old.csv, old_data.csv, users.db), a table and a branch still read one-way; the check only decides whether a plan needs a rival read, never the guard` → 'delete old_data.csv' can't pass as a symbol (\b(?!\.) after the word); 'delete `rm -rf /`' would skip the rival read, but the guard still judges the command at run time [tree b6a2d639b2ed] (2026-11-02T01:51:43Z)
- (audit edge) `self-review: _one_way skips a delete or drop only when the text right after the verb is a code identifier (backticked, snake_case word not followed by a dot, a dotted name whose last part has an underscore, or a call); a file name (old.csv, old_data.csv, users.db), a table and a branch still read one-way; the check only decides whether a plan needs a rival read, never the guard` → 'drop the unused fmcore._x helper' and 'delete parse_args()' skip; 'drop the users table' and 'delete the release branch' don't [tree b6a2d639b2ed] (2026-11-02T01:51:43Z)
- (audit self) `self-review: _one_way skips a delete or drop only when the text right after the verb is a code identifier (backticked, snake_case word not followed by a dot, a dotted name whose last part has an underscore, or a call); a file name (old.csv, old_data.csv, users.db), a table and a branch still read one-way; the check only decides whether a plan needs a rival read, never the guard` → no findings [tree b6a2d639b2ed] (2026-11-02T01:51:43Z)
## Log
- 2026-11-02T01:35:34Z created
- 2026-11-02T01:38:39Z planned from capture
- 2026-11-02T01:44:25Z focused
- 2026-11-02T01:44:26Z predicted from its closes: 7 min, 1 attempt(s)
- 2026-11-02T01:52:08Z done
- 2026-11-02T01:52:10Z committed 33297402 (2 files)
- 2026-11-02T01:52:11Z guard authorization added: publish
- 2026-11-02T01:57:08Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2424 [FEATURE M, planned, 2 steps] rival_split is read: a parked one-way door says whether the cold rival read the task differently, and ambiguous ones lead the final …
- research T-2184-review: Verdict: changes needed.** Two MEDIUM defects, plus acceptance criteria 4 and 5 still open. [stale: plugin/lib/fmfind.py, plugin/lib/fmgenesis.py…
- T-2342 [FEATURE M, done, 4 steps] Stop only at an irreversible, ambiguous step (Mission 5, #8): plan steps are classified one-way or two-way by the guard's own command p…
- decision 2026-11-02: [costly] One-way doors keep parking whether or not the task is ambiguous; rival_split only words and orders the park (T-2424)
- similar past tasks were M: consider --tier M
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_core.py
## Why not caught
HARD_RE matches the verb alone; its tests named data (a release, a branch, a table), never a step that removes a symbol from source, which this session's T-2427 did ('delete _CONF_RE').
## Lessons
- A verb list over-fires on its first case from another domain; check what the verb's object is, and keep the stricter reading for data
## Plan gaps
- failed first: step 1 red test: _one_way on briefs with each step: the two code-symbol steps give '', the three data step…
## Files touched
- plugin/tests/test_second.py
- plugin/lib/fmcore.py
