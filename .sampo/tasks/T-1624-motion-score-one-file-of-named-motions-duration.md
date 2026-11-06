---
id: T-1624
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmmotion.py, plugin/lib/fmcli.py, plugin/tests/test_motion_score.py, CHANGELOG.md, plugin/skills/playbooks/references/ui/motion.md, MASTER.md, plugin/lib/fmdesign.py]
depends_on: []
source: user
created: 2026-10-22T20:57:09Z
updated: 2026-10-22T22:01:28Z
base: 11d8d394fc972ea17f94249866bf63c1f88d7335
base_tree: b50c18332c01445cb79e46a5625952233b8b180b
plan0_at: 2026-10-22T21:30:48Z
plan0_scope: [plugin/lib/fmmotion.py, plugin/lib/fmcli.py, plugin/tests/test_motion_score.py, CHANGELOG.md]
verified: strong
---
# Motion Score: one file of named motions (duration token, easing, properties, reduced form) checked by fm motion check
## Raw request
> Motion Score: one file of named motions (duration token, easing, properties, reduced form) checked by fm motion check
## Interpretation
A Motion Score is one file (motion.toml at the project root, or a path given) naming each motion the UI uses: name, duration (a number of ms or a token name resolved from DESIGN.md's Tokens table), easing (a named curve or cubic-bezier), the properties it animates, and its reduced form under prefers-reduced-motion (none, fade or instant). plugin/lib/fmmotion.py loads and checks it; fm motion check [PATH] [--json] lists problems (a motion with no reduced form, an unknown easing, a duration outside 0–2000 ms, duplicate names, a token DESIGN.md lacks). The UI playbook names the verb, so it works from Claude Code.
## Assumptions (confidence)
## Acceptance criteria
- [x] a score with a motion lacking a reduced form fails naming it — verify with `python3 plugin/tests/run.py test_motion_score.Format`
## Non-goals
## Approach (options → choice → why)
Options: CSS-first (parse @keyframes and transitions from stylesheets: no place for intent or the reduced form); a JSON score; a TOML score read with tomllib. Choice: TOML: hand-edited, allows comments, stdlib reader; a .json file with the same schema is accepted too. Compilers to CSS, WAAPI and three.js come in T-1625.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] schema and validation in fmmotion.py
3. [x] fm motion check verb
## Resume here
## Docs impact
~/.claude/foreman/MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_motion_score.Format` → ✗ exit 1 · run.py: no test matches test_motion_score.Format [ran] [tree d4776bb34b63] (2026-10-22T21:33:22Z)
- (ac 1) `python3 plugin/tests/run.py test_motion_score.Format 2>&1 | tail -40` → exit 0 · Ran 8 tests in 0.4s (1 classes, 16 at a time; slowest: Format 0s) / OK [ran] [tree d87a3588a79e] (2026-10-22T21:35:27Z)
- (step 2) `python3 plugin/tests/run.py test_motion_score.Format 2>&1 | tail -40` → exit 0 · Ran 8 tests in 0.4s (1 classes, 16 at a time; slowest: Format 0s) / OK [ran] [tree d87a3588a79e] (2026-10-22T21:35:27Z)
- (ac 1) `python3 plugin/tests/run.py test_motion_score.Format 2>&1 | tail -5` → exit 0 · Ran 8 tests in 0.3s (1 classes, 16 at a time; slowest: Format 0s) / OK [ran] [tree 8d7cd7d392e7] (2026-10-22T21:35:37Z)
- (step 3) `python3 plugin/tests/run.py test_motion_score.Format 2>&1 | tail -5` → exit 0 · Ran 8 tests in 0.3s (1 classes, 16 at a time; slowest: Format 0s) / OK [ran] [tree 8d7cd7d392e7] (2026-10-22T21:35:37Z)
- (step 2) `python3 plugin/tests/run.py test_motion_score.Format` → exit 0 · Ran 8 tests in 0.4s (1 classes, 16 at a time; slowest: Format 0s) / OK [ran] [tree 8d7cd7d392e7] (2026-10-22T21:35:39Z)
- (step 3) `python3 plugin/tests/run.py test_motion_score test_help` → exit 0 · Ran 16 tests in 0.9s (5 classes, 16 at a time; slowest: Help 1s, PromptApprovals 1s, Cli 0s) / OK [ran] [tree 90a81741cbc6] (2026-10-22T21:36:22Z)
- (step 1) `python3 plugin/tests/run.py test_motion_score` → ✗ exit 1 · Ran 18 tests in 1.3s (2 classes, 16 at a time; slowest: Cli 1s, Format 1s) / FAILED (2 classes) [ran] [tree b64a305226ad] (2026-10-22T21:46:08Z)
- (step 2) `python3 plugin/tests/run.py test_motion_score test_design_tokens` → exit 0 · Ran 52 tests in 9.1s (5 classes, 16 at a time; slowest: Extract 9s, Palette 4s, Cli 2s) / OK [ran] [tree 09396204b66c] (2026-10-22T21:48:53Z)
- (step 3) `python3 plugin/tests/run.py test_motion_score test_help` → exit 0 · Ran 24 tests in 1.9s (5 classes, 16 at a time; slowest: Help 2s, PromptApprovals 2s, Cli 1s) / OK [ran] [tree 09396204b66c] (2026-10-22T21:48:56Z)
- (step 3) `python3 plugin/tests/run.py test_motion_score test_help test_worker_reads test_doctor` → exit 0 · Ran 84 tests in 10.4s (26 classes, 16 at a time; slowest: WorkerOnlyReads 9s, Command 8s, ViewsRepair 6s) / OK [ran] [tree e956103ad731] (2026-10-22T21:54:55Z)
- (ac 1) `python3 plugin/tests/run.py test_motion_score.Format` → exit 0 · Ran 15 tests in 0.5s (1 classes, 16 at a time; slowest: Format 0s) / OK [ran] [tree 0b7fc7ed1d7b] (2026-10-22T22:00:38Z)
- (step 3) `python3 plugin/tests/run.py test_motion_score test_help test_worker_reads test_design_tokens` → exit 0 · Ran 60 tests in 3.4s (9 classes, 16 at a time; slowest: Extract 3s, WorkerOnlyReads 2s, Palette 1s) / OK [ran] [tree 0b7fc7ed1d7b] (2026-10-22T22:00:42Z)
- (audit adversary) `score text printed quoted; 1 MB cap, special files and non-UTF-8 refused, deep nesting exits 2` → tested [tree 0b7fc7ed1d7b] (2026-10-22T22:00:42Z)
- (audit edge) `every Tokens table read, case-insensitive heading, truncated values named, bare-number and unit-less durations explained, steps()/linear() accepted with bounded regexes` → tested [tree 0b7fc7ed1d7b] (2026-10-22T22:00:43Z)
- (audit operator) `fm motion check exit 0 clean, 1 problems, 2 unreadable; [motion.NAME] tables accepted` → tested [tree 0b7fc7ed1d7b] (2026-10-22T22:00:43Z)
- (audit maintainer) `none means rest state never played, documented for T-1625; extract keeps values up to 200 characters` → clean [tree 0b7fc7ed1d7b] (2026-10-22T22:00:43Z)
- (audit intent) `criterion: a score with a motion lacking a reduced form fails naming it` → met (18 tests) [tree 0b7fc7ed1d7b] (2026-10-22T22:00:43Z)
- (step 1) `python3 plugin/tests/run.py test_motion_score` → exit 0 · Ran 18 tests in 0.7s (2 classes, 16 at a time; slowest: Cli 1s, Format 0s) / OK [ran] [tree 0b7fc7ed1d7b] (2026-10-22T22:00:56Z)
- (ac 1) `python3 plugin/tests/run.py test_motion_score.Format` → exit 0 · Ran 15 tests in 0.5s (1 classes, 16 at a time; slowest: Format 0s) / OK [ran] [tree 0b7fc7ed1d7b] (2026-10-22T22:00:57Z)
- (audit adversary) `one fm-reviewer five-lens pass; all findings fixed test-first; criterion green after the merge` → hostile score files bounded [tree 0b7fc7ed1d7b] (2026-10-22T22:00:57Z)
- (audit edge) `one fm-reviewer five-lens pass; all findings fixed test-first; criterion green after the merge` → token tables, truncation, durations and easings [tree 0b7fc7ed1d7b] (2026-10-22T22:00:57Z)
- (audit intent) `one fm-reviewer five-lens pass; all findings fixed test-first; criterion green after the merge` → met [tree 0b7fc7ed1d7b] (2026-10-22T22:00:57Z)
## Log
- 2026-10-22T20:57:09Z created
- 2026-10-22T20:57:10Z set scope=['plugin/lib/fmmotion.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_motion_score.py', 'CHANGELOG.md']
- 2026-10-22T20:57:11Z split from T-1526 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:29:50Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_motion_score.Format`
- 2026-10-22T21:30:14Z criterion 1 text: a score with a motion lacking a reduced form fails naming it — verify with python3 plugin/tests/run.py test_motion_score.Format → a score with a motion lacking a reduced form fails naming it
- 2026-10-22T21:30:32Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1624.builder.md
- 2026-10-22T21:30:48Z focused
- 2026-10-22T21:36:00Z set scope=['plugin/lib/fmmotion.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_motion_score.py', 'CHANGELOG.md', 'plugin/skills/playbooks/references/ui/motion.md', 'MASTER.md']
- 2026-10-22T21:45:08Z set scope=['plugin/lib/fmmotion.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_motion_score.py', 'CHANGELOG.md', 'plugin/skills/playbooks/references/ui/motion.md', 'MASTER.md', 'plugin/lib/fmdesign.py']
- 2026-10-22T21:56:20Z merged worktree-agent-a2157612bc6afde97 (7 file(s))
- 2026-10-22T22:00:25Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2157612bc6afde97
- 2026-10-22T22:00:28Z focused
- 2026-10-22T22:00:44Z scope: MASTER.md fmmotion entry, plugin/skills/playbooks/references/ui/motion.md (none = rest state), plugin/lib/fmdesign.py (extract keeps 200-character values) and fmcli registration
- 2026-10-22T22:01:28Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Motion: choreography, timing and reduced motion (skills/playbooks/references/ui/motion.md)
- T-1492 [FEATURE M, done, 2 steps] Motion playbook: choreography, timing and reduced motion — lesson: Sibling playbooks need one stated precedence rule where their number…
- T-1506 [FEATURE M, done, 3 steps] fm design lint: a stdlib check for generic tells and craft slips — lesson: A lint's fixtures should include the real-world forms of eac…
- decision 2026-10-22: T-1479 brainstorm: 548 ideas grounded into 26 capabilities; round 1 (19 tasks: UI design, motion and 3D playbooks and template, fm design lint, TUI …
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmdesign.py, plugin/lib/fmmotion.py, plugin/skills/playbooks/references/ui/motion.md, plugin/tests/test_motion_score.py; re-ground the plan against them before editing
## Why not caught
tests only fed tables written by fm design extract
## Lessons
- A format that reads another tool's table must re-read the header at every table and say when a value was cut by the writer, or valid values read as errors
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_motion_score.py
- plugin/lib/fmmotion.py
- plugin/lib/fmcli.py
- plugin/skills/playbooks/references/ui/motion.md
- MASTER.md
- CHANGELOG.md
- plugin/lib/fmdesign.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmimg.py
- plugin/lib/fmmutate.py
- plugin/lib/fmreplay.py
- plugin/tests/fixtures/gen_evasions.py
- plugin/tests/fixtures/guard_cases.jsonl
- plugin/tests/fixtures/guard_evasions.jsonl
- plugin/tests/fixtures/guard_untested.json
- plugin/tests/test_code_tui.py
- plugin/tests/test_guard_hardening.py
- plugin/tests/test_raster.py
- plugin/tests/test_reliability_tools.py
- plugin/tests/test_replay.py
- plugin/tests/test_site_hero.py
- site/build.py
- site/index.html
- site/style.css
- plugin/lib/fmlanes.py
- plugin/tests/test_lanes.py
