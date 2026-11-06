---
id: T-0038
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py]
depends_on: []
source: self
created: 2026-09-26T19:31:32Z
updated: 2026-09-26T21:15:56Z
base: dfa585a44dbf9ac65b2d3e4151e008e691206d47
---
# Stop evidence gate: attribute completion words to the nearest '▸ Step N/M' header
## Raw request
> Stop evidence gate: a completion word under a finished step's '▸ Step N/M' header (Foreman output style) counts as a claim about the current step; claims_done should attribute claims to the nearest preceding step header, not only the 60 chars before the word
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a claim under a finished step's header doesn't fire the gate for the current step; a claim under the current step's header still does
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_hooks, then claims_done honours the nearest preceding step header
## Resume here
## Docs impact
## Verification evidence
- (step 1) `fm check: python3 -m unittest discover -s plugin/tests -q; fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · 4 passed: python3 -m unittest discover -s plugin/tests -q → exit 0 · Ran 397 tests in 89.198s / OK; fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (24 pass, 2 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                28.8    33.3     150  [0] / SessionEnd                  26.0    27.0     150  [0] [ran] [tree 8e08d5c32db5] (2026-09-26T21:15:46Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -k claims test_hooks` → exit 0 · Ran 3 tests in 1.629s / OK [ran] [tree 8e08d5c32db5] (2026-09-26T21:15:48Z)
- (audit self) `self checklist: diff re-read, all claims_done callers (only _evidence_gate), header regex anchored on the reply format's ▸ marker, false-negative case (current-step claim left under an old header) accepted: the gate is a once-per-step nudge` → no findings; 397 tests OK [tree a20578947701] (2026-09-26T21:15:56Z)
## Log
- 2026-09-26T19:31:32Z created
- 2026-09-26T19:55:13Z planned from capture
- 2026-09-26T21:11:14Z user approved core in Claude Code's permission prompt
- 2026-09-26T21:11:19Z focused
- 2026-09-26T21:15:56Z done
## Follow-ups captured
