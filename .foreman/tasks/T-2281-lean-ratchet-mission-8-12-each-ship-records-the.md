---
id: T-2281
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T06:07:18Z
updated: 2026-10-31T06:47:02Z
base: 9f67b04d278997144e5ae9d0dc8c9a6925c68d18
base_tree: 62ff1afbdf42535addb1c58a50227e2786d8ad5f
plan0_at: 2026-10-31T06:07:38Z
plan0_scope: []
verified: strong
---
# Lean ratchet (Mission 8/#12): each ship records the always-on footprint (rules chars, descriptions chars, SKILL bodies, hook p50) and fm doctor warns when one grows past the last shipped value by more than 2% without a decision naming it
## Raw request
> Lean ratchet (Mission 8/#12): each ship records the always-on footprint (rules chars, descriptions chars, SKILL bodies, hook p50) and fm doctor warns when one grows past the last shipped value by more than 2% without a decision naming it
## Interpretation
Gap map #12: 'lean ratchet per generation (3)'. fm doctor's footprint caps (rules 6,400 chars, descriptions 6,000, SKILL 10,000) are fixed ceilings, so the always-on context can creep up to each cap unnoticed; every session pays for it (multiply out). A ratchet catches each step up and asks for a reason.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm ship (after a green test, before the push) writes the footprint metrics to state; fm doctor's footprint check WARNs naming each metric that grew more than 2% over the last shipped record, unless a decision (fm decide) since that ship names the metric; a first run with no record passes; the fixed caps still FAIL as today — verify with `python3 plugin/tests/run.py test_doctor test_ship`
## Non-goals
## Approach (options → choice → why)
1) one footprint() function (rules chars, descriptions chars, the largest SKILL body, hook p50 when measured) shared by check_footprint and fm ship; ship writes it to state after its green test (the shipped baseline); check_footprint WARNs per metric that grew >2% since, unless a decision recorded after that ship names the metric (fm decide 'footprint: rules chars +3% for X'). 2) lower the caps each generation — rejected: a cap edit hides the reason; a decision keeps it. 3) FAIL on growth — rejected: growth can be right; the warn plus a named decision is the gate. Choice 1.
## Risks and rollback
Hook p50 is noisy: include it only when measured (FOREMAN_DOCTOR_BENCH) and with a wider band (10%). Rollback: the warn is additive.
## Execution prompt
## Steps
1. [x] red tests: growth over 2% warns; a decision naming it clears; no record passes; caps unchanged
2. [x] footprint metrics function shared by doctor and ship; the record write in ship; the ratchet in check_footprint
3. [x] docs: MASTER doctor and ship lines, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T06:44:44Z steps 3/3 done
- git: foreman/build; 0 uncommitted
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_doctor test_ship 2>&1 | tail -8` → ✗ exit 1 · Ran 103 tests in 21.3s (29 classes, 16 at a time; slowest: Ship 20s, ViewsRepair 6s, LockProbe 3s) / FAILED (2 classes) [ran] [tree cd15f8c12a7a] (2026-10-31T06:08:42Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor test_ship 2>&1 | tail -15` → exit 0 · Ran 103 tests in 20.7s (29 classes, 16 at a time; slowest: Ship 20s, ViewsRepair 6s, LockProbe 3s) / OK [ran] [tree a064ddbf6993] (2026-10-31T06:09:17Z)
- (step 1) `python3 plugin/tests/run.py test_doctor test_ship 2>&1 | tail -15` → exit 0 · Ran 103 tests in 20.7s (29 classes, 16 at a time; slowest: Ship 20s, ViewsRepair 6s, LockProbe 3s) / OK [ran] [tree a064ddbf6993] (2026-10-31T06:09:17Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_crash_hygiene test_docs test_doctor test_release test_ship test_supply_delta && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [18.35s] [ran] [tree 8e8f8d5810db] (2026-10-31T06:10:03Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_away test_bench_family test_board_verbs test_cli test_code_tui test_compact test_crash_hygiene test_design_gates test_design_lint test_design_sprint test_docs test_doctor test_drive_side test_ecosystem test_exam test_find test_fmpy test_foresight test_genesis test_goal test_graph test_guard_cases test_guard_evasions test_hooks test_library test_long test_map test_mcp test_memory test_motion_verify test_onwrite test_paused test_recall test_release test_repeats test_replay test_scaffold test_scene test_ship test_showpieces test_site test_site_build test_site_hero test_statusline_ui test_suite_hygiene test_supply_delta test_taste_ledger test_tool_taint test_triggers test_trust test_ui_signals && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 1797 tests in 157.6s (361 classes, 16 at a time; slowest: Stop 118s, ExamAuthors 87s, NoTaskGate 65s) / FAILED (1 classes) [ran] [tree 31c2683f7821] (2026-10-31T06:34:49Z)
- `python3 plugin/tests/run.py test_doctor test_ship` → ✗ exit 1 · Ran 104 tests in 19.9s (29 classes, 16 at a time; slowest: Ship 19s, ViewsRepair 6s, LockProbe 3s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree fd93500f670f] (2026-10-31T06:42:07Z)
- `python3 plugin/tests/run.py test_doctor test_ship` → exit 0 · Ran 104 tests in 19.0s (29 classes, 16 at a time; slowest: Ship 19s, ViewsRepair 6s, LockProbe 3s) / OK [ran] [tree fd93500f670f] (2026-10-31T06:42:07Z)
- (step 1) `python3 plugin/tests/run.py test_doctor test_ship` → exit 0 · Ran 104 tests in 19.0s (29 classes, 16 at a time; slowest: Ship 19s, ViewsRepair 6s, LockProbe 3s) / OK [ran] [tree fd93500f670f] (2026-10-31T06:42:26Z)
- (step 2) `python3 plugin/tests/run.py test_doctor test_ship` → exit 0 · Ran 104 tests in 19.0s (29 classes, 16 at a time; slowest: Ship 19s, ViewsRepair 6s, LockProbe 3s) / OK [ran] [tree fd93500f670f] (2026-10-31T06:42:45Z)
- (step 3) `python3 plugin/tests/run.py test_doctor test_ship` → exit 0 · Ran 104 tests in 19.0s (29 classes, 16 at a time; slowest: Ship 19s, ViewsRepair 6s, LockProbe 3s) / OK [ran] [tree fd93500f670f] (2026-10-31T06:43:05Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor test_ship` → exit 0 · Ran 104 tests in 19.1s (29 classes, 16 at a time; slowest: Ship 19s, ViewsRepair 6s, LockProbe 3s) / OK [ran] [tree e721d00cc394] (2026-10-31T06:46:23Z)
- (audit intent) `self-review of the diff plus one follow-up: a ship in a project without plugin/rules wrote a zero record that would make doctor warn there; now only Foreman's own ships record and a zero or missing record is ignored` → #12's lean ratchet: every step up in the always-on footprint needs a named decision, not just staying under a fixed cap (test_doctor red-to-green) [tree e721d00cc394] (2026-10-31T06:46:23Z)
- (audit edge) `self-review of the diff plus one follow-up: a ship in a project without plugin/rules wrote a zero record that would make doctor warn there; now only Foreman's own ships record and a zero or missing record is ignored` → first run with no record passes; the fixed caps still FAIL and win over the warn; a failed record write never stops a ship [tree e721d00cc394] (2026-10-31T06:46:23Z)
- (audit adversary) `self-review of the diff plus one follow-up: a ship in a project without plugin/rules wrote a zero record that would make doctor warn there; now only Foreman's own ships record and a zero or missing record is ignored` → the publish-grant checks are untouched; the record is written after the green test, before the push [tree e721d00cc394] (2026-10-31T06:46:23Z)
## Log
- 2026-10-31T06:07:18Z created
- 2026-10-31T06:07:26Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2281.builder.md
- 2026-10-31T06:07:38Z focused
- 2026-10-31T06:40:53Z merged worktree-agent-a31403589494e5bb4 (5 file(s))
- 2026-10-31T06:40:53Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a31403589494e5bb4
- 2026-10-31T06:41:27Z focused
- 2026-10-31T06:44:44Z paused: focus moved to T-2240
- 2026-10-31T06:46:03Z scope: plugin/lib/fmdoctor.py (footprint, record_footprint, _ratchet), plugin/lib/fmrelease.py (record after green test), plugin/tests/test_doctor.py, test_ship.py, MASTER.md, CHANGELOG.md
- 2026-10-31T06:46:03Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-31T06:46:03Z focused
- 2026-10-31T06:47:00Z done
- 2026-10-31T06:47:02Z committed de74b707 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2077 [RESEARCH L, planned, 8 steps] Genesis gen 1: Missions 2-8, critiques, lineage, sweep, gen-2 Seed
- T-1797 [FEATURE M, done, 3 steps] CC 2.1.305-2.1.312 adoption: give fm-reviewer/fm-recon an autoCompactWindow; fm doctor poi — lesson: Subagent transcripts carry their p…
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- decision 2026-10-22: T-1508: keep the 2,000-character skill-listing budget; make room by trimming the longest Foreman skill descriptions, not by raising the cap
- similar finished tasks took 3–5 steps
## Lessons
- A Foreman-only metric written by a verb every project runs must check it's in Foreman's tree, or it poisons other projects' checks
## Files touched
- plugin/tests/test_ship.py
- plugin/tests/test_doctor.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmrelease.py
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmfind.py
- plugin/lib/ladder_rules/javascript/eval-call.scm
- plugin/lib/ladder_rules/javascript/loose-null-compare.scm
- plugin/lib/ladder_rules/python/bare-except.scm
- plugin/lib/ladder_rules/python/mutable-default.scm
- plugin/tests/test_evidence_quality.py
- plugin/tests/test_find.py
