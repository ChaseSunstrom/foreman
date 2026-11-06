---
id: T-0189
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmreplay.py,plugin/lib/fmcli.py,plugin/tests/test_replay.py,CHANGELOG.md,MASTER.md]
depends_on: []
source: user
created: 2026-10-03T19:13:11Z
updated: 2026-10-03T19:18:24Z
base: c67bca7ff617250e12c0dd450fb8ae9c771d987b
base_tree: aa2faea47d3baa3158902a4260e57e50b3852e4c
verified: strong
---
# fm replay: the guard replayed on the real commands of recent sessions, verdict changes reported, a gate when the guard changes
## Raw request
> fm replay: the guard replayed on the real commands of recent sessions, verdict changes reported, a gate when the guard changes
## Interpretation
Brainstorm round 4's top idea (four lenses): guard false positives were this session's main friction and two real bypasses surfaced only by accident while grounding them; nothing checks a guard change against the commands Claude really runs.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm replay reports newly blocked and newly allowed real commands and accepts a baseline — verify with `python3 plugin/tests/run.py -k test_replay`
## Non-goals
## Approach (options → choice → why)
A: fm replay reads Bash tool calls (command + cwd) from Claude Code's session logs under ~/.claude/projects (last 14 days, newest first, up to 5000 distinct), runs each through fmguard.check with no grants in its own folder, and compares the verdicts with the last accepted baseline (state/guard-replay.json: hashes and verdicts only); it lists newly blocked and newly allowed commands (redacted) and exits 1 on any change until --accept; a project gate scoped to plugin/lib/fmguard.py. B (rejected): a fixed hand-written corpus — the T-0160 differential test already is one, and it never saw the forms Claude actually writes.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test (red)
2. [x] fmreplay.py and the command
3. [x] the gate, docs, audit
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md (guard limits: fm replay)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_replay` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Replay 0s) / FAILED (1 classes) [ran] [tree d6575e70ab9c] (2026-10-03T19:13:27Z)
- (step 2) `python3 plugin/tests/run.py -k test_replay` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Replay 0s) / OK [ran] [tree d827c1c86389] (2026-10-03T19:13:51Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.3    32.3     150  [0] / SessionEnd                  28.9    29.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 19:08 UTC; python3 plugin/tests/run.py → e [ran] [tree c0db97db81c2] (2026-10-03T19:18:15Z)
- (ac 1) `python3 plugin/tests/run.py -k test_replay` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Replay 0s) / OK [ran] [tree c0db97db81c2] (2026-10-03T19:18:24Z)
- (audit intent) `self: the test (changed verdicts reported both ways, accept rebaselines, no command text in the baseline) and a real run over 5000 commands in 7 s that found two false positives` → a guard change is now checked against the commands Claude really runs, as the round-4 brainstorm's top idea asked; its first run already found two false positives (T-0190) [tree c0db97db81c2] (2026-10-03T19:18:24Z)
- (audit operator) `self: the test (changed verdicts reported both ways, accept rebaselines, no command text in the baseline) and a real run over 5000 commands in 7 s that found two false positives` → commands are read only in memory from the user's own session logs; the baseline keeps a hash and a verdict per command; listed examples are redacted and cut to 140 characters; the gate runs only when fmguard.py changes (7 s); 'new to the corpus' moves as sessions are written and never fails the gate [tree c0db97db81c2] (2026-10-03T19:18:24Z)
## Log
- 2026-10-03T19:13:11Z created
- 2026-10-03T19:13:11Z focused
- 2026-10-03T19:18:24Z done
- 2026-10-03T19:18:24Z committed 9665e80 (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261003-round4: 127 new ideas (6 lenses x 2 rounds, past the 152 of rounds 1-3). Grounded against the code and this session.
- decision 2026-10-03: Round 4 slate: guard replay corpus (M) and a mod version check in fm doctor (S) first; four followups to the inbox
- T-0178 [SECURITY M, done, 3 steps] Guard: a heredoc starts only outside quotes — a quoted heredoc marker hid every later line from the guard — lesson: A false-positive r…
- T-0184 [RESEARCH M, done, 2 steps] Super-improve Foreman: round 4 brainstorm past the 152 earlier ideas, grounded slate — lesson: Count lenses per idea: the one four len…
- similar finished tasks took 2–3 steps
## Lessons
- Test a filter against its real traffic, not only its imagined attacks: 5000 real commands found in seconds two false positives that a week of hand-written cases had missed.
## Files touched
- plugin/tests/test_replay.py
- plugin/lib/fmreplay.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
