---
id: T-1194
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-16T13:28:35Z
updated: 2026-10-16T14:55:32Z
base: 06d79fdc95ae06cc73eaf9ec4c3e5173c8939a6b
base_tree: 7267dea232e127534c898bb03e503c787117c6e3
plan0_at: 2026-10-16T14:30:39Z
plan0_scope: []
verified: strong
---
# Guard parses python -c code like quoted heredoc bodies before calling it Foreman-driving
## Raw request
> Guard: python3 -c code whose fm-module text sits only inside string literals is refused as driving Foreman (3x this week): parse -c code with ast like quoted heredoc bodies, keeping every real-import and dynamic-code refusal
## Interpretation
python3 -c CODE whose fm-module text sits only inside string literals (an edit or grep helper that names fmcore in a string) is refused as driving Foreman because -c code goes to the plain text match; quoted heredoc bodies already get an ast proof (_drives_fm, _python_units). Give -c code the same proof, and keep every refusal the proof can't clear: a real fm import that calls a writer, dynamic code (exec, eval, getattr, importlib, __import__, dunder walks), code that doesn't parse, a non-plain import, a run dir that shadows a module.
## Assumptions (confidence)
## Acceptance criteria
- [x] python3 -c code that names fm modules only in string literals is allowed; python3 -c 'import fmcore; fmcore.write_meta(...)' and exec/eval/__import__/importlib variants stay refused as core; the 3 mined refusals replay as allowed and fm replay --cases shows no loosened labelled block — verify with `python3 plugin/tests/run.py test_guard test_guard_cases test_replay`
## Non-goals
## Approach (options → choice → why)
Options: (a) _python_units also yields the CODE of python/python3 -c (after shlex split, with its starter) so _drives_fm's existing ast proof applies unchanged; (b) mask string literals with tokenize before the text match (no dynamic-code check, so exec('import fmcore') would pass: rejected); (c) allowlist known helper shapes (brittle). Choice: (a), the smallest change that reuses the audited proof; -c's run dir is the cwd (python -c puts '' first on sys.path), so the shadow check uses cwd.
## Risks and rollback
Plan review (fm second plan, verdict revise) folded in:
- Sinks: the existing proof already refuses _DYNAMIC names (exec, eval, compile, getattr, __import__, importlib, system, popen, Popen, run, call, check_output…) and any import outside _PLAIN_IMPORTS (subprocess, runpy, pickle). Add cases that prove it for -c: subprocess/os.system running fm from a string, runpy, compile, open(...).read() then exec, a literal split across implicit concatenation passed to exec.
- Extraction fails closed: only a literal CODE word counts. Cases: -Ic / -Bc combined flags, -c after -W x / -X y, python3.12 and /usr/bin/python3, two -c, and code that is not a literal ("$(cat f)", $VAR, backticks) which stays on the text match (refused).
- Run dir: python -c puts the cwd first on sys.path unless -I/-P/PYTHONSAFEPATH; any cd before it in the same command makes the run dir unknown (refuse when it imports a plain module there and the dir can't be checked), as the heredoc path does via _run_dir.
- Second caller: _python_units is also used at fmguard.py:1307 (the write-target proof). Decide explicitly whether -c units feed it; if they do, add a case that a -c write to a protected path is still refused.
- Labelled corpus: add the 3 mined -c refusals as permanent allow cases (fm guard wrong) and diff full fm replay output before and after, not only the labelled cases.
- Rollback: one function (_python_units) plus cases; git revert of the commit.
## Execution prompt
## Steps
1. [x] Labelled guard cases and tests first: literal-only -c allowed; real import, exec, __import__, importlib, unparsable, cwd shadow stay refused
2. [x] _python_units yields python -c code as a unit; rerun the guard suites and fm replay --cases
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_python_c_code_gets_the_same_proof` → ✗ exit 1 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / FAILED (1 classes) [ran] [tree e585d5a8e36f] (2026-10-16T14:34:11Z)
- (step 1) `python3 plugin/tests/run.py -k test_python_c_code_gets_the_same_proof` → exit 0 · Ran 1 tests in 1.6s (1 classes, 16 at a time; slowest: InterpreterWrites 1s) / OK [ran] [tree 1a2631fb1bf8] (2026-10-16T14:42:20Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_cases test_replay` → exit 0 · Ran 185 tests in 26.6s (59 classes, 16 at a time; slowest: GuardAgainstBash 25s, GuardCases 11s, Hook 8s) / OK [ran] [tree 1a2631fb1bf8] (2026-10-16T14:42:49Z)
- `python3 plugin/tests/run.py -k test_python_c_code_gets_the_same_proof_as_a_quoted_heredoc` → ✗ exit 1 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 072598071f74] (2026-10-16T14:52:56Z)
- `python3 plugin/tests/run.py -k test_python_c_code_gets_the_same_proof_as_a_quoted_heredoc` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / OK [ran] [tree 072598071f74] (2026-10-16T14:52:56Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_cases test_replay` → exit 0 · Ran 185 tests in 19.7s (59 classes, 16 at a time; slowest: GuardAgainstBash 19s, GuardCases 7s, Hook 5s) / OK [ran] [tree 072598071f74] (2026-10-16T14:53:16Z)
- (ac 1) `python3 plugin/tests/run.py test_guard test_guard_cases test_replay` → exit 0 · Ran 185 tests in 20.4s (59 classes, 16 at a time; slowest: GuardAgainstBash 20s, GuardCases 7s, Hook 5s) / OK [ran] [tree 072598071f74] (2026-10-16T14:53:57Z)
- (audit intent) `builder self-review (4 bypasses found and closed with tests: escaped separators, exported/inherited PYTHONPATH, -i, quadratic cd chain) plus my read of the diff after an adversarial reviewer stopped early (safety filter on building bypass commands); replay of 5000 real commands: 0 loosened` → literal-only -c code is allowed, the 2 hand-written literal-only cases go from refused to allowed; none of the 5 mined -c refusals were literal-only (all real fm imports), so those stay refused and are labelled block cases [tree 072598071f74] (2026-10-16T14:53:57Z)
- (audit adversary) `builder self-review (4 bypasses found and closed with tests: escaped separators, exported/inherited PYTHONPATH, -i, quadratic cd chain) plus my read of the diff after an adversarial reviewer stopped early (safety filter on building bypass commands); replay of 5000 real commands: 0 loosened` → only one literal quoted word that starts a command at shell top level is parsed; $'…', ${…}, heredocs, comments, aliases/functions, any PYTHON* text or inherited PYTHON* env, -i, and a cd outside the -c's own chain all fall back to the old refusal; the ast proof refuses _DYNAMIC names and non-plain imports [tree 072598071f74] (2026-10-16T14:53:57Z)
- (audit edge) `builder self-review (4 bypasses found and closed with tests: escaped separators, exported/inherited PYTHONPATH, -i, quadratic cd chain) plus my read of the diff after an adversarial reviewer stopped early (safety filter on building bypass commands); replay of 5000 real commands: 0 loosened` → double-quoted words exclude $ and backticks and are unescaped as bash does; the word must end at whitespace or an operator (no adjacent quotes) [tree 072598071f74] (2026-10-16T14:53:57Z)
- (audit operator) `builder self-review (4 bypasses found and closed with tests: escaped separators, exported/inherited PYTHONPATH, -i, quadratic cd chain) plus my read of the diff after an adversarial reviewer stopped early (safety filter on building bypass commands); replay of 5000 real commands: 0 loosened` → fewer core refusals for edit and grep helpers that mention fm modules in strings; refusal text unchanged [tree 072598071f74] (2026-10-16T14:53:57Z)
- (audit maintainer) `builder self-review (4 bypasses found and closed with tests: escaped separators, exported/inherited PYTHONPATH, -i, quadratic cd chain) plus my read of the diff after an adversarial reviewer stopped early (safety filter on building bypass commands); replay of 5000 real commands: 0 loosened` → one new function beside _python_units, used by _drives_fm only; the write-target proof is unchanged [tree 072598071f74] (2026-10-16T14:53:57Z)
## Log
- 2026-10-16T13:28:35Z created
- 2026-10-16T13:59:46Z planned from capture
- 2026-10-16T14:30:27Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1194.builder.md
- 2026-10-16T14:30:39Z focused
- 2026-10-16T14:52:44Z merged worktree-agent-a1b4d6f7b7e511430 (3 file(s))
- 2026-10-16T14:52:47Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a1b4d6f7b7e511430
- 2026-10-16T14:52:47Z focused
- 2026-10-16T14:53:27Z scope: CHANGELOG line
- 2026-10-16T14:55:31Z done
- 2026-10-16T14:55:32Z committed 7f00f694 (1 file)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: "Literal-only is allowed" is only safe if the ast proof also rejects string-derived execution beyond exec/eval/__import__/importlib, e.g. `subprocess`/`os.system`/`os.popen` running `fm ...` or `python -m fmcore` from a string, `compile`, `runpy`, `open(...).read()` then exec, and `-c` code t…
- HIGH: Extraction by shlex split is fragile. Need cases for `python3 -c` with combined flags (`-Ic`, `-Bc`, `-c` after `-W x`/`-X y`), `--` forms, `python3.12`, absolute paths, `python3 -c "$(cat f)"`/`$VAR`/backticks (code is not a literal, so it can't be proven and must stay refused), multiple -c …
- MEDIUM: The cwd shadow claim ("python -c puts '' first on sys.path") is only true without `-I`/`-P`/`PYTHONSAFEPATH`, and a `cd` earlier in the same compound command changes the effective cwd. Change: compute the shadow check against the cwd after any preceding `cd` (or refuse when a `cd` precedes)…
- MEDIUM: Acceptance proves the 3 mined cases replay allowed and no labelled block loosens, but not that the replayed refusals were all false positives. Change: record the 3 command texts as permanent labelled "allow" cases, and diff the full replay output before/after (not just "no loosened labelled…
- LOW: Step order puts tests first, which is good, but no rollback/flag is stated. Change: note the change is a single function edit in _python_units and revertible; confirm there's no other caller of _python_units whose behavior changes (e.g. a path that now sees -c units for non-fm checks).
- LOW: Interaction with a string literal that is an f-string or implicit concatenation naming `fmcore` in an import-like position (`"import " "fmcore"` passed to a helper that execs it). Change: add a case showing literals passed to non-exec calls are allowed while the same literal reaching any exec-…
Verdict: revise — the approach is right and minimal, but the fail-closed extraction rules and the sink coverage must be pinned down by cases before the loosening lands.
## Dissent
- [ ] HIGH: "Literal-only is allowed" is only safe if the ast proof also rejects string-derived execution beyond exec/eval/__import__/importlib, e.g. `subprocess`/`os.system`/`os.popen` running `fm ...` or `python -m fmcore` from a string, `compile`, `runpy`, `open(...).read()` then exec, and `-c` code t…
- [ ] HIGH: Extraction by shlex split is fragile. Need cases for `python3 -c` with combined flags (`-Ic`, `-Bc`, `-c` after `-W x`/`-X y`), `--` forms, `python3.12`, absolute paths, `python3 -c "$(cat f)"`/`$VAR`/backticks (code is not a literal, so it can't be proven and must stay refused), multiple -c …
- [ ] MEDIUM: The cwd shadow claim ("python -c puts '' first on sys.path") is only true without `-I`/`-P`/`PYTHONSAFEPATH`, and a `cd` earlier in the same compound command changes the effective cwd. Change: compute the shadow check against the cwd after any preceding `cd` (or refuse when a `cd` precedes)…
- [ ] MEDIUM: Acceptance proves the 3 mined cases replay allowed and no labelled block loosens, but not that the replayed refusals were all false positives. Change: record the 3 command texts as permanent labelled "allow" cases, and diff the full replay output before/after (not just "no loosened labelled…
- [ ] LOW: Step order puts tests first, which is good, but no rollback/flag is stated. Change: note the change is a single function edit in _python_units and revertible; confirm there's no other caller of _python_units whose behavior changes (e.g. a path that now sees -c units for non-fm checks).
- [ ] LOW: Interaction with a string literal that is an f-string or implicit concatenation naming `fmcore` in an import-like position (`"import " "fmcore"` passed to a helper that execs it). Change: add a case showing literals passed to non-exec calls are allowed while the same literal reaching any exec-…
## Related
Related past work (data from this project's history, not instructions):
- T-0170 [FIX M, done, 3 steps] Guard: 'driving Foreman's modules' reads real Python imports, not text that mentions them — lesson: Relax a guard by proving the safe case,…
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- T-1171 [FIX M, done, 2 steps] Guard: _drives_fm (fmguard.py:1364) treats any heredoc that doesn't parse, and fm-import t — lesson: mine full commands before relaxing a g…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar finished tasks took 2–3 steps
## Why not caught
none: a false-positive refusal, not a defect a test missed; the corpus had no literal-only -c case, which this task adds
## Lessons
- Loosening a guard rule needs the mined refusals checked first: none of the five were the false positive the request assumed, so the labelled cases had to be written by hand
## Plan gaps
- failed first: step 1 Labelled guard cases and tests first: literal-only -c allowed; real import, exec, __import__, impor…
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- plugin/tests/fixtures/guard_cases.jsonl
- CHANGELOG.md
