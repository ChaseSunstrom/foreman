---
id: T-0197
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: [CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-03T19:50:48Z
updated: 2026-10-03T19:51:13Z
base: 5e06eaf6c8f62958889d28961180e560b1ab50dc
base_tree: ff77e8352a91f2480eeaf46bc3fae25f1fb41fc5
verified: ok
---
# The test-suite gate skips a CHANGELOG-only change
## Raw request
> The test-suite gate skips a CHANGELOG-only change
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] after a pass, a CHANGELOG-only edit skips run.py — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] scope gate 5 to the paths tests read; show a changelog-only edit skips it
## Resume here
## Docs impact
## Verification evidence
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (26 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · skipped: nothing under plugin/**, install.sh changed since its pass at 19:50 UTC; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 19:50 UTC; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed [ran] [tree 0b80892925cf] (2026-10-03T19:50:54Z)
- (ac 1) `fm check` → exit 0 · ✓ all 6 gates passed on this exact tree already (run at 19:50 UTC); cached (fm check --fresh reruns) [ran] [tree 0b80892925cf] (2026-10-03T19:51:13Z)
- (audit self) `self-review: the paths list covers every file outside plugin/ the tests read (MASTER/README/BUILD_PROMPT via test_docs and test_docsdrift, the install scripts via test_cli/test_doctor); tests use CHANGELOG.md only inside scratch repos (grep); fm doctor stays unscoped since it reads the installed state` → no findings [tree 0b80892925cf] (2026-10-03T19:51:13Z)
## Log
- 2026-10-03T19:50:48Z created
- 2026-10-03T19:50:48Z focused
- 2026-10-03T19:51:13Z done
- 2026-10-03T19:51:13Z committed 8ee47b1 (1 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0126 [FEATURE M, done, 3 steps] Gates by path: a gate can declare the paths it covers and is skipped when none changed since its last pass — lesson: A cache entry deri…
- research T-0126-review: Verdict:** changes needed. Two gates can be skipped when a covered file changed (renames, and the wrapped-around skip chain). One skipped pass is…
- research T-0088-review: Verdict:** approve with nits. I read the diff and the `fmcore.py`/`fmcli.py` code it calls into. I ran no tests, so the three verify commands in …
- research brainstorm-20260926-super3-slate: Build: G1 evidence that proves nothing (0 tests ran / no tests collected) is recorded as a failure · G2 pre-audit flags test t…
## Measurements
gate re-run after a CHANGELOG-only edit: before ≈ 28–38 s (fm doctor 5.9 s + run.py 22–32 s, both re-ran) → after ≈ 6 s (fm doctor only; run.py 'skipped: nothing under … changed'); every task edits CHANGELOG after its last code pass
## Files touched
- CHANGELOG.md
