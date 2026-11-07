---
id: T-3376
type: FIX
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/kalevala.py, plugin/tests/test_genesis.py, plugin/tests/test_kalevala.py, site/genesis/genesis.js]
depends_on: []
source: discovered
created: 2026-11-06T06:21:37Z
updated: 2026-11-06T16:29:48Z
base: fa1d2afd7007ccd837a2dd4a1f0efb98b9aa8b51
base_tree: 6d8795c37f5b444945ab89b1e3c129955c9fe2c7
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-06T08:58:27Z
plan0_scope: []
builder_returned: 2026-11-06T09:30:32Z
lane_stop: merged 2026-11-06T14:55:36Z
verified: strong
lane_verified: 4a2f5f0747348634c69768ac6a3d45f465bd5e5e
---
# Kalevala watch(): one unreadable tower file blanks the whole Kalevala block instead of…
## Raw request
> FIX: kalevala watch(): one unreadable tower file blanks the whole Kalevala block instead of only that tower's row (T-3266); and the Rune dialog's close handler drops the URL query string
## Interpretation
Reading 1: kalevala.watch() catches per tower and returns an unreadable row; genesis.js dialog close keeps location.search. Reading 2 ruled out: live.js has no Rune dialog (its replaceState already keeps search).
## Assumptions (confidence)
## Acceptance criteria
- [x] watch() keeps good towers when one tower's file is corrupt — verify with `python3 plugin/tests/run.py test_kalevala`
- [x] genesis dialog close keeps location.search — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
1) try/except per tower in watch(), rounds skip error rows; likely outcome: one row shows unreadable, fails if a caller reads missing keys. 2) use what exists: the row dict shape and _tower_state; guard in rune helpers instead, fails if other callers hide errors. 3) catch in the CLI printer only; fails since rounds also call watch(). Choice 1 (80%): one guard where all callers route; JS replaceState to pathname+search plus a static test.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests then fixes for both
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_kalevala test_genesis -k corrupt_tower -k query_string` → exit 0 · Ran 2 tests in 81.6s (2 jobs, 16 at a time; slowest: KalevalaWatch 2s, GenesisExport 0s) / OK [ran] [tree c3feedb66f38] [world 2f1906870a] (2026-11-06T09:07:51Z)
- `sampo check --affected (affected tests only): plugin/lib/sampo/louhi.py plugin/tests/test_exam.py && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 126 · bash: line 1: plugin/lib/sampo/louhi.py: Permission denied [ran] [tree c3feedb66f38] [world 2f1906870a] (2026-11-06T09:08:08Z)
- (step 1) `python3 plugin/tests/run.py test_kalevala -k unreadable_tower -k corrupt_tower` → exit 0 · Ran 2 tests in 4.2s (1 jobs, 16 at a time; slowest: KalevalaWatch 0s) / OK [ran] [tree 5730c7b032bb] [world 2f1906870a] (2026-11-06T09:21:26Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_design_gates test_design_lint test_design_sprint test_docs test_doctor test_fmpy test_genesis test_goal test_kalevala test_left_out test_map test_models test_moons_scale test_moonshot test_motion_verify test_rename_scan test_replay test_sampo_design test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 1152 tests in 295.0s (235 jobs, 16 at a time; slowest: Ship 24s, CardsPage 14s, ProofBeforePresentation 12s) / FAILED (2 classes: test_docs.PluginFiles, test_docs.MapShards) [ran] [tree 5730c7b032bb] [world 2f1906870a] (2026-11-06T09:26:25Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree cee4e180c1d9] (2026-11-06T14:55:39Z)
- `python3 plugin/tests/run.py test_genesis test_kalevala` → ✗ exit 1 · Ran 297 tests in 116.4s (34 jobs, 16 at a time; slowest: ProofBeforePresentation 15s, GenerationReview 15s, KalevalaStep 10s) / FAILED (2 classes: test_kalevala.KalevalaWatch, test_genesis.GenesisExpo (start tree + this task's tests) [ran] [tree cee4e180c1d9] [world 2f1906870a] (2026-11-06T14:59:05Z)
- `python3 plugin/tests/run.py test_genesis test_kalevala` → exit 0 · Ran 297 tests in 84.2s (34 jobs, 16 at a time; slowest: ProofBeforePresentation 14s, GenerationReview 10s, GenesisCheck 10s) / OK [ran] [tree cee4e180c1d9] [world 2f1906870a] (2026-11-06T14:59:05Z)
- (ac 1) `python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 72 tests in 73.0s (9 jobs, 16 at a time; slowest: KalevalaStep 14s, Kalevala 6s, KalevalaCapabilities 3s) / OK [ran] [tree cee4e180c1d9] [world 2f1906870a] (2026-11-06T15:02:23Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 225 tests in 118.9s (25 jobs, 16 at a time; slowest: ProofBeforePresentation 15s, GenerationReview 13s, GenesisSweep 10s) / OK [ran] [tree cee4e180c1d9] [world 2f1906870a] (2026-11-06T15:02:23Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree cee4e180c1d9] (2026-11-06T15:02:23Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree cee4e180c1d9] (2026-11-06T15:02:23Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree cee4e180c1d9] (2026-11-06T15:02:23Z)
## Log
- 2026-11-06T06:21:37Z created
- 2026-11-06T08:58:14Z planned: it has criteria and steps
- 2026-11-06T08:58:26Z focused
- 2026-11-06T08:58:27Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-06T10:44:38Z criterion 1 verify: `python3 plugin/tests/run.py plugin/tests/test_kalevala.py` → `python3 plugin/tests/run.py test_kalevala`
- 2026-11-06T10:44:38Z criterion 1 verify: run.py takes test names, not paths (a path refused T-3375's merge); moved to the name form
- 2026-11-06T10:44:39Z criterion 2 verify: `python3 plugin/tests/run.py plugin/tests/test_genesis.py` → `python3 plugin/tests/run.py test_genesis`
- 2026-11-06T10:44:39Z criterion 2 verify: run.py takes test names, not paths (a path refused T-3375's merge); moved to the name form
- 2026-11-06T14:55:36Z merged worktree-agent-a7f1efe0d728b7852 (4 file(s))
- 2026-11-06T14:55:37Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a7f1efe0d728b7852
- 2026-11-06T14:55:37Z focused
- 2026-11-06T14:55:39Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/kalevala.py', 'plugin/tests/test_genesis.py', 'plugin/tests/test_kalevala.py', 'site/genesis/genesis.js']
- 2026-11-06T14:55:39Z scope: widened at merge to the reviewed lane's own diff (4a2f5f074), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T15:03:26Z done
- 2026-11-06T15:03:30Z committed 1259d8351 (1 file)
- 2026-11-06T16:29:48Z verified: the full suite is green on 1078ed22d, which contains 4a2f5f074
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3266 [FEATURE M, active, 3 steps] Remake the Rune page (site/genesis) in the Sampo look with Kalevala: every tower, the meta-generations and Väinämöinen's acts
- T-3050 [FEATURE L, blocked, 6 steps] Kalevala: many Rune towers at once on every aspect of Sampo, overseen by Väinämöinen, and evolving its own setup
- T-2756 [FIX S, done, 1 steps] fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row… — lesson: Key a dedupe on the stable identifier (…
- decision 2026-11-05: Kalevala (T-3050): namespaced Rune towers per aspect run at once, Väinämöinen oversees against the user's intent, Kalevala's own generations evolve …
- the similar finished task took 1 steps
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Files touched
- plugin/tests/test_kalevala.py
- plugin/tests/test_genesis.py
- plugin/lib/sampo/kalevala.py
- site/genesis/genesis.js
- CHANGELOG.md
