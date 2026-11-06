---
id: T-1752
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmbus.py, plugin/lib/fmcore.py, plugin/lib/fmhome.py, plugin/lib/fmsync.py, plugin/agents/fm-builder.md, plugin/tests/test_cli.py, plugin/tests/test_bus.py, plugin/tests/test_core.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T05:06:05Z
updated: 2026-10-23T05:27:41Z
batch: [T-1747, T-1748, T-1750]
base: d63d2058a74bdc47c06dce949382b8a7c6808ab0
base_tree: bda435ac628acd25062d26e85c1faf978e5d20ec
plan0_at: 2026-10-23T05:22:12Z
plan0_scope: [plugin/lib/fmcli.py, plugin/lib/fmbus.py, plugin/lib/fmcore.py, plugin/lib/fmhome.py, plugin/lib/fmsync.py, plugin/agents/fm-builder.md, plugin/tests/test_cli.py, plugin/tests/test_bus.py, plugin/tests/test_core.py, CHANGELOG.md]
verified: strong
---
# Workflow output fixes: check --affected --evidence records evidence, lease take lists only its own, a confirm gap says …
## Raw request
> T-1747: fm check --affected --evidence ID records no evidence, yet the builder contract tells builders to rely on it: record it, or reword the contract
> T-1748: fm lease take prints every lease in the project instead of only the ones it took
> T-1750: fmcore.plan_gaps' confirm text says 'a child found this request in an old session', which is wrong for imported or synced tasks: say why this task waits
## Interpretation
Do T-1747, T-1748, T-1750 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-1752. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1747: fm check --affected --evidence ID records the affected run as evidence on the task's current step (or the builder contract stops saying it does) — verify with `python3 plugin/tests/run.py test_cli.AffectedPairs`
- [x] T-1748: fm lease take prints only the leases it took and any conflicts, not every lease in the project — verify with `python3 plugin/tests/run.py test_bus.Lease`
- [x] T-1750: plan_gaps' confirm line says why the task waits (imported, synced, or found in an old session) from a reason the brief records — verify with `python3 plugin/tests/run.py test_core`
## Non-goals
## Approach (options → choice → why)
Three output fixes, test-first. T-1747: read how --evidence is handled for a full run and do the same for --affected (one code path), recording the affected command and result; if --affected evidence would let a task close without full gates, keep the close gate unchanged (it still needs fm check). T-1748: mirror T-1729's drop output for take. T-1750: a confirm_why meta field set where confirm is set (fm home import, fm sync, the old-session finder), shown by plan_gaps; default text when absent.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1747: Fm check --affected --evidence ID records no evidence, yet the builder contract tells buil
2. [x] T-1748: Fm lease take prints every lease in the project instead of only the ones it took
3. [x] T-1750: Fmcore.plan_gaps' confirm text says 'a child found this request in an old session', which
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli.AffectedPairs` → red as expected (exit 1) · Ran 5 tests in 5.8s (1 classes, 16 at a time; slowest: AffectedPairs 5s) / FAILED (1 classes) [ran] [tree af98b2d0a2b4] (2026-10-23T05:22:31Z)
- (ac 1) `python3 plugin/tests/run.py test_cli.AffectedPairs 2>&1 | grep -E "AssertionError|Error|^OK" | head -3` → exit 0 · OK [ran] [tree 12b6de22935a] (2026-10-23T05:22:48Z)
- (step 2) `python3 plugin/tests/run.py test_cli.AffectedPairs 2>&1 | grep -E "AssertionError|Error|^OK" | head -3` → exit 0 · OK [ran] [tree 12b6de22935a] (2026-10-23T05:22:48Z)
- (step 2) `python3 plugin/tests/run.py test_bus.Lease` → red as expected (exit 1) · Ran 5 tests in 4.0s (1 classes, 16 at a time; slowest: Lease 4s) / FAILED (1 classes) [ran] [tree 93736d81dc3c] (2026-10-23T05:23:09Z)
- (step 3) `python3 plugin/tests/run.py test_core.Planning` → red as expected (exit 1) · run.py: no test matches test_core.Planning [ran] [tree e86d9c4803dd] (2026-10-23T05:23:53Z)
- (step 3) `python3 plugin/tests/run.py test_core.Stages` → red as expected (exit 1) · Ran 5 tests in 0.2s (1 classes, 16 at a time; slowest: Stages 0s) / FAILED (1 classes) [ran] [tree e86d9c4803dd] (2026-10-23T05:23:56Z)
- (step 1) `python3 plugin/tests/run.py test_cli.AffectedPairs test_bus.Lease test_core.Stages` → exit 0 · Ran 15 tests in 9.3s (3 classes, 16 at a time; slowest: AffectedPairs 9s, Lease 7s, Stages 0s) / OK [ran] [tree 0ef42254285f] (2026-10-23T05:25:07Z)
- (step 2) `python3 plugin/tests/run.py test_cli.AffectedPairs test_bus.Lease test_core.Stages` → exit 0 · Ran 15 tests in 9.5s (3 classes, 16 at a time; slowest: AffectedPairs 9s, Lease 7s, Stages 0s) / OK [ran] [tree 0ef42254285f] (2026-10-23T05:25:17Z)
- (step 3) `python3 plugin/tests/run.py test_cli.AffectedPairs test_bus.Lease test_core.Stages` → exit 0 · Ran 15 tests in 7.9s (3 classes, 16 at a time; slowest: AffectedPairs 8s, Lease 7s, Stages 0s) / OK [ran] [tree 0ef42254285f] (2026-10-23T05:25:25Z)
- (ac 1) `python3 plugin/tests/run.py test_cli.AffectedPairs` → exit 0 · Ran 5 tests in 4.7s (1 classes, 16 at a time; slowest: AffectedPairs 5s) / OK [ran] [tree 0ef42254285f] (2026-10-23T05:25:31Z)
- (ac 2) `python3 plugin/tests/run.py test_bus.Lease` → exit 0 · Ran 5 tests in 4.0s (1 classes, 16 at a time; slowest: Lease 4s) / OK [ran] [tree 0ef42254285f] (2026-10-23T05:25:35Z)
- (ac 3) `python3 plugin/tests/run.py test_core` → exit 0 · Ran 74 tests in 1.8s (17 classes, 16 at a time; slowest: WritesAndLocks 2s, PreToolUse 1s, ActiveFast 1s) / OK [ran] [tree 0ef42254285f] (2026-10-23T05:25:37Z)
- (ac 1) `python3 plugin/tests/run.py test_cli.AffectedPairs` → exit 0 · Ran 5 tests in 4.7s (1 classes, 16 at a time; slowest: AffectedPairs 5s) / OK [ran] [tree 0ef42254285f] (2026-10-23T05:25:56Z)
- (ac 2) `python3 plugin/tests/run.py test_bus.Lease` → exit 0 · Ran 5 tests in 4.0s (1 classes, 16 at a time; slowest: Lease 4s) / OK [ran] [tree 0ef42254285f] (2026-10-23T05:25:56Z)
- (ac 3) `python3 plugin/tests/run.py test_core` → exit 0 · Ran 74 tests in 1.9s (17 classes, 16 at a time; slowest: WritesAndLocks 2s, PreToolUse 1s, ActiveFast 1s) / OK [ran] [tree 0ef42254285f] (2026-10-23T05:25:56Z)
- (audit intent) `self: the affected run records evidence with the same add_evidence call a full run uses, labelled 'affected tests only' (close still needs a full fm check); lease take prints only what it took (8 then '… N more'), overlaps stay on stderr; confirm_why is set where confirm is set (fm sync settle, fm home import, the bench replay), shown plain and capped at 160 characters, and a pulled brief's own confirm_why is dropped so only this machine says why` → builders' affected runs leave evidence as the contract says; lease take reads like lease drop; a waiting task says why it waits [tree 0ef42254285f] (2026-10-23T05:25:56Z)
- (audit adversary) `self: the affected run records evidence with the same add_evidence call a full run uses, labelled 'affected tests only' (close still needs a full fm check); lease take prints only what it took (8 then '… N more'), overlaps stay on stderr; confirm_why is set where confirm is set (fm sync settle, fm home import, the bench replay), shown plain and capped at 160 characters, and a pulled brief's own confirm_why is dropped so only this machine says why` → confirm_why from a synced brief is dropped (a repo can't word the reason); it's plain()ed before display [tree 0ef42254285f] (2026-10-23T05:25:56Z)
- (audit edge) `self: the affected run records evidence with the same add_evidence call a full run uses, labelled 'affected tests only' (close still needs a full fm check); lease take prints only what it took (8 then '… N more'), overlaps stay on stderr; confirm_why is set where confirm is set (fm sync settle, fm home import, the bench replay), shown plain and capped at 160 characters, and a pulled brief's own confirm_why is dropped so only this machine says why` → no confirm_why falls back to the old-session text; --affected evidence lands on --step/--ac like a full run's [tree 0ef42254285f] (2026-10-23T05:25:56Z)
- `python3 plugin/tests/run.py test_cli.AffectedPairs test_bus.Lease test_core.Stages` → ✗ exit 1 · Ran 15 tests in 5.4s (3 classes, 16 at a time; slowest: AffectedPairs 5s, Lease 4s, Stages 0s) / FAILED (3 classes) (start tree + this task's tests) [ran] [tree 0ef42254285f] (2026-10-23T05:26:55Z)
- `python3 plugin/tests/run.py test_cli.AffectedPairs test_bus.Lease test_core.Stages` → exit 0 · Ran 15 tests in 4.7s (3 classes, 16 at a time; slowest: AffectedPairs 5s, Lease 4s, Stages 0s) / OK [ran] [tree 0ef42254285f] (2026-10-23T05:26:55Z)
- (audit intent) `self: the affected run records evidence with the same add_evidence call a full run uses, labelled 'affected tests only' (close still needs a full fm check); lease take prints only what it took (8 then '… N more'), overlaps stay on stderr; confirm_why is set where confirm is set (fm sync settle, fm home import, the bench replay), shown plain and capped at 160 characters, and a pulled brief's own confirm_why is dropped so only this machine says why` → builders' affected runs leave evidence as the contract says; lease take reads like lease drop; a waiting task says why it waits [tree 0ef42254285f] (2026-10-23T05:26:56Z)
- (audit adversary) `self: the affected run records evidence with the same add_evidence call a full run uses, labelled 'affected tests only' (close still needs a full fm check); lease take prints only what it took (8 then '… N more'), overlaps stay on stderr; confirm_why is set where confirm is set (fm sync settle, fm home import, the bench replay), shown plain and capped at 160 characters, and a pulled brief's own confirm_why is dropped so only this machine says why` → confirm_why from a synced brief is dropped (a repo can't word the reason); it's plain()ed before display [tree 0ef42254285f] (2026-10-23T05:26:56Z)
- (audit edge) `self: the affected run records evidence with the same add_evidence call a full run uses, labelled 'affected tests only' (close still needs a full fm check); lease take prints only what it took (8 then '… N more'), overlaps stay on stderr; confirm_why is set where confirm is set (fm sync settle, fm home import, the bench replay), shown plain and capped at 160 characters, and a pulled brief's own confirm_why is dropped so only this machine says why` → no confirm_why falls back to the old-session text; --affected evidence lands on --step/--ac like a full run's [tree 0ef42254285f] (2026-10-23T05:26:56Z)
## Log
- 2026-10-23T05:06:05Z created
- 2026-10-23T05:06:19Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_cli.AffectedPairs`
- 2026-10-23T05:06:19Z criterion 1 text: T-1747: Fm check --affected --evidence ID records no evidence, yet the builder contract tells buil works → T-1747: fm check --affected --evidence ID records the affected run as evidence on the task's current step (or the builder contract stops saying it does)
- 2026-10-23T05:06:19Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_bus.Lease`
- 2026-10-23T05:06:19Z criterion 2 text: T-1748: Fm lease take prints every lease in the project instead of only the ones it took works → T-1748: fm lease take prints only the leases it took and any conflicts, not every lease in the project
- 2026-10-23T05:06:20Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_core`
- 2026-10-23T05:06:20Z criterion 3 text: T-1750: Fmcore.plan_gaps' confirm text says 'a child found this request in an old session', which works → T-1750: plan_gaps' confirm line says why the task waits (imported, synced, or found in an old session) from a reason the brief records
- 2026-10-23T05:06:20Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmbus.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmhome.py', 'plugin/lib/fmsync.py', 'plugin/agents/fm-builder.md', 'plugin/tests/test_cli.py', 'plugin/tests/test_bus.py', 'plugin/tests/test_core.py', 'CHANGELOG.md']
- 2026-10-23T05:18:42Z grounding T-1747: _check_affected (fmcli.py ~4480) runs the linked tests and prints, but never reads args.evidence; the full run records evidence with mutate(p, args.evidence, lambda b: b.add_evidence(cmd, result, step=args.step, ac=args.ac, tree=tree, ran=True)) at ~3820. Fix: the same call after the affected run (cmd = the affected command, result = run_result), labelled 'affected tests only' so it never reads as the full gates; the close gate still needs a full fm check (check_run), unchanged.
- 2026-10-23T05:22:12Z focused
- 2026-10-23T05:25:45Z scope: plugin/lib/fmbench.py (a replay-written task's confirm says why), plugin/tests/test_cli.py, test_bus.py, test_core.py
- 2026-10-23T05:27:39Z done
- 2026-10-23T05:27:41Z committed fe3648e5 (10 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1731 [FIX M, done, 4 steps] Lane and close friction: finish --commit and shared files, CLEAN behaviour-lock in builder briefs, check --affected ski… — lesson: Skip a t…
- T-1736 [CLEAN M, done, 4 steps] Small cleanups: one WCAG contrast function, unique help-tier positions, doctor's variation selectors, a MASTER.md modul… — lesson: A doc …
- T-0729 [FIX S, done, 3 steps] Friction: lane rm unlocks a finished builder's worktree; no false re-ask note on capture
- decision 2026-10-16: T-1032 plan: automatic failure→fix pairing in the hooks, recall across projects, pre-run warning, feedback counts, fm fix CLI, git transport via fm …
- similar finished tasks took 3–4 steps
- likely tests for the scope: plugin/tests/test_bus.py, plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_sync.py
## Why not caught
none: each was found in use by builders, not a regression
## Lessons
- Output that confirms an action should list only what that action did
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- plugin/tests/test_bus.py
- plugin/lib/fmbus.py
- plugin/tests/test_core.py
- plugin/lib/fmcore.py
- plugin/lib/fmsync.py
- plugin/lib/fmhome.py
- plugin/lib/fmbench.py
- CHANGELOG.md
