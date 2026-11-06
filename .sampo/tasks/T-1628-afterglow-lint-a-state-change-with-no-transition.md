---
id: T-1628
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmdesign.py, plugin/tests/test_motion_verify.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-22T20:57:19Z
updated: 2026-10-22T22:23:14Z
base: 1d177f86f5b1b8c657f76476f0feab458f52a71e
base_tree: 7840c0572fbbee8c3b7583301ac4a1aae5961cf5
plan0_at: 2026-10-22T21:56:18Z
plan0_scope: [plugin/lib/fmdesign.py, plugin/tests/test_motion_verify.py, CHANGELOG.md]
verified: strong
---
# Afterglow lint: a state change with no transition, as a rule in fm design lint
## Raw request
> Afterglow lint: a state change with no transition, as a rule in fm design lint
## Interpretation
fm design lint gains an afterglow rule: a state change (:hover, :focus, :active, [aria-*], .is-*) that changes colour, background, transform or opacity with no transition or animation on the element is flagged, since an instant jump reads as a glitch. Reduced-motion blocks are exempt.
## Assumptions (confidence)
## Acceptance criteria
- [x] a :hover colour change with no transition is flagged — verify with `python3 plugin/tests/run.py test_motion_verify.Afterglow`
## Non-goals
## Approach (options → choice → why)
Options: a browser check (heavy); a CSS rule in the existing lint engine next to untokened-duration; a style guide line only. Choice: the lint rule: the engine already parses blocks and selectors, so it's a few lines and a fixture.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test fixture CSS
2. [x] rule next to untokened-duration
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_motion_verify.Afterglow` → exit 0 · Ran 2 tests in 0.2s (1 classes, 16 at a time; slowest: Afterglow 0s) / OK [ran] [tree 6d4cb95cb9cf] (2026-10-22T21:57:16Z)
- (step 2) `python3 plugin/tests/run.py test_design_lint` → exit 0 · Ran 29 tests in 0.8s (3 classes, 16 at a time; slowest: Allow 1s, Rules 1s, Site 0s) / OK [ran] [tree 6d4cb95cb9cf] (2026-10-22T21:57:17Z)
- (step 2) `python3 plugin/tests/run.py test_motion_verify test_design_lint` → exit 0 · Ran 31 tests in 0.8s (4 classes, 16 at a time; slowest: Allow 1s, Rules 1s, Site 0s) / OK [ran] [tree 83d6d2de9287] (2026-10-22T22:10:04Z)
- (ac 1) `python3 plugin/tests/run.py test_motion_verify.Afterglow` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: Afterglow 0s) / OK [ran] [tree dd88c694b653] (2026-10-22T22:23:08Z)
- (step 2) `python3 plugin/tests/run.py test_motion_verify test_design_lint` → exit 0 · Ran 31 tests in 1.1s (4 classes, 16 at a time; slowest: Allow 1s, Rules 1s, Afterglow 0s) / OK [ran] [tree dd88c694b653] (2026-10-22T22:23:09Z)
- (audit self) `read the rule and fixtures after the review fixes` → * transitions and nested & selectors no longer misfire; zero-length and delay-only transitions count as none; no-preference isn't exempt; one finding per block [tree dd88c694b653] (2026-10-22T22:23:10Z)
- (audit design) `review design lens` → message names the element, says the match is by selector text and how to silence it; site transitions 150 ms colour/opacity only [tree dd88c694b653] (2026-10-22T22:23:10Z)
- (ac 1) `python3 plugin/tests/run.py test_motion_verify.Afterglow` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: Afterglow 0s) / OK [ran] [tree dd88c694b653] (2026-10-22T22:23:12Z)
- (audit design) `one fm-reviewer pass (self, design); findings fixed test-first` → clear message and safe defaults [tree dd88c694b653] (2026-10-22T22:23:12Z)
- (audit self) `one fm-reviewer pass (self, design); findings fixed test-first` → no findings [tree dd88c694b653] (2026-10-22T22:23:12Z)
## Log
- 2026-10-22T20:57:19Z created
- 2026-10-22T20:57:20Z set scope=['plugin/lib/fmdesign.py', 'plugin/tests/test_motion_verify.py', 'CHANGELOG.md']
- 2026-10-22T20:57:21Z split from T-1527 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:29:51Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_motion_verify.Afterglow`
- 2026-10-22T21:30:15Z criterion 1 text: a :hover colour change with no transition is flagged — verify with python3 plugin/tests/run.py test_motion_verify.Afterglow → a :hover colour change with no transition is flagged
- 2026-10-22T21:55:58Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1628.builder.md
- 2026-10-22T21:56:17Z focused
- 2026-10-22T22:10:02Z scope: site/style.css (150 ms transitions on nav, copy, side links, chart marks) and fixtures/design/afterglow/, so the site's own clean-lint test passes
- 2026-10-22T22:22:56Z merged worktree-agent-a06e3b6ec0efdfaf2 (8 file(s))
- 2026-10-22T22:22:57Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a06e3b6ec0efdfaf2
- 2026-10-22T22:23:01Z focused
- 2026-10-22T22:23:11Z scope: site/style.css gained short hover transitions so the site stays lint-clean under the new rule; MASTER.md one line
- 2026-10-22T22:23:14Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1506-review: Verdict:** changes needed. I could only read the code, not run it, so every finding below is a code trace and none was executed. Four fixes shoul…
- playbook Motion: choreography, timing and reduced motion (skills/playbooks/references/ui/motion.md)
- T-1646 [FEATURE M, planned, 3 steps] Design gates: an accessibility and motion audit gate and a design-debt sweep
- decision 2026-10-20: T-1300 slate: round 1 = C1 renderer, C2 motion engine, C3 live track, C4 gradients/contrast/focal line, C5 event flashes, C7 odometer/sparklines, C2…
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmdesign.py, plugin/tests/test_motion_verify.py; re-ground the plan against them before editing
## Why not caught
fixtures covered flat selectors only
## Lessons
- A lint that exits 1 must close its known false-positive classes (universal selectors, nesting) before it joins the default set
## Files touched
- plugin/tests/fixtures/design/afterglow/slop.css
- plugin/tests/fixtures/design/afterglow/crafted.css
- plugin/tests/test_motion_verify.py
- plugin/lib/fmdesign.py
- site/style.css
- CHANGELOG.md
- plugin/tests/fixtures/design/afterglow/crafted_nest.css
- plugin/tests/fixtures/design/afterglow/crafted_star.css
