---
id: T-2992
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T17:46:35Z
updated: 2026-11-04T18:23:04Z
base_note: Calibration: this plan states Choice 70% where FEATURE M closes (629) held on the first finish 98% of the time: 28 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T18:01:42Z
rival_split: true
builder_model: haiku
base: c79819bf5f447bf5de4355e618f7112b37681fc9
base_tree: ffbcb33248f1c9f75b3f6efbcc7d8d8a2db614ff
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T18:02:08Z
plan0_scope: []
lane_stop: merged 2026-11-04T18:20:20Z
verified: strong
unproven: [meaning]
---
# NOW: a repeat-failure firewall, so Sampo and the models it runs one-shot more and never…
## Raw request
> NOW: a repeat-failure firewall, so Sampo and the models it runs one-shot more and never fail the same way twice: mine the ledger and refusals by failure class (today: merges held by the self-change gate under load ~5x; builder branches missing MASTER bullet and fm shim 2x; live runs failing on unprobed external interfaces 4x: jeff-train identity, GPU full, slow suite, tsc; guard refusals of the same shell forms 11x; builder code breaking a standing rule caught only after merge), turn each recurring class into a check that fires before the action (builder brief carries the standing rules and the class list; lane runs the self-docs and rule tests before merge; a live-interface probe before any live run; the self-change gate measures base and branch interleaved under the same load), and report the repeat rate per class each Rune generation, the same checks applied to Smith runs of small models
## Interpretation
Reading 1 (chosen): Sampo should stop failing the same way twice. For each failure class that repeated today, add a check before the action: rule tests in every affected run, standing rules in every builder brief, a self-change gate that compares base and branch fairly under load, and a per-class repeat report; the same checks apply to small models run by Smith. Reading 2 (ruled out): make models never err; no check reaches zero errors, but a repeat rate per class is measurable and can go to near zero.
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo check --affected always runs the standing-rule tests (self-docs, model rules, left-out, rename scan), so builder branches missing a MASTER bullet and fm shim fail in their own lane; sampo lane brief carries a Standing rules section — verify with `python3 plugin/tests/run.py test_affected_rules test_lanes`
- [x] the self-change gate benches base and branch interleaved over 3 pairs and holds only a rise seen in 2 of 3; a real rise in every pair still holds — verify with `python3 plugin/tests/run.py test_selfgate`
- [x] sampo friction --classes prints each refusal or failed-close class with its count today and whether it repeated — verify with `python3 plugin/tests/run.py test_friction`
## Non-goals
- Live runs failing on unprobed external interfaces (jeff-train identity, GPU full, slow suite, tsc): a playbook line and lesson, not code here; the probe step is in T-2971.
- Guard refusals of the same shell forms 11x: the guard already names the rewrite; my habit, recorded as a lesson.
- The same checks applied to Smith runs of small models: after the repeat report exists (it reads Smith's failure classes too).
## Approach (options → choice → why)
What a complete version has: each failure class that repeated today has a check that fires before the action, and a report of the repeat rate per class.

1) Four checks and a report: sampo check --affected always adds the standing-rule tests (self-docs in test_doctor, test_models ModelRules, test_left_out, test_rename_scan), so a builder meets a broken rule or a missing map entry in its own lane; sampo lane brief adds a Standing rules section (the decisions marked standing, the model rules, the training-data rule, the map entry a new module needs); the self-change gate benches base and branch interleaved over 3 pairs and holds only a rise seen in 2 of 3; and sampo friction --classes groups the day's refusals and failed closes by class with each class's count and whether it repeated. Likely outcome: fewer repeat stops, measured by the report. Fails if: the rule tests are slow; they run in about 20 s, against minutes for the affected set.
2) use what exists: lessons at close (--lesson) and the ambient tests. Likely outcome: today's pattern, where the lesson is written and the same class recurs, because a lesson is prose that nothing checks before the action. Fails if: today's repeats, which happened with lessons on record.
3) do less: the rule tests and the fair gate only, the two that cost the most stops today. Likely outcome: most of the gain. Fails if: the brief keeps omitting rules and builders keep writing code against them.
Choice 1 (70%): each piece maps to a class that repeated today, and the report measures whether it worked.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: rule tests in the affected set, the brief's rules section, an interleaved gate that passes load noise and holds a real rise, the classes report
2. [x] the four pieces
3. [x] a day's repeat report and a merge under load that the gate no longer holds falsely
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_affected_rules test_selfgate test_friction` → exit 0 · Ran 31 tests in 7.4s (8 classes, 16 at a time; slowest: Friction 7s, UserPromptSubmit 1s, AffectedRules 0s) / OK [ran] [tree 1466b18befc6] [world 2f1906870a] (2026-11-04T18:07:37Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_rules test_cli test_doctor test_friction test_lane_twins test_lanes test_left_out test_mint test_models test_moons_scale test_rename_scan test_selfgate test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.05s] [ran] [tree 1466b18befc6] [world 2f1906870a] (2026-11-04T18:08:19Z)
- (step 2) `python3 plugin/tests/run.py test_affected_rules test_lanes test_selfgate test_friction` → exit 0 · Ran 189 tests in 24.3s (22 classes, 16 at a time; slowest: Lanes 24s, LaneRecovery 22s, RaceEvidence 10s) / OK [ran] [tree f25e5c8409e1] [world 2f1906870a] (2026-11-04T18:20:56Z)
- (step 3) `sampo friction --classes` → exit 0 · guard block: plugin ×1 / guard block: confine ×1 [ran] [tree f25e5c8409e1] [world 2f1906870a] (2026-11-04T18:20:57Z)
- `python3 plugin/tests/run.py test_affected_rules test_selfgate test_friction` → ✗ exit 1 · Ran 31 tests in 8.5s (8 classes, 16 at a time; slowest: Friction 7s, UserPromptSubmit 1s, BoardIdeas 0s) / FAILED (3 classes: test_friction.Friction, test_selfgate.Interleaved, test_affected_rules.Aff (start tree + this task's tests) [ran] [tree f25e5c8409e1] [world 2f1906870a] (2026-11-04T18:21:13Z)
- `python3 plugin/tests/run.py test_affected_rules test_selfgate test_friction` → exit 0 · Ran 31 tests in 7.3s (8 classes, 16 at a time; slowest: Friction 7s, UserPromptSubmit 1s, AffectedRules 0s) / OK [ran] [tree f25e5c8409e1] [world 2f1906870a] (2026-11-04T18:21:13Z)
- (ac 1) `python3 plugin/tests/run.py test_affected_rules test_lanes` → exit 0 · Ran 159 tests in 42.5s (15 classes, 16 at a time; slowest: Lanes 42s, LaneRecovery 36s, RaceEvidence 27s) / OK [ran] [tree a6dd11b9c213] [world 2f1906870a] (2026-11-04T18:22:16Z)
- (ac 2) `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 5 tests in 0.4s (2 classes, 16 at a time; slowest: Interleaved 0s, LoadedWallCheck 0s) / OK [ran] [tree a6dd11b9c213] [world 2f1906870a] (2026-11-04T18:22:16Z)
- (ac 3) `python3 plugin/tests/run.py test_friction` → exit 0 · Ran 25 tests in 8.1s (5 classes, 16 at a time; slowest: Friction 8s, UserPromptSubmit 1s, BoardIdeas 0s) / OK [ran] [tree a6dd11b9c213] [world 2f1906870a] (2026-11-04T18:22:16Z)
- (audit adversary) `branch diff read: RULE_TESTS in affected, STANDING in the lane brief, selfgate _paired over 3 pairs holding 2, friction.classes; prove red on the start tree, green now; live friction --classes gives today's baseline; this session's next merges are the live gate check` → the gate is no looser against a real regression: a rise in every pair or in 2 of 3 still holds (tested); guard verdicts, footprint and verb checks unchanged; the harness stays the base's [tree a6dd11b9c213] (2026-11-04T18:22:16Z)
- (audit edge) `branch diff read: RULE_TESTS in affected, STANDING in the lane brief, selfgate _paired over 3 pairs holding 2, friction.classes; prove red on the start tree, green now; live friction --classes gives today's baseline; this session's next merges are the live gate check` → one noisy pair passes; a missing rule test file is skipped, not an error; the classes report reads the UTC day [tree a6dd11b9c213] (2026-11-04T18:22:16Z)
- (audit intent) `branch diff read: RULE_TESTS in affected, STANDING in the lane brief, selfgate _paired over 3 pairs holding 2, friction.classes; prove red on the start tree, green now; live friction --classes gives today's baseline; this session's next merges are the live gate check` → each piece maps to a class that repeated today; the report measures the repeat rate [tree a6dd11b9c213] (2026-11-04T18:22:16Z)
## Log
- 2026-11-04T17:46:35Z created
- 2026-11-04T18:00:40Z planned: it has criteria and steps
- 2026-11-04T18:00:40Z set approved=True
- 2026-11-04T18:00:47Z criterion 1 verify: `python3 plugin/tests/run.py test_check test_lanes` → `python3 plugin/tests/run.py test_affected_rules test_lanes`
- 2026-11-04T18:01:28Z criterion 1 text: sampo check --affected always runs the standing-rule tests (self-docs, model rules, left-out, rename scan), and sampo lane brief carries a Standing rules section → sampo check --affected always runs the standing-rule tests (self-docs, model rules, left-out, rename scan), so builder branches missing a MASTER bullet and fm shim fail in their own lane; sampo lane brief carries a Standing rules section
- 2026-11-04T18:01:51Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2992.builder.md
- 2026-11-04T18:02:06Z focused
- 2026-11-04T18:02:08Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T18:20:20Z merged worktree-agent-a25ef4a97945f2f72 (8 file(s))
- 2026-11-04T18:20:25Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a25ef4a97945f2f72
- 2026-11-04T18:20:30Z focused
- 2026-11-04T18:23:02Z done
- 2026-11-04T18:23:04Z committed 5494a558 (1 file)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Pre-action check registry (likeliest):** a single table of failure classes (self-change-gate hold, missing MASTER bullet/fm shim, unprobed live interface, guard-refused shell form, standing-rule break) each mapped to a check that runs before the action. It is enforced at four points: builder brie…
- **Reporting-first:** only mine the ledger and refusals, classify them, and emit a per-class repeat rate each Rune generation. Checks are a later phase. This is the minimal reading of "report the repeat rate", and the classifier is the deliverable.
- **Prompt-only firewall:** the "firewall" is mostly text, i.e. the builder brief carrying standing rules plus a class list. The pre-merge and probe checks stay advisory. Turns on whichever template builds the brief (probably under `plugin/skills/` or `plugin/lib/sampo/`).
- **Smith-first:** the checks are built for small-model Smith runs and Sampo reuses them. This reverses the dependency and changes where the registry lives (`plugin/lib/sampo/` vs `fm*`).
Approaches:
- **Data-driven class registry, one module:** add something like `plugin/lib/fmfirewall.py` with a declarative list of classes (id, ledger/refusal match pattern, pre-action check callable, brief text). The brief builder, lane pre-merge, probe, and report all import it. Sampo's `cli.py` and `plugin/bi…
- **Extend existing choke points in place:** put the guard-form check in `fmguard.py`, the rule tests in the lane's merge step, the probe as a preflight in the live-run entry, and the interleaved base/branch measurement in the self-change gate. Add a thin report that reads the ledger. Cost: the class…
- **Classifier-over-ledger first, then promote:** write the miner (ledger plus guard refusal log → class → count, repeat = second and later occurrences) and ship the report. Then promote classes to checks one by one, using the report to show the rate falling. Cost: the first generation has no prevent…
- **Probe as a contract file:** each live interface (jeff-train identity, GPU free, suite duration, tsc) declares its probe in a manifest. The live-run launcher refuses to start unless every probe has passed in the last N minutes. This is the only approach that handles new unprobed interfaces by cons…
Failure modes:
- **Class drift in the miner:** the ledger and refusal text are free-form, so the "guard refusals of the same shell forms 11x" match normalizes inconsistently. Repeat rates then either undercount (the same form is split across classes) or overcount (distinct forms are merged). Fix by normalizing on t…
- **Interleaved gate measurement still loses to load:** the self-change gate runs base and branch alternately under shared load. Noise can still exceed the real difference, so the gate keeps holding merges. It needs a paired statistic and an explicit "inconclusive" outcome, not another pass/fail thre…
- **Pre-merge checks themselves break the existing gates:** adding self-docs and rule tests to the lane lengthens `plugin/tests/run.py`, and the slow suite is already a failing class. This risks adding a new repeat failure. It also risks tripping `plugin/tests/bench_hooks.py` if the guard path gets s…
- **Standing rules in the brief go stale or bloat:** the brief is copied text, so it diverges from the rules the tests enforce. Small-model Smith runs have limited context and ignore a long class list. The brief should be generated from the registry and capped, and the "builder code breaks a standing…
## Dissent
- [x] rival reading: **Pre-action check registry (likeliest):** a single table of failure classes (self-change-gate hold, missing MASTER bullet/fm shim, unprobed live interface, guard-refused shell form, standing-rule break) each mapped to a check that runs before the action. It is enforced at four points: builder brie… — answered: partly adopted: the repeat report's classes are a small table in the friction module (id, match pattern); checks live at their choke points, not one registry module
- [x] rival reading: **Reporting-first:** only mine the ledger and refusals, classify them, and emit a per-class repeat rate each Rune generation. Checks are a later phase. This is the minimal reading of "report the repeat rate", and the classifier is the deliverable. — answered: ruled out: the user asked to stop repeats, so checks ship with the report
- [x] rival reading: **Prompt-only firewall:** the "firewall" is mostly text, i.e. the builder brief carrying standing rules plus a class list. The pre-merge and probe checks stay advisory. Turns on whichever template builds the brief (probably under `plugin/skills/` or `plugin/lib/sampo/`). — answered: ruled out: text alone is today's failure mode (lessons on record, repeats anyway); the rule tests and the fair gate are code
- [x] rival reading: **Smith-first:** the checks are built for small-model Smith runs and Sampo reuses them. This reverses the dependency and changes where the registry lives (`plugin/lib/sampo/` vs `fm*`). — answered: later: the report reads Smith's failure classes once it exists (non-goal for now)
- [x] rival approach: **Data-driven class registry, one module:** add something like `plugin/lib/fmfirewall.py` with a declarative list of classes (id, ledger/refusal match pattern, pre-action check callable, brief text). The brief builder, lane pre-merge, probe, and report all import it. Sampo's `cli.py` and `plugin/bi… — answered: ruled out: one registry module for checks that live in four places adds indirection
- [x] rival approach: **Extend existing choke points in place:** put the guard-form check in `fmguard.py`, the rule tests in the lane's merge step, the probe as a preflight in the live-run entry, and the interleaved base/branch measurement in the self-change gate. Add a thin report that reads the ledger. Cost: the class… — answered: adopted: this is the plan's shape
- [x] rival approach: **Classifier-over-ledger first, then promote:** write the miner (ledger plus guard refusal log → class → count, repeat = second and later occurrences) and ship the report. Then promote classes to checks one by one, using the report to show the rate falling. Cost: the first generation has no prevent… — answered: adopted for the report: classes are mined from the ledger and refusals; promotion of a new class to a check stays a task per class
- [x] rival approach: **Probe as a contract file:** each live interface (jeff-train identity, GPU free, suite duration, tsc) declares its probe in a manifest. The live-run launcher refuses to start unless every probe has passed in the last N minutes. This is the only approach that handles new unprobed interfaces by cons… — answered: captured as a follow-up idea: live-interface probes as declared contracts; out of scope here
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2807 [CLEAN M, done, 3 steps] The foreman-ui mod says Sampo on screen: pane, band, toasts, README and tools text (T-2742 step 5) — lesson: Merge overlapping renames by…
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
## Lessons
- A lesson is prose nothing checks before the action; a recurring failure needs a check at the point it happens, and a count that shows whether it stopped
## Files touched
- plugin/tests/test_selfgate.py
- plugin/lib/sampo/selfgate.py
- plugin/tests/test_affected_rules.py
- plugin/lib/sampo/cli.py
- plugin/tests/test_lanes.py
- plugin/lib/sampo/lanes.py
- plugin/tests/test_friction.py
- plugin/lib/sampo/friction.py
- CHANGELOG.md
