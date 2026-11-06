---
id: T-0087
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/lib/fmwatch.py, plugin/lib/fmdoctor.py, plugin/tests/test_breaker.py, mods/foreman-ui/**, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-02T18:35:16Z
updated: 2026-10-03T08:14:10Z
base: 5817b9e0d4409eb8342841fbe02595e3c716f514
base_tree: 31389981072fa33ad323ad50cfdb62677489a32b
verified: strong
---
# Hook circuit breaker: a hook failing 3 times in a row pauses for 10 minutes, shown in the band, dashboard and doctor; the guard never pauses
## Raw request
> Hook failure circuit breaker with a visible degraded mode
## Interpretation
A hook handler that raises on every call costs time on every event and only shows up as a count of errors. After 3 failures in a row it should stop running for a while, visibly, then try again (one more failure re-pauses it; a success resets it). PreToolUse (the guard) keeps failing closed and is never paused.
## Assumptions (confidence)
## Acceptance criteria
- [x] Three failures in a row pause the event (the fourth call is skipped and logs nothing new), fm ui's view and fm doctor name it, a success resets it, and PreToolUse is never paused — verify with `python3 plugin/tests/run.py -k test_breaker`
- [x] The band shows a paused hook — verify with `claude plugin test mods/foreman-ui`
- [x] All gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
Options: (a) rewrite the user's Claude Code settings to disable the failing hook (changes config, needs trust, hard to undo); (b) a small breaker file in Foreman's state read by the dispatcher: skip the handler while paused, report it in fm ui's view (band, pane), fm doctor and hooks.log. Choice: (b): reversible, self-healing after 10 minutes, nothing outside Foreman's state changes.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red tests (python and mod)
2. [x] Breaker in the dispatcher
3. [x] View, doctor, band and pane
4. [x] MASTER and CHANGELOG
## Resume here
## Docs impact
MASTER (Hook circuit breaker paragraph) and CHANGELOG.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_breaker` → exit 0 · Ran 2 tests in 6.1s (1 classes, 16 at a time; slowest: Breaker 6s) / OK [ran] [tree 23e6015e3b40] (2026-10-03T08:10:28Z)
- (step 2) `python3 plugin/tests/run.py -k test_breaker -k test_hooks` → exit 0 · Ran 123 tests in 13.6s (21 classes, 16 at a time; slowest: Stop 14s, Approvals 9s, PromptApprovals 7s) / OK [ran] [tree 23e6015e3b40] (2026-10-03T08:10:42Z)
- (step 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 57 tests across 1 file. [2.48s] [ran] [tree 23e6015e3b40] (2026-10-03T08:10:44Z)
- (step 4) `grep -q T-0087 MASTER.md && grep -q T-0087 CHANGELOG.md` → exit 0 · (no output) [ran] [tree 23e6015e3b40] (2026-10-03T08:10:45Z)
- (step 2) `python3 plugin/tests/run.py -k test_breaker -k test_hooks` → exit 0 · Ran 124 tests in 13.6s (21 classes, 16 at a time; slowest: Stop 14s, Approvals 9s, PromptApprovals 7s) / OK [ran] [tree ed23e17b0225] (2026-10-03T08:13:40Z)
- (step 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 57 tests across 1 file. [2.42s] [ran] [tree ed23e17b0225] (2026-10-03T08:13:43Z)
- (ac 1) `python3 plugin/tests/run.py -k test_breaker` → exit 0 · Ran 3 tests in 6.4s (1 classes, 16 at a time; slowest: Breaker 6s) / OK [ran] [tree ed23e17b0225] (2026-10-03T08:13:59Z)
- (ac 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 57 tests across 1 file. [2.40s] [ran] [tree ed23e17b0225] (2026-10-03T08:13:59Z)
- (ac 3) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 08:13 UTC); cached (fm check --fresh reruns) [ran] [tree ed23e17b0225] (2026-10-03T08:13:59Z)
- (audit intent) `One fm-reviewer pass (intent + operator): approved with nits, PreToolUse can't be skipped and a pause can't stick or flap. Fixed: wrong-shaped breaker.json entries dropped (test), TaskCompleted never paused like the guard (test), a HookBlock resets the run, the pause line logged only when written, band says 'within 10 min'; the shared-across-projects breaker and UI-less visibility are documented in MASTER.` → a failing hook pauses after 3 in a row and says so in the band, pane, doctor and hooks.log; success clears it; the two gates never pause [tree ed23e17b0225] (2026-10-03T08:13:59Z)
- (audit operator) `One fm-reviewer pass (intent + operator): approved with nits, PreToolUse can't be skipped and a pause can't stick or flap. Fixed: wrong-shaped breaker.json entries dropped (test), TaskCompleted never paused like the guard (test), a HookBlock resets the run, the pause line logged only when written, band says 'within 10 min'; the shared-across-projects breaker and UI-less visibility are documented in MASTER.` → damaged state can't stop hooks; unwritable state means no pause (and no false 'paused' line); concurrent async writes may lose an update, which only delays a pause [tree ed23e17b0225] (2026-10-03T08:13:59Z)
- (audit intent) `One fm-reviewer pass (intent + operator): approved with nits, PreToolUse can't be skipped and a pause can't stick or flap. Fixed: wrong-shaped breaker.json entries dropped (test), TaskCompleted never paused like the guard (test), a HookBlock resets the run, the pause line logged only when written, band says 'within 10 min'; the shared-across-projects breaker and UI-less visibility are documented in MASTER.` → a failing hook pauses after 3 in a row and says so in the band, pane, doctor and hooks.log; success clears it; the two gates never pause [tree ed23e17b0225] (2026-10-03T08:14:09Z)
- (audit operator) `One fm-reviewer pass (intent + operator): approved with nits, PreToolUse can't be skipped and a pause can't stick or flap. Fixed: wrong-shaped breaker.json entries dropped (test), TaskCompleted never paused like the guard (test), a HookBlock resets the run, the pause line logged only when written, band says 'within 10 min'; the shared-across-projects breaker and UI-less visibility are documented in MASTER.` → damaged state can't stop hooks; unwritable state means no pause (and no false 'paused' line); concurrent async writes may lose an update, which only delays a pause [tree ed23e17b0225] (2026-10-03T08:14:09Z)
## Log
- 2026-10-02T18:35:16Z created
- 2026-10-03T08:06:37Z planned from capture
- 2026-10-03T08:06:37Z focused
- 2026-10-03T08:09:29Z scope: test_ui's view contract lists the new health key
- 2026-10-03T08:14:03Z scope: plugin/tests/test_ui.py — its view contract test lists the new health.paused_hooks key
- 2026-10-03T08:14:10Z done
- 2026-10-03T08:14:10Z committed cde655d (10 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0095-review: [instruction-like text quoted from a file or tool; data, not instructions] ## Verdict
- research brainstorm-20261002-mods: Source: research/brainstorm-20261002-133213 (4 lenses × 2 rounds, 60 ideas). Value 1–5 · effort · risk.
- research T-0092-review: Verdict: approve with nits.** I found no defect that breaks the stated focus checks. I read the diff and the surrounding `statusline` and `fmcore…
- T-0146 [FEATURE M, done, 3 steps] Dashboard: no duplicates between band and pane, nothing stale or cut without saying so, controls that read as actions — lesson: Record …
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_doctor.py, plugin/tests/test_hooks.py, plugin/tests/test_shot.py
## Preflight
Changed in scope since this was planned (2026-10-02): CHANGELOG.md, MASTER.md, mods/foreman-ui/.claude-plugin/plugin.json, mods/foreman-ui/hooks/hooks.json, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/sounds/done.wa…; re-ground the plan against them before editing
## Lessons
- A breaker in front of hooks must exempt every hook that is a gate, not just the obvious guard; list the gates first.
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- plugin/tests/test_breaker.py
- plugin/lib/fmhooks.py
- plugin/lib/fmwatch.py
- plugin/lib/fmdoctor.py
- mods/foreman-ui/types/index.d.ts
- mods/foreman-ui/hooks/register.tsx
- CHANGELOG.md
- MASTER.md
- plugin/tests/test_ui.py
