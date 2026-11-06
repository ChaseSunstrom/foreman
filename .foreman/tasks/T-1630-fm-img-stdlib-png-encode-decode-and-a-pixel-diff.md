---
id: T-1630
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmimg.py, plugin/lib/fmcli.py, plugin/tests/test_raster.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-22T20:57:23Z
updated: 2026-10-22T21:51:48Z
base: 1220d50d956dca2c2fc9daee4eb773dc8def49d8
base_tree: 56f0657398f97d796e1cde017ae18b3a092dbb56
plan0_at: 2026-10-22T21:30:46Z
plan0_scope: [plugin/lib/fmimg.py, plugin/lib/fmcli.py, plugin/tests/test_raster.py, CHANGELOG.md]
verified: strong
---
# fm img: stdlib PNG encode/decode and a pixel diff with a changed-pixel count
## Raw request
> fm img: stdlib PNG encode/decode and a pixel diff with a changed-pixel count
## Interpretation
plugin/lib/fmimg.py is a stdlib PNG codec: decode 8-bit grey, RGB, RGBA and palette images with all five filters; encode RGB or RGBA with filter 0; zlib only. diff(a, b) returns the changed-pixel count and bounding box. fm img info PATH prints the size and mode; fm img diff A B [--out PATH] [--json] prints counts and can write a diff image. It's the base for fm shot --diff (T-1637) and the rasteriser (T-1631). An fm verb, so it works from Claude Code.
## Assumptions (confidence)
## Acceptance criteria
- [x] a PNG round trip keeps the pixels and a diff of two images reports the changed count — verify with `python3 plugin/tests/run.py test_raster.Img`
## Non-goals
## Approach (options → choice → why)
Options: Pillow (optional, often missing); shelling out to ImageMagick (external, varies by machine); a stdlib zlib+struct codec. Choice: stdlib: deterministic and always there; Pillow is never required. Interlaced (Adam7) and 16-bit images are refused with a clear error (ponytail: add when a real screenshot needs them). Inputs are capped (dimensions and decompressed size checked before inflating) so a crafted PNG can't exhaust memory.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test with a 4x4 image
2. [x] encode/decode with zlib, filters 0-4
3. [x] fm img diff verb
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_raster.Img` → ✗ exit 1 · run.py: no test matches test_raster.Img [ran] [tree dfbcf98089fc] (2026-10-22T21:34:20Z)
- (ac 1) `python3 plugin/tests/run.py test_raster.Img 2>&1 | tail -40` → exit 0 · Ran 8 tests in 1.0s (1 classes, 16 at a time; slowest: Img 1s) / OK [ran] [tree 3e772ccd5496] (2026-10-22T21:36:03Z)
- (step 2) `python3 plugin/tests/run.py -k test_raster.Img.test_round_trip -k test_raster.Img.test_every_filter -k test_raster.Img.test_grey -k test_raster.Img.test_refuses -k test_raster.Img.test_inflate -k test_raster.Img.test_pillow` → exit 0 · Ran 6 tests in 0.4s (1 classes, 16 at a time; slowest: Img 0s) / OK [ran] [tree 925bddb3815d] (2026-10-22T21:36:54Z)
- (step 3) `python3 plugin/tests/run.py -k test_raster.Img.test_diff -k test_raster.Img.test_fm_img -k test_help` → exit 0 · Ran 8 tests in 0.9s (4 classes, 16 at a time; slowest: Help 1s, PromptApprovals 1s, Img 1s) / OK [ran] [tree 925bddb3815d] (2026-10-22T21:36:55Z)
- (ac 1) `python3 plugin/tests/run.py test_raster.Img 2>&1 | tail -20` → exit 0 · Ran 8 tests in 1.1s (1 classes, 16 at a time; slowest: Img 1s) / OK [ran] [tree 4222d79b15b7] (2026-10-22T21:37:28Z)
- (ac 1) `python3 plugin/tests/run.py test_raster.Img` → exit 0 · Ran 8 tests in 1.2s (1 classes, 16 at a time; slowest: Img 1s) / OK [ran] [tree e04e45c7a7a6] (2026-10-22T21:39:31Z)
- (ac 1) `python3 plugin/tests/run.py test_raster.Img` → exit 0 · Ran 12 tests in 1.6s (1 classes, 16 at a time; slowest: Img 1s) / OK [ran] [tree f5ca22964706] (2026-10-22T21:46:48Z)
- (ac 1) `python3 plugin/tests/run.py test_raster.Img` → exit 0 · Ran 12 tests in 2.6s (1 classes, 16 at a time; slowest: Img 2s) / OK [ran] [tree f9a8d9db66a4] (2026-10-22T21:50:44Z)
- (step 3) `python3 plugin/tests/run.py test_raster test_worker_reads test_help` → exit 0 · Ran 20 tests in 4.5s (5 classes, 16 at a time; slowest: WorkerOnlyReads 4s, Img 3s, Help 2s) / OK [ran] [tree f9a8d9db66a4] (2026-10-22T21:50:49Z)
- (audit adversary) `chunk names printed safely; size checked before inflate and inflate capped (tracemalloc test fails without the cap); FIFO opened non-blocking; palette index past PLTE refused` → fixed with tests [tree f9a8d9db66a4] (2026-10-22T21:50:50Z)
- (audit edge) `zero size, w*h over the cap, IDAT split across chunks, 16-bit palette message, size-mismatch diff` → tested [tree f9a8d9db66a4] (2026-10-22T21:50:51Z)
- (audit operator) `fm img info and diff; exit 0 same, 1 differ, 2 error; --out 0600 via temp file and rename, never over an input` → tested; workers may run info and diff, not --out [tree f9a8d9db66a4] (2026-10-22T21:50:52Z)
- (audit maintainer) `one walk for count and image; crc32 chaining; docstring states worst case at the caps` → clean [tree f9a8d9db66a4] (2026-10-22T21:50:52Z)
- (audit intent) `criterion: a PNG round trip keeps pixels and a diff reports the changed count` → met (12 tests); diff gains tol and alpha-0 equality for T-1637 [tree f9a8d9db66a4] (2026-10-22T21:50:53Z)
- (ac 1) `python3 plugin/tests/run.py test_raster.Img` → exit 0 · Ran 12 tests in 2.7s (1 classes, 16 at a time; slowest: Img 2s) / OK [ran] [tree f9a8d9db66a4] (2026-10-22T21:51:03Z)
- (audit adversary) `one fm-reviewer five-lens pass; all findings fixed test-first; criterion green after the merge` → hostile PNGs bounded and refused safely [tree f9a8d9db66a4] (2026-10-22T21:51:03Z)
- (audit edge) `one fm-reviewer five-lens pass; all findings fixed test-first; criterion green after the merge` → degenerate sizes and split IDAT tested [tree f9a8d9db66a4] (2026-10-22T21:51:03Z)
- (audit intent) `one fm-reviewer five-lens pass; all findings fixed test-first; criterion green after the merge` → met (12 tests) [tree f9a8d9db66a4] (2026-10-22T21:51:03Z)
## Log
- 2026-10-22T20:57:23Z created
- 2026-10-22T20:57:24Z set scope=['plugin/lib/fmimg.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_raster.py', 'CHANGELOG.md']
- 2026-10-22T20:57:25Z split from T-1529 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:29:52Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_raster.Img`
- 2026-10-22T21:30:15Z criterion 1 text: a PNG round trip keeps the pixels and a diff of two images reports the changed count — verify with python3 plugin/tests/run.py test_raster.Img → a PNG round trip keeps the pixels and a diff of two images reports the changed count
- 2026-10-22T21:30:32Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1630.builder.md
- 2026-10-22T21:30:46Z focused
- 2026-10-22T21:37:41Z scope: MASTER.md, one short fmimg entry in the lib list, as the main thread asked
- 2026-10-22T21:50:29Z merged worktree-agent-a05f6b0f7a94b2ac8 (5 file(s))
- 2026-10-22T21:50:29Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a05f6b0f7a94b2ac8
- 2026-10-22T21:50:31Z focused
- 2026-10-22T21:50:53Z scope: MASTER.md got one fmimg entry in the plugin/lib row (self-docs); fmcli WORKER_SUBREADS gained img
- 2026-10-22T21:51:48Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1529 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Stdlib pixels: a software 3D rasteriser for deterministic frames (intege
- playbook Visual QA: screenshots, an eyeball pass and a receipt (skills/playbooks/references/ui/visual-qa.md)
- T-1637 [FEATURE M, planned, 3 steps] fm shot --diff: a fallback font fails; a pixel diff under the baseline's noise floor passes
- decision 2026-10-20: Foreman Code's TUI (T-1283) is a stdlib curses client of fm code's --json event stream with a widget layer that themes and extensions build on; exte…
- likely tests for the scope: plugin/tests/test_cli.py
## Why not caught
the first bomb test checked pixels, which a capped and an uncapped decode both produced
## Lessons
- A bomb test must fail without the cap it protects: measure memory, not just the output, when later code reads only part of what was inflated
## Plan gaps
- failed first: step 1 failing test with a 4x4 image
## Files touched
- plugin/tests/test_raster.py
- plugin/lib/fmimg.py
- plugin/lib/fmcli.py
- MASTER.md
- CHANGELOG.md
