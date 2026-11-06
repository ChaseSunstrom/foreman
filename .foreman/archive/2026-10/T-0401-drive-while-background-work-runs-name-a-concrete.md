---
id: T-0401
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T03:57:17Z
updated: 2026-10-09T04:00:39Z
base: d17133227f3fbc2f4bdf1cae1b43a8600301b10b
base_tree: e07045952de86d019f91040bf037443414450c61
verified: strong
---
# Drive: while background work runs, name a concrete queued task to start (builder lane / plan / block), offer up to 3 in turn, then wait — JARVIS idled with 20+ queued ('nothing else to do')
## Raw request
> Drive: while background work runs, name a concrete queued task to start (builder lane / plan / block), offer up to 3 in turn, then wait — JARVIS idled with 20+ queued ('nothing else to do')
## Interpretation
The user saw JARVIS parked on two background jobs with 20+ tasks queued: the drive pushed once per running set with generic advice ('the next step's test, audit lenses, docs …') and then let every later Stop end the turn. The session said 'nothing else to do' and called T-0153 blocked without blocking it. While background work runs and other work is queued, the drive must name a concrete next task and how to start it, again on the next Stop, until candidates run out.
## Assumptions (confidence)
## Acceptance criteria
- [x] with queued independent work, each Stop during background work names the next candidate and how to start it; a task depending on the active one is skipped; once candidates run out it waits — verify with `python3 plugin/tests/run.py -k test_drive_offers_queued_work_while_background_runs`
## Non-goals
## Approach (options → choice → why)
(A, chosen) per Stop while jobs run: the next independent queued task not yet offered for this running set — skip the active one, blocked ones, ones whose depends_on/inferred_deps include the active task, and ones already in a lane — with how to start it: planned S/M → fm lane brief ID and launch the builder it prints; L or captured → ground and plan it (fm task new --from / intake §2); a task that can't move → fm task block ID "why". Offer at most 3 per running set (DRIVE_MAX still caps), then wait as today. Rejected: (B) launch lanes from the hook — hooks can't start agents; (C) suggest headless fm run workers — they'd share one checkout; (D) repeat the generic push every Stop — no direction, loops.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first
2. [x] candidates in _drive; message with fm lane brief / plan / fm task block
3. [x] gate, changelog, ship
## Resume here
## Docs impact
CHANGELOG Unreleased
## Verification evidence
- `python3 plugin/tests/run.py -k test_drive_offers_queued_work_while_background_runs` → ✗ exit 1 · Ran 1 tests in 1.5s (1 classes, 16 at a time; slowest: Stop 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree cd6a718fd4c6] (2026-10-09T03:59:09Z)
- `python3 plugin/tests/run.py -k test_drive_offers_queued_work_while_background_runs` → exit 0 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree cd6a718fd4c6] (2026-10-09T03:59:09Z)
- (step 1) `python3 plugin/tests/run.py -k test_drive_offers_queued_work_while_background_runs` → exit 0 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree cd6a718fd4c6] (2026-10-09T03:59:11Z)
- (step 2) `python3 plugin/tests/run.py -p test_hooks.py` → exit 0 · Ran 127 tests in 17.0s (18 classes, 16 at a time; slowest: Stop 17s, Approvals 10s, SessionStart 9s) / OK [ran] [tree cd6a718fd4c6] (2026-10-09T03:59:28Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (27 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed (slower: 6.0 s vs a usual 4.0 s); python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.9    32.7     150  [0] / SessionEnd                  29.1    31.7     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/r [ran] [tree e655d2a0ab7e] (2026-10-09T04:00:29Z)
- (ac 1) `python3 plugin/tests/run.py -k test_drive_offers_queued_work_while_background_runs` → exit 0 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree e655d2a0ab7e] (2026-10-09T04:00:39Z)
- (audit intent) `self: traced the Stop path for a lone task (unchanged: one generic push, then wait), queued independent work (a new concrete offer per Stop, up to 3), a dependent task (skipped), headless runs (excluded); hook suite 127/127` → JARVIS's case — background jobs running, tasks queued — now gets 'Start T-… now: fm lane brief …' on each Stop instead of idling; a task that can't move is told to be blocked (test) [tree e655d2a0ab7e] (2026-10-09T04:00:39Z)
- (audit edge) `self: traced the Stop path for a lone task (unchanged: one generic push, then wait), queued independent work (a new concrete offer per Stop, up to 3), a dependent task (skipped), headless runs (excluded); hook suite 127/127` → no queue → old behaviour; offers reset when the job set changes; DRIVE_MAX still caps continuations; tasks already briefed for a lane or depending on the active one are skipped [tree e655d2a0ab7e] (2026-10-09T04:00:39Z)
- (audit operator) `self: traced the Stop path for a lone task (unchanged: one generic push, then wait), queued independent work (a new concrete offer per Stop, up to 3), a dependent task (skipped), headless runs (excluded); hook suite 127/127` → at most 3 extra continuations per set of jobs; each is a drive_offer event, so fm friction can count them [tree e655d2a0ab7e] (2026-10-09T04:00:39Z)
## Log
- 2026-10-09T03:57:17Z created
- 2026-10-09T03:57:27Z focused
- 2026-10-09T04:00:39Z done
- 2026-10-09T04:00:39Z committed 94f2f48 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0364 [FIX L, done, 5 steps] Foreman keeps working while background jobs run, plans and brainstorms wider, uses subagents — lesson: Read the user's transcripts before t…
- T-0096 [FIX M, done, 3 steps] Drive resumes when background work finished mid-turn — lesson: A wait that depends on an event the hook might never see needs a second sign…
- research mission-20261008-195201: Request: super improve foreman
- decision 2026-09-26: Work T-0019 (drive vs background work) before T-0016: T-0016's five-lens audit runs background agents, where drive currently pushes the turn on ever…
- similar finished tasks took 3–5 steps
## Lessons
- A push that only lists ideas lets the model decline them; name one task and the exact command to start it, and offer the next on the next Stop
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
