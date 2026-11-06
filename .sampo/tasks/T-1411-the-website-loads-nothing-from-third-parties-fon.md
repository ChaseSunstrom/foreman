---
id: T-1411
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-10-21T19:01:41Z
base: f700ac7a13f3d94ed0685a14f73c751847bf11a4
base_tree: 144f21c81ad614ce47d8c5448e144ead3f2d5109
plan0_at: 2026-10-21T17:33:07Z
plan0_scope: []
verified: strong
---
# The website loads nothing from third parties: fonts self-hosted, and the site build fails on any outside host
## Raw request
> FIX: The website loads nothing from third parties: fonts self-hosted, and site/build.py fails on any outside host in a built page (S24, B20)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: python3 site/build.py exits non-zero on a fixture page linking fonts.googleapis.com and zero on the real site
## Interpretation
site/build.py's pages load Google Fonts (build.py:196-198), against Foreman's nothing-leaves-the-machine stance. Self-host the fonts (or fall back to system fonts) and make the build refuse any outside host so it can't come back.
## Assumptions (confidence)
## Acceptance criteria
- [x] python3 site/build.py exits non-zero on a page that links fonts.googleapis.com and zero on the real site, whose pages load no outside host — verify with `python3 plugin/tests/run.py test_docs`
## Non-goals
## Approach (options → choice → why)
Options: (A) vendor the woff2 files under site/assets/fonts with their OFL licences and @font-face rules (chosen if the files are small and licensed for it); (B) drop the web fonts for a system stack (no assets, a slight look change); (C) keep the CDN (rejected: the defect). Plus a build-time scan of every emitted page for http(s) URLs outside the repo's own GitHub links, failing the build.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: the build refuses a fixture page with an outside host; the real build has none
2. [x] Self-host or drop the fonts; add the outside-host scan to build.py; docs
## Resume here
## Docs impact
CHANGELOG line; site build docstring
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_docs 2>&1 | tail -15` → ✗ exit 1 · Ran 50 tests in 8.2s (12 classes, 16 at a time; slowest: TaskLifecycle 5s, TaskDocsDrift 2s, DocsDrift 1s) / FAILED (1 classes) [ran] [tree 02e2ad0a9012] (2026-10-21T17:36:40Z)
- (step 1) `python3 plugin/tests/run.py test_docs` → ✗ exit 1 · Ran 50 tests in 4.2s (12 classes, 16 at a time; slowest: TaskLifecycle 4s, TaskDocsDrift 2s, DocsDrift 1s) / FAILED (1 classes) [ran] [tree 02e2ad0a9012] (2026-10-21T17:36:48Z)
- (ac 1) `python3 plugin/tests/run.py test_docs 2>&1 | tail -15` → exit 0 · Ran 50 tests in 3.7s (12 classes, 16 at a time; slowest: TaskLifecycle 3s, Site 2s, TaskDocsDrift 1s) / OK [ran] [tree 69619c7c9801] (2026-10-21T17:38:31Z)
- (step 2) `python3 plugin/tests/run.py test_docs 2>&1 | tail -15` → exit 0 · Ran 50 tests in 3.7s (12 classes, 16 at a time; slowest: TaskLifecycle 3s, Site 2s, TaskDocsDrift 1s) / OK [ran] [tree 69619c7c9801] (2026-10-21T17:38:31Z)
- (step 2) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 50 tests in 3.5s (12 classes, 16 at a time; slowest: TaskLifecycle 3s, Site 1s, TaskDocsDrift 1s) / OK [ran] [tree 69619c7c9801] (2026-10-21T17:38:43Z)
- (step 2) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 50 tests in 3.2s (12 classes, 16 at a time; slowest: TaskLifecycle 3s, Site 2s, TaskDocsDrift 1s) / OK [ran] [tree c91e26bd60c0] (2026-10-21T18:58:01Z)
- (ac 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 50 tests in 3.5s (12 classes, 16 at a time; slowest: TaskLifecycle 3s, Site 2s, TaskDocsDrift 1s) / OK [ran] [tree c91e26bd60c0] (2026-10-21T18:58:06Z)
- (audit intent) `self: read the diff — Google Fonts links gone from layout() and index.html; style.css font stacks name Barlow/JetBrains Mono first then system faces; build.py's outside_hosts scans every built html/svg/css/js and exits 1 naming file and URL` → the real site builds (exit 0) and a fixture page with a Google Fonts link fails naming it (test_docs) [tree c91e26bd60c0] (2026-10-21T18:58:06Z)
- (audit edge) `self: read the diff — Google Fonts links gone from layout() and index.html; style.css font stacks name Barlow/JetBrains Mono first then system faces; build.py's outside_hosts scans every built html/svg/css/js and exits 1 naming file and URL` → <a> links, og:image, SVG namespaces, data: URLs and the site's own host don't count; 13 flagged and 9 allowed cases in test_what_counts_as_loading_an_outside_host; known misses: runtime-built URLs, CSS escapes, meta refresh [tree c91e26bd60c0] (2026-10-21T18:58:06Z)
- (audit operator) `self: read the diff — Google Fonts links gone from layout() and index.html; style.css font stacks name Barlow/JetBrains Mono first then system faces; build.py's outside_hosts scans every built html/svg/css/js and exits 1 naming file and URL` → no browser here, so the fallback fonts' look on the deployed site is unchecked [tree c91e26bd60c0] (2026-10-21T18:58:06Z)
- (audit self) `self: read the diff — Google Fonts links gone from layout() and index.html; style.css font stacks name Barlow/JetBrains Mono first then system faces; build.py's outside_hosts scans every built html/svg/css/js and exits 1 naming file and URL` → no findings [tree c91e26bd60c0] (2026-10-21T18:58:06Z)
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-21T17:32:34Z planned from capture
- 2026-10-21T17:32:48Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1411.builder.md
- 2026-10-21T17:33:06Z focused
- 2026-10-21T18:16:13Z merged worktree-agent-a878c47e8e7e4f4c1 (4 file(s))
- 2026-10-21T18:24:18Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a878c47e8e7e4f4c1
- 2026-10-21T18:57:57Z focused
- 2026-10-21T19:01:41Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1385 [FEATURE M, dropped, 0 steps] Site/build.py:196-198` pulls Google Fonts, against the project's stance that nothing leave
- research brainstorm-fm-anthropic-catalogue: Source: research/brainstorm-20261021-120257 (fm ideas, 10 lenses, 4 rounds, 3 deepened, --seen every earlier ideas.md: 520 ne…
- T-1396 [SECURITY M, planned, 2 steps] Hostile skills and plugins can't get past the indexer: a 25+ item corpus quarantined with reasons, the Agent Skills spec checked, o…
- decision 2026-10-20: [cites: research/brainstorm-20261020] Round 1 of the 2026-10-20 brainstorm builds T-1254 (cost per fully-correct session on the page), T-1255 (Claud…
## Why not caught
none: a new policy, not a regression
## Lessons
- A no-third-party rule holds only with a build check that fails on violation; removing the links once doesn't keep them out
## Plan gaps
- failed first: step 1 Failing test: the build refuses a fixture page with an outside host; the real build has none
## Files touched
- plugin/tests/test_docs.py
- site/build.py
- site/index.html
- site/style.css
- CHANGELOG.md
- MASTER.md
- README.md
- plugin/lib/fmcli.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmlib.py
- plugin/lib/fmplugins.py
- plugin/tests/fixtures/hostile/corpus.json
- plugin/tests/fixtures/hostile/marketplace.json
- plugin/tests/test_code.py
- plugin/tests/test_doctor.py
- plugin/tests/test_lib_hostile.py
- plugin/tests/test_library.py
