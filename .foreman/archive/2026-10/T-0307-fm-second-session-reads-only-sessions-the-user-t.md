---
id: T-0307
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T18:06:11Z
updated: 2026-10-04T18:07:58Z
base: 2b2de0a4cfc88976606f291abd476f659c73cea6
base_tree: 885d8d2c5c43ea10aa3c377c0838cd35de7d5d80
verified: strong
---
# fm second session reads only sessions the user typed in, not SDK/print-mode runs (escape from T-0276)
## Raw request
> fm second session reads only sessions the user typed in, not SDK/print-mode runs (escape from T-0276)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a newer SDK transcript is skipped and the newest interactive one is read — verify with `python3 plugin/tests/run.py -p 'test_second*.py' -k Interactive`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, then skip sdk-entrypoint transcripts in fmsecond
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p 'test_second*.py' -k Interactive` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Session 0s) / FAILED (1 classes) [ran] [tree c7d2833485b6] (2026-10-04T18:06:23Z)
- (step 1) `python3 plugin/tests/run.py -p 'test_second*.py' -k Interactive` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Session 0s) / OK [ran] [tree df54083efc6c] (2026-10-04T18:06:31Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (26 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.0    32.1     150  [0] / SessionEnd                  28.1    30.6     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 09:59 UTC; python3 plugin/tests/run.py → exit 0 · Ran 821 tests in [ran] [tree 386858a03196] (2026-10-04T18:07:52Z)
- (ac 1) `python3 plugin/tests/run.py -p 'test_second*.py' -k Interactive` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Session 0s) / OK [ran] [tree 386858a03196] (2026-10-04T18:07:57Z)
- (audit intent) `self: red→green on test_second Interactive (the SDK run's prompt was read; now the older interactive session is); second, night and hooks suites pass; fm check exit 0` → the night shift's false capture T-0306 came from an sdk-py background review transcript; this project holds 124 sdk-py, 1 sdk-cli and 8 cli transcripts, so the newest file is usually not the user's [tree 386858a03196] (2026-10-04T18:07:57Z)
- (audit edge) `self: red→green on test_second Interactive (the SDK run's prompt was read; now the older interactive session is); second, night and hooks suites pass; fm check exit 0` → transcripts with no entrypoint (older Claude Code) still count as interactive; at most the 20 newest files are scanned; none typed in → 'no earlier session to review' as before [tree 386858a03196] (2026-10-04T18:07:57Z)
- (audit self) `self: red→green on test_second Interactive (the SDK run's prompt was read; now the older interactive session is); second, night and hooks suites pass; fm check exit 0` → no findings [tree 386858a03196] (2026-10-04T18:07:57Z)
## Log
- 2026-10-04T18:06:11Z created
- 2026-10-04T18:06:11Z focused
- 2026-10-04T18:07:57Z done
- 2026-10-04T18:07:58Z committed 503ecf8 (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0298-review-1: Findings
- research T-0276-review-1: Verdict: changes needed.** One race and one privacy gap are verified. One self-triggering effect is likely but I did not confirm it by running …
- T-0291 [SECURITY M, done, 3 steps] Session review security fixes: export --out confined to the project, second-session captures always ask, judge staging … — lesson: A f…
- research T-0264-review-1: All three reviews are below. Only fmhooks, fmcore, fmcli, fmplugins and fmevolve were read. I did not run the tests or the PreToolUse hook. [st…
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
## Lessons
- Transcripts in a project folder aren't all the user's: SDK and print-mode runs land there too, tagged by entrypoint (cli vs sdk-*)
## Files touched
- plugin/tests/test_second.py
- plugin/lib/fmsecond.py
- CHANGELOG.md
