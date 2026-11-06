---
id: T-2904
type: CLEAN
tier: M
status: dropped
priority: normal
scope: [site/tools/port.py, site/tools/annotate.py, site/tools/writeif.py, site/tools/README.md, design/sampo/directions/12-forge-illustrated/**, plugin/tests/test_site_build.py]
depends_on: []
source: discovered
created: 2026-11-04T06:16:57Z
updated: 2026-11-05T02:20:07Z
base: b3ac10ff49295f54456dfa8a6c32f2b8fa9b9888
base_tree: ab0d245b6375d38111d3d00152230ace0565424a
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-11-05T02:14:26Z
plan0_scope: [site/tools/port.py, site/tools/annotate.py, site/tools/writeif.py, site/tools/README.md, design/sampo/directions/12-forge-illustrated/**, plugin/tests/test_site_build.py]
---
# Keep 12's port scripts (port.py, annotate.py) in the repo under site/tools, writing…
## Raw request
> CLEAN: keep 12's port scripts (port.py, annotate.py) in the repo under site/tools, writing tokens.json only when its content changes
## Interpretation
Reading 1 (taken): the picked design direction 12 (the illustrated forge, T-2788) and the scripts that ported it into the site live only in a session's scratch folder; keep them in the repo: the direction's source (index.html, NOTES.md, its _src generator, assets and logo SVGs; not the 1.7 GB of review renders) under design/sampo/directions/12-forge-illustrated beside emberline, orrery and runestone, and port.py and annotate.py under site/tools, writing outputs only when their content changes. port.py's helper port_css.py was lost with a builder's worktree (not in git), so the tools are kept as the record of the port with that gap stated. Reading 2 (ruled out): rebuild port_css.py: the port was one-time; the site has since moved on from its output.
## Assumptions (confidence)
## Acceptance criteria
- [ ] port.py and annotate.py live under site/tools with repo-relative paths and run from the repo root — verify with `python3 site/tools/port.py --help`
- [x] port.py writes tokens.json only when its content changes: a rerun with no change leaves the file and its mtime alone — verify with `python3 plugin/tests/run.py test_site_build`
- [x] Direction 12's source (index.html, NOTES.md, _src without caches, assets and logo SVGs) lives under design/sampo/directions/12-forge-illustrated, under 5 MB — verify with `test -f design/sampo/directions/12-forge-illustrated/index.html && test -f design/sampo/directions/12-forge-illustrated/_src/art.py && [ $(du -sm design/sampo/directions/12-forge-illustrated | cut -f1) -lt 5 ]`
## Non-goals
## Approach (options → choice → why)
1) use what exists: copy the files, a tiny write-if-changed helper in site/tools used by port.py for every output, a README saying how the port ran and what is missing: likely outcome: the direction and its port survive the session. 2) keep everything (1.8 GB): fails if: the repo carries 1.7 GB of review renders. 3) do less: the scripts only: fails if: the direction's source, which the site's look comes from, still lives only in a temp folder. Choice 1 (85%).
## Risks and rollback
Blast radius (sampo graph blast): co-changes CHANGELOG.md, site/build.py, site/index.html, site/style.css, site/genesis/index.html; past FIXes T-2060, T-2061, T-2087.
## Execution prompt
## Steps
1. [x] copy, repo-relative paths, write-if-changed (test first)
## Resume here
<!-- auto -->
- 2026-11-05T02:15:29Z step 1/1: copy, repo-relative paths, write-if-changed (test first)
- git: foreman/build; 8 uncommitted: plugin/lib/sampo/jeffexport.py, plugin/lib/sampo/smith.py, plugin/tests/test_code.py, plugin/tests/test_jeff_export.py, plugin/tests/test_site_build.py, design/sampo/directions/12-forge-illustrated/, scripts/, site/tools/
- touched since last checkpoint: plugin/tests/test_site_build.py, site/tools/writeif.py, site/tools/annotate.py, site/tools/port.py, site/tools/README.md, design/sampo/directions/12-forge-illustrated/NOTES.md, design/sampo/directions/12-forge-illustrated/_src/art.py, design/sampo/directions/12-forge-illustrated/_src/build.py, design/sampo/directions/12-forge-illustrated/_src/crops.py, design/sampo/directions/12-forge-illustrated/_src/final.sh, design/sampo/directions/12-forge-illustrated/_src/fonts/Archivo-normal.woff2, design/sampo/directions/12-forge-illustrated/_src/fonts/BodoniModa-italic.woff2, design/sampo/directions/12-forge-illustrated/_src/fonts/BodoniModa-normal.woff2, design/sampo/directions/12-forge-illustrated/_src/fonts/MartianMono-normal.woff2, design/sampo/directions/12-forge-illustrated/_src/frames.py
## Docs impact
site/tools/README.md (new): how the port ran, its inputs, and that port_css.py is lost so port.py is kept as a record; CHANGELOG line.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_site_build` → exit 0 · Ran 15 tests in 5.0s (9 classes, 16 at a time; slowest: Landing 4s, Reproducible 2s, TitleCard 2s) / OK [ran] [tree cc7865c8de8b] [world 2f1906870a] (2026-11-05T02:17:22Z)
- `du -sb design/sampo/directions/12-forge-illustrated | awk '{exit !($1 < 5000000)}' && test -f site/tools/port.py && test -f site/tools/annotate.py && python3 -m py_compile site/tools/port.py site/tools/annotate.py site/tools/writeif.py && echo ok` → exit 0 · ok [ran] [tree cc7865c8de8b] [world 2f1906870a] (2026-11-05T02:17:23Z)
- (ac 1) `python3 site/tools/port.py --help` → ✗ exit 1 · ^^^^^^^^^^^^^^^ / ModuleNotFoundError: No module named 'port_css' [ran] [tree 0048bb10ff5c] [world 2f1906870a] (2026-11-05T02:18:20Z)
- (ac 2) `python3 plugin/tests/run.py test_site_build` → exit 0 · Ran 15 tests in 3.9s (9 classes, 16 at a time; slowest: Landing 3s, Reproducible 2s, TitleCard 2s) / OK [ran] [tree 0048bb10ff5c] [world 2f1906870a] (2026-11-05T02:18:20Z)
- (ac 3) `test -f design/sampo/directions/12-forge-illustrated/index.html && test -f design/sampo/directions/12-forge-illustrated/_src/art.py && [ $(du -sm design/sampo/directions/12-forge-illustrated | cut -f1) -lt 5 ]` → exit 0 · (no output) [ran] [tree 0048bb10ff5c] [world 2f1906870a] (2026-11-05T02:18:20Z)
- (ac 1) `python3 -m py_compile site/tools/annotate.py && python3 site/tools/port.py 2>&1 | grep -q 'lost (see site/tools/README.md)'` → exit 0 · (no output) [ran] [tree 419e0a3e832a] [world 2f1906870a] (2026-11-05T02:19:26Z)
- (ac 3) `test -f design/site/12-forge-illustrated/index.html && test -f design/site/12-forge-illustrated/_src/art.py && [ $(du -sm design/site/12-forge-illustrated | cut -f1) -lt 5 ] && ! grep -rq /home/ design/site/12-forge-illustrated` → exit 0 · (no output) [ran] [tree 419e0a3e832a] [world 2f1906870a] (2026-11-05T02:19:26Z)
- (step 1) `python3 plugin/tests/run.py test_site_build test_sampo_design` → exit 0 · Ran 44 tests in 4.2s (13 classes, 16 at a time; slowest: Landing 3s, Reproducible 2s, Logo 2s) / OK [ran] [tree 419e0a3e832a] [world 2f1906870a] (2026-11-05T02:19:32Z)
- (ac 1) `python3 site/tools/port.py --help` → ✗ exit 1 · port.py needs .fm-scratch/port_css.py, which was lost (see site/tools/README.md) [ran] [tree 419e0a3e832a] [world 2f1906870a] (2026-11-05T02:19:40Z)
## Log
- 2026-11-04T06:16:57Z created
- 2026-11-05T02:09:13Z set scope=['site/tools/port.py', 'site/tools/annotate.py', 'plugin/tests/test_site_build.py']
- 2026-11-05T02:09:15Z planned: it has criteria and steps
- 2026-11-05T02:09:15Z set approved=True
- 2026-11-05T02:14:23Z set scope=['site/tools/port.py', 'site/tools/annotate.py', 'site/tools/writeif.py', 'site/tools/README.md', 'design/sampo/directions/12-forge-illustrated/**', 'plugin/tests/test_site_build.py']
- 2026-11-05T02:14:25Z focused
- 2026-11-05T02:14:26Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-11-05T02:17:35Z scope: CHANGELOG.md (the user-visible line for keeping direction 12 and the port tools)
- 2026-11-05T02:18:06Z steer-free fix: _src's eight shot scripts named a Playwright path under the account home; now CHROME_SHELL or ~/.cache (no tracked file carries a home path)
- 2026-11-05T02:19:05Z scope: design/site/12-forge-illustrated/** replaces design/sampo/directions/12-forge-illustrated/**: that folder is the three logo directions and test_sampo_design pins exactly three
- 2026-11-05T02:20:07Z dropped: criteria 1 and 3 had stale checks (port.py --help cannot run without the lost port_css.py; direction 12 moved from the logo directions folder to design/site); recreated with --redo
- 2026-11-05T02:20:07Z work at drop saved: 9001f07add2c (restore: git -C ~/.claude/foreman restore --source=9001f07add2c --worktree -- :/)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2850 [FEATURE M, done, 4 steps] Port 12's logo system and tokens into design/sampo: mark, simplified mark, animated mark, mark-light, mono, icon-16, wordmark, README h…
- T-2788 [FEATURE L, done, 7 steps] Sampo's theme is the illustrated forge (12-forge-illustrated, user pick 2026-11-03): super-improved, then carried through the logo and …
- decision 2026-11-03: [revisited: Sampo's logo is the Runestone direction] [check: python3 plugin/tests/run.py test_sampo_design] Sampo's logo is the Runestone direction …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_audit.py, plugin/tests/test_audit_run.py, plugin/tests/test_code_tui.py, plugin/tests/test_design_diverge.py, plugin/tests/test_design_gat…
