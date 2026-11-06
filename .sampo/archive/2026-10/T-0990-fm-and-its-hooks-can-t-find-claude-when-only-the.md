---
id: T-0990
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py,plugin/tests/test_core.py,CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-15T23:21:41Z
updated: 2026-10-15T23:26:25Z
base: a8ac36915a89058b871d9641a50a48ed3c1d8971
base_tree: 1a19f7fe81e3cbcc48a57143c07b03f8ff7597ee
verified: strong
---
# fm and its hooks can't find claude when only the native install (~/.local/bin/claude) exists and PATH lacks ~/.local/bin: roundtrip gate, doctor scripts, fm run fail
## Raw request
> fm and its hooks can't find claude when only the native install (~/.local/bin/claude) exists and PATH lacks ~/.local/bin: roundtrip gate, doctor scripts, fm run fail
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with claude only in ~/.local/bin and not on PATH, fmcore puts ~/.local/bin on PATH; a claude already on PATH is left first — verify with `python3 plugin/tests/run.py -k NativeClaude`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] PATH fix in fmcore
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k NativeClaude` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: NativeClaude 0s) / FAILED (1 classes) [ran] [tree a5a51547ff3b] (2026-10-15T23:21:54Z)
- (step 2) `python3 plugin/tests/run.py -k NativeClaude` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: NativeClaude 0s) / FAILED (1 classes) [ran] [tree 01e9d5936ff2] (2026-10-15T23:22:03Z)
- (step 2) `python3 plugin/tests/run.py -k NativeClaude` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: NativeClaude 0s) / OK [ran] [tree 7a64f682afb4] (2026-10-15T23:22:25Z)
- (step 2) `python3 plugin/tests/run.py -k NativeClaude` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: NativeClaude 0s) / OK [ran] [tree 5a39e56c5188] (2026-10-15T23:25:58Z)
- (step 1) `python3 plugin/tests/run.py -k NativeClaude` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: NativeClaude 0s) / FAILED (1 classes) [ran] [tree 607a880955ce] (2026-10-15T23:26:14Z)
- (step 2) `python3 plugin/tests/run.py -k NativeClaude` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: NativeClaude 0s) / OK [ran] [tree 0410d08e470d] (2026-10-15T23:26:22Z)
- (ac 1) `python3 plugin/tests/run.py -k NativeClaude` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: NativeClaude 0s) / OK [ran] [tree 0410d08e470d] (2026-10-15T23:26:22Z)
- (audit edge) `self: one PATH fix at fmcore import (every fm command and hook imports it), only when claude isn't on PATH and ~/.local/bin/claude is executable; the roundtrip gate passes through fm (17/17)` → a claude already on PATH stays first; no native install → PATH untouched; HOME unset → expanduser [tree 0410d08e470d] (2026-10-15T23:26:22Z)
- (audit adversary) `self: one PATH fix at fmcore import (every fm command and hook imports it), only when claude isn't on PATH and ~/.local/bin/claude is executable; the roundtrip gate passes through fm (17/17)` → only prepends the user's own ~/.local/bin, and only when no claude is found at all; a planted ~/.local/bin/claude already outranks nothing a user chose [tree 0410d08e470d] (2026-10-15T23:26:22Z)
- (audit self) `self: one PATH fix at fmcore import (every fm command and hook imports it), only when claude isn't on PATH and ~/.local/bin/claude is executable; the roundtrip gate passes through fm (17/17)` → no findings [tree 0410d08e470d] (2026-10-15T23:26:22Z)
## Log
- 2026-10-15T23:21:41Z created
- 2026-10-15T23:21:42Z focused
- 2026-10-15T23:26:24Z done
- 2026-10-15T23:26:25Z committed c61d072 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0855 [FIX M, done, 5 steps] A fresh install is clean and works from a shell: doctor passes and shows only problems, fm check finds the test runner,… — lesson: Walk thr…
- T-0785 [FEATURE S, done, 2 steps] fm doctor names the Foreman features the installed Claude Code is too old for — lesson: a probe for a setting must look where Foreman w…
- T-0368 [FIX M, done, 3 steps] fm and the hooks re-run under a supported Python when python3 is below 3.12.7 — lesson: Check the interpreter a remote Foreman really runs …
- decision 2026-10-15: Update Claude Code with its native installer (claude install latest → ~/.local/bin, which updates itself without root) and put ~/.local/bin first on…
- likely tests for the scope: plugin/tests/test_core.py
## Plan gaps
- failed first: step 1 failing test
- failed first: step 2 PATH fix in fmcore
## Files touched
- plugin/tests/test_core.py
- plugin/lib/fmcore.py
- CHANGELOG.md
