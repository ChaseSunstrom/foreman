---
id: T-2997
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: [T-2998, T-2999]
source: user
created: 2026-11-04T18:26:16Z
updated: 2026-11-04T20:57:27Z
base: 881e863554f21fa00e09e35fddfdf98b181d47f6
verified: strong
---
# A live local website of everything Sampo is doing: the session, builders, jobs, local and cloud models, the GPU, animated flows between them, in the Sampo forge theme, always running
## Raw request
> can you create a local website I can view that is constantly running showing everything youre doing, local models, visualizations (aniamtions between things like models and such), etc.? matching the Sampo theme?
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo live serves the page on 127.0.0.1 with a live snapshot and stream; the page shows focus, queue, lanes, jobs, models, GPU and animated flows in the forge theme — verify with `python3 plugin/tests/run.py test_live`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-2998 server and data feed
2. [x] T-2999 the page
3. [x] run it always on; a screenshot review against the design taste
## Resume here
## Docs impact
CHANGELOG, MASTER.md, files-1, files-lib-2
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_live` → exit 0 · Ran 35 tests in 15.0s (9 classes, 16 at a time; slowest: Page 14s, Serve 7s, Snapshot 3s) / OK [ran] [tree fd07607d8e5d] [world 2f1906870a] (2026-11-04T20:56:25Z)
- (step 2) `python3 plugin/tests/run.py test_live_page` → exit 0 · Ran 11 tests in 14.8s (2 classes, 16 at a time; slowest: Page 14s, Files 0s) / OK [ran] [tree fd07607d8e5d] [world 2f1906870a] (2026-11-04T20:56:40Z)
- (step 3) `systemctl --user is-active sampo-live && sampo shot http://127.0.0.1:46459/?t=4sEOUz-UfshwURIhb7sNkcBs8SPuhemBnmNrtpNXQ2Y --frames 2 --every 1500 --out /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/live-shots8` → exit 0 · frame-00.png … frame-01.png (2 frames 1500 ms apart, real time) / poster.png (frame-00.png: the most painted of 2) [ran] [tree fd07607d8e5d] [world 2f1906870a] (2026-11-04T20:56:48Z)
- (ac 1) `python3 plugin/tests/run.py test_live` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T20:56:25Z [ran] [tree fd07607d8e5d] [world 2f1906870a] (2026-11-04T20:56:56Z)
- (audit intent) `rolled up from its children's audits: T-2998 (server, via T-3014's review), T-2999 (page, fm-reviewer with the design lens), T-3014 (live-data fixes, fm-reviewer), T-3020 (always-on unit); my screenshot review on fixtures and on live data against the design taste` → a constantly running local page of everything Sampo does, models and animated flows between them, in the forge theme: met, served by the sampo-live user service at 127.0.0.1:46459 [tree fd07607d8e5d] (2026-11-04T20:56:56Z)
- (audit adversary) `rolled up from its children's audits: T-2998 (server, via T-3014's review), T-2999 (page, fm-reviewer with the design lens), T-3014 (live-data fixes, fm-reviewer), T-3020 (always-on unit); my screenshot review on fixtures and on live data against the design taste` → loopback only, one-time token to cookie, Host check, CSP with nonces, textContent only, flat static names [tree fd07607d8e5d] (2026-11-04T20:56:56Z)
- (audit edge) `rolled up from its children's audits: T-2998 (server, via T-3014's review), T-2999 (page, fm-reviewer with the design lens), T-3014 (live-data fixes, fm-reviewer), T-3020 (always-on unit); my screenshot review on fixtures and on live data against the design taste` → failing collectors leave fields empty; reconnect backs off and resets its clock; a restart issues a new link [tree fd07607d8e5d] (2026-11-04T20:56:56Z)
- (audit operator) `rolled up from its children's audits: T-2998 (server, via T-3014's review), T-2999 (page, fm-reviewer with the design lens), T-3014 (live-data fixes, fm-reviewer), T-3020 (always-on unit); my screenshot review on fixtures and on live data against the design taste` → no model cost; one small append per model call; snapshot cached and shared; idle frame cap pending in T-3019 [tree fd07607d8e5d] (2026-11-04T20:56:56Z)
- (audit maintainer) `rolled up from its children's audits: T-2998 (server, via T-3014's review), T-2999 (page, fm-reviewer with the design lens), T-3014 (live-data fixes, fm-reviewer), T-3020 (always-on unit); my screenshot review on fixtures and on live data against the design taste` → test_live (35) and test_live_page (11) pin the server, data feed and page [tree fd07607d8e5d] (2026-11-04T20:56:56Z)
## Log
- 2026-11-04T18:26:16Z created
- 2026-11-04T18:26:50Z set depends_on=['T-2998', 'T-2999'], approved=True
- 2026-11-04T20:55:13Z guard authorization added: system
- 2026-11-04T20:56:25Z start point recorded late (no focus had kept one): its diff starts at 881e863
- 2026-11-04T20:57:27Z done
## Follow-ups captured
## Build vs reuse
Reuses settingsserve's local-only auth (one-time token, cookie, Host check, CSP), core's briefs and ledger, moonscale and smallcards status, louhi's bench rows, models.json profiles, and site/forge.css's theme; nothing existing serves a live web view (sampo watch is a terminal dashboard, sampo ui --json a pane view model).
## Lessons
- An always-on view of the system is only done when it runs supervised on real data; fixtures hid three gaps
## Files touched
- plugin/lib/sampo/jeffexport.py
- plugin/tests/test_jeff_export.py
