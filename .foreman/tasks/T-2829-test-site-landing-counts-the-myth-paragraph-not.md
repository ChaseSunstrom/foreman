---
id: T-2829
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-03T18:38:58Z
updated: 2026-11-03T18:45:13Z
base: aa1fc81e5707133d6c3929c51633c9fdf6eea0c8
base_tree: 07445d19b39c6dd3938f6c5f1a72cdd9965cd383
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-03T18:43:44Z
plan0_scope: []
verified: ok
---
# test_site_landing counts the myth paragraph, not every Ilmarinen: the decisions page shows real fm decide rows that name Ilmarinen's forge, so the ship's scratch-tree build failed
## Raw request
> test_site_landing counts the myth paragraph, not every Ilmarinen: the decisions page shows real fm decide rows that name Ilmarinen's forge, so the ship's scratch-tree build failed
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the myth paragraph is told once, on the landing page only, while other pages may name Ilmarinen in data — verify with `python3 plugin/tests/run.py test_site_landing`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red: a decisions row naming Ilmarinen fails the current test; then match the paragraph's own sentence
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_site_landing` → exit 0 · Ran 8 tests in 4.6s (1 classes, 16 at a time; slowest: Landing 4s) / OK [ran] [tree 3efa9dbd1f8c] [world 2f1906870a] (2026-11-03T18:44:48Z)
- (step 1) `python3 plugin/tests/run.py test_site_landing` → exit 0 · Ran 8 tests in 4.6s (1 classes, 16 at a time; slowest: Landing 4s) / OK [ran] [tree 3efa9dbd1f8c] [world 2f1906870a] (2026-11-03T18:44:48Z)
- (audit self) `self: the count keys on the paragraph's own sentence, so decision rows quoting the name no longer trip it; the fixture's injected row keeps the case red-provable on any stats.json; the paragraph-contents check below it still asserts every myth name` → no findings [tree 3efa9dbd1f8c] (2026-11-03T18:44:48Z)
## Log
- 2026-11-03T18:38:58Z created
- 2026-11-03T18:43:43Z focused
- 2026-11-03T18:43:44Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-03T18:45:05Z done
- 2026-11-03T18:45:13Z committed adf706a5 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2759 [FEATURE M, done, 4 steps] The landing page in the forge world (T-2742 step 7b): a hero where the Sampo mill turns and runes write themselves into the headline ov…
- T-2788 [FEATURE L, planned, 6 steps] Sampo's site and logo rebuilt in the Kirjokansi direction fused with Ilmarinen's forge (T-2772 pick): the astrolabe mark and every v…
- T-2760 [FEATURE M, done, 3 steps] README and INSTALL say Sampo (T-2742 step 8a): the Runestone README header (dark and light), every Foreman name and command in the Samp…
- decision 2026-11-03: [outward] [cites: user steer 2026-11-03: picked 1 Kirjokansi, then 'I like both 1 and 2'] Sampo's look is Kirjokansi fused with Ilmarinen's forge: t…
## Regression test
none: the fix is in the test itself. The fixture now injects a decision row naming Ilmarinen; with the old bare-word count test_site_landing failed (observed red 2026-11-03 before the count changed), green after.
## Why not caught
none: the committed stats.json had no decision naming Ilmarinen; only the scratch tree's refreshed stats did
## Files touched
- plugin/tests/test_site_landing.py
