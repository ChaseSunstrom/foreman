---
id: T-2016
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T16:53:17Z
updated: 2026-10-29T17:03:31Z
base: 102e58e7e582f18efe97c85ce9d7d8a1eafc9fba
base_tree: ff7ba731c472b529fe3c718a35ed5854bcfa0df1
plan0_at: 2026-10-29T16:53:18Z
plan0_scope: []
verified: strong
---
# fm next loads every brief once, and fm builds only the parser of the command it runs
## Raw request
> fm next and the prompt hook load every brief once per call, not up to five times
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] next_for and cmd_next load briefs once — verify with `python3 plugin/tests/run.py test_nudges -k loads_briefs_once`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] next_for loads once and passes it on; cmd_next shares its load with unanswered_asks and lanes.stopped; the prompt hook shares state_dict's load with next_for (measure fm next before/after)
2. [x] main builds only the parser of the command it runs (~80 ms of 214 subparsers); a test proves every command's partial parser matches the full one
## Resume here
<!-- auto -->
- 2026-10-29T16:56:56Z steps 2/2 done
- git: foreman/build; 4 uncommitted: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_cli.py, plugin/tests/test_nudges.py
- touched since last checkpoint: /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/next_t.py, plugin/tests/test_nudges.py, plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/tests/test_cli.py
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_nudges -k loads_briefs_once 2>&1 | grep -E "Assertion|^OK|FAIL|Error" | head -4` → ✗ exit 1 · FAILED (failures=1) / FAILED (1 classes) [ran] [tree bff367e4395e] (2026-10-29T16:54:34Z)
- (step 1) `python3 plugin/tests/run.py test_nudges -k loads_briefs_once` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: OneLoad 0s) / OK [ran] [tree 17b20773c52e] (2026-10-29T16:55:00Z)
- (step 2) `python3 plugin/tests/run.py test_cli -k ParserOnce 2>&1 | grep -E "Error|^OK|FAIL|^AssertionError|Ran" | head -6` → exit 0 · Ran 2 tests in 0.9s (1 classes, 16 at a time; slowest: ParserOnce 0s) / OK [ran] [tree d6351447b629] (2026-10-29T16:56:55Z)
- (step 2) `python3 plugin/tests/run.py test_cli -k builds_only_its_command` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: ParserOnce 0s) / OK [ran] [tree d6351447b629] (2026-10-29T16:58:30Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmcore.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, ; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                41.4    43.6     150  [0] / SessionEnd                  36.3    39.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 782077dede7e] (2026-10-29T17:02:43Z)
- (ac 1) `python3 plugin/tests/run.py test_nudges -k loads_briefs_once` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: OneLoad 0s) / OK [ran] [tree 782077dede7e] (2026-10-29T17:02:52Z)
- (audit intent) `self: read the whole diff; the parser test builds every command alone and compares it to the full parser, options and nested subcommands included` → fm next loads briefs once (test counts calls) and each run builds one command's parser; a typo, bare fm or leading option still gets the full parser [tree 782077dede7e] (2026-10-29T17:02:52Z)
- (audit edge) `self: read the whole diff; the parser test builds every command alone and compares it to the full parser, options and nested subcommands included` → -p=x, a bare -p, aliases, fm help and fm which (full parser) checked; a skipped parser that is iterated fails the every-command test [tree 782077dede7e] (2026-10-29T17:02:52Z)
- (audit self) `self: read the whole diff; the parser test builds every command alone and compares it to the full parser, options and nested subcommands included` → no findings [tree 782077dede7e] (2026-10-29T17:02:52Z)
## Log
- 2026-10-29T16:53:17Z created
- 2026-10-29T16:53:17Z focused
- 2026-10-29T16:55:01Z numbers (S/st, 1199 briefs): fm next min 187 -> 172 ms, median 194 -> 181 ms
- 2026-10-29T16:56:02Z set title=fm next loads every brief once, and fm builds only the parser of the command it runs
- 2026-10-29T16:58:39Z scope: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_cli.py, plugin/tests/test_nudges.py, CHANGELOG.md
- 2026-10-29T17:03:15Z done
- 2026-10-29T17:03:16Z committed fadef947 (5 files)
- 2026-10-29T17:03:31Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- T-1697 [FEATURE M, done, 3 steps] Hooks name the Foreman skill to load: Next lines and stage notes say which skill (or playbook) fits, within the prompt budget — lesson:…
- T-1873 [FEATURE M, done, 3 steps] Fm scene gallery: every built-in scene on one contact sheet, each with a one-line caption — lesson: A playbook has a token ceiling (tes…
- decision 2026-10-23: T-1623: the five UI contract rules are written down from what the UI playbooks already require: motion (reduced motion as its own path), contrast (p…
## Measurements
fm next min 187 → 143 ms, median 194 → 147 ms (1199 briefs)
## Plan gaps
- added late: main builds only the parser of the command it runs (~80 ms of 214 subparsers); a test proves every command's partial pa…
## Files touched
- plugin/tests/test_nudges.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/tests/test_cli.py
- CHANGELOG.md
