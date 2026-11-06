---
id: T-0175
type: SECURITY
tier: L
status: done
priority: normal
scope: [plugin/lib/fmguard.py,plugin/tests/test_guard.py,plugin/tests/test_guard_diff.py,CHANGELOG.md,MASTER.md]
depends_on: []
source: self
created: 2026-10-03T09:27:38Z
updated: 2026-10-03T09:52:58Z
base: fc4c7c53613f4c80ad70fc4b15e127192c1b00d0
base_tree: aabc10dae56a7d63ddf120f7746cb53c5b0049f0
verified: strong
---
# Guard: writes through a variable are checked — known NAME=literal values and $HOME resolve write, copy and cd targets (&& chains too); a target still unknown counts as writing any protected path the command names
## Raw request
> Guard state-direct: a cd into a scratch repo is ignored when resolving .foreman/x, and .foreman inside python string literals counts as a write — evidence: two T-0174 probe commands blocked (echo into a scratch repo's .foreman/x after cd; a python heredoc whose replace() text mentioned .foreman)
## Interpretation
Found while grounding T-0175 (a scratch-repo probe blocked as state-direct): check_bash skips every write, tee/cp and tree target containing $ or a backtick, so x=<core file>; echo > $x, $HOME/.claude/…, cp src $x and $(echo <core>) all pass unchecked — a fail-open path in a fail-closed guard. The reverse problem caused the original friction: cd $d in an && chain isn't followed (variables are tracked only in ;-joined commands), so a relative write after it is judged against the project root.
## Assumptions (confidence)
## Acceptance criteria
- [x] a write through a variable or $HOME is checked, and a known harmless one isn't — verify with `python3 plugin/tests/run.py -k test_a_write_through_a_variable_is_checked`
- [x] real bash agrees on && chains: every form the differential test runs is still blocked — verify with `python3 plugin/tests/run.py -k test_every_form_that_runs_a_dangerous_call_is_blocked`
## Non-goals
## Approach (options → choice → why)
A: extend T-0151's tracked env (unquoted NAME=literal, read as written) from rm targets to write, tree and cd targets, pre-seeded with HOME (only when nothing in the command assigns HOME), and treat a chain joined only by && as straight-line (a command there runs only after every earlier one ran, so sequential values hold; mixing && with ; or newlines stays unresolved: false && D=x; rm $D is the T-0161 trap). A target still unresolvable after that counts as writing every path the command names (each word resolved against the tracked cwd), the way interpreter code already does — coarse but closed. B (rejected): block every unresolvable write target outright — closed too, but for f in *; do … > $f.bak would need a yes it can't even be granted for (no category). C (rejected): run the command under a shell parser to compute values — the guard stays dependency-free and a parser still can't know runtime values.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests first: guard table rows and && EXTRA forms (red)
2. [x] resolve targets through the tracked env; && chains straight-line; unknown targets scan named paths
3. [x] gates, docs, five-lens audit
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md (guard limits: variables in targets, places the shell may be, inherited names)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_a_write_through_a_variable_is_checked` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Core 0s) / FAILED (1 classes) [ran] [tree 18372ebe1649] (2026-10-03T09:33:51Z)
- (step 1) `python3 plugin/tests/run.py -k test_every_form_that_runs_a_dangerous_call_is_blocked` → exit 0 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: GuardAgainstBash 1s) / OK [ran] [tree 18372ebe1649] (2026-10-03T09:33:53Z)
- (step 2) `python3 plugin/tests/run.py -k test_a_write_through_a_variable_is_checked` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Core 0s) / FAILED (1 classes) [ran] [tree 7e78ad487bae] (2026-10-03T09:35:13Z)
- (step 2) `python3 plugin/tests/run.py -k test_every_form_that_runs_a_dangerous_call_is_blocked` → exit 0 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: GuardAgainstBash 1s) / OK [ran] [tree c446b5cfd682] (2026-10-03T09:36:26Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py` → exit 0 · 5 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · skipped: nothing under plugin/**, install.sh changed since its pass at 09:37 UTC; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 09:37 UTC; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed [ran] [tree a30310f0ce99] (2026-10-03T09:38:37Z)
- (step 2) `python3 plugin/tests/run.py -k test_a_write_through_a_variable_is_checked` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Core 0s) / OK [ran] [tree f2397b69ba6d] (2026-10-03T09:46:31Z)
- (step 2) `python3 plugin/tests/run.py -k test_every_form_that_runs_a_dangerous_call_is_blocked` → exit 0 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: GuardAgainstBash 1s) / OK [ran] [tree f2397b69ba6d] (2026-10-03T09:46:32Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py` → exit 0 · 5 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.2    33.5     150  [0] / SessionEnd                  28.3    29.3     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 09:15 UTC; python3 plugin/tests/run.py → e [ran] [tree 82d9b2426d37] (2026-10-03T09:47:25Z)
- (step 2) `python3 plugin/tests/run.py -k test_a_write_through_a_variable_is_checked` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Core 0s) / OK [ran] [tree e67e48abadf4] (2026-10-03T09:51:53Z)
- (step 2) `python3 plugin/tests/run.py -k test_every_form_that_runs_a_dangerous_call_is_blocked` → exit 0 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: GuardAgainstBash 1s) / OK [ran] [tree e67e48abadf4] (2026-10-03T09:51:54Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py` → exit 0 · 5 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.1    32.0     150  [0] / SessionEnd                  28.6    32.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 09:15 UTC; python3 plugin/tests/run.py → e [ran] [tree aa5825b1bfcd] (2026-10-03T09:52:41Z)
- (ac 1) `python3 plugin/tests/run.py -k test_a_write_through_a_variable_is_checked` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Core 0s) / OK [ran] [tree aa5825b1bfcd] (2026-10-03T09:52:58Z)
- (ac 2) `python3 plugin/tests/run.py -k test_every_form_that_runs_a_dangerous_call_is_blocked` → exit 0 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: GuardAgainstBash 1s) / OK [ran] [tree aa5825b1bfcd] (2026-10-03T09:52:58Z)
- (audit intent) `two fm-reviewer passes (all five lenses, then a targeted re-review of the reworked cd/env model); every finding fixed with a test row or documented` → closes the fail-open path (write, tee, copy and tree targets with a $ were skipped) and the original friction (d=/tmp/x && cd $d && echo > .foreman/x); cd $(mktemp -d) && … .foreman/x stays blocked by the T-0158 tail re-read, documented as coarse [tree aa5825b1bfcd] (2026-10-03T09:52:58Z)
- (audit adversary) `two fm-reviewer passes (all five lenses, then a targeted re-review of the reworked cd/env model); every finding fixed with a test row or documented` → review 1 found eval/read re-setting HOME, cd in a subshell/background/pipe/; chain, and false blocks; review 2 found ! chains, pushd -n/+N, CDPATH set without its name, ~+/~user — all fixed with rows in Core.test_a_write_through_a_variable_is_checked; the differential bash test has 7 new && forms and passes; remaining limits: values a shell profile changes (documented), glob/brace targets (captured) [tree aa5825b1bfcd] (2026-10-03T09:52:58Z)
- (audit edge) `two fm-reviewer passes (all five lenses, then a targeted re-review of the reworked cd/env model); every finding fixed with a test row or documented` → reads that name a core file while writing to a name the command can't set are allowed; a straight cd into an existing or mkdir -p made folder is certain, so the ; and multi-line forms aren't blocked; impossible guesses (an existing file as a folder) skipped [tree aa5825b1bfcd] (2026-10-03T09:52:58Z)
- (audit operator) `two fm-reviewer passes (all five lenses, then a targeted re-review of the reworked cd/env model); every finding fixed with a test row or documented` → an unknown target's block names the path it could be ('not known before it runs: it could be …'); a probe of this session's everyday commands stays allowed; hook latency bench passes [tree aa5825b1bfcd] (2026-10-03T09:52:58Z)
- (audit maintainer) `two fm-reviewer passes (all five lenses, then a targeted re-review of the reworked cd/env model); every finding fixed with a test row or documented` → one helper per concern (_outside, _top, _moved, _possible, _target_cats), each with its why; MASTER's guard-limits paragraph and CHANGELOG describe the model [tree aa5825b1bfcd] (2026-10-03T09:52:58Z)
## Log
- 2026-10-03T09:27:38Z created
- 2026-10-03T09:33:19Z planned from capture
- 2026-10-03T09:33:25Z set approved=True
- 2026-10-03T09:33:25Z focused
- 2026-10-03T09:35:13Z hypothesis: routing cd, write and tree targets through the tracked env (HOME-seeded, && chains straight-line) plus a named-path scan for unknown targets turns all 17 table rows green without breaking any existing guard or differential test
- 2026-10-03T09:36:23Z result: hypothesis held after two corrections — a cd the guard can't follow now marks the cwd lost (relative targets become $PWD/name and are tried against each named path), and the HOME=/tmp row was my error (bash writes under /tmp)
- 2026-10-03T09:46:15Z review fixes: names are known only where the command can't set them (no bare NAME, no eval/read/declare-like builtin, no computed command): values from Claude Code's environment, HOME the user's; cd tracks every place the shell may be (an && chain replaces, ; and branches add), plus paths below a folder it can't name (unresolved cd, CDPATH); a guess must be a possible path
- 2026-10-03T09:51:52Z second review fixes: ! makes a chain unsure; pushd -n/+N/-N; CDPATH assumed whenever any name may be set; ~+/~-/~user; a straight cd into an existing (or mkdir -p made) folder is certain, ending the ; false block; rm trusts no inherited value but HOME, write targets keep Claude Code's environment (documented limit: a profile may change it)
- 2026-10-03T09:52:58Z done
- 2026-10-03T09:52:58Z committed a6a5169 (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- research T-0161-review: Verdict: changes needed.** `_track_vars` still has bypasses, and one of them is the same class T-0161 set out to close. I traced each through `_s…
- research t0018-r5-maintainer: HIGH — plugin/lib/fmguard.py:188-198 (`_protected_roots`) vs plugin/lib/fmguard.py:165-171 (`_is_core`) — tree-write guard misses project-l…
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- A fail-closed guard needs its skip paths audited as hard as its block paths: 'unresolvable → skip' was a silent allow sitting next to fail-closed rm handling, and modelling where a cd lands took two adversarial passes to get right.
## Files touched
- plugin/tests/test_guard.py
- plugin/tests/test_guard_diff.py
- plugin/lib/fmguard.py
- MASTER.md
- CHANGELOG.md
