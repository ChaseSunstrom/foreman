---
id: T-3573
type: PERFORMANCE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-07T02:24:28Z
updated: 2026-11-07T03:24:21Z
lane: ~/.claude/foreman.lanes/T-3573
lane_branch: foreman/T-3573
base: 746ca71b53870cb530fb6a5b61ddf2324ec5760c
base_tree: 624d8cb4b78f002d60e7ad2565e20ee8f6a18b24
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T02:43:10Z
plan0_scope: []
---
# A state index so reads stop re-parsing everything: sampo next reads ~2,345 brief files…
## Raw request
> PERFORMANCE: a state index so reads stop re-parsing everything: sampo next reads ~2,345 brief files and a 114k-line ledger per call (275 ms); keep one compact index (brief metadata, ledger offsets/aggregates) updated on write and read in O(changed) — benefits Python today and the Rust fast path later
## Interpretation
Reading 1 (chosen): make the existing reads cheap: every sampo next / state / ui call re-reads all ~2,370 briefs (500 open ones fully parsed) and re-scans the ~114k-line ledger (ledger_events walks every line since a task's creation; ledger_tail parses 5,000 lines); make them O(changed) with self-validating indexes, output unchanged. Reading 2 (ruled out): change callers to read less (narrower windows, fewer kinds): that changes what next/state/ui print, and the brief asks for identical behaviour.
## Assumptions (confidence)
## Acceptance criteria
- [ ] ledger_events through the kind index returns exactly the plain scan's events: fresh build, appended lines, a rewritten/rolled file, a corrupt or stale index, a partial last line — verify with `nice -n 10 python3 plugin/tests/run.py test_ledger_kinds test_ledger_index`
- [ ] load_briefs with open briefs indexed equals the full parse; a stale entry, a missing/corrupt index and a concurrent save are re-read, never served stale — verify with `nice -n 10 python3 plugin/tests/run.py -k brief_index test_core`
## Non-goals
## Approach (options → choice → why)
1) Per-ledger-file kind→line-offset index, built on read and extended only over appended bytes, validated by inode + indexed size + hash of the last indexed line, rebuilt when missing/corrupt/stale; likely outcome: ledger_events goes from a full-history line scan to a small JSON load plus the matching lines. 2) Maintain the index inside log_event; fails if: every hook append pays a ~1 MB index rewrite under the ledger flock. 3) A sqlite mirror of ledger and briefs; fails if: a new failure mode and migration (T-2022 already refused heavier stores). 4) Do less: only a C-level byte prefilter over the whole ledger (no state); likely outcome: 2-3x, still O(history). Briefs: extend the T-2022 index to open briefs as stubs in a small second file (briefs-open.json), so a save never rewrites the big closed index. Choice 1 + open-brief stubs (80%): no writer cost, self-healing, never trusted when it doesn't validate.
## Risks and rollback
First read after deploy builds the ledger indexes (~1-3 s once per process that gets there first; monthly again after fm tidy's roll). A stub's body is read when first needed, so meta (index time) and body (read time) can differ by a concurrent save: the same window T-2022's closed stubs had; writers re-read under the lock. Ledger since-windows assume time-ordered stamps (log_event stamps under the flock), as _seek_since already did. Rollback: git revert; deleting briefs-open.json, briefs-closed.json or cache/index-*.json is always safe.
## Execution prompt
## Steps
1. [ ] failing tests: ledger index parity + rebuild/stale/partial line; open-brief index parity + stale/concurrent save  <- CURRENT
2. [x] ledger kind index in core (ledger_events reads only candidate lines)
3. [x] open briefs indexed as stubs (briefs-open.json), memo of the parsed index; cmd_next/ui ledger_tail kind prefilter if the profile still shows it
4. [x] bench before/after on a copy of the real state (next, state --json, ui --json)
## Resume here
## Docs impact
docs/map/files-1.md and MASTER.md: one row/bullet for the read caches (briefs-index.json, briefs-open.json, briefs-closed.json's widened meaning, cache/index-<ledger file>.json): what they hold, how they are checked, that deleting any is safe.
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_ledger_kinds` → ✗ exit 1 · Ran 6 tests in 4.0s (1 jobs, 16 at a time; slowest: LedgerIndex 1s) / FAILED (1 classes: test_ledger_kinds.LedgerIndex) [ran] [tree ecc60e600f78] [world 2f1906870a] (2026-11-07T02:46:57Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py -k brief_index test_core` → ✗ exit 1 · Ran 11 tests in 13.5s (1 jobs, 16 at a time; slowest: BriefIndex 4s) / FAILED (1 classes: test_core.BriefIndex) [ran] [tree d57087718fc5] [world 2f1906870a] (2026-11-07T02:53:51Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_ledger_kinds test_ledger_index` → exit 0 · Ran 14 tests in 23.4s (2 jobs, 16 at a time; slowest: Memo 2s, LedgerIndex 1s) / OK [ran] [tree f15affbd287a] [world 2f1906870a] (2026-11-07T03:13:04Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py -k brief_index test_core` → exit 0 · Ran 11 tests in 44.4s (11 jobs, 16 at a time; slowest: BriefIndex.test_brief_index_a_stub_copies_edits_and_renders_like_a_parsed_brief 1s, BriefIndex.test_brief_index_concurrent_saves_and_loads_end_li [ran] [tree f15affbd287a] [world 2f1906870a] (2026-11-07T03:13:49Z)
- (step 4) `bash /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/t3573/final.sh 5` → exit 0 · lane PreToolUse        median    85 ms cpu  first    85  [86, 83, 85, 88, 85] / lane PostToolUse       median   128 ms cpu  first   126  [128, 124, 126, 128, 133] [ran] [tree f15affbd287a] [world 2f1906870a] (2026-11-07T03:14:36Z)
- (step 4) `python3 /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/t3573/final2.py 7` → exit 0 · PreToolUse           62 →    58 ms cpu (-6%)   first 60 → 58 / PostToolUse          96 →    83 ms cpu (-14%)   first 96 → 78 [ran] [tree f15affbd287a] [world 2f1906870a] (2026-11-07T03:16:16Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_ledger_kinds test_core test_ledger_index` → exit 0 · Ran 171 tests in 5.6s (32 jobs, 16 at a time; slowest: ConfidenceRoutes 4s, BriefIndex 3s, Migrate 3s) / OK [ran] [tree db456a3c517e] [world 2f1906870a] (2026-11-07T03:24:14Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py -k brief_index test_core` → exit 0 · Ran 12 tests in 3.5s (1 jobs, 16 at a time; slowest: BriefIndex 3s) / OK [ran] [tree db456a3c517e] [world 2f1906870a] (2026-11-07T03:24:21Z)
## Log
- 2026-11-07T02:24:28Z created
- 2026-11-07T02:42:50Z planned: it has criteria and steps
- 2026-11-07T02:42:55Z lane: ~/.claude/foreman.lanes/T-3573 on foreman/T-3573
- 2026-11-07T02:43:09Z focused
- 2026-11-07T02:43:10Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T03:09:09Z steer: skipped the per-process memo of the parsed brief index: after open-brief stubs a load is ~15 ms (2,371 stats + 1.6 MB of index JSON), and a memo would need a copy of every stub's meta (about what the parse costs); widened briefs-closed.json to every non-active brief so active_brief_fast (T-3577's area) skips open briefs without a text change there
- 2026-11-07T03:14:26Z criterion 1 verify: `nice -n 10 python3 plugin/tests/run.py test_ledger_index` → `nice -n 10 python3 plugin/tests/run.py test_ledger_kinds test_ledger_index`
- 2026-11-07T03:15:40Z scope: core.py (ledger index, brief index, ledger_tail kinds), cli.py/friction.py (callers moved to ledger_tail kinds), grants.py (queued reads the indexed snip), watch.py (TYPICAL kinds), docs/map/files-1.md + MASTER.md (the new state caches), tests
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- decision 2026-11-07: [costly] T-3571: speed Sampo up with a native Rust fast path for the per-call hot paths (hook dispatch, guard, statusline, ui, next) plus a state in…
## Measurements
CPU ms (user+sys, median of 7, main vs lane interleaved, each on its own fresh copy of the real project state: 2,371 briefs, 136k ledger lines): sampo next 277 → 154 (-44%), sampo state --json 211 → 184 (-13%), fm ui --json 567 → 442 (-22%), Stop hook 119 → 91 (-24%), UserPromptSubmit 287 → 184 (-36%), PreToolUse Bash 62 → 58 (-6%), PostToolUse Bash 96 → 83 (-14%). Same run from the agent shell (more env, heavier load): 402 → 229, 312 → 262, 832 → 642, 168 → 132, 461 → 275, 90 → 85, 143 → 124. Outputs of next/state/ui identical but for 1 s worktree ages. First call after deploy builds the indexes (~2-3 s once).
