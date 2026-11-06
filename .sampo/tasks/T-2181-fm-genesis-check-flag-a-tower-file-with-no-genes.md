---
id: T-2181
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T15:44:05Z
updated: 2026-10-31T05:16:23Z
group: genesis check gates on tower files
base: 7815a2897a97838e2e79ac9e748018bdbe037a7b
base_tree: 7ce78a4f72ff711ba59a53777e36bcd9c1f53dc4
plan0_at: 2026-10-31T04:45:52Z
plan0_scope: []
verified: strong
---
# fm genesis check: flag a tower file with no genesis_read pass newer than its last write…
## Raw request
> fm genesis check: flag a tower file with no genesis_read pass newer than its last write (hand-edited or pre-T-2166 files still count today) (T-2166 review, intent lens)
## Interpretation
Steer 2: every tower file gets a cold second read. fm genesis put only files a doc after its cold read passes, but nothing checks that the file still holds that text: a hand edit (or a file from before T-2166) passes fm genesis check unread.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis check flags a put-able tower file whose text was changed after its passing put, and a file with no pass on record; a file put through a passing read, or one with a ledger pass just before its mtime, is clean; OWNED files and gen-0.md are exempt — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
1) put records {name: sha256 of the bytes _file wrote} in a state JSON (p.dir, beside READS/ACCEPTED) after its read passes; fm genesis check gains a 'read' entry listing each put-able tower file (SHAPE, not OWNED, not gen-0.md) whose current bytes have no matching record: 'no cold-read pass for its current text: fm genesis put it again'. A file with no record yet counts as read when the ledger holds a genesis_read pass for its name (or a name#section pass for every section) at most 120 s before its mtime (the put writes right after the read), so today's passed files aren't all flagged. 2) mtime vs newest pass only — rejected: a copy or touch fakes it, and a hand edit within the window passes. 3) re-read everything — rejected: cost, and long files don't converge (T-2221). Choice 1.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: hand edit after put flagged; legacy file with ledger pass clean; legacy without flagged; OWNED exempt
2. [x] put records the hash; check's read entry; status/next shows it
3. [x] CHANGELOG, MASTER genesis check line, genesis SKILL.md
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md, plugin/skills/genesis/SKILL.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_genesis 2>&1 | tail -15` → ✗ exit 1 · Ran 147 tests in 18.6s (17 classes, 16 at a time; slowest: GenesisRead 16s, GenesisCheck 15s, GenesisDrift 13s) / FAILED (1 classes) [ran] [tree 3bb16071706d] (2026-10-31T04:47:10Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis 2>&1 | grep -v "^ File\|~~" | tail -40` → exit 0 · Ran 147 tests in 15.5s (17 classes, 16 at a time; slowest: GenesisRead 15s, GenesisCheck 14s, GenesisDrift 12s) / OK [ran] [tree 143023e1518d] (2026-10-31T04:47:39Z)
- (step 1) `python3 plugin/tests/run.py test_genesis 2>&1 | grep -v "^ File\|~~" | tail -40` → exit 0 · Ran 147 tests in 15.5s (17 classes, 16 at a time; slowest: GenesisRead 15s, GenesisCheck 14s, GenesisDrift 12s) / OK [ran] [tree 143023e1518d] (2026-10-31T04:47:39Z)
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 147 tests in 19.1s (17 classes, 16 at a time; slowest: GenesisRead 19s, GenesisCheck 18s, GenesisDrift 16s) / OK [ran] [tree 1461b99fc1a7] (2026-10-31T04:48:11Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_board_surfaces test_cli test_core test_cost test_design_surfaces test_design_tokens test_docs test_doctor test_edit_cards test_extras test_followups test_genesis test_guard test_guard_cases test_hooks test_ideation test_judgment test_lib_hostile test_lib_source_kill test_library test_nudges test_onwrite test_playbook_use test_plugin_parity test_plugins test_replan test_scene test_scout test_second test_shade test_showpieces test_site_gallery test_skillroute test_smoke_profiles test_speed test_steering test_supply_delta test_taste_ledger test_tidy test_ui test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [50.78s] [ran] [tree 1461b99fc1a7] (2026-10-31T04:51:31Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis 2>&1 | grep -v "^ File\|~~" | tail -20` → ✗ exit 1 · Ran 149 tests in 30.1s (17 classes, 16 at a time; slowest: GenesisRead 29s, GenesisCheck 26s, GenesisDrift 25s) / FAILED (2 classes) [ran] [tree 625501db4b54] (2026-10-31T04:55:36Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis 2>&1 | grep -v "^ File\|~~" | tail -20` → ✗ exit 1 · Ran 149 tests in 22.0s (17 classes, 16 at a time; slowest: GenesisRead 21s, GenesisCheck 19s, GenesisDrift 17s) / FAILED (1 classes) [ran] [tree 8b9c9faeff51] (2026-10-31T04:56:25Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis 2>&1 | grep -B3 -A6 "^FAIL"` → ✗ exit 1 · Ran 149 tests in 37.6s (17 classes, 16 at a time; slowest: GenesisRead 36s, GenesisCheck 34s, GenesisDrift 32s) / FAILED (1 classes) [ran] [tree 8b9c9faeff51] (2026-10-31T04:57:06Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis 2>&1 | tail -4` → exit 0 · Ran 149 tests in 28.6s (17 classes, 16 at a time; slowest: GenesisRead 28s, GenesisCheck 25s, GenesisDrift 22s) / OK [ran] [tree cf9c70ea2a7f] (2026-10-31T04:57:43Z)
- (step 2) `python3 plugin/tests/run.py test_genesis 2>&1 | tail -4` → exit 0 · Ran 149 tests in 28.6s (17 classes, 16 at a time; slowest: GenesisRead 28s, GenesisCheck 25s, GenesisDrift 22s) / OK [ran] [tree cf9c70ea2a7f] (2026-10-31T04:57:43Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_board_surfaces test_cli test_core test_cost test_design_surfaces test_design_tokens test_docs test_doctor test_edit_cards test_extras test_followups test_genesis test_guard test_guard_cases test_hooks test_ideation test_judgment test_lib_hostile test_lib_source_kill test_library test_nudges test_onwrite test_playbook_use test_plugin_parity test_plugins test_replan test_scene test_scout test_second test_shade test_showpieces test_site_gallery test_skillroute test_smoke_profiles test_speed test_steering test_supply_delta test_taste_ledger test_tidy test_ui test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [35.73s] [ran] [tree cf9c70ea2a7f] (2026-10-31T05:02:25Z)
- `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 149 tests in 9.0s (17 classes, 16 at a time; slowest: GenesisRead 8s, GenesisCheck 7s, GenesisDrift 6s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree 495d9409e57f] (2026-10-31T05:10:45Z)
- `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 149 tests in 11.6s (17 classes, 16 at a time; slowest: GenesisRead 11s, GenesisCheck 10s, GenesisDrift 9s) / OK [ran] [tree 495d9409e57f] (2026-10-31T05:10:45Z)
- `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 150 tests in 31.4s (17 classes, 16 at a time; slowest: GenesisRead 28s, GenesisCheck 23s, GenesisDrift 21s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree f4900c718e1e] (2026-10-31T05:13:01Z)
- `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 150 tests in 31.6s (17 classes, 16 at a time; slowest: GenesisRead 31s, GenesisCheck 29s, GenesisDrift 24s) / OK [ran] [tree f4900c718e1e] (2026-10-31T05:13:01Z)
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 150 tests in 28.0s (17 classes, 16 at a time; slowest: GenesisRead 27s, GenesisCheck 25s, GenesisDrift 21s) / OK [ran] [tree f4900c718e1e] (2026-10-31T05:13:30Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 150 tests in 20.3s (17 classes, 16 at a time; slowest: GenesisRead 20s, GenesisCheck 18s, GenesisDrift 17s) / OK [ran] [tree f4900c718e1e] (2026-10-31T05:13:50Z)
- (step 3) `grep -c T-2181 MASTER.md plugin/skills/genesis/SKILL.md` → exit 0 · MASTER.md:1 / plugin/skills/genesis/SKILL.md:0 [ran] [tree f4900c718e1e] (2026-10-31T05:13:50Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 150 tests in 21.2s (17 classes, 16 at a time; slowest: GenesisRead 21s, GenesisCheck 20s, GenesisDrift 18s) / OK [ran] [tree 92f713364e06] (2026-10-31T05:14:22Z)
- (audit intent) `self + one fm-reviewer pass (2 medium, 3 low, all fixed with tests); on the real tower the first version flagged 9 files because a whole-file pass didn't count for a file with sections; fixed test-first, now only gen-1/mission-genesis.md (only a failed read on record) is flagged` → steer 2 enforced on the files: a tower file's current bytes must be the ones a passing put filed, or a legacy pass sits just before its mtime (test_genesis red-to-green) [tree 92f713364e06] (2026-10-31T05:14:22Z)
- (audit adversary) `self + one fm-reviewer pass (2 medium, 3 low, all fixed with tests); on the real tower the first version flagged 9 files because a whole-file pass didn't count for a file with sections; fixed test-first, now only gen-1/mission-genesis.md (only a failed read on record) is flagged` → only put records a hash; _file without record never blesses text; grow/confirm keep a record only when the prior bytes were read; a section pass from a put that failed elsewhere doesn't clear a file; the record sits in guarded state [tree 92f713364e06] (2026-10-31T05:14:22Z)
- (audit edge) `self + one fm-reviewer pass (2 medium, 3 low, all fixed with tests); on the real tower the first version flagged 9 files because a whole-file pass didn't count for a file with sections; fixed test-first, now only gen-1/mission-genesis.md (only a failed read on record) is flagged` → whole-file legacy pass counts for a sectioned file; ledger scanned only when a record is missing; write and record under one lock [tree 92f713364e06] (2026-10-31T05:14:22Z)
## Log
- 2026-10-30T15:44:05Z created
- 2026-10-31T04:45:35Z set tier=M
- 2026-10-31T04:45:36Z planned: it has criteria and steps
- 2026-10-31T04:45:37Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2181.builder.md
- 2026-10-31T04:45:51Z focused
- 2026-10-31T05:10:23Z merged worktree-agent-a1d264c8787f09d9b (4 file(s))
- 2026-10-31T05:10:23Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a1d264c8787f09d9b
- 2026-10-31T05:10:23Z focused
- 2026-10-31T05:13:51Z scope: plugin/lib/fmgenesis.py (put, _file, read_check, check), plugin/tests/test_genesis.py, MASTER.md, plugin/skills/genesis/SKILL.md, CHANGELOG.md
- 2026-10-31T05:16:21Z done
- 2026-10-31T05:16:23Z committed 12f054f6 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2191 [FEATURE L, done, 4 steps] The user's standing intent (steer 2026-10-30 #7, STANDING INTENT): file it in the tower… — lesson: A rule that says 'a format check is …
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (second): standing rule] Every tower file (seed, mission, critique, coverage, not-yet, exam entry) gets a cold H…
## Lessons
- A legacy-evidence rule must be run against the real history before it lands: the rule written from the reviewer's case alone flagged nine files that had passed
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- MASTER.md
- plugin/skills/genesis/SKILL.md
- CHANGELOG.md
