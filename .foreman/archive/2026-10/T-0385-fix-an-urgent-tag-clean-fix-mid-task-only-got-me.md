---
id: T-0385
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T01:26:26Z
updated: 2026-10-09T01:39:39Z
base: f5abd65bbc1301db072c61fc267760e4e2a87cb1
base_tree: a87fa64ebdcbfcec56ccabc0d86966e32fe81acb
verified: strong
---
# FIX: an urgent tag (CLEAN!:, FIX!: …) mid-task only got 'Message has 1 intake item (CLEAN!
## Raw request
> FIX: an urgent tag (CLEAN!:, FIX!: …) mid-task only got 'Message has 1 intake item (CLEAN!)'; the prompt note must say: checkpoint <active> now and focus this (JARVIS finished three tasks first)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] an urgent tag while another task is active tells Claude to checkpoint it and switch now; with no active task, no switch line — verify with `python3 plugin/tests/run.py -k test_urgent_tag_mid_task_says_switch_now`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first, then the note in the UserPromptSubmit intake line
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k test_urgent_tag_mid_task_says_switch_now` → ✗ exit 1 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: UserPromptSubmit 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree a7a601beb83c] (2026-10-09T01:38:16Z)
- `python3 plugin/tests/run.py -k test_urgent_tag_mid_task_says_switch_now` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: UserPromptSubmit 0s) / OK [ran] [tree a7a601beb83c] (2026-10-09T01:38:16Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (26 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.0    33.0     150  [0] / SessionEnd                  29.5    31.1     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/run.py → exit 0 · Ran 909 tests in [ran] [tree ac0ab6984f1c] (2026-10-09T01:39:38Z)
- (ac 1) `python3 plugin/tests/run.py -k test_urgent_tag_mid_task_says_switch_now` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: UserPromptSubmit 0s) / OK [ran] [tree ac0ab6984f1c] (2026-10-09T01:39:38Z)
- (audit intent) `self: traced the note against an active task and none; hook suite green` → an urgent item mid-task names the active task, fm checkpoint and 'now'; nothing active, no switch line (test) [tree ac0ab6984f1c] (2026-10-09T01:39:38Z)
- (audit edge) `self: traced the note against an active task and none; hook suite green` → a non-urgent item mid-task gets no switch line; the note stays within the prompt budget (existing test) [tree ac0ab6984f1c] (2026-10-09T01:39:38Z)
- (audit self) `self: traced the note against an active task and none; hook suite green` → no findings [tree ac0ab6984f1c] (2026-10-09T01:39:38Z)
## Log
- 2026-10-09T01:26:26Z created
- 2026-10-09T01:37:55Z focused
- 2026-10-09T01:39:39Z done
- 2026-10-09T01:39:39Z committed 9ad3ab6 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0259 [FIX S, done, 1 steps] fm intake: CONTEXT/DONE-WHEN lines between items belong to the item above; trailing ones still apply to all
- research T-0257-review: MEDIUM** — `plugin/lib/fmcli.py:540` (host built by `_create`), with the gate at `plugin/lib/fmcore.py:1449`. An explore item (`TAG?:`) is meant …
- T-0262 [FEATURE M, done, 4 steps] Smarter nudges: already-covered requests, decision revisit triggers, quieter ignored hints — lesson: Text Foreman later parses for tags…
- decision 2026-10-04: The recursive brainstorm loop is dry: pass 5 kept 2 small ideas (built as T-0287) and pass 6 (fresh lenses: performance, unspoken needs; 43 titles) …
- similar finished tasks took 1–4 steps
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
