---
id: T-0420
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T13:45:42Z
updated: 2026-10-09T13:57:43Z
base: 59aa18b11f67a75fa8b6ca696b52507433e953c0
base_tree: 11c86366c4c242a367e8d71396a3081caef87604
verified: strong
---
# fm smoke: a page that stops responding can't hang the crawl
## Raw request
> fm smoke: a page that stops responding can't hang the crawl
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the crawl script prints its partial result and exits when a view hangs, naming the view — verify with `python3 plugin/tests/run.py -k test_smoke`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] watchdog per view (30 s) and overall (215 s), partial JSON always printed
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `ssh -o BatchMode=yes <host> 'cd /tmp/fmsmoke-red && FOREMAN_PLAYWRIGHT=/opt/jarvis/jarvis-web/node_modules/playwright python3 plugin/tests/run.py -k test_smoke_survives'` → ✗ exit 1 · Ran 1 tests in 240.7s (1 classes, 10 at a time; slowest: SmokeInABrowser 240s) / FAILED (1 classes) [ran] [tree 924715d830a8] (2026-10-09T13:56:07Z)
- (step 1) `ssh -o BatchMode=yes <host> 'cd /tmp/fmsmoke-test && FOREMAN_PLAYWRIGHT=/opt/jarvis/jarvis-web/node_modules/playwright python3 plugin/tests/run.py -p test_smoke.py'` → exit 0 · Ran 9 tests in 75.2s (2 classes, 10 at a time; slowest: SmokeInABrowser 75s, Smoke 2s) / OK [ran] [tree 924715d830a8] (2026-10-09T13:57:23Z)
- (ac 1) `python3 plugin/tests/run.py -k test_smoke` → exit 0 · Ran 9 tests in 1.4s (2 classes, 16 at a time; slowest: Smoke 1s, SmokeInABrowser 0s) / OK [ran] [tree f571cc52c5ec] (2026-10-09T13:57:37Z)
- (audit edge) `self: diff read; per-view 30 s race, per-viewport share of the deadline, a process-level timer that prints and exits; a frozen renderer's context is closed without waiting; red (old script: 240.7 s, FAILED) then green (9 tests OK) on JARVIS's real browser` → a hang in the start view, a tab, or a nav page all land in the same catch; the phone viewport still runs in a fresh renderer after a desktop hang (the test sees both) [tree f571cc52c5ec] (2026-10-09T13:57:37Z)
- (audit self) `self: diff read; per-view 30 s race, per-viewport share of the deadline, a process-level timer that prints and exits; a frozen renderer's context is closed without waiting; red (old script: 240.7 s, FAILED) then green (9 tests OK) on JARVIS's real browser` → no findings [tree f571cc52c5ec] (2026-10-09T13:57:37Z)
- (audit edge) `self: diff read; per-view 30 s race, per-viewport share of the deadline, a process-level timer that prints and exits; a frozen renderer's context is closed without waiting; red then green on JARVIS's real browser` → a hang in the start view, a tab, or a nav page all land in the same catch; the phone viewport still runs in a fresh renderer after a desktop hang [tree f571cc52c5ec] (2026-10-09T13:57:43Z)
- (audit self) `self: diff read; per-view 30 s race, per-viewport share of the deadline, a process-level timer that prints and exits; a frozen renderer's context is closed without waiting; red then green on JARVIS's real browser` → no findings [tree f571cc52c5ec] (2026-10-09T13:57:43Z)
## Log
- 2026-10-09T13:45:42Z created
- 2026-10-09T13:45:43Z focused
- 2026-10-09T13:57:43Z done
- 2026-10-09T13:57:43Z committed d4d8dff (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0417-review: Changes needed. The placeholder selector and the alert rule will flag healthy apps. A permanent spinner can also make the crawl hit its timeout a…
- research T-0206-review: Verdict: changes needed.** There is one MEDIUM robustness bug and two LOWs. I found no HIGH SSRF hole. I traced this by reading the code and did …
- research smoke-tomllib: Asked 2026-10-04 · 1 sub-question(s) · 8 claims: 7 quote found, 1 quote not found, 0 unchecked. ✓ means the quoted words are on the cited page, n…
- playbook Test-Driven Development Workflow (skills/playbooks/references/verify/tdd-workflow.md)
## Regression test
test_smoke.SmokeInABrowser.test_smoke_survives_a_page_that_stops_responding: it needs a real browser, so it ran on JARVIS — failing with the pre-fix script (HEAD's smoke_web.cjs in /tmp/fmsmoke-red: 240.7 s, FAILED, recorded) and passing with the fix (/tmp/fmsmoke-test: 9 tests OK, recorded); two folders, so two command strings
## Lessons
- Any crawl of someone else's page needs a watchdog outside the page: in-page calls have no timeout of their own.
## Files touched
- plugin/tests/test_smoke.py
- plugin/lib/smoke_web.cjs
- CHANGELOG.md
