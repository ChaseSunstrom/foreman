**Verdict:** approve with nits. PreToolUse can never be paused, and the pause cannot get stuck or flap. The findings below are all MEDIUM or LOW.

**Findings**

1. MEDIUM — `plugin/lib/fmhooks.py:78-79` — The breaker entry is read and used outside the `try`. If `breaker.json` holds valid JSON of the wrong shape, every non-PreToolUse hook crashes before any handler runs. Examples are `{"Stop": "x"}` (`str.get` raises AttributeError) and `{"Stop": {"until": "x"}}` (the `>` comparison raises TypeError). Nothing ever rewrites the file, so Stop, SessionStart and the rest fail on every call until someone deletes it. `paused_hooks()` at line 59 has the same TypeError when `until` is a string, which crashes `fm doctor` and `fm ui`. Fix: coerce entries in `breaker()`, keeping only dicts with numeric `fails` and `until`, and treat anything else as `{}`. There is no corrupt-file test. Confidence: high. Truncated or non-JSON files are handled correctly by the `except` at line 53.

2. MEDIUM — `plugin/lib/fmhooks.py:50, 66` — The breaker is global, in `c.state_dir()/logs`. One project's bad brief that makes Stop fail three times pauses Stop, SessionStart and the rest for every project and session for 10 minutes. The band and doctor show a pause, but they don't say which project's input caused it. Fix: key the entry by project or event, or document it as global. Confidence: medium, since I did not confirm that `state_dir()` is shared across projects.

3. MEDIUM — `plugin/lib/fmhooks.py:79-80, 1427` — A pause fails open on a safety gate. While TaskCompleted is paused, `task_completed`'s evidence refusal (the `HookBlock` at line 1427) does not run. Completion with no step evidence then passes silently. The same silence applies to Stop drive, SessionStart context and PostToolUse evidence and touch recording. The band and the pane's hooks line show this only when foreman-ui is running. Without foreman-ui, only `fm doctor` shows it. Fix: tell the user in the hook's own output channel, or exempt TaskCompleted, or note it in the docs. Confidence: high for the behaviour, medium for the severity.

4. LOW — `plugin/lib/fmhooks.py:87-91` — A `HookBlock` is neither a success nor a failure. It does not clear `fails`, so the sequence fail, fail, block, fail pauses "in a row" even though a block happened in between. Fix: call `_breaker_set(event, None)` when `state` is non-empty before printing the block message. Confidence: high.

5. LOW — `mods/foreman-ui/hooks/register.tsx:1211-1214` — The band text hardcodes "failed 3 times in a row and runs again in 10 min". After 9 minutes it still says 10 minutes. Fix: send `until` or the remaining minutes in the view, or say "for up to 10 min". The doctor text ("10 min after its last failure") is accurate. Confidence: high.

6. LOW — `plugin/lib/fmhooks.py:65-67, 97-99` — When `breaker.json` is unwritable, `_breaker_set` swallows the OSError and the pause is never persisted. The code then logs "paused for 10 min … runs again at HH:MM" anyway. Doctor and the band then show no pause, and the hook keeps running and failing. Fix: have `_breaker_set` return a success flag and log the pause line only when the write landed. Confidence: high.

**Acceptance criteria**
- Three failures pause an event, the fourth call logs nothing, `fm ui` and `fm doctor` name it, a success resets it, and PreToolUse is never paused: met by the code, covered by `test_breaker`. I did not run the tests.
- The band shows a paused hook: met by the new foreman-ui test and the `register.tsx` change. I did not run it.
- All gates pass: not verifiable from the code.

**Operator:** can PreToolUse be skipped? No. The event check at line 75 runs before any breaker read, and a corrupt `breaker.json` cannot touch it. After a pause the first retry succeeds or re-pauses on one more failure, so a pause cannot get stuck. Concurrent async hooks can lose an update, which is acknowledged in the `ponytail:` comment and harmless.

- intent: changes needed (nit-level: findings 3 and 4 on the "visible degraded mode" and "in a row" meaning)
- operator: changes needed (findings 1, 2, 5 and 6)

**Not checked:** the adversary, edge and maintainer lenses, and the test run.
