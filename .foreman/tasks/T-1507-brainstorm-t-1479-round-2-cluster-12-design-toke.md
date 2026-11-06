---
id: T-1507
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmdesign.py, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/skills/design-extract/SKILL.md, plugin/tests/test_design_tokens.py, plugin/tests/test_design_lint.py, plugin/tests/test_hooks.py, plugin/tests/test_docs.py, plugin/tests/fixtures/design-tokens, plugin/skills/playbooks/references/ui/type-and-colour.md, plugin/skills/playbooks/references/ui/design-direction.md, plugin/skills/playbooks/ratchet.json, plugin/skills/directions/SKILL.md, MASTER.md, plugin/README.md, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:40Z
updated: 2026-10-22T21:15:27Z
base: 04ed2eca2774ab642b9aed981d74ca70a63a1cef
base_tree: f7518f8bde5b421cb9a5ae7e1f2a925af9380cbe
plan0_at: 2026-10-22T20:04:38Z
plan0_scope: [plugin/lib/fmdesign.py, plugin/lib/fmcli.py, plugin/skills/design-extract/SKILL.md, plugin/tests/test_design_tokens.py, plugin/skills/playbooks/references/ui/type-and-colour.md, CHANGELOG.md]
verified: strong
---
# Brainstorm T-1479 round 2 (cluster 12): design tokens: a design-extract skill that derives
## Raw request
> Brainstorm T-1479 round 2 (cluster 12): design tokens: a design-extract skill that derives DESIGN.md from a repo's CSS custom properties, and a stdlib script that makes a light/dark pair from one OKLCH seed with contrast proofs and exports DTCG, CSS variables or Tailwind
## Interpretation
Design tokens for any project: a design-extract skill that reads a repo's CSS custom properties (and Tailwind config when present) into a DESIGN.md token table, and fm design palette SEED that makes a light/dark OKLCH palette from one seed colour with contrast proofs (the type-and-colour playbook's script, now an fm verb) and exports DTCG JSON, CSS variables or a Tailwind theme. Works from Claude Code (an fm verb or /foreman: command) as well as fm code.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm design palette makes a light/dark pair from a seed whose body text meets 4.5:1 (7:1 dark) and exports DTCG, CSS and Tailwind — verify with `cd plugin/tests && python3 -m unittest test_design_tokens.Palette`
- [x] fm design extract writes a DESIGN.md token table from a fixture's :root custom properties; fm design contrast checks a token file's pairs — verify with `cd plugin/tests && python3 -m unittest test_design_tokens.Extract`
## Non-goals
## Approach (options → choice → why)
Options: a JS colour library (a dependency); chosen: stdlib OKLCH maths (already in ui/type-and-colour.md's proof script) moved into plugin/lib/fmdesign.py beside the lint; extract reads :root custom properties with a small tokenizer.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] palette, contrast and export in fmdesign.py
3. [x] extract and the design-extract skill
4. [x] review fixes: linear _props, strict DESIGN.md writes, nested dark media, ## Direction means a direction, lint string braces
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_design_tokens` → ✗ exit 1 · Ran 25 tests in 2.0s (3 classes, 16 at a time; slowest: Extract 2s, Palette 1s, ScratchNames 0s) / FAILED (2 classes) [ran] [tree e5fc2f6a5668] (2026-10-22T20:12:31Z)
- (step 2) `python3 plugin/tests/run.py test_design_tokens.Palette` → exit 0 · Ran 11 tests in 1.2s (1 classes, 16 at a time; slowest: Palette 1s) / OK [ran] [tree 41804d9b74fb] (2026-10-22T20:17:45Z)
- (step 3) `python3 plugin/tests/run.py test_design_tokens 2>&1 | grep -E "^(FAIL|ERROR):|Error|assert|^Ran|OK|FAILED" | head -30` → exit 0 · Ran 26 tests in 1.6s (3 classes, 16 at a time; slowest: Extract 1s, Palette 1s, ScratchNames 0s) / OK [ran] [tree 3b26f0bf9a5e] (2026-10-22T20:19:31Z)
- (step 3) `python3 plugin/tests/run.py test_design_tokens.Extract test_design_lint test_docs` → exit 0 · Ran 92 tests in 1.8s (16 classes, 16 at a time; slowest: Extract 2s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 6f32ab8f4115] (2026-10-22T20:20:44Z)
- (step 3) `python3 plugin/tests/run.py test_design_tokens test_design_lint test_docs test_library test_playbook_check` → exit 0 · Ran 176 tests in 7.0s (35 classes, 16 at a time; slowest: LibSources 7s, Extract 3s, Snippets 2s) / OK [ran] [tree 9ed901a5feaa] (2026-10-22T20:24:57Z)
- (step 4) `python3 plugin/tests/run.py test_design_lint test_docs test_hooks.DesignNudge` → ✗ exit 1 · Ran 82 tests in 3.2s (16 classes, 16 at a time; slowest: DesignNudge 3s, TaskLifecycle 1s, Allow 1s) / FAILED (2 classes) [ran] [tree f577c3762008] (2026-10-22T20:40:00Z)
- (step 4) `python3 plugin/tests/run.py test_design_lint test_design_tokens test_docs test_hooks test_library test_playbook_check` → exit 0 · Ran 379 tests in 44.0s (58 classes, 16 at a time; slowest: Stop 44s, NoTaskGate 33s, PreToolUse 26s) / OK [ran] [tree 32ad0e1f3fab] (2026-10-22T20:44:35Z)
- (step 1) `python3 plugin/tests/run.py test_design_lint test_design_tokens test_docs test_hooks` → exit 0 · Ran 321 tests in 71.1s (44 classes, 16 at a time; slowest: Stop 71s, NoTaskGate 59s, PreToolUse 54s) / OK [ran] [tree 007a4e7f2078] (2026-10-22T21:12:21Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_design_tokens.Palette` → exit 0 · Ran 12 tests in 0.955s / OK [ran] [tree 007a4e7f2078] (2026-10-22T21:12:22Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_design_tokens.Extract` → exit 0 · Ran 21 tests in 2.869s / OK [ran] [tree 007a4e7f2078] (2026-10-22T21:12:26Z)
- (audit adversary) `fm-reviewer adversary pass (research/T-1507-review.md)` → quadratic _props on deep nesting fixed (linear, hostile 80k-deep test under 5 s); DESIGN.md writes: non-UTF-8 refused unchanged, CRLF kept, symlinks written through, one lock; lint string braces no longer end blocks early [tree 007a4e7f2078] (2026-10-22T21:12:33Z)
- (audit edge) `review edge lens` → nested dark @media and &.dark read as dark; !important stripped; a root selector must be the whole selector; skipped files reported; outside sources shown as …/folder/file [tree 007a4e7f2078] (2026-10-22T21:12:33Z)
- (audit operator) `fm design palette/extract/contrast via tests after the merge` → 321 tests across lint, tokens, docs, hooks green; palette margin floor+0.03 over 3,005 seeds [tree 007a4e7f2078] (2026-10-22T21:12:34Z)
- (audit maintainer) `review maintainer lens` → Python 3.11+ stated for standalone contrast; design-extract in SKILLS/USER_ONLY; ratchet recorded; fmcodetui.contrast duplicates fmdesign.contrast (noted) [tree 007a4e7f2078] (2026-10-22T21:12:34Z)
- (audit intent) `both criteria: palette pair meeting 4.5:1/7:1 with DTCG/CSS/Tailwind export; extract to a DESIGN.md token table and contrast over a token file` → met: Palette (12) and Extract (21) green after the merge [tree 007a4e7f2078] (2026-10-22T21:12:34Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_design_tokens.Palette` → exit 0 · Ran 12 tests in 0.948s / OK [ran] [tree 007a4e7f2078] (2026-10-22T21:12:44Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_design_tokens.Extract` → exit 0 · Ran 21 tests in 2.870s / OK [ran] [tree 007a4e7f2078] (2026-10-22T21:12:44Z)
- (audit adversary) `one fm-reviewer five-lens pass; 10 findings fixed test-first by the builder; both criteria green after the merge` → linear token parsing under hostile nesting; strict DESIGN.md writes under one lock [tree 007a4e7f2078] (2026-10-22T21:12:44Z)
- (audit edge) `one fm-reviewer five-lens pass; 10 findings fixed test-first by the builder; both criteria green after the merge` → nested dark blocks, !important, whole-selector roots, string braces in the lint [tree 007a4e7f2078] (2026-10-22T21:12:44Z)
- (audit adversary) `one fm-reviewer five-lens pass; 10 findings fixed test-first by the builder; both criteria green after the merge` → linear token parsing under hostile nesting; strict DESIGN.md writes under one lock [tree 007a4e7f2078] (2026-10-22T21:13:52Z)
- (audit edge) `one fm-reviewer five-lens pass; 10 findings fixed test-first by the builder; both criteria green after the merge` → nested dark blocks, !important, whole-selector roots, string braces in the lint [tree 007a4e7f2078] (2026-10-22T21:13:52Z)
## Log
- 2026-10-22T17:36:40Z created
- 2026-10-22T17:50:22Z steer: T-1489's contrast-proof script (in ui/type-and-colour.md) becomes an fm verb or a design-lint rule here, so Claude Code can run it
- 2026-10-22T17:55:36Z set scope=['plugin/lib/fmdesign.py', 'plugin/lib/fmcli.py', 'plugin/skills/design-extract/SKILL.md', 'plugin/tests/test_design_tokens.py', 'plugin/skills/playbooks/references/ui/type-and-colour.md', 'CHANGELOG.md']
- 2026-10-22T20:04:20Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1507.builder.md
- 2026-10-22T20:04:36Z focused
- 2026-10-22T20:11:26Z set scope=['plugin/lib/fmdesign.py', 'plugin/lib/fmcli.py', 'plugin/skills/design-extract/SKILL.md', 'plugin/tests/test_design_tokens.py', 'plugin/tests/fixtures/design-tokens', 'plugin/skills/playbooks/references/ui/type-and-colour.md', 'plugin/skills/playbooks/references/ui/design-direction.md', 'plugin/skills/directions/SKILL.md', 'MASTER.md', 'plugin/README.md', 'CHANGELOG.md']
- 2026-10-22T20:11:29Z scope: + fixtures/design-tokens (extract fixture), design-direction.md (Tokens section in the DESIGN.md template), directions/SKILL.md (points at fm design extract), MASTER.md and plugin/README.md (verb and skill docs)
- 2026-10-22T20:31:24Z set scope=['plugin/lib/fmdesign.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmhooks.py', 'plugin/skills/design-extract/SKILL.md', 'plugin/tests/test_design_tokens.py', 'plugin/tests/test_design_lint.py', 'plugin/tests/test_hooks.py', 'plugin/tests/test_docs.py', 'plugin/tests/fixtures/design-tokens', 'plugin/skills/playbooks/references/ui/type-and-colour.md', 'plugin/skills/playbooks/references/ui/design-direction.md', 'plugin/skills/playbooks/ratchet.json', 'plugin/skills/directions/SKILL.md', 'MASTER.md', 'plugin/README.md', 'CHANGELOG.md']
- 2026-10-22T20:31:25Z review fixes: scope + fmhooks._design_note and test_hooks (## Direction means a direction), test_docs (SKILLS), test_design_lint (string-brace hostile test), ratchet.json
- 2026-10-22T21:10:50Z merged worktree-agent-ab2317ff153244c8d (17 file(s))
- 2026-10-22T21:10:54Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab2317ff153244c8d
- 2026-10-22T21:10:55Z focused
- 2026-10-22T21:13:51Z scope: README.md, plugin/commands/settings.md, plugin/lib/fmbus.py, fmcode.py, fmcodetui.py, fmdemo.py, fmlib.py, fmnew.py came from other tasks' merges (T-1519, T-1543) brought into this lane by its foreman/build merge, not T-1507 edits
- 2026-10-22T21:15:25Z done
- 2026-10-22T21:15:27Z committed a46cdf36 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook UI playbooks (skills/playbooks/references/ui/INDEX.md)
- T-1489 [FEATURE M, done, 2 steps] UI playbook: type and colour — lesson: Embedded scripts in a playbook should be run by the writer against the playbook's own example; i…
- research brainstorm-20261022-grounding-b: ids: b032, b034, b035, b036, b037, b038, b072, b073, b074, b075, b077, b121, b162, b177 [stale: plugin/lib/fmcli.py changed sin…
- decision 2026-10-20: T-1300 slate: round 1 = C1 renderer, C2 motion engine, C3 live track, C4 gradients/contrast/focal line, C5 event flashes, C7 odometer/sparklines, C2…
- the similar finished task took 2 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/README.md, plugin/lib/fmcli.py, plugin/lib/fmdesign.py, plugin/lib/fmhooks.py, plugin/skills/design-extract/SKILL.md, plugin/skills/directions/SKILL.md, plugin/skills/…; re-ground the plan against them before editing
## Why not caught
fixtures were shallow; the review tried 80k-deep nesting
## Lessons
- A parser that re-scans the parent for each nested block is quadratic; carry the parent's flags down instead
## Plan gaps
- added late: review fixes: linear _props, strict DESIGN.md writes, nested dark media, ## Direction means a direction, lint string br…
- failed first: step 1 failing tests
- failed first: step 4 review fixes: linear _props, strict DESIGN.md writes, nested dark media, ## Direction means a direc…
## Files touched
- plugin/tests/fixtures/design-tokens/ui/tokens.css
- plugin/tests/fixtures/design-tokens/ui/card.css
- plugin/tests/fixtures/design-tokens/ui/tailwind.config.js
- plugin/tests/test_design_tokens.py
- plugin/lib/fmdesign.py
- plugin/lib/fmcli.py
- plugin/skills/design-extract/SKILL.md
- plugin/skills/playbooks/references/ui/type-and-colour.md
- plugin/skills/directions/SKILL.md
- plugin/skills/playbooks/references/ui/design-direction.md
- MASTER.md
- plugin/README.md
- plugin/tests/test_docs.py
- plugin/tests/test_hooks.py
- plugin/tests/test_design_lint.py
- plugin/lib/fmhooks.py
- plugin/skills/playbooks/ratchet.json
- CHANGELOG.md
- README.md
- plugin/commands/settings.md
- plugin/lib/fmbus.py
- plugin/lib/fmcode.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmdemo.py
- plugin/lib/fmlib.py
- plugin/lib/fmnew.py
- plugin/lib/fmoracle.py
- plugin/lib/fmplaybooks.py
- plugin/lib/fmrecall.py
- plugin/lib/fmreplay.py
