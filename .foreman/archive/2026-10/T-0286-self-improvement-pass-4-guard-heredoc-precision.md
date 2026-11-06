---
id: T-0286
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-04T08:29:35Z
updated: 2026-10-04T08:45:14Z
batch: [T-0282, T-0283, T-0284, T-0285, T-0279]
base: a0d1b804b084c9d1f3acd743952080322a09315b
base_tree: ce97aae406e72794bb8d98009e19a90f3db3e503
verified: strong
---
# Self-improvement pass 4: guard heredoc precision, test lockout of the real claude, untrusted-text sinks, escapes, hunk …
## Raw request
> T-0282: Guard: parse 'cd DIR && python3 - <<EOF' heredocs like bare ones (an edit script whose strings mention import fmX is blocked only because of the cd prefix)
> T-0283: Tests can never reach the real claude: a lockout claude after the stub dirs in helpers PATH (a stub that fails to exec fell through to the real binary)
> T-0284: Adversary lens follows untrusted text to its sinks (terminal, model prompt, URL, shell, file path, git config) and the pre-audit flags network/ingest code
> T-0285: Escapes: a FIX/SECURITY request naming a done task logs an escape against it with the lenses that passed it; fm friction lists escapes
> T-0279: fm task prove --hunks skips new (untracked) files: a new module's code is never hunk-proven — split new files into per-definition hunks
## Interpretation
Pass 4 of the recursive self-improvement: five small fixes from grounded friction. Guard precision (never weaker), money safety in tests, a security lens that names sinks, escape tracking (review recall over time), and hunk proof that reaches new files.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0282: a `cd DIR && python3 - <<'EOF'` heredoc is parsed like a bare one — an edit script whose strings mention `import fmX` passes, real fm imports with mutator calls still block, and a `;`, pipe or `$(` in the cd chain keeps the text match — verify with `python3 plugin/tests/run.py -p test_pass4.py -k GuardHeredoc`
- [x] T-0283: in the test suite a `claude` that the PATH lookup reaches past the test's stub dirs is a lockout script that fails loudly, before any spend — verify with `python3 plugin/tests/run.py -p test_pass4.py -k Lockout`
- [x] T-0284: the adversary lens follows untrusted text to its sinks (terminal, model prompt, URL/network, shell, file path, git config/hooks), and the pre-audit marks network/ingest code security-sensitive — verify with `python3 plugin/tests/run.py -p test_pass4.py -k Sinks`
- [x] T-0285: capturing or creating a FIX/SECURITY request that names a done task records an escape against it (with the lenses that passed it), and fm friction lists escapes — verify with `python3 plugin/tests/run.py -p test_pass4.py -k Escapes`
- [x] T-0279: fm task prove --hunks splits a new Python file into its top-level definitions and removes each alone, naming an untested one — verify with `python3 plugin/tests/run.py -p test_pass4.py -k NewFiles`
## Non-goals
## Approach (options → choice → why)
Guard: allow a leading chain of plain `cd PATH &&` before `python - <<` (the cd target without shell metacharacters), keep every other check → the AST proof runs on more real edit scripts; no new relaxation beyond the cd. Lockout: a temp dir with a failing `claude` appended right after os.environ PATH's stub positions — tests prepend stub dirs to os.environ['PATH'], so prepending the lockout to os.environ PATH at helpers import puts it after every stub and before the real binary. Sinks: words in audit.md's adversary prompt + _SENSITIVE_CODE patterns. Escapes: at capture/task new, T-ids in the text that are done → ledger event escape; friction section. New files: per-definition mutations via ast for added .py files.
## Risks and rollback
Guard change is security-relevant: tests must show real fm drives still block with the cd prefix and with metacharacters in the chain. Rollback: revert the commit.
## Execution prompt
## Steps
1. [x] T-0282: Guard: parse 'cd DIR && python3 - <<EOF' heredocs like bare ones (an edit script whose str
2. [x] T-0283: Tests can never reach the real claude: a lockout claude after the stub dirs in helpers PAT
3. [x] T-0284: Adversary lens follows untrusted text to its sinks (terminal, model prompt, URL, shell, fi
4. [x] T-0285: Escapes: a FIX/SECURITY request naming a done task logs an escape against it with the lens
5. [x] T-0279: Fm task prove --hunks skips new (untracked) files: a new module's code is never hunk-prove
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md, plugin/skills/intake/references/audit.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_pass4.py` → ✗ exit 1 · Ran 5 tests in 0.5s (5 classes, 16 at a time; slowest: Escapes 0s, NewFiles 0s, Sinks 0s) / FAILED (5 classes) [ran] [tree 10bcbcb71fea] (2026-10-04T08:30:49Z)
- (step 1) `python3 plugin/tests/run.py -p test_pass4.py -k GuardHeredoc` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: GuardHeredoc 0s) / OK [ran] [tree 277382ccc253] (2026-10-04T08:32:38Z)
- (step 2) `python3 plugin/tests/run.py -p test_pass4.py -k Lockout` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Lockout 0s) / OK [ran] [tree 277382ccc253] (2026-10-04T08:32:38Z)
- (step 3) `python3 plugin/tests/run.py -p test_pass4.py -k Sinks` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Sinks 0s) / OK [ran] [tree 277382ccc253] (2026-10-04T08:32:39Z)
- (step 4) `python3 plugin/tests/run.py -p test_pass4.py -k Escapes` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Escapes 1s) / OK [ran] [tree 277382ccc253] (2026-10-04T08:32:40Z)
- (step 5) `python3 plugin/tests/run.py -p test_pass4.py -k NewFiles` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: NewFiles 0s) / OK [ran] [tree 277382ccc253] (2026-10-04T08:32:40Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  integrity            6 repo(s) and state intact / fm doctor: OK (24 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.9    32.0     150  [0] / SessionEnd                  28.4    29.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 08:06 UTC; python3 plugin/tests/run.py → exit 0 · Ran 773 te [ran] [tree 277382ccc253] (2026-10-04T08:33:38Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p "test_pass4.py" && python3 plugin/tests/run.py -p "test_hunks*"` → 9/12 hunks proven; unproven: plugin/lib/fmcli.py @@ -597 +647 @@ def task_prove_hunks(p, b, args):; plugin/lib/fmcli.py @@ -801,0 +851,2 @@ def task_new(p, args):; plugin/lib/fmguard.py @@ -699 +699,2 @@ def _python_units(cmd): [inconclusive] [ran] [tree 277382ccc253] (2026-10-04T08:33:57Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p "test_pass4.py" && python3 plugin/tests/run.py -p "test_hunks*"` → 10/12 hunks proven; unproven: plugin/lib/fmcli.py @@ -597 +647 @@ def task_prove_hunks(p, b, args):; plugin/lib/fmguard.py @@ -699 +699,2 @@ def _python_units(cmd): [inconclusive] [ran] [tree 74b81624da38] (2026-10-04T08:34:20Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  integrity            6 repo(s) and state intact / fm doctor: OK (24 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.0    32.4     150  [0] / SessionEnd                  27.7    29.4     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 08:06 UTC; python3 plugin/tests/run.py → exit 0 · Ran 775 te [ran] [tree c2e3c0bd9e35] (2026-10-04T08:39:30Z)
- (step 1) `python3 plugin/tests/run.py -p test_pass4.py -k GuardHeredoc` → exit 0 · Ran 3 tests in 0.1s (1 classes, 16 at a time; slowest: GuardHeredoc 0s) / OK [ran] [tree c2e3c0bd9e35] (2026-10-04T08:39:45Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p "test_pass4.py" && python3 plugin/tests/run.py -p "test_hunks*" && python3 plugin/tests/run.py -p "test_guard*"` → 15/20 hunks proven, 5 more not run (--max); unproven: plugin/lib/fmcli.py @@ -597 +647 @@ def task_prove_hunks(p, b, args):; plugin/lib/fmguard.py @@ -339 +373 @@ def _live_heredocs(cmd):; plugin/lib/fmguard.py @@ -358 +392 @@ def _heredocs(cmd):; plugin/lib/fmguard.py @@ -382 +416 @@ def _drop_data_heredocs(cmd):; plugin/lib/fmguard.py @@ -699 +733,2 @@ def _python_units(cmd): [inconclusive] [ran] [tree c2e3c0bd9e35] (2026-10-04T08:40:17Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p "test_pass4.py" && python3 plugin/tests/run.py -p "test_hunks*" && python3 plugin/tests/run.py -p "test_guard*"` → 21/25 hunks proven; unproven: plugin/lib/fmcli.py @@ -597 +647 @@ def task_prove_hunks(p, b, args):; plugin/lib/fmguard.py @@ -339 +373 @@ def _live_heredocs(cmd):; plugin/lib/fmguard.py @@ -358 +392 @@ def _heredocs(cmd):; plugin/lib/fmguard.py @@ -699 +733,2 @@ def _python_units(cmd): [inconclusive] [ran] [tree f1a1ddf31c7d] (2026-10-04T08:41:13Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p "test_pass4.py" && python3 plugin/tests/run.py -p "test_hunks*" && python3 plugin/tests/run.py -p "test_guard*"` → 23/26 hunks proven; unproven: plugin/lib/fmcli.py @@ -546 +613,0 @@ def task_prove_hunks(p, b, args):; plugin/lib/fmcli.py @@ -597 +672 @@ def task_prove_hunks(p, b, args):; plugin/lib/fmguard.py @@ -699 +733,2 @@ def _python_units(cmd): [inconclusive] [ran] [tree 5392f27f37fa] (2026-10-04T08:44:00Z)
- (step 1) `python3 plugin/tests/run.py -p test_pass4.py -k GuardHeredoc` → exit 0 · Ran 4 tests in 0.1s (1 classes, 16 at a time; slowest: GuardHeredoc 0s) / OK [ran] [tree c74785bb61c1] (2026-10-04T08:44:11Z)
- (step 5) `python3 plugin/tests/run.py -p test_pass4.py -k NewFiles` → exit 0 · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: NewFiles 1s) / OK [ran] [tree c74785bb61c1] (2026-10-04T08:44:12Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  integrity            6 repo(s) and state intact / fm doctor: OK (24 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.3    32.2     150  [0] / SessionEnd                  28.4    29.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 08:06 UTC; python3 plugin/tests/run.py → exit 0 · Ran 777 te [ran] [tree c74785bb61c1] (2026-10-04T08:45:04Z)
- (ac 1) `python3 plugin/tests/run.py -p test_pass4.py -k GuardHeredoc` → exit 0 · Ran 4 tests in 0.1s (1 classes, 16 at a time; slowest: GuardHeredoc 0s) / OK [ran] [tree c74785bb61c1] (2026-10-04T08:45:14Z)
- (ac 2) `python3 plugin/tests/run.py -p test_pass4.py -k Lockout` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Lockout 0s) / OK [ran] [tree c74785bb61c1] (2026-10-04T08:45:14Z)
- (ac 3) `python3 plugin/tests/run.py -p test_pass4.py -k Sinks` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Sinks 0s) / OK [ran] [tree c74785bb61c1] (2026-10-04T08:45:14Z)
- (ac 4) `python3 plugin/tests/run.py -p test_pass4.py -k Escapes` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Escapes 1s) / OK [ran] [tree c74785bb61c1] (2026-10-04T08:45:14Z)
- (ac 5) `python3 plugin/tests/run.py -p test_pass4.py -k NewFiles` → exit 0 · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: NewFiles 1s) / OK [ran] [tree c74785bb61c1] (2026-10-04T08:45:14Z)
- (audit adversary) `one fm-reviewer pass, adversary-focused on the guard change (T-0286-review-1): 2 HIGH + 1 MEDIUM-HIGH parse mismatches between the guard's heredoc reading and bash's (continued starter line, a second <<\E form, a loosely matched delimiter) and 1 LOW-MEDIUM (a module in the cd target shadowing an import, a regression of this change in _proved_writes) — all reproduced as failing tests, then fixed once in check_bash (_join_continued) and in every splitter (_ends_body); guard replay over 5,000 real commands: 0 newly blocked, 0 newly allowed. Dogfooding prove --hunks exposed a T-0271 bug (zero-context reverse hunks applied at the wrong identical line) — reproduced, test-first, fixed with an exact revert; hunks 23/26 proven (rest: a removed unused import, a timeout-only label, a docstring). The non-guard members were covered by their tests, not by the reviewer` → guard parse now matches bash for continuations, delimiters, double heredoc forms and module shadowing; relaxation limited to plain cd chains [tree c74785bb61c1] (2026-10-04T08:45:14Z)
- (audit edge) `one fm-reviewer pass, adversary-focused on the guard change (T-0286-review-1): 2 HIGH + 1 MEDIUM-HIGH parse mismatches between the guard's heredoc reading and bash's (continued starter line, a second <<\E form, a loosely matched delimiter) and 1 LOW-MEDIUM (a module in the cd target shadowing an import, a regression of this change in _proved_writes) — all reproduced as failing tests, then fixed once in check_bash (_join_continued) and in every splitter (_ends_body); guard replay over 5,000 real commands: 0 newly blocked, 0 newly allowed. Dogfooding prove --hunks exposed a T-0271 bug (zero-context reverse hunks applied at the wrong identical line) — reproduced, test-first, fixed with an exact revert; hunks 23/26 proven (rest: a removed unused import, a timeout-only label, a docstring). The non-guard members were covered by their tests, not by the reviewer` → deleted files and new files in hunk reverts, <<- tab delimiters, relative cd without a known cwd (refused), a stub without a shebang [tree c74785bb61c1] (2026-10-04T08:45:14Z)
- (audit intent) `one fm-reviewer pass, adversary-focused on the guard change (T-0286-review-1): 2 HIGH + 1 MEDIUM-HIGH parse mismatches between the guard's heredoc reading and bash's (continued starter line, a second <<\E form, a loosely matched delimiter) and 1 LOW-MEDIUM (a module in the cd target shadowing an import, a regression of this change in _proved_writes) — all reproduced as failing tests, then fixed once in check_bash (_join_continued) and in every splitter (_ends_body); guard replay over 5,000 real commands: 0 newly blocked, 0 newly allowed. Dogfooding prove --hunks exposed a T-0271 bug (zero-context reverse hunks applied at the wrong identical line) — reproduced, test-first, fixed with an exact revert; hunks 23/26 proven (rest: a removed unused import, a timeout-only label, a docstring). The non-guard members were covered by their tests, not by the reviewer` → five member criteria each with a test class; T-0279 widened to the revert bug it exposed [tree c74785bb61c1] (2026-10-04T08:45:14Z)
## Log
- 2026-10-04T08:29:35Z created
- 2026-10-04T08:30:11Z focused
- 2026-10-04T08:32:31Z hypothesis: per-definition mutations for new .py files make NewFiles pass without changing the existing hunk tests (test_hunks)
- 2026-10-04T08:32:38Z confirmed: NewFiles and test_hunks green; ruled out a regression in git-hunk mutations
- 2026-10-04T08:37:44Z hypothesis: the continued-line bypass is in the general heredoc scan, not _python_units — every body splitter starts the body on the next physical line, while bash first joins a backslash-continued starter line, so the redirect on line 2 is read as body by all checks
- 2026-10-04T08:38:29Z confirmed: continued starter lines were joined by bash but not by any guard splitter; ruled out _python_units as the only site — fixed once in check_bash (_join_continued) and with exact body ends in all four splitters
- 2026-10-04T08:45:14Z done
- 2026-10-04T08:45:14Z committed e5cf898 (9 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-pass-4: Source: research/brainstorm-20261004-030846 (two lenses — reliability and trust in its own verdicts; user value — × 2 rounds, past passes 1–3…
- T-0170 [FIX M, done, 3 steps] Guard: 'driving Foreman's modules' reads real Python imports, not text that mentions them — lesson: Relax a guard by proving the safe case,…
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- decision 2026-10-04: Brainstorm pass 4: 4 grounded ideas (cd-prefixed python heredocs parsed by the guard, test lockout of the real claude, untrusted-text sinks in the a…
## Lessons
- A mutation tool must put each mutation exactly where the diff says: zero-context git apply drifts to the nearest identical line, crediting one hunk's verdict to another
## Files touched
- plugin/tests/test_pass4.py
- plugin/lib/fmguard.py
- plugin/tests/helpers.py
- plugin/skills/intake/references/audit.md
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/lib/fmfriction.py
- CHANGELOG.md
- MASTER.md
