---
id: T-2298
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T08:37:55Z
updated: 2026-10-31T09:26:00Z
builder_model: sonnet
base: 79fefc175edd1ebe21a46bebf487a93ab00b4b9a
base_tree: 3526fb3cf041ff2a48c0071e2553e1c6f3ad439e
plan0_at: 2026-10-31T08:54:51Z
plan0_scope: []
verified: strong
---
# fm doctor's usage burn and unloaded skills checks reuse their last result while their inputs are unchanged
## Raw request
> fm doctor: 'usage burn' takes ~15 s and 'unloaded skills' ~7 s of a 30 s+ run (T-2279's timing, builder's machine): cache or bound them so doctor stays fast
## Interpretation
Two advisory doctor checks rescan history on every run: usage burn reads two days of every project's transcripts (fmcost.burn_findings) and unloaded skills reads 30 days of global events; together ~22 s of a 30 s+ doctor (T-2279's timing). Reuse each result while the files it reads are unchanged, so a second doctor is fast and still exact.
## Assumptions (confidence)
## Acceptance criteria
- [x] With a stubbed slow burn_findings and global_events, a second check_usage_burn and check_unloaded_skills call with no input file changed returns the same Result without calling them; touching an input (a transcript or events.jsonl grows) recomputes — verify with `python3 plugin/tests/run.py test_doctor`
- [x] The cache is JSON under the state dir (never pickle), keyed on the inputs' paths, sizes and mtimes plus the day, and a corrupt or missing cache file just recomputes — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
Options: 1) cache each check's Result in JSON keyed on the (path, size, mtime) of the files it reads, plus the date so a window boundary refreshes; 2) make the scans themselves faster (seek to the window, index by day); 3) skip both unless fm doctor --full. Choice 1: exact (any new event or transcript line changes a key), small, and keeps the checks in every run; 2 is more code across fmcost; 3 hides the findings.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red tests: second call with unchanged inputs skips the scan; a grown input recomputes; a corrupt cache recomputes
2. [x] Add a small JSON result cache keyed on input stats for the two checks; leave their output unchanged
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_doctor 2>&1 | tail -15` → ✗ exit 1 · Ran 85 tests in 32.6s (30 classes, 16 at a time; slowest: ViewsRepair 26s, LockProbe 12s, Command 9s) / FAILED (1 classes) [ran] [tree 3269b56040dd] (2026-10-31T08:56:10Z)
- (ac 2) `python3 plugin/tests/run.py test_doctor 2>&1 | tail -15` → ✗ exit 1 · Ran 85 tests in 32.6s (30 classes, 16 at a time; slowest: ViewsRepair 26s, LockProbe 12s, Command 9s) / FAILED (1 classes) [ran] [tree 3269b56040dd] (2026-10-31T08:56:10Z)
- (step 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 85 tests in 27.8s (30 classes, 16 at a time; slowest: ViewsRepair 25s, LockProbe 13s, Timing 7s) / OK [ran] [tree d8bfa90c003a] (2026-10-31T08:57:34Z)
- (step 2) `python3 plugin/tests/run.py test_doctor test_usage_burn` → exit 0 · Ran 87 tests in 34.3s (30 classes, 16 at a time; slowest: ViewsRepair 32s, LockProbe 14s, Command 8s) / OK [ran] [tree d8bfa90c003a] (2026-10-31T08:58:09Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_crash_hygiene test_doctor test_supply_delta && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [68.80s] [ran] [tree d8bfa90c003a] (2026-10-31T09:00:11Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor 2>&1 | grep -E "^(FAIL|ERROR|OK|FAILED)"` → ✗ exit 1 · FAILED (failures=3, errors=1) / FAILED (1 classes) [ran] [tree 92bad6fd5e6f] (2026-10-31T09:14:24Z)
- (ac 2) `python3 plugin/tests/run.py test_doctor 2>&1 | grep -E "^(FAIL|ERROR|OK|FAILED)"` → ✗ exit 1 · FAILED (failures=3, errors=1) / FAILED (1 classes) [ran] [tree 92bad6fd5e6f] (2026-10-31T09:14:24Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_core test_crash_hygiene test_doctor test_supply_delta && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [20.87s] [ran] [tree f2ee6aaf919e] (2026-10-31T09:15:29Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor 2>&1 | grep -E "^(FAIL|ERROR|OK|FAILED)"` → ✗ exit 1 · FAILED (errors=1) / FAILED (1 classes) [ran] [tree 848949f890cd] (2026-10-31T09:15:55Z)
- (ac 2) `python3 plugin/tests/run.py test_doctor 2>&1 | grep -E "^(FAIL|ERROR|OK|FAILED)"` → ✗ exit 1 · FAILED (errors=1) / FAILED (1 classes) [ran] [tree 848949f890cd] (2026-10-31T09:15:55Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_core test_crash_hygiene test_doctor test_supply_delta && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [19.31s] [ran] [tree c6d77f3e18a5] (2026-10-31T09:16:38Z)
- (step 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 90 tests in 4.1s (30 classes, 16 at a time; slowest: ViewsRepair 4s, LockProbe 3s, Timing 2s) / OK [ran] [tree 15cd69cda118] (2026-10-31T09:24:05Z)
- (step 2) `python3 plugin/tests/run.py test_doctor test_core` → exit 0 · Ran 185 tests in 4.5s (52 classes, 16 at a time; slowest: ViewsRepair 4s, LockProbe 3s, BriefIndex 2s) / OK [ran] [tree 15cd69cda118] (2026-10-31T09:24:10Z)
- (step 2) `FOREMAN_DOCTOR_BENCH=0 fm doctor --json > /dev/null` → FOREMAN_DOCTOR_BENCH=0 fm doctor --json > /dev/null: 2.708s → 2.778s (3 runs each) [ran] [tree 15cd69cda118] (2026-10-31T09:24:38Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 90 tests in 4.2s (30 classes, 16 at a time; slowest: ViewsRepair 4s, LockProbe 3s, Timing 2s) / OK [ran] [tree 4005eb75fe99] (2026-10-31T09:25:34Z)
- (ac 2) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 90 tests in 4.2s (30 classes, 16 at a time; slowest: ViewsRepair 4s, LockProbe 3s, Timing 2s) / OK [ran] [tree 4005eb75fe99] (2026-10-31T09:25:34Z)
- (audit intent) `one fm-reviewer pass (intent, operator, adversary, edge, maintainer): HIGH (key held sizes and exact mtimes of files that grow every turn, so in-session repeats always missed), MEDIUM (raw forecast full_at in the key), MEDIUM (RecursionError on a deep-nested cache), LOWs (tampered cached text, dead hit flag); all fixed test-first, plus T-2300's shared event-file list and _load_json's RecursionError; I read the fixed diff` → a repeat doctor in the same session reuses the two history scans instead of redoing them [tree 4005eb75fe99] (2026-10-31T09:25:34Z)
- (audit adversary) `one fm-reviewer pass (intent, operator, adversary, edge, maintainer): HIGH (key held sizes and exact mtimes of files that grow every turn, so in-session repeats always missed), MEDIUM (raw forecast full_at in the key), MEDIUM (RecursionError on a deep-nested cache), LOWs (tampered cached text, dead hit flag); all fixed test-first, plus T-2300's shared event-file list and _load_json's RecursionError; I read the fixed diff` → JSON only, read capped at 64 KB, RecursionError caught, a hit takes only status in PASS/WARN/FAIL and a c.plain'd fitted detail [tree 4005eb75fe99] (2026-10-31T09:25:34Z)
- (audit edge) `one fm-reviewer pass (intent, operator, adversary, edge, maintainer): HIGH (key held sizes and exact mtimes of files that grow every turn, so in-session repeats always missed), MEDIUM (raw forecast full_at in the key), MEDIUM (RecursionError on a deep-nested cache), LOWs (tampered cached text, dead hit flag); all fixed test-first, plus T-2300's shared event-file list and _load_json's RecursionError; I read the fixed diff` → an append within the hour still hits (up to 1 h stale, accepted for 2- and 30-day aggregates); a new day or a moved hour recomputes; the forecast keys on the hours shown [tree 4005eb75fe99] (2026-10-31T09:25:34Z)
- (audit operator) `one fm-reviewer pass (intent, operator, adversary, edge, maintainer): HIGH (key held sizes and exact mtimes of files that grow every turn, so in-session repeats always missed), MEDIUM (raw forecast full_at in the key), MEDIUM (RecursionError on a deep-nested cache), LOWs (tampered cached text, dead hit flag); all fixed test-first, plus T-2300's shared event-file list and _load_json's RecursionError; I read the fixed diff` → one small JSON file in the state dir; two concurrent doctors can overwrite each other's entry, costing only a recompute [tree 4005eb75fe99] (2026-10-31T09:25:34Z)
- (audit maintainer) `one fm-reviewer pass (intent, operator, adversary, edge, maintainer): HIGH (key held sizes and exact mtimes of files that grow every turn, so in-session repeats always missed), MEDIUM (raw forecast full_at in the key), MEDIUM (RecursionError on a deep-nested cache), LOWs (tampered cached text, dead hit flag); all fixed test-first, plus T-2300's shared event-file list and _load_json's RecursionError; I read the fixed diff` → global_event_files is the one list global_events and the key share (T-2300) [tree 4005eb75fe99] (2026-10-31T09:25:34Z)
## Log
- 2026-10-31T08:37:55Z created
- 2026-10-31T08:38:55Z planned from capture
- 2026-10-31T08:54:34Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2298.builder.md
- 2026-10-31T08:54:49Z focused
- 2026-10-31T09:24:00Z merged worktree-agent-ad20c9874cc00fdbc (3 file(s))
- 2026-10-31T09:24:00Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad20c9874cc00fdbc
- 2026-10-31T09:24:00Z focused
- 2026-10-31T09:25:29Z scope: plugin/lib/fmdoctor.py, plugin/lib/fmcore.py (global_event_files, T-2300 folded in), plugin/tests/test_doctor.py, MASTER.md, CHANGELOG.md
- 2026-10-31T09:25:58Z done
- 2026-10-31T09:26:00Z committed b6557ebb (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1800 [PERFORMANCE M, done, 3 steps] Foreman reasons ahead: names why usage burns, unasked (session start, fm doctor, fm digest) — lesson: Account-wide scans hung on a …
- T-1797 [FEATURE M, done, 3 steps] CC 2.1.305-2.1.312 adoption: give fm-reviewer/fm-recon an autoCompactWindow; fm doctor poi — lesson: Subagent transcripts carry their p…
- T-1810 [FEATURE M, done, 4 steps] Session start sweeps for problems nobody raised: CI on main, a changed model/window/CC (cost math redone), a stale blocked pile, overdu…
- decision 2026-10-30: Cold reads converge by per-line acceptance (keyed on line text + charter hash), not by majority reads or diff-only reads: every line still gets a wh…
## Measurements
repeat doctor, the two checks: warm cache hits measured here 11 ms (usage burn) + 1 ms (unloaded skills); cold not measured here (a valid before-run was denied; fm task evidence --bench ran fm from PATH, the current code, on both sides: 2.71 s -> 2.78 s whole doctor, so it isn't a before/after); the builder's cold timing under load ~100 was 15.6 s + 7 s
## Lessons
- A bench whose command resolves through PATH times the current code on both sides: a before/after needs the start tree's own entry point, or it measures nothing
## Files touched
- plugin/tests/test_doctor.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmcore.py
- MASTER.md
- CHANGELOG.md
