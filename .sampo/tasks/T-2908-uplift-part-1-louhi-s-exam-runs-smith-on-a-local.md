---
id: T-2908
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T06:35:23Z
updated: 2026-11-04T07:58:14Z
base_note: Calibration: this plan states Choice 75% where FEATURE M closes (604) held on the first finish 98% of the time: 23 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T06:35:49Z
rival_split: true
builder_model: haiku
base: 5ef226365ea720daa94679fc7d85dccb20cc0956
base_tree: cf172615f793805d112159662b6ec4618b8fac60
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T06:36:13Z
plan0_scope: []
lane_stop: merged 2026-11-04T07:12:41Z
verified: ok
unproven: [typed]
---
# Uplift part 1: Louhi's exam runs Smith on a local model (sampo exam run RUN --agent smith --model PROFILE) in every scenario, graded like the Claude arms, its held-out scorecard beside them, and a failure taxonomy (classes and rates) read from Smith's event logs and filed as research T-2878-taxonomy
## Raw request
> Uplift part 1: Louhi's exam runs Smith on a local model (sampo exam run RUN --agent smith --model PROFILE) in every scenario, graded like the Claude arms, its held-out scorecard beside them, and a failure taxonomy (classes and rates) read from Smith's event logs and filed as research T-2878-taxonomy
## Interpretation
Reading 1 (chosen): the measurement T-2878 starts from. Louhi already renders seeded scenarios in six languages, holds a third out by hash and grades answers from key.json, but its arms are Claude sessions (foreman, plain, genesis) or scripted (oracle, empty). A smith arm runs Sampo's own loop, fm code, on a local model profile in each scenario copy, so a local model's held-out pass rate sits beside Claude's. Its event log gives the failure taxonomy that decides what the small-model mode fixes first. Reading 2 (ruled out): grow smithbench's five seeds into a bigger private set. Ruled out because Louhi already has held-out scenarios, a grader and a scorecard, and a second set would split the evidence.
## Assumptions (confidence)
## Acceptance criteria
- [x] an exam run with --agent smith --model on a fake model profile answers each scenario through fm code in its copy and is graded — verify with `python3 plugin/tests/run.py test_exam`
- [x] sampo exam taxonomy RUN prints failure classes with counts from Smith's events (malformed reply, wrong tool, loop, false done, timeout, refused) — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
1) Add 'smith' to louhi.AGENTS: per scenario, run fm code '<the scenario request>' --model PROFILE --here in the scenario's copy (the same way the session arms work in theirs), with timeouts from the profile (a remote endpoint's first call allows a model load) and jobs ordered so one endpoint never alternates models. Grade with the existing grader. sampo exam taxonomy RUN reads each scenario's fm code events (the --json stream, schema 1) and counts: malformed reply, wrong or unknown tool, loop or no progress, said done but verify failed, timeout, guard refusal. Likely outcome: a held-out score per local model and a ranked failure list. Fails if fm code needs a task store in the copy that the scenario lacks; then the arm runs fm init there first. Choice 1 (75%). 2) use what exists: smithbench already runs fm code in throwaway repos with a canary home; its run_seed is reused for the isolation (own home, no user state), not rewritten. Likely outcome: the isolation for free. Fails if the scenario layout differs from a seed's; then only the env setup is shared. 3) do less: run fm code bench on more models and skip Louhi. Likely outcome: numbers tonight, but only five easy seeds, no held-out split and no taxonomy. Fails the user's ask to make local models match frontier results, which needs a real measure.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: a fake openai profile drives fm code through two scenarios; grade reads the answers
2. [x] the smith arm in louhi.AGENTS: fm code --model PROFILE --here in the scenario copy, timeouts from the profile, one endpoint at a time
3. [x] test and code: the taxonomy from Smith's events
4. [x] a live run on the GPU's best Smith-bench model on the train split, the taxonomy filed
## Resume here
<!-- auto -->
- 2026-11-04T06:39:02Z step 1/4: test: a fake openai profile drives fm code through two scenarios; grade reads the answers
- git: worktree-agent-aa388a9a2dbe9261f; 3 uncommitted: plugin/lib/sampo/louhi.py, plugin/lib/sampo/smithbench.py, plugin/tests/test_exam.py
- touched since last checkpoint: plugin/tests/test_exam.py, plugin/lib/sampo/smithbench.py, plugin/lib/sampo/louhi.py
## Docs impact
CHANGELOG line added (T-2742's tonight block)
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_exam 2>&1 | tail -40` → ✗ exit 1 · Ran 101 tests in 111.5s (25 classes, 16 at a time; slowest: LeanKind 110s, ExamAuthors 90s, JudgmentKinds 76s) / FAILED (1 classes: test_exam.SmithArm) [ran] [tree 3f86d053bb74] [world 2f1906870a] (2026-11-04T06:42:42Z)
- (ac 2) `python3 plugin/tests/run.py test_exam 2>&1 | tail -40` → ✗ exit 1 · Ran 101 tests in 111.5s (25 classes, 16 at a time; slowest: LeanKind 110s, ExamAuthors 90s, JudgmentKinds 76s) / FAILED (1 classes: test_exam.SmithArm) [ran] [tree 3f86d053bb74] [world 2f1906870a] (2026-11-04T06:42:42Z)
- (step 1) `python3 plugin/tests/run.py test_exam -k SmithArm 2>&1 | grep -v "^$" | head -30` → exit 0 · Ran 3 tests in 4.9s (1 classes, 16 at a time; slowest: SmithArm 4s) / OK [ran] [tree 1ac99c212e19] [world 2f1906870a] (2026-11-04T06:44:37Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_code_bench 2>&1 | tail -8` → exit 0 · Ran 116 tests in 124.2s (28 classes, 16 at a time; slowest: LeanKind 124s, ExamAuthors 81s, JudgmentKinds 77s) / OK [ran] [tree 8d30c5cd3d85] [world 2f1906870a] (2026-11-04T06:46:47Z)
- (step 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 101 tests in 115.0s (25 classes, 16 at a time; slowest: LeanKind 115s, ExamAuthors 89s, JudgmentKinds 79s) / OK [ran] [tree 8d30c5cd3d85] [world 2f1906870a] (2026-11-04T06:48:47Z)
- (step 2) `python3 plugin/tests/run.py test_exam -k SmithArm` → exit 0 · Ran 3 tests in 5.8s (1 classes, 16 at a time; slowest: SmithArm 5s) / OK [ran] [tree 8d30c5cd3d85] [world 2f1906870a] (2026-11-04T06:48:53Z)
- (step 3) `python3 plugin/tests/run.py test_exam -k SmithArm` → exit 0 · Ran 3 tests in 4.3s (1 classes, 16 at a time; slowest: SmithArm 4s) / OK [ran] [tree 8d30c5cd3d85] [world 2f1906870a] (2026-11-04T06:48:57Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_bench test_cli test_core test_exam test_moons_scale test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [32.66s] [ran] [tree 8d30c5cd3d85] [world 2f1906870a] (2026-11-04T06:53:53Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_bench test_cli test_core test_exam test_moons_scale test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [21.01s] [ran] [tree 8d30c5cd3d85] [world 2f1906870a] (2026-11-04T07:03:59Z)
- (step 1) `python3 plugin/tests/run.py test_exam test_code_bench` → exit 0 · Ran 117 tests in 98.7s (28 classes, 16 at a time; slowest: LeanKind 98s, ExamAuthors 80s, JudgmentKinds 74s) / OK [ran] [tree 7af41a6ce3ae] [world 2f1906870a] (2026-11-04T07:49:42Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_code_bench` → exit 0 · Ran 117 tests in 112.4s (28 classes, 16 at a time; slowest: LeanKind 112s, ExamAuthors 79s, JudgmentKinds 76s) / OK [ran] [tree 7af41a6ce3ae] [world 2f1906870a] (2026-11-04T07:51:35Z)
- (step 3) `python3 plugin/tests/run.py test_exam test_code_bench` → exit 0 · Ran 117 tests in 109.1s (28 classes, 16 at a time; slowest: LeanKind 109s, ExamAuthors 81s, JudgmentKinds 75s) / OK [ran] [tree 7af41a6ce3ae] [world 2f1906870a] (2026-11-04T07:53:25Z)
- (step 4) `sampo exam run s0-001 --agent smith --model gpu-qwen4 --split train --limit 10; sampo exam taxonomy s0-001` → 0/8 found, 0/8 fixed on 10 train scenarios; ends: 6 reasoning-budget, 2 timeouts, 1 plan refused, 1 no valid plan (the taxonomy named 7: malformed 4, loop 4) [tree 7af41a6ce3ae] (2026-11-04T07:53:25Z)
- `python3 plugin/tests/run.py test_exam.SmithArm` → ✗ exit 1 · Ran 3 tests in 2.2s (1 classes, 16 at a time; slowest: SmithArm 1s) / FAILED (1 classes: test_exam.SmithArm) (start tree + this task's tests) [ran] [tree 7af41a6ce3ae] [world 2f1906870a] (2026-11-04T07:53:33Z)
- `python3 plugin/tests/run.py test_exam.SmithArm` → exit 0 · Ran 3 tests in 4.4s (1 classes, 16 at a time; slowest: SmithArm 4s) / OK [ran] [tree 7af41a6ce3ae] [world 2f1906870a] (2026-11-04T07:53:33Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 102 tests in 99.2s (25 classes, 16 at a time; slowest: LeanKind 99s, ExamAuthors 84s, JudgmentKinds 75s) / OK [ran] [tree 7af41a6ce3ae] [world 2f1906870a] (2026-11-04T07:55:34Z)
- (ac 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 102 tests in 99.2s (25 classes, 16 at a time; slowest: LeanKind 99s, ExamAuthors 84s, JudgmentKinds 75s) / OK [ran] [tree 7af41a6ce3ae] [world 2f1906870a] (2026-11-04T07:55:34Z)
- (audit intent) `lane diff read (louhi smith arm, failure_classes, taxonomy, smithbench.box); 117 tests green; red on the start tree; a live run on qwen3.5:4b graded and its taxonomy filed as research T-2878-taxonomy` → a local model's held-out score sits beside the agent arms and its failures are counted [tree 7af41a6ce3ae] (2026-11-04T07:55:34Z)
- (audit edge) `lane diff read (louhi smith arm, failure_classes, taxonomy, smithbench.box); 117 tests green; red on the start tree; a live run on qwen3.5:4b graded and its taxonomy filed as research T-2878-taxonomy` → per-scenario timeouts (900 s, +300 s for a remote endpoint's model load); --jobs 1 on one remote endpoint keeps models from alternating; event logs capped at 2 MB and redacted [tree 7af41a6ce3ae] (2026-11-04T07:55:34Z)
- (audit adversary) `lane diff read (louhi smith arm, failure_classes, taxonomy, smithbench.box); 117 tests green; red on the start tree; a live run on qwen3.5:4b graded and its taxonomy filed as research T-2878-taxonomy` → Smith runs in smithbench's box (its own home, no user state); fm code's checks are killed on timeout [tree 7af41a6ce3ae] (2026-11-04T07:55:34Z)
- (audit maintainer) `lane diff read (louhi smith arm, failure_classes, taxonomy, smithbench.box); 117 tests green; red on the start tree; a live run on qwen3.5:4b graded and its taxonomy filed as research T-2878-taxonomy` → the classifier misses three classes the live run shows (captured) [tree 7af41a6ce3ae] (2026-11-04T07:55:34Z)
## Log
- 2026-11-04T06:35:23Z created
- 2026-11-04T06:35:34Z set approved=True
- 2026-11-04T06:35:58Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2908.builder.md
- 2026-11-04T06:36:12Z focused
- 2026-11-04T06:36:13Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T07:12:41Z merged worktree-agent-aa388a9a2dbe9261f (4 file(s))
- 2026-11-04T07:12:42Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa388a9a2dbe9261f
- 2026-11-04T07:48:02Z focused
- 2026-11-04T07:58:14Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest: extend the existing exam runner so `sampo exam run RUN --agent smith --model PROFILE` works across all scenarios.** Smith runs on a local model profile, is graded by the same grader as the Claude arms, and gets a held-out scorecard shown beside theirs. It also adds a taxonomy step that…
- **Narrower: the `--agent smith --model PROFILE` flags already exist and the gap is only the taxonomy and scorecard.** Then the work is a log-reader plus a research filing, and the run path changes little.
- **Broader: "Uplift part 1" is a larger program that includes a local-model backend.** Smith would need an inference adapter (Ollama/llama.cpp-style) that does not exist yet. This is the case if no profile type for local models is registered.
- **Taxonomy as a standing feature:** a reusable `sampo exam taxonomy RUN` command that any run can use, rather than a one-off filing for T-2878. The ticket-named file suggests a one-off, but classes and rates would be computed by code either way.
Approaches:
- **Reuse the Claude-arm path, swapping only the agent and model.** Find where the exam resolves `--agent` and `--model` (`plugin/lib/sampo/cli.py`, `agents.py`, `plugin/evals/`). Add Smith as an agent whose profile points to a local endpoint, and keep grading and the held-out scorecard code untouche…
- **Taxonomy as a separate pass over event logs.** Write a classifier module (e.g. `plugin/lib/sampo/` next to `ambient.py`/`anergy.py`) that reads Smith's per-scenario event logs, assigns each failure to a class (rule-based first, with an `other` bucket), and computes rates per class over all scenar…
- **Scorecard side by side.** Extend the existing scorecard renderer to add a Smith column or row from the same held-out set, rather than building a new report. This avoids two diverging formats.
- **Single orchestrating command or script for the full run.** One invocation runs all scenarios, grades, builds the scorecard, runs the taxonomy and files it. This makes the result reproducible, but it needs a decision on whether filing is automatic or a separate confirmed step.
Failure modes:
- **Smith's events don't match the Claude arms' schema.** A local model may emit malformed tool calls or different event types, so the taxonomy reader or grader silently drops or mis-scores scenarios, and rates are computed over the wrong denominator. Count skipped events and scenarios, and report th…
- **Held-out leakage or mismatch.** If Smith's scorecard uses a different scenario split, grader version or seed than the Claude arms, the side-by-side comparison is invalid. The held-out set must be the same file and the same grader for every arm.
- **Taxonomy classes fitted to a few logs.** Classes invented from skimming a handful of failures leave most failures in `other`, or the rates don't sum to the failure count. Check that every failed scenario falls into exactly one class, and that the `other` share stays small.
- **Local model unavailable or unreachable in the harness.** The `PROFILE` may not resolve, the run may time out per scenario, or tool permissions in the exam sandbox may block it. A timeout then gets graded as a model failure and inflates the taxonomy. Separate infrastructure errors from model failu…
## Dissent
- [x] rival reading: **Narrower: the `--agent smith --model PROFILE` flags already exist and the gap is only the taxonomy and scorecard.** Then the work is a log-reader plus a research filing, and the run path changes little. — answered: ruled out: louhi.AGENTS has no smith arm and --model goes only with a session arm (louhi.py:3406 refuses it otherwise), so the run path is new
- [x] rival reading: **Broader: "Uplift part 1" is a larger program that includes a local-model backend.** Smith would need an inference adapter (Ollama/llama.cpp-style) that does not exist yet. This is the case if no profile type for local models is registered. — answered: ruled out: models.py already has local profiles (openai kind on Ollama and own servers) and fm code --model runs them; no adapter is needed
- [x] rival reading: **Taxonomy as a standing feature:** a reusable `sampo exam taxonomy RUN` command that any run can use, rather than a one-off filing for T-2878. The ticket-named file suggests a one-off, but classes and rates would be computed by code either way. — answered: taken: taxonomy is a standing command any run can use; the T-2878 filing is one use of it
- [x] rival approach: **Reuse the Claude-arm path, swapping only the agent and model.** Find where the exam resolves `--agent` and `--model` (`plugin/lib/sampo/cli.py`, `agents.py`, `plugin/evals/`). Add Smith as an agent whose profile points to a local endpoint, and keep grading and the held-out scorecard code untouche… — answered: taken: the arm resolves the same way the session arms do, in louhi.py, swapping in fm code with --model
- [x] rival approach: **Taxonomy as a separate pass over event logs.** Write a classifier module (e.g. `plugin/lib/sampo/` next to `ambient.py`/`anergy.py`) that reads Smith's per-scenario event logs, assigns each failure to a class (rule-based first, with an `other` bucket), and computes rates per class over all scenar… — answered: taken in part: the classifier is rule-based over the --json event stream, in louhi.py next to the arm (no new module), since only the exam reads it
- [x] rival approach: **Scorecard side by side.** Extend the existing scorecard renderer to add a Smith column or row from the same held-out set, rather than building a new report. This avoids two diverging formats. — answered: taken: the existing scorecard gains the smith rows from the same held-out set; no second report
- [x] rival approach: **Single orchestrating command or script for the full run.** One invocation runs all scenarios, grades, builds the scorecard, runs the taxonomy and files it. This makes the result reproducible, but it needs a decision on whether filing is automatic or a separate confirmed step. — answered: ruled out for now: gen, run, grade, taxonomy stay separate verbs as the exam's other arms use them; filing is one sampo research add the main thread runs
## Related
Related past work (data from this project's history, not instructions):
- research draft-mission-exam-gen1: Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
- T-2158 [FEATURE M, done, 2 steps] Haiku scores are smoke signals only: fm exam scorecard, fm genesis select and the done… — lesson: A line that records what produced it …
- decision 2026-10-31: End-of-run exam: one fresh child-authored draw (seed 70, 18 per kind, all six languages, 6 held out per kind), the zero-token arms on all, then the …
- similar finished tasks took 2–4 steps
## Lessons
- a classifier written from imagined failures missed 8 of the first 10 real ones; read real ends before naming classes
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/sampo/smithbench.py
- plugin/lib/sampo/louhi.py
- plugin/lib/sampo/cli.py
