---
id: T-1506
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmdesign.py, plugin/lib/fmcli.py, plugin/tests/test_design_lint.py, plugin/tests/fixtures/design, CHANGELOG.md, site, MASTER.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:25Z
updated: 2026-10-22T18:18:24Z
base: 1844b2bd3991cdb277a64d487da5d1da9cb281b5
base_tree: e1b9cc8c368e83fe3daa428943f512f40e428423
plan0_at: 2026-10-22T17:41:59Z
plan0_scope: [plugin/lib/fmdesign.py plugin/lib/fmcli.py plugin/tests/test_design_lint.py plugin/tests/fixtures/design CHANGELOG.md site]
verified: strong
---
# fm design lint: a stdlib check for generic tells and craft slips
## Raw request
> fm design lint: a stdlib check for generic tells and craft slips
## Interpretation
Brainstorm T-1479 cluster 4: nothing checks UI code for the tells of generated design or for craft slips. A stdlib lint over .css/.scss/.html/.jsx/.tsx/.vue/.svelte files: generic tells (only a system or Inter font stack, the purple-to-blue gradient, one border-radius everywhere, the same soft grey shadow on every card), and craft slips (img without alt, an animation or transition with no prefers-reduced-motion path, animating width/height/top/left instead of transform/opacity, a flash faster than 3 per second, Math.random() in rendering code without a seed, a duration not taken from a token when tokens exist). Each rule has an id, a one-line why and a fix; each ships a slop/crafted fixture pair that gates its precision.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm design lint flags each rule's slop fixture and passes its crafted twin, with rule id, file:line and the fix — verify with `cd plugin/tests && python3 -m unittest test_design_lint.Rules`
- [x] the lint over Foreman's own site/ is clean, each finding fixed or allowed with its reason inline — verify with `cd plugin/tests && python3 -m unittest test_design_lint.Site`
## Non-goals
## Approach (options → choice → why)
Options: a headless browser computing styles (a dependency); a full CSS parser (large); chosen: regex and small tokenizers per rule over source text, precision first (a rule that can't be precise is left out), rule list documented in the verb's help; an inline 'design-lint: allow RULE why' comment silences one finding. ponytail: text rules, not computed style.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: a fixture pair per rule
2. [x] plugin/lib/fmdesign.py rules and the fm design lint verb
3. [x] run it on site/ and settle each finding
## Resume here
## Docs impact
CHANGELOG.md line; MASTER.md entry; the verb's help
## Verification evidence
- (step 1) `python3 -m unittest discover -s plugin/tests -p test_design_lint.py` → ✗ exit 1 · Ran 1 test in 0.000s / FAILED (errors=1) [ran] [tree 3c530b3034a7] (2026-10-22T17:46:04Z)
- (step 2) `python3 -m unittest discover -s plugin/tests -p test_design_lint.py` → exit 0 · Ran 19 tests in 1.755s / OK [ran] [tree c72b3f5a564b] (2026-10-22T17:55:40Z)
- (step 3) `python3 plugin/bin/fm design lint site` → exit 0 · design lint: clean (2 file(s)) [ran] [tree c72b3f5a564b] (2026-10-22T17:55:41Z)
- (step 2) `python3 -m unittest discover -s plugin/tests -p test_design_lint.py` → exit 0 · Ran 19 tests in 1.309s / OK [ran] [tree bb4e54ec6583] (2026-10-22T17:57:55Z)
- (step 2) `python3 -m unittest discover -s plugin/tests -p test_design_lint.py` → exit 0 · Ran 28 tests in 1.885s / OK [ran] [tree 9f4a8abf2d02] (2026-10-22T18:14:52Z)
- (step 3) `python3 plugin/bin/fm design lint site` → exit 0 · design lint: clean (2 file(s)) [ran] [tree 9f4a8abf2d02] (2026-10-22T18:14:52Z)
- `cd plugin/tests && python3 -m unittest test_design_lint` → ✗ exit 1 · Ran 1 test in 0.000s / FAILED (errors=1) (start tree + this task's tests) [ran] [tree 9aa81cfc85e6] (2026-10-22T18:17:26Z)
- `cd plugin/tests && python3 -m unittest test_design_lint` → exit 0 · Ran 28 tests in 2.277s / OK [ran] [tree 9aa81cfc85e6] (2026-10-22T18:17:26Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_design_lint.Rules` → exit 0 · Ran 9 tests in 0.685s / OK [ran] [tree 9aa81cfc85e6] (2026-10-22T18:17:37Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_design_lint.Site` → exit 0 · Ran 1 test in 0.007s / OK [ran] [tree 9aa81cfc85e6] (2026-10-22T18:17:38Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_design_lint` → exit 0 · Ran 28 tests in 1.140s / OK [ran] [tree 9aa81cfc85e6] (2026-10-22T18:17:39Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_design_lint` → exit 0 · Ran 28 tests in 1.082s / OK [ran] [tree 9aa81cfc85e6] (2026-10-22T18:17:41Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_design_lint` → exit 0 · Ran 28 tests in 1.099s / OK [ran] [tree 9aa81cfc85e6] (2026-10-22T18:17:42Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_design_lint.Rules` → exit 0 · Ran 9 tests in 0.489s / OK [ran] [tree a7f9e158cd03] (2026-10-22T18:17:53Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_design_lint.Site` → exit 0 · Ran 1 test in 0.008s / OK [ran] [tree a7f9e158cd03] (2026-10-22T18:17:53Z)
- (audit intent) `builder test-first on fixtures; one fm-reviewer pass found 7 issue groups (a /dev/zero symlink hang, CSS-in-JS dynamic values, one-radius scope, // comments, Tailwind/Next forms, Math.random scope, smaller edges), all fixed in a second round with 21 new fixtures; proved red on the start tree; site/ lints clean; affected 230 tests green` → catches the generic tells and craft slips the design playbooks name, from Claude Code or fm code [tree a7f9e158cd03] (2026-10-22T18:17:53Z)
- (audit adversary) `builder test-first on fixtures; one fm-reviewer pass found 7 issue groups (a /dev/zero symlink hang, CSS-in-JS dynamic values, one-radius scope, // comments, Tailwind/Next forms, Math.random scope, smaller edges), all fixed in a second round with 21 new fixtures; proved red on the start tree; site/ lints clean; affected 230 tests green` → regular files only, bounded reads, non-blocking open, realpath dedupe, 5000-file cap, linear on hostile input (a test holds it under 5 s) [tree a7f9e158cd03] (2026-10-22T18:17:53Z)
- (audit edge) `builder test-first on fixtures; one fm-reviewer pass found 7 issue groups (a /dev/zero symlink hang, CSS-in-JS dynamic values, one-radius scope, // comments, Tailwind/Next forms, Math.random scope, smaller edges), all fixed in a second round with 21 new fixtures; proved red on the start tree; site/ lints clean; affected 230 tests green` → the Math.random render-path scan doesn't skip strings or comments (stated weakest link); not-read forms listed in the help [tree a7f9e158cd03] (2026-10-22T18:17:53Z)
- (audit maintainer) `builder test-first on fixtures; one fm-reviewer pass found 7 issue groups (a /dev/zero symlink hang, CSS-in-JS dynamic values, one-radius scope, // comments, Tailwind/Next forms, Math.random scope, smaller edges), all fixed in a second round with 21 new fixtures; proved red on the start tree; site/ lints clean; affected 230 tests green` → one fixture pair per rule is the precision gate; MASTER.md lists fmdesign [tree a7f9e158cd03] (2026-10-22T18:17:53Z)
- (audit operator) `builder test-first on fixtures; one fm-reviewer pass found 7 issue groups (a /dev/zero symlink hang, CSS-in-JS dynamic values, one-radius scope, // comments, Tailwind/Next forms, Math.random scope, smaller edges), all fixed in a second round with 21 new fixtures; proved red on the start tree; site/ lints clean; affected 230 tests green` → exit 0 clean, 1 findings, 2 no UI files [tree a7f9e158cd03] (2026-10-22T18:17:53Z)
## Log
- 2026-10-22T17:36:25Z created
- 2026-10-22T17:41:47Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1506.builder.md
- 2026-10-22T17:41:58Z focused
- 2026-10-22T17:59:00Z set scope=['plugin/lib/fmdesign.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_design_lint.py', 'plugin/tests/fixtures/design', 'CHANGELOG.md', 'site', 'MASTER.md']
- 2026-10-22T18:17:10Z merged worktree-agent-a54c85e87a50d8471 (52 file(s))
- 2026-10-22T18:17:11Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a54c85e87a50d8471
- 2026-10-22T18:17:11Z focused
- 2026-10-22T18:18:22Z done
- 2026-10-22T18:18:24Z committed 496e6438 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Motion: choreography, timing and reduced motion (skills/playbooks/references/ui/motion.md)
- research brainstorm-20261022-grounding-a: Ground truth for the whole batch, from the repo.
- research brainstorm-20261022-catalogue: Request: "super recursive brainstorm and improve foreman, way more skills/playbooks/way better more capable code, config in the t…
- decision 2026-10-20: T-1300 slate: round 1 = C1 renderer, C2 motion engine, C3 live track, C4 gradients/contrast/focal line, C5 event flashes, C7 odometer/sparklines, C2…
## Why not caught
new capability
## Lessons
- A lint's fixtures should include the real-world forms of each tell (Tailwind classes, CSS-in-JS, SCSS) or it only catches the fixture's form.
## Plan gaps
- failed first: step 1 failing tests: a fixture pair per rule
## Files touched
- plugin/tests/fixtures/design/generic-font/slop.css
- plugin/tests/fixtures/design/generic-font/crafted.css
- plugin/tests/fixtures/design/purple-blue-gradient/slop.css
- plugin/tests/fixtures/design/purple-blue-gradient/crafted.css
- plugin/tests/fixtures/design/purple-blue-gradient/slop-tailwind.jsx
- plugin/tests/fixtures/design/purple-blue-gradient/crafted-tailwind.jsx
- plugin/tests/fixtures/design/one-radius/slop.css
- plugin/tests/fixtures/design/one-radius/crafted.css
- plugin/tests/fixtures/design/same-shadow/slop.css
- plugin/tests/fixtures/design/same-shadow/crafted.css
- plugin/tests/fixtures/design/img-alt/slop.html
- plugin/tests/fixtures/design/img-alt/crafted.html
- plugin/tests/fixtures/design/img-alt/slop.jsx
- plugin/tests/fixtures/design/img-alt/crafted.jsx
- plugin/tests/fixtures/design/reduced-motion/slop.css
- plugin/tests/fixtures/design/reduced-motion/crafted.css
- plugin/tests/fixtures/design/layout-animation/slop.css
- plugin/tests/fixtures/design/layout-animation/crafted.css
- plugin/tests/fixtures/design/flash/slop.css
- plugin/tests/fixtures/design/flash/crafted.css
- plugin/tests/fixtures/design/unseeded-random/slop.jsx
- plugin/tests/fixtures/design/unseeded-random/crafted.jsx
- plugin/tests/fixtures/design/untokened-duration/slop.css
- plugin/tests/fixtures/design/untokened-duration/crafted.css
- plugin/tests/test_design_lint.py
- plugin/lib/fmdesign.py
- plugin/lib/fmcli.py
- MASTER.md
- plugin/tests/fixtures/design/generic-font/crafted-fontface.css
- plugin/tests/fixtures/design/generic-font/slop-next.tsx
