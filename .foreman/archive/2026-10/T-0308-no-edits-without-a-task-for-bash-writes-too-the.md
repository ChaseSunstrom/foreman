---
id: T-0308
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T18:23:20Z
updated: 2026-10-04T18:27:31Z
base: 503ecf872e884d73936b8c2a470191f3e48e5428
base_tree: a82033f04ea619df293308317ca132ee00f5908f
verified: strong
---
# No edits without a task, for Bash writes too: the guard refuses shell writes into the project while no task is active
## Raw request
> No edits without a task, for Bash writes too: the guard refuses shell writes into the project while no task is active
## Interpretation
The court replay R-T-0218 changed code through Bash only, with no task: in bypass mode Claude Code steers edits to sed and heredocs, and the no-task gate only covers Edit/Write. Close that path with the guard's existing write-target parsing.
## Assumptions (confidence)
## Acceptance criteria
- [x] with no active task, shell writes into the project (redirect, sed -i, cp, interpreter open()) are refused with the one-command fix; reads, fm, scratch, /tmp, state and quiet sessions are not; an active task allows them — verify with `python3 plugin/tests/run.py -p test_hooks.py -k NoTaskGate`
- [x] the guard suite and replay corpus still pass — verify with `python3 plugin/tests/run.py -p test_guard.py`
## Non-goals
## Approach (options → choice → why)
A: a guard category 'brief' (not grantable; fixed by starting a task) that classify_write returns for paths strictly inside the project when the hook says no task is active — reuses every write parser (redirects, sed -i, cp/mv/tee, interpreter open(), guessed targets) and folds the Edit-only gate into one rule. B: a second Bash write parser in the hook's no-task gate — duplicates the guard's parsing and drifts. Choose A. Strictly inside: a checkout-wide git write (merge, pull, branch switch) targets the root and stays allowed.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests for Bash writes with no task
2. [x] brief category in the guard, set by the hook when no task is active; the Edit-only gate folds into it
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_hooks.py -k NoTaskGate` → ✗ exit 1 · Ran 5 tests in 1.9s (1 classes, 16 at a time; slowest: NoTaskGate 2s) / FAILED (1 classes) [ran] [tree 16d47e873041] (2026-10-04T18:23:33Z)
- (step 1) `python3 plugin/tests/run.py -p test_hooks.py -k NoTaskGate` → exit 0 · Ran 5 tests in 1.9s (1 classes, 16 at a time; slowest: NoTaskGate 2s) / OK [ran] [tree 939b3ac4de87] (2026-10-04T18:24:51Z)
- (step 2) `python3 plugin/tests/run.py -p test_guard.py` → exit 0 · Ran 56 tests in 0.2s (16 classes, 16 at a time; slowest: PluginChanges 0s, InterpreterWrites 0s, Core 0s) / OK [ran] [tree 583266aa2489] (2026-10-04T18:25:44Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (26 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.0    32.8     150  [0] / SessionEnd                  28.4    32.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 09:59 UTC; python3 plugin/tests/run.py → exit 0 · Ran 822 tests in [ran] [tree 583266aa2489] (2026-10-04T18:26:45Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p test_hooks.py -k NoTaskGate` → 8/9 hunks proven; unproven: plugin/lib/fmhooks.py @@ -992,13 +986,0 @@ def _in_project(path, p): [inconclusive] [ran] [tree 583266aa2489] (2026-10-04T18:27:13Z)
- (ac 1) `python3 plugin/tests/run.py -p test_hooks.py -k NoTaskGate` → exit 0 · Ran 5 tests in 2.0s (1 classes, 16 at a time; slowest: NoTaskGate 2s) / OK [ran] [tree 583266aa2489] (2026-10-04T18:27:31Z)
- (ac 2) `python3 plugin/tests/run.py -p test_guard.py` → exit 0 · Ran 56 tests in 0.2s (16 classes, 16 at a time; slowest: PluginChanges 0s, Core 0s, InterpreterWrites 0s) / OK [ran] [tree 583266aa2489] (2026-10-04T18:27:31Z)
- (audit intent) `self (subagent cap reached): red→green NoTaskGate (7 shell write forms refused, 7 non-writes allowed, quiet and active-task allowed); guard, hooks, builder, cli, replay suites pass; fm check exit 0 with replay 0 newly allowed; hunk proof 8/9 (the 9th is the dead gate's deletion)` → closes the path the court replay R-T-0218 used (Bash edits with no task); the Edit/Write gate folds into the same guard rule with the same one-command fix [tree 583266aa2489] (2026-10-04T18:27:31Z)
- (audit adversary) `self (subagent cap reached): red→green NoTaskGate (7 shell write forms refused, 7 non-writes allowed, quiet and active-task allowed); guard, hooks, builder, cli, replay suites pass; fm check exit 0 with replay 0 newly allowed; hunk proof 8/9 (the 9th is the dead gate's deletion)` → only adds refusals — brief is NOT_AUTHORIZABLE (fm ask can't grant it; starting a task clears it); state-direct still wins on state paths; known gap: a bare file name in python -c isn't a target (the coarse rule needs a path-looking string), heredoc python is AST-proved [tree 583266aa2489] (2026-10-04T18:27:31Z)
- (audit edge) `self (subagent cap reached): red→green NoTaskGate (7 shell write forms refused, 7 non-writes allowed, quiet and active-task allowed); guard, hooks, builder, cli, replay suites pass; fm check exit 0 with replay 0 newly allowed; hunk proof 8/9 (the 9th is the dead gate's deletion)` → a project under /tmp isn't exempted by the /tmp scratch entry (same as confine); checkout-wide git writes (merge, pull) target the root and stay allowed; FOREMAN_QUIET sessions skip it as before; auto memory under ~/.claude/projects exempt [tree 583266aa2489] (2026-10-04T18:27:31Z)
## Log
- 2026-10-04T18:23:20Z created
- 2026-10-04T18:23:20Z focused
- 2026-10-04T18:27:31Z done
- 2026-10-04T18:27:31Z committed 8ae2e89 (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- T-0180 [SECURITY M, done, 3 steps] Guard: a standing or trusted yes covers a finding's plain path only — relative shell writes named by their real path, annotated detail…
- research T-0286-review-1: Changes needed. I found no new hole that the `cd` prefix itself opens. The `cd` chain does make four existing parse mismatches reachable from a…
- research T-0258-review-1: Verdict:** changes needed. I found one HIGH cross-feature issue, two MEDIUM, and the rest are LOW doc or maintainer drift. I read the whole dif…
## Lessons
- A gate on one tool is a suggestion to use another: enforce the rule where every write path is parsed (the guard), not per tool
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmguard.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
