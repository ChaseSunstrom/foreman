---
id: T-0873
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T14:11:51Z
updated: 2026-10-15T14:26:18Z
base: 427b8f473597cf0c1bb2760074f7d3aaaa241bf6
base_tree: 8110229c22e6949b7043e1d7aea613478debe359
verified: strong
---
# Help text carries no ticket ids: strip (T-NNNN) from fm's command help, with a test that fails if one comes back
## Raw request
> Help text carries no ticket ids: strip (T-NNNN) from fm's command help, with a test that fails if one comes back
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] no fm help or -h text contains a T-NNNN id — verify with `python3 plugin/tests/run.py test_help`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test, then strip the ids
## Resume here
<!-- auto -->
- 2026-10-15T14:17:12Z step 1/1: Failing test, then strip the ids
- git: foreman/build; 2 uncommitted: README.md, INSTALL.md
## Docs impact
none: help text
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_help` → exit 0 · Ran 4 tests in 0.7s (2 classes, 16 at a time; slowest: Help 1s, PromptApprovals 1s) / OK [ran] [tree 6bfe441055f7] (2026-10-15T14:24:26Z)
- `python3 plugin/tests/run.py test_help` → ✗ exit 1 · Ran 4 tests in 1.0s (2 classes, 16 at a time; slowest: Help 1s, PromptApprovals 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 6bfe441055f7] (2026-10-15T14:24:28Z)
- `python3 plugin/tests/run.py test_help` → exit 0 · Ran 4 tests in 0.7s (2 classes, 16 at a time; slowest: Help 1s, PromptApprovals 1s) / OK [ran] [tree 6bfe441055f7] (2026-10-15T14:24:28Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py — commit it through a task, or git checkout it back / fm doctor: OK (34 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.8    34.2     150  [0] / SessionEnd                  30.3    31.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui [ran] [tree 6bfe441055f7] (2026-10-15T14:26:13Z)
- (ac 1) `python3 plugin/tests/run.py test_help` → exit 0 · Ran 4 tests in 0.7s (2 classes, 16 at a time; slowest: Help 1s, PromptApprovals 1s) / OK [ran] [tree 6bfe441055f7] (2026-10-15T14:26:17Z)
- (audit self) `self: ids stripped at display (parser help and fm help) so source comments keep provenance; a test walks every command's -h, fm --help and fm help --all` → no findings [tree 6bfe441055f7] (2026-10-15T14:26:17Z)
## Log
- 2026-10-15T14:11:51Z created
- 2026-10-15T14:16:55Z focused
- 2026-10-15T14:17:12Z paused: focus moved to T-0872
- 2026-10-15T14:23:30Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-15T14:23:30Z focused
- 2026-10-15T14:26:17Z done
- 2026-10-15T14:26:18Z committed 443eac5 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- T-0781 [FEATURE S, done, 2 steps] Sessions are named after their task: SessionStart and UserPromptSubmit set sessionTitle when the active task changes — lesson: a rename…
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
- research t0015-final-check: T-0015 final adversary check of f602cb0: HIGH `fm ask … -h` printed argparse help to the hook's stdout ahead of the JSON decision (PreToolUse…
## Behaviour lock
test_help and the full suite ran green on this tree before the first edit (fm check cached pass from T-0872's run)
## Lessons
- Strip internal ids where text is shown, not where it's written: provenance stays in the source
## Files touched
- plugin/tests/test_help.py
- plugin/lib/fmcli.py
