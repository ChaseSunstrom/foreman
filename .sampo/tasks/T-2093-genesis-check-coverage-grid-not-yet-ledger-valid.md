---
id: T-2093
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T04:36:58Z
updated: 2026-10-30T04:52:54Z
base: c2a662148bd92e9ed0435d1193347f39713f76e4
base_tree: 5dbdf1d14568a1fe253e98c34bcc794d7d1bae74
plan0_at: 2026-10-30T04:37:12Z
plan0_scope: []
verified: strong
---
# Genesis check: coverage grid + not-yet ledger validation (fm genesis check)
## Raw request
> Genesis check: coverage grid + not-yet ledger validation (fm genesis check)
## Interpretation
Gen-1 standing rules 1-3 (seed.md): coverage.md has one '## <area>' per row and one '- <stage> × <surface>: F|I|N/A: …' line per cell, no empty cell; not-yet.md items carry a blocker, ≥2 tried approaches, what unblocks them and a retry this generation. A deterministic checker makes both rules enforceable (the sweep and the orchestrator call it). Part of Genesis Mission 2 (T-2077).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis check flags empty/bad coverage cells and not-yet items lacking 2 tries or this generation's retry; exits 1 on any — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis`
- [x] status shows coverage filled/empty and not-yet open counts — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
Approaches: (a) fmgenesis.check(p) parsing both docs with regexes, used by fm genesis check, status and later the sweep (chosen: smallest, one place); (b) a JSON/TOML grid instead of markdown (rejected: seed fixes the markdown format, and the site renders the docs); (c) model-graded fill check (rejected for the check itself: deterministic first; a model --fill can come later). Required rows = gen-0 §2's capabilities (read from gen-0, no hardcoded list); stages and surfaces are the seed's 8×8; F paths resolve against the project root; I cells need an existing (file); current gen = the newest gen with a seed.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests for coverage and not-yet checks
2. [x] implement check + status counts + CLI verb
3. [x] docs: MASTER.md, CHANGELOG, skill line
## Resume here
<!-- auto -->
- 2026-10-30T04:41:20Z step 1/3: red tests for coverage and not-yet checks
- git: foreman/build; 5 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py
- touched since last checkpoint: plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, CHANGELOG.md, MASTER.md
## Docs impact
MASTER.md fmgenesis entry (check), CHANGELOG Unreleased
## Verification evidence
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis.GenesisCheck` → ✗ exit 1 · Ran 6 tests in 1.3s (1 classes, 16 at a time; slowest: GenesisCheck 1s) / FAILED (1 classes) [ran] [tree 29cb94291c22] (2026-10-30T04:38:55Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis 2>&1 | tail -30` → ✗ exit 1 · Ran 20 tests in 2.7s (4 classes, 16 at a time; slowest: GenesisLive 2s, Genesis 1s, GenesisCheck 1s) / FAILED (1 classes) [ran] [tree 64cf6e36d7fd] (2026-10-30T04:40:11Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis 2>&1 | tail -30` → ✗ exit 1 · Ran 20 tests in 2.7s (4 classes, 16 at a time; slowest: GenesisLive 2s, Genesis 1s, GenesisCheck 1s) / FAILED (1 classes) [ran] [tree 64cf6e36d7fd] (2026-10-30T04:40:11Z)
- (step 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis` → exit 0 · Ran 20 tests in 2.6s (4 classes, 16 at a time; slowest: GenesisLive 2s, Genesis 1s, GenesisCheck 1s) / OK [ran] [tree 2abdf0871837] (2026-10-30T04:40:41Z)
- (step 3) `grep -c 'fm genesis check' CHANGELOG.md MASTER.md` → exit 0 · CHANGELOG.md:1 / MASTER.md:0 [ran] [tree cf8646ee5cc0] (2026-10-30T04:40:56Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis 2>&1 | grep -E "FAIL|ERROR|Error|assert|^Ran|^OK|FAILED" | head -20` → ✗ exit 1 · Ran 22 tests in 2.7s (4 classes, 16 at a time; slowest: GenesisLive 2s, GenesisCheck 2s, Genesis 1s) / FAILED (1 classes) [ran] [tree e12ef4ed8cee] (2026-10-30T04:43:47Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis 2>&1 | grep -E "FAIL|ERROR|Error|assert|^Ran|^OK|FAILED" | head -20` → ✗ exit 1 · Ran 22 tests in 2.7s (4 classes, 16 at a time; slowest: GenesisLive 2s, GenesisCheck 2s, Genesis 1s) / FAILED (1 classes) [ran] [tree e12ef4ed8cee] (2026-10-30T04:43:47Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis` → exit 0 · Ran 22 tests in 2.7s (4 classes, 16 at a time; slowest: GenesisLive 2s, GenesisCheck 2s, Genesis 1s) / OK [ran] [tree b33f8a3d2bf5] (2026-10-30T04:48:14Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis` → exit 0 · Ran 22 tests in 2.7s (4 classes, 16 at a time; slowest: GenesisLive 2s, GenesisCheck 2s, Genesis 1s) / OK [ran] [tree b33f8a3d2bf5] (2026-10-30T04:48:14Z)
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis.GenesisCheck` → exit 0 · Ran 8 tests in 1.8s (1 classes, 16 at a time; slowest: GenesisCheck 2s) / OK [ran] [tree b33f8a3d2bf5] (2026-10-30T04:48:14Z)
- (audit intent) `fm-reviewer pass (intent, edge, operator, adversary, maintainer); 1 medium + 6 low verified and fixed test-first` → CHANGELOG reworded to what ships; status line now says K empty [tree b33f8a3d2bf5] (2026-10-30T04:48:14Z)
- (audit edge) `fm-reviewer pass (intent, edge, operator, adversary, maintainer); 1 medium + 6 low verified and fixed test-first` → empty field no longer borrows the next line ([ \t]* after the colon, test); tries counted as distinct; grid with no ## rows flagged; trailing ,;. stripped from F paths; not-yet '… N more' line [tree b33f8a3d2bf5] (2026-10-30T04:48:14Z)
- (audit adversary) `fm-reviewer pass (intent, edge, operator, adversary, maintainer); 1 medium + 6 low verified and fixed test-first` → no findings — cell paths realpath-contained, problem text through c.plain, export scrubbed [tree b33f8a3d2bf5] (2026-10-30T04:48:14Z)
- (audit maintainer) `fm-reviewer pass (intent, edge, operator, adversary, maintainer); 1 medium + 6 low verified and fixed test-first` → two new tests pin the empty-field and duplicate-tries cases [tree b33f8a3d2bf5] (2026-10-30T04:48:14Z)
- (audit operator) `fm-reviewer pass (intent, edge, operator, adversary, maintainer); 1 medium + 6 low verified and fixed test-first` → export no longer runs the check twice [tree b33f8a3d2bf5] (2026-10-30T04:48:14Z)
## Log
- 2026-10-30T04:36:58Z created
- 2026-10-30T04:37:12Z focused
- 2026-10-30T04:44:36Z scope: fmcli.py (check action), fmgenesis.py (checker), test_genesis.py are the feature itself; review fixes: empty-field regex, distinct tries, no-rows problem, punctuated F paths, not-yet more line, empty count in status, export skips the double check
- 2026-10-30T04:48:35Z done
- 2026-10-30T04:48:36Z committed 7f3fc3f3 (5 files)
- 2026-10-30T04:50:40Z guard authorization added: publish
- 2026-10-30T04:52:54Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-30: [cites: user steer 2026-10-29: COVERAGE BY GRID, NOT BY LUCK] Genesis standing rule: coverage by grid — coverage.md (fm genesis put): rows = the 13 …
- T-2077 [RESEARCH L, planned, 8 steps] Genesis gen 1: Missions 2-8, critiques, lineage, sweep, gen-2 Seed
- research mission-20261029-233102: Request: Genesis Mission 2 (#13 Genesis as a feature): fm genesis runs the whole tower by itself in any project — writes its own gen-0 …
- T-2078 [FEATURE M, done, 3 steps] fm genesis: the tower's home: init saves gen-0 verbatim and read-only, put files tower docs under research/genesis, status shows the to…
- the similar finished task took 3 steps
## Lessons
- A regex field parser with \s* after the colon reads across lines: use [ \t]* for line-scoped fields
## Plan gaps
- failed first: step 1 red tests for coverage and not-yet checks
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
