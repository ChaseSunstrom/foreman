---
id: T-2095
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T04:46:49Z
updated: 2026-10-30T05:10:48Z
base: 7f3fc3f345b859a9f7135fd1b700c4e9439db3d7
base_tree: b33f8a3d2bf52216978bb48315468ba15ffd7d99
plan0_at: 2026-10-30T04:51:21Z
plan0_scope: []
verified: ok
---
# fm genesis step: the tower's next action from its files, resumable after any kill
## Raw request
> fm genesis step: the tower's next action from its files, resumable after any kill
## Interpretation
A read-only fmgenesis.step(p) derives the tower's one next action from the tower files alone (gen-0, seeds, missions with Task: ids and intake blocks, critiques, lineage, drift, sweep, report). fm genesis step [--json] prints it with its command; fm next's idle path names it while a tower is open. A kill anywhere resumes to the same action because nothing but the files is read.
## Assumptions (confidence)
## Acceptance criteria
- [x] step names the next action per stage from the files alone; a kill after every stage resumes to the same action; caps (8 rows, 4 levels) and the lock hold; fm next names it while a tower is open — verify with `plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
Options: A tower files are the state (chosen, mission design A); B a JSON journal (second record that can drift); C a headless driver (built on A later); D a fm loop mode (open-ended, no done test). A wins: resumable for free and readable by a fresh session. Ponytail cuts: no lock (step is read-only; put already locks), no budget line, no separate stalled-tower note (fm next surfaces it each turn). Caps: >8 seed rows is fatal; the 4-level cap is SHAPE. SHAPE gains gen-N/drift.md and gen-N/sweep.md.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: per-stage next action, kill-and-resume, caps, corrupt file, lock
2. [x] fmgenesis.step + fm genesis step [--json]
3. [x] fm next idle path + stalled-tower note; docs MASTER/CHANGELOG, site status line
## Resume here
<!-- auto -->
- 2026-10-30T05:00:57Z steps 3/3 done
- git: foreman/build; 7 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, site/genesis/genesis.js
- touched since last checkpoint: plugin/lib/fmcli.py, site/genesis/genesis.js, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e3.txt, CHANGELOG.md, MASTER.md, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e4.txt, plugin/lib/fmcore.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py
- failures met: couldn't fetch workflows for foreman: http 0: api rate limit exceeded for 0.0.0.0. (but h…
## Docs impact
MASTER.md fmgenesis entry (step), CHANGELOG Unreleased line, site Genesis page shows next
## Verification evidence
- (step 1) `GenesisStep tests appended before the code (6 tests: every stage in order, blocked brief, two dry generations then report, every 3rd gen fm evolve, caps and unknown task, CLI/status/export/fm next)` → red: fmgenesis has no attribute step [tree 7800fbfa4992] (2026-10-30T04:57:09Z)
- (step 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis` → exit 0 · Ran 28 tests in 2.7s (5 classes, 16 at a time; slowest: GenesisLive 3s, GenesisCheck 2s, GenesisStep 1s) / OK [ran] [tree 7800fbfa4992] (2026-10-30T04:57:12Z)
- (step 3) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis test_site` → exit 0 · Ran 53 tests in 3.0s (14 classes, 16 at a time; slowest: GenesisLive 3s, Header 3s, GenesisCheck 2s) / OK [ran] [tree 5d2c437c9dac] (2026-10-30T04:57:45Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmgenesis.py — commit it through a task, or git checkout it back / fm doct; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                27.1    28.7     150  [0] / SessionEnd                  23.9    25.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 5d2c437c9dac] (2026-10-30T05:01:12Z)
- (audit intent) `fm-reviewer pass over the diff against the 4 criteria` → met after fixes: kill window across fm intake now names the made briefs (test_a_kill_after_fm_intake_names_its_briefs) [tree 6977abb5e0a7] (2026-10-30T05:03:22Z)
- (audit adversary) `fm-reviewer: malformed seed table, bogus Task ids, prose tag lines` → fatal on unparseable table and unknown ids; only the first fenced block counts [tree 6977abb5e0a7] (2026-10-30T05:03:22Z)
- (audit edge) `kill between intake and put; unreadable tower; load_briefs cost timed` → orphans named; fm next falls through on any step error; fm genesis step 82 ms total [tree 6977abb5e0a7] (2026-10-30T05:03:22Z)
- (audit operator) `fm genesis step output and exit code; fm next text` → one action + command; exit 1 only for fatal; CHANGELOG notes priority over the forever loop [tree 6977abb5e0a7] (2026-10-30T05:03:22Z)
- (audit maintainer) `fm-reviewer maintainer lens` → level comment fixed; BLOCK regex reuses c.parse_intake and fmcli._title, no new parser [tree 6977abb5e0a7] (2026-10-30T05:03:22Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmgenesis.py — commit it through a task, or git checkout it back / fm doct; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                27.5    31.2     150  [0] / SessionEnd                  24.1    26.0     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 6977abb5e0a7] (2026-10-30T05:06:33Z)
- (ac 1) `plugin/tests/run.py test_genesis` → ✗ exit 126 · bash: line 1: plugin/tests/run.py: Permission denied [ran] [tree 6977abb5e0a7] (2026-10-30T05:06:56Z)
- (ac 1) `plugin/tests/run.py test_genesis` → exit 0 · Ran 31 tests in 3.6s (5 classes, 16 at a time; slowest: GenesisLive 3s, GenesisCheck 2s, GenesisStep 2s) / OK [ran] [tree d086a4a15a07] (2026-10-30T05:07:29Z)
- (audit edge) `fm-reviewer five-lens pass; 4 confirmed findings fixed test-first (kill window across fm intake, unparseable seed table, fm next crash on step error, prose tag lines counted), 1 doc fix, 1 measured no-change; full gates green after the fixes` → a kill between fm intake and the Task: put names the briefs already made; an unreadable tower falls through in fm next; fm genesis step costs 82 ms with the archive loaded [tree d086a4a15a07] (2026-10-30T05:07:29Z)
- (audit intent) `re-checked after the last change (run.py made executable so criterion 1's command runs as written)` → met: all 4 criteria hold; test_genesis 31 OK run directly [tree d086a4a15a07] (2026-10-30T05:07:56Z)
- (audit adversary) `re-checked after the chmod` → no new surface: a mode change on the test runner only [tree d086a4a15a07] (2026-10-30T05:07:56Z)
- (audit edge) `re-checked after the chmod` → unchanged [tree d086a4a15a07] (2026-10-30T05:07:56Z)
- (audit operator) `re-checked after the chmod` → plugin/tests/run.py now runs as ./run.py too [tree d086a4a15a07] (2026-10-30T05:07:56Z)
- (audit maintainer) `re-checked after the chmod` → matches its shebang [tree d086a4a15a07] (2026-10-30T05:07:56Z)
- (audit edge) `fm-reviewer five-lens pass; 4 confirmed findings fixed test-first (kill window across fm intake, unparseable seed table, fm next crash on step error, prose tag lines counted), 1 doc fix, 1 measured no-change; full gates green after the fixes` → a kill between fm intake and the Task: put names the briefs already made; an unreadable tower falls through in fm next; fm genesis step costs 82 ms with the archive loaded [tree d086a4a15a07] (2026-10-30T05:08:03Z)
## Log
- 2026-10-30T04:46:49Z created
- 2026-10-30T04:51:20Z steer: lock criterion met by construction — step is read-only and put already locks; no budget line or stall note (ponytail)
- 2026-10-30T04:51:20Z focused
- 2026-10-30T05:08:25Z done
- 2026-10-30T05:08:26Z committed 62b95b2c (8 files)
- 2026-10-30T05:08:36Z guard authorization added: publish
- 2026-10-30T05:10:48Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2078 [FEATURE M, done, 3 steps] fm genesis: the tower's home: init saves gen-0 verbatim and read-only, put files tower docs under research/genesis, status shows the to…
- research T-2078-review: Verdict:** approve with nits. The three acceptance criteria are met, and `put` refuses gen-0 and every path outside the tower shape. I found one …
- research T-2093-review: Verdict: changes needed.** One MEDIUM defect lets the not-yet check pass an item that has an empty field. The other findings are LOW. I traced th…
- decision 2026-10-30: [cites: user: read SEED_PROMPT.md] Genesis setup: autonomy full, drive on, loop on, contract off, lane max 6, mandate until 2026-11-13; T-2077 is th…
## Lessons
- A resumable state machine over files has to check every write window between two commands, not only reruns over the same files: the gap between fm intake and fm genesis put was the one place a resume duplicated work.
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmgenesis.py
- site/genesis/genesis.js
- CHANGELOG.md
- MASTER.md
- plugin/tests/run.py
