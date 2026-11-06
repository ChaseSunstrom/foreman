---
id: T-1785
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-23T12:25:02Z
updated: 2026-10-28T10:27:52Z
group: site pages and playbook examples
base: b734071b2fa3325e0bd124b827eea5abb87ddf90
base_tree: c974f29be2ce838c5f26c93a0feff72c6692362d
plan0_at: 2026-10-28T09:46:07Z
plan0_scope: []
verified: strong
---
# Site gallery: every design playbook (references/ui/*.md) has a reproducible example page b
## Raw request
> Site gallery: every design playbook (references/ui/*.md) has a reproducible example page built by one command, so a reader sees the playbook's result (from T-1650)
## Interpretation
Each UI playbook under plugin/skills/playbooks/references/ui/ (INDEX.md aside) gets a worked example page that shows the playbook's result: a standalone HTML file shipped beside the playbooks (references/ui/examples/NAME.html; scene-3d's is templates/scene.html), named in the playbook's own text. python3 site/build.py (the site's one command) copies them to site/gallery/NAME.html and writes site/gallery/index.html: one card per playbook with its when-to-use line and a link. Each example is self-contained (no outside host), passes fm design lint (fm new check) and keeps the five-rule UI contract (reduced motion, contrast, keyboard, 360 px, states).
## Assumptions (confidence)
## Acceptance criteria
- [x] Every UI playbook has an example that exists, is named in the playbook, passes fm new check and loads no outside host; build.py writes gallery/index.html linking each and gallery/NAME.html — verify with `python3 plugin/tests/run.py test_site_gallery`
- [x] The site builds clean and its existing tests stay green — verify with `python3 plugin/tests/run.py test_site test_site_build test_site_hero`
## Non-goals
No screenshots or browser at build time; no new template kinds for fm new; no rewrite of the playbooks beyond one pointer line each.
## Approach (options → choice → why)
Complete version: 12 examples (11 new + the scene template), playbook pointers, a gallery index in the site nav, a test that every UI playbook has one that lints clean and loads nothing outside, the build writing them. Options: (1) hand-written standalone examples beside the playbooks, copied by build.py — chosen: they ship with the plugin, open from disk, are lint-checked like fm new's templates; (2) examples generated in Python inside build.py — rejected: unreadable, not reusable outside the site; (3) screenshots — rejected: a browser at build time, binary blobs, not reproducible; (4) link only existing artifacts (scene template, site charts) — covers 3 of 12. Work split: infra + test here; examples by sonnet fm-builder lanes in worktrees (separate files, no conflicts), merged and spot-checked.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Gallery infra red-first: test_site_gallery.py, build.py writes gallery/, INDEX.md and each playbook name their example
2. [x] Examples: 11 pages by fm-builder lanes (design-direction, type-and-colour, composition, interaction, motion, game-feel, data-viz, scrollytelling, sound-design, visual-qa, terminal-ui), merged
3. [x] Gates, spot-check the pages in a browser, review
## Resume here
<!-- auto -->
- 2026-10-28T10:20:01Z steps 3/3 done
- git: foreman/build; 23 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmplaybooks.py, plugin/skills/playbooks/references/ui/INDEX.md, plugin/skills/playbooks/references/ui/composition.md, plugin/skills/playbooks/references/ui/data-viz.md, plugin/skills/playbooks/references/ui/design-direction.md, plugin/skills/playbooks/references/ui/examples/composition.html, plugin/skills/playbooks/references/ui/examples/terminal-ui.html, plugin/skills/playbooks/references/ui/examples/type-and-colour.html
- touched since last checkpoint: site/pages.py, site/build.py, plugin/tests/test_site_gallery.py, plugin/skills/playbooks/references/ui/composition.md, plugin/skills/playbooks/references/ui/examples/terminal-ui.html, plugin/skills/playbooks/references/ui/examples/composition.html, plugin/skills/playbooks/references/ui/examples/type-and-colour.html, plugin/tests/test_playbook_check.py, plugin/lib/fmplaybooks.py, plugin/skills/playbooks/references/ui/data-viz.md, plugin/skills/playbooks/references/ui/scrollytelling.md
- failures met: type-and-colour.html: old text not found: ' --text: #0; --text-muted: #0; --border: #0d0…'; assertionerror: 0 != 0 : ✗ composition.html: in no index (skill.md, or index.md named in …
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_site_gallery` → red as expected (exit 1) · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: Gallery 0s) / FAILED (1 classes) [ran] [tree c1c8dcc8048a] (2026-10-28T09:47:38Z)
- (step 2) `python3 plugin/tests/run.py test_site_gallery test_site_build` → ✗ exit 1 · Ran 7 tests in 1.7s (5 classes, 16 at a time; slowest: TitleCard 1s, Gallery 1s, Reproducible 0s) / FAILED (2 classes) [ran] [tree 1b10a2eabe88] (2026-10-28T10:09:20Z)
- (step 2) `python3 plugin/tests/run.py test_site_gallery test_site_build test_site_hero` → exit 0 · Ran 21 tests in 14.8s (7 classes, 16 at a time; slowest: Scene 14s, Hero 2s, TitleCard 1s) / OK [ran] [tree f1073375ca41] (2026-10-28T10:10:13Z)
- (step 3) `python3 plugin/tests/run.py test_site_gallery test_site_build` → exit 0 · Ran 9 tests in 1.9s (5 classes, 16 at a time; slowest: TitleCard 1s, Reproducible 1s, Gallery 1s) / OK [ran] [tree 85a50577dc49] (2026-10-28T10:18:35Z)
- (ac 1) `python3 plugin/tests/run.py test_site_gallery` → exit 0 · Ran 4 tests in 0.6s (1 classes, 16 at a time; slowest: Gallery 0s) / OK [ran] [tree eb911fa7de56] (2026-10-28T10:26:48Z)
- (ac 2) `python3 plugin/tests/run.py test_site test_site_build test_site_hero` → ✗ exit 1 · Ran 23 tests in 11.9s (8 classes, 16 at a time; slowest: Scene 12s, Header 3s, Hero 1s) / FAILED (1 classes) [ran] [tree eb911fa7de56] (2026-10-28T10:26:48Z)
- (ac 2) `python3 plugin/tests/run.py test_site test_site_build test_site_hero` → exit 0 · Ran 23 tests in 12.0s (8 classes, 16 at a time; slowest: Scene 12s, Header 3s, Hero 1s) / OK [ran] [tree eb911fa7de56] (2026-10-28T10:27:39Z)
- (audit intent) `One fm-reviewer pass over the gallery diff; every finding fixed and re-probed (360 px in light, dark and reduced motion 9/9, behaviour probes, fm new check on each page); full fm check green` → each UI playbook names a worked example page; the site's Gallery copies and links all 12, and test_site_gallery keeps each passing fm new check [tree eb911fa7de56] (2026-10-28T10:27:39Z)
- (audit design) `One fm-reviewer pass over the gallery diff; every finding fixed and re-probed (360 px in light, dark and reduced motion 9/9, behaviour probes, fm new check on each page); full fm check green` → dark muted text at 7:1, filters show a check as well as colour, reload uses aria-disabled, a status region announces deploy state, terminal-ui keys only fire while the screen or a control has focus (WCAG 2.1.4) [tree eb911fa7de56] (2026-10-28T10:27:39Z)
- (audit adversary) `One fm-reviewer pass over the gallery diff; every finding fixed and re-probed (360 px in light, dark and reduced motion 9/9, behaviour probes, fm new check on each page); full fm check green` → SVG/XLink/XHTML namespace URIs are exempt only inside script or CSS text, a src still counts; an Example path that leaves the library stops the build [tree eb911fa7de56] (2026-10-28T10:27:39Z)
- (audit edge) `One fm-reviewer pass over the gallery diff; every finding fixed and re-probed (360 px in light, dark and reduced motion 9/9, behaviour probes, fm new check on each page); full fm check green` → 360 px with no sideways scroll or console error in all three modes; an HTML comment's src is not a link [tree eb911fa7de56] (2026-10-28T10:27:39Z)
- (audit maintainer) `One fm-reviewer pass over the gallery diff; every finding fixed and re-probed (360 px in light, dark and reduced motion 9/9, behaviour probes, fm new check on each page); full fm check green` → one Example: regex in pages.gallery; the folder index rule is tested; gallery pages are exempt from the site theme head because they are copied byte for byte [tree eb911fa7de56] (2026-10-28T10:27:39Z)
## Log
- 2026-10-23T12:25:02Z created
- 2026-10-28T09:44:30Z criterion 2 verify: `python3 plugin/tests/run.py test_site` → `python3 plugin/tests/run.py test_site test_site_build test_site_hero`
- 2026-10-28T09:46:06Z focused
- 2026-10-28T09:53:06Z paused: focus moved to T-1829
- 2026-10-28T09:54:44Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-28T09:54:44Z focused
- 2026-10-28T10:00:03Z steer: 11 pages in three builder lanes T-1830/T-1831/T-1832 (launched 2026-10-28); T-1803 split into T-1833 (routing) and T-1834 (use) lanes; inbox next, one lane each as slots free
- 2026-10-28T10:05:40Z paused: focus moved to T-1832
- 2026-10-28T10:08:17Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-28T10:08:17Z focused
- 2026-10-28T10:08:58Z paused: focus moved to T-1830
- 2026-10-28T10:09:17Z focused
- 2026-10-28T10:27:50Z done
- 2026-10-28T10:27:52Z committed 271f40ec (32 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1495 [FEATURE M, done, 2 steps] 3D template: a zero-dependency single-file WebGL2 scene — lesson: A probe that can't drive animation frames (dump-dom) passes vacuously…
- playbook UI playbooks (fm playbooks show ui/INDEX)
- T-1494 [FEATURE M, done, 2 steps] 3D playbook: scene composition, budget and survival contract — lesson: API facts from memory in a playbook need a reviewer who checks e…
- decision 2026-10-23: T-1623: the five UI contract rules are written down from what the UI playbooks already require: motion (reduced motion as its own path), contrast (p…
- similar finished tasks took 2–2 steps
## Lessons
- Files added under skills/playbooks/references face test_docs attribution, the playbook index rule and the token ratchet: a lane adding them must run test_docs and test_playbook_check, not only its own tests
## Plan gaps
- failed first: step 2 Examples: 11 pages by fm-builder lanes (design-direction, type-and-colour, composition, interaction…
## Files touched
- plugin/tests/test_site_gallery.py
- site/pages.py
- site/build.py
- plugin/skills/playbooks/references/ui/composition.md
- plugin/skills/playbooks/references/ui/data-viz.md
- plugin/skills/playbooks/references/ui/design-direction.md
- plugin/skills/playbooks/references/ui/game-feel.md
- plugin/skills/playbooks/references/ui/interaction.md
- plugin/skills/playbooks/references/ui/motion.md
- plugin/skills/playbooks/references/ui/scene-3d.md
- plugin/skills/playbooks/references/ui/scrollytelling.md
- plugin/skills/playbooks/references/ui/sound-design.md
- plugin/skills/playbooks/references/ui/terminal-ui.md
- plugin/skills/playbooks/references/ui/type-and-colour.md
- plugin/skills/playbooks/references/ui/visual-qa.md
- plugin/skills/playbooks/references/ui/INDEX.md
- CHANGELOG.md
- MASTER.md
- plugin/skills/playbooks/references/ui/examples/terminal-ui.html
- plugin/skills/playbooks/references/ui/examples/composition.html
- plugin/skills/playbooks/references/ui/examples/type-and-colour.html
- plugin/tests/test_playbook_check.py
- plugin/lib/fmplaybooks.py
- plugin/skills/playbooks/references/ui/examples/data-viz.html
- plugin/skills/playbooks/references/ui/examples/design-direction.html
- plugin/skills/playbooks/references/ui/examples/game-feel.html
- plugin/skills/playbooks/references/ui/examples/interaction.html
- plugin/skills/playbooks/references/ui/examples/motion.html
- plugin/skills/playbooks/references/ui/examples/scrollytelling.html
- plugin/skills/playbooks/references/ui/examples/sound-design.html
