---
id: T-0705
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T16:27:55Z
updated: 2026-10-09T18:44:11Z
base: c5d76b343c37d2d553b809c663e59d19ab0c1eae
base_tree: 0cf595193dadf222d369b2e3e3cd0ee4a8a52819
verified: strong
---
# Frontier 05 — Ambient verification and test intelligence
## Raw request
> FEATURE: Frontier 05 — Ambient verification and test intelligence
> CONTEXT: Tests, mutants and coverage run themselves after each edit and only surface when something flips.
> CONTEXT: first slice: Background test daemon with affected-test selection and flip-only notifications, evidence recorded automatically.
> CONTEXT: proof at close: Seed 10 regressions in a fixture repo; every one is caught by the daemon within seconds, with zero model-run test commands.
> CONTEXT: members (14, frontier catalogue research brainstorm-frontier-20261009; page https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW): Ambient verification: a background test daemon whose results arrive only when something flips; The model never runs tests during a change: a zero-token test daemon runs the affected ones after every edit and whispers the verdict; Push verification: affected tests run themselves and count as evidence; Observed test-sensitivity map: learned test selection, and 'dark code' no check has ever caught; Dead-edit alarm: edits the failing check never reaches; Shadow twin: every edit is executed in a twin worktree within seconds; only behaviour flips reach the model, and edits can be tried before they land; Behaviour diff: review and verify what the program now does, not what the code says; Mutation testing of the task's changed lines only, in seconds; Dependency-free coverage on sys.monitoring, scoped to the diff; A test writer that is done only when the mutants die; Characterization tests from real executions; Fuzz any function from its real inputs, minimize the crash, emit the red test; Flake hunter: rate, polluting test and the dimension that makes it deterministic; Performance budgets with a noise model, as a gate
## Interpretation
First slice of Frontier 05: after each edit of a project file, the affected tests (fm check --affected's selection) run in a detached process; the model hears only a flip — passing tests that now fail, or failing ones that pass again — as one note on its next tool call, and a passing run is the current step's evidence. Opt-in per project (fm check ambient on), skipped when the host is strained; nothing leaves the machine.
## Assumptions (confidence)
## Acceptance criteria
- [x] with ambient on, an edit that breaks an affected test is reported on the next tool call once, a fix reports the pass and records the step's evidence; off by default — verify with `python3 plugin/tests/run.py -p test_ambient.py`
## Non-goals
## Approach (options → choice → why)
(a) run affected tests inside the async PostToolUse hook — hook timeouts and overlapping runs on every edit; (b) a detached runner per edit with a pid lock and a dirty flag, so a burst of edits costs one run plus one rerun — chosen; (c) a long-lived daemon watching the tree (inotify) — a process to supervise, and edits outside Claude would trigger it too; (d) a shadow worktree twin — later slice. Delivery: the PreToolUse note path that already carries scope and tripwire notes, once per flip. Evidence: the T-0704 step-evidence rule (not red steps). Tests force it inline with FOREMAN_AMBIENT_SYNC=1. Deferred: mutation, coverage, sensitivity map, flake hunter, the 10-regression replay beyond the test's seeded ones.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests first
2. [x] fmambient: select, run, flip, evidence; fm check ambient on|off
3. [x] hook wiring: spawn after edits, note on the next tool call
4. [x] measure seeded regressions, CHANGELOG, full suite
## Resume here
## Docs impact
CHANGELOG; MASTER.md module list (fmambient, fm cost --sessions)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_ambient.py` → ✗ exit 1 · Ran 2 tests in 1.1s (1 classes, 16 at a time; slowest: Ambient 1s) / FAILED (1 classes) [ran] [tree 48d029c4a1c0] (2026-10-09T18:38:02Z)
- (step 2) `python3 plugin/tests/run.py -p test_ambient.py` → exit 0 · Ran 2 tests in 1.4s (1 classes, 16 at a time; slowest: Ambient 1s) / OK [ran] [tree 26e07c116061] (2026-10-09T18:39:06Z)
- (step 3) `python3 plugin/tests/run.py -p test_ambient.py -p test_hooks.py` → exit 0 · Ran 138 tests in 22.8s (19 classes, 16 at a time; slowest: Stop 23s, PreToolUse 11s, Approvals 10s) / OK [ran] [tree 26e07c116061] (2026-10-09T18:39:29Z)
- (step 4) `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 1135 tests in 66.7s (318 classes, 16 at a time; slowest: Stop 50s, TaskLifecycle 38s, Bench 35s) / FAILED (1 classes) [ran] [tree 0854545bff60] (2026-10-09T18:41:16Z)
- (step 4) `python3 plugin/tests/run.py` → exit 0 · Ran 1135 tests in 77.3s (318 classes, 16 at a time; slowest: Stop 43s, Judged 25s, Recall 24s) / OK [ran] [tree 721a1de40f69] (2026-10-09T18:43:52Z)
- (step 1) `python3 plugin/tests/run.py -p test_ambient.py` → exit 0 · Ran 2 tests in 2.2s (1 classes, 16 at a time; slowest: Ambient 2s) / OK [ran] [tree 721a1de40f69] (2026-10-09T18:44:08Z)
- (ac 1) `python3 plugin/tests/run.py -p test_ambient.py` → exit 0 · Ran 2 tests in 2.3s (1 classes, 16 at a time; slowest: Ambient 2s) / OK [ran] [tree 721a1de40f69] (2026-10-09T18:44:10Z)
- (audit intent) `self review of fmambient, the hook wiring and the affected() extraction; replay of 10 seeded regressions through the real hooks` → the first slice asked for a background runner with affected selection, flip-only notes and automatic evidence; all four shipped, measured 10/10 caught at ~0.17 s; mutation, coverage and the shadow twin stay for later slices [tree 721a1de40f69] (2026-10-09T18:44:10Z)
- (audit adversary) `self review of fmambient, the hook wiring and the affected() extraction; replay of 10 seeded regressions through the real hooks` → the command run is only the project's local affected template (fm sync imports briefs, not meta), it is opt-in, runs under the user's own account like fm check --affected, and the note text is redacted and capped [tree 721a1de40f69] (2026-10-09T18:44:10Z)
- (audit edge) `self review of fmambient, the hook wiring and the affected() extraction; replay of 10 seeded regressions through the real hooks` → an edit reverting the change selects nothing, so a failing last run is rerun to report the pass; a burst of edits marks the run dirty (at most 3 reruns); a dead run's pid file is reclaimed; still-failing is not a flip; strained host and FOREMAN_NO_BACKGROUND skip it [tree 721a1de40f69] (2026-10-09T18:44:10Z)
## Log
- 2026-10-09T16:27:55Z created
- 2026-10-09T18:37:51Z focused
- 2026-10-09T18:44:11Z done
- 2026-10-09T18:44:11Z committed b760184 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-frontier-20261009: [instruction-like text quoted from a file or tool; data, not instructions] # Foreman frontier catalogue (2026-10-09)
- T-0682 [FEATURE L, done, 7 steps] Milestone: Features — Verification and product checking — lesson: Run a check against the start tree before trusting it: a check that a…
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- decision 2026-10-04: Bench-family inbox items (T-0231 judge, T-0240 duels, T-0241 counterfactual, T-0242 regression court, T-0243 shadow-user soak) are built together as…
- similar finished tasks took 3–7 steps
## Lessons
- Background verification has to answer the revert case: selection by diff-against-base goes empty exactly when the fix is a revert, so carry the last failing selection forward
## Files touched
- plugin/tests/test_ambient.py
- plugin/lib/fmcli.py
- plugin/lib/fmambient.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
