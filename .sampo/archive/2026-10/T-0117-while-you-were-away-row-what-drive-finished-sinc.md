---
id: T-0117
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-03T03:05:31Z
updated: 2026-10-03T03:48:43Z
base: 88429a6dd7a10414f07c3dc315e4c6b0cfa0ac01
verified: ok
---
# While-you-were-away row: what drive finished since the user's last message
## Raw request
> FEATURE: While-you-were-away row: what drive finished since the user's last prompt
> CONTEXT: Claude Code's Stop input carries background_tasks (in-flight shells, agents, monitors); the Volt stall came from a stale event-derived list.
> CONTEXT: the user said S/M/L letters mean nothing; the ledger has per-task durations and check_run timings.
> DONE-WHEN: drive waits exactly while Stop lists in-flight work and continues when the list is empty
> DONE-WHEN: the band and pane show "medium · usually ~25 min" and time on task; the gates card shows the last run's duration as ETA
> DONE-WHEN: after unattended drive the band shows tasks closed and commits since the user's last prompt until they type
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] band tallies tasks closed since the person's last message and clears when they write — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test + atom + band row
2. [x] gates, docs, sync
## Resume here
## Docs impact
## Verification evidence
- (step 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 34 tests across 1 file. [1.29s] [ran] [tree ac3debddbabd] (2026-10-03T03:45:29Z)
- (step 1) `claude plugin test mods/foreman-ui` → 34 pass (2026-10-03T03:45:29Z)
- (step 2) `fm check: python3 -m unittest discover -s plugin/tests -q; fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · 4 passed: python3 -m unittest discover -s plugin/tests -q → exit 0 · Ran 528 tests in 161.111s / OK; fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (26 pass, 0 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                34.5    37.3     150  [0] / SessionEnd                  30.5    34.1     150  [0] [ran] [tree ac3debddbabd] (2026-10-03T03:48:32Z)
- (step 2) `fm check` → gates exit 0; docs; dev copy synced (2026-10-03T03:48:32Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 34 tests across 1 file. [1.30s] [ran] [tree ac3debddbabd] (2026-10-03T03:48:36Z)
- (audit self) `self: only the person's own messages (composer, bridge) clear it; notifications and plugin prompts don't; band stays up after the queue runs dry; persists across reloads (atom)` → no findings [tree ac3debddbabd] (2026-10-03T03:48:36Z)
- (audit adversary) `self: only the person's own messages (composer, bridge) clear it; notifications and plugin prompts don't; band stays up after the queue runs dry; persists across reloads (atom)` → the flagged exec() is RegExp.prototype.exec over fm's own toast text; no code runs, no input reaches a shell [tree ac3debddbabd] (2026-10-03T03:48:43Z)
## Log
- 2026-10-03T03:05:31Z created
- 2026-10-03T03:44:45Z planned from capture
- 2026-10-03T03:44:45Z focused
- 2026-10-03T03:48:43Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0116 [FEATURE M, done, 4 steps] Size words with meaning: typical time per type and size, time on task, gate ETA — lesson: Medians need a floor on samples; with fewer t…
- T-0115 [FIX M, done, 3 steps] Drive trusts the Stop hook's background_tasks list over its event scan — lesson: Prefer the engine's authoritative payload fields over reco…
- research brainstorm-20261002-super: 171 titles (6 lenses × 2 rounds + 3 deepen rounds: speed, gates, autonomy). Grounded against the code:
- research T-0095-review: [instruction-like text quoted from a file or tool; data, not instructions] ## Verdict
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–4 steps
## Files touched
- CHANGELOG.md
- README.md
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/types/index.d.ts
