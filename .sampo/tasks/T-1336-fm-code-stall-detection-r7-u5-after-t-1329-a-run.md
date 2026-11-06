---
id: T-1336
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-21T03:47:22Z
updated: 2026-10-21T17:02:21Z
base: 70c03f02ed196302a1137296810dac91c4322849
base_tree: 56bbb25c9ca60f5aa10397bbf44f45c6e9d1cb29
plan0_at: 2026-10-21T13:40:16Z
plan0_scope: []
verified: strong
---
# fm code names a stall: a CLI turn silent for FM_STALL s (default 120) gets a stalled event with its likely cause, and the TUI shows how long since it was last heard
## Raw request
> fm code stall detection (R7+U5, after T-1329): a runner silent for N s gets a 'stalled' event with a named cause (no bytes since launch, a terminal prompt, rate-limit text, idle on CPU); the status bar always shows 'last heard Ns ago' and a silent run shows a card naming the wait with w wait / k kill / m switch runner; fm code why ID explains a run
## Interpretation
The nixie run 'just isn't doing anything': live progress (T-1329) shows tool use and a heartbeat, but nothing says a turn is stuck or why. After FM_STALL seconds with no output at all, say so once, with the likely cause read from what the CLI printed last.
## Assumptions (confidence)
## Acceptance criteria
- [x] a fake worker that prints a line then sleeps past FM_STALL gets one stalled event naming 'silent'; one that prints nothing names 'no output since launch'; one whose last line asks (y/n) names a prompt; one that prints a rate-limit message names the limit — verify with `python3 plugin/tests/run.py test_code_worker`
- [x] the TUI draws a stalled event as a warning line in Activity and the status bar says how long since the CLI was last heard — verify with `python3 plugin/tests/run.py test_code_tui`
## Non-goals
## Approach (options → choice → why)
Options: (A) the reader thread's sink keeps the time and tail of the last bytes; the idle beat turns into one stalled event per silence past FM_STALL, cause from the tail (no output since launch; a question or (y/n) prompt; rate or usage limit text; else silent N s) (chosen: same thread as the other live events, no new process); (B) a watchdog thread per turn (two emitters); (C) ps/CPU sampling of the child (platform-specific; later). The TUI shows 'last heard N s ago' from working events and a warn line for stalled; s already stops. fm code why ID and the w/k/m card are captured as follow-ups.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: fake workers that go silent four ways; the TUI's stalled line and last-heard status
2. [x] fmcode: last-bytes time and tail in the sinks, stalled events with a cause from the beat; TUI line and status
3. [x] Docs
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_a_turn_ -k test_a_quiet_turn -k test_a_stall_is` → ✗ exit 1 · Ran 9 tests in 15.0s (4 classes, 16 at a time; slowest: Worker 15s, UnexplainedSpend 0s, TaskAt 0s) / FAILED (2 classes) [ran] [tree cae1403479f9] (2026-10-21T13:48:30Z)
- (ac 1) `python3 plugin/tests/run.py test_code_worker 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|FAILED|^OK" | head -20` → exit 0 · Ran 58 tests in 107.2s (1 classes, 16 at a time; slowest: Worker 107s) / OK [ran] [tree 01dd4205bf0b] (2026-10-21T13:54:43Z)
- (step 2) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 59 tests in 69.5s (1 classes, 16 at a time; slowest: Worker 69s) / OK [ran] [tree 746c73efd5bf] (2026-10-21T13:56:40Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 96 tests in 7.0s (14 classes, 16 at a time; slowest: Fuzz 7s, Command 5s, Events 3s) / OK [ran] [tree 746c73efd5bf] (2026-10-21T13:56:48Z)
- (step 3) `python3 -c "import sys; sys.path.insert(0, 'plugin/lib'); import fmcode; assert 'FM_STALL' in fmcode.EVENTS['stalled'] and 'silent' in fmcode.EVENTS['working']"` → exit 0 · (no output) [ran] [tree 746c73efd5bf] (2026-10-21T13:56:52Z)
- (step 1) `python3 plugin/tests/run.py test_code_worker test_code_tui` → exit 0 · Ran 159 tests in 181.1s (15 classes, 16 at a time; slowest: Worker 181s, Command 32s, Fuzz 32s) / OK [ran] [tree eeec304e30d8] (2026-10-21T16:55:41Z)
- (ac 1) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 61 tests in 145.5s (1 classes, 16 at a time; slowest: Worker 145s) / OK [ran] [tree eeec304e30d8] (2026-10-21T16:58:34Z)
- (ac 2) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 98 tests in 25.2s (14 classes, 16 at a time; slowest: Command 25s, Fuzz 23s, Events 9s) / OK [ran] [tree eeec304e30d8] (2026-10-21T16:58:34Z)
- (audit intent) `self: read the builder's diff on the merged tree; one stalled event per silence (keyed on the last byte's time), cause read from the last 2 KB with escape codes stripped and lines made printable, the last line redacted; pump passes (heard, tail) to on_idle through the same exception guard; both suites pass merged with T-1343 and T-1354` → four silence kinds each named (launch, prompt, limit, silent); the TUI's warning line and 'last heard' status [tree eeec304e30d8] (2026-10-21T16:58:34Z)
- (audit adversary) `self: read the builder's diff on the merged tree; one stalled event per silence (keyed on the last byte's time), cause read from the last 2 KB with escape codes stripped and lines made printable, the last line redacted; pump passes (heard, tail) to on_idle through the same exception guard; both suites pass merged with T-1343 and T-1354` → the stalled text is redacted and made printable before it reaches a terminal [tree eeec304e30d8] (2026-10-21T16:58:34Z)
- (audit edge) `self: read the builder's diff on the merged tree; one stalled event per silence (keyed on the last byte's time), cause read from the last 2 KB with escape codes stripped and lines made printable, the last line redacted; pump passes (heard, tail) to on_idle through the same exception guard; both suites pass merged with T-1343 and T-1354` → words-based cause: a CLI printing 'quota' in passing reads as limited (ponytail note); the planner's stderr isn't read, so a prompt printed there isn't seen [tree eeec304e30d8] (2026-10-21T16:58:34Z)
- (audit operator) `self: read the builder's diff on the merged tree; one stalled event per silence (keyed on the last byte's time), cause read from the last 2 KB with escape codes stripped and lines made printable, the last line redacted; pump passes (heard, tail) to on_idle through the same exception guard; both suites pass merged with T-1343 and T-1354` → FM_STALL sets the wait; working events carry 'silent' [tree eeec304e30d8] (2026-10-21T16:58:34Z)
- (audit maintainer) `self: read the builder's diff on the merged tree; one stalled event per silence (keyed on the last byte's time), cause read from the last 2 KB with escape codes stripped and lines made printable, the last line redacted; pump passes (heard, tail) to on_idle through the same exception guard; both suites pass merged with T-1343 and T-1354` → stall_cause is a pure function with its own unit test; the w/k/m card and fm code why are T-1373 [tree eeec304e30d8] (2026-10-21T16:58:34Z)
## Log
- 2026-10-21T03:47:22Z created
- 2026-10-21T13:39:11Z planned from capture
- 2026-10-21T13:39:52Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1336.builder.md
- 2026-10-21T13:40:15Z focused
- 2026-10-21T16:35:42Z merged worktree-agent-a52eb9c3bca2960ce (6 file(s))
- 2026-10-21T16:35:43Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a52eb9c3bca2960ce
- 2026-10-21T16:52:27Z focused
- 2026-10-21T16:55:42Z scope: CHANGELOG.md — its line
- 2026-10-21T17:02:18Z done
- 2026-10-21T17:02:21Z committed 4305d519 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-fm-code-catalogue: Source: research/brainstorm-20261020-222518 (fm ideas, 10 lenses, 4 rounds, 3 deepened; 522 distinct ideas). Grounded in two halve…
- research mission-20261020-222446.pack: super improve fm code, make it genuinely amazing: launch it as an app like claude (fm code with no request), able to manage ANY CL…
- research mission-20261020-222446: Request: super improve fm code, make it genuinely amazing: launch it as an app like claude (fm code with no request), able to manage AN…
- decision 2026-10-21: fm code's no-setup default picks only a runner whose read-only mode is verified here (claude); codex/gemini plan only when named, with a note
## Lessons
- Read a stall's cause from the same reader thread that drains the output: it already has the last bytes and their time, so no second watcher is needed
## Plan gaps
- failed first: step 1 Failing tests: fake workers that go silent four ways; the TUI's stalled line and last-heard status
## Files touched
- plugin/tests/test_code_worker.py
- plugin/tests/test_code_tui.py
- plugin/lib/fmcore.py
- plugin/lib/fmmodels.py
- plugin/lib/fmcode.py
- plugin/lib/fmcodetui.py
- CHANGELOG.md
