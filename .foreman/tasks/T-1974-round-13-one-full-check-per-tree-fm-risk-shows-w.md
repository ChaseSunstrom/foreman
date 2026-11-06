---
id: T-1974
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T11:32:47Z
updated: 2026-10-29T11:43:23Z
batch: [T-1971, T-1972, T-1973]
base: 52af012a93f73553b3360d6d59fe94fb98f7c59b
base_tree: db028cf60ec8e455a16c1d51b14534f9888fe8db
plan0_at: 2026-10-29T11:35:49Z
plan0_scope: []
verified: strong
---
# round 13: one full check per tree, fm risk shows what spent it, ambient after mid-gate edits
## Raw request
> T-1971: FIX: A second full fm check started while another runs on the same tree overwrites its gates_running marker and runs a second suite beside it; whichever ends first clears the marker for both. fm check now waits (at most 10 minutes, saying so) for another live full check on this tree, then reuses its cached pass when the tree is unchanged, and clears the marker only when it is its own (fmcli _cmd_check).
> DONE-WHEN: a full fm check started beside a live one waits for it and says so; the marker is cleared only by its owner :: python3 plugin/tests/run.py test_ambient test_close_gates
> T-1972: FIX: fm risk lists the guard rules that spend risk first: today the 8-row collision list showed only routine core/brief habits, so what spent the budget (system, rm-outside, pipe-shell blocks) was hidden (fmrisk cmd_risk).
> DONE-WHEN: with more than 8 routine rules, a spending rule still shows in fm risk :: python3 plugin/tests/run.py test_risk
> T-1973: FIX: An edit made while full gates run gets no ambient run (T-1965) and no pass (T-1963), and nothing tests it until the next fm check. When a full fm check ends and the tree changed during it, it starts one ambient run for those edits (fmcli _cmd_check → fmambient.after_edit).
> DONE-WHEN: a full check whose tree changed mid-run starts an ambient run afterward :: python3 plugin/tests/run.py test_ambient
## Interpretation
Do T-1971, T-1972, T-1973 as one batch: one gate run, one self-review (pace: no subagents), one commit. T-1971: a full fm check waits for another live full check on this tree, then computes its tree and cached pass; it clears gates_running only when the pid is its own. T-1972: fm risk's collision list shows spending rules first. T-1973: a full check whose tree changed while it ran starts one ambient run afterward.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1971: a full fm check started beside a live one waits for it and says so; the marker is cleared only by its owner :: python3 plugin/tests/run.py test_ambient test_close_gates — verify with `python3 plugin/tests/run.py test_ambient -k another`
- [x] T-1972: with more than 8 routine rules, a spending rule still shows in fm risk :: python3 plugin/tests/run.py test_risk — verify with `python3 plugin/tests/run.py test_risk -k spending`
- [x] T-1973: a full check whose tree changed mid-run starts an ambient run afterward :: python3 plugin/tests/run.py test_ambient — verify with `python3 plugin/tests/run.py test_ambient -k changed_mid`
## Non-goals
## Approach (options → choice → why)
T-1971 options: (a) wait for a live gates_running on this tree before computing the tree and the cached pass, so the other run's pass is reused; (b) refuse the second check; (c) lock file. Choice (a): it mirrors T-1964's ambient wait, reuses c.gates_live(here=True), and the cache answers at once when the tree is unchanged. Clear the marker only when its pid is ours. T-1972 options: sort spending rules first in cmd_risk; a separate today-only section; raise the 8-row cap. Choice: stable sort by spends, one line. T-1973 options: start one ambient run for wrote_paths after the marker clears; queue a dirty flag the next edit picks up; say so in the note only. Choice: one fmambient.after_edit call, which already checks ambient on, host strain and live gates.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1971: A second full fm check started while another runs on the same tree overwrites its gates_ru
2. [x] T-1972: Fm risk lists the guard rules that spend risk first: today the 8-row collision list showed
3. [x] T-1973: An edit made while full gates run gets no ambient run (T-1965) and no pass (T-1963), and n
## Resume here
## Docs impact
CHANGELOG Unreleased Fix line; MASTER fmambient (T-1971, T-1973) and risk budget (T-1972) lines.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ambient -k another` → ✗ exit 1 · Ran 48 tests in 10.7s (38 classes, 16 at a time; slowest: Ambient 10s, Claims 5s, Digest 3s) / FAILED (1 classes) [ran] [tree 8205c93fdb29] (2026-10-29T11:36:28Z)
- (step 2) `python3 plugin/tests/run.py test_risk -k spending` → ✗ exit 1 · Ran 9 tests in 4.1s (1 classes, 16 at a time; slowest: Risk 4s) / FAILED (1 classes) [ran] [tree 8205c93fdb29] (2026-10-29T11:36:33Z)
- (step 3) `python3 plugin/tests/run.py test_ambient -k changed_mid` → ✗ exit 1 · Ran 8 tests in 9.8s (1 classes, 16 at a time; slowest: Ambient 10s) / FAILED (1 classes) [ran] [tree 8205c93fdb29] (2026-10-29T11:36:43Z)
- (step 1) `python3 plugin/tests/run.py test_ambient -k another` → exit 0 · Ran 48 tests in 13.0s (38 classes, 16 at a time; slowest: Ambient 13s, Claims 5s, Digest 3s) / OK [ran] [tree e7ff99ee0891] (2026-10-29T11:37:40Z)
- (step 2) `python3 plugin/tests/run.py test_risk -k spending` → exit 0 · Ran 9 tests in 4.1s (1 classes, 16 at a time; slowest: Risk 4s) / OK [ran] [tree e7ff99ee0891] (2026-10-29T11:37:45Z)
- (step 3) `python3 plugin/tests/run.py test_ambient -k changed_mid` → exit 0 · Ran 8 tests in 11.9s (1 classes, 16 at a time; slowest: Ambient 12s) / OK [ran] [tree e7ff99ee0891] (2026-10-29T11:37:57Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmrisk.py — commit it through a task, or git checkout it back / fm doctor: OK (48 pass, 6 warn, ; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.1    42.4     150  [0] / SessionEnd                  35.1    37.0     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 3d1eb91bb1e9] (2026-10-29T11:42:15Z)
- (ac 1) `python3 plugin/tests/run.py test_ambient -k another` → exit 0 · Ran 48 tests in 12.8s (38 classes, 16 at a time; slowest: Ambient 13s, Claims 5s, Digest 3s) / OK [ran] [tree 3d1eb91bb1e9] (2026-10-29T11:42:55Z)
- (ac 2) `python3 plugin/tests/run.py test_risk -k spending` → exit 0 · Ran 9 tests in 4.1s (1 classes, 16 at a time; slowest: Risk 4s) / OK [ran] [tree 3d1eb91bb1e9] (2026-10-29T11:42:55Z)
- (ac 3) `python3 plugin/tests/run.py test_ambient -k changed_mid` → exit 0 · Ran 8 tests in 11.9s (1 classes, 16 at a time; slowest: Ambient 12s) / OK [ran] [tree 3d1eb91bb1e9] (2026-10-29T11:42:55Z)
- (audit intent) `self-review (pace: no subagents): the wait sits before the tree and cached-pass reads, so a check started beside a live one reuses its pass; only _cmd_check writes gates_running and nothing calls it in-process, so it never waits on itself; a dead or other-tree marker (fm ship scratch) is ignored by gates_live(here=True); tests that set a live marker never run fm check after it` → each member's red test now passes (another, spending, changed_mid) [tree 3d1eb91bb1e9] (2026-10-29T11:42:55Z)
- (audit edge) `self-review (pace: no subagents): the wait sits before the tree and cached-pass reads, so a check started beside a live one reuses its pass; only _cmd_check writes gates_running and nothing calls it in-process, so it never waits on itself; a dead or other-tree marker (fm ship scratch) is ignored by gates_live(here=True); tests that set a live marker never run fm check after it` → a 10-minute wait timeout leaves two runs, and each clears only its own marker; a gate that writes files starts one ambient run of affected tests per check [tree 3d1eb91bb1e9] (2026-10-29T11:42:55Z)
## Log
- 2026-10-29T11:32:47Z created
- 2026-10-29T11:35:48Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_ambient -k another`
- 2026-10-29T11:35:48Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_risk -k spending`
- 2026-10-29T11:35:48Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_ambient -k changed_mid`
- 2026-10-29T11:35:49Z focused
- 2026-10-29T11:43:21Z done
- 2026-10-29T11:43:23Z committed 24df1292 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1967 [FEATURE M, done, 3 steps] round 12: fm check waits for an ambient run, ambient skips during gates, loop round respects pace — lesson: A slowdown reason from fmbu…
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- T-1377 [FEATURE M, done, 3 steps] A false-done benchmark: impossible tasks where the only right outcome is saying it can't b — lesson: A benchmark of honesty needs an ob…
- decision 2026-10-23: Usage pace: subagents paused at 75% weekly usage with 27% of the week gone; work continues in the main thread, security items first (T-1751, T-1749)…
## Why not caught
none: T-1964/T-1965 tested the ambient side of 'one suite at a time' only; the full-check pair, the risk list order and the mid-gate edit had no test until now
## Lessons
- A shared marker written by one process and cleared by any is only safe with one writer at a time: wait for the live owner, and clear only your own
## Plan gaps
- failed first: step 1 T-1971: A second full fm check started while another runs on the same tree overwrites its gates_ru
- failed first: step 2 T-1972: Fm risk lists the guard rules that spend risk first: today the 8-row collision list showed
- failed first: step 3 T-1973: An edit made while full gates run gets no ambient run (T-1965) and no pass (T-1963), and n
## Files touched
- plugin/tests/test_ambient.py
- plugin/tests/test_risk.py
- plugin/lib/fmcli.py
- plugin/lib/fmrisk.py
- CHANGELOG.md
- MASTER.md
