---
id: T-2113
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T07:08:59Z
updated: 2026-10-30T07:36:25Z
base: 581a38202dd510ffadd9875f2b880d654abc71f2
base_tree: edbdab5e05e7e33bb44eafbf1cd57107491b5856
plan0_at: 2026-10-30T07:22:32Z
plan0_scope: []
verified: strong
---
# fm genesis charter seal + privilege diff (mission-genesis brief 8, tier 3): init seals…
## Raw request
> FEATURE: fm genesis charter seal + privilege diff (mission-genesis brief 8, tier 3): init seals gen-0 (sha256 file, 444, ledger event); drift fails on a changed or unsealed gen-0; sweep gets a privileges row that turns red on a grant kind the generation used that it didn't have before, unless the user granted it in the window
## Interpretation
Brief 8 of mission-genesis (gen-0 NEVER: never grant yourself anything or lower your own guard). Seal: init writes gen-0.sha256 (whole-file hash, 0444; stricter than hashing only the MUST/NEVER lines and simpler) and drift fails when gen-0 no longer matches, or has no seal. Privilege diff: sweep gets a privileges row listing grant kinds used (task_set --allow, fm ask grants, standing yes, spent grants) since the generation started; a kind no earlier generation used and the user didn't grant in this window is red.
## Assumptions (confidence)
## Acceptance criteria
- [x] init seals gen-0; drift is drifted on a changed or unsealed gen-0 and clean after a restore or a same-bytes reseal; a sealed gen-0 refuses init — verify with `python3 plugin/tests/run.py test_genesis`
- [x] sweep's privileges row is red on a grant kind no earlier generation used, clean once the user grants it — verify with `python3 plugin/tests/run.py test_genesis`
- [x] export carries seal; site, MASTER, README, CHANGELOG, skill say it; the live tower is sealed — verify with `python3 plugin/tests/run.py test_docs test_genesis`
## Non-goals
## Approach (options → choice → why)
Chosen: a sha256 file beside gen-0 plus a ledger scan in sweep (reuses ledger_tail, parse_ts, the sweep row helper). Rejected: hash inside meta.json (one more place to sync; a tower copied elsewhere loses it); a git-tracked gen-0 (the tower lives in ignored state); halting at each grant in the hook (the guard is protected core and already asks; the sweep is the generation boundary gen-0 §7 names). Captured: none.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests first: seal + privileges + export seal (red)
2. [x] fmgenesis: seal/sealed, drift, status, privileges row
3. [x] docs, site, export; seal the live tower
## Resume here
<!-- auto -->
- 2026-10-30T07:29:47Z step 1/3: tests first: seal + privileges + export seal (red)
- git: foreman/build; 7 uncommitted: CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmgenesis.py, plugin/skills/genesis/SKILL.md, plugin/tests/test_genesis.py, site/genesis/genesis.js
- touched since last checkpoint: CHANGELOG.md, README.md, plugin/skills/genesis/SKILL.md, site/genesis/genesis.js, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2109t.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2109a.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2113r.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, MASTER.md
- failures met: syntaxerror: unterminated triple-quoted string literal (detected at line 0)
## Docs impact
MASTER.md, CHANGELOG.md, README.md, plugin/skills/genesis/SKILL.md, site/genesis/genesis.js
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 64 tests in 3.9s (11 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 3s, GenesisCheck 3s) / FAILED (3 classes) [ran] [tree 66f82080e429] (2026-10-30T07:22:48Z)
- (step 2) `python3 plugin/tests/run.py test_genesis.GenesisDrift test_genesis.GenesisSweep` → exit 0 · Ran 10 tests in 3.5s (2 classes, 16 at a time; slowest: GenesisSweep 3s, GenesisDrift 1s) / OK [ran] [tree 159e554770a9] (2026-10-30T07:23:01Z)
- (step 3) `python3 plugin/tests/run.py test_genesis test_docs` → exit 0 · Ran 144 tests in 8.5s (32 classes, 16 at a time; slowest: Fences 8s, GenesisLive 4s, GenesisSweep 4s) / OK [ran] [tree 7dc98ccad793] (2026-10-30T07:24:40Z)
- (step 3) `python3 plugin/tests/run.py test_genesis test_docs` → exit 0 · Ran 145 tests in 8.4s (32 classes, 16 at a time; slowest: Fences 8s, GenesisLive 4s, GenesisSweep 4s) / OK [ran] [tree 5e26ab64d91e] (2026-10-30T07:29:55Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 65 tests in 3.9s (11 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 5e26ab64d91e] (2026-10-30T07:33:58Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 65 tests in 3.9s (11 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 5e26ab64d91e] (2026-10-30T07:33:58Z)
- (ac 3) `python3 plugin/tests/run.py test_docs test_genesis` → exit 0 · Ran 145 tests in 8.4s (32 classes, 16 at a time; slowest: Fences 8s, GenesisLive 4s, GenesisSweep 4s) / OK [ran] [tree 5e26ab64d91e] (2026-10-30T07:33:58Z)
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 65 tests in 3.9s (11 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 5e26ab64d91e] (2026-10-30T07:33:58Z)
- (audit intent) `one fm-reviewer pass over the diff (intent, adversary, edge, operator, maintainer); findings verified, fixed test-first; full gates EXIT 0 (4365+ tests)` → grants weren't meant to count as uses → fixed, grant events now only exempt a kind [tree 5e26ab64d91e] (2026-10-30T07:33:58Z)
- (audit adversary) `one fm-reviewer pass over the diff (intent, adversary, edge, operator, maintainer); findings verified, fixed test-first; full gates EXIT 0 (4365+ tests)` → delete or forge gen-0.sha256 beside an edit to reseal → fixed, seal() reads the hex genesis_init logged first; forged-pair test [tree 5e26ab64d91e] (2026-10-30T07:33:58Z)
- (audit edge) `one fm-reviewer pass over the diff (intent, adversary, edge, operator, maintainer); findings verified, fixed test-first; full gates EXIT 0 (4365+ tests)` → a kind used in an archived ledger month looked new → fixed via c.ledger_events; LOW left: for n>1 the window start is sweep.md's mtime, so a sweep rerun moves it [tree 5e26ab64d91e] (2026-10-30T07:33:58Z)
- (audit operator) `one fm-reviewer pass over the diff (intent, adversary, edge, operator, maintainer); findings verified, fixed test-first; full gates EXIT 0 (4365+ tests)` → drift/status/export name the seal problem and its fix command; LOW left: a garbage seal file gets no recovery hint (ledger seal wins anyway) [tree 5e26ab64d91e] (2026-10-30T07:33:58Z)
- (audit maintainer) `one fm-reviewer pass over the diff (intent, adversary, edge, operator, maintainer); findings verified, fixed test-first; full gates EXIT 0 (4365+ tests)` → hashlib import hoisted, archive case tested; noticed: step/check don't read sealed() (drift does, and step waits on drift) [tree 5e26ab64d91e] (2026-10-30T07:33:58Z)
## Log
- 2026-10-30T07:08:59Z created
- 2026-10-30T07:22:31Z planned: it has criteria and steps
- 2026-10-30T07:22:32Z focused
- 2026-10-30T07:34:04Z done
- 2026-10-30T07:34:06Z committed e08d2d73 (7 files)
- 2026-10-30T07:34:11Z guard authorization added: publish
- 2026-10-30T07:36:25Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- T-2099 [FEATURE M, done, 5 steps] fm genesis draft/spec — gen-0 from a line or nothing; per-project spec with a held-out… — lesson: cover() tag words counted as shared w…
- decision 2026-10-30: [outward] [cites: gen-0 MUST line 11] T-2076's push and any later push of Genesis work wait for a publish grant: they go in the final report
- similar finished tasks took 4–5 steps
## Lessons
- A seal file beside the file it seals proves nothing: anchor the hash where an edit can't reach (the append-only ledger), and test the forged pair, not just the edit
## Plan gaps
- failed first: step 1 tests first: seal + privileges + export seal (red)
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
- README.md
- plugin/skills/genesis/SKILL.md
- site/genesis/genesis.js
