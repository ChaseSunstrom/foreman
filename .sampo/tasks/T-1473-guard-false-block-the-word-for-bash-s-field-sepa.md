---
id: T-1473
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/test_guard_diff.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T16:05:25Z
updated: 2026-10-22T18:37:33Z
base: aea55198d17117bece982141beba404163546b31
base_tree: a01188b256f75ab5e9b9c7798101cb0c7500021c
plan0_at: 2026-10-22T18:14:33Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/test_guard_diff.py, CHANGELOG.md]
verified: strong
---
# Guard: prose naming the field separator in a quoted argument isn't a block
## Raw request
> Guard false block: the word for bash's field-separator variable inside a double-quoted argument (prose passed to fm task set --text) was refused as 'system: may be changed on a line that splits words'; a quoted word that is an argument, not an assignment, can't change it
## Interpretation
fm task set ... --text holding prose with the words eval and the field-separator variable and a $ was refused as 'system: may be changed on a line that splits words'; the words were inside a double-quoted argument.
## Assumptions (confidence)
## Acceptance criteria
- [x] a quoted argument naming eval, the separator and $ passes; "eval" 'X=…' as a command word and every existing separator case still block — verify with `cd plugin/tests && python3 -m unittest test_guard.SeparatorProse`
- [x] the real-bash forms corpus still passes — verify with `cd plugin/tests && python3 -m unittest test_guard_diff`
## Non-goals
## Approach (options → choice → why)
Grounded: _ifs_unreadable (fmguard.py ~697) sets hidden = _RUNS_HERE.search(rest) over the raw line, so the word eval inside a double-quoted argument counts as an eval that may set the separator; text then includes the quoted prose, which names it, and a $ in that prose counts as an expansion: refused. Options: (1) mask quotes before the eval search — rejected: a quoted command word ("eval" 'X=…') is still eval to bash; (2) chosen: decide "runs here" from command words, the first word of each simple command after the guard's own unquoting (_split/_tokens/_strip_wrappers), eval, source, ., builtin eval, command eval; quoted words in argument position are data. Every existing IFS test and test_guard_diff's real-bash FORMS must still pass; add the false block as an allow case and quoted-command-word evals as block cases.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] runs-here from command words
## Resume here
<!-- auto -->
- 2026-10-22T18:22:51Z step 1/2: failing test
- git: foreman/build; 2 uncommitted: plugin/lib/fmguard.py, plugin/tests/test_guard.py
- touched since last checkpoint: /tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/probe_ifs.py, plugin/tests/test_guard.py, /tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/trace_ifs.py, plugin/lib/fmguard.py
## Docs impact
CHANGELOG.md
## Verification evidence
- `cd plugin/tests && python3 -m unittest test_guard.SeparatorProse` → ✗ exit 1 · Ran 2 tests in 0.062s / FAILED (failures=2) (start tree + this task's tests) [ran] [tree 1b4f1dbe18ca] (2026-10-22T18:24:36Z)
- `cd plugin/tests && python3 -m unittest test_guard.SeparatorProse` → exit 0 · Ran 2 tests in 0.082s / OK [ran] [tree 1b4f1dbe18ca] (2026-10-22T18:24:36Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_guard.SeparatorProse` → exit 0 · Ran 2 tests in 0.110s / OK [ran] [tree 1b4f1dbe18ca] (2026-10-22T18:24:42Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_guard test_guard_diff test_guard_pipes` → exit 0 · Ran 132 tests in 12.273s / OK [ran] [tree 1b4f1dbe18ca] (2026-10-22T18:24:55Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard.SeparatorProse` → exit 0 · Ran 2 tests in 0.029s / OK [ran] [tree 1b4f1dbe18ca] (2026-10-22T18:24:56Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_guard_diff` → exit 0 · Ran 3 tests in 6.132s / OK [ran] [tree 1b4f1dbe18ca] (2026-10-22T18:25:02Z)
- `cd plugin/tests && python3 -m unittest test_guard.SeparatorProse` → ✗ exit 1 · Ran 3 tests in 0.062s / FAILED (failures=2) (start tree + this task's tests) [ran] [tree df261d4acf01] (2026-10-22T18:32:06Z)
- `cd plugin/tests && python3 -m unittest test_guard.SeparatorProse` → exit 0 · Ran 3 tests in 0.060s / OK [ran] [tree df261d4acf01] (2026-10-22T18:32:06Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_guard.SeparatorProse test_guard test_guard_diff test_guard_pipes test_guard_evasions test_guard_cases test_guard_debris` → exit 0 · Ran 153 tests in 10.067s / OK [ran] [tree df261d4acf01] (2026-10-22T18:32:22Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_guard.SeparatorProse test_guard test_guard_diff test_guard_pipes test_guard_evasions test_guard_cases test_guard_debris` → exit 0 · Ran 153 tests in 10.657s / OK [ran] [tree df261d4acf01] (2026-10-22T18:32:33Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard.SeparatorProse` → exit 0 · Ran 3 tests in 0.056s / OK [ran] [tree df261d4acf01] (2026-10-22T18:32:34Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_guard_diff` → exit 0 · Ran 3 tests in 4.726s / OK [ran] [tree df261d4acf01] (2026-10-22T18:32:39Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmguard.py — commit it through a task, or git checkout it back / fm doctor: OK (41 pass, 7 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                43.4    47.5     150  [0] / SessionEnd                  37.9    44.4     150  [0] (slower: 54.3 s vs a usual 23.2 s); claude plugin test mods/foreman-ui → exit 0 · s [ran] [tree df261d4acf01] (2026-10-22T18:36:51Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard.SeparatorProse` → exit 0 · Ran 3 tests in 0.052s / OK [ran] [tree df261d4acf01] (2026-10-22T18:37:06Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_guard_diff` → exit 0 · Ran 3 tests in 4.569s / OK [ran] [tree df261d4acf01] (2026-10-22T18:37:06Z)
- (audit intent) `one fm-reviewer adversary pass: one HIGH (escaped $IFS in eval text) fixed test-first; the fix only widens refusals (hidden broader, escapes live when hidden), so no re-review` → prose naming eval, IFS and $ in a quoted argument now passes (fm task log, echo); escaped forms are literal text [tree df261d4acf01] (2026-10-22T18:37:06Z)
- (audit adversary) `one fm-reviewer adversary pass: one HIGH (escaped $IFS in eval text) fixed test-first; the fix only widens refusals (hidden broader, escapes live when hidden), so no re-review` → eval/source after keywords, !, case ), prefix assignments, trap, mapfile -C, readarray -C, alias and sourced heredocs still refuse; odd/even backslash runs checked; review finding fixed [tree df261d4acf01] (2026-10-22T18:37:06Z)
- (audit edge) `one fm-reviewer adversary pass: one HIGH (escaped $IFS in eval text) fixed test-first; the fix only widens refusals (hidden broader, escapes live when hidden), so no re-review` → unquoted literal \$IFS passes; \\$IFS (escaped backslash then a real expansion) refuses; $'…' only fails closed when real [tree df261d4acf01] (2026-10-22T18:37:06Z)
- (audit maintainer) `one fm-reviewer adversary pass: one HIGH (escaped $IFS in eval text) fixed test-first; the fix only widens refusals (hidden broader, escapes live when hidden), so no re-review` → SeparatorProse holds allow and block cases, red on the start tree [tree df261d4acf01] (2026-10-22T18:37:06Z)
- (audit intent) `one fm-reviewer adversary pass: one HIGH (escaped $IFS in eval text) fixed test-first; the fix only widens refusals (hidden broader, escapes live when hidden), so no re-review` → prose naming eval, IFS and $ in a quoted argument now passes (fm task log, echo); escaped forms are literal text [tree df261d4acf01] (2026-10-22T18:37:24Z)
- (audit adversary) `one fm-reviewer adversary pass: one HIGH (escaped $IFS in eval text) fixed test-first; the fix only widens refusals (hidden broader, escapes live when hidden), so no re-review` → eval/source after keywords, !, case ), prefix assignments, trap, mapfile -C, readarray -C, alias and sourced heredocs still refuse; odd/even backslash runs checked; review finding fixed [tree df261d4acf01] (2026-10-22T18:37:24Z)
- (audit edge) `one fm-reviewer adversary pass: one HIGH (escaped $IFS in eval text) fixed test-first; the fix only widens refusals (hidden broader, escapes live when hidden), so no re-review` → unquoted literal \$IFS passes; \\$IFS (escaped backslash then a real expansion) refuses; $'…' only fails closed when real [tree df261d4acf01] (2026-10-22T18:37:24Z)
- (audit maintainer) `one fm-reviewer adversary pass: one HIGH (escaped $IFS in eval text) fixed test-first; the fix only widens refusals (hidden broader, escapes live when hidden), so no re-review` → SeparatorProse holds allow and block cases, red on the start tree [tree df261d4acf01] (2026-10-22T18:37:24Z)
## Log
- 2026-10-22T16:05:25Z created
- 2026-10-22T16:06:43Z planned from capture
- 2026-10-22T16:37:16Z blocked: waits for T-1263's lane (its gaps may touch fmguard.py's separator checks)
- 2026-10-22T17:14:28Z set status=planned
- 2026-10-22T18:14:32Z focused
- 2026-10-22T18:14:47Z paused: focus moved to T-1491
- 2026-10-22T18:20:14Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-22T18:20:14Z focused
- 2026-10-22T18:37:19Z scope: plugin/skills/playbooks/references/ui/interaction.md changed under T-1491 (committed, its own task) since T-1473's base; T-1473 never edited it
- 2026-10-22T18:37:32Z done
- 2026-10-22T18:37:33Z committed c03b8b20 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1480 [SECURITY M, done, 4 steps] Guard gap: $'…' ANSI-C quoted command names and C=env; $C variable indirection get past th — lesson: A guard pre-pass must find struct…
- research T-0411-review: Verdict: changes needed.** I found three bypasses in `_expand_literal_loops`. I could not run bash (read-only), so each one is traced from the co…
- research T-1480-review: Verdict: changes needed.** This was a read-only review: I could not run anything, so neither finding has been executed against the guard. Both co…
- decision 2026-10-21: T-1330 approved by self-critique (full autonomy): the app is views inside fm code tui's existing App; --task works a planned brief with a per-task l…
- likely tests for the scope: plugin/tests/test_guard.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmguard.py, plugin/tests/test_guard.py; re-ground the plan against them before editing
## Why not caught
the guard's eval detection listed command positions, not every keyword and prefix that can precede eval
## Lessons
- An escape is literal only in the shell that reads it first: anything that runs text again (eval, source, trap, mapfile -C, alias) turns \$ back into $, so a guard rule that trusts escapes must know every re-runner
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
- plugin/skills/playbooks/references/ui/interaction.md
