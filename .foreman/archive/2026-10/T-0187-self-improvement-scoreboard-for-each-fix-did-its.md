---
id: T-0187
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmfriction.py,plugin/tests/test_friction.py,CHANGELOG.md,MASTER.md]
depends_on: []
source: followup
created: 2026-10-03T19:12:03Z
updated: 2026-10-03T19:38:51Z
base: bfcfce892aa4f40e9bf5c990e52a4bc756b95c6d
base_tree: f1e8d2f2f2d09b4bee8b65e20d090c8714781a16
verified: strong
---
# Self-improvement scoreboard: the friction digest rechecks each earlier guard block with today's guard and shows the trend since the last pass
## Raw request
> Self-improvement scoreboard: for each fix, did its friction stop — brainstorm round 4, value 3
## Interpretation
The RSI loop (fm friction → subagent → self tasks) can't tell whether a fix removed its friction: the digest lists 'done since: T-0178' with no outcome. Give it the outcome: each guard block it lists is re-run through today's guard (the full command from the session's transcript), labelled 'today's guard allows it' (a fix cleared it) or 'still blocks'; and a trend line compares this window's friction per 100 tool calls with the last pass's window.
## Assumptions (confidence)
## Acceptance criteria
- [x] digest labels cleared and still-blocking guard blocks, and shows the trend after a mark — verify with `python3 plugin/tests/run.py -k test_the_digest_rechecks_guard_blocks_and_shows_the_trend`
## Non-goals
## Approach (options → choice → why)
A (chosen): use what's recorded — the guard-block event's session id and command prefix find the full command and its folder in that session's transcript, fmreplay.verdicts rechecks it; fm friction --mark stores the closing window's counts so the next digest can show before → after. B (rejected): tasks carry the friction key they fix (fm capture --friction KEY) and the digest checks whether that key recurred after the close — precise, but needs a new flag and discipline the subagent's captures don't follow today, and guard fixes (most of the self tasks so far) are measured better by a recheck than by recurrence.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test (red)
2. [x] recheck guard blocks with today's guard; counts stored at mark; trend line
3. [x] gates, real digest, docs
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md (fm friction: recheck and trend)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_the_digest_rechecks_guard_blocks_and_shows_the_trend` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Friction 0s) / FAILED (1 classes) [ran] [tree 4f9376fbdf3f] (2026-10-03T19:36:11Z)
- (step 2) `python3 plugin/tests/run.py -k test_the_digest_rechecks_guard_blocks_and_shows_the_trend` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Friction 0s) / OK [ran] [tree c546be64a812] (2026-10-03T19:36:43Z)
- (step 2) `python3 plugin/tests/run.py -k test_the_digest_rechecks_guard_blocks_and_shows_the_trend` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Friction 0s) / OK [ran] [tree e7fee0a3a35f] (2026-10-03T19:37:07Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 2 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.0    32.8     150  [0] / SessionEnd                  28.1    29.7     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 19:08 UTC; python3 plugin/tests/run.py → e [ran] [tree e7fee0a3a35f] (2026-10-03T19:37:49Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 2 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.0    32.9     150  [0] / SessionEnd                  27.7    29.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 19:08 UTC; python3 plugin/tests/run.py → e [ran] [tree 58df7cf362ea] (2026-10-03T19:38:41Z)
- (ac 1) `python3 plugin/tests/run.py -k test_the_digest_rechecks_guard_blocks_and_shows_the_trend` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Friction 0s) / OK [ran] [tree 58df7cf362ea] (2026-10-03T19:38:51Z)
- (audit intent) `self: the test (a cleared block, a real one, the trend after a mark) and the real digest (the $D/$f block T-0190 fixed reads 'today's guard allows it'; the volt rm -rf block, a true block, 'still blocks')` → the loop asked 'did the fix remove its friction' with only titles to go on; now each guard block carries today's verdict and the trend compares windows per 100 tool calls [tree 58df7cf362ea] (2026-10-03T19:38:51Z)
- (audit edge) `self: the test (a cleared block, a real one, the trend after a mark) and the real digest (the $D/$f block T-0190 fixed reads 'today's guard allows it'; the volt rm -rf block, a true block, 'still blocks')` → no transcript left (rotated or another machine) → no word rather than a guess; non-Bash blocks skipped; a session id that isn't a plain id never reaches glob; a window with no tool calls shows no trend; the recheck uses no grants, so 'allows it' never comes from a standing yes [tree 58df7cf362ea] (2026-10-03T19:38:51Z)
- (audit operator) `self: the test (a cleared block, a real one, the trend after a mark) and the real digest (the $D/$f block T-0190 fixed reads 'today's guard allows it'; the volt rm -rf block, a true block, 'still blocks')` → the real digest takes 0.9 s scanning the sessions it names; the mark counts without rechecking [tree 58df7cf362ea] (2026-10-03T19:38:51Z)
## Log
- 2026-10-03T19:12:03Z created
- 2026-10-03T19:35:48Z planned from capture
- 2026-10-03T19:35:48Z focused
- 2026-10-03T19:38:51Z done
- 2026-10-03T19:38:51Z committed ba9e34f (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0172 [FEATURE S, done, 3 steps] Guard blocks log a short redacted command, and the friction digest shows one per kind — lesson: A self-improvement loop needs the raw e…
- T-0125 [FEATURE M, done, 4 steps] Recursive self-improvement loop: fm friction digests Foreman's own friction since the last pass, fm next calls for a pass every N close…
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- likely tests for the scope: plugin/tests/test_friction.py
## Lessons
- A loop that fixes its own friction needs the outcome, not the title: re-running the old input through today's code answers 'did it work' directly, where recurrence counts need weeks of data.
## Files touched
- plugin/tests/test_friction.py
- plugin/lib/fmfriction.py
- CHANGELOG.md
- MASTER.md
