---
id: T-1206
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T14:51:15Z
updated: 2026-10-16T15:07:52Z
base: 8c9c6d874d5d542adde0c4d75dc576bbe5db284d
base_tree: 2be248c194c0b35cf684301744a654813b77bafa
plan0_at: 2026-10-16T15:00:50Z
plan0_scope: []
verified: ok
---
# A GitHub Pages site for Foreman: one modern page with the real demo, the loop, the guard and install
## Raw request
> Can you make a beautiful and modern website for foreman for github pages?
## Interpretation
A public landing page at chasesunstrom.github.io/foreman that shows what Foreman is in its own vernacular (a foreman on site: work orders, inspections, stamps), built from the README's real content and the recorded session (demo/live.mp4), with install in one copy, light and dark themes, phone to desktop, fast (no framework), and deployed by a GitHub Actions Pages workflow from site/ on pushes to main.
## Assumptions (confidence)
## Acceptance criteria
- [x] site/index.html renders with no console errors at 390 px and 1440 px in light and dark, every section present, links resolve, the video plays from the copied asset; a Pages workflow builds _site from site/ plus demo/live.mp4 and demo/demo.svg — verify with `python3 -c "import html.parser,sys;html.parser.HTMLParser().feed(open('site/index.html').read());print('ok')" && test -f .github/workflows/pages.yml`
## Non-goals
## Approach (options → choice → why)
A complete version has: hero with the real recorded session, the eight-station loop, the seven things it enforces, the guard refusing real commands, evidence, builder lanes, other agents (codex, gemini, opencode), honest numbers, install with copy buttons, footer links, OG/meta, favicon, reduced-motion and keyboard focus. Options: (a) hand-built static site/ (one HTML, one CSS, tiny JS) deployed by an Actions Pages workflow that also copies demo assets, no build step; (b) Jekyll from docs/ (GitHub's default, but it would duplicate the 1.8 MB video into docs/ and adds Liquid/theme overhead); (c) a framework (Astro/Next) static export (a Node toolchain in a Python repo, for one page). Choice: (a): one page needs no generator, the workflow avoids duplicating assets, and it previews by opening the file. Enabling Pages (Settings, Pages, Source: GitHub Actions) is a one-time setting only the user can flip.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Design plan (tokens, type, layout) and the page: site/index.html, site/style.css, site/assets
2. [x] Pages workflow (.github/workflows/pages.yml) and a doc test that its paths exist
3. [x] Screenshot at phone and desktop width, light and dark; fix what looks off
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 -c "import html.parser;html.parser.HTMLParser().feed(open('site/index.html').read());print('parsed')" && ls site/assets` → exit 0 · foreman.svg / poster.jpg [ran] [tree be5bdf391699] (2026-10-16T15:05:56Z)
- (step 2) `python3 plugin/tests/run.py -k test_every_local_link_resolves_and_the_workflow_copies_what_exists` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Site 0s) / OK [ran] [tree be5bdf391699] (2026-10-16T15:05:57Z)
- (step 3) `headless Chromium screenshots of the assembled _site at 390 px and 1440 px, light and dark (scratchpad shoot.sh)` → all four render: hero, loop, rules, guard, evidence, lanes, stack, numbers, not-for, install, footer; lanes labels and hero width fixed after the first pass [tree be5bdf391699] (2026-10-16T15:05:57Z)
- (ac 1) `python3 -c "import html.parser,sys;html.parser.HTMLParser().feed(open('site/index.html').read());print('ok')" && test -f .github/workflows/pages.yml` → exit 0 · ok [ran] [tree be5bdf391699] (2026-10-16T15:06:13Z)
- `python3 plugin/tests/run.py -k test_every_local_link_resolves_and_the_workflow_copies_what_exists` → exit 0 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: Site 0s) / OK [ran] [tree be5bdf391699] (2026-10-16T15:06:13Z)
- (audit intent) `self review against the brief and the frontend-design checklist: real content from the README and real numbers (744 from the round tag, 2,004 tests at 1.2.33, the 5,000-command replay corpus); four screenshots read; claims checked against code (fail-closed onFailure block, snapshots, replay gate on guard tasks, lane resume)` → hero with the real recorded session, the eight stations, the seven rules, guard, proof, lanes, other agents, numbers, when-not-to-use, install with copy; deploys from site/ via Actions [tree be5bdf391699] (2026-10-16T15:06:13Z)
- (audit adversary) `self review against the brief and the frontend-design checklist: real content from the README and real numbers (744 from the round tag, 2,004 tests at 1.2.33, the 5,000-command replay corpus); four screenshots read; claims checked against code (fail-closed onFailure block, snapshots, replay gate on guard tasks, lane resume)` → static page, no user input; the workflow uses only first-party actions, no event text in run:, least permissions (contents read, pages write, id-token write); localStorage wrapped in try [tree be5bdf391699] (2026-10-16T15:06:13Z)
- (audit edge) `self review against the brief and the frontend-design checklist: real content from the README and real numbers (744 from the round tag, 2,004 tests at 1.2.33, the 5,000-command replay corpus); four screenshots read; claims checked against code (fail-closed onFailure block, snapshots, replay gate on guard tasks, lane resume)` → works with reduced motion (video gets controls, stations shown done), without clipboard API, without JS (content is static), at 390 px with no sideways scroll except inside the command boxes [tree be5bdf391699] (2026-10-16T15:06:13Z)
- (audit operator) `self review against the brief and the frontend-design checklist: real content from the README and real numbers (744 from the round tag, 2,004 tests at 1.2.33, the 5,000-command replay corpus); four screenshots read; claims checked against code (fail-closed onFailure block, snapshots, replay gate on guard tasks, lane resume)` → deploy needs Pages set to GitHub Actions once; the workflow runs only when site/ or the two demo files change; the 1.8 MB video loads metadata only until it scrolls into view [tree be5bdf391699] (2026-10-16T15:06:13Z)
- (audit maintainer) `self review against the brief and the frontend-design checklist: real content from the README and real numbers (744 from the round tag, 2,004 tests at 1.2.33, the 5,000-command replay corpus); four screenshots read; claims checked against code (fail-closed onFailure block, snapshots, replay gate on guard tasks, lane resume)` → one HTML file with tokens on :root and a dark set; a test keeps every local link and the workflow's copied files resolvable [tree be5bdf391699] (2026-10-16T15:06:13Z)
## Log
- 2026-10-16T14:51:15Z created
- 2026-10-16T15:00:49Z planned from capture
- 2026-10-16T15:00:49Z focused
- 2026-10-16T15:06:10Z scope: site/, .github/workflows/pages.yml, MASTER row, CHANGELOG line, the Site test in test_docs.py
- 2026-10-16T15:07:51Z done
- 2026-10-16T15:07:52Z committed 6d4d43b8 (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1035 [FEATURE M, done, 2 steps] Re-record the README demo video and refresh the README's pictures with the new UI (chat se — lesson: Record the demo after the UI work …
- research mission-20261016-095938.pack: can you make foreman code? an even better harness than CC, that works with other CLI tools/models as an amazing harness, etc.?
- research mission-20261016-095938: Request: can you make foreman code? an even better harness than CC, that works with other CLI tools/models as an amazing harness, etc.?
- decision 2026-10-16: T-1054: every wild cluster (23) plus the earlier catalogue's skips became briefs T-1057..T-1087; the forever loop (T-1057) goes first after the demo…
- the similar finished task took 2 steps
## Lessons
- A marketing page for a dev tool reads honest when every claim maps to a check in the code; three of the first-draft claims had to be confirmed against the code before they stayed
## Files touched
- site/assets/poster.jpg
- site/assets/foreman.svg
- site/index.html
- .github/workflows/pages.yml
- MASTER.md
- plugin/tests/test_docs.py
- CHANGELOG.md
