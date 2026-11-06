---
id: T-1646
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmdesign.py, plugin/tests/test_design_gates.py, CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/skills/ui-design/SKILL.md]
depends_on: [T-1645]
source: user
created: 2026-10-22T20:58:14Z
updated: 2026-10-23T03:03:41Z
base: 88f60b15e65e2f10b14a9e1422e4253d63ee41b0
base_tree: 3924ad7e39282299d28656a2cdb12334bd60b057
plan0_at: 2026-10-23T02:21:43Z
plan0_scope: [plugin/lib/fmdesign.py, plugin/tests/test_design_gates.py, CHANGELOG.md]
verified: strong
---
# Design gates: an accessibility and motion audit gate and a design-debt sweep
## Raw request
> Design gates: an accessibility and motion audit gate and a design-debt sweep
## Interpretation
A second design gate: an accessibility and motion audit (contrast pairs through fmdesign.contrast, a reduced-motion path for every animation, focus styles present) and a design-debt sweep counting untokened literals per file, both reusing the lint rules' output.
## Assumptions (confidence)
## Acceptance criteria
- [x] the audit flags a missing reduced-motion path and the sweep counts untokened literals — verify with `python3 plugin/tests/run.py test_design_gates.Audit`
## Non-goals
## Approach (options → choice → why)
Options: axe-core in a browser (optional dependency, heavier); static checks over the lint engine; both. Choice: static checks first, axe when the browser exists later.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] reuse lint rule output
3. [x] sweep totals
## Resume here
## Docs impact
plugin/skills/ui-design/SKILL.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_design_gates.Audit 2>&1 | tail -15` → ✗ exit 1 · Ran 4 tests in 1.4s (1 classes, 16 at a time; slowest: Audit 0s) / FAILED (1 classes) [ran] [tree 558c20fa01e8] (2026-10-23T02:23:35Z)
- (step 1) `python3 plugin/tests/run.py test_design_gates.Audit` → ✗ exit 1 · Ran 4 tests in 0.4s (1 classes, 16 at a time; slowest: Audit 0s) / FAILED (1 classes) [ran] [tree 558c20fa01e8] (2026-10-23T02:23:38Z)
- (step 2) `python3 plugin/tests/run.py test_design_gates.Audit test_design_lint` → exit 0 · Ran 33 tests in 2.6s (4 classes, 16 at a time; slowest: Allow 2s, Rules 2s, Audit 1s) / OK [ran] [tree 5b496b7f955f] (2026-10-23T02:26:50Z)
- (step 3) `python3 plugin/tests/run.py test_design_gates test_design_tokens test_motion_verify` → exit 0 · Ran 56 tests in 7.3s (7 classes, 16 at a time; slowest: Extract 7s, Sample 3s, Palette 3s) / OK [ran] [tree 5b496b7f955f] (2026-10-23T02:26:59Z)
- (ac 1) `python3 plugin/tests/run.py test_design_gates.Audit 2>&1 | grep -E "^(FAIL|ERROR|AssertionError)|Error:" | head -20` → ✗ exit 1 · FAILED (failures=2, errors=1) / FAILED (1 classes) [ran] [tree 77c6a0453fe0] (2026-10-23T02:41:01Z)
- (step 1) `python3 plugin/tests/run.py test_design_gates.Audit` → ✗ exit 1 · Ran 8 tests in 0.4s (1 classes, 16 at a time; slowest: Audit 0s) / FAILED (1 classes) [ran] [tree 77c6a0453fe0] (2026-10-23T02:41:04Z)
- (step 2) `python3 plugin/tests/run.py test_design_gates test_design_lint` → exit 0 · Ran 43 tests in 2.1s (5 classes, 16 at a time; slowest: Rules 2s, Brief 2s, Allow 2s) / OK [ran] [tree f3fb01a950b6] (2026-10-23T02:43:16Z)
- (step 3) `python3 plugin/tests/run.py test_design_gates.Audit test_design_tokens test_motion_verify test_docs` → exit 0 · Ran 121 tests in 11.2s (21 classes, 16 at a time; slowest: Fences 11s, Extract 7s, TaskLifecycle 4s) / OK [ran] [tree f3fb01a950b6] (2026-10-23T02:43:28Z)
- (ac 1) `python3 plugin/tests/run.py test_design_gates test_design_lint` → exit 0 · Ran 43 tests in 1.1s (5 classes, 16 at a time; slowest: Brief 1s, Allow 1s, Rules 1s) / OK [ran] [tree e51b49b4263e] (2026-10-23T03:01:45Z)
- (step 1) `python3 plugin/tests/run.py test_design_gates.Audit` → exit 0 · Ran 8 tests in 0.6s (1 classes, 16 at a time; slowest: Audit 0s) / OK [ran] [tree e51b49b4263e] (2026-10-23T03:02:01Z)
- (ac 1) `python3 plugin/tests/run.py test_design_gates.Audit` → exit 0 · Ran 8 tests in 0.6s (1 classes, 16 at a time; slowest: Audit 0s) / OK [ran] [tree e51b49b4263e] (2026-10-23T03:02:02Z)
- (audit intent) `fm-reviewer full pass; 4 MEDIUMs fixed test-first: var()-based colour functions aren't debt (shadcn CSS counts 0); interactive-element match is case-sensitive with a tag boundary (<Button>, Array<A> no longer count); focus counts only visible outline/shadow/border/background/color/decoration, not :focus-within or :not(:focus-visible); contrast reads shadcn foreground pairs and a blocking a11y gate with nothing checkable fails; LOWs: skipped files noted, one radius per declaration, @property skipped, kinds= on _literals` → fm design check's a11y gate (contrast pairs, reduced motion, flashes, img alt, visible focus) and debt gate (untokened literals per file under a budget) report like the brief gate, advisory or blocking [tree e51b49b4263e] (2026-10-23T03:02:02Z)
- (audit edge) `fm-reviewer full pass; 4 MEDIUMs fixed test-first: var()-based colour functions aren't debt (shadcn CSS counts 0); interactive-element match is case-sensitive with a tag boundary (<Button>, Array<A> no longer count); focus counts only visible outline/shadow/border/background/color/decoration, not :focus-within or :not(:focus-visible); contrast reads shadcn foreground pairs and a blocking a11y gate with nothing checkable fails; LOWs: skipped files noted, one radius per declaration, @property skipped, kinds= on _literals` → token-only CSS has zero debt; component-library tags aren't mistaken for elements; an unreadable contrast set is said, and fails when blocking [tree e51b49b4263e] (2026-10-23T03:02:02Z)
- (audit maintainer) `fm-reviewer full pass; 4 MEDIUMs fixed test-first: var()-based colour functions aren't debt (shadcn CSS counts 0); interactive-element match is case-sensitive with a tag boundary (<Button>, Array<A> no longer count); focus counts only visible outline/shadow/border/background/color/decoration, not :focus-within or :not(:focus-visible); contrast reads shadcn foreground pairs and a blocking a11y gate with nothing checkable fails; LOWs: skipped files noted, one radius per declaration, @property skipped, kinds= on _literals` → the lint and the debt count share one literal parser [tree e51b49b4263e] (2026-10-23T03:02:02Z)
- (audit operator) `fm-reviewer full pass; 4 MEDIUMs fixed test-first: var()-based colour functions aren't debt (shadcn CSS counts 0); interactive-element match is case-sensitive with a tag boundary (<Button>, Array<A> no longer count); focus counts only visible outline/shadow/border/background/color/decoration, not :focus-within or :not(:focus-visible); contrast reads shadcn foreground pairs and a blocking a11y gate with nothing checkable fails; LOWs: skipped files noted, one radius per declaration, @property skipped, kinds= on _literals` → ui-design, the fm design help and MASTER name all three gates [tree e51b49b4263e] (2026-10-23T03:02:02Z)
- (audit intent) `fm-reviewer full pass; 4 MEDIUMs fixed test-first: var()-based colour functions aren't debt (shadcn CSS counts 0); interactive-element match is case-sensitive with a tag boundary; focus counts only visible properties, not :focus-within or :not(:focus-visible); contrast reads shadcn pairs and a blocking a11y gate with nothing checkable fails; LOWs: skipped files noted, one radius per declaration, @property skipped` → fm design check's a11y gate (contrast pairs, reduced motion, flashes, img alt, visible focus) and debt gate (untokened literals per file under a budget) report like the brief gate, advisory or blocking [tree e51b49b4263e] (2026-10-23T03:02:51Z)
- (audit adversary) `fm-reviewer full pass; 4 MEDIUMs fixed test-first: var()-based colour functions aren't debt (shadcn CSS counts 0); interactive-element match is case-sensitive with a tag boundary; focus counts only visible properties, not :focus-within or :not(:focus-visible); contrast reads shadcn pairs and a blocking a11y gate with nothing checkable fails; LOWs: skipped files noted, one radius per declaration, @property skipped` → DESIGN.md and CSS are project data read with fmdesign's capped reader; the budget parses as at most 9 digits; output goes through render_gates' control/bidi cleaning; nothing is written [tree e51b49b4263e] (2026-10-23T03:02:51Z)
- (audit edge) `fm-reviewer full pass; 4 MEDIUMs fixed test-first: var()-based colour functions aren't debt (shadcn CSS counts 0); interactive-element match is case-sensitive with a tag boundary; focus counts only visible properties, not :focus-within or :not(:focus-visible); contrast reads shadcn pairs and a blocking a11y gate with nothing checkable fails; LOWs: skipped files noted, one radius per declaration, @property skipped` → token-only CSS has zero debt; component-library tags aren't mistaken for elements; an unreadable contrast set is said, and fails when blocking [tree e51b49b4263e] (2026-10-23T03:02:51Z)
- (audit maintainer) `fm-reviewer full pass; 4 MEDIUMs fixed test-first: var()-based colour functions aren't debt (shadcn CSS counts 0); interactive-element match is case-sensitive with a tag boundary; focus counts only visible properties, not :focus-within or :not(:focus-visible); contrast reads shadcn pairs and a blocking a11y gate with nothing checkable fails; LOWs: skipped files noted, one radius per declaration, @property skipped` → the lint and the debt count share one literal parser [tree e51b49b4263e] (2026-10-23T03:02:51Z)
## Log
- 2026-10-22T20:58:14Z created
- 2026-10-22T20:58:16Z set scope=['plugin/lib/fmdesign.py', 'plugin/tests/test_design_gates.py', 'CHANGELOG.md']
- 2026-10-22T20:58:18Z split from T-1535 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T20:58:19Z set depends_on=['T-1645']
- 2026-10-22T21:29:58Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_design_gates.Audit`
- 2026-10-22T21:30:21Z criterion 1 text: the audit flags a missing reduced-motion path and the sweep counts untokened literals — verify with python3 plugin/tests/run.py test_design_gates.Audit → the audit flags a missing reduced-motion path and the sweep counts untokened literals
- 2026-10-23T02:21:19Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1646.builder.md
- 2026-10-23T02:21:42Z focused
- 2026-10-23T02:27:23Z set scope=['plugin/lib/fmdesign.py', 'plugin/tests/test_design_gates.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T02:27:24Z scope: MASTER.md added, the lead asked for its design check sentence
- 2026-10-23T02:43:32Z set scope=['plugin/lib/fmdesign.py', 'plugin/tests/test_design_gates.py', 'CHANGELOG.md', 'MASTER.md', 'plugin/lib/fmcli.py', 'plugin/skills/ui-design/SKILL.md']
- 2026-10-23T02:43:33Z scope: fmcli.py design help and ui-design SKILL.md, the review asked for the gate docs
- 2026-10-23T03:01:42Z merged worktree-agent-ac02568c9c74766c7 (6 file(s))
- 2026-10-23T03:01:42Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac02568c9c74766c7
- 2026-10-23T03:01:42Z focused
- 2026-10-23T03:01:53Z scope: fmcli design help, ui-design SKILL.md and MASTER.md name the gates (review item)
- 2026-10-23T03:03:41Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1506 [FEATURE M, done, 3 steps] fm design lint: a stdlib check for generic tells and craft slips — lesson: A lint's fixtures should include the real-world forms of eac…
- T-1535 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Design gates: an executable design brief that fails the build, an access
- research T-1628-review: Verdict: approve with nits.** I read the code only and ran no tests; this session had no execution tool. The rule is cheap and its fixtures match…
- decision 2026-10-20: T-1300 slate: round 1 = C1 renderer, C2 motion engine, C3 live track, C4 gradients/contrast/focal line, C5 event flashes, C7 odometer/sparklines, C2…
- the similar finished task took 3 steps
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmdesign.py, plugin/skills/ui-design/SKILL.md, plugin/tests/test_design_gates.py; re-ground the plan against them before editing
## Lessons
- A gate that can't check something must fail when blocking, not silently pass
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_design_gates.py
- plugin/lib/fmdesign.py
- MASTER.md
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- plugin/lib/fmroll.py
- plugin/lib/fmshot.py
- plugin/skills/ui-design/SKILL.md
- plugin/tests/test_design_tokens.py
- plugin/tests/test_docs.py
- plugin/tests/test_fmshot.py
- plugin/tests/test_hooks.py
- plugin/tests/test_looks_gallery.py
- plugin/commands/settings.md
- plugin/lib/fmdoctor.py
- plugin/lib/fmflow.py
- plugin/lib/fmsettings.py
- plugin/tests/test_control_room.py
- plugin/tests/test_flow.py
