---
id: T-1716
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmmotion.py, plugin/tests/test_motion_verify.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T01:47:38Z
updated: 2026-10-23T12:35:43Z
base: e3714c7e911d9be6f66b29251c1ad3b8dbb25b59
base_tree: ee90a1e5d33ab1fb1008fdc77dc0be5d40649728
plan0_at: 2026-10-23T12:34:40Z
plan0_scope: [plugin/lib/fmmotion.py, plugin/tests/test_motion_verify.py, CHANGELOG.md]
verified: strong
---
# Fm motion verify: sample through fmshot.Browser (no Playwright, one page) instead of the w
## Raw request
> fm motion verify: sample through fmshot.Browser (no Playwright, one page) instead of the whole frozen smoke crawl; see fmmotion.sample's docstring (from T-1627)
## Interpretation
fm motion verify samples the page in fm shot's browser (no Playwright, one page) instead of fm smoke's whole frozen crawl: the frozen profile's script before load, then smoke_web.cjs's own sampleMotion evaluated in the page; with no browser, the score alone is checked and why is said, as before.
## Assumptions (confidence)
## Acceptance criteria
- [x] verify samples a served page in fm shot's browser with Playwright unset, and with no browser says so and checks the score — verify with `python3 plugin/tests/run.py test_motion_verify`
## Non-goals
## Approach (options → choice → why)
Options: (1) fmshot.Browser + FREEZE + Runtime.evaluate of sampleMotion's source read from smoke_web.cjs (chosen: one sampler, no Playwright, the path fmmotion.sample's docstring already named); (2) keep the crawl and add the browser as a fallback (rejected: two paths to keep in step, and the crawl needs Playwright); (3) port sampleMotion to Python over CDP calls (rejected: a second copy of the sampler).
## Risks and rollback
## Execution prompt
## Steps
1. [x] one page in fm shot's browser, test first
## Resume here
## Docs impact
CHANGELOG line; fm motion verify's help names no browser; the motion playbook says fm motion verify samples the page, which still holds.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_motion_verify` → ✗ exit 1 · Ran 14 tests in 1.6s (2 classes, 16 at a time; slowest: Sample 1s, Afterglow 0s) / FAILED (1 classes) [ran] [tree 0b4529902081] (2026-10-23T12:34:43Z)
- (step 1) `python3 plugin/tests/run.py test_motion_verify test_smoke test_fmshot test_cli` → exit 0 · Ran 196 tests in 23.8s (46 classes, 16 at a time; slowest: TaskLifecycle 24s, Diff 23s, Capture 11s) / OK [ran] [tree e306a5479519] (2026-10-23T12:35:24Z)
- (ac 1) `python3 plugin/tests/run.py test_motion_verify` → exit 0 · Ran 14 tests in 2.3s (2 classes, 16 at a time; slowest: Sample 2s, Afterglow 0s) / OK [ran] [tree e306a5479519] (2026-10-23T12:35:34Z)
- (ac 1) `python3 plugin/tests/run.py test_motion_verify` → exit 0 · Ran 14 tests in 2.3s (2 classes, 16 at a time; slowest: Sample 2s, Afterglow 0s) / OK [ran] [tree e306a5479519] (2026-10-23T12:35:37Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): the sampler's source is read from smoke_web.cjs, so fm smoke and verify run one copy; the browser gets fm shot's FREEZE before load as fm shot --frozen does; every exit path closes the browser; the page's returned value is checked for shape before use` → verify needs no Playwright any more: any Chromium fm shot finds samples the page, one page instead of a whole crawl [tree e306a5479519] (2026-10-23T12:35:37Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): the sampler's source is read from smoke_web.cjs, so fm smoke and verify run one copy; the browser gets fm shot's FREEZE before load as fm shot --frozen does; every exit path closes the browser; the page's returned value is checked for shape before use` → no browser anywhere says fm shot's own message and checks the score alone; a browser that won't start, a page that won't load or a sampler that throws is said with the score still checked; a hostile page's returned samples are filtered to objects and its notes cut to 300 characters [tree e306a5479519] (2026-10-23T12:35:37Z)
## Log
- 2026-10-23T01:47:38Z created
- 2026-10-23T12:34:35Z set tier=M, scope=['plugin/lib/fmmotion.py', 'plugin/tests/test_motion_verify.py', 'CHANGELOG.md']
- 2026-10-23T12:34:39Z focused
- 2026-10-23T12:35:41Z done
- 2026-10-23T12:35:43Z committed 5a69ae52 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1627 [FEATURE M, done, 3 steps] Motion verification: frames sampled under the frozen-time smoke profile asserted against the score within tolerance — lesson: Verifying…
- T-1636 [FEATURE M, done, 3 steps] fm shot: viewport and frame captures and a poster frame per animated page, or a stated reason without a browser — lesson: Headless Chro…
- research T-1509-review: Verdict: changes needed.** The default gate failure (finding 1) and the untested exit-code fix (finding 2) block approval. The rest are nits. [st…
- decision 2026-10-23: T-1623: the five UI contract rules are written down from what the UI playbooks already require: motion (reduced motion as its own path), contrast (p…
## Preflight
Changed in scope since this was planned (2026-10-23): CHANGELOG.md, plugin/lib/fmmotion.py, plugin/tests/test_motion_verify.py; re-ground the plan against them before editing
## Lessons
- When two tools need the same in-page logic, read one source file into both rather than porting it
## Plan gaps
- failed first: step 1 one page in fm shot's browser, test first
## Files touched
- plugin/tests/test_motion_verify.py
- CHANGELOG.md
- plugin/lib/fmmotion.py
