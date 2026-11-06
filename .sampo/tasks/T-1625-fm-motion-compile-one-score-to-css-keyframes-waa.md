---
id: T-1625
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmmotion.py, plugin/lib/fmcli.py, plugin/tests/test_motion_score.py, CHANGELOG.md, MASTER.md]
depends_on: [T-1624]
source: user
created: 2026-10-22T20:57:12Z
updated: 2026-10-22T23:03:20Z
base: f4b25c5cbac8bdd96f6970630b8b8d048d7051a6
base_tree: 9cf46e4cc74ef52f66270084dcd7fe20a81e1e7c
plan0_at: 2026-10-22T22:28:16Z
plan0_scope: [plugin/lib/fmmotion.py, plugin/lib/fmcli.py, plugin/tests/test_motion_score.py, CHANGELOG.md]
verified: strong
---
# fm motion compile: one score to CSS keyframes, WAAPI and three.js tween params with equal timings
## Raw request
> fm motion compile: one score to CSS keyframes, WAAPI and three.js tween params with equal timings
## Interpretation
fm motion compile [PATH] --to css|waapi|three emits a Motion Score (T-1624) as CSS @keyframes and transition custom properties, a WAAPI options object per motion, or three.js tween parameters; every target carries the same duration and easing, and each motion's reduced form is emitted too (a prefers-reduced-motion block for CSS, a reduced variant object for the others).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm motion compile emits three targets whose durations all equal the score's — verify with `python3 plugin/tests/run.py test_motion_score.Compile`
## Non-goals
## Approach (options → choice → why)
Options: a template engine (a dependency); one emitter per target as plain string builders; a single JSON the targets read at runtime. Choice: three string emitters: no dependency, diffable output, and a test can compare durations across targets.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test comparing durations
2. [x] three string emitters
3. [x] --to flag
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_motion_score.Compile 2>&1 | tail -8` → ✗ exit 1 · Ran 5 tests in 1.9s (1 classes, 16 at a time; slowest: Compile 0s) / FAILED (1 classes) [ran] [tree 525f17007f85] (2026-10-22T22:33:24Z)
- (step 1) `python3 plugin/tests/run.py test_motion_score.Compile` → ✗ exit 1 · Ran 5 tests in 0.6s (1 classes, 16 at a time; slowest: Compile 0s) / FAILED (1 classes) [ran] [tree 525f17007f85] (2026-10-22T22:33:27Z)
- (ac 1) `python3 plugin/tests/run.py test_motion_score.Compile 2>&1 | tail -40` → ✗ exit 1 · Ran 5 tests in 2.4s (1 classes, 16 at a time; slowest: Compile 2s) / FAILED (1 classes) [ran] [tree 11f27ba3d980] (2026-10-22T22:35:47Z)
- (step 2) `python3 plugin/tests/run.py test_motion_score.Compile` → exit 0 · Ran 6 tests in 0.7s (1 classes, 16 at a time; slowest: Compile 0s) / OK [ran] [tree 2564cb572a3e] (2026-10-22T22:39:31Z)
- (step 3) `python3 plugin/tests/run.py test_motion_score` → exit 0 · Ran 24 tests in 0.8s (3 classes, 16 at a time; slowest: Cli 1s, Compile 1s, Format 0s) / OK [ran] [tree 2564cb572a3e] (2026-10-22T22:39:32Z)
- (step 3) `python3 plugin/tests/run.py test_motion_score` → exit 0 · Ran 24 tests in 1.2s (3 classes, 16 at a time; slowest: Cli 1s, Compile 1s, Format 1s) / OK [ran] [tree f6e6b7bda484] (2026-10-22T22:41:00Z)
- (step 3) `python3 plugin/tests/run.py test_motion_score` → ✗ exit 1 · Ran 26 tests in 2.3s (3 classes, 16 at a time; slowest: Cli 2s, Compile 2s, Format 1s) / FAILED (1 classes) [ran] [tree 3158fd992a0d] (2026-10-22T22:54:03Z)
- (step 3) `python3 plugin/tests/run.py test_motion_score` → exit 0 · Ran 26 tests in 3.0s (3 classes, 16 at a time; slowest: Compile 3s, Cli 2s, Format 2s) / OK [ran] [tree 501a9d6cf56e] (2026-10-22T22:54:50Z)
- (ac 1) `python3 plugin/tests/run.py test_motion_score` → exit 0 · Ran 26 tests in 1.0s (3 classes, 16 at a time; slowest: Compile 1s, Cli 1s, Format 0s) / OK [ran] [tree 1d37d1598b73] (2026-10-22T23:02:44Z)
- (ac 1) `python3 plugin/tests/run.py test_motion_score.Compile` → exit 0 · Ran 8 tests in 1.0s (1 classes, 16 at a time; slowest: Compile 1s) / OK [ran] [tree 1d37d1598b73] (2026-10-22T23:02:46Z)
- (audit intent) `fm-reviewer full pass on the lane; MEDIUM (none transition invalidating a comma list) and five LOWs fixed test-first: all 0s transition, header label escapes */ and </, compile --json problems on stdout, check refuses --to/--out, ASCII names, JS reduced() matches the CSS` → fm motion compile turns one clean Motion Score into CSS custom properties and keyframes, a WAAPI module and three.js tween params, all carrying the score's durations and easings [tree 1d37d1598b73] (2026-10-22T23:02:46Z)
- (audit adversary) `fm-reviewer full pass on the lane; MEDIUM (none transition invalidating a comma list) and five LOWs fixed test-first: all 0s transition, header label escapes */ and </, compile --json problems on stdout, check refuses --to/--out, ASCII names, JS reduced() matches the CSS` → names and properties are ASCII-only by regex and JSON-dumped into JS; the header label escapes */ and </; --out refuses the score itself, replaces a symlink rather than writing through it [tree 1d37d1598b73] (2026-10-22T23:02:46Z)
- (audit edge) `fm-reviewer full pass on the lane; MEDIUM (none transition invalidating a comma list) and five LOWs fixed test-first: all 0s transition, header label escapes */ and </, compile --json problems on stdout, check refuses --to/--out, ASCII names, JS reduced() matches the CSS` → reduced forms (none/instant/fade) shared by all targets; a none motion's transition is all 0s so a comma list stays valid; JS and CSS agree on reduce for every data-motion value; bezier/steps/linear easing match the CSS Easing spec [tree 1d37d1598b73] (2026-10-22T23:02:46Z)
- (audit operator) `fm-reviewer full pass on the lane; MEDIUM (none transition invalidating a comma list) and five LOWs fixed test-first: all 0s transition, header label escapes */ and </, compile --json problems on stdout, check refuses --to/--out, ASCII names, JS reduced() matches the CSS` → problems exit 1 and write nothing, as JSON under --json; check refuses compile's flags instead of ignoring them [tree 1d37d1598b73] (2026-10-22T23:02:46Z)
## Log
- 2026-10-22T20:57:12Z created
- 2026-10-22T20:57:13Z set scope=['plugin/lib/fmmotion.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_motion_score.py', 'CHANGELOG.md']
- 2026-10-22T20:57:14Z split from T-1526 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T20:57:14Z set depends_on=['T-1624']
- 2026-10-22T21:29:50Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_motion_score.Compile`
- 2026-10-22T21:30:14Z criterion 1 text: fm motion compile emits three targets whose durations all equal the score's — verify with python3 plugin/tests/run.py test_motion_score.Compile → fm motion compile emits three targets whose durations all equal the score's
- 2026-10-22T22:28:03Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1625.builder.md
- 2026-10-22T22:28:16Z focused
- 2026-10-22T22:38:45Z set scope=['plugin/lib/fmmotion.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_motion_score.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-22T22:38:52Z scope: widened to MASTER.md, the main thread asked for one short addition to the fmmotion entry
- 2026-10-22T23:02:23Z merged worktree-agent-afaf730de2938d0a8 (5 file(s))
- 2026-10-22T23:02:23Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-afaf730de2938d0a8
- 2026-10-22T23:02:35Z focused
- 2026-10-22T23:02:44Z scope: MASTER.md — the fmmotion entry names compile (builder, logged on the lane)
- 2026-10-22T23:03:20Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1526 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Motion Score: one file of named motions that compiles to CSS, WAAPI, thr
- T-1624 [FEATURE M, done, 3 steps] Motion Score: one file of named motions (duration token, easing, properties, reduced form) checked by fm motion check — lesson: A forma…
- playbook Motion: choreography, timing and reduced motion (skills/playbooks/references/ui/motion.md)
- decision 2026-10-22: Round-3 L tasks split into 34 M/S children (T-1618..T-1669, T-1609/T-1610 for T-1513); the parts recon judged speculative went to the inbox as follo…
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmmotion.py, plugin/tests/test_motion_score.py; re-ground the plan against them before editing
## Lessons
- In CSS, none inside a comma-separated transition list invalidates the whole declaration; emit all 0s for an empty transition
## Plan gaps
- failed first: step 1 failing test comparing durations
## Files touched
- plugin/tests/test_motion_score.py
- plugin/lib/fmmotion.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
