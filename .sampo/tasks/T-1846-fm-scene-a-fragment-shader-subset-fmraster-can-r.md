---
id: T-1846
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmshade.py, plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_shade.py, MASTER.md, CHANGELOG.md, plugin/skills/playbooks/references/ui/scene-3d.md]
depends_on: []
source: discovered
created: 2026-10-28T17:20:59Z
updated: 2026-10-28T19:36:23Z
base: 95c36696aa8097ecb2bf791c2ebdbaf36775201f
base_tree: 3fe8e2d3523597af6c17a10e6de74a8d864593b0
plan0_at: 2026-10-28T18:56:22Z
plan0_scope: [plugin/lib/fmshade.py, plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_shade.py, MASTER.md, CHANGELOG.md, plugin/skills/playbooks/references/ui/scene-3d.md]
verified: strong
---
# Fm scene: a fragment-shader subset fmraster can run per pixel (uniforms, a few built-ins),
## Raw request
> fm scene: a fragment-shader subset fmraster can run per pixel (uniforms, a few built-ins), so a shader card previews offline (from T-1635)
## Interpretation
fm scene shade FILE renders a shader card (its glsl block) or a .frag/.glsl file on the CPU to a PNG: the GLSL ES subset the 8 shader cards use, plus Shadertoy's mainImage/iTime/iResolution. Unset uniforms take preview defaults; --set overrides. Anything outside the subset is refused naming its line.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm scene shade runs the GLSL subset per pixel to a PNG (uv gradient, iTime, swizzles, built-ins match hand-computed pixels) and refuses what's outside it naming the line — verify with `python3 plugin/tests/run.py test_shade`
## Non-goals
## Approach (options → choice → why)
Options: (a) tree-walking closures in fmraster; (b) compile the GLSL to Python source from a parsed, typed AST: every name gets a prefix, every literal is re-parsed, exec with no builtins (nothing from the source runs as Python); (c) numpy (a new dependency). Choice: (b) in a new fmshade.py: as safe as (a), 3-5x faster, Python locals for GLSL locals. fmraster stays integer-only. Static types drive uint wrapping, integer division and mat*vec. Derivatives: a second pass reads each 2x2 quad partner's recorded argument, as a GPU does. Rejected: (c), (a) (too slow for 8 cards per test run).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Shade tests, red
2. [x] fmraster.shade interpreter, fm scene shade, docs, green
## Resume here
<!-- auto -->
- 2026-10-28T19:30:51Z steps 2/2 done
- git: foreman/build; 7 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmscene.py, plugin/skills/playbooks/references/ui/scene-3d.md, plugin/lib/fmshade.py, plugin/tests/test_shade.py
- touched since last checkpoint: plugin/lib/fmcli.py, CHANGELOG.md, MASTER.md, plugin/skills/playbooks/references/ui/scene-3d.md, plugin/tests/test_shade.py, plugin/lib/fmscene.py, plugin/lib/fmshade.py
- failures met: assertionerror: lists differ: ['fmshade'] != []; 0.0
## Docs impact
~/.claude/foreman/plugin/skills/playbooks/references/ui/scene-3d.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_shade` → red as expected (exit 1) · Ran 9 tests in 0.4s (1 classes, 16 at a time; slowest: Shade 0s) / FAILED (1 classes) [ran] [tree 3b4496651ace] (2026-10-28T18:57:49Z)
- (ac 1) `python3 plugin/tests/run.py test_shade 2>&1 | tail -40` → ✗ exit 1 · FAILED (1 classes) / ✗ exit 1 (0.6 s; last 24 of 24 lines) [ran] [tree 68d8b4ff9658] (2026-10-28T19:14:49Z)
- (step 2) `python3 plugin/tests/run.py test_shade` → exit 0 · Ran 9 tests in 0.8s (1 classes, 16 at a time; slowest: Shade 1s) / OK [ran] [tree db08825f9500] (2026-10-28T19:16:27Z)
- (step 2) `python3 plugin/tests/run.py test_shade` → exit 0 · Ran 11 tests in 0.9s (1 classes, 16 at a time; slowest: Shade 1s) / OK [ran] [tree 3850bbd51f67] (2026-10-28T19:26:24Z)
- (ac 1) `python3 plugin/tests/run.py test_shade` → exit 0 · Ran 11 tests in 0.9s (1 classes, 16 at a time; slowest: Shade 1s) / OK [ran] [tree ca02aa8e415e] (2026-10-28T19:35:57Z)
- (audit intent) `one fm-reviewer pass over five lenses; 9 findings all fixed test-first (test_shade 11/11); fm check exit 0, 3992 tests; pre-audit 'secret-looking' is the tokenizer's TOKEN = [REDACTED] line, a false positive` → AC met: fm scene shade runs a GLSL ES subset per pixel to a PNG; tests cover uv gradient, iTime, swizzles, built-ins, uint wrap, quad derivatives, every shader card, line-named refusals [tree ca02aa8e415e] (2026-10-28T19:35:57Z)
- (audit adversary) `one fm-reviewer pass over five lenses; 9 findings all fixed test-first (test_shade 11/11); fm check exit 0, 3992 tests; pre-audit 'secret-looking' is the tokenizer's TOKEN = [REDACTED] line, a false positive` → source text never reaches the generated code as code; no exec escape; per-pixel 100000 and per-render 100M step budgets, 64 derivatives a pixel [tree ca02aa8e415e] (2026-10-28T19:35:57Z)
- (audit edge) `one fm-reviewer pass over five lenses; 9 findings all fixed test-first (test_shade 11/11); fm check exit 0, 3992 tests; pre-audit 'secret-looking' is the tokenizer's TOKEN = [REDACTED] line, a false positive` → --out naming FILE refused, odd-size derivatives exact, deep nesting and const divide-by-zero become named errors, unterminated comment names its line [tree ca02aa8e415e] (2026-10-28T19:35:57Z)
- (audit operator) `one fm-reviewer pass over five lenses; 9 findings all fixed test-first (test_shade 11/11); fm check exit 0, 3992 tests; pre-audit 'secret-looking' is the tokenizer's TOKEN = [REDACTED] line, a false positive` → a runaway loop stops in ~16 s; the busiest card at 512x512 renders in ~20 s; default 160x100 [tree ca02aa8e415e] (2026-10-28T19:35:57Z)
- (audit maintainer) `one fm-reviewer pass over five lenses; 9 findings all fixed test-first (test_shade 11/11); fm check exit 0, 3992 tests; pre-audit 'secret-looking' is the tokenizer's TOKEN = [REDACTED] line, a false positive` → one module, tests per fix, MASTER bullet per module, playbook line within its ratchet [tree ca02aa8e415e] (2026-10-28T19:35:57Z)
## Log
- 2026-10-28T17:20:59Z created
- 2026-10-28T18:38:42Z set type=FEATURE, tier=M, scope=['plugin/lib/fmraster.py', 'plugin/lib/fmscene.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_scene.py', 'MASTER.md', 'CHANGELOG.md', 'plugin/skills/playbooks/references/ui/scene-3d.md']
- 2026-10-28T18:56:21Z set scope=['plugin/lib/fmshade.py', 'plugin/lib/fmscene.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_shade.py', 'MASTER.md', 'CHANGELOG.md', 'plugin/skills/playbooks/references/ui/scene-3d.md']
- 2026-10-28T18:56:22Z focused
- 2026-10-28T18:57:42Z criterion 1 verify: `python3 plugin/tests/run.py Shade` → `python3 plugin/tests/run.py test_shade`
- 2026-10-28T19:15:45Z hypothesis: interpreter is correct (8/9 green); only failure is argparse missing 'shade' — wiring rules it in/out
- 2026-10-28T19:24:08Z review fixes: red = test_shade hangs (timeout 124) on precision without ';' — hostile-input + odd-size derivative + --out==FILE tests added
- 2026-10-28T19:36:21Z done
- 2026-10-28T19:36:23Z committed 791bf449 (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1635 [FEATURE M, done, 3 steps] Scene.json to terminal cells through the rasteriser, a shader subset, import from three.js — lesson: A renderer's frame helper shared b…
- T-1851 [FEATURE M, done, 2 steps] 3D showpiece: terrain, a heightfield of churn or cost over time (from T-1655) — lesson: A collision fallback name needs its own loop: o…
- T-1849 [FEATURE M, done, 2 steps] 3D showpiece: the guard airlock, a scene of what the guard let through and held (from T-16 — lesson: A playbook trim can delete text a …
- decision 2026-10-22: T-1585: the guard refuses commands that name CLAUDECODE or CLAUDE_CODE_ENTRYPOINT to unset or override them, not a whole fresh environment (env -i, …
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_scene.py
## Preflight
Changed in scope since this was planned (2026-10-28): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmscene.py, plugin/skills/playbooks/references/ui/scene-3d.md; re-ground the plan against them before editing
## Lessons
- a custom error that subclasses ValueError is swallowed by a broad except ValueError: re-raise it first
## Files touched
- plugin/tests/test_shade.py
- plugin/lib/fmshade.py
- plugin/lib/fmscene.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/playbooks/references/ui/scene-3d.md
