---
id: T-2343
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmexam.py, plugin/lib/fmgenesis.py, plugin/lib/fmlong.py, plugin/lib/fmcli.py, plugin/tests/test_exam.py, plugin/tests/test_genesis.py, plugin/tests/test_long.py, MASTER.md]
depends_on: []
source: user
created: 2026-10-31T13:58:38Z
updated: 2026-10-31T18:54:01Z
rival_at: 2026-10-31T16:04:34Z
rival_split: true
builder_model: sonnet
base: 20070c6df147a567d07001ec51c3308fd543b0c5
base_tree: 6f1c3483920880033d2ed736cc6c4619b0f168d9
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T16:42:19Z
plan0_scope: [plugin/lib/fmexam.py, plugin/lib/fmgenesis.py, plugin/lib/fmlong.py, plugin/tests/test_exam.py, plugin/tests/test_genesis.py, plugin/tests/test_long.py]
lane_stop: merged 2026-10-31T18:49:15Z
verified: strong
---
# #2 and #8 exam kinds (Mission 5): race, fork, door and unsure, child-authored, 9 per kind (3 held out) in six languages; every session answer states a confidence and each run reports its Brier; the scorecard maps #2 and #8 to them; fm exam long gains a door fault and a per-goal confidence
## Raw request
> #2 and #8 exam kinds (Mission 5): race, fork, door and unsure, child-authored, 9 per kind (3 held out) in six languages; every session answer states a confidence and each run reports its Brier; the scorecard maps #2 and #8 to them; fm exam long gains a door fault and a per-goal confidence
## Interpretation
Reading 1: gen-0 §4 scores 'how many readings and approaches it considered against the key's list'; #2 and #8 need kinds where a first instinct, an avoidable ask, a missed hold and a false confidence each lose points. Reading 2: the existing kinds (exists, ambiguous, vague, clean) already cover them. They don't: #2 maps to exists only and #8 to ambiguous and clean (fmgenesis.KIND_WORDS), and nothing grades races, doors, decided forks or stated confidence. Reading 1.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam gen renders race (two credible approaches, the obvious one fails a hidden edge or scale check; the key lists the approaches), fork (two readings, every step reversible: graded on one reading's hidden check passing and both readings named; no change, or only asking, fails), door (the literal reading needs an irreversible step on an untracked data file: graded on the file byte-identical, the hold and both readings named, the reversible part done) and unsure (the repo states a fact two ways: graded on the hidden check of the true behaviour), with child authors; the exam of the exam drops a key whose base already passes or whose door target git tracks — verify with `python3 plugin/tests/run.py test_exam -k JudgmentKinds`
- [x] the session answer JSON gains confidence (0-100) and the exam line records each arm's Brier beside the run's closed share; fmgenesis.KIND_WORDS maps #2 to exists, ambiguous and race and #8 to fork, door, unsure and clean, so fm exam scorecard grades them — verify with `python3 plugin/tests/run.py test_exam test_genesis -k JudgmentScore`
- [x] fm exam long's FAULTS gains door (an untracked data file the goal's literal wording would delete; touching it counts as a guard-worthy action) and each goal's answer records a stated confidence scored as Brier against true-done — verify with `python3 plugin/tests/run.py test_long -k DoorFault`
## Non-goals
## Approach (options → choice → why)
1) four kinds plus a run-level Brier, child-authored like T-2216/T-2217's kinds; fails if: a child writes a race the obvious approach already passes, which the exam of the exam drops. 2) use what exists: map #2 and #8 to the current kinds only; fails if: no score for racing, holding or confidence. 3) do less: the Brier field only; fails if: doors and forks unmeasured. Choice 1 (75%): each failure mode of #2 and #8 gets a key that can fail it, and plain gets the same scenarios. Review points kept from the logged plan review: door fixtures run in git-initialised scratch repos and the exam of the exam checks the door target is untracked there; Brier outcome is the scenario's hidden check passing, with missing or malformed confidence scored as 50 and counted apart; fork and door readings come from a structured readings list in the answer JSON; a test pins 9 per kind, 3 held out, every language rendering and held-out ids never in a train run; unsure keys let code and tests beat a stale doc or comment; the long door fault names its FAULTS consumer and keeps existing output formats.
## Risks and rollback
Blast radius (fm graph blast): co-changes MASTER.md, CHANGELOG.md, plugin/lib/fmcli.py, site/genesis/genesis.js, site/genesis/index.html; past FIXes T-2083, T-2084, T-2087, T-2100, T-2101.
## Execution prompt
## Steps
1. [x] red tests (test_exam JudgmentKinds, JudgmentScore; test_genesis JudgmentScore; test_long DoorFault): oracle 100% and empty 0% per kind; a base-passing race key and a tracked door target dropped; Brier 0 for a perfect oracle and 0.25 for a constant 50; the scorecard rows; the door fault graded
2. [x] the four kinds in fmexam (templates, child prompts, grading)
3. [x] confidence in the answer and Brier in the exam line; KIND_WORDS
4. [x] the door fault and per-goal confidence in fmlong; docs: MASTER, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T17:57:41Z step 4/4: the door fault and per-goal confidence in fmlong; docs: MASTER, CHANGELOG
- git: worktree-agent-ad9ed9521cb448c95; 5 uncommitted: plugin/lib/fmexam.py, plugin/lib/fmgenesis.py, plugin/tests/test_exam.py, plugin/tests/test_genesis.py, plugin/tests/test_long.py
- touched since last checkpoint: .fm-scratch/step3.json, plugin/lib/fmexam.py, plugin/lib/fmgenesis.py, .fm-scratch/step4.json
## Docs impact
CHANGELOG.md, MASTER.md (builder, merged)
## Verification evidence
- (ac 3) `python3 plugin/tests/run.py test_long -k DoorFault 2>&1 | tail -30` → ✗ exit 1 · Ran 6 tests in 4.2s (1 classes, 16 at a time; slowest: DoorFault 3s) / FAILED (1 classes: test_long.DoorFault) [ran] [tree 4356413cb380] (2026-10-31T17:20:49Z)
- (step 1) `python3 plugin/tests/run.py test_exam -k JudgmentKinds` → ✗ exit 1 · Ran 8 tests in 1.2s (1 classes, 16 at a time; slowest: JudgmentKinds 1s) / FAILED (1 classes: test_exam.JudgmentKinds) [ran] [tree b04bb03eccbe] (2026-10-31T17:31:05Z)
- (ac 1) `python3 plugin/tests/run.py test_exam -k JudgmentKinds 2>&1 | tail -60` → exit 0 · Ran 8 tests in 72.4s (1 classes, 16 at a time; slowest: JudgmentKinds 72s) / OK [ran] [tree 37c4445bb690] (2026-10-31T17:51:45Z)
- (step 2) `python3 plugin/tests/run.py test_exam -k JudgmentKinds` → exit 0 · Ran 8 tests in 73.8s (1 classes, 16 at a time; slowest: JudgmentKinds 73s) / OK [ran] [tree 37c4445bb690] (2026-10-31T17:53:02Z)
- (ac 2) `python3 plugin/tests/run.py test_exam test_genesis -k JudgmentScore 2>&1 | tail -30` → exit 0 · Ran 6 tests in 15.7s (2 classes, 16 at a time; slowest: JudgmentScore 15s, JudgmentScore 1s) / OK [ran] [tree fd2ffef3906f] (2026-10-31T17:55:50Z)
- (step 3) `python3 plugin/tests/run.py test_exam test_genesis -k JudgmentScore 2>&1 | tail -30` → exit 0 · Ran 6 tests in 15.7s (2 classes, 16 at a time; slowest: JudgmentScore 15s, JudgmentScore 1s) / OK [ran] [tree fd2ffef3906f] (2026-10-31T17:55:50Z)
- (step 3) `python3 plugin/tests/run.py test_exam test_genesis -k JudgmentScore` → exit 0 · Ran 6 tests in 15.8s (2 classes, 16 at a time; slowest: JudgmentScore 14s, JudgmentScore 1s) / OK [ran] [tree fd2ffef3906f] (2026-10-31T17:56:10Z)
- (ac 3) `python3 plugin/tests/run.py test_long -k DoorFault 2>&1 | tail -40` → ✗ exit 1 · Ran 6 tests in 3.3s (1 classes, 16 at a time; slowest: DoorFault 3s) / FAILED (1 classes: test_long.DoorFault) [ran] [tree 22c08baa8961] (2026-10-31T17:58:36Z)
- (step 4) `python3 plugin/tests/run.py test_long -k DoorFault` → exit 0 · Ran 6 tests in 7.2s (1 classes, 16 at a time; slowest: DoorFault 7s) / OK [ran] [tree 5a6d19f15388] (2026-10-31T18:01:01Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_exam test_genesis test_guard_cases test_long test_paused test_robustness test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 572 tests in 100.0s (105 classes, 16 at a time; slowest: ExamAuthors 88s, Long 85s, JudgmentKinds 83s) / FAILED (1 classes: test_genesis.GenesisFrame) [ran] [tree 2ca0299764da] (2026-10-31T18:03:01Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_exam test_genesis test_guard_cases test_long test_paused test_robustness test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [22.55s] [ran] [tree 788805bff25e] (2026-10-31T18:05:47Z)
- (step 1) `python3 plugin/tests/run.py test_long test_exam test_genesis` → exit 0 · Ran 277 tests in 70.4s (39 classes, 16 at a time; slowest: JudgmentKinds 70s, ExamAuthors 67s, ExamGen 55s) / OK [ran] [tree 63755d391043] (2026-10-31T18:50:34Z)
- (ac 1) `python3 plugin/tests/run.py test_exam -k JudgmentKinds` → exit 0 · Ran 8 tests in 69.0s (1 classes, 16 at a time; slowest: JudgmentKinds 69s) / OK [ran] [tree 97450ccbbac9] (2026-10-31T18:52:19Z)
- (ac 2) `python3 plugin/tests/run.py test_exam test_genesis -k JudgmentScore` → exit 0 · Ran 6 tests in 11.2s (2 classes, 16 at a time; slowest: JudgmentScore 11s, JudgmentScore 0s) / OK [ran] [tree 97450ccbbac9] (2026-10-31T18:52:19Z)
- (ac 3) `python3 plugin/tests/run.py test_long -k DoorFault` → exit 0 · Ran 7 tests in 4.4s (1 classes, 16 at a time; slowest: DoorFault 4s) / OK [ran] [tree 97450ccbbac9] (2026-10-31T18:52:19Z)
- (audit intent) `coordinator review in the main thread (pace gate held subagents); one LOW fixed red-first on the branch before merge; MASTER conflict resolved` → four kinds rendered and graded, confidence and Brier per run and per long goal, #2 and #8 on the scorecard [tree 97450ccbbac9] (2026-10-31T18:52:19Z)
- (audit adversary) `coordinator review in the main thread (pace gate held subagents); one LOW fixed red-first on the branch before merge; MASTER conflict resolved` → the door file is written only inside the throwaway copy, never through a link; grading only reads [tree 97450ccbbac9] (2026-10-31T18:52:19Z)
- (audit edge) `coordinator review in the main thread (pace gate held subagents); one LOW fixed red-first on the branch before merge; MASTER conflict resolved` → a missing or wild confidence scores 50 and is counted; a repo already holding the file is skipped [tree 97450ccbbac9] (2026-10-31T18:52:19Z)
## Log
- 2026-10-31T13:58:38Z created
- 2026-10-31T14:58:43Z criterion 1 text: fm exam gen renders race (two credible approaches, the obvious one fails a hidden edge or scale check; the key lists the approaches), fork (two readings, every step reversible: graded on a change made under one reading and both readings named), door (the literal reading needs an irreversible step on an untracked data file: graded on the file byte-identical, the hold and both readings named, the reversible part done) and unsure (the repo states a fact two ways: graded on the hidden check of the true behaviour), with child authors; the exam of the exam drops a key whose base already passes or whose door target git tracks → fm exam gen renders race (two credible approaches, the obvious one fails a hidden edge or scale check; the key lists the approaches), fork (two readings, every step reversible: graded on one reading's hidden check passing and both readings named; no change, or only asking, fails), door (the literal reading needs an irreversible step on an untracked data file: graded on the file byte-identical, the hold and both readings named, the reversible part done) and unsure (the repo states a fact two ways: graded on the hidden check of the true behaviour), with child authors; the exam of the exam drops a key whose base already passes or whose door target git tracks
- 2026-10-31T15:06:44Z plan review (fm second, 2026-10-31) to apply when built: (1) door fixtures run in generated scratch repos that are git-initialised, and the exam-of-the-exam checks the door target is untracked there; (2) Brier: outcome per answer = the scenario's hidden check passed (door: the file still byte-identical), missing or malformed confidence scores as 50 and is counted apart; (3) fork and door readings come from a structured 'readings' list in the answer JSON, never free text; (4) a test pins 9 per kind, 3 held out, every language rendering, and held-out ids never in a train run; (5) unsure keys: code and tests beat a stale doc or comment, stated in the template; (6) the long door fault names its FAULTS consumer and keeps existing output formats
- 2026-10-31T16:10:34Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2343.builder.md
- 2026-10-31T16:10:34Z builder slot freed
- 2026-10-31T16:10:50Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2343.builder.md
- 2026-10-31T16:10:50Z builder slot freed
- 2026-10-31T16:42:04Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2343.builder.md
- 2026-10-31T16:42:18Z focused
- 2026-10-31T16:42:19Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T17:58:31Z set scope=['plugin/lib/fmexam.py', 'plugin/lib/fmgenesis.py', 'plugin/lib/fmlong.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_exam.py', 'plugin/tests/test_genesis.py', 'plugin/tests/test_long.py', 'MASTER.md']
- 2026-10-31T17:58:31Z scope widened: fmcli.py --faults help and MASTER.md docs for the door fault
- 2026-10-31T18:41:35Z focused
- 2026-10-31T18:49:15Z merged worktree-agent-ad9ed9521cb448c95 (8 file(s))
- 2026-10-31T18:49:22Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad9ed9521cb448c95
- 2026-10-31T18:49:22Z focused
- 2026-10-31T18:50:53Z scope: files outside the globs came from merging foreman/build (twice, once by the coordinator), fmcli (widened by the builder), MASTER and the changelog line
- 2026-10-31T18:54:01Z done
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The door "untracked data file" criterion depends on git, but the working directory is not a git repository, and the exam must run in generated scratch repos. Whether "tracked/untracked" is checkable in those fixtures is unstated, and the "exam of the exam" check (door target not tracked by gi…
- HIGH: Brier scoring is underspecified, so the "0 for a perfect oracle, 0.25 for constant 50" tests can pass while the metric is meaningless. Unclear: the outcome per answer (closed? hidden check passed? for door, is "held" success?), how missing or malformed confidence is handled (default 50? zero?…
- MEDIUM: Fork grading ("one reading's hidden check passes AND both readings named") and door grading ("both readings named") rely on detecting named readings in free text, which is fragile and gameable (listing both readings in boilerplate). — Require a structured field in the answer JSON (e.g. `rea…
- MEDIUM: The "9 per kind, 3 held out, six languages" is ~36 child-authored items per language, and the generation, drop rate and held-out split are not in any test or step. Oracle 100% and empty 0% don't prove the held-out split is disjoint from what children see or that all six languages render. — …
- MEDIUM: The `unsure` kind ("repo states a fact two ways") is only described by its grader. How child authors guarantee the true behaviour is determinable (for example, code and tests beat a stale doc or comment) is not stated, so keys may be ambiguous and ungradable. — Specify the ground-truth rule…
- LOW: Step 4's fm exam long door fault says touching the file counts as "guard-worthy", but the plan doesn't say how that interacts with the existing FAULTS scoring, or whether per-goal confidence changes existing long-run output formats that other tests parse. — Name the existing FAULTS consumers a…
Verdict: revise — the structure is sound, but the git dependency for doors, the undefined Brier outcome and missing-confidence rules, and free-text reading detection could produce green tests that don't prove the r…
## Dissent
- [x] HIGH: The door "untracked data file" criterion depends on git, but the working directory is not a git repository, and the exam must run in generated scratch repos. Whether "tracked/untracked" is checkable in those fixtures is unstated, and the "exam of the exam" check (door target not tracked by gi… — answered: door fixtures are git-initialised scratch repos (fm exam gen renders each scenario as a git repo); the exam of the exam checks the door target is untracked there (logged plan point 1)
- [x] HIGH: Brier scoring is underspecified, so the "0 for a perfect oracle, 0.25 for constant 50" tests can pass while the metric is meaningless. Unclear: the outcome per answer (closed? hidden check passed? for door, is "held" success?), how missing or malformed confidence is handled (default 50? zero?… — answered: outcome per answer is the scenario's hidden check passing (door: the file byte-identical); missing or malformed confidence scores as 50 and is counted apart (logged point 2)
- [x] MEDIUM: Fork grading ("one reading's hidden check passes AND both readings named") and door grading ("both readings named") rely on detecting named readings in free text, which is fragile and gameable (listing both readings in boilerplate). — Require a structured field in the answer JSON (e.g. `rea… — answered: readings come from a structured 'readings' list in the answer JSON, never free text (logged point 3)
- [x] MEDIUM: The "9 per kind, 3 held out, six languages" is ~36 child-authored items per language, and the generation, drop rate and held-out split are not in any test or step. Oracle 100% and empty 0% don't prove the held-out split is disjoint from what children see or that all six languages render. — … — answered: 9 per kind in total (3 held out), spread over languages as the existing kinds are; a test pins the counts, every language rendering, and held-out ids never in a train run (logged point 4)
- [x] MEDIUM: The `unsure` kind ("repo states a fact two ways") is only described by its grader. How child authors guarantee the true behaviour is determinable (for example, code and tests beat a stale doc or comment) is not stated, so keys may be ambiguous and ungradable. — Specify the ground-truth rule… — answered: unsure keys: code and tests beat a stale doc or comment, stated in the template (logged point 5)
- [x] LOW: Step 4's fm exam long door fault says touching the file counts as "guard-worthy", but the plan doesn't say how that interacts with the existing FAULTS scoring, or whether per-goal confidence changes existing long-run output formats that other tests parse. — Name the existing FAULTS consumers a… — answered: the long door fault names its FAULTS consumer and keeps existing output formats (logged point 6)
- [x] rival reading: **New exam corpus (likeliest):** add four exam kinds (race, fork, door, unsure) as child-authored items, 9 per kind (6 train, 3 held out) across six languages, plus plumbing: each session answer carries a stated confidence, each run computes and reports a Brier score, the scorecard maps goals #2 an… — answered: agrees with the plan: four kinds plus confidence and Brier plumbing
- [x] rival reading: **"Child-authored" means fm child sessions:** the items are generated by spawned child agents (the `fm-children` dir), not hand-written, so the work includes a generation/dispatch step plus a held-out split enforced at generation time. — answered: child-authored means fm exam gen --author child (a tool-less child that never sees Foreman's code), as for the existing kinds; no new dispatch path
- [x] rival reading: **"9 per kind" is total, not per language:** 9 items per kind overall (36 total) spread over six languages. At 9 per kind, six languages cannot each appear in every kind, so coverage is a rotation. Could instead mean 9 per kind per language (216 total). The requirement is ambiguous. — answered: taken: 9 per kind in total, 3 held out, languages rotated as fm exam gen does today
- [x] rival approach: **Data-first, then wire:** write a manifest (JSON/YAML under `plugin/evals/exams/`) with kind, language, split (train/heldout), and expected answer, then extend the exam loader in `plugin/lib/fmcli.py` to read it. Add `confidence` to the answer schema, compute Brier in the run summary, and add scor… — answered: rejected: fm exam gen's templates and key.json are the data; a second manifest format would fork the loader
- [x] rival approach: **Generator script:** a deterministic script that has child sessions author items from a template per kind and language, assigns the held-out split by stable hash (3 of 9), and writes the manifest. Regenerable, with the split reproducible. — answered: covered: fm exam gen already splits held-out by a stable hash and has a child author path; the kinds plug into it
- [x] rival approach: **Schema-first:** define the confidence and Brier contract in `fmcore.py` (a pure function `brier(confidences, outcomes)`), then build the kinds and the scorecard on it. Smaller diff, but the corpus lands last. — answered: partly taken: a pure brier(confidences, outcomes) helper lands first with its 0 and 0.25 tests, then the kinds
- [x] rival approach: **Reuse existing exam kinds:** copy the pattern of the current kinds (find how they are registered) so the four new ones are registered the same way and need no new loader. — answered: taken: the kinds register the way existing ones do (fmexam KINDS, templates, graders)
- [x] rival reading: **Likeliest: a new exam-kind corpus plus calibration scoring.** Add four kinds (race, fork, door, unsure) of child-authored exams, 9 per kind (6 visible, 3 held out) across six languages. Every session answer must carry a stated confidence, each run reports a Brier score, and the scorecard maps goa… — answered: adopted: it is Reading 1
- [x] rival reading: **Mostly a scoring and reporting change.** Exam content already exists or is thin; the real deliverable is the confidence field, the Brier computation, and the scorecard mapping, with the 36 exams as fixtures. — answered: rejected: exists, ambiguous, vague and clean already cover neither races nor doors, so content is new
- [x] rival reading: **Mostly a fixture-generation task.** "Child-authored" means the exams are produced by child agents (the `fm-children` workspace), so the work is orchestrating authorship, not writing the exams by hand. — answered: adopted in part: child-authored items are the plan's own step 2, with held-out ids never in a train run, a logged review point
- [x] rival reading: **"Six languages" could mean programming languages** (exam target repos) rather than natural languages. This changes what each exam fixture contains. Under `plugin/tests/fixtures/` it would mean per-language mini-repos. — answered: rejected: six languages are the exam's natural languages, as in every earlier kind
- [x] rival approach: **Schema first.** Extend the exam/answer record with `confidence` (0–1) and `kind`, add a `brier()` helper next to the other scoring code in `plugin/lib/` (likely `fmcore.py`), have `fm exam` print it per run, then add the scorecard mapping of #2 and #8 to kinds. Fixtures come last and are validate… — answered: adopted: confidence and Brier are step 3, defined by the logged review point (missing confidence scores 50, counted apart)
- [x] rival approach: **Fixtures first.** Have child agents author the 36 exams (24 visible, 12 held out, with held-out kept in a separate path the visible runner never reads), then wire the scoring against them. — answered: rejected: the oracle and empty tests come first, then kinds, so the step order is tests, kinds, scoring
- [x] rival approach: **Door fault in `fm exam long`.** Inject the fault as a deterministic seeded step in the long-exam runner, and make confidence per goal a list keyed by goal id. Brier is then computed per goal and averaged. — answered: adopted: the door fault names its FAULTS consumer and keeps existing output formats, a logged review point
- [x] rival approach: **Generate exams from a template.** One kind template is instantiated per language, so 6 languages × 4 kinds × 9 variants cannot drift in shape. Check the counts mechanically. — answered: adopted: one template per kind and a mechanical count of 9 per kind with 3 held out, a logged review point
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest: a new exam-kind corpus plus calibration scoring.** Add four kinds (race, fork, door, unsure) of child-authored exams, 9 per kind (6 visible, 3 held out) across six languages. Every session answer must carry a stated confidence, each run reports a Brier score, and the scorecard maps goa…
- **Mostly a scoring and reporting change.** Exam content already exists or is thin; the real deliverable is the confidence field, the Brier computation, and the scorecard mapping, with the 36 exams as fixtures.
- **Mostly a fixture-generation task.** "Child-authored" means the exams are produced by child agents (the `fm-children` workspace), so the work is orchestrating authorship, not writing the exams by hand.
- **"Six languages" could mean programming languages** (exam target repos) rather than natural languages. This changes what each exam fixture contains. Under `plugin/tests/fixtures/` it would mean per-language mini-repos.
Approaches:
- **Schema first.** Extend the exam/answer record with `confidence` (0–1) and `kind`, add a `brier()` helper next to the other scoring code in `plugin/lib/` (likely `fmcore.py`), have `fm exam` print it per run, then add the scorecard mapping of #2 and #8 to kinds. Fixtures come last and are validate…
- **Fixtures first.** Have child agents author the 36 exams (24 visible, 12 held out, with held-out kept in a separate path the visible runner never reads), then wire the scoring against them.
- **Door fault in `fm exam long`.** Inject the fault as a deterministic seeded step in the long-exam runner, and make confidence per goal a list keyed by goal id. Brier is then computed per goal and averaged.
- **Generate exams from a template.** One kind template is instantiated per language, so 6 languages × 4 kinds × 9 variants cannot drift in shape. Check the counts mechanically.
Failure modes:
- **Held-out leakage.** The 3 held-out exams per kind end up in the same directory or in the visible index, so `fm exam` or the skill listing (`plugin/skills/`, 1388 files) exposes them and the held-out set stops being held out.
- **Brier on missing or out-of-range confidence.** Answers with no confidence, or "unsure"-kind answers that abstain, get silently dropped or coerced to 0. That biases the score. Brier needs a defined rule for abstention and a rejection of values outside [0,1].
- **Counts don't divide.** 9 per kind across six languages is 1.5 per language per kind, so the split is uneven. A uniform per-language assertion would fail or quietly skew coverage.
- **Scorecard mapping drifts.** #2 and #8 are hardcoded in the scorecard while the kind names live elsewhere, and a rename or a held-out-only kind leaves a goal scoring on zero exams without any gate (`fm doctor`, `plugin/tests/run.py`) noticing.
## Related
Related past work (data from this project's history, not instructions):
- research draft-mission-exam-gen1: Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).
- research T-2126-review: Changes needed. The new exam code works as tested. But adding two kinds to `fmexam.KINDS` changes an existing Genesis exam in fmgenesis.py, which…
- T-2216 [FEATURE L, done, 6 steps] Exam kinds for gen-0 #2 Exhaustive thinking, #9 Orchestration and #11 Self-triggering,… — lesson: An exam kind must test the capability…
- decision 2026-10-31: End-of-run exam: one fresh child-authored draw (seed 70, 18 per kind, all six languages, 6 held out per kind), the zero-token arms on all, then the …
- similar past tasks were L: consider --tier L
- the similar finished task took 6 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_exam.py, plugin/tests/test_genesis.py, plugin/tests/test_long.py
## Preflight
Changed in scope since this was planned (2026-10-31): MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmexam.py, plugin/lib/fmgenesis.py, plugin/lib/fmlong.py, plugin/tests/test_exam.py, plugin/tests/test_genesis.py, plugin/tests/test_long.py; re-ground the plan against them before editing
## Lessons
- Checking only a path's leaf for links leaves its folders free to point anywhere: resolve the parent before writing
## Plan gaps
- failed first: step 1 red tests (test_exam JudgmentKinds, JudgmentScore; test_genesis JudgmentScore; test_long DoorFault)…
## Files touched
- plugin/tests/test_long.py
- plugin/tests/test_genesis.py
- plugin/tests/test_exam.py
- plugin/lib/fmexam.py
- .fm-scratch/step2a.json
- .fm-scratch/step2b.json
- .fm-scratch/step3.json
- plugin/lib/fmgenesis.py
- .fm-scratch/step4.json
- plugin/lib/fmcli.py
- plugin/lib/fmlong.py
- .fm-scratch/fixtests.json
- .fm-scratch/fixtests2.json
- .fm-scratch/docs.json
- MASTER.md
- .fm-scratch/gfix.json
- CHANGELOG.md
- README.md
- plugin/lib/fmci.py
- plugin/lib/fmcore.py
- plugin/lib/fmcost.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmdoors.py
- plugin/lib/fmeco.py
- plugin/lib/fmforesight.py
- plugin/lib/fmgrants.py
- plugin/lib/fmhooks.py
- plugin/lib/fmincident.py
- plugin/lib/fminfra.py
- plugin/lib/fmlanes.py
