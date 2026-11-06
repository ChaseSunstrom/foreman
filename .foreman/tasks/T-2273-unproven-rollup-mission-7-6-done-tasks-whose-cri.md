---
id: T-2273
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T04:52:51Z
updated: 2026-10-31T06:02:44Z
base: e39b5cf97211c9aaa8b5f1120e3f888b2ba85f8e
base_tree: 38405beaf14bdb8a3c06d0ed5e603749baa9f8cb
plan0_at: 2026-10-31T05:47:02Z
plan0_scope: []
verified: strong
---
# Unproven rollup (Mission 7, #6): done tasks whose criteria rest on typed or inconclusive evidence, or UI changes with no visual check, counted and listed on every surface
## Raw request
> Unproven rollup (Mission 7, #6): done tasks whose criteria rest on typed or inconclusive evidence, or UI changes with no visual check, counted and listed on every surface
## Interpretation
Gap map #6: proof exists per task (evidence --run, typed evidence when a check can't run here, --inconclusive, UI shots), but nothing rolls up what was closed without a run, so 'done' reads the same whether a criterion ran green or was typed by hand. gen-0 asks for verifying anything, labelled.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm proof [--days N] [--json] lists each done task in the window with a claim not proven by a run here: a criterion whose evidence was typed (not run), an inconclusive one, a UI file change with no shot/smoke/stories evidence; fm status, fm digest and the genesis §8 report each show the count with 'fm proof'; a task whose every criterion ran green is never listed — verify with `python3 plugin/tests/run.py test_proof test_status`
## Non-goals
## Approach (options → choice → why)
1) c.unproven(p, days=30): for done briefs closed in the window, read each criterion's evidence lines (the run mark vs typed, the inconclusive mark) and the task's touched files (a UI extension: css/html/tsx/jsx/svelte/vue) against evidence naming fm shot/smoke/stories/flow; fm proof prints them grouped by kind, --json for the pane/MCP; one 'unproven: N (fm proof)' line in fm status, fm digest and fmgenesis' report. 2) block closes with typed evidence — rejected: typed evidence is legitimate when a check can't run here; the label is the point. 3) per-domain proof kinds (data/infra/perf) first — later: the rollup is the frame they plug into. Choice 1.
## Risks and rollback
Old tasks with evidence from before the run mark existed would all read unproven: the window (30 days) and the mark's date bound it; noted in the output.
## Execution prompt
## Steps
1. [x] red tests: typed, inconclusive and UI-without-shot each listed; all-run task not listed; the count on status and digest
2. [x] c.unproven(p, days) from briefs' evidence marks and touched files; fm proof verb; status/digest/report lines
3. [x] docs: MASTER, README verification section, CHANGELOG
## Resume here
## Docs impact
MASTER.md, README.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_proof` → exit 0 · Ran 6 tests in 4.5s (3 classes, 16 at a time; slowest: Proof 4s, Palette 0s, FindRankValue 0s) / OK [ran] [tree fb20f3c360e9] (2026-10-31T05:49:46Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_core test_cost test_cost_forecast test_docs test_economics test_exam test_export test_guard_cases test_paused test_proof test_round_g test_statusline_ui && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [12.92s] [ran] [tree fb20f3c360e9] (2026-10-31T05:52:22Z)
- (step 2) `python3 plugin/tests/run.py test_proof 2>&1 | tail -8` → exit 0 · Ran 7 tests in 14.4s (3 classes, 16 at a time; slowest: Proof 14s, Palette 0s, FindRankValue 0s) / OK [ran] [tree 253f1eb02f86] (2026-10-31T05:54:17Z)
- (step 3) `python3 plugin/tests/run.py test_proof test_cli test_genesis test_docs 2>&1 | tail -6` → exit 0 · Ran 378 tests in 29.4s (79 classes, 16 at a time; slowest: TaskLifecycle 29s, GenesisRead 17s, CaptureAndIntake 15s) / OK [ran] [tree 577663676b88] (2026-10-31T05:55:02Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_core test_cost test_cost_forecast test_docs test_economics test_exam test_export test_genesis test_guard_cases test_paused test_proof test_reasoning test_round_g test_statusline_ui && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 3 fail / Ran 154 tests across 4 files. [94.37s] [ran] [tree ca0a3713c837] (2026-10-31T05:58:32Z)
- `python3 plugin/tests/run.py test_proof` → ✗ exit 1 · Ran 7 tests in 5.6s (3 classes, 16 at a time; slowest: Proof 4s, Palette 0s, FindRankValue 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree cfc311a1e3cd] (2026-10-31T06:00:03Z)
- `python3 plugin/tests/run.py test_proof` → exit 0 · Ran 7 tests in 5.4s (3 classes, 16 at a time; slowest: Proof 5s, Palette 0s, FindRankValue 0s) / OK [ran] [tree cfc311a1e3cd] (2026-10-31T06:00:03Z)
- (step 1) `python3 plugin/tests/run.py test_proof test_cli test_genesis test_docs` → exit 0 · Ran 379 tests in 23.3s (79 classes, 16 at a time; slowest: TaskLifecycle 23s, GenesisRead 12s, CaptureAndIntake 10s) / OK [ran] [tree cfc311a1e3cd] (2026-10-31T06:00:27Z)
- (step 2) `python3 plugin/tests/run.py test_proof test_cli test_genesis test_docs` → exit 0 · Ran 379 tests in 30.3s (79 classes, 16 at a time; slowest: TaskLifecycle 30s, GenesisRead 19s, CaptureAndIntake 15s) / OK [ran] [tree cfc311a1e3cd] (2026-10-31T06:00:57Z)
- (step 3) `grep -c T-2273 MASTER.md README.md` → exit 0 · MASTER.md:1 / README.md:1 [ran] [tree cfc311a1e3cd] (2026-10-31T06:00:57Z)
- (ac 1) `python3 plugin/tests/run.py test_proof test_status` → exit 0 · Ran 24 tests in 5.1s (12 classes, 16 at a time; slowest: Proof 5s, StatuslineUi 1s, Genesis 1s) / OK [ran] [tree e378dcf59981] (2026-10-31T06:01:16Z)
- (audit intent) `self + measured on the real project: the first version added 1.6 s to fm status; sent back, now a cache keyed on the task folders' stats: warm fm status ~110 ms (was ~250 ms before the change)` → a claim closed without a run here is labelled and counted on status, digest, genesis status/export and the scorecard; the real project shows 347 such tasks in 30 days (test_proof red-to-green) [tree e378dcf59981] (2026-10-31T06:01:16Z)
- (audit edge) `self + measured on the real project: the first version added 1.6 s to fm status; sent back, now a cache keyed on the task folders' stats: warm fm status ~110 ms (was ~250 ms before the change)` → a later green run clears a typed or red line; a typed line naming fm shot doesn't count as a UI check; the ledger isn't in the cache key, so a post-close edit shows at the next brief change (noted) [tree e378dcf59981] (2026-10-31T06:01:16Z)
- (audit operator) `self + measured on the real project: the first version added 1.6 s to fm status; sent back, now a cache keyed on the task folders' stats: warm fm status ~110 ms (was ~250 ms before the change)` → fm status stays fast; fm proof and fm digest always recompute [tree e378dcf59981] (2026-10-31T06:01:16Z)
## Log
- 2026-10-31T04:52:51Z created
- 2026-10-31T05:46:34Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2273.builder.md
- 2026-10-31T05:47:01Z focused
- 2026-10-31T05:59:43Z merged worktree-agent-a6e17a5304afcaa15 (8 file(s))
- 2026-10-31T05:59:44Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a6e17a5304afcaa15
- 2026-10-31T05:59:44Z focused
- 2026-10-31T06:01:10Z scope: plugin/lib/fmcore.py (unproven, unproven_cached, all_touches), plugin/lib/fmcli.py (cmd_proof, status line), fmdigest, fmgenesis (status/export), fmexam scorecard line, plugin/tests/test_proof.py, MASTER.md, README.md, CHANGELOG.md
- 2026-10-31T06:02:42Z done
- 2026-10-31T06:02:44Z committed f03acae6 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research draft-mission-genesis-gen1: Task: T-2093 (brief 1, fm genesis check), T-2095 (brief 2, fm genesis step), T-2099 (brief 3, fm genesis draft/spec), T-2102 (brief …
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- research draft-critique-initiative-gen1: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- decision 2026-10-31: While the Genesis tower waits on T-2221 (Mission 3's critique; the cold-read rule change is the user's steer-2 call, T-2246), build the gap map's Mi…
- the similar finished task took 5 steps
## Lessons
- Any rollup added to a polled surface needs a measured warm cost on the real project before merge: the test project's 5 briefs hid a 1.6 s scan
## Files touched
- plugin/tests/test_proof.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/lib/fmcost.py
- plugin/lib/fmexam.py
- MASTER.md
- README.md
- plugin/lib/fmgenesis.py
- CHANGELOG.md
