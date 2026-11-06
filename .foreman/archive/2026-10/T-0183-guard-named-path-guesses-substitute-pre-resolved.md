---
id: T-0183
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py,plugin/tests/test_guard.py,CHANGELOG.md,MASTER.md]
depends_on: []
source: discovered
created: 2026-10-03T19:01:34Z
updated: 2026-10-03T19:08:54Z
base: 0a467937d0f4feec38a0bbd3c16a7d4187935fcc
base_tree: 3b008ccd1c63a4fc974331a253f2a4b02bc23274
verified: strong
---
# Guard: unknown-target guesses come from the command's own words, pair up across unknown parts, and know a literal set once before any branch
## Raw request
> Guard: named-path guesses substitute pre-resolved absolute words into every unknown part (cp src/$f $D/$f in a for loop guessed <abs>/<abs> under state/, a never-grantable state-direct block); guess with words as written, and know a NAME=literal assigned once in a branchy command's straight prefix — evidence: T-0182's sync command blocked
## Interpretation
T-0182's sync command (D=<dir>; for f in …; do cp src/$f $D/$f; done; … fm task finish … --lens '…'): D is a literal set once, but the for loop makes the command branchy so D counts as unknown; the guesses then took the word 'state' from fm's text arguments and put that one absolute path into both unknown parts, guessing <fhome>/state/<fhome>/state, a never-grantable state-direct block.
## Assumptions (confidence)
## Acceptance criteria
- [x] a literal set before a loop is known, fm text gives no guesses, unknown parts pair up — verify with `python3 plugin/tests/run.py -k test_guesses_come_from_the_command_and_pair_up`
- [x] real bash agrees — verify with `python3 plugin/tests/run.py -k test_every_form_that_runs_a_dangerous_call_is_blocked`
## Non-goals
## Approach (options → choice → why)
A: (1) guess words come from the command with fm's arguments blanked (_mask_fm, as the interpreter gate does); (2) words as written are substituted per unknown part, the first two parts paired (each part up to 64 words), later parts a neutral name, then the whole guess resolved; (3) in a branchy command, NAME=literal assignments in its straight top-level prefix (before any branch, pipe, subshell or keyword) are known when the name is written bare nowhere else and nothing can set names indirectly. B (rejected): drop the guesses for multi-part targets — reopens the T-0175 hole for for-loop writes.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests (red)
2. [x] masked words, paired parts, prefix literals
3. [x] gates, docs, audit
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md (guard limits: guesses and prefix literals)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_guesses_come_from_the_command_and_pair_up` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Core 0s) / FAILED (1 classes) [ran] [tree bbb82f80c55e] (2026-10-03T19:06:41Z)
- (step 2) `python3 plugin/tests/run.py -k test_guesses_come_from_the_command_and_pair_up` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Core 0s) / OK [ran] [tree 51f12a1e410d] (2026-10-03T19:07:33Z)
- (step 2) `python3 plugin/tests/run.py -k test_every_form_that_runs_a_dangerous_call_is_blocked` → exit 0 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: GuardAgainstBash 1s) / OK [ran] [tree 51f12a1e410d] (2026-10-03T19:07:43Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py` → exit 0 · 5 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.1    32.4     150  [0] / SessionEnd                  28.2    30.0     150  [0]; claude plugin test mods/foreman-ui → exit 0 · 0 fail / Ran 58 tests across 1 file. [2.55s]; python3 plugin/tests/run.py → exit 0 · Ran 604 tests in 22.4s (1 [ran] [tree 51f12a1e410d] (2026-10-03T19:08:35Z)
- (ac 1) `python3 plugin/tests/run.py -k test_guesses_come_from_the_command_and_pair_up` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Core 0s) / OK [ran] [tree aa2faea47d3b] (2026-10-03T19:08:53Z)
- (ac 2) `python3 plugin/tests/run.py -k test_every_form_that_runs_a_dangerous_call_is_blocked` → exit 0 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: GuardAgainstBash 1s) / OK [ran] [tree aa2faea47d3b] (2026-10-03T19:08:53Z)
- (audit intent) `self-review against the T-0161/T-0175 soundness rules; the bash differential test; 604 tests; the original blocked command now passes` → the sync loop that blocked this session passes, fm's prose no longer feeds guesses, and a two-part loop write (for a … for b … > $a/$b) into core is now caught by pairing, which the old one-word guess missed [tree aa2faea47d3b] (2026-10-03T19:08:53Z)
- (audit adversary) `self-review against the T-0161/T-0175 soundness rules; the bash differential test; 604 tests; the original blocked command now passes` → the prefix literal is used only when the name is written bare exactly once in the whole command and no builtin can set names indirectly (both tested: set twice in the loop, eval before it); the prefix ends at the first branch, pipe, subshell, group, keyword, substitution or backtick and at a separator before it, so a pipeline or skipped && never contributes; a quote that holds such a token only shortens the prefix; guesses for a third unknown part use a neutral name (documented); worst case 91 ms for two 80-word parts, capped at 48 words a part [tree aa2faea47d3b] (2026-10-03T19:08:53Z)
## Log
- 2026-10-03T19:01:34Z created
- 2026-10-03T19:06:32Z planned from capture
- 2026-10-03T19:06:32Z focused
- 2026-10-03T19:08:53Z done
- 2026-10-03T19:08:54Z committed c67bca7 (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0175 [SECURITY L, done, 3 steps] Guard: writes through a variable are checked — known NAME=literal values and $HOME resolve write, copy and cd targets (&& chains too);…
- research T-0161-review: Verdict: changes needed.** `_track_vars` still has bypasses, and one of them is the same class T-0161 set out to close. I traced each through `_s…
- T-0177 [SECURITY M, done, 3 steps] Guard: glob and brace write targets are checked as bash expands them — lesson: A path check is only as good as the path bash will real…
- T-0180 [SECURITY M, done, 3 steps] Guard: a standing or trusted yes covers a finding's plain path only — relative shell writes named by their real path, annotated detail…
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- A guess generator is only as safe as its vocabulary: feeding it the command's prose (fm's text) and pre-resolved paths produced impossible guesses that the never-grantable state-direct category turned into a hard stop.
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
- MASTER.md
