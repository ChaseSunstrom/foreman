---
id: T-0271
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/, plugin/skills/, MASTER.md, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-04T07:05:46Z
updated: 2026-10-04T07:11:10Z
base: 2c4af45b45ba014df619af798e2fdf86b379d8f5
base_tree: 6f3011be89bb1a34b54adf90f4a62decbc45c970
verified: strong
---
# Hunk mutation proof: fm task prove --hunks
## Raw request
> Hunk mutation proof: fm task prove ID --hunks reverts each hunk of the task's diff alone and runs the criteria's checks; a hunk whose removal fails nothing is reported unproven
## Interpretation
Today a guard test passed for the wrong reason. A check proves a change only if undoing each part of the change makes it fail; fm task prove checks that for the whole diff at once, not per part.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task prove ID --hunks --run CMD reverts each code hunk of the task's diff alone in a scratch worktree and names every hunk whose removal still passes CMD — verify with `python3 plugin/tests/run.py -p "test_hunks*"`
- [x] all hunks proven records passing evidence; any unproven records an inconclusive line naming them (it never counts as passing) — verify with `python3 plugin/tests/run.py -p "test_hunks*" -k Evidence`
## Non-goals
## Approach (options → choice → why)
Options: (a) a mutation-testing library (mutmut — Python only, not stdlib, slow); (b) revert the task's own hunks one at a time (git diff -U0 from the task's start snapshot, git apply -R --unidiff-zero in a detached worktree of the current tree) and run the given check. Choice (b): language-agnostic, stdlib + git, and it tests exactly what the task changed. Code files only (tests stay current), at most --max hunks (default 20), each run with --timeout. Unproven hunks are recorded as inconclusive evidence — a signal to strengthen the check, never a pass.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Tests first: plugin/tests/test_hunks.py
2. [x] Implement prove --hunks in fmcli (worktree at the current tree, git apply -R per hunk, restore, run)
3. [x] Docs: MASTER.md, CHANGELOG.md, references/verification.md
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md, plugin/skills/intake/references/execute.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p "test_hunks*"` → ✗ exit 1 · Ran 3 tests in 0.5s (2 classes, 16 at a time; slowest: Hunks 0s, Evidence 0s) / FAILED (2 classes) [ran] [tree 2610005740d1] (2026-10-04T07:06:33Z)
- (step 2) `fm task prove --hunks: python3 plugin/tests/run.py -p "test_hunks*"` → exit 0 · 4/4 hunks proven [ran] [tree 4f46c6b00bce] (2026-10-04T07:07:23Z)
- (step 3) `grep -c 'hunks' MASTER.md CHANGELOG.md plugin/skills/intake/references/execute.md` → exit 0 · CHANGELOG.md:1 / plugin/skills/intake/references/execute.md:1 [ran] [tree 9fba7641bd71] (2026-10-04T07:07:41Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  integrity            6 repo(s) and state intact / fm doctor: OK (24 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.7    31.7     150  [0] / SessionEnd                  28.0    29.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 06:33 UTC; python3 plugin/tests/run.py → exit 0 · Ran 723 te [ran] [tree 9fba7641bd71] (2026-10-04T07:08:29Z)
- (step 2) `python3 plugin/tests/run.py -p "test_hunks*"` → exit 0 · Ran 5 tests in 1.3s (2 classes, 16 at a time; slowest: Hunks 1s, Evidence 1s) / OK [ran] [tree be66567c7cb0] (2026-10-04T07:10:12Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  integrity            6 repo(s) and state intact / fm doctor: OK (24 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.1    33.8     150  [0] / SessionEnd                  28.5    31.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 06:33 UTC; python3 plugin/tests/run.py → exit 0 · Ran 725 te [ran] [tree be66567c7cb0] (2026-10-04T07:11:02Z)
- (ac 1) `python3 plugin/tests/run.py -p "test_hunks*"` → exit 0 · Ran 5 tests in 1.3s (2 classes, 16 at a time; slowest: Hunks 1s, Evidence 1s) / OK [ran] [tree be66567c7cb0] (2026-10-04T07:11:10Z)
- (ac 2) `python3 plugin/tests/run.py -p "test_hunks*" -k Evidence` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Evidence 1s) / OK [ran] [tree be66567c7cb0] (2026-10-04T07:11:10Z)
- (audit intent) `fm-reviewer pass over all lenses (research T-0271-review-1); 2 HIGH + 2 MEDIUM + 2 LOW fixed with tests; dogfooded on its own diff (4/4 hunks proven)` → criteria met — per-hunk revert names what the check doesn't notice; working tree never touched [tree be66567c7cb0] (2026-10-04T07:11:10Z)
- (audit adversary) `fm-reviewer pass over all lenses (research T-0271-review-1); 2 HIGH + 2 MEDIUM + 2 LOW fixed with tests; dogfooded on its own diff (4/4 hunks proven)` → fixed — no pass without a full run (skipped, --max-cut or zero tested is inconclusive), baseline run on the unchanged scratch tree, timeouts not counted as caught [tree be66567c7cb0] (2026-10-04T07:11:10Z)
- (audit edge) `fm-reviewer pass over all lenses (research T-0271-review-1); 2 HIGH + 2 MEDIUM + 2 LOW fixed with tests; dogfooded on its own diff (4/4 hunks proven)` → fixed — tab-terminated paths with spaces, deleted files reset+cleaned between hunks, literal pathspecs, commit-tree failure (and gpgsign) reported first [tree be66567c7cb0] (2026-10-04T07:11:10Z)
- (audit operator) `fm-reviewer pass over all lenses (research T-0271-review-1); 2 HIGH + 2 MEDIUM + 2 LOW fixed with tests; dogfooded on its own diff (4/4 hunks proven)` → ok — docs; --max bounds the runs [tree be66567c7cb0] (2026-10-04T07:11:10Z)
- (audit maintainer) `fm-reviewer pass over all lenses (research T-0271-review-1); 2 HIGH + 2 MEDIUM + 2 LOW fixed with tests; dogfooded on its own diff (4/4 hunks proven)` → ok — ponytail note on hunk granularity [tree be66567c7cb0] (2026-10-04T07:11:10Z)
## Log
- 2026-10-04T07:05:46Z created
- 2026-10-04T07:06:20Z planned from capture
- 2026-10-04T07:06:21Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/', 'plugin/skills/', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-04T07:06:21Z focused
- 2026-10-04T07:11:10Z done
- 2026-10-04T07:11:10Z committed fdc3f35 (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-pass-2: Source: research/brainstorm-20261004-020314 (4 lenses × 2 rounds, past pass 1 and three earlier lists; 82 new titles). Pack: pass 1's results…
- research t0016-maintainer: ds failures from removing tracked plugins/marketplaces only as a print statement (`err = ...; print(f\"Could not remove {what} {name}: {err}\"…
- T-0170 [FIX M, done, 3 steps] Guard: 'driving Foreman's modules' reads real Python imports, not text that mentions them — lesson: Relax a guard by proving the safe case,…
- T-0261 [FEATURE M, done, 4 steps] Evidence quality: inconclusive runs, assumed vs verified facts, surprise log — lesson: Filtering a marked line out of the one accessor …
## Lessons
- A proof tool must first show its check passes on the unmodified input; otherwise every mutation 'fails' and a broken check proves everything
## Files touched
- plugin/tests/test_hunks.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/intake/references/execute.md
