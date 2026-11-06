---
id: T-0190
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py,plugin/tests/test_guard.py,plugin/tests/test_guard_diff.py,CHANGELOG.md,MASTER.md]
depends_on: []
source: self
created: 2026-10-03T19:15:25Z
updated: 2026-10-03T19:20:48Z
base: 9665e8043a1eaa0391cf812774cd1d69f857d78e
base_tree: c0db97db81c253e544c920335428fc6e97f46ca1
verified: strong
---
# Guard: guesses never use a variable's own name; rm targets use literals set once before a branch
## Raw request
> Guard, found by fm replay: guess words include a variable's own name (S=…; cat > $S/x guessed '<cwd>/S/x', state-direct in a state folder), and rm targets don't use T-0183's prefix literals (S=<scratch> && rm -rf $S/x | … blocked rm-outside) — evidence: replay of 5000 real commands, 123 blocked
## Interpretation
fm replay's first run: S=<scratch>; cat > $S/x guessed '<cwd>/S/x' (the word S is the variable's name, split off its '='), a state-direct block from inside a state folder; and S=<scratch> && rm -rf $S/x | … stayed rm-outside because rm uses only straight-line values, not T-0183's prefix literals.
## Assumptions (confidence)
## Acceptance criteria
- [x] names aren't guesses and rm uses prefix literals — verify with `python3 plugin/tests/run.py -k test_replay_found_false_positives`
- [x] real bash agrees — verify with `python3 plugin/tests/run.py -k test_every_form_that_runs_a_dangerous_call_is_blocked`
## Non-goals
## Approach (options → choice → why)
A: guess words come from the text with NAME= prefixes removed; rm args take the prefix literals when the command is branchy (same conditions: set once at the top before any branch, written bare nowhere else, no builtin that sets names indirectly). B (rejected): special-case scratch paths in rm — the general rule is sound and covers more.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests and bash forms (red)
2. [x] names out of the words; rm prefix literals
3. [x] replay, gates, docs, audit
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md (guard limits)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_replay_found_false_positives` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Core 0s) / FAILED (1 classes) [ran] [tree b8c0eeb8d5d1] (2026-10-03T19:19:07Z)
- (step 1) `python3 plugin/tests/run.py -k test_every_form_that_runs_a_dangerous_call_is_blocked` → exit 0 · Ran 1 tests in 1.2s (1 classes, 16 at a time; slowest: GuardAgainstBash 1s) / OK [ran] [tree b8c0eeb8d5d1] (2026-10-03T19:19:08Z)
- (step 2) `python3 plugin/tests/run.py -k test_replay_found_false_positives` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Core 0s) / OK [ran] [tree a53c2490c7e3] (2026-10-03T19:19:18Z)
- (step 2) `python3 plugin/tests/run.py -k test_every_form_that_runs_a_dangerous_call_is_blocked` → exit 0 · Ran 1 tests in 1.2s (1 classes, 16 at a time; slowest: GuardAgainstBash 1s) / OK [ran] [tree a53c2490c7e3] (2026-10-03T19:19:19Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.4    33.0     150  [0] / SessionEnd                  28.7    29.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 19:08 UTC; python3 plugin/tests/run.py → e [ran] [tree a53c2490c7e3] (2026-10-03T19:20:36Z)
- (ac 1) `python3 plugin/tests/run.py -k test_replay_found_false_positives` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Core 0s) / OK [ran] [tree 27c8297f1053] (2026-10-03T19:20:48Z)
- (ac 2) `python3 plugin/tests/run.py -k test_every_form_that_runs_a_dangerous_call_is_blocked` → exit 0 · Ran 1 tests in 1.2s (1 classes, 16 at a time; slowest: GuardAgainstBash 1s) / OK [ran] [tree 27c8297f1053] (2026-10-03T19:20:48Z)
- (audit intent) `self: the replay gate's own first use — exactly the one intended real command flipped (rm of a scratchpad folder), nothing newly blocked; the bash differential test with four new rm forms` → both replay findings addressed; the second example (a write while cd'd inside the state folder) still blocks, since any unknown target there could be state [tree 27c8297f1053] (2026-10-03T19:20:48Z)
- (audit adversary) `self: the replay gate's own first use — exactly the one intended real command flipped (rm of a scratchpad folder), nothing newly blocked; the bash differential test with four new rm forms` → rm uses a prefix literal only under T-0183's conditions (set once at the top, before any branch; bare nowhere else; no indirect setter); the new bash forms (set again in a loop, a tilde before a pipe, printf -v, read in a while) are all still blocked in real bash; dropping NAME= from guess words leaves every value in [tree 27c8297f1053] (2026-10-03T19:20:48Z)
## Log
- 2026-10-03T19:15:25Z created
- 2026-10-03T19:18:58Z planned from capture
- 2026-10-03T19:18:58Z focused
- 2026-10-03T19:20:48Z done
- 2026-10-03T19:20:48Z committed e2b83c6 (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0183 [FIX M, done, 3 steps] Guard: unknown-target guesses come from the command's own words, pair up across unknown parts, and know a literal set once before any branc…
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- research T-0161-review: Verdict: changes needed.** `_track_vars` still has bypasses, and one of them is the same class T-0161 set out to close. I traced each through `_s…
- T-0175 [SECURITY L, done, 3 steps] Guard: writes through a variable are checked — known NAME=literal values and $HOME resolve write, copy and cd targets (&& chains too);…
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- A replay gate turns a guard change into a reviewable diff: the change's whole real-world effect was one line, which made accepting it a decision, not a hope.
## Files touched
- plugin/tests/test_guard.py
- plugin/tests/test_guard_diff.py
- plugin/lib/fmguard.py
- CHANGELOG.md
- MASTER.md
