---
id: T-0902
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T17:09:21Z
updated: 2026-10-15T17:59:37Z
base: b7843974d8863d1a4eed57df1d25814cb6431de9
base_tree: 3218828ee820717c03fce73941cdeaf1bd694572
verified: strong
---
# Showcase: a recorded demo of Foreman at work in the README, and a README that reads well
## Raw request
> Showcase: make the README better and nicer, and record a video (or GIF/cast) of Foreman working so it can be showcased (user, 2026-10-15)
## Interpretation
The user wants Foreman showcased: a recording of it working that plays in the README, and a README that is better and nicer to read. fm demo is the honest subject (the real fm and guard on a seeded bug, no model, deterministic), so: give it a pace and colour fit for recording, record it as an asciinema cast, render that to an animated SVG the README embeds (GitHub plays it), and restructure the README: a short pitch, the demo, what it does in scannable form, quick start, then the detail (kept, folded into sections and <details>).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm demo --pace paces it and colours a terminal, and stays plain and quick otherwise — verify with `python3 plugin/tests/run.py test_demo`
- [x] the README embeds the recording and every section of the old one survives — verify with `python3 -c "import sys; t=open('README.md').read(); need=['demo/demo.svg','Install','When not to use','Permissions','Headless','Updating','fm demo']; m=[x for x in need if x not in t]; sys.exit(print(m) or 1) if m else None"`
## Non-goals
## Approach (options → choice → why)
1) fm demo --pace + colour → asciinema cast (stdlib pty recorder) → animated SVG via svg-term-cli (chosen: deterministic, re-recordable by one script, crisp at any size, plays inline on GitHub, no model spend). 2) VHS tape → GIF (needs a Go binary and ttyd downloaded; GIFs are large and blurry). 3) A screen recording of a real Claude Code session with the foreman-ui band (most impressive but needs the user's desktop, a live model and many takes; nondeterministic). 4) Static screenshots (no motion). Complete version: paced coloured demo, a script that records and renders it, the cast kept for asciinema play, the SVG in docs/, README restructured with nothing factual lost; a real-session recording noted as a follow-up.
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm demo --pace and colour (test first)
2. [x] record: a script that records fm demo to a cast and renders docs/demo.svg
3. [x] README rewrite
4. [x] docs, review
## Resume here
<!-- auto -->
- 2026-10-15T17:43:48Z steps 4/4 done
- git: foreman/build; 9 uncommitted: CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmdemo.py, plugin/lib/fmdoctor.py, plugin/lib/fmguard.py, plugin/tests/test_demo.py, plugin/tests/test_safety.py, demo/
## Docs impact
README rewritten; MASTER file map (demo/) and fmdemo --pace; CHANGELOG round 5
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_demo test_help` → exit 0 · Ran 8 tests in 4.0s (3 classes, 16 at a time; slowest: Demo 4s, Help 1s, PromptApprovals 1s) / OK [ran] [tree 334b94561f8e] (2026-10-15T17:30:14Z)
- (step 3) `python3 -c "import sys; t=open('README.md').read(); need=['demo/demo.svg','Install','When not to use','Permissions','Headless','Updating','fm demo']; m=[x for x in need if x not in t]; sys.exit(print(m) or 1) if m else None"` → exit 0 · (no output) [ran] [tree 334b94561f8e] (2026-10-15T17:30:15Z)
- (step 2) `python3 -c "import json; ev=[json.loads(l) for l in open('demo/demo.cast')]; assert ev[0]['version']==2 and ev[-1][0] > 25; import os; assert os.path.getsize('demo/demo.svg') > 100000 and os.path.getsize('demo/demo.mp4') > 100000; print(len(ev)-1, 'events', round(ev[-1][0]), 's')"` → exit 0 · 627 events 30 s [ran] [tree 7437f9fb679f] (2026-10-15T17:41:31Z)
- (step 4) `fm doctor` → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmdemo.py, plugin/lib/fmdoctor.py, plugin/lib/fmguard.py — commit it through a task, or git checkout it back / fm doc [ran] [tree 7437f9fb679f] (2026-10-15T17:41:40Z)
- (ac 1) `python3 plugin/tests/run.py test_demo` → exit 0 · Ran 4 tests in 3.7s (1 classes, 16 at a time; slowest: Demo 4s) / OK [ran] [tree 7437f9fb679f] (2026-10-15T17:43:39Z)
- (ac 2) `python3 -c "import sys; t=open('README.md').read(); need=['demo/demo.svg','Install','When not to use','Permissions','Headless','Updating','fm demo']; m=[x for x in need if x not in t]; sys.exit(print(m) or 1) if m else None"` → exit 0 · (no output) [ran] [tree 7437f9fb679f] (2026-10-15T17:43:39Z)
- (audit intent) `self review: the recording is the real fm demo (no model, deterministic), checked by still frames at 9 s and 33 s and an MP4 frame at 17 s; the cast and SVG carry no home path or user name (grep: 0); README keeps every fact of the old one (install flags, permissions, mod detail folded into <details>), and fm doctor's flag check now reads a Flags heading with bullets` → the user asked for a README that is better and nicer and a recording of Foreman working to showcase: the README now opens with the pitch, the animated demo and a why table, then quick start; demo/demo.mp4 is a 30 s shareable video, demo/demo.svg plays inline on GitHub, demo/record.py re-records both [tree 7437f9fb679f] (2026-10-15T17:43:39Z)
- (audit operator) `self review: the recording is the real fm demo (no model, deterministic), checked by still frames at 9 s and 33 s and an MP4 frame at 17 s; the cast and SVG carry no home path or user name (grep: 0); README keeps every fact of the old one (install flags, permissions, mod detail folded into <details>), and fm doctor's flag check now reads a Flags heading with bullets` → re-recording needs npx (svg-term-cli@2.1.1 pinned) and, for --mp4, Playwright's headless Chromium (or CHROME) and ffmpeg, each named in the script's error; the recording moved from docs/ to demo/ because a docs/ folder made fm docs read the playbooks' example docs/adr paths as this repo's [tree 7437f9fb679f] (2026-10-15T17:43:39Z)
- (audit intent) `self review: the recording is the real fm demo (no model, deterministic), checked by still frames at 9 s and 33 s and an MP4 frame at 17 s; the cast and SVG carry no home path or user name (grep: 0); README keeps every fact of the old one (install flags, permissions, mod detail folded into <details>), and fm doctor's flag check now reads a Flags heading with bullets` → the user asked for a README that is better and nicer and a recording of Foreman working to showcase: the README now opens with the pitch, the animated demo and a why table, then quick start; demo/demo.mp4 is a 30 s shareable video, demo/demo.svg plays inline on GitHub, demo/record.py re-records both [tree 7437f9fb679f] (2026-10-15T17:59:30Z)
- (audit operator) `self review: the recording is the real fm demo (no model, deterministic), checked by still frames at 9 s and 33 s and an MP4 frame at 17 s; the cast and SVG carry no home path or user name (grep: 0); README keeps every fact of the old one (install flags, permissions, mod detail folded into <details>), and fm doctor's flag check now reads a Flags heading with bullets` → re-recording needs npx (svg-term-cli@2.1.1 pinned) and, for --mp4, Playwright's headless Chromium (or CHROME) and ffmpeg, each named in the script's error; the recording moved from docs/ to demo/ because a docs/ folder made fm docs read the playbooks' example docs/adr paths as this repo's [tree 7437f9fb679f] (2026-10-15T17:59:30Z)
- (audit adversary) `self review: the recording is the real fm demo (no model, deterministic), checked by still frames at 9 s and 33 s and an MP4 frame at 17 s; the cast and SVG carry no home path or user name (grep: 0); README keeps every fact of the old one (install flags, permissions, mod detail folded into <details>), and fm doctor's flag check now reads a Flags heading with bullets` → this task doesn't change the guard (fmguard.py in its window is T-0894's and T-0901's, committed under their ids); the published recording shows only the demo's throwaway paths as <demo>, and record.py runs the pinned svg-term-cli version through npx [tree 7437f9fb679f] (2026-10-15T17:59:30Z)
## Log
- 2026-10-15T17:09:21Z created
- 2026-10-15T17:15:53Z planned from capture
- 2026-10-15T17:15:53Z focused
- 2026-10-15T17:18:54Z paused: focus moved to T-0901
- 2026-10-15T17:26:12Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-15T17:26:12Z focused
- 2026-10-15T17:29:46Z criterion 2 verify: `python3 -c "import sys; t=open('README.md').read(); need=['docs/demo.svg','Install','When not to use','Permissions','Headless','Updating','fm demo']; m=[x for x in need if x not in t]; sys.exit(print(m) or 1) if m else None"` → `python3 -c "import sys; t=open('README.md').read(); need=['demo/demo.svg','Install','When not to use','Permissions','Headless','Updating','fm demo']; m=[x for x in need if x not in t]; sys.exit(print(m) or 1) if m else None"`
- 2026-10-15T17:30:35Z paused: focus moved to T-0894
- 2026-10-15T17:41:30Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-15T17:41:30Z focused
- 2026-10-15T17:43:48Z paused: focus moved to T-0894
- 2026-10-15T17:44:14Z focused
- 2026-10-15T17:44:15Z scope: T-0894's commit 23d528a swept in this task's demo/ files and the fmdoctor Flags change (made while T-0894 was focused); redoing it locally (unpushed) so T-0894 keeps its 2 files and these land here
- 2026-10-15T17:59:12Z user approved core in Claude Code's permission prompt
- 2026-10-15T17:59:30Z note: the fm demo --pace parser lines in fmcli.py went out in T-0901's commit c059744 (same file, committed while this was paused)
- 2026-10-15T17:59:31Z done
- 2026-10-15T17:59:31Z committed 82db46f (8 files)
- 2026-10-15T17:59:37Z commit amended to f7a22df: adds demo/record.py and the fmdoctor Flags check, which the close left out as another task's
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0870 [FEATURE M, done, 2 steps] fm demo: see Foreman work in a minute without model calls (a temp repo with a seeded bug: brief, guard block, red test, fix, evidence, …
- research brainstorm-round4-20261015: 437 ideas (9 lenses x 4 rounds + 3 deepen rounds, past every earlier run) from new evidence: a clean-HOME newcomer install, a survey…
- T-0328 [FEATURE L, done, 9 steps] FEATURE: Foreman Desktop v2 — clean up the UI so it looks less AI-made and better organize — lesson: Read another tool's internal store…
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
## Lessons
- Showcase with the deterministic path, not a live model run: a seeded demo that drives the real CLI records identically every time, so the README can never drift from what the product does
## Files touched
- plugin/tests/test_demo.py
- plugin/lib/fmcli.py
- plugin/lib/fmdemo.py
- docs/record_demo.py
- docs/demo.cast
- docs/demo.svg
- README.md
- MASTER.md
- CHANGELOG.md
- demo/demo.cast
- demo/demo.mp4
- demo/demo.svg
- demo/record.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmguard.py
- plugin/tests/test_safety.py
