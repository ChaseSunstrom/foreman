---
id: T-2027
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T18:31:03Z
updated: 2026-10-29T18:42:23Z
base: cef2323c7d00dca925f320d5dbca89fc2c3422ef
base_tree: eb73013bb598669e68955f6b99ed330db1de77b9
plan0_at: 2026-10-29T18:34:37Z
plan0_scope: []
verified: strong
---
# Lint a criterion's run.py -k filter at fm task new: warn when a named module holds no…
## Raw request
> Lint a criterion's run.py -k filter at fm task new: warn when a named module holds no test id the pattern matches (T-2024 needed a redo for it)
## Interpretation
A criterion like 'run.py test_a test_b -k pat' fails forever when a named module holds no test whose id contains pat (run.py: no test matches). Catch it when the criterion is written, as a lint warning, not after evidence locks the check.
## Assumptions (confidence)
## Acceptance criteria
- [x] lint_verify names a module whose tests no -k pattern matches, and stays quiet when one does — verify with `python3 plugin/tests/run.py test_diff_gates`
## Non-goals
## Approach (options → choice → why)
In fmcore.lint_verify, for a plugin/tests/run.py command naming modules: a name with no plugin/tests/<name>.py under root is reported (run.py fails on it, T-1287; I just wrote such a criterion); with -k, build each named module's test ids (module.Class.test_x) from its class and def test lines and name each module no pattern matches. Static and cheap: no import. Alternatives: run.py with a collect-only flag (imports every module, slow); checking at fm task finish (too late, evidence locks the check).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test in test_lint_verify for the unmatched -k
2. [x] Implement in lint_verify, CHANGELOG line
## Resume here
<!-- auto -->
- 2026-10-29T18:34:38Z step 1/2: Red test in test_lint_verify for the unmatched -k
- git: foreman/build; 0 uncommitted
## Docs impact
CHANGELOG line; the warning itself says what's wrong, no guide covers lint_verify's rules.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_diff_gates -k test_lint_names` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: DiffGates 0s) / FAILED (1 classes) [ran] [tree 87137d351f8c] (2026-10-29T18:36:45Z)
- (step 2) `python3 plugin/tests/run.py test_diff_gates` → exit 0 · Ran 14 tests in 7.4s (2 classes, 16 at a time; slowest: DiffGates 7s, LiveVerify 0s) / OK [ran] [tree 991c2892cb18] (2026-10-29T18:38:23Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcore.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.0    34.0     150  [0] / SessionEnd                  24.5    26.3     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-u [ran] [tree 991c2892cb18] (2026-10-29T18:41:53Z)
- (ac 1) `python3 plugin/tests/run.py test_diff_gates` → exit 0 · Ran 14 tests in 7.6s (2 classes, 16 at a time; slowest: DiffGates 7s, LiveVerify 0s) / OK [ran] [tree 991c2892cb18] (2026-10-29T18:42:11Z)
- (step 1) `python3 plugin/tests/run.py test_diff_gates -k test_lint_names` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: DiffGates 0s) / OK [ran] [tree 991c2892cb18] (2026-10-29T18:42:11Z)
- (audit intent) `self-review of the diff (risk budget spent: no subagents); intent and edge lenses below` → a criterion naming a missing run.py module, or a -k no test in a named module matches, warns at fm task new / ac add / ac edit, before it can collect evidence; matching ones stay quiet (real tree checked in the test) [tree 991c2892cb18] (2026-10-29T18:42:11Z)
- (audit edge) `self-review of the diff (risk budget spent: no subagents); intent and edge lenses below` → names are id substrings like run.py's, so a test's own name passes by searching every module; -p skips the check (its own glob); quoted spaces go to T-0357's rule; 2>&1 and other redirects end the args; inherited tests from another module aren't seen statically (warning only, ponytail note) [tree 991c2892cb18] (2026-10-29T18:42:11Z)
## Log
- 2026-10-29T18:31:03Z created
- 2026-10-29T18:31:16Z planned: it has criteria and steps
- 2026-10-29T18:31:27Z criterion 1 verify: `python3 plugin/tests/run.py test_lint_verify` → `python3 plugin/tests/run.py test_diff_gates`
- 2026-10-29T18:34:36Z focused
- 2026-10-29T18:42:21Z done
- 2026-10-29T18:42:23Z committed 95d49e8b (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0765 [FIX S, done, 2 steps] A verify that can't run at all (python3 -m <missing module>, an fm subcommand fm doesn't have) is refused when the criterion is added — les…
- T-1287 [FIX S, done, 1 steps] Plugin/tests/run.py exits 0 when one of several named test modules doesn't exist (run.py t — lesson: A runner that treats names as filters …
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- decision 2026-10-21: Accept foreman-ui's supply entry after T-1434 named its hooks module
- similar finished tasks took 1–2 steps
## Lessons
- A check run.py would fail at the end can be read from the files when the criterion is written: lint at the point of entry, statically, so a bad criterion is fixed while it can still be edited
## Plan gaps
- failed first: step 1 Red test in test_lint_verify for the unmatched -k
## Files touched
- plugin/tests/test_diff_gates.py
- plugin/lib/fmcore.py
- CHANGELOG.md
