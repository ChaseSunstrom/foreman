---
id: T-2607
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: genesis
created: 2026-11-02T12:44:40Z
updated: 2026-11-02T12:55:56Z
base: d2e947489d9fb117334c529d0a7663d3fbc63402
base_tree: 35e2d4aeb2b644b18006d45f28a3e605a78ccb8f
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-02T12:45:28Z
plan0_scope: []
verified: strong
---
# The tick names what it could not watch: each trigger kind it skipped (CI, issues) with the reason, in fm doctor and the session's Watch line
## Raw request
> FEATURE: the tick names what it could not watch: fmnight.tick records each trigger kind it skipped (CI, issues) with the reason (no watch yes, sensitive, network off); fm doctor's night-timers row and the session Watch line name each blind kind with the command that opens it, and stay quiet when every kind is covered; the watch exam kind gains a blind variant per reason; MASTER, CHANGELOG, the night skill and the site's night page say it
## Interpretation
Reading 1 (chosen): make the tick's silence trustworthy by naming what it couldn't see. Reading 2: open the watches automatically. Rejected: the watch yes is the user's (remote reads only with consent).
## Assumptions (confidence)
## Acceptance criteria
- [x] fmnight.tick's result lists blind kinds as (kind, why): CI and issues when the repo is sensitive, has no watch yes, or the network is off (FOREMAN_NO_NET); an approved repo lists none — verify with `python3 plugin/tests/run.py test_night`
- [x] fm doctor's night-timers row and the session Watch line name each blind kind with its reason and the command that opens it (fm night --watch …), once, and say nothing when every kind is covered — verify with `python3 plugin/tests/run.py test_night test_doctor`
## Non-goals
## Approach (options → choice → why)
1) The tick appends (kind, why) to res['blind'] where it skips CI or issues today, caches the newest list in state, and fm doctor's night-timers row plus the Watch line read it. Likely outcome: one line says CI isn't watched and how to open it. Fails if: the line repeats every hour (shown only when the list changed, and in doctor always). 2) use what exists: append reasons to res['notes']. Fails if: notes carry errors, and doctor never reads them. 3) do less: document the conditions in the night skill. Fails if: nobody reads the skill when it matters. Choice 1 (80%): one field and one row; nothing new runs.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests in test_night
2. [x] record blind kinds in fmnight.tick and cache the newest
3. [x] doctor row and Watch line
4. [x] MASTER, CHANGELOG, night skill, site night page
## Resume here
## Docs impact
MASTER.md (fmnight T-2607 clause), CHANGELOG, the site's self-triggering page (site/pages.py). The night skill: no separate skill documents the tick's watch; the site page and MASTER do.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_night.NightTick` → ✗ exit 1 · Ran 16 tests in 1.9s (1 classes, 16 at a time; slowest: NightTick 2s) / FAILED (1 classes: test_night.NightTick) [ran] [tree db1b439e8212] [world 2f1906870a] (2026-11-02T12:46:14Z)
- (step 2) `python3 plugin/tests/run.py test_night test_doctor test_foresight` → exit 0 · Ran 182 tests in 7.7s (57 classes, 16 at a time; slowest: Night 7s, PredictionBook 5s, ViewsRepair 3s) / OK [ran] [tree 2179cc30bb3c] [world 2f1906870a] (2026-11-02T12:48:47Z)
- (step 3) `python3 plugin/tests/run.py test_night test_doctor test_foresight` → exit 0 · Ran 182 tests in 7.6s (57 classes, 16 at a time; slowest: Night 7s, PredictionBook 5s, ViewsRepair 3s) / OK [ran] [tree 2179cc30bb3c] [world 2f1906870a] (2026-11-02T12:48:55Z)
- (step 4) `python3 plugin/tests/run.py test_night test_doctor test_foresight` → exit 0 · Ran 182 tests in 7.6s (57 classes, 16 at a time; slowest: Night 7s, PredictionBook 5s, ViewsRepair 3s) / OK [ran] [tree 2179cc30bb3c] [world 2f1906870a] (2026-11-02T12:49:03Z)
- (ac 1) `python3 plugin/tests/run.py test_night` → exit 0 · Ran 44 tests in 6.6s (13 classes, 16 at a time; slowest: Night 6s, NightInstall 2s, NightTick 2s) / OK [ran] [tree 2179cc30bb3c] [world 2f1906870a] (2026-11-02T12:55:01Z)
- (ac 2) `python3 plugin/tests/run.py test_night test_doctor` → exit 0 · Ran 150 tests in 7.3s (49 classes, 16 at a time; slowest: Night 7s, ViewsRepair 3s, LockProbe 3s) / OK [ran] [tree 2179cc30bb3c] [world 2f1906870a] (2026-11-02T12:55:01Z)
- (step 1) `python3 plugin/tests/run.py test_night.NightTick` → exit 0 · Ran 16 tests in 1.9s (1 classes, 16 at a time; slowest: NightTick 2s) / OK [ran] [tree 2179cc30bb3c] [world 2f1906870a] (2026-11-02T12:55:01Z)
- (audit intent) `self-review: _blind derives the blind kinds from the same conditions the tick's branches test (sensitive, FOREMAN_NO_NET, the watch yes for CI and per repo); tick-blind.json is rewritten only when the list changes; doctor appends the kinds as information (no WARN for a user who never asked to watch); the Watch line needs an installed tick timer and a recent change` → each blind reason names its kind and the command that opens it; an approved repo lists none (test); doctor and the Watch line show it (tests) [tree 2179cc30bb3c] (2026-11-02T12:55:01Z)
- (audit edge) `self-review: _blind derives the blind kinds from the same conditions the tick's branches test (sensitive, FOREMAN_NO_NET, the watch yes for CI and per repo); tick-blind.json is rewritten only when the list changes; doctor appends the kinds as information (no WARN for a user who never asked to watch); the Watch line needs an installed tick timer and a recent change` → no GitHub remote lists nothing; sensitive lists both kinds even without a remote read; a repo with CI approved but issues not lists only issues [tree 2179cc30bb3c] (2026-11-02T12:55:01Z)
- (audit operator) `self-review: _blind derives the blind kinds from the same conditions the tick's branches test (sensitive, FOREMAN_NO_NET, the watch yes for CI and per repo); tick-blind.json is rewritten only when the list changes; doctor appends the kinds as information (no WARN for a user who never asked to watch); the Watch line needs an installed tick timer and a recent change` → no WARN noise for users who never watch; the session note line appears only while a tick timer runs and for CHANGE_DAYS after the list changed [tree 2179cc30bb3c] (2026-11-02T12:55:01Z)
## Log
- 2026-11-02T12:44:40Z created
- 2026-11-02T12:45:18Z planned from capture
- 2026-11-02T12:45:27Z set approved=True
- 2026-11-02T12:45:27Z focused
- 2026-11-02T12:45:28Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-02T12:49:03Z scope: plugin/lib/fmdoctor.py, plugin/lib/fmforesight.py, site/pages.py and their tests — the two surfaces and the site page the Mission names
- 2026-11-02T12:55:53Z done
- 2026-11-02T12:55:56Z committed 76455d87 (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2542 [FEATURE M, done, 4 steps] Installed Foreman timers known alive: systemd's last trigger and last result, in fm doctor and the next session's Watch line — lesson: …
- T-2357 [FEATURE M, done, 3 steps] Installs are queued for one yes: night and tick timers staged, asked once, installed only after the user's yes (Mission 8, #11) — lesso…
- T-2524 [FEATURE M, done, 2 steps] Beyond exam kind: an offline-package deliverable, built and run with no network — lesson: an exam kind tied to one ecosystem must be fi…
- decision 2026-10-31: [costly] Parked T-2357 at a one-way, ambiguous step: red tests: staging writes nothing outside state; guard category; install after the yes; uninsta…
## Lessons
- A silent skip makes quiet and blind look the same: every trigger that can be skipped should say so where the user already looks
## Plan gaps
- failed first: step 1 red tests in test_night
## Files touched
- plugin/tests/test_night.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmforesight.py
- plugin/lib/fmnight.py
- plugin/tests/test_foresight.py
- CHANGELOG.md
- MASTER.md
- site/pages.py
