---
id: T-0414
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T05:04:40Z
updated: 2026-10-09T14:08:24Z
base: 4ca8609aac5a8beb53bc5ac88632f8171583c469
base_tree: 308b1d7118e5eb96d16b7b33e95279836fb405bd
verified: strong
---
# Guard: a data-reading python -c is judged by what runs before it
## Raw request
> FIX: pipe-shell: curl … | python3 -c 'json.load(sys.stdin)' is refused whenever any other command on the line isn't a plain data tool, even ones that run after the pipeline finished (JARVIS 4× in one session: '…| python3 -c …; git log; git fetch', '…| python3 -c …; nvidia-smi; (timeout 3 curl … > scratch/up.log)', 'A=$(grep …); IP=…; fm task evidence … --run "! git grep … && curl … | python3 -c …"'). Plan: (a) ignore commands strictly after python's pipeline joined by ; && || newline (not &: concurrent); (b) maybe: plain assignments of names absent from the environment and not PYTHON*/LD_*/PATH/HOME, when their $( ) commands are themselves checked
## Interpretation
curl … | python3 -c CODE passes when CODE only reads the download as data and every other command on the line is a plain data tool. JARVIS keeps adding unrelated commands after the pipeline (nvidia-smi, git fetch, a scratch log) and before it (T=$(grep …); API=…). Commands that run after python has exited can't change what it does; a plain assignment of a name the environment doesn't have can't reach python either.
## Assumptions (confidence)
## Acceptance criteria
- [x] a data-reading python -c passes with later commands of any kind and earlier plain assignments; a bare & anywhere, an assignment of an exported or PYTHON* name, or a $( ) that writes still refuses; real bash rows agree — verify with `python3 plugin/tests/run.py -k test_data_python_ignores_what_runs_after`
## Non-goals
## Approach (options → choice → why)
(A, chosen) (a) pass _reads_pipe_as_data only the commands up to the end of python's pipeline, when the line has no bare & (a backgrounded group runs beside python); (b) a command that is only NAME=value words counts as writing nothing when each NAME is absent from the environment and not PYTHON*/LD_*/PATH/HOME/ENV/BASH_ENV, and its $( ) commands are themselves data tools. (B, rejected) allow read-only git subcommands: git grep -O runs a pager, git log/diff --output write. (C, rejected) hint only: the refusal stays.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: allowed and refused rows (unit + real-bash diff rows)
2. [x] slice cmds at the pipeline's end; assignment-only commands as data
3. [x] replay, gate, changelog, ship
## Resume here
## Docs impact
CHANGELOG entries (T-0414, T-0421, T-0422)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_data_python_ignores_what_runs_after` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: DataPythonAfter 0s) / FAILED (1 classes) [ran] [tree 3be452a7f0ea] (2026-10-09T13:41:05Z)
- (step 1) `python3 plugin/tests/run.py -p test_guard_diff.py` → ✗ exit 1 · Ran 1 tests in 1.8s (1 classes, 16 at a time; slowest: GuardAgainstBash 2s) / FAILED (1 classes) [ran] [tree 3be452a7f0ea] (2026-10-09T13:41:07Z)
- (step 2) `python3 plugin/tests/run.py -k test_data_python_ignores_what_runs_after` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: DataPythonAfter 0s) / OK [ran] [tree f030bbdf0558] (2026-10-09T13:43:57Z)
- (step 2) `python3 plugin/tests/run.py -p test_guard*.py` → exit 0 · Ran 82 tests in 2.1s (30 classes, 16 at a time; slowest: GuardAgainstBash 2s, InterpreterWrites 0s, PluginChanges 0s) / OK [ran] [tree f030bbdf0558] (2026-10-09T13:43:59Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (29 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.9    33.1     150  [0] / SessionEnd                  29.6    30.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 13:13 UTC; python3 plugin/tests/run.py → exit 0 · Ran 955 tests in [ran] [tree b9c00aaaa276] (2026-10-09T13:45:23Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed on this tree (run at 13:45 UTC) [ran] [tree b9c00aaaa276] (2026-10-09T13:45:28Z)
- (step 3) `fm replay` → exit 0 · 0 newly allowed (possible bypasses) / 574 new to the corpus [ran] [tree b9c00aaaa276] (2026-10-09T13:45:42Z)
- (step 2) `python3 plugin/tests/run.py -k test_data_python_ignores_what_runs_after` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: DataPythonAfter 0s) / FAILED (1 classes) [ran] [tree 9bf449244653] (2026-10-09T14:02:48Z)
- (step 2) `python3 plugin/tests/run.py -p test_guard.py -p test_guard_diff.py` → exit 0 · Ran 80 tests in 2.1s (29 classes, 16 at a time; slowest: GuardAgainstBash 2s, PluginChanges 0s, KnownVars 0s) / OK [ran] [tree 4e4184515270] (2026-10-09T14:04:06Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (28 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.7    33.6     150  [0] / SessionEnd                  29.7    32.1     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 13:13 UTC; python3 plugin/tests/run.py → exit 0 · Ran 968 tests in [ran] [tree 80129685eaba] (2026-10-09T14:06:55Z)
- (step 1) `python3 plugin/tests/run.py -k test_data_python_ignores_what_runs_after` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: DataPythonAfter 0s) / OK [ran] [tree 80129685eaba] (2026-10-09T14:08:24Z)
- (ac 1) `python3 plugin/tests/run.py -k test_data_python_ignores_what_runs_after` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: DataPythonAfter 0s) / OK [ran] [tree 80129685eaba] (2026-10-09T14:08:24Z)
- (audit adversary) `builder branch + one adversary fm-reviewer pass (HIGH: quoted ')' depth miscount → fixed, two real-bash rows); full gate exit 0; replay 0 newly allowed of 5000` → bare &, groups with redirects/pipes, quoted parens, PYTHON*/LD_*/PATH/HOME/IFS assignments, quoted $( ) and backticks, printf -v, heredoc substitutions, tainted names — each refused, unit + real bash [tree 80129685eaba] (2026-10-09T14:08:24Z)
- (audit intent) `builder branch + one adversary fm-reviewer pass (HIGH: quoted ')' depth miscount → fixed, two real-bash rows); full gate exit 0; replay 0 newly allowed of 5000` → JARVIS's '…| python3 -c …; git log; git fetch' and 'T=$(grep …); API=…; curl … | python3 -c …' now pass; '! git grep … && curl … | python3' still refuses (git grep -O runs a pager: option B rejected) [tree 80129685eaba] (2026-10-09T14:08:24Z)
- (audit edge) `builder branch + one adversary fm-reviewer pass (HIGH: quoted ')' depth miscount → fixed, two real-bash rows); full gate exit 0; replay 0 newly allowed of 5000` → 'sleep 1 & curl … | python3' now refuses (a bare & anywhere); a line with a quoted paren falls back to the old whole-line rule [tree 80129685eaba] (2026-10-09T14:08:24Z)
- (audit operator) `builder branch + one adversary fm-reviewer pass (HIGH: quoted ')' depth miscount → fixed, two real-bash rows); full gate exit 0; replay 0 newly allowed of 5000` → no new message; the existing hint already says how a data-reading python passes [tree 80129685eaba] (2026-10-09T14:08:24Z)
- (audit maintainer) `builder branch + one adversary fm-reviewer pass (HIGH: quoted ')' depth miscount → fixed, two real-bash rows); full gate exit 0; replay 0 newly allowed of 5000` → Cmd gained depth; the top-level test is one expression with its reason above it [tree 80129685eaba] (2026-10-09T14:08:24Z)
## Log
- 2026-10-09T05:04:40Z created
- 2026-10-09T05:06:22Z analysis: of JARVIS's 4 blocks, (a) commands after the pipeline fixes 1 (… | python3 -c …; nvidia-smi; (timeout 3 curl … > scratch/up.log)); (a)+(b) assignments fixes 2 (T=$(grep …); API=…; curl -H … | python3 -c …; git log; git fetch). Not fixable safely: an earlier background hf download … &, and an earlier git grep (git grep -O runs a pager; git log/diff --output write). (a) must keep every command when the line has a bare & anywhere (a subshell or group backgrounded runs beside python). Call site: fmguard.check_bash, _reads_pipe_as_data(c, argv, cmds, cwds)
- 2026-10-09T05:06:35Z planned from capture
- 2026-10-09T13:24:23Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0414.builder.md
- 2026-10-09T13:24:39Z focused
- 2026-10-09T14:02:29Z merged worktree-agent-a0864fcff2994e067 (4 file(s))
- 2026-10-09T14:02:29Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a0864fcff2994e067
- 2026-10-09T14:02:29Z focused
- 2026-10-09T14:04:07Z merged the builder's branch (df9d352); review (adversary): HIGH — a quoted ')' made _split count python outside a ( ) group whose > json.py or | tee json.py runs beside it; real bash confirmed (two EXTRA rows). Fixed: top also needs every command at depth >= 0 and bare paren tokens to match the unquoted parens
- 2026-10-09T14:04:13Z paused: focus moved to T-0421
- 2026-10-09T14:08:15Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-09T14:08:15Z focused
- 2026-10-09T14:08:24Z done
- 2026-10-09T14:08:24Z committed 4328aa2 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0369 [FIX M, done, 2 steps] Guard: pin the pipe proof's strictness (premise of a self-improvement finding was false) — lesson: Before widening a guard from a friction …
- research rsi-pass-20261008: 1. **Answer.** I could ground one improvement fully (the pipe-shell false block) and one partly (state-direct from guessed variable targets).…
- research T-0344-review: Verdict: changes needed.** I had no shell, so these are traced by reading `plugin/lib/fmguard.py` and the tests. I did not run any command. [stal…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- the similar finished task took 2 steps
- start here (files T-0369 touched): plugin/tests/test_guard.py, plugin/lib/fmguard.py
## Lessons
- A parser that drops quoting can't be trusted about structure the quotes could fake: cross-check its counts against the masked text and fail closed when they differ.
## Files touched
- .claude/worktrees/agent-a0864fcff2994e067/plugin/tests/test_guard.py
- .claude/worktrees/agent-a0864fcff2994e067/plugin/tests/test_guard_diff.py
- .claude/worktrees/agent-a0864fcff2994e067/plugin/lib/fmguard.py
- .claude/worktrees/agent-a0864fcff2994e067/CHANGELOG.md
- plugin/tests/test_guard_diff.py
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- .claude-plugin/marketplace.json
- .gitattributes
- CHANGELOG.md
- MASTER.md
- plugin/.claude-plugin/plugin.json
- plugin/lib/fmcli.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmhooks.py
- plugin/lib/fmsmoke.py
- plugin/lib/smoke_web.cjs
- plugin/tests/test_guard_pipes.py
- plugin/tests/test_hooks.py
- plugin/tests/test_smoke.py
