---
id: T-3220
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/tests/test_moons_scale.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-05T17:29:52Z
updated: 2026-11-05T18:40:18Z
trigger: ci-red
trigger_key: 09aeed4b8bce88fb
base: eb7b7ad31e4e6a56fe57431c5eff0e63f60b6ff8
base_tree: 2fb9bf6700250be6ac3f0e9feb39ed62084113f3
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T17:44:50Z
plan0_scope: []
verified: strong
unproven: [meaning]
---
# FIX: CI on main is red at fcf658d (tests)
## Raw request
> FIX: CI on main is red at fcf658d (tests)
> CONTEXT: found by the session-start sweep (T-1810): https://github.com/ChaseSunstrom/sampo/commit/fcf658dbe492037e4d671b322fbb43bc85ff8379
> CI-red: fcf658dbe492037e4d671b322fbb43bc85ff8379
## Interpretation
CI on GitHub main fails test_moons_scale.Families and Promote since 2026-11-04: the tests patch _local and models.embed but _reps picks the embedder through _embedder, which discovers this box's Ollama embedding models; CI has none, so it falls back to shingles and different families. Reproduced: FOREMAN_NO_LOCAL_MODELS=1 fails 2 classes on origin/main and 11 on HEAD.
## Assumptions (confidence)
## Acceptance criteria
- [x] test_moons_scale passes with local models hidden as on CI, and still passes on this box — verify with `FOREMAN_NO_LOCAL_MODELS=1 python3 plugin/tests/run.py test_moons_scale && python3 plugin/tests/run.py test_moons_scale`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] pin each moons test's embedder (the box's Ollama embedding models leaked into Families, Promote and 9 more)
2. [x] sweep the whole suite with local models hidden for other box-dependent tests
## Resume here
<!-- auto -->
- 2026-11-05T17:49:13Z step 2/2: sweep the whole suite with local models hidden for other box-dependent tests
- git: foreman/build; 3 uncommitted: CHANGELOG.md, plugin/tests/test_moons_scale.py, scripts/
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `FOREMAN_NO_LOCAL_MODELS=1 python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 114 tests in 5.2s (76 jobs, 16 at a time; slowest: Catalogue 4s, Route 3s, FamilyLinks 3s) / OK [ran] [tree 3f9540fc548e] [world 2f1906870a] (2026-11-05T17:46:00Z)
- (step 2) `FOREMAN_NO_LOCAL_MODELS=1 python3 plugin/tests/run.py test_moons_scale test_live_page.Page test_long.Long test_code_fakes.CodeFakes test_code_tui.Command test_hooks.NoTaskGateClose` → exit 0 · Ran 207 tests in 33.6s (192 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 25s, Page.test_the_network_view_draws_three_columns_and_pulse [ran] [tree 843fa2466bb8] [world 2f1906870a] (2026-11-05T18:15:20Z)
- `FOREMAN_NO_LOCAL_MODELS=1 python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 114 tests in 7.2s (20 jobs, 16 at a time; slowest: Yield 5s, KeepGrow 5s, Writers 4s) / OK (start tree + this task's tests) [ran] [tree 843fa2466bb8] [world 2f1906870a] (2026-11-05T18:15:34Z)
- `FOREMAN_NO_LOCAL_MODELS=1 python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 114 tests in 5.4s (26 jobs, 16 at a time; slowest: Yield 5s, Writers 4s, Catalogue 4s) / OK [ran] [tree 843fa2466bb8] [world 2f1906870a] (2026-11-05T18:15:34Z)
- (ac 1) `FOREMAN_NO_LOCAL_MODELS=1 python3 plugin/tests/run.py test_moons_scale && python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 114 tests in 12.4s (26 jobs, 16 at a time; slowest: Yield 12s, Wilder 12s, Writers 10s) / OK [ran] [tree 56dba25d3391] [world 2f1906870a] (2026-11-05T18:16:12Z)
- (audit intent) `self: every test helper that builds families or reps now patches _embedder, as go() already did; the discovery test drops FOREMAN_NO_LOCAL_MODELS beside MOONS_EMBED since it serves its own fake Ollama; swept the full suite with local models hidden` → test_moons_scale passes with no local models (CI) and with them (this box) [tree 56dba25d3391] (2026-11-05T18:16:12Z)
- (audit edge) `self: every test helper that builds families or reps now patches _embedder, as go() already did; the discovery test drops FOREMAN_NO_LOCAL_MODELS beside MOONS_EMBED since it serves its own fake Ollama; swept the full suite with local models hidden` → build(local=False) now really takes the cached-vectors path; before, the box's embedder made 'server down' a no-op [tree 56dba25d3391] (2026-11-05T18:16:12Z)
- (audit operator) `self: every test helper that builds families or reps now patches _embedder, as go() already did; the discovery test drops FOREMAN_NO_LOCAL_MODELS beside MOONS_EMBED since it serves its own fake Ollama; swept the full suite with local models hidden` → CI goes green only when this lands on GitHub main; sampo ship carries it [tree 56dba25d3391] (2026-11-05T18:16:12Z)
- (audit self) `self: every test helper that builds families or reps now patches _embedder, as go() already did; the discovery test drops FOREMAN_NO_LOCAL_MODELS beside MOONS_EMBED since it serves its own fake Ollama; swept the full suite with local models hidden` → no findings [tree 56dba25d3391] (2026-11-05T18:16:12Z)
## Log
- 2026-11-05T17:29:52Z created
- 2026-11-05T17:44:44Z set tier=S
- 2026-11-05T17:44:46Z planned: it has criteria and steps
- 2026-11-05T17:44:48Z focused
- 2026-11-05T17:44:50Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T17:46:06Z paused: focus moved to T-3160
- 2026-11-05T17:48:57Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-05T17:48:57Z focused
- 2026-11-05T17:49:14Z paused: focus moved to T-3210
- 2026-11-05T18:13:11Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-05T18:13:11Z focused
- 2026-11-05T18:14:46Z sweep: FOREMAN_NO_LOCAL_MODELS=1 full suite, 6809 tests: 7 classes red; alone, only test_models.Profiles/LocalContext stay red, and they test discovery itself with their own fake servers, which the env var turns off (CI doesn't set it); the other 5 were load flakes at load 60 (green alone). Log: scratchpad closes/nolocal-sweep.log
- 2026-11-05T18:15:44Z set scope=['plugin/tests/test_moons_scale.py', 'CHANGELOG.md']
- 2026-11-05T18:16:54Z done
- 2026-11-05T18:16:58Z committed 98a29e7f (2 files)
- 2026-11-05T18:17:19Z guard authorization added: publish
- 2026-11-05T18:17:19Z ship: main pushes are standing-approved (2026-10-29: 'feel free to push to main at any time without asking me'); shipping the 274 commits main lacks so CI goes green
- 2026-11-05T18:40:18Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2969 [FIX M, blocked, 4 steps] CI on main is green again: test_moons_scale stops needing a live embedder (T-3002) and test_ui_replay's timeout kills claude's own child…
- T-3152 [FIX S, done, 2 steps] Moons' local-only fill names why no local model answered and tries the next local model (this box's GPU) before it stops — lesson: A sweep …
- T-2446 [FIX S, done, 1 steps] FIX: CI on main is red at 3581621 (tests) — lesson: A test that builds with a site package must skip where the interpreter the product runs…
- decision 2026-11-04: Moon bulk generation runs on jarvis (qwen3.8-27b) now that the user supplied LLM_API_KEY; Haiku stays the fallback. llama-swap serves no embeddings …
## Regression test
none separate: the fix is in the tests themselves (they leaked the box's Ollama embedders), so the start tree with the new tests is green by construction. Red before: FOREMAN_NO_LOCAL_MODELS=1 run.py test_moons_scale failed 11 classes on the committed test file (and 2 on origin/main, matching CI's Families/Promote); green after, with and without local models.
## Why not caught
no local gate runs tests with local models hidden; T-3229 adds that
## Lessons
- a test that mocks a picker's fallback but not the picker itself passes only on boxes with the real thing: run model tests with FOREMAN_NO_LOCAL_MODELS=1 before landing
## Files touched
- plugin/tests/test_moons_scale.py
- CHANGELOG.md
