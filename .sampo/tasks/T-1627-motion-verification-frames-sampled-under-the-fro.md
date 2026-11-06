---
id: T-1627
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmmotion.py, plugin/lib/fmsmoke.py, plugin/lib/smoke_web.cjs, plugin/tests/test_motion_verify.py, CHANGELOG.md]
depends_on: [T-1624]
source: user
created: 2026-10-22T20:57:16Z
updated: 2026-10-23T01:53:15Z
base: d1d78062cd62fcf7eb454bdd75050a45b1d45f46
base_tree: 4a8946dc8313590daae0d386e56ccde977bf7426
plan0_at: 2026-10-22T23:42:12Z
plan0_scope: [plugin/lib/fmmotion.py, plugin/lib/fmsmoke.py, plugin/lib/smoke_web.cjs, plugin/tests/test_motion_verify.py, CHANGELOG.md]
verified: strong
---
# Motion verification: frames sampled under the frozen-time smoke profile asserted against the score within tolerance
## Raw request
> Motion verification: frames sampled under the frozen-time smoke profile asserted against the score within tolerance
## Interpretation
Motion verification: the frozen-time smoke profile samples an element's animated properties at fixed times; fmmotion.verify compares those samples with what the score says (within a tolerance) and prints a text diff naming the motion and property that drifted. Without a browser it says so and checks only the score. Canned sample JSON drives the tests.
## Assumptions (confidence)
## Acceptance criteria
- [x] sampled values within tolerance pass, a changed timing shows in the diff, no browser says so — verify with `python3 plugin/tests/run.py test_motion_verify.Sample`
## Non-goals
## Approach (options → choice → why)
Options: video capture and frame diffing (heavy, flaky); computed-style sampling under a frozen clock (exact, cheap); trusting the CSS. Choice: sampling under the frozen clock smoke already has (freeze()); the browser stays optional.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test on canned sample JSON
2. [x] assert and text diff in fmmotion
3. [x] optional Playwright sampling in smoke_web.cjs
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_motion_verify.Sample 2>&1 | tail -5` → ✗ exit 1 · Ran 5 tests in 5.6s (1 classes, 16 at a time; slowest: Sample 1s) / FAILED (1 classes) [ran] [tree 15c4bcb75877] (2026-10-23T01:27:55Z)
- (step 1) `python3 plugin/tests/run.py test_motion_verify.Sample` → ✗ exit 1 · Ran 5 tests in 1.3s (1 classes, 16 at a time; slowest: Sample 1s) / FAILED (1 classes) [ran] [tree 15c4bcb75877] (2026-10-23T01:27:59Z)
- (ac 1) `python3 plugin/tests/run.py test_motion_verify.Sample 2>&1 | grep -v "^$" | head -40` → ✗ exit 1 · Ran 5 tests in 1.3s (1 classes, 16 at a time; slowest: Sample 1s) / FAILED (1 classes) [ran] [tree 2869b3f7e960] (2026-10-23T01:28:43Z)
- (ac 1) `python3 plugin/tests/run.py test_motion_verify.Sample 2>&1 | grep -v "^$" | head -30` → ✗ exit 1 · Ran 5 tests in 3.7s (1 classes, 16 at a time; slowest: Sample 3s) / FAILED (1 classes) [ran] [tree 2012c3ffb7bb] (2026-10-23T01:29:31Z)
- (ac 1) `python3 plugin/tests/run.py test_motion_verify.Sample 2>&1 | tail -3` → exit 0 · Ran 5 tests in 2.4s (1 classes, 16 at a time; slowest: Sample 2s) / OK [ran] [tree 184418fbb3d3] (2026-10-23T01:29:44Z)
- (step 2) `python3 plugin/tests/run.py test_motion_verify.Sample` → exit 0 · Ran 5 tests in 2.2s (1 classes, 16 at a time; slowest: Sample 2s) / OK [ran] [tree 184418fbb3d3] (2026-10-23T01:29:51Z)
- (step 3) `python3 plugin/tests/run.py test_motion_verify 2>&1 | grep -v "^$" | tail -15` → exit 0 · Ran 10 tests in 2.1s (2 classes, 16 at a time; slowest: Sample 2s, Afterglow 0s) / OK [ran] [tree 06519fc2986a] (2026-10-23T01:30:36Z)
- (step 3) `python3 plugin/tests/run.py test_motion_verify` → exit 0 · Ran 10 tests in 1.8s (2 classes, 16 at a time; slowest: Sample 2s, Afterglow 0s) / OK [ran] [tree 06519fc2986a] (2026-10-23T01:30:42Z)
- (ac 1) `python3 plugin/tests/run.py test_motion_verify.Sample 2>&1 | grep -E "^(FAIL|ERROR|Assertion|OK|Ran)" | head -20` → ✗ exit 1 · Ran 8 tests in 6.0s (1 classes, 16 at a time; slowest: Sample 4s) / FAILED (1 classes) [ran] [tree 2e4f0a64d9ad] (2026-10-23T01:44:36Z)
- (step 2) `python3 plugin/tests/run.py test_motion_verify.Sample` → exit 0 · Ran 8 tests in 3.1s (1 classes, 16 at a time; slowest: Sample 3s) / OK [ran] [tree d771d92dc15a] (2026-10-23T01:47:27Z)
- (step 3) `python3 plugin/tests/run.py test_motion_verify` → exit 0 · Ran 12 tests in 3.0s (2 classes, 16 at a time; slowest: Sample 3s, Afterglow 0s) / OK [ran] [tree d771d92dc15a] (2026-10-23T01:47:31Z)
- (ac 1) `python3 plugin/tests/run.py test_motion_verify test_motion_score test_smoke` → exit 0 · Ran 73 tests in 24.3s (10 classes, 16 at a time; slowest: ProfilesFromFm 24s, Smoke 7s, Sample 4s) / OK [ran] [tree aa752c469cfe] (2026-10-23T01:52:00Z)
- (ac 1) `python3 plugin/tests/run.py test_motion_verify.Sample` → exit 0 · Ran 8 tests in 3.3s (1 classes, 16 at a time; slowest: Sample 3s) / OK [ran] [tree aa752c469cfe] (2026-10-23T01:52:16Z)
- (audit intent) `fm-reviewer pass (shared with T-1622); 2 MEDIUMs fixed test-first: repeating animations sampled over one held forward iteration then restored; only linearly-interpolated properties compared, colours/rotations noted not failed; LOWs: truncation and throw notes, reduced-motion forms skipped, per-test node skips, no-Playwright path tested, fm smoke --json without samples` → fm motion verify holds sampled values to the score's duration and curve within 2% of travel; a changed timing shows as a drift naming motion, property, time, expected and sampled values [tree aa752c469cfe] (2026-10-23T01:52:16Z)
- (audit adversary) `fm-reviewer pass (shared with T-1622); 2 MEDIUMs fixed test-first: repeating animations sampled over one held forward iteration then restored; only linearly-interpolated properties compared, colours/rotations noted not failed; LOWs: truncation and throw notes, reduced-motion forms skipped, per-test node skips, no-Playwright path tested, fm smoke --json without samples` → page samples validated (names in the score, finite bounded numbers, caps); node runs a constant script with data on stdin and a 30 s timeout [tree aa752c469cfe] (2026-10-23T01:52:16Z)
- (audit edge) `fm-reviewer pass (shared with T-1622); 2 MEDIUMs fixed test-first: repeating animations sampled over one held forward iteration then restored; only linearly-interpolated properties compared, colours/rotations noted not failed; LOWs: truncation and throw notes, reduced-motion forms skipped, per-test node skips, no-Playwright path tested, fm smoke --json without samples` → infinite/iterating animations, rotations and colour spaces no longer read as false drifts; no browser or no node says so and checks only the score [tree aa752c469cfe] (2026-10-23T01:52:16Z)
- (audit operator) `fm-reviewer pass (shared with T-1622); 2 MEDIUMs fixed test-first: repeating animations sampled over one held forward iteration then restored; only linearly-interpolated properties compared, colours/rotations noted not failed; LOWs: truncation and throw notes, reduced-motion forms skipped, per-test node skips, no-Playwright path tested, fm smoke --json without samples` → the frozen crawl survives a throwing animation; fm smoke --json output unchanged [tree aa752c469cfe] (2026-10-23T01:52:16Z)
## Log
- 2026-10-22T20:57:16Z created
- 2026-10-22T20:57:17Z set scope=['plugin/lib/fmmotion.py', 'plugin/lib/fmsmoke.py', 'plugin/lib/smoke_web.cjs', 'plugin/tests/test_motion_verify.py', 'CHANGELOG.md']
- 2026-10-22T20:57:18Z split from T-1527 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T20:57:19Z set depends_on=['T-1624']
- 2026-10-22T21:29:51Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_motion_verify.Sample`
- 2026-10-22T21:30:15Z criterion 1 text: sampled values within tolerance pass, a changed timing shows in the diff, no browser says so — verify with python3 plugin/tests/run.py test_motion_verify.Sample → sampled values within tolerance pass, a changed timing shows in the diff, no browser says so
- 2026-10-22T23:41:58Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1627.builder.md
- 2026-10-22T23:42:11Z focused
- 2026-10-23T01:51:25Z merged worktree-agent-aa99b5b9f698bb6fc (7 file(s))
- 2026-10-23T01:51:26Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa99b5b9f698bb6fc
- 2026-10-23T01:51:31Z focused
- 2026-10-23T01:52:11Z scope: smoke_web.cjs (sampleMotion), fmsmoke.py (motion pass-through), fmcli.py (verify action), MASTER.md
- 2026-10-23T01:53:15Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1527 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Motion verification: assert motion as sampled frames and filmstrips, a c
- T-1509 [FEATURE M, done, 4 steps] Brainstorm T-1479 round 2 (cluster 14): fm smoke hostile profiles: torture content (long w — lesson: A new check added to an existing g…
- research T-1509-review: Verdict: changes needed.** The default gate failure (finding 1) and the untested exit-code fix (finding 2) block approval. The rest are nits. [st…
- decision 2026-10-20: T-1300 slate: round 1 = C1 renderer, C2 motion engine, C3 live track, C4 gradients/contrast/focal line, C5 event flashes, C7 odometer/sparklines, C2…
- the similar finished task took 4 steps
- likely tests for the scope: plugin/tests/test_smoke.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmmotion.py, plugin/lib/fmsmoke.py, plugin/lib/smoke_web.cjs, plugin/tests/test_motion_verify.py; re-ground the plan against them before editing
## Lessons
- Verifying an interpolation needs the same space the page interpolates in: computed matrices and colours aren't linear in the sampled numbers
## Plan gaps
- failed first: step 1 failing test on canned sample JSON
## Files touched
- plugin/tests/test_motion_verify.py
- plugin/lib/fmmotion.py
- plugin/lib/fmcli.py
- plugin/lib/fmsmoke.py
- plugin/lib/smoke_web.cjs
- MASTER.md
- CHANGELOG.md
