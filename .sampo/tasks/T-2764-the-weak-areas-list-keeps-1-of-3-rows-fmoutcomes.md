---
id: T-2764
type: CLEAN
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/outcomes.py, plugin/tests/test_metacog.py]
depends_on: []
source: self
created: 2026-11-03T04:14:01Z
updated: 2026-11-03T14:57:30Z
builder_model: sonnet
base: 7f2872fdf4ce40fd98c31d3f0c4768d2d54cb1d4
base_tree: b3eb410e32c8ea61fd2c3bd61fb15b96eb64af89
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-03T04:36:01Z
plan0_scope: [plugin/lib/sampo/outcomes.py, plugin/tests/test_metacog.py]
lane_stop: merged 2026-11-03T04:54:21Z
verified: strong
---
# The weak-areas list (fm outcomes --atlas, the friction digest) shows a file or language only when 2+ of its tasks needed a later fix or closed weak, the bar fm focus's caution already uses; one bad task is an anecdote
## Raw request
> CLEAN: the weak-areas list keeps 1-of-3 rows (fmoutcomes.py:1068 keeps r[2] or r[3]) while caution() needs bad>=2 (:1079); filter atlas_lines to bad>=2 and skip plugin/tests/fixtures
## Interpretation
Reading 1 (chosen): atlas_lines (plugin/lib/sampo/outcomes.py:1064) keeps any row with one bad or weak task, while caution() (:1076) needs bad >= 2. So the friction digest listed three crafted*.css fixtures at '1 of 3', likely one task counted three times. Use the same 2+ bar in atlas_lines, counting bad and weak together. Reading 2 (ruled out): skip plugin/tests/fixtures by path. That is a hardcoded list, and a 1-of-3 source file is just as much an anecdote.
## Assumptions (confidence)
## Acceptance criteria
- [x] a file with 1 bad task of 3 is left out of atlas_lines and a file with 2 of 3 is listed; with none left the list says so — verify with `python3 plugin/tests/run.py test_metacog`
- [x] the friction digest and the outcomes suites stay green — verify with `python3 plugin/tests/run.py test_metacog test_friction test_inbox_more`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: change the filter to r[2] + r[3] >= 2, matching caution's threshold. Likely outcome: one line plus one test. Fails if: a user relies on single-task rows; fm outcomes --atlas --json still returns every row.
2. Dedupe rows by task id. Fails if: atlas() doesn't keep task ids, so this needs a schema change for a cosmetic list.
3. Do less: leave it as it is. Fails if: the digest keeps sending the recon pass to noise.
Choice 1 (90%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_metacog: 1-of-3 rows left out, 2-of-3 kept
2. [x] atlas_lines keeps rows with bad + weak >= 2
## Resume here
## Docs impact
none: fm outcomes --atlas output is the doc
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_metacog 2>&1 | tail -8` → ✗ exit 1 · Ran 4 tests in 19.9s (3 classes, 16 at a time; slowest: Atlas 16s, Calibrate 10s, Honest 2s) / FAILED (1 classes: test_metacog.Atlas) [ran] [tree f524cd5baa64] [world 2f1906870a] (2026-11-03T04:38:27Z)
- (ac 2) `python3 plugin/tests/run.py test_metacog test_friction test_inbox_more 2>&1 | tail -8` → exit 0 · Ran 64 tests in 43.0s (17 classes, 16 at a time; slowest: Friction 41s, Served 20s, Atlas 20s) / OK [ran] [tree 262e32cdca16] [world 2f1906870a] (2026-11-03T04:39:16Z)
- (step 1) `python3 plugin/tests/run.py test_metacog test_friction test_inbox_more 2>&1 | tail -8` → exit 0 · Ran 64 tests in 43.0s (17 classes, 16 at a time; slowest: Friction 41s, Served 20s, Atlas 20s) / OK [ran] [tree 262e32cdca16] [world 2f1906870a] (2026-11-03T04:39:16Z)
- (step 1) `python3 plugin/tests/run.py test_metacog` → exit 0 · Ran 4 tests in 20.1s (3 classes, 16 at a time; slowest: Atlas 19s, Calibrate 12s, Honest 3s) / OK [ran] [tree 262e32cdca16] [world 2f1906870a] (2026-11-03T04:39:40Z)
- (step 2) `python3 plugin/tests/run.py test_metacog test_friction test_inbox_more` → exit 0 · Ran 64 tests in 36.8s (17 classes, 16 at a time; slowest: Friction 36s, Atlas 20s, Served 19s) / OK [ran] [tree 262e32cdca16] [world 2f1906870a] (2026-11-03T04:40:18Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  version skew         config-c6930b ran 1.2.50, lacks 654 (T-0001, T-0002, T-0012, T-0042 …); gitter-588bc6 ran 1.2.50, lacks 654 (T-0001, T-0002, T-0012, T-0042 …); trader-feebec ran 1.2.50, lac (slower: 51.9 s vs a usual 32.3 s); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · SessionEnd                 159.7   204.7     150  [0] / machine busy (load 3.1 per core): judged by each hook's CPU time, not wall time (T-0805) [ran] [tree 255e2fab14f1] [world 2f1906870a] (2026-11-03T04:48:44Z)
- (ac 1) `python3 plugin/tests/run.py test_metacog` → exit 0 · Ran 4 tests in 3.8s (3 classes, 16 at a time; slowest: Atlas 4s, Calibrate 3s, Honest 1s) / OK [ran] [tree 1b964dd8dbe8] [world 2f1906870a] (2026-11-03T14:56:27Z)
- (ac 2) `python3 plugin/tests/run.py test_metacog test_friction test_inbox_more` → exit 0 · Ran 64 tests in 8.3s (17 classes, 16 at a time; slowest: Friction 8s, Served 6s, Atlas 5s) / OK [ran] [tree 1b964dd8dbe8] [world 2f1906870a] (2026-11-03T14:56:27Z)
- (audit intent) `self: read the diff; the weak-areas list needs two distinct bad or weak tasks` → one bad task is an anecdote; the atlas lists an area at caution()'s bar [tree 1b964dd8dbe8] (2026-11-03T14:56:27Z)
- (audit edge) `self: read the diff; the weak-areas list needs two distinct bad or weak tasks` → max(bad, weak) >= 2 means two distinct tasks; a task both bad and weak counts once [tree 1b964dd8dbe8] (2026-11-03T14:56:27Z)
- (audit adversary) `self: read the diff; the weak-areas list needs two distinct bad or weak tasks` → no external input; counts come from the outcome record [tree 1b964dd8dbe8] (2026-11-03T14:56:27Z)
- (audit self) `self: read the diff; the weak-areas list needs two distinct bad or weak tasks` → no findings [tree 1b964dd8dbe8] (2026-11-03T14:56:27Z)
- `python3 plugin/tests/run.py test_metacog` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T14:56:27Z [ran] [tree 1b964dd8dbe8] [world 2f1906870a] (2026-11-03T14:56:57Z)
- (audit intent) `self: read the diff; the weak-areas list needs two distinct bad or weak tasks` → one bad task is an anecdote; the atlas lists an area at caution()'s bar [tree 1b964dd8dbe8] (2026-11-03T14:56:57Z)
- (audit edge) `self: read the diff; the weak-areas list needs two distinct bad or weak tasks` → max(bad, weak) >= 2 means two distinct tasks; a task both bad and weak counts once [tree 1b964dd8dbe8] (2026-11-03T14:56:57Z)
- (audit adversary) `self: read the diff; the weak-areas list needs two distinct bad or weak tasks` → no external input; counts come from the outcome record [tree 1b964dd8dbe8] (2026-11-03T14:56:57Z)
- (audit self) `self: read the diff; the weak-areas list needs two distinct bad or weak tasks` → no findings [tree 1b964dd8dbe8] (2026-11-03T14:56:57Z)
## Log
- 2026-11-03T04:14:01Z created
- 2026-11-03T04:19:20Z planned from capture
- 2026-11-03T04:19:21Z set approved=True
- 2026-11-03T04:35:22Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2764.builder.md
- 2026-11-03T04:35:54Z focused
- 2026-11-03T04:36:01Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-03T04:54:21Z merged worktree-agent-a9b97501e2af35375 (2 file(s))
- 2026-11-03T04:54:41Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9b97501e2af35375
- 2026-11-03T05:48:27Z focused
- 2026-11-03T05:48:29Z scope: files outside the scope since focus came from other lanes' merge commits, not this task's edits
- 2026-11-03T05:48:31Z paused: focus moved to T-2765
- 2026-11-03T14:56:13Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T14:56:13Z focused
- 2026-11-03T14:57:30Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2763 [CLEAN S, active, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate s…
- T-2610 [FIX M, done, 3 steps] Calibration reads compare like with like: a close or a task or choice bet counts once its 30-day window finished — lesson: When one read of…
- research T-2337-review: Changes needed.** Two acceptance criteria are not met: no bar check runs at finish, and Foreman's own evidence can still move a bar. I read the c…
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_outcomes.py
## Preflight
Changed in scope since this was planned (2026-11-03): plugin/lib/sampo/outcomes.py, plugin/tests/test_metacog.py; re-ground the plan against them before editing
## Behaviour lock
none: the builder lane's pre-edit fm check timed out at 600 s under machine load ~55 on 2026-11-03 (T-2797), so no lock was recorded before the first edit; the change is covered by its targeted tests and the post-merge full suite
## Lessons
- A threshold must count distinct things, not one thing twice
## Files touched
- plugin/tests/test_metacog.py
- plugin/lib/sampo/outcomes.py
