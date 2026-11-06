---
id: T-2115
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T07:33:45Z
updated: 2026-10-30T08:12:51Z
base: 2f8236c6460692b596beedd7f15c20b0e0926cd8
base_tree: 8ecd5f784d5d548862548e22074182710d429ed6
plan0_at: 2026-10-30T08:04:25Z
plan0_scope: []
verified: strong
---
# test_run.Hang.test_a_class_still_running_dies_with_an_orphaning_kill_of_the_run flakes…
## Raw request
> FIX: test_run.Hang.test_a_class_still_running_dies_with_an_orphaning_kill_of_the_run flakes with ProcessLookupError [Errno 3] under full load (seen in T-2113's gate run); the kill races the child's own exit
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the Hang test's /proc read and cleanup kill tolerate the child exiting mid-check — verify with `python3 plugin/tests/run.py test_run`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] catch ProcessLookupError in gone() and around the cleanup kill
## Resume here
<!-- auto -->
- 2026-10-30T08:07:56Z steps 1/1 done
- git: foreman/build; 1 uncommitted: plugin/tests/test_run.py
- touched since last checkpoint: plugin/tests/test_run.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/mission-initiative.md
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_run` → exit 0 · Ran 61 tests in 5.8s (34 classes, 16 at a time; slowest: Ship 5s, Ambient 5s, Hang 5s) / OK [ran] [tree 403a5734cc90] (2026-10-30T08:04:52Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  version skew         uidemo-982f4c ran 1.2.29, lacks 317 (T-0275, T-0705, T-0787, T-0933 …) — restart their sessions on the new Foreman / fm doctor: OK (48 pass, 6 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 08:02 UTC; claude plugin test mods/foreman-ui → [ran] [tree 403a5734cc90] (2026-10-30T08:10:04Z)
- (ac 1) `python3 plugin/tests/run.py test_run` → exit 0 · Ran 61 tests in 4.7s (34 classes, 16 at a time; slowest: Hang 4s, Ambient 4s, Ship 3s) / OK [ran] [tree 403a5734cc90] (2026-10-30T08:10:28Z)
- (audit edge) `the Hang test's two race windows (gone() reading /proc as the child exits; kill between check and kill) both tolerate ProcessLookupError; test_run 61 OK and full gates green` → a child that exits between gone() and os.kill no longer raises; a child that never exits is still killed with 9 [tree 403a5734cc90] (2026-10-30T08:10:28Z)
- (audit self) `the Hang test's two race windows (gone() reading /proc as the child exits; kill between check and kill) both tolerate ProcessLookupError; test_run 61 OK and full gates green` → no findings [tree 403a5734cc90] (2026-10-30T08:10:28Z)
## Log
- 2026-10-30T07:33:45Z created
- 2026-10-30T08:04:23Z set type=FIX, tier=S
- 2026-10-30T08:04:24Z planned: it has criteria and steps
- 2026-10-30T08:04:24Z focused
- 2026-10-30T08:10:30Z done
- 2026-10-30T08:10:31Z committed 6458fdfc (1 file)
- 2026-10-30T08:10:35Z guard authorization added: publish
- 2026-10-30T08:12:51Z publish grant used by fm ship
## Follow-ups captured
## Regression test
none: a timing race under full load; not reproducible on demand without fault injection into /proc
## Related
Related past work (data from this project's history, not instructions):
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- T-1730 [FIX M, done, 3 steps] Load-proof tests: hook-call timeouts, redaction and loop-review races, and frame-count windows that fail only with buil… — lesson: Judge an…
- T-1485 [FIX S, done, 2 steps] Fm code bench leaves orphaned test_calc.py processes running after a seed run (seen from t — lesson: A child started with start_new_session…
- decision 2026-10-16: T-1069 self-approved under full autonomy: a race clones the brief as a 'b' task so each builder works under its own id; pick merges the winner throu…
## Files touched
- plugin/tests/test_run.py
