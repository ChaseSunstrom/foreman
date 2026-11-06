---
id: T-2159
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-30T14:08:41Z
updated: 2026-10-30T14:40:16Z
base: fe25294c74feba41276c6d07af5d78cd49bd2cca
base_tree: a297675d052e5077de71e5af438cff0e0b1f553f
plan0_at: 2026-10-30T14:18:06Z
plan0_scope: [plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# Coverage must be real: reset coverage.md's templated cells (a shim to…, a site page to…,…
## Raw request
> Coverage must be real: reset coverage.md's templated cells (a shim to…, a site page to…, a panel to…) to empty, and make fm genesis check flag a cell that reads the same as another row's with the area name swapped, so only concrete file- or gap-grounded cells count (steer 2026-10-30 rule 2)
## Interpretation
The user's steer (rule 2): coverage.md was template-filled ('a shim to…', 'a panel to…'), so the grid's 'no empty cell' rule passed on filler. A cell counts only when it names something concrete; one that reads the same as another slot's cell with the area or stage swapped is templated: a coverage problem naming its twin, not filled. The check lives in coverage(), so fm genesis check, seed and sweep all enforce it; the existing templated cells are reset to empty.
## Assumptions (confidence)
## Acceptance criteria
- [x] a templated I or N/A cell (same frame as a cell in another slot with the area or stage phrase swapped) is a coverage problem naming its twin and isn't counted filled; a concrete cell and an F cell still count — verify with `python3 plugin/tests/run.py test_genesis`
- [x] coverage.md's templated cells are reset to empty and fm genesis check reports no templated cell — verify with `fm genesis check --json | python3 -c "import json,sys; sys.exit(json.load(sys.stdin)['coverage']['templated'])"`
- [x] of two identical F cells only the later copy is flagged, a surface-swapped twin in one slot is flagged, and a non-F cell under 3 words is too short — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
Complete version: coverage() refuses a templated I or N/A cell (not filled, a problem naming its twin), fm genesis check and status show the count, coverage.md's templated cells are reset to empty, and the seed asks for concrete cells. Options: (a) per surface column, a cell is templated when difflib's word-level match with a cell in another slot shares >= 4 words and ratio >= 0.6 — it reads the same with the area or stage phrase swapped (chosen: learned from the grid itself, no phrase list; on today's coverage.md it flags 1121 of 1138 I cells and all 44 N/A, keeps the 17 concrete ones, 0.6 s); (b) a hard-coded list of frames ('a shim to', 'a panel to') — rejected: misses the next template, and the standing rule is no hardcoded lists; (c) only a cold fm second read — kept as the second opinion the seed asks for, but non-deterministic and paid; (d) n-gram frequency across rows — flags legitimate shared nouns. F cells stay exempt: they name a shipped path, and one feature can serve two areas.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: test_genesis case for a templated pair, a concrete pair and an F duplicate
2. [x] coverage(): templated twins per surface column (difflib, words >= 4, ratio >= 0.6), problem names the twin; MASTER, CHANGELOG
3. [x] reset coverage.md's templated cells to empty via fm genesis put
## Resume here
<!-- auto -->
- 2026-10-30T14:32:08Z steps 3/3 done
- git: foreman/build; 4 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py
- touched since last checkpoint: plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py
## Docs impact
MASTER.md fmgenesis row, CHANGELOG Unreleased
## Verification evidence
- `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 79 tests in 9.9s (12 classes, 16 at a time; slowest: GenesisLive 8s, GenesisSweep 7s, GenesisCheck 7s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree a97e15af544a] (2026-10-30T14:20:08Z)
- `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 79 tests in 12.0s (12 classes, 16 at a time; slowest: GenesisLive 12s, GenesisSweep 10s, GenesisCheck 9s) / FAILED (1 classes) [ran] [tree a97e15af544a] (2026-10-30T14:20:08Z)
- `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 79 tests in 5.1s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree cff07e679e6f] (2026-10-30T14:21:11Z)
- `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 79 tests in 4.3s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree cff07e679e6f] (2026-10-30T14:21:11Z)
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 79 tests in 4.3s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree cff07e679e6f] (2026-10-30T14:21:16Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 79 tests in 4.3s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 66bb16552a55] (2026-10-30T14:22:04Z)
- (step 3) `fm genesis check --json | python3 -c "import json,sys; sys.exit(json.load(sys.stdin)['coverage']['templated'])"` → exit 0 · (no output) [ran] [tree 66bb16552a55] (2026-10-30T14:22:39Z)
- (ac 2) `fm genesis check --json | python3 -c "import json,sys; sys.exit(json.load(sys.stdin)['coverage']['templated'])"` → exit 0 · (no output) [ran] [tree 66bb16552a55] (2026-10-30T14:22:39Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 79 tests in 4.3s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 66bb16552a55] (2026-10-30T14:22:44Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 79 tests in 4.3s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree f930cbcb0c86] (2026-10-30T14:34:56Z)
- (ac 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 79 tests in 4.3s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree f930cbcb0c86] (2026-10-30T14:35:00Z)
- (ac 2) `fm genesis check --json | python3 -c "import json,sys; sys.exit(json.load(sys.stdin)['coverage']['templated'])"` → exit 0 · (no output) [ran] [tree f930cbcb0c86] (2026-10-30T14:35:01Z)
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 79 tests in 4.3s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree f930cbcb0c86] (2026-10-30T14:35:05Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 79 tests in 4.3s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree f930cbcb0c86] (2026-10-30T14:35:10Z)
- (step 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 79 tests in 4.3s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree f930cbcb0c86] (2026-10-30T14:35:15Z)
- (audit intent) `fm-reviewer (research T-2159-review)` → 2 LOW: short cells now a 'too short' problem (3+ words besides the area); both twins flagged by design except an F-F pair, where only the later copy is [tree 6533e23ab8ed] (2026-10-30T14:35:50Z)
- (audit edge) `fm-reviewer (research T-2159-review)` → 1 LOW: templated problems now list before the empty ones, so a short listing and the 50-problem export show them first [tree 6533e23ab8ed] (2026-10-30T14:35:50Z)
- (audit operator) `fm-reviewer (research T-2159-review)` → 1 LOW: timing claim replaced by a measurement, 0.28 s on a full 1,408-cell grid [tree 6533e23ab8ed] (2026-10-30T14:35:50Z)
- (audit maintainer) `fm-reviewer (research T-2159-review)` → 2 LOW + test gap: seed table says 'ungrounded or templated'; difflib moved to the header; test asserts each row's ideas and bad counts after twins [tree 6533e23ab8ed] (2026-10-30T14:35:51Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 79 tests in 4.3s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 6533e23ab8ed] (2026-10-30T14:35:55Z)
- (ac 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 79 tests in 4.3s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 6533e23ab8ed] (2026-10-30T14:36:00Z)
- (ac 2) `fm genesis check --json | python3 -c "import json,sys; sys.exit(json.load(sys.stdin)['coverage']['templated'])"` → exit 0 · (no output) [ran] [tree 6533e23ab8ed] (2026-10-30T14:36:00Z)
- (ac 2) `fm genesis check --json | python3 -c "import json,sys; sys.exit(json.load(sys.stdin)['coverage']['templated'])"` → exit 0 · (no output) [ran] [tree 6533e23ab8ed] (2026-10-30T14:36:23Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 79 tests in 4.3s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 6533e23ab8ed] (2026-10-30T14:36:42Z)
- (ac 2) `fm genesis check --json | python3 -c "import json,sys; sys.exit(json.load(sys.stdin)['coverage']['templated'])"` → exit 0 · (no output) [ran] [tree 6533e23ab8ed] (2026-10-30T14:36:42Z)
- (ac 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 79 tests in 4.3s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 6533e23ab8ed] (2026-10-30T14:36:42Z)
- (audit intent) `one fm-reviewer pass (intent, edge, operator, maintainer: 6 LOW + 1 test gap, all fixed) plus three cold Haiku reads of coverage.md, the last a pass` → steer 1's real-coverage rule and steer 2's automatic check hold: templated cells along area, stage and surface are refused, short cells too; coverage.md has 0 templated [tree 6533e23ab8ed] (2026-10-30T14:36:42Z)
- (audit edge) `one fm-reviewer pass (intent, edge, operator, maintainer: 6 LOW + 1 test gap, all fixed) plus three cold Haiku reads of coverage.md, the last a pass` → an F-F twin flags only the later copy; a surface-swapped twin in one slot is caught; empties list last [tree 6533e23ab8ed] (2026-10-30T14:36:42Z)
## Log
- 2026-10-30T14:08:41Z created
- 2026-10-30T14:13:20Z set type=FEATURE, tier=M, scope=['plugin/lib/fmgenesis.py', 'plugin/tests/test_genesis.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-30T14:13:21Z planned: it has criteria and steps
- 2026-10-30T14:18:04Z focused
- 2026-10-30T14:22:39Z criterion 2 verify: `fm genesis check` → `fm genesis check --json | python3 -c "import json,sys; sys.exit(json.load(sys.stdin)['coverage']['templated'])"`
- 2026-10-30T14:34:51Z steer 2: the cold read's identical F cells across areas are now caught by the detector (F included, later copy flagged), so the same class needs no second steer
- 2026-10-30T14:36:23Z cold read 3 (fm-scout haiku): VERDICT pass; fixed the one overstated cell it named (12 plan × CLI fmbudget) and dropped Performance's vague copy
- 2026-10-30T14:37:04Z done
- 2026-10-30T14:37:06Z committed b38f9f3a (4 files)
- 2026-10-30T14:37:53Z guard authorization added: publish
- 2026-10-30T14:40:16Z publish grant used by fm ship
## Follow-ups captured
## Behaviour lock
test_genesis GenesisCheck: a full grid of distinct cells still passes 192/192; empty, ungrounded and unknown cells are still flagged as before
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-30: [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] Coverage must be real: a coverage.md cell counts only when it n…
- research T-2093-review: Verdict: changes needed.** One MEDIUM defect lets the not-yet check pass an item that has an empty field. The other findings are LOW. I traced th…
- T-2093 [FEATURE M, done, 3 steps] Genesis check: coverage grid + not-yet ledger validation (fm genesis check) — lesson: A regex field parser with \s* after the colon rea…
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_genesis.py
## Lessons
- A templated-text detector has to compare along every axis a writer can swap (area, stage and surface), and include grounded cells too: identical F cells across areas passed the first version
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
