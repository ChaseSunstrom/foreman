---
id: T-1637
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmshot.py, plugin/lib/smoke_web.cjs, plugin/lib/fmimg.py, plugin/tests/test_shot.py, CHANGELOG.md]
depends_on: [T-1636, T-1630]
source: user
created: 2026-10-22T20:57:45Z
updated: 2026-10-23T02:25:48Z
base: d7e6b5537792a4b2340f8d639c0ac789a1d3aaf4
base_tree: 39de8a8d3381710eeda0401ee593d11d446743fe
plan0_at: 2026-10-23T01:48:17Z
plan0_scope: [plugin/lib/fmshot.py, plugin/lib/smoke_web.cjs, plugin/lib/fmimg.py, plugin/tests/test_shot.py, CHANGELOG.md]
verified: strong
---
# fm shot --diff: a fallback font fails; a pixel diff under the baseline's noise floor passes
## Raw request
> fm shot --diff: a fallback font fails; a pixel diff under the baseline's noise floor passes
## Interpretation
fm shot --diff BASE compares new shots with a baseline: a page whose fonts fell back (document.fonts reports a face not loaded) fails; a pixel difference under the baseline's own noise floor (measured from repeated baseline shots) passes, above it fails with the changed area. Uses fmimg's diff.
## Assumptions (confidence)
## Acceptance criteria
- [x] a fallback font fails and a diff under the floor passes — verify with `python3 plugin/tests/run.py test_fmshot.Diff`
## Non-goals
## Approach (options → choice → why)
Options: a fixed pixel threshold (flaky across machines); perceptual diff libraries (dependencies); a floor measured per baseline. Choice: the measured floor: it adapts to the page's own noise (animations, anti-aliasing) without a magic number.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests on canned data
2. [x] document.fonts check in the crawler
3. [x] noise floor from repeated baseline shots
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_fmshot.Diff` → ✗ exit 1 · Ran 5 tests in 5.6s (1 classes, 16 at a time; slowest: Diff 4s) / FAILED (1 classes) [ran] [tree cbabc74a063c] (2026-10-23T01:50:58Z)
- (step 2) `python3 plugin/tests/run.py test_fmshot.Diff` → exit 0 · Ran 5 tests in 16.4s (1 classes, 16 at a time; slowest: Diff 16s) / OK [ran] [tree 9daec84c6c10] (2026-10-23T01:53:39Z)
- (step 3) `python3 plugin/tests/run.py test_fmshot` → exit 0 · Ran 22 tests in 24.3s (4 classes, 16 at a time; slowest: Diff 24s, Capture 16s, InABrowser 9s) / OK [ran] [tree 9daec84c6c10] (2026-10-23T01:54:04Z)
- (step 1) `python3 plugin/tests/run.py test_fmshot` → ✗ exit 1 · Ran 28 tests in 29.5s (4 classes, 16 at a time; slowest: Diff 29s, Capture 13s, InABrowser 8s) / FAILED (2 classes) [ran] [tree cf3ea7a55a2e] (2026-10-23T02:10:13Z)
- (step 3) `python3 plugin/tests/run.py test_fmshot` → exit 0 · Ran 28 tests in 22.8s (4 classes, 16 at a time; slowest: Diff 23s, Capture 9s, Unruly 6s) / OK [ran] [tree 6bda4f9cd70a] (2026-10-23T02:15:16Z)
- (ac 1) `python3 plugin/tests/run.py test_fmshot.Diff` → exit 0 · Ran 11 tests in 26.3s (1 classes, 16 at a time; slowest: Diff 26s) / OK [ran] [tree e51bd7c5a0a8] (2026-10-23T02:23:52Z)
- (ac 1) `python3 plugin/tests/run.py test_fmshot.Diff` → exit 0 · Ran 11 tests in 27.9s (1 classes, 16 at a time; slowest: Diff 28s) / OK [ran] [tree e51bd7c5a0a8] (2026-10-23T02:24:29Z)
- (audit intent) `fm-reviewer pass (shared with T-1651); 4 MEDIUMs fixed test-first: --diff with no browser exits 1 'not compared' and an empty --diff is refused; fonts count only for visible text (canvas page tested in a real browser); fonts() has its own 10 s limit and can't abort later pages, unchecked fonts fail under --diff; the floor reports its frame count, 'unmeasured' with none, and warns on an animated baseline; LOWs: realpath refusal, bidi/zero-width stripping` → fm shot --diff BASE fails a page whose fonts fell back or whose pixels changed past the baseline's own noise floor, naming the changed box [tree e51bd7c5a0a8] (2026-10-23T02:24:29Z)
- (audit adversary) `fm-reviewer pass (shared with T-1651); 4 MEDIUMs fixed test-first: --diff with no browser exits 1 'not compared' and an empty --diff is refused; fonts count only for visible text (canvas page tested in a real browser); fonts() has its own 10 s limit and can't abort later pages, unchecked fonts fail under --diff; the floor reports its frame count, 'unmeasured' with none, and warns on an animated baseline; LOWs: realpath refusal, bidi/zero-width stripping` → page-controlled family names cleaned (control, bidi, zero-width) and capped; --diff can't point into the output folder, by symlink or relative path [tree e51bd7c5a0a8] (2026-10-23T02:24:29Z)
- (audit edge) `fm-reviewer pass (shared with T-1651); 4 MEDIUMs fixed test-first: --diff with no browser exits 1 'not compared' and an empty --diff is refused; fonts count only for visible text (canvas page tested in a real browser); fonts() has its own 10 s limit and can't abort later pages, unchecked fonts fail under --diff; the floor reports its frame count, 'unmeasured' with none, and warns on an animated baseline; LOWs: realpath refusal, bidi/zero-width stripping` → different-size, missing, empty and self-linked baselines fail; no browser is 'not compared', never a pass [tree e51bd7c5a0a8] (2026-10-23T02:24:29Z)
- (audit operator) `fm-reviewer pass (shared with T-1651); 4 MEDIUMs fixed test-first: --diff with no browser exits 1 'not compared' and an empty --diff is refused; fonts count only for visible text (canvas page tested in a real browser); fonts() has its own 10 s limit and can't abort later pages, unchecked fonts fail under --diff; the floor reports its frame count, 'unmeasured' with none, and warns on an animated baseline; LOWs: realpath refusal, bidi/zero-width stripping` → an animated baseline is called out with --frozen as the fix [tree e51bd7c5a0a8] (2026-10-23T02:24:29Z)
## Log
- 2026-10-22T20:57:45Z created
- 2026-10-22T20:57:46Z set scope=['plugin/lib/fmshot.py', 'plugin/lib/smoke_web.cjs', 'plugin/lib/fmimg.py', 'plugin/tests/test_shot.py', 'CHANGELOG.md']
- 2026-10-22T20:57:47Z split from T-1531 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T20:57:48Z set depends_on=['T-1636', 'T-1630']
- 2026-10-22T21:29:54Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_shot.Diff`
- 2026-10-22T21:30:18Z criterion 1 text: a fallback font fails and a diff under the floor passes — verify with python3 plugin/tests/run.py test_shot.Diff → a fallback font fails and a diff under the floor passes
- 2026-10-22T23:42:51Z criterion 1 verify: `python3 plugin/tests/run.py test_shot.Diff` → `python3 plugin/tests/run.py test_fmshot.Diff`
- 2026-10-22T23:42:52Z plan: build after T-1636 merges, by the same builder (it knows fmshot.Browser); tests move with fm shot's to test_fmshot.py
- 2026-10-23T01:47:53Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1637.builder.md
- 2026-10-23T01:48:12Z focused
- 2026-10-23T02:23:05Z merged worktree-agent-abc11ae62cf8e6442 (5 file(s))
- 2026-10-23T02:23:06Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-abc11ae62cf8e6442
- 2026-10-23T02:23:23Z focused
- 2026-10-23T02:24:00Z scope: MASTER.md (fmshot entry), plugin/tests/test_fmshot.py and the fmcli --diff flag; build-merge files committed by their tasks
- 2026-10-23T02:25:42Z done
- 2026-10-23T02:25:48Z committed 73984054 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1531 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): fm shot: a visual proof loop on the smoke harness with animation frames,
- research T-1631-review: Verdict: approve with nits.** The brief names no audit lens, so I covered intent, adversary, edge, operator and maintainer together. I could only…
- T-1636 [FEATURE M, done, 3 steps] fm shot: viewport and frame captures and a poster frame per animated page, or a stated reason without a browser — lesson: Headless Chro…
- decision 2026-10-22: Recommendation: keep 2 SE as the bench gate's fail line (3-5% false alarms); add an inconclusive verdict for a pass-total loss between 1 and 2 SE th…
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_fmshot.py, plugin/tests/test_shot.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmimg.py, plugin/lib/fmshot.py, plugin/lib/smoke_web.cjs, plugin/tests/test_shot.py; re-ground the plan against them before editing
## Lessons
- A visual-regression gate must fail when it couldn't look: no browser or an unchecked font is a failure under --diff, not a skip
## Plan gaps
- failed first: step 1 failing tests on canned data
## Files touched
- plugin/tests/test_fmshot.py
- plugin/lib/fmshot.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcost.py
- plugin/lib/fmdesign.py
- plugin/lib/fmdoctor.py
- plugin/skills/ui-design/SKILL.md
- plugin/tests/test_design_gates.py
- plugin/tests/test_doctor.py
