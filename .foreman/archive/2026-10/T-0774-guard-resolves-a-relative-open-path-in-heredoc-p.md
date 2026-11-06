---
id: T-0774
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py]
depends_on: []
source: discovered
created: 2026-10-14T15:54:05Z
updated: 2026-10-14T16:16:56Z
group: guard coverage gaps
base: 6fa82e459402dbdd86941a206bc9558c73dd33e8
base_tree: 1cb62933d809f100a7fe13eaf672088837450f51
verified: strong
---
# Guard: heredoc python started by 'cd DIR && python3 -' resolves its relative open() targets in DIR only
## Raw request
> Guard resolves a relative open() path in heredoc python against the session cwd, not the command's own 'cd <scratchpad> &&' (python3 - <<EOF open('clusters.py','w') after cd scratchpad was refused as a write to the foreman home)
## Interpretation
_proved_writes resolves each relative open() target against the session cwd and every cd target in the command (fmguard.py:1234), so 'cd <scratchpad> && python3 - <<EOF open("x.py","w")' was refused as a write to the Foreman home. When the starter's only directory changes are 'cd D &&' links, python runs in D or not at all (_run_dir already computes D for sys.path), so D is the one base.
## Assumptions (confidence)
## Acceptance criteria
- [x] 'cd S && python3 - <<EOF open("x.py","w")' with S outside Foreman's home isn't a core write; 'cd S; python3 -', 'cd a; cd S && python3 -' and a variable cd still resolve against every base — verify with `cd plugin/tests && python3 -m unittest test_guard.InterpreterWrites`
## Non-goals
## Approach (options → choice → why)
Options: keep every base (false blocks); trust _run_dir always (a 'cd a; cd b && python3 -' runs in a/b if a exists, cwd/b otherwise: a miss); trust it only when the starter has no other cd/pushd/popd and every cd target is literal. Chose the last.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing guard test
2. [x] One base from a literal && cd chain
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_guard.InterpreterWrites.test_a_literal_cd_chain_picks_the_folder_python_writes_in` → ✗ exit 1 · Ran 1 test in 0.019s / FAILED (failures=1) [ran] [tree fe409f16c58d] (2026-10-14T16:11:27Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_guard.InterpreterWrites.test_a_literal_cd_chain_picks_the_folder_python_writes_in` → ✗ exit 1 · Ran 1 test in 0.056s / FAILED (failures=1) [ran] [tree ad6494c4ad76] (2026-10-14T16:11:40Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_guard test_guard_diff` → exit 0 · Ran 84 tests in 11.888s / OK [ran] [tree f69da5f41d4e] (2026-10-14T16:12:27Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard.InterpreterWrites` → exit 0 · Ran 9 tests in 0.180s / OK [ran] [tree f69da5f41d4e] (2026-10-14T16:12:27Z)
- `cd plugin/tests && python3 -m unittest test_guard.InterpreterWrites.test_a_literal_cd_chain_picks_the_folder_python_writes_in` → ✗ exit 1 · Ran 1 test in 0.032s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree f69da5f41d4e] (2026-10-14T16:12:28Z)
- `cd plugin/tests && python3 -m unittest test_guard.InterpreterWrites.test_a_literal_cd_chain_picks_the_folder_python_writes_in` → exit 0 · Ran 1 test in 0.047s / OK [ran] [tree f69da5f41d4e] (2026-10-14T16:12:28Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_guard test_guard_diff` → exit 0 · Ran 84 tests in 4.928s / OK [ran] [tree 1b9fa94e43dd] (2026-10-14T16:14:34Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard.InterpreterWrites` → exit 0 · Ran 9 tests in 0.121s / OK [ran] [tree 1b9fa94e43dd] (2026-10-14T16:14:34Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard.InterpreterWrites` → exit 0 · Ran 9 tests in 0.120s / OK [ran] [tree 1b9fa94e43dd] (2026-10-14T16:16:55Z)
- (audit adversary) `self: diff read; _chain_dir returns one folder only when every python starter changes folder solely by cd LIT && links to absolute, ~, ./ or ../ targets and the rest of the command is nothing but the heredocs' end lines; otherwise every named folder counts as before` → fm-reviewer found a MEDIUM (a cd the regex can't see on another line: "cd", \cd, source); fixed by allowing only end lines outside the starters; the reproducer and source/pushd/cd -/variable/semicolon forms are in the test; replay corpus: 0 newly allowed [tree 1b9fa94e43dd] (2026-10-14T16:16:55Z)
- (audit edge) `self: diff read; _chain_dir returns one folder only when every python starter changes folder solely by cd LIT && links to absolute, ~, ./ or ../ targets and the rest of the command is nothing but the heredocs' end lines; otherwise every named folder counts as before` → cd - (OLDPWD) and CDPATH lookups are excluded by the target-prefix rule; different folders across starters fall back [tree 1b9fa94e43dd] (2026-10-14T16:16:55Z)
- (audit self) `self: diff read; _chain_dir returns one folder only when every python starter changes folder solely by cd LIT && links to absolute, ~, ./ or ../ targets and the rest of the command is nothing but the heredocs' end lines; otherwise every named folder counts as before` → no findings [tree 1b9fa94e43dd] (2026-10-14T16:16:55Z)
## Log
- 2026-10-14T15:54:05Z created
- 2026-10-14T16:03:27Z planned from capture
- 2026-10-14T16:11:08Z focused
- 2026-10-14T16:14:35Z review (adversary, fm-reviewer): MEDIUM — a folder change the regex can't see ("cd", \cd, source, eval) on another line let _chain_dir pick the wrong folder; fixed: the rest of the command may hold only the heredocs' end lines, else every named folder counts as before; reproducer added to the test
- 2026-10-14T16:16:56Z done
- 2026-10-14T16:16:56Z committed ac84803 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- T-0175 [SECURITY L, done, 3 steps] Guard: writes through a variable are checked — known NAME=literal values and $HOME resolve write, copy and cd targets (&& chains too);…
- research T-0286-review-1: Changes needed. I found no new hole that the `cd` prefix itself opens. The `cd` chain does make four existing parse mismatches reachable from a…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar past tasks were L: consider --tier L
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- a guard relaxation that trusts 'nothing else changes X' must whitelist what the rest may be, not blacklist the spellings it knows
## Plan gaps
- failed first: step 1 Failing guard test
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
