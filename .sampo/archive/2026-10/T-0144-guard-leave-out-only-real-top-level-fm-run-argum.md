---
id: T-0144
type: SECURITY
tier: L
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, mods/foreman-ui/**, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-03T06:05:38Z
updated: 2026-10-03T06:12:47Z
base: 762fab1001123ecf792135be4d14409270fdc8d9
base_tree: 6fadfad13a8fb6557f52807d5dd055256c8b62a5
verified: ok
---
# Guard: leave out only real top-level fm --run arguments from the interpreter claude-check (a fake --run in a heredoc or -c body hid code); mod rows clean every escape sequence
## Raw request
> Guard: leave out only real top-level fm --run arguments from the interpreter claude-check (a fake --run in a heredoc or -c body hid code); mod rows clean every escape sequence
## Interpretation
Two automated security findings. HIGH: _interp_code removed every regex match of --run "…"/'…' from the whole command, heredoc and -c bodies included, so code could carry a fake --run quote that swallowed its own claude plugin call, or pass the call as a --run argument to python itself. MEDIUM: foreman-ui strips only CSI colour codes from shell output; OSC, other escapes, C1 controls and bidi overrides reach Text (the engine refuses control characters, so the row falls back, but the cleaning should be whole).
## Assumptions (confidence)
## Acceptance criteria
- [x] a fake --run quote inside a heredoc, inside a -c body, or as a non-fm argument no longer hides claude plugin code; heredoc + fm task evidence --run "claude plugin test …" still passes — verify with `python3 plugin/tests/run.py -p test_guard.py`
- [x] shell output lines, the shown command and diff lines drop OSC/CSI/C1 escape sequences and bidi overrides — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
A) span-level: strip a --run span only when it starts at shell top level (quote scan of the heredoc-stripped text) in a simple command whose word is fm (after wrappers), and append heredoc bodies verbatim; everything uncertain is kept, so errors fail closed. B) rebuild the code from shell tokens minus fm --run values: loses shell-level quotes the claude regex needs (node -e … "claude plugin install" as argv would pass). C) never strip: blocks the common heredoc + fm --run "claude plugin test" command. Choice A. Mod: one exported clean() (CSI, OSC, other ESC sequences, C0/C1 controls, bidi overrides, tabs) used by outputSummary, the shell row's command and changedLines.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests for the three bypasses and for escape cleaning
2. [x] _interp_code strips only top-level fm --run spans outside heredoc bodies; kit clean() used for output, command and diff
3. [x] gates, one reviewer pass over all five lenses
## Resume here
## Docs impact
CHANGELOG entry; MASTER guard limits paragraph
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_guard.py -k reads_only_the_code; scratchpad/t144_check.py` → red first (heredoc fake --run: 'unexpectedly None'); the check script shows all three were hidden by the old strip (2026-10-03T06:06:25Z)
- (step 2) `python3 plugin/tests/run.py -p test_guard.py && claude plugin test mods/foreman-ui` → guard OK; mod 46 pass 0 fail (clean: OSC/CSI/ESC/C1/bidi gone, \r keeps the last segment) (2026-10-03T06:07:07Z)
- (step 3) `fm check; reviewer pass (research T-0144-review)` → gates 5/5; reviewer: MEDIUM $'…' desync + LOW clean gaps, both fixed test-first, plus a sibling <<\EOF bypass found while tracing; scratchpad t144_check2.py shows both were hidden by the first fix (2026-10-03T06:12:33Z)
- (ac 1) `python3 plugin/tests/run.py -p test_guard.py` → exit 0 · Ran 44 tests in 0.1s (15 classes, 16 at a time; slowest: GitDestructive 0s, Authorization 0s, InterpreterWrites 0s) / OK [ran] [tree 61eac4ed3744] (2026-10-03T06:12:47Z)
- (ac 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 46 tests across 1 file. [2.01s] [ran] [tree 61eac4ed3744] (2026-10-03T06:12:47Z)
- (audit intent) `one fm-reviewer pass (research T-0144-review) plus my own trace` → both automated findings addressed — fake --run in heredoc/-c bodies and as an interpreter argument no longer hides claude plugin code; mod rows clean every escape form [tree 61eac4ed3744] (2026-10-03T06:12:47Z)
- (audit adversary) `one fm-reviewer pass (research T-0144-review) plus my own trace` → reviewer found $'…' desync (MEDIUM) and clean() gaps (LOW); tracing found <<\EOF unrecognised heredoc bypass; all three fixed test-first, the two guard ones shown hidden-before/seen-now by scratchpad t144_check2.py. Remaining limit (documented in MASTER): obfuscated spellings aren't recognised, the guard is a speed bump [tree 61eac4ed3744] (2026-10-03T06:12:47Z)
- (audit edge) `one fm-reviewer pass (research T-0144-review) plus my own trace` → <<< here-strings excluded from the heredoc count, arithmetic << makes it read everything (fail closed), CRLF lines keep their text, an unterminated OSC/DCS swallows to line end as a terminal does, abbreviated --ru flags are never left out (read whole) [tree 61eac4ed3744] (2026-10-03T06:12:47Z)
- (audit operator) `one fm-reviewer pass (research T-0144-review) plus my own trace` → the everyday heredoc + fm task evidence/finish --run "claude plugin test …" still passes (test ok case); everything uncertain reads the whole command, so the worst case is a false block with the usual fm ask path [tree 61eac4ed3744] (2026-10-03T06:12:47Z)
- (audit maintainer) `one fm-reviewer pass (research T-0144-review) plus my own trace` → _HEREDOC_START shared by _heredocs and the check; _top_level documented as wrong only towards False; clean() is the one sanitizer for every drawn line [tree 61eac4ed3744] (2026-10-03T06:12:47Z)
## Log
- 2026-10-03T06:05:38Z created
- 2026-10-03T06:05:38Z focused
- 2026-10-03T06:12:33Z scope: MASTER.md — the guard's interpreter-check description, updated with fmguard.py as the pre-audit asked
- 2026-10-03T06:12:47Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0018-r4-edge: id":"8a23d3ef-86ad-40e5-8b8c-023d98996326","isSidechain":true,"agentId":"a885e6176c24d785f","message":{"model":"claude-sonnet-5","id":"msg_011CfS…
- research t0018-r5-adversary: HIGH — `~/.claude/foreman/plugin/lib/fmguard.py:188-198` (`_protected_roots`) and `:146-147` (`_CRED_DIRS`/`_CRED_FILES`) — tree-w…
- T-0141 [FEATURE M, done, 3 steps] Clean tool rows: Edit/Write results as Foreman rows with a compact coloured diff; shell commands wrap under themselves — lesson: Snapsh…
- research T-0120-review: Verdict
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_guard.py, plugin/tests/test_shot.py
## Lessons
- A text strip that excludes spans must be anchored to the parser's view of the command (top level, real fm call), and must give up — read everything — wherever the scan can't follow the shell
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- mods/foreman-ui/tests/foreman-ui.test.tsx
- MASTER.md
- CHANGELOG.md
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
