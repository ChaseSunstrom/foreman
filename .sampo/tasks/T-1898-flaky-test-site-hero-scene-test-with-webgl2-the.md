---
id: T-1898
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/tests/test_site_hero.py, plugin/lib/fmcore.py, plugin/tests/test_gate_friction.py, CHANGELOG.md]
depends_on: [T-1900]
source: discovered
created: 2026-10-29T02:40:06Z
updated: 2026-10-29T04:40:51Z
base: 6e128b9daedb862c595343428a073cc3227b2fb4
base_tree: 5ce6d4070ba1a0b219cf07eabd38850e9592e357
plan0_at: 2026-10-29T04:31:12Z
plan0_scope: [plugin/tests/test_site_hero.py, plugin/lib/fmcore.py, plugin/tests/test_gate_friction.py, CHANGELOG.md]
verified: strong
---
# The site-hero scene test waits by frames, not timer ticks, and the flaky note shows the assertion, not a rule line
## Raw request
> Flaky: test_site_hero.Scene.test_with_webgl2_the_scene_goes_live_survives_a_lost_context_and_caps_the_pixel_ratio failed then passed on the same tree in fm check (T-1875 gates); find the race
## Interpretation
The probe's wait polled 300 virtual 10 ms ticks; virtual time runs ahead while a loaded compositor has not drawn a frame, so ResizeObserver (which makes the scene live) had not fired: first=poster, dpr 0.33. rAF ticks only advance with rendering. The note printed the excerpt's last line, unittest's trailing ----- rule.
## Assumptions (confidence)
## Acceptance criteria
- [x] The flaky note's line under each test is the assertion (AssertionError: …), never unittest's trailing rule — verify with `python3 plugin/tests/run.py test_gate_friction`
- [x] The probe runs in real time over DevTools (as spied), so virtual time can't run out its waits before a loaded machine draws; it passes under --load 16 — verify with `python3 plugin/tests/run.py --load 16 -k test_with_webgl2 test_site_hero`
## Non-goals
## Approach (options → choice → why)
Probe in real time over DevTools via spied (page/init/expr parameters), with HEARD faking a device pixel ratio of 3 and recording console output, errors and rejections; the probe always writes its result (try/catch, skips lose/restore unless live). Flaky note: failure_excerpt drops unittest's trailing rule lines and the note shows the last Error/Exception line. Alternatives considered: longer virtual-time budget (still flaked), polling frames by rAF (still virtual), a load-aware timeout only (doesn't fix virtual time).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failure_excerpt test red (trailing rule, note line)
2. [x] failure_excerpt drops trailing rules; the note picks the exception line; the probe runs over DevTools in real time; green
3. [x] CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-29T04:33:54Z steps 3/3 done
- git: foreman/build; 4 uncommitted: CHANGELOG.md, plugin/lib/fmcore.py, plugin/tests/test_gate_friction.py, plugin/tests/test_site_hero.py
- touched since last checkpoint: plugin/tests/test_gate_friction.py, CHANGELOG.md, plugin/lib/fmcore.py, plugin/tests/test_site_hero.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1912t.txt, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1912i.txt
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_gate_friction` → red as expected (exit 1) · Ran 5 tests in 4.1s (2 classes, 16 at a time; slowest: Flakes 4s, Typos 3s) / FAILED (1 classes) [ran] [tree 9762f4d7e340] (2026-10-29T04:31:21Z)
- (step 2) `python3 plugin/tests/run.py test_gate_friction test_site_hero` → exit 0 · Ran 23 tests in 16.0s (4 classes, 16 at a time; slowest: Scene 16s, Flakes 4s, Typos 3s) / OK [ran] [tree 6a12ae58f4aa] (2026-10-29T04:31:47Z)
- (step 3) `grep -c 'T-1898' CHANGELOG.md` → exit 0 · 1 [ran] [tree 6a12ae58f4aa] (2026-10-29T04:31:48Z)
- (ac 1) `python3 plugin/tests/run.py test_gate_friction` → exit 0 · Ran 10 tests in 2.3s (2 classes, 16 at a time; slowest: Flakes 2s, Typos 2s) / OK [ran] [tree 27acd7c34cd1] (2026-10-29T04:40:23Z)
- (ac 2) `python3 plugin/tests/run.py --load 16 -k test_with_webgl2 test_site_hero` → exit 0 · Ran 13 tests in 17.4s (2 classes, 16 at a time; slowest: Scene 17s, Hero 3s) / OK [ran] [tree 27acd7c34cd1] (2026-10-29T04:40:23Z)
- (audit intent) `fm-reviewer early pass: approve with nits, all fixed` → probe runs in real time; dpr pinned at 2 [tree 27acd7c34cd1] (2026-10-29T04:40:23Z)
- (audit edge) `fm-reviewer early pass: approve with nits, all fixed` → the probe always reports, through a throw or a scene that never went live [tree 27acd7c34cd1] (2026-10-29T04:40:23Z)
- (audit adversary) `fm-reviewer early pass: approve with nits, all fixed` → test-only page and a log excerpt; no findings [tree 27acd7c34cd1] (2026-10-29T04:40:23Z)
- (audit maintainer) `fm-reviewer early pass: approve with nits, all fixed` → spied's docstring names init and expr [tree 27acd7c34cd1] (2026-10-29T04:40:23Z)
## Log
- 2026-10-29T02:40:06Z created
- 2026-10-29T02:43:23Z planned: it has criteria and steps
- 2026-10-29T02:43:23Z set title=The site-hero scene test waits by frames, not timer ticks, and the flaky note shows the assertion, not a rule line, type=FIX, tier=M, scope=['plugin/tests/test_site_hero.py', 'plugin/lib/fmcore.py', 'plugin/tests/test_gate_friction.py', 'CHANGELOG.md']
- 2026-10-29T02:55:57Z set depends_on=['T-1877']
- 2026-10-29T03:06:15Z set depends_on=['T-1900']
- 2026-10-29T04:23:50Z criterion 2 verify: `python3 plugin/tests/run.py test_site_hero` → `python3 plugin/tests/run.py --load 16 -k test_with_webgl2 test_site_hero`
- 2026-10-29T04:23:50Z criterion 2 text: The probe waits on animation frames, so a slow compositor under load cannot time out the first wait; 8 concurrent runs pass → The probe runs in real time over DevTools (as spied), so virtual time can't run out its waits before a loaded machine draws; it passes under --load 16
- 2026-10-29T04:31:11Z focused
- 2026-10-29T04:33:55Z paused: focus moved to T-1913
- 2026-10-29T04:40:00Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-29T04:40:00Z focused
- 2026-10-29T04:40:49Z done
- 2026-10-29T04:40:51Z committed 485c5c60 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook 3D on the web: a designed scene that never breaks the page (fm playbooks show ui/scene-3d)
- T-1495 [FEATURE M, done, 2 steps] 3D template: a zero-dependency single-file WebGL2 scene — lesson: A probe that can't drive animation frames (dump-dom) passes vacuously…
- T-1610 [FEATURE M, done, 3 steps] Site hero scene: a single-file WebGL2 proof-chain scene over the poster (tasks as stations, red to green as light along the track), fro…
- decision 2026-10-09: T-0476 quarantine skipped: fm check keeps treating a gate flaky 2+ times as failing
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_core.py
## Preflight
Changed in scope since this was planned (2026-10-29): CHANGELOG.md, plugin/lib/fmcore.py; re-ground the plan against them before editing
## Why not caught
the probe ran in virtual time, which a quiet machine never ran out
## Lessons
- drive browser probes in real time; headless virtual time races a loaded machine
## Files touched
- plugin/tests/test_gate_friction.py
- CHANGELOG.md
- plugin/lib/fmcore.py
- plugin/tests/test_site_hero.py
