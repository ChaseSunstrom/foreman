---
id: T-3097
type: CLEAN
tier: M
status: done
priority: normal
scope: [site/tools/**, design/site/**, plugin/tests/test_site_build.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-05T02:20:07Z
updated: 2026-11-05T02:23:21Z
base: b3ac10ff49295f54456dfa8a6c32f2b8fa9b9888
base_tree: ab0d245b6375d38111d3d00152230ace0565424a
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-11-05T02:20:09Z
plan0_scope: []
verified: strong
unproven: [infra, ui-unshot]
---
# Keep direction 12 and its port tools in the repo (site/tools, design/site), writing outputs only when changed
## Raw request
> Keep direction 12 and its port tools in the repo (site/tools, design/site), writing outputs only when changed
## Interpretation
Reading 1 (chosen): keep the source of direction 12 and the port scripts that made the landing in the repo, as a record, with the lost port_css.py stated. Reading 2: rebuild port_css.py so the port reruns byte-for-byte; rejected, the port was one-time (T-2851) and the landing has moved on.
## Assumptions (confidence)
## Acceptance criteria
- [x] port.py and annotate.py live under site/tools; port.py, missing its lost port_css.py helper, stops with a message naming site/tools/README.md instead of a traceback — verify with `python3 -m py_compile site/tools/annotate.py && python3 site/tools/port.py 2>&1 | grep -q 'lost (see site/tools/README.md)'`
- [x] port.py writes outputs only when their content changes: a rerun with no change leaves the file and its mtime alone — verify with `python3 plugin/tests/run.py test_site_build`
- [x] Direction 12's source (index.html, NOTES.md, _src without caches, assets and logo SVGs) lives under design/site/12-forge-illustrated, beside not inside the logo directions, under 5 MB, with no account home path; the logo directions' tests still pass — verify with `test -f design/site/12-forge-illustrated/index.html && test -f design/site/12-forge-illustrated/_src/art.py && [ $(du -sm design/site/12-forge-illustrated | cut -f1) -lt 5 ] && ! grep -rq /home/ design/site/12-forge-illustrated && python3 plugin/tests/run.py test_sampo_design`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: copy 12's source and port.py/annotate.py as they are, add a 16-line write_if_changed; likely outcome: kept, rerun leaves no churn, port.py stops with a clear message. 2. Do less: keep only port.py and annotate.py; fails if: the direction itself is lost with the scratchpad. 3. Rebuild port_css.py; fails if: 12's stylesheet split cannot be recovered exactly. Choice 1 (85%)
## Risks and rollback
## Execution prompt
## Steps
1. [x] copy, repo-relative paths, write-if-changed (test first), README, changelog
## Resume here
## Docs impact
site/tools/README.md (new): how the port ran, its inputs, and that port_css.py is lost so port.py is kept as a record; CHANGELOG line.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_site_build test_sampo_design` → exit 0 · Ran 44 tests in 2.2s (13 classes, 16 at a time; slowest: Landing 2s, Reproducible 1s, TitleCard 1s) / OK [ran] [tree 9b2a47d0a4b1] [world 2f1906870a] (2026-11-05T02:20:25Z)
- (ac 1) `python3 -m py_compile site/tools/annotate.py && python3 site/tools/port.py 2>&1 | grep -q 'lost (see site/tools/README.md)'` → exit 0 · (no output) [ran] [tree 9b2a47d0a4b1] [world 2f1906870a] (2026-11-05T02:20:26Z)
- (ac 2) `python3 plugin/tests/run.py test_site_build` → exit 0 · Ran 15 tests in 2.2s (9 classes, 16 at a time; slowest: Landing 2s, Reproducible 1s, TitleCard 1s) / OK [ran] [tree 9b2a47d0a4b1] [world 2f1906870a] (2026-11-05T02:20:28Z)
- (ac 3) `test -f design/site/12-forge-illustrated/index.html && test -f design/site/12-forge-illustrated/_src/art.py && [ $(du -sm design/site/12-forge-illustrated | cut -f1) -lt 5 ] && ! grep -rq /home/ design/site/12-forge-illustrated && python3 plugin/tests/run.py test_sampo_design` → exit 0 · Ran 29 tests in 1.0s (4 classes, 16 at a time; slowest: Logo 1s, Tokens 0s, Directions 0s) / OK [ran] [tree 9b2a47d0a4b1] [world 2f1906870a] (2026-11-05T02:20:30Z)
- (ac 1) `python3 -m py_compile site/tools/annotate.py && python3 site/tools/port.py 2>&1 | grep -q 'lost (see site/tools/README.md)'` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T02:20:26Z [ran] [tree 9b2a47d0a4b1] [world 2f1906870a] (2026-11-05T02:20:35Z)
- (ac 2) `python3 plugin/tests/run.py test_site_build` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T02:20:28Z [ran] [tree 9b2a47d0a4b1] [world 2f1906870a] (2026-11-05T02:20:35Z)
- (ac 3) `test -f design/site/12-forge-illustrated/index.html && test -f design/site/12-forge-illustrated/_src/art.py && [ $(du -sm design/site/12-forge-illustrated | cut -f1) -lt 5 ] && ! grep -rq /home/ design/site/12-forge-illustrated && python3 plugin/tests/run.py test_sampo_design` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T02:20:30Z [ran] [tree 9b2a47d0a4b1] [world 2f1906870a] (2026-11-05T02:20:35Z)
- (audit intent) `self: the tools and direction 12's source were only in the scratchpad and are now kept in the repo (design/site, beside the logo directions), with the lost port_css.py stated and port.py stopping with a message naming it` → kept at design/site/12-forge-illustrated (2.2 MB; 1.7 GB of review renders, the tower and PNG renders left out) and site/tools; outputs written only when changed [tree 9b2a47d0a4b1] (2026-11-05T02:20:35Z)
- (audit edge) `self: the tools and direction 12's source were only in the scratchpad and are now kept in the repo (design/site, beside the logo directions), with the lost port_css.py stated and port.py stopping with a message naming it` → a rerun with unchanged content leaves mtime alone (test); a missing parent dir is created; the logo directions' tests, which pin exactly three directions, still pass with 12 kept outside that folder [tree 9b2a47d0a4b1] (2026-11-05T02:20:35Z)
- (audit adversary) `self: the tools and direction 12's source were only in the scratchpad and are now kept in the repo (design/site, beside the logo directions), with the lost port_css.py stated and port.py stopping with a message naming it` → no secrets or home paths in the copied files (the eight _src shot scripts named the account's home, now CHROME_SHELL or ~) [tree 9b2a47d0a4b1] (2026-11-05T02:20:35Z)
- (audit intent) `self: the tools and direction 12's source were only in the scratchpad and are now kept in the repo (design/site, beside the logo directions), with the lost port_css.py stated and port.py stopping with a message naming it` → kept at design/site/12-forge-illustrated (2.2 MB; 1.7 GB of review renders, the tower and PNG renders left out) and site/tools; outputs written only when changed [tree 9b2a47d0a4b1] (2026-11-05T02:22:01Z)
- (audit edge) `self: the tools and direction 12's source were only in the scratchpad and are now kept in the repo (design/site, beside the logo directions), with the lost port_css.py stated and port.py stopping with a message naming it` → a rerun with unchanged content leaves mtime alone (test); a missing parent dir is created; the logo directions' tests, which pin exactly three directions, still pass with 12 kept outside that folder [tree 9b2a47d0a4b1] (2026-11-05T02:22:01Z)
- (audit adversary) `self: the tools and direction 12's source were only in the scratchpad and are now kept in the repo (design/site, beside the logo directions), with the lost port_css.py stated and port.py stopping with a message naming it` → no secrets or home paths in the copied files (the eight _src shot scripts named the account's home, now CHROME_SHELL or ~) [tree 9b2a47d0a4b1] (2026-11-05T02:22:01Z)
## Log
- 2026-11-05T02:20:07Z created
- 2026-11-05T02:20:07Z redo of T-2904: takes over its start point and edited files
- 2026-11-05T02:20:08Z focused
- 2026-11-05T02:20:09Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-11-05T02:20:17Z set scope=['site/tools/**', 'design/site/**', 'plugin/tests/test_site_build.py', 'CHANGELOG.md']
- 2026-11-05T02:20:17Z set approved=True
- 2026-11-05T02:22:00Z scope: design/sampo/directions/12-forge-illustrated/** was the first copy's place; the files moved to design/site/12-forge-illustrated and nothing is left there (test_sampo_design pins the three logo directions)
- 2026-11-05T02:23:18Z done
- 2026-11-05T02:23:21Z committed d5494d7b (40 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2904 [CLEAN M, dropped, 1 steps] Keep 12's port scripts (port.py, annotate.py) in the repo under site/tools, writing…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2851 [FEATURE M, done, 3 steps] Port 12's landing page into site/: index.html, style.css and site.js from 12's site/ split, fonts self-hosted in site/assets/fonts with…
- decision 2026-11-05: T-2904: port.py is kept as a record that stops with a clear message, not rebuilt, since port_css.py is lost and the port was one-time
- similar finished tasks took 3–9 steps
## Behaviour lock
none: the change adds new files only (site/tools, design/site, one new test class) and one CHANGELOG line; no existing code changes behaviour; test_site_build and test_sampo_design ran green after
## Lessons
- Check a folder's tests before adding to it: design/sampo/directions looked like the home for a site direction but is the logo directions, pinned at three by test_sampo_design. Keep the source of anything that ships in the repo the same task, as T-2851's port_css.py was lost with its builder's worktree.
## Files touched
- plugin/tests/test_site_build.py
- site/tools/writeif.py
- site/tools/annotate.py
- site/tools/port.py
- site/tools/README.md
- design/sampo/directions/12-forge-illustrated/NOTES.md
- design/sampo/directions/12-forge-illustrated/_src/art.py
- design/sampo/directions/12-forge-illustrated/_src/build.py
- design/sampo/directions/12-forge-illustrated/_src/crops.py
- design/sampo/directions/12-forge-illustrated/_src/final.sh
- design/sampo/directions/12-forge-illustrated/_src/fonts/Archivo-normal.woff2
- design/sampo/directions/12-forge-illustrated/_src/fonts/BodoniModa-italic.woff2
- design/sampo/directions/12-forge-illustrated/_src/fonts/BodoniModa-normal.woff2
- design/sampo/directions/12-forge-illustrated/_src/fonts/MartianMono-normal.woff2
- design/sampo/directions/12-forge-illustrated/_src/frames.py
- design/sampo/directions/12-forge-illustrated/_src/fullpage.py
- design/sampo/directions/12-forge-illustrated/_src/hero.py
- design/sampo/directions/12-forge-illustrated/_src/led2.png
- design/sampo/directions/12-forge-illustrated/_src/marks.py
- design/sampo/directions/12-forge-illustrated/_src/measure.py
- design/sampo/directions/12-forge-illustrated/_src/page.html
- design/sampo/directions/12-forge-illustrated/_src/page.js
- design/sampo/directions/12-forge-illustrated/_src/sections.py
- design/sampo/directions/12-forge-illustrated/_src/sheet.html
- design/sampo/directions/12-forge-illustrated/_src/sheetshot.py
- design/sampo/directions/12-forge-illustrated/_src/shot.py
- design/sampo/directions/12-forge-illustrated/_src/stations.py
- design/sampo/directions/12-forge-illustrated/_src/style.css
- design/sampo/directions/12-forge-illustrated/_src/trace.py
- design/sampo/directions/12-forge-illustrated/_src/trim.py
