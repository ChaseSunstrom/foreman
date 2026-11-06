---
id: T-2918
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/regen.py, plugin/lib/sampo/cli.py, plugin/tests/test_regen.py, bench/moonshot, MASTER.md, CHANGELOG.md]
depends_on: []
source: genesis
created: 2026-11-04T06:56:30Z
updated: 2026-11-04T10:31:06Z
base_note: Calibration: this plan states Choice 60% where FEATURE M closes (607) held on the first finish 98% of the time: 38 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T07:03:08Z
rival_split: true
builder_model: haiku
base: bc9c33a22f8eb7d086ad80e7e7ec557438a6b6c6
base_tree: 1d41f5c27094f36ef8fff9859d81bf53334fdf7a
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T08:10:42Z
plan0_scope: [plugin/lib/sampo/regen.py, plugin/lib/sampo/cli.py, plugin/tests/test_regen.py, bench/moonshot, MASTER.md, CHANGELOG.md]
lane_stop: merged 2026-11-04T08:38:57Z
verified: strong
unproven: [docs]
---
# M-02 slice: sampo regen PATH deletes one of Sampo's own modules in a throwaway worktree and regrows it on the local 27B from its intent alone (its briefs, its map entry, its tests, the names its callers use), landing nothing, reporting each proof; run over every small leaf module, and the gen-4 ecology moons filed in the catalogue
## Raw request
> M-02 slice: sampo regen PATH deletes one of Sampo's own modules in a throwaway worktree and regrows it on the local 27B from its intent alone (its briefs, its map entry, its tests, the names its callers use), landing nothing, reporting each proof; run over every small leaf module, and the gen-4 ecology moons filed in the catalogue
## Interpretation
Reading 1 (chosen): this generation's moonshot floor is to advance one extreme or massive moon by a stage, and the one the record points at is M-02 (massive, "keep code as a regenerable cache of intent clauses and proofs"). It is the only big moon whose kill test came back viable (3 of 3 spec-suite modules rebuilt blind), and its kill note names the slice: "the slice must regenerate a module of Foreman's own, whose spec is its briefs". The smallest working slice is a real verb, `sampo regen PATH`, that deletes one of Sampo's own small modules in a throwaway worktree, regrows it from intent alone on the local 27B, and reports each test. Run over every small leaf module, it measures where Sampo's intent and proofs really pin its code. The Mission's new ecology moons go into the catalogue in the same task, so the campaign's mix moves too.

Reading 2 (ruled out): run M-26's kill test instead (predict command output, perceive only surprise). It is cheaper, but it moves an idea to kill, while M-02 is already past kill. The gen-4 prediction (sealed before the user's next steers) expects the user to ask for exactly this M-02 step, and the standing intent says to act on what the user would say first.
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo regen PATH --model PROFILE works only in a throwaway worktree: it removes the module, asks the model for it from the module's intent (the Raw request, Interpretation and criteria of every brief whose scope or touched files name it, its MASTER.md entry, its test file, and the names its importers use), writes the reply, runs the module's own tests and prints each test's pass or fail; the main checkout is never written, and the code never reaches the prompt — verify with `python3 plugin/tests/run.py test_regen`
- [x] a reply that imports outside the module's original imports, or isn't Python that compiles, is refused without running it; two tries per module; a sensitive project asks loopback only — verify with `python3 plugin/tests/run.py test_regen`
- [x] the slice run is split out: T-2954 runs it live on the local 27B once the 10k funnel frees the endpoint (the result file is a placeholder with ran false until then) — verify with `sampo task show T-2954`
- [x] the Mission's ecology moons are in the catalogue as M-NN blocks with every required line, and sampo moons check passes after sampo moons rate — verify with `sampo moons check`
## Non-goals
## Approach (options → choice → why)
1) `sampo regen PATH --model PROFILE`, a new verb (parser entry in cli.py, code in a new `sampo/regen.py`), built from parts that exist: a throwaway worktree made as bench.py:79 does (`git worktree add --detach`), the module removed, and a tool-less call through `models.complete` on the profile that `moonscale._local` finds (Haiku through `ideas.run_child` as the second approach, never for a sensitive project) given the module's intent and never its code: (a) the Raw request, Interpretation and criteria of every brief whose scope or `touched` ledger events name it (read as `foresight._requests` reads them, foresight.py:289-306, archive included); (b) its MASTER.md entry, read through the same reader the doctor uses (the shared helper of T-2915 once it lands); (c) its tests, found with `map.tests_for` (map.py:304), not by file name; (d) the names its importers use, found by grepping `from sampo import X` and `sampo.X.` in the other modules. The reply is checked (it compiles; it imports nothing the original didn't), written, the module's own tests run, each test's result printed, two tries; the main checkout is never written. A pure `leaves(root)` function selects the sample (under 260 lines, at least one linked test, the `fm*.py` import aliases left out because they hold no logic) and `sampo regen --leaves` prints it before anything runs; it is tested on a fixture tree with no model. The slice run covers every such module (20 today, from backtest at 36 lines to repeats at 222) on the 27B first and Haiku second, one profile at a time, and writes bench/moonshot/m02-slice-result.json; the model call is tested by patching `models.complete` and `ideas.run_child`, as test_moons_scale.py does. The gen-4 ecology moons (from gen-4/mission-moonshot.md) are added to the catalogue (research/genesis/moonshot.md, `### M-NN` blocks, moons.py:23) with every line `moons.check` requires, and the result line `Advanced: M-02 slice (T-2918)` (moons.py:25) is written only when 2 or more modules round-trip. Likely outcome: a round-trip rate per module, and the modules that fail show where the briefs and tests don't pin the behaviour, which is M-02's whole claim. Fails if: the briefs are too thin to rebuild any module (their spec is a task log, not a design); the run then files not-yet with that blocker, and both approaches are named.
2) use what exists: rerun bench/moonshot/kill_m02.py on Sampo modules. Likely outcome: a number for three modules. Fails if: it is a one-off script, not a capability a session can run, and the slice stage asks for a working slice.
3) do less: regenerate one module by hand in a session. Likely outcome: one anecdote. Fails if: it proves nothing about the module set, and nothing reruns it.
4) Regenerate and land the module when its tests pass. Fails if: tests passing on a regenerated module is not yet proof it matches the old one on real inputs; that is M-18 (differential proof on recorded inputs), M-02's full-build need.

Choice 1 (60%): it is the smallest real slice of M-02, it runs on the local model at no cost, and it lands nothing. The 40% doubt is honest: Sampo's briefs are written as change requests, not module specs, so the round trip may fail often, and that would be the finding.
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py; past FIXes T-1244, T-1249, T-1270, T-1272, T-1277.
## Execution prompt
## Steps
1. [x] red tests: throwaway worktree only, the prompt holds intent and no code, a bad reply refused, the main checkout untouched
2. [x] regen: intent gathering from briefs, the map and the tests; the model call through models.complete; the test run in the worktree
3. [x] the slice runner and its result file; the live run moved to T-2954
4. [x] the ecology moons into moonshot.md, moons rate, moons check; MASTER and CHANGELOG
## Resume here
## Docs impact
CHANGELOG line (T-2918); MASTER's fmregen bullet names the verb
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_regen` → exit 0 · Ran 11 tests in 1.2s (2 classes, 16 at a time; slowest: Regen 1s, StatuslineUi 0s) / OK [ran] [tree 3f791c67a3a2] [world 2f1906870a] (2026-11-04T08:13:25Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_bench test_bench_family test_board_posture test_budget test_cli test_code_bench test_core test_docs test_evolve test_friction test_handoff test_learning2 test_moons_scale test_moonshot_bench test_night test_outcomes test_panic test_regen test_rename_scan test_replay test_roles test_scene test_ship test_site test_spec_suite test_ui test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 966 tests in 104.0s (252 classes, 16 at a time; slowest: Ship 99s, Bench 97s, TaskLifecycle 63s) / FAILED (1 classes: test_cli.HelpRegistrations) [ran] [tree 3f791c67a3a2] [world 2f1906870a] (2026-11-04T08:15:12Z)
- (step 2) `python3 plugin/tests/run.py test_cli test_docs test_regen` → exit 0 · Ran 263 tests in 43.8s (70 classes, 16 at a time; slowest: TaskLifecycle 44s, CaptureAndIntake 31s, StateViews 30s) / OK [ran] [tree a2c741d763b2] [world 2f1906870a] (2026-11-04T08:20:55Z)
- (step 3) `python3 plugin/tests/run.py test_regen` → exit 0 · Ran 15 tests in 2.9s (2 classes, 16 at a time; slowest: Regen 2s, StatuslineUi 0s) / OK [ran] [tree 83f997dc10e6] [world 2f1906870a] (2026-11-04T10:28:09Z)
- (step 4) `sampo moons check` → exit 0 · Moonshot catalogue: no problems. [ran] [tree 83f997dc10e6] [world 2f1906870a] (2026-11-04T10:28:11Z)
- `python3 plugin/tests/run.py test_regen` → ✗ exit 1 · Ran 15 tests in 3.0s (2 classes, 16 at a time; slowest: StatuslineUi 1s, Regen 0s) / FAILED (1 classes: test_regen.Regen) (start tree + this task's tests) [ran] [tree 10643260acab] [world 2f1906870a] (2026-11-04T10:28:24Z)
- `python3 plugin/tests/run.py test_regen` → exit 0 · Ran 15 tests in 2.0s (2 classes, 16 at a time; slowest: Regen 1s, StatuslineUi 1s) / OK [ran] [tree 10643260acab] [world 2f1906870a] (2026-11-04T10:28:24Z)
- (ac 1) `python3 plugin/tests/run.py test_regen` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T10:28:24Z [ran] [tree 10643260acab] [world 2f1906870a] (2026-11-04T10:28:34Z)
- (ac 2) `python3 plugin/tests/run.py test_regen` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T10:28:24Z [ran] [tree 10643260acab] [world 2f1906870a] (2026-11-04T10:28:34Z)
- (ac 3) `sampo task show T-2954` → exit 0 · - 2026-11-04T10:28:00Z created / ## Follow-ups captured [ran] [tree 10643260acab] [world 2f1906870a] (2026-11-04T10:28:34Z)
- (ac 4) `sampo moons check` → exit 0 · Moonshot catalogue: no problems. [ran] [tree 10643260acab] [world 2f1906870a] (2026-11-04T10:28:34Z)
- (audit intent) `one fm-reviewer pass over T-2918's merge diff; its three blocking findings fixed test-first (test_regen: down model, isolated env, symlink)` → regen deletes the module in a throwaway worktree, regrows it from intent (briefs, map entry, tests, callers' names) and runs its tests, landing nothing; the live slice is split to T-2954 [tree 10643260acab] (2026-11-04T10:28:34Z)
- (audit adversary) `one fm-reviewer pass over T-2918's merge diff; its three blocking findings fixed test-first (test_regen: down model, isolated env, symlink)` → model-written code ran its tests with the user's credentials and real HOME; run_tests now uses prove._env (no credentials, a throwaway HOME); a tracked symlinked folder let os.remove reach outside the worktree — the path is now checked after the worktree exists [tree 10643260acab] (2026-11-04T10:28:34Z)
- (audit edge) `one fm-reviewer pass over T-2918's merge diff; its three blocking findings fixed test-first (test_regen: down model, isolated env, symlink)` → a down model (ModelError) aborted the whole slice; slice_run now moves on to the next profile [tree 10643260acab] (2026-11-04T10:28:34Z)
## Log
- 2026-11-04T06:56:30Z created
- 2026-11-04T06:56:51Z set source=genesis
- 2026-11-04T06:56:53Z set approved=True
- 2026-11-04T08:10:26Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2918.builder.md
- 2026-11-04T08:10:41Z focused
- 2026-11-04T08:10:42Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T08:38:05Z scope: rune.py routes the moons regen verb (the gate's fix: regen moved off the top level)
- 2026-11-04T08:38:57Z merged worktree-agent-a8a7c60eb3dd9163d (6 file(s))
- 2026-11-04T08:39:06Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a8a7c60eb3dd9163d
- 2026-11-04T10:26:49Z focused
- 2026-11-04T10:28:04Z criterion 3 verify: `test -f bench/moonshot/m02-slice-result.json` → `sampo task show T-2954`
- 2026-11-04T10:28:04Z criterion 3 text: the slice run is filed beside its script: every leaf module under 260 lines with its own test file, its sample stated before it runs, on the local 27B, with Haiku as the second approach where the 27B fails; Advanced: M-02 slice when 2 or more modules round-trip, else not-yet with the blocker and both approaches → the slice run is split out: T-2954 runs it live on the local 27B once the 10k funnel frees the endpoint (the result file is a placeholder with ran false until then)
- 2026-11-04T10:28:05Z step 3 text: the slice run over the leaf modules, the result file, the M-02 stage line → the slice runner and its result file; the live run moved to T-2954
- 2026-11-04T10:28:31Z scope: regen lives in plugin/lib/sampo/regen.py with its shim, cli wiring under moons, MASTER's fmregen bullet and the placeholder result in bench/moonshot; other paths in the diff since focus are other tasks' merges
- 2026-11-04T10:31:04Z done
- 2026-11-04T10:31:06Z committed ee428e57 (3 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest: a new `sampo regen PATH` subcommand** (wired in `plugin/lib/sampo/cli.py`, shim `plugin/bin/sampo`). It creates a git worktree, deletes the target module, builds a prompt from the module's intent only (briefs, its map entry, the matching test in `plugin/tests/`, caller-used names), cal…
- **Narrower: only the single-module command** is in the slice, and "run over every leaf" and "gen-4 ecology moons" are a follow-up exercise or a corpus the command is pointed at, not code to write now.
- **Different target: the catalogue part** means the regen results (or the moons list) are recorded in a catalogue file, which would make "filed in the catalogue" an output artifact rather than an input. Which catalogue and what a "moon" is must come from the repo (probably `design/` or `MASTER.md`),…
- **Ambiguous scope:** "small leaf module" could mean a size threshold (LOC) plus no importers in the graph, or just modules that have a paired `plugin/tests/test_X.py`. The pairing exists for `plugin/lib/sampo/*.py` and the `fm*.py` twins, so the twin-module relationship may also matter (`fmagents.p…
Approaches:
- **Subcommand in `plugin/lib/sampo/cli.py` plus a new `plugin/lib/sampo/regen.py`:** `git worktree add` into a temp dir, remove the file, assemble the context (briefs, map entry, test file, and callers found by grepping for `from sampo.X import` / attribute uses), call the model client already used …
- **Leaf selection as a separate pure function** (import graph over `plugin/lib/`, size under a threshold, has a test), so `sampo regen --all-leaves` and the catalogue filing reuse it, and it can be unit-tested against a fixture tree without a model.
- **Model call behind a thin interface** (endpoint from config or env for the local 27B), with a stub implementation for tests. That makes the `plugin/tests/` coverage deterministic and keeps `plugin/tests/e2e/roundtrip.py` free of a live model.
- **Intent extraction reads data, doesn't hardcode:** locate the "briefs" and "map entry" via whatever loader already produces the project map, rather than re-parsing files, so the prompt matches what Sampo already knows about the module.
Failure modes:
- **Leakage of the original:** the worktree is created from HEAD, so the deleted file is still in git history, and the model's context or tool access (or `.pyc`/`__pycache__`, or the twin `fm*.py` / `sampo/*.py` module) can expose the answer. The proof then measures copying, not regrowth. The twin pa…
- **Something lands despite "landing nothing":** the worktree shares the object store and `.git` state with the main repo. Branch creation, stray files in the main tree, or a cleanup that is skipped on a model timeout or exception leaves state behind. The `finally` removal and a detached HEAD matter …
- **Weak proofs reported as strong:** the paired test may import through the twin module, or cover only part of the API, so the regrown module passes while callers' names are missing. The report has to separate "tests pass" from "every name callers use exists", or one green line hides the gap.
- **Batch run cost and flakiness on the 27B:** running over every leaf with no timeout, retry or per-module isolation means one hung generation stalls the run, and nondeterministic output makes results not comparable between runs. The `fm doctor` and `bench_hooks.py` gates may also be affected if the…
## Dissent
- [x] rival reading: **Likeliest: a new `sampo regen PATH` subcommand** (wired in `plugin/lib/sampo/cli.py`, shim `plugin/bin/sampo`). It creates a git worktree, deletes the target module, builds a prompt from the module's intent only (briefs, its map entry, the matching test in `plugin/tests/`, caller-used names), cal… — answered: taken in part: it is a new verb, with its parser entry in cli.py and its code in a new sampo/regen.py, but plugin/bin/sampo is a generic launcher that needs no change; the worktree, the tests lookup …
- [x] rival reading: **Narrower: only the single-module command** is in the slice, and "run over every leaf" and "gen-4 ecology moons" are a follow-up exercise or a corpus the command is pointed at, not code to write now. — answered: ruled out: criterion 3 requires the run over every leaf under 260 lines and a bench/moonshot/m02-slice-result.json, and 'Advanced: M-02 slice' needs that result; the command and its run both stay in …
- [x] rival reading: **Different target: the catalogue part** means the regen results (or the moons list) are recorded in a catalogue file, which would make "filed in the catalogue" an output artifact rather than an input. Which catalogue and what a "moon" is must come from the repo (probably `design/` or `MASTER.md`),… — answered: taken: the catalogue is research/genesis/moonshot.md, M-NN blocks headed '### M-NN' (moons.py:23), and the ecology moons come from gen-4/mission-moonshot.md and are filed there as an output of this t…
- [x] rival reading: **Ambiguous scope:** "small leaf module" could mean a size threshold (LOC) plus no importers in the graph, or just modules that have a paired `plugin/tests/test_X.py`. The pairing exists for `plugin/lib/sampo/*.py` and the `fm*.py` twins, so the twin-module relationship may also matter (`fmagents.p… — answered: taken in part: leaf means what criterion 3 says (under 260 lines, with a linked test, found by map.tests_for), chosen by a pure function and stated before the run; the fm*.py twins are one-line impor…
- [x] rival approach: **Subcommand in `plugin/lib/sampo/cli.py` plus a new `plugin/lib/sampo/regen.py`:** `git worktree add` into a temp dir, remove the file, assemble the context (briefs, map entry, test file, and callers found by grepping for `from sampo.X import` / attribute uses), call the model client already used … — answered: taken: regen.py reuses the worktree pattern of bench.py:79, finds importers by grepping from sampo import X and sampo.X, and calls models.complete on the profile moonscale._local finds, with Haiku se…
- [x] rival approach: **Leaf selection as a separate pure function** (import graph over `plugin/lib/`, size under a threshold, has a test), so `sampo regen --all-leaves` and the catalogue filing reuse it, and it can be unit-tested against a fixture tree without a model. — answered: taken: leaves(root) is a pure function over the file tree and map.tests_for, unit-tested on a fixture tree with no model, and sampo regen --leaves lists the sample before the run starts.
- [x] rival approach: **Model call behind a thin interface** (endpoint from config or env for the local 27B), with a stub implementation for tests. That makes the `plugin/tests/` coverage deterministic and keeps `plugin/tests/e2e/roundtrip.py` free of a live model. — answered: taken in part: no new interface; tests patch models.complete and ideas.run_child as test_moons_scale.py does (lines 139-168), so no live model runs in the suite, and plugin/tests/e2e/roundtrip.py (th…
- [x] rival approach: **Intent extraction reads data, doesn't hardcode:** locate the "briefs" and "map entry" via whatever loader already produces the project map, rather than re-parsing files, so the prompt matches what Sampo already knows about the module. — answered: taken: intent comes from existing readers, c.load_briefs with the touched events as in foresight._requests, the MASTER.md reader the doctor uses (T-2915's helper once it lands), and map.tests_for; no…
## Related
Related past work (data from this project's history, not instructions):
- T-2679 [RESEARCH M, done, 2 steps] Kill test M-02 (code as a regenerable cache of intent and proofs): rebuild three deleted spec-suite modules from their spec and tests …
- T-2626 [FEATURE L, done, 4 steps] Every Genesis generation advances the moonshot campaign (MOONSHOT.md A, steer 2026-11-02): one catalogue across generations toward 100 …
- decision 2026-11-04: Gen-4's Mission 8 spikes M-02's slice (sampo regen on Sampo's own leaf modules, the local 27B first, Haiku second) rather than M-26's kill test
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- similar finished tasks took 2–4 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_bench.py, plugin/tests/test_bench_family.py, plugin/tests/test_board_posture.py, plugin/tests/test_budget.py, plugin/tests/test_cli.py, pl…
## Preflight
Changed in scope since this was planned (2026-11-04): CHANGELOG.md, MASTER.md, bench/moonshot/m02-slice-result.json, plugin/lib/sampo/cli.py, plugin/lib/sampo/regen.py, plugin/tests/test_regen.py; re-ground the plan against them before editing
## Lessons
- Code a model writes is untrusted input: run it with prove's isolated env from the first version, never the session's
## Files touched
- plugin/tests/test_regen.py
- plugin/lib/sampo/regen.py
- plugin/lib/sampo/cli.py
- MASTER.md
- bench/moonshot/m02-slice-result.json
- plugin/lib/sampo/rune.py
- CHANGELOG.md
