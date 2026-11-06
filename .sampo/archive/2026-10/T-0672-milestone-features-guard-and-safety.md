---
id: T-0672
type: SECURITY
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:13Z
updated: 2026-10-09T16:27:39Z
batch: [T-0441, T-0462, T-0478, T-0479, T-0480, T-0502]
base: b70a350a3df4b9e3e023803324f6ec7eb054f70a
base_tree: cd21fddebf7ac73f1d6f8e8d7b824e04a96a2cc4
verified: strong
---
# Milestone: Features — Guard and safety
## Raw request
> T-0441: SECURITY: Exfiltration and secrets (C031, value 4/5, effort M, risk med)
>   first version: Extend fm secrets into a done-gate check on the task diff and outbound-looking commands (curl/scp of files matching secret patterns) already refused by guard; skip honeytokens. Strictly adds refusals.
>   what it is: Scan outbound data, redact secrets at write time, plant honeytokens and label information flow between projects.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 6 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0462: SECURITY: Cleanup as a done gate (C036, value 3/5, effort S, risk low)
>   first version: In fm check/finish, list untracked files and stray tmp/worktrees the task created that are outside its scope and warn (block only with a flag). Reuse fmtidy lists.
>   what it is: Sweep leftovers after every task, treat cleanup as a done obligation and run a recurring janitor with deletion-safety proof.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 5 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0478: SECURITY: Snapshots, undo and irreversibility (C030, value 3/5, effort M, risk med)
>   first version: First version: before a destructive-category grant is used, record git stash-create/HEAD sha in the task log and name restorable vs irreversible in the ask text. No effect ledger yet.
>   what it is: Snapshot before risky actions, classify what git can restore, keep an effect ledger and budget irreversible steps.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 9 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0479: SECURITY: Supply-chain and install trust (C032, value 3/5, effort M, risk low)
>   first version: Record a content hash of each enabled plugin and MCP tool description in doctor and warn on change between runs. Detection only.
>   what it is: Gate dependency changes, quarantine unknown repos, pin and diff plugins and MCP descriptions, and sign releases.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 6 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0480: SECURITY: Hardening Foreman's own surfaces (C034, value 3/5, effort M, risk med)
>   first version: First version: one sanitizer for rendered strings (strip ESC/OSC) applied to statusline and task output, plus a fuzz test of the approval-phrase parser in fmcore. Skip desktop IPC lockdown here.
>   what it is: Neutralise control sequences, audit symlinks and permissions, lock down the desktop IPC, fuzz the approval parser and keep an executable threat model.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 8 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0502: SECURITY: Guard as policy data and verified artifact (C026, value 3/5, effort L, risk high)
>   first version: Cheap first step only: log a rule id per block into the event log and report fire counts in fm friction/replay (decision ledger). Defer the data-table rewrite and IR; a rewrite risks loosening the guard, so gate it on the monotonicity check via fm replay.
>   what it is: Express guard rules as data with origins and fire records, compile them to an effect IR, and prove a rule change can't loosen the guard.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 13 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Do T-0441, T-0462, T-0478, T-0479, T-0480, T-0502 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0672. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0441: Exfiltration and secrets (C031, value 4/5, effort M, risk med) works — verify with `python3 plugin/tests/run.py -p test_safety.py -k SecretsGate`
- [x] T-0462: Cleanup as a done gate (C036, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_safety.py -k CleanupGate`
- [x] T-0478: Snapshots, undo and irreversibility (C030, value 3/5, effort M, risk med) works — verify with `python3 plugin/tests/run.py -p test_safety.py -k UndoPoint`
- [x] T-0479: Supply-chain and install trust (C032, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_safety.py -k SupplyChainHash`
- [x] T-0480: Hardening Foreman's own surfaces (C034, value 3/5, effort M, risk med) works — verify with `python3 plugin/tests/run.py -p test_safety.py -k RenderSanitizer`
- [x] T-0502: Guard as policy data and verified artifact (C026, value 3/5, effort L, risk high) works — verify with `python3 plugin/tests/run.py -p test_safety.py -k RuleIds`
## Non-goals
## Approach (options → choice → why)
One milestone, six first slices, strictly adding checks or logging (plan review: revise, folded in). Tests in plugin/tests/test_safety.py, a class per member, each with concrete cases incl. a false-positive case: SecretsGate (a diff adding an AWS-style key or a private-key block is flagged at fm task finish; a test fixture named *fake*/example and a hash literal are not; warn by default, block only with --strict); CleanupGate (untracked files the task created outside its scope and leftover worktrees are listed at finish as a warning, never a block); UndoPoint (before a destructive-category grant is used, the task log records git stash create / HEAD sha, and the fm ask text says restorable vs irreversible); SupplyChainHash (fm doctor stores state/supply.json: sha256 of each enabled plugin's manifest+hooks and each MCP server command; first run is a silent baseline; a change warns once with the diff and fm doctor --accept-supply re-baselines); RenderSanitizer (ESC/OSC/CSI stripped from task titles in statusline and fm output; approval-phrase parser fuzzed with a fixed seed, 500 cases); RuleIds (each guard block event carries a rule id from the check that fired, existing consumers unchanged; fm replay and fm friction report fire counts). Order: RuleIds first (guard-touching) then an intermediate guard-suite run, then the rest. One commit per member inside the batch so each can be reverted alone; full gates, fm replay (nothing newly allowed) and one reviewer pass once at close.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0441: Exfiltration and secrets (C031, value 4/5, effort M, risk med)
2. [x] T-0462: Cleanup as a done gate (C036, value 3/5, effort S, risk low)
3. [x] T-0478: Snapshots, undo and irreversibility (C030, value 3/5, effort M, risk med)
4. [x] T-0479: Supply-chain and install trust (C032, value 3/5, effort M, risk low)
5. [x] T-0480: Hardening Foreman's own surfaces (C034, value 3/5, effort M, risk med)
6. [x] T-0502: Guard as policy data and verified artifact (C026, value 3/5, effort L, risk high)
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_safety.py` → ✗ exit 1 · Ran 0 tests in 0.0s (0 classes, 16 at a time; slowest: ) / NO TESTS RAN [ran] [tree cd21fddebf7a] (2026-10-09T16:12:53Z)
- (step 1) `python3 plugin/tests/run.py -p test_safety.py` → ✗ exit 1 · Ran 10 tests in 0.5s (6 classes, 16 at a time; slowest: RenderSanitizer 1s, RuleIds 0s, SecretsGate 0s) / FAILED (5 classes) [ran] [tree d2d59f2854ed] (2026-10-09T16:13:17Z)
- (step 7) `python3 plugin/tests/run.py -p test_safety.py -k RuleIds` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: RuleIds 0s) / OK [ran] [tree 25fa77bd1a96] (2026-10-09T16:16:33Z)
- (step 6) `python3 plugin/tests/run.py -p test_safety.py -k RuleIds` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: RuleIds 0s) / OK [ran] [tree 25fa77bd1a96] (2026-10-09T16:16:38Z)
- (step 1) `python3 plugin/tests/run.py -p test_safety.py -k SecretsGate -k CleanupGate` → exit 0 · Ran 3 tests in 0.6s (2 classes, 16 at a time; slowest: SecretsGate 1s, CleanupGate 0s) / OK [ran] [tree b30a98406cfb] (2026-10-09T16:19:38Z)
- (step 2) `python3 plugin/tests/run.py -p test_safety.py -k SecretsGate -k CleanupGate` → exit 0 · Ran 3 tests in 0.6s (2 classes, 16 at a time; slowest: SecretsGate 1s, CleanupGate 0s) / OK [ran] [tree b30a98406cfb] (2026-10-09T16:19:39Z)
- (step 3) `python3 plugin/tests/run.py -p test_safety.py -k UndoPoint` → exit 0 · Ran 2 tests in 0.2s (1 classes, 16 at a time; slowest: UndoPoint 0s) / OK [ran] [tree 1bfb3c516d0c] (2026-10-09T16:20:10Z)
- (step 4) `python3 plugin/tests/run.py -p test_safety.py -k SupplyChainHash` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: SupplyChainHash 0s) / OK [ran] [tree c04ac65b9cf8] (2026-10-09T16:20:42Z)
- (step 5) `python3 plugin/tests/run.py -p test_safety.py -k RenderSanitizer` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: RenderSanitizer 0s) / OK [ran] [tree c04ac65b9cf8] (2026-10-09T16:20:43Z)
- (step 3) `python3 plugin/tests/run.py -p test_safety.py` → exit 0 · Ran 11 tests in 1.4s (6 classes, 16 at a time; slowest: SecretsGate 1s, CleanupGate 1s, RuleIds 1s) / OK [ran] [tree 01b9ffd25515] (2026-10-09T16:27:33Z)
- (ac 1) `python3 plugin/tests/run.py -p test_safety.py -k SecretsGate` → exit 0 · Ran 2 tests in 1.2s (1 classes, 16 at a time; slowest: SecretsGate 1s) / OK [ran] [tree 01b9ffd25515] (2026-10-09T16:27:38Z)
- (ac 2) `python3 plugin/tests/run.py -p test_safety.py -k CleanupGate` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: CleanupGate 1s) / OK [ran] [tree 01b9ffd25515] (2026-10-09T16:27:38Z)
- (ac 3) `python3 plugin/tests/run.py -p test_safety.py -k UndoPoint` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: UndoPoint 0s) / OK [ran] [tree 01b9ffd25515] (2026-10-09T16:27:38Z)
- (ac 4) `python3 plugin/tests/run.py -p test_safety.py -k SupplyChainHash` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: SupplyChainHash 0s) / OK [ran] [tree 01b9ffd25515] (2026-10-09T16:27:38Z)
- (ac 5) `python3 plugin/tests/run.py -p test_safety.py -k RenderSanitizer` → exit 0 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: RenderSanitizer 1s) / OK [ran] [tree 01b9ffd25515] (2026-10-09T16:27:38Z)
- (ac 6) `python3 plugin/tests/run.py -p test_safety.py -k RuleIds` → exit 0 · Ran 2 tests in 0.8s (1 classes, 16 at a time; slowest: RuleIds 1s) / OK [ran] [tree 01b9ffd25515] (2026-10-09T16:27:38Z)
- (audit intent) `six slices test-first (one red run for all classes), per-class checks per step, rule ids first with an intermediate guard check, commit per member; one close-out fm check (999+ tests, replay 0 newly allowed); one fm-reviewer pass plus the commit scanner: every nit fixed test-first (supply hash covers whole install trees and per-project MCP, never crashes doctor, an unreadable baseline warns; close warnings never crash a closed task and skip caches; placeholder filter per token; undo text says exactly what's covered, stash pinned under refs/foreman/undo, unrecorded work logged)` → six first slices, each only adding a check or logging [tree 01b9ffd25515] (2026-10-09T16:27:38Z)
- (audit adversary) `six slices test-first (one red run for all classes), per-class checks per step, rule ids first with an intermediate guard check, commit per member; one close-out fm check (999+ tests, replay 0 newly allowed); one fm-reviewer pass plus the commit scanner: every nit fixed test-first (supply hash covers whole install trees and per-project MCP, never crashes doctor, an unreadable baseline warns; close warnings never crash a closed task and skip caches; placeholder filter per token; undo text says exactly what's covered, stash pinned under refs/foreman/undo, unrecorded work logged)` → rule_id is an attribute only (no guard decision changed, replay 0 newly allowed); no secret value is printed (test); supply hashing is local, nothing sent [tree 01b9ffd25515] (2026-10-09T16:27:38Z)
- (audit edge) `six slices test-first (one red run for all classes), per-class checks per step, rule ids first with an intermediate guard check, commit per member; one close-out fm check (999+ tests, replay 0 newly allowed); one fm-reviewer pass plus the commit scanner: every nit fixed test-first (supply hash covers whole install trees and per-project MCP, never crashes doctor, an unreadable baseline warns; close warnings never crash a closed task and skip caches; placeholder filter per token; undo text says exactly what's covered, stash pinned under refs/foreman/undo, unrecorded work logged)` → garbled or wrong-shaped registry and baseline files warn, never crash or rebaseline; placeholder tokens skipped, real tokens on lines that say 'your' still flagged [tree 01b9ffd25515] (2026-10-09T16:27:38Z)
- (audit operator) `six slices test-first (one red run for all classes), per-class checks per step, rule ids first with an intermediate guard check, commit per member; one close-out fm check (999+ tests, replay 0 newly allowed); one fm-reviewer pass plus the commit scanner: every nit fixed test-first (supply hash covers whole install trees and per-project MCP, never crashes doctor, an unreadable baseline warns; close warnings never crash a closed task and skip caches; placeholder filter per token; undo text says exactly what's covered, stash pinned under refs/foreman/undo, unrecorded work logged)` → warnings never block a close; doctor gains one check [tree 01b9ffd25515] (2026-10-09T16:27:38Z)
- (audit maintainer) `six slices test-first (one red run for all classes), per-class checks per step, rule ids first with an intermediate guard check, commit per member; one close-out fm check (999+ tests, replay 0 newly allowed); one fm-reviewer pass plus the commit scanner: every nit fixed test-first (supply hash covers whole install trees and per-project MCP, never crashes doctor, an unreadable baseline warns; close warnings never crash a closed task and skip caches; placeholder filter per token; undo text says exactly what's covered, stash pinned under refs/foreman/undo, unrecorded work logged)` → helpers live beside their callers (fmcli close, fmhooks grant, fmdoctor check); test_safety has a class per member [tree 01b9ffd25515] (2026-10-09T16:27:38Z)
## Log
- 2026-10-09T15:40:13Z created
- 2026-10-09T16:03:58Z criterion 1 verify: `` → `python3 plugin/tests/run.py -p test_safety.py -k SecretsGate`
- 2026-10-09T16:03:58Z criterion 2 verify: `` → `python3 plugin/tests/run.py -p test_safety.py -k CleanupGate`
- 2026-10-09T16:03:58Z criterion 3 verify: `` → `python3 plugin/tests/run.py -p test_safety.py -k UndoPoint`
- 2026-10-09T16:03:58Z criterion 4 verify: `` → `python3 plugin/tests/run.py -p test_safety.py -k SupplyChainHash`
- 2026-10-09T16:03:58Z criterion 5 verify: `` → `python3 plugin/tests/run.py -p test_safety.py -k RenderSanitizer`
- 2026-10-09T16:03:59Z criterion 6 verify: `` → `python3 plugin/tests/run.py -p test_safety.py -k RuleIds`
- 2026-10-09T16:03:59Z set approved=True
- 2026-10-09T16:05:35Z plan review (fm second plan): revise -> folded in: concrete and false-positive cases, warn-not-block defaults, guard step first with an intermediate check, commit per member, supply baseline/accept, seeded fuzz
- 2026-10-09T16:09:08Z focused
- 2026-10-09T16:09:17Z paused: focus moved to T-0699
- 2026-10-09T16:09:56Z focused
- 2026-10-09T16:10:56Z paused: focus moved to T-0700
- 2026-10-09T16:12:56Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-09T16:12:56Z focused
- 2026-10-09T16:15:26Z RuleIds green; intermediate guard check next (the plan's revert point)
- 2026-10-09T16:19:44Z hypothesis checked: the 8 fmcli edits are two helpers plus their call; SecretsGate and CleanupGate classes green after them; nothing else in fmcli changed
- 2026-10-09T16:23:01Z paused: focus moved to T-0673
- 2026-10-09T16:25:26Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-09T16:25:26Z focused
- 2026-10-09T16:27:38Z done
- 2026-10-09T16:27:39Z committed 5b835be (5 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: Acceptance criteria are only `-k <Class>` test runs, and the tests are written by the same engineer alongside the code. They prove the tests pass, not that the behavior matches each request. Several first-version lines are underspecified: T-0441's "outbound-looking commands already refused by…
- HIGH: "Strictly adds refusals" is only checked by `fm replay` once, at close. A false-positive secret scan on the task diff or a cleanup block could stall every future task's done-gate, and nothing in the plan measures that. For T-0441 and T-0462, the plan must make the default non-blocking or flag…
- HIGH: Batching six changes, including T-0502 (risk high, touching guard block events), into one run with full gates only at close makes failures hard to localize. A break in the shared guard or event-log path can't be attributed to a step, and the one commit can't be partly reverted. T-0441 and T-0…
- MEDIUM: Shared-file conflict risk: all six classes go in one `test_safety.py` and likely share `fm check/finish`, doctor, and the event log. Writing all failing tests first, then implementing sequentially, is fine, but the plan doesn't say how a later step's test is kept from failing because of an …
- MEDIUM: T-0479 stores hashes of plugin/MCP descriptions "between runs", so it needs persistent state, and the plan says nothing about where it lives, what the first run does (baseline, not a warning), or what happens when a legitimate update changes the hash. T-0478 similarly writes a `git stash-cr…
- LOW: The T-0480 approval-phrase fuzz test must be deterministic (fixed seed, bounded iterations), or it becomes a flaky gate. T-0502 should also say where fire counts are surfaced (`fm friction`/`replay`) and that the rule id is added without changing existing block event consumers. — Seed the fuzz…
Verdict: revise — the scope is feasible, but the tests need concrete cases and false-positive coverage, and the guard-touching steps need an intermediate check and a revert path before the batch starts.
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-foreman-20261009: 835 ideas, 103 capabilities; every idea is listed under exactly one capability.
- T-0550 [SECURITY M, dropped, 0 steps] Hardening Foreman's own surfaces (C034, value 3/5, effort M, risk med)
- T-0511 [SECURITY M, dropped, 0 steps] Exfiltration and secrets (C031, value 4/5, effort M, risk med)
- decision 2026-09-26: Full autonomy never asks mid-run but still can't grant itself core or run destructive/irreversible guard categories: those are recorded with fm ask …
## Lessons
- a safety claim shown to the user (restorable) must state its limits; a reviewer will find the gap between the claim and the mechanism
## Files touched
- plugin/tests/test_safety.py
- plugin/lib/fmguard.py
- plugin/lib/fmhooks.py
- plugin/lib/fmfriction.py
- plugin/lib/fmcli.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcore.py
- plugin/lib/fmeco.py
- plugin/lib/fmwatch.py
- plugin/tests/test_doctor.py
- plugin/tests/test_ecosystem.py
