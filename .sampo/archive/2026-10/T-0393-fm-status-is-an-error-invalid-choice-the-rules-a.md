---
id: T-0393
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T02:27:53Z
updated: 2026-10-09T02:29:43Z
base: 71cc04dbfbf6fa5330106afad99d580882609d3d
base_tree: 7af099637b214a66f91f0bdae1b34d6f81c6f594
verified: strong
---
# fm status is an error (invalid choice; the rules and /foreman:status say 'status'): make it an alias of fm state
## Raw request
> fm status is an error (invalid choice; the rules and /foreman:status say 'status'): make it an alias of fm state
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm status prints what fm state prints — verify with `python3 plugin/tests/run.py -k test_status_is_state`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first, then the alias
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k test_status_is_state` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Help 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree d2a9143dbc49] (2026-10-09T02:28:18Z)
- `python3 plugin/tests/run.py -k test_status_is_state` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Help 0s) / FAILED (1 classes) [ran] [tree d2a9143dbc49] (2026-10-09T02:28:18Z)
- `python3 plugin/tests/run.py -k test_status_is_state` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Help 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 93125c0710a7] (2026-10-09T02:28:37Z)
- `python3 plugin/tests/run.py -k test_status_is_state` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Help 0s) / OK [ran] [tree 93125c0710a7] (2026-10-09T02:28:37Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (27 pass, 4 warn, 0 fail) (slower: 14.4 s vs a usual 7.1 s); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.7    34.3     150  [0] / SessionEnd                  28.8    30.7     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/ [ran] [tree e6cf10f7a402] (2026-10-09T02:29:42Z)
- (ac 1) `python3 plugin/tests/run.py -k test_status_is_state` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Help 0s) / OK [ran] [tree e6cf10f7a402] (2026-10-09T02:29:43Z)
- (audit intent) `self: alias shares state's parser and flags; help tier lists it once; fm status run on the real project` → fm status prints what fm state prints (test); fm help lists it [tree e6cf10f7a402] (2026-10-09T02:29:43Z)
- (audit edge) `self: alias shares state's parser and flags; help tier lists it once; fm status run on the real project` → fm status --brief/--line work (same parser) [tree e6cf10f7a402] (2026-10-09T02:29:43Z)
- (audit self) `self: alias shares state's parser and flags; help tier lists it once; fm status run on the real project` → no findings [tree e6cf10f7a402] (2026-10-09T02:29:43Z)
## Log
- 2026-10-09T02:27:53Z created
- 2026-10-09T02:27:53Z focused
- 2026-10-09T02:29:43Z done
- 2026-10-09T02:29:43Z committed 7b8aa97 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Security Review Skill (skills/playbooks/references/security/security-review.md)
- research T-0274-review-1: Verdict: approve with nits.** `note_flakes` can't change the exit code or hide a failure. The findings are a regex false-name problem, one miss…
- research brainstorm-pass-2: Source: research/brainstorm-20261004-020314 (4 lenses × 2 rounds, past pass 1 and three earlier lists; 82 new titles). Pack: pass 1's results…
- research T-0269-review-2: Verdict:** changes needed. I read the code only and ran nothing, so each "not blocked" below comes from tracing the code and is unexecuted.
## Files touched
- plugin/tests/test_help.py
- plugin/lib/fmcli.py
- CHANGELOG.md
