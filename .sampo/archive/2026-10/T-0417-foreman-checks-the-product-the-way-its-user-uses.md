---
id: T-0417
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T13:23:25Z
updated: 2026-10-09T13:39:19Z
base: 4ca8609aac5a8beb53bc5ac88632f8171583c469
base_tree: 308b1d7118e5eb96d16b7b33e95279836fb405bd
verified: ok
---
# Foreman checks the product the way its user uses it
## Raw request
> Foreman checks the product the way its user uses it
## Interpretation
The user: "foreman should be able to find these issues and stuff itself, why was this never caught and fixed automatically?" JARVIS closed 34 tasks with unit tests and CI green while its web UI had two panels that never loaded, an error toast on every load, and overlaps at phone width; and it idled 10–46 min at a time with drive_wait logged but never acted on. Foreman's evidence accepts any passing command and nothing exercises the running product; idle time is recorded but nothing turns it into work.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm smoke on a page whose panel never loads, logs a console error or overflows at 390px fails and names each defect; on a healthy page passes — verify with `python3 plugin/tests/run.py -k test_smoke`
- [x] fm check runs fm smoke when one is set — verify with `python3 plugin/tests/run.py -k test_check_runs_smoke`
- [x] a drained queue in full autonomy gets one product-check push — verify with `python3 plugin/tests/run.py -k test_drained_queue_checks_the_product`
## Non-goals
## Approach (options → choice → why)
Complete version: (1) fm smoke — a product check Foreman runs: for a web UI, a bundled headless-browser crawl (the project's Playwright, else none with a clear note) of every tab/route at desktop and phone width that fails on loading placeholders still visible after 5 s, console/page errors, failed or 4xx/5xx requests, horizontal overflow and covered controls, with screenshots kept for review; for an HTTP API, its health routes; set once with fm smoke set <kind> <url>; (2) fm check runs fm smoke as a gate when set, so every task close checks the real product; fm doctor nudges a project with a UI surface and no smoke; (3) a drained queue in full autonomy is not the end: the drive pushes one product check and capture pass; (4) idle accounting: fm doctor and fm friction report the session's long waits, and a wait over 15 min with work queued is captured as friction automatically. Options: (A, chosen) a generic runner + per-project config, reusing fmmission.surfaces to detect the UI; (B, rejected) guidance only (tell the agent to write smoke tests): JARVIS shows it doesn't happen unprompted; (C, rejected) rely on CI: CI was green throughout.
## Risks and rollback
## Execution prompt
## Steps
1. [x] plan: grounding (fmmission.surfaces, gates config, playwright availability), self-approve
2. [x] drained-queue push in the drive (builder lane)
3. [x] fm smoke web crawl + set/config + tests (test-first with a local fixture page)
4. [x] fm check gate + doctor nudge; idle accounting in fm friction
5. [x] gate, changelog, ship; set JARVIS's smoke
## Resume here
## Docs impact
CHANGELOG entry; MASTER.md lib map (fmsmoke + smoke_web.cjs)
## Verification evidence
- (step 2) `python3 plugin/tests/run.py -p test_hooks.py` → exit 0 · Ran 130 tests in 18.3s (18 classes, 16 at a time; slowest: Stop 18s, Approvals 10s, SessionStart 9s) / OK [ran] [tree 063482dc8a22] (2026-10-09T13:27:06Z)
- (step 3) `python3 plugin/tests/run.py -p test_smoke.py` → exit 0 · Ran 8 tests in 1.4s (2 classes, 16 at a time; slowest: Smoke 1s, SmokeInABrowser 0s) / OK [ran] [tree 7eb62ec9fb28] (2026-10-09T13:31:51Z)
- (step 3) `ssh -o BatchMode=yes <host> 'cd /tmp/fmsmoke-test && FOREMAN_PLAYWRIGHT=/opt/jarvis/jarvis-web/node_modules/playwright python3 plugin/tests/run.py -p test_smoke.py'` → exit 0 · Ran 8 tests in 13.3s (2 classes, 10 at a time; slowest: SmokeInABrowser 13s, Smoke 2s) / OK [ran] [tree 7eb62ec9fb28] (2026-10-09T13:32:05Z)
- (step 4) `python3 plugin/tests/run.py -p test_doctor.py -p test_smoke.py` → exit 0 · Ran 32 tests in 5.9s (8 classes, 16 at a time; slowest: Command 6s, Smoke 1s, RestoreState 0s) / OK [ran] [tree 7eb62ec9fb28] (2026-10-09T13:32:11Z)
- (step 1) `grounding` → fmmission.surfaces detects the web UI; gates are meta checks (fm check add); JARVIS has Playwright in jarvis-web/node_modules and no fm checks at all; approach A self-approved [tree 7eb62ec9fb28] (2026-10-09T13:32:17Z)
- (step 5) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (28 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.2    33.6     150  [0] / SessionEnd                  30.1    31.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 13:13 UTC; python3 plugin/tests/run.py → exit 0 · Ran 963 tests in [ran] [tree 7eb62ec9fb28] (2026-10-09T13:33:29Z)
- (step 3) `ssh -o BatchMode=yes <host> 'cd /tmp/fmsmoke-test && FOREMAN_PLAYWRIGHT=/opt/jarvis/jarvis-web/node_modules/playwright python3 plugin/tests/run.py -p test_smoke.py'` → exit 0 · Ran 8 tests in 14.3s (2 classes, 10 at a time; slowest: SmokeInABrowser 14s, Smoke 2s) / OK [ran] [tree e445df08dd10] (2026-10-09T13:37:42Z)
- (step 2) `python3 plugin/tests/run.py -p test_hooks.py` → exit 0 · Ran 130 tests in 18.7s (18 classes, 16 at a time; slowest: Stop 19s, Approvals 10s, SessionStart 9s) / OK [ran] [tree e445df08dd10] (2026-10-09T13:38:01Z)
- (step 5) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (28 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.4    34.7     150  [0] / SessionEnd                  29.5    31.7     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 13:13 UTC; python3 plugin/tests/run.py → exit 0 · Ran 963 tests in [ran] [tree e445df08dd10] (2026-10-09T13:39:06Z)
- (ac 1) `python3 plugin/tests/run.py -k test_smoke` → exit 0 · Ran 8 tests in 1.5s (2 classes, 16 at a time; slowest: Smoke 1s, SmokeInABrowser 0s) / OK [ran] [tree e445df08dd10] (2026-10-09T13:39:18Z)
- (ac 2) `python3 plugin/tests/run.py -k test_check_runs_smoke` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Smoke 1s) / OK [ran] [tree e445df08dd10] (2026-10-09T13:39:18Z)
- (ac 3) `python3 plugin/tests/run.py -k test_drained_queue_checks_the_product` → exit 0 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree e445df08dd10] (2026-10-09T13:39:18Z)
- (audit intent) `self + one fm-reviewer pass (research T-0417-review: 1 high, 8 medium, 5 low); every finding fixed and re-verified (browser rows on JARVIS for the false positives and nav fallback; hooks rows for the drive); full gate exit 0; live run on JARVIS matches what a user sees` → the user's question — why wasn't this caught — is answered by a gate that opens the real page: its first live run found JARVIS's stuck panel, mic error toast and a 502; after JARVIS's fix it shows only the toast [tree e445df08dd10] (2026-10-09T13:39:18Z)
- (audit adversary) `self + one fm-reviewer pass (research T-0417-review: 1 high, 8 medium, 5 low); every finding fixed and re-verified (browser rows on JARVIS for the false positives and nav fallback; hooks rows for the drive); full gate exit 0; live run on JARVIS matches what a user sees` → FOREMAN_SMOKE_RUNNER only for a Foreman home in a temp folder (can't forge a gate); page text stripped of control characters and capped; FOREMAN_PLAYWRIGHT is environment-level, as any require [tree e445df08dd10] (2026-10-09T13:39:18Z)
- (audit edge) `self + one fm-reviewer pass (research T-0417-review: 1 high, 8 medium, 5 low); every finding fixed and re-verified (browser rows on JARVIS for the false positives and nav fallback; hooks rows for the drive); full gate exit 0; live run on JARVIS matches what a user sees` → no Playwright → skipped with a note (lanes, other machines); server down → defect + 'start it or fm smoke set off'; 200 s deadline prints partial results; apps without tabs → nav links or a note; Tailwind placeholder:, clipped announcers, sticky headers → no false positive (tested) [tree e445df08dd10] (2026-10-09T13:39:18Z)
- (audit operator) `self + one fm-reviewer pass (research T-0417-review: 1 high, 8 medium, 5 low); every finding fixed and re-verified (browser rows on JARVIS for the false positives and nav fallback; hooks rows for the drive); full gate exit 0; live run on JARVIS matches what a user sees` → fm smoke set web URL / set off WHY; screenshots of the last 3 runs; doctor WARN for a web UI without a check [tree e445df08dd10] (2026-10-09T13:39:18Z)
- (audit maintainer) `self + one fm-reviewer pass (research T-0417-review: 1 high, 8 medium, 5 low); every finding fixed and re-verified (browser rows on JARVIS for the false positives and nav fallback; hooks rows for the drive); full gate exit 0; live run on JARVIS matches what a user sees` → one Python module, one crawl script, no new dependency (the project's own Playwright); the drive's two drained pushes share one marker [tree e445df08dd10] (2026-10-09T13:39:18Z)
## Log
- 2026-10-09T13:23:25Z created
- 2026-10-09T13:24:36Z focused
- 2026-10-09T13:26:47Z step 2: drained-queue push done (keyed on the number of briefs, so a task made and closed in one turn re-arms it; skipped when what's left waits on the user, as test_full_autonomy_skips… requires); hooks suite OK
- 2026-10-09T13:31:49Z set approved=True
- 2026-10-09T13:37:27Z review (research T-0417-review): fixed — Tailwind placeholder:/spinner false positives (selector now aria-busy, skeleton, shimmer, loading on non-controls), clipped role=alert announcers, sticky/dialog overlaps (fixed-only, outside dialogs), other-port API errors (any port on the app's host, 5xx anywhere), apps without tabs (nav links, or a note), the 240 s timeout losing all results (200 s deadline, partial output), no Playwright blocking fm check (skipped with a note), .claude relpath, the drive's smoke mention when off, FOREMAN_SMOKE_RUNNER forging a gate (temp homes only), page text sanitized, drained push only after a worked turn and within DRIVE_MAX; also the wait-branch product push once per drain, not per job set. Live JARVIS rerun: the panels JARVIS fixed at 6157e37b no longer show, the mic alert does
- 2026-10-09T13:39:19Z done
- 2026-10-09T13:39:19Z committed 4f5e714 (9 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0415 [FIX M, done, 3 steps] Drive: long-lived jobs and an empty queue never leave a session idle — lesson: A wait rule keyed on 'anything running' breaks when somethin…
- T-0364 [FIX L, done, 5 steps] Foreman keeps working while background jobs run, plans and brainstorms wider, uses subagents — lesson: Read the user's transcripts before t…
- T-0401 [FIX M, done, 3 steps] Drive: while background work runs, name a concrete queued task to start (builder lane / plan / block), offer up to 3 in turn, then wait — J…
- decision 2026-09-26: T-0014 permission mode: fm serve passes --permission-mode only when given; otherwise Remote Control uses the user's own defaultMode (bypass here, se…
## Lessons
- Green tests prove the code agrees with itself; only opening the product proves the user can use it — make that a gate, or it never happens.
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- plugin/tests/test_smoke.py
- plugin/lib/fmsmoke.py
- plugin/lib/smoke_web.cjs
- plugin/lib/fmcli.py
- plugin/lib/fmdoctor.py
- MASTER.md
- CHANGELOG.md
