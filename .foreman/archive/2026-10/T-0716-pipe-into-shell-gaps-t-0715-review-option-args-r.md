---
id: T-0716
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T16:37:53Z
updated: 2026-10-09T16:53:45Z
base: d79af72a16c284133886fdac60b4a301d2dc1514
base_tree: b8fbafaa0e2476af01574467ed619bbf68e0ea43
verified: strong
---
# Pipe-into-shell gaps (T-0715 review): option args read as script (bash -o posix, python3 -
## Raw request
> Pipe-into-shell gaps (T-0715 review): option args read as script (bash -o posix, python3 -W ignore, node -r m, perl -I d), grouped or computed readers (| { bash; }, | (sh), | $SH), -c text that sources /dev/stdin; fail closed on unknown options
## Interpretation
Close the T-0715 review gaps so a shell or interpreter that runs piped-in text is refused: value-taking options misread as a script (bash -o posix, python3 -W ignore, node -r m, perl -I d, ruby -r x), bash -s with positional args, piped groups and wrappers ({ bash; }, (sh), env/exec/timeout), computed names (| $SH), and inline code that execs stdin (bash -c 'source /dev/stdin', python3 -c 'exec(sys.stdin.read())'). A positional only counts as a script when it looks like a path. Data readers stay allowed.
## Assumptions (confidence)
## Acceptance criteria
- [x] PipeIntoShell gaps refused, data readers allowed — verify with `python3 plugin/tests/run.py -p test_guard_pipes.py -k PipeIntoShell`
- [x] no new false positives on real commands — verify with `fm replay --days 30`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: the review's bypasses as PipeIntoShell rows
2. [x] model value options, -s, script-looking positionals, groups/wrappers, computed names, stdin-exec inline code
3. [x] replay real commands for false positives
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_guard_pipes.py -k PipeIntoShell` → ✗ exit 1 · Ran 2 tests in 0.1s (1 classes, 16 at a time; slowest: PipeIntoShell 0s) / FAILED (1 classes) [ran] [tree 65158d17b021] (2026-10-09T16:45:18Z)
- (step 2) `python3 plugin/tests/run.py -p test_guard_pipes.py -p test_guard.py -p test_safety.py` → exit 0 · Ran 101 tests in 2.8s (44 classes, 16 at a time; slowest: SecretsGate 2s, RuleIds 2s, RenderSanitizer 2s) / OK [ran] [tree 14bedc57b9cd] (2026-10-09T16:48:30Z)
- (step 2) `python3 plugin/tests/run.py -p test_guard_pipes.py -k PipeIntoShell` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: PipeIntoShell 0s) / OK [ran] [tree 8e1cd71c8441] (2026-10-09T16:52:25Z)
- (step 3) `fm replay --days 30` → exit 0 · 0 newly allowed (possible bypasses) / 232 new to the corpus [ran] [tree 8e1cd71c8441] (2026-10-09T16:52:52Z)
- (ac 1) `python3 plugin/tests/run.py -p test_guard_pipes.py -k PipeIntoShell` → exit 0 · Ran 2 tests in 0.1s (1 classes, 16 at a time; slowest: PipeIntoShell 0s) / OK [ran] [tree 4b1ed43100d4] (2026-10-09T16:53:44Z)
- (ac 2) `fm replay --days 30` → exit 0 · 0 newly allowed (possible bypasses) / 291 new to the corpus [ran] [tree 4b1ed43100d4] (2026-10-09T16:53:44Z)
- (audit adversary) `self adversary pass over _reads_stdin_code/_inline_runs_stdin: option values, -s, clusters (-eo, -Wignore), attached -c code, busybox applet, xargs placeholders, perl/ruby -n/-p loops, awk system, read loops; tightened the runner words after the replay (json.load, re.compile, literal_eval, quoted 'system') and the quoted $( ) tail` → 22 bypass rows from the review and my pass refused; known ceiling: inline code is pattern-matched (sed e, find -exec sh from stdin, a fd other than 0 slip), logged as a ponytail comment for the nested $( ) case [tree 4b1ed43100d4] (2026-10-09T16:53:44Z)
- (audit edge) `self adversary pass over _reads_stdin_code/_inline_runs_stdin: option values, -s, clusters (-eo, -Wignore), attached -c code, busybox applet, xargs placeholders, perl/ruby -n/-p loops, awk system, read loops; tightened the runner words after the replay (json.load, re.compile, literal_eval, quoted 'system') and the quoted $( ) tail` → 0 newly blocked / 0 newly allowed over 5,000 real commands; data readers (json.load, re.compile, ast.literal_eval, perl -ne print, awk print, | $GREP pat) stay allowed [tree 4b1ed43100d4] (2026-10-09T16:53:44Z)
- (audit self) `self adversary pass over _reads_stdin_code/_inline_runs_stdin: option values, -s, clusters (-eo, -Wignore), attached -c code, busybox applet, xargs placeholders, perl/ruby -n/-p loops, awk system, read loops; tightened the runner words after the replay (json.load, re.compile, literal_eval, quoted 'system') and the quoted $( ) tail` → no findings [tree 4b1ed43100d4] (2026-10-09T16:53:44Z)
## Log
- 2026-10-09T16:37:53Z created
- 2026-10-09T16:45:06Z focused
- 2026-10-09T16:48:23Z hypothesis: the replay's 16 new blocks are all json.load(sys.stdin) data readers matched by the 'load' word, which is now removed from _RUNS_IT; adding rows for json.load/re.compile/literal_eval (allowed) and perl -ne system / awk system / read-loop (refused) will pass and the replay will show 0 newly blocked
- 2026-10-09T16:50:46Z replay FP 1: inline python with the string 'system' (a quoted word, not a call); FP 2: a $( ) body parsed as '| $(grep -m1 ^# $f' (computed name, bare-word args) → computed names now take any positional as a script (| $GREP pat stays allowed), runner words in quotes don't count
- 2026-10-09T16:53:45Z done
- 2026-10-09T16:53:45Z committed e157abf (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0344-review: Verdict: changes needed.** I had no shell, so these are traced by reading `plugin/lib/fmguard.py` and the tests. I did not run any command. [stal…
- T-0369 [FIX M, done, 2 steps] Guard: pin the pipe proof's strictness (premise of a self-improvement finding was false) — lesson: Before widening a guard from a friction …
- T-0414 [FIX M, done, 3 steps] Guard: a data-reading python -c is judged by what runs before it — lesson: A parser that drops quoting can't be trusted about structure the…
- decision 2026-10-03: Self-approve T-0175 (L, guard): approach A
- similar past tasks were M: consider --tier M
- similar finished tasks took 2–3 steps
## Files touched
- plugin/tests/test_guard_pipes.py
- plugin/lib/fmguard.py
- CHANGELOG.md
