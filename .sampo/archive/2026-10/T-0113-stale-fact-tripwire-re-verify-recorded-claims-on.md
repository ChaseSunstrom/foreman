---
id: T-0113
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/tests/test_stale.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-03T03:05:24Z
updated: 2026-10-03T08:50:00Z
base: 70433f7675615f8267f380a3135668eec164508e
base_tree: b2606532a8bbed0ac4c8ec0f6221abe1c376f1d8
verified: ok
---
# Stale-fact tripwire: on resume, name the paths and code names a brief cites that existed when the task started and are gone now
## Raw request
> Stale-fact tripwire: re-verify recorded claims on resume
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] A resumed task whose brief cites a file and a function deleted since it started gets a stale warning naming both (fm resume and session start), and a file it plans to create isn't flagged — verify with `python3 plugin/tests/run.py -k test_stale`
- [x] Hook latency stays in budget; all gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test
2. [x] stale_refs, shown by resume, session start and re-focus
3. [x] MASTER and CHANGELOG
## Resume here
## Docs impact
MASTER (Stale-fact tripwire) and CHANGELOG.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_stale` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: StaleRefs 0s) / OK [ran] [tree 6c0afb8d7018] (2026-10-03T08:49:59Z)
- (step 2) `python3 plugin/tests/run.py -k test_stale` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: StaleRefs 0s) / OK [ran] [tree 6c0afb8d7018] (2026-10-03T08:49:59Z)
- (step 3) `grep -q T-0113 MASTER.md && grep -q T-0113 CHANGELOG.md` → exit 0 · (no output) [ran] [tree 6c0afb8d7018] (2026-10-03T08:49:59Z)
- (ac 1) `python3 plugin/tests/run.py -k test_stale` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: StaleRefs 0s) / OK [ran] [tree 6c0afb8d7018] (2026-10-03T08:50:00Z)
- (ac 2) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 08:49 UTC); cached (fm check --fresh reruns) [ran] [tree 6c0afb8d7018] (2026-10-03T08:50:00Z)
- (audit self) `self: the test deletes a committed file and its function after the task starts: resume and session start name both, and a file the step plans to create isn't flagged (it never existed at the start point); git calls are bounded (20 paths, 8 names, 10 s each) and failures cost only the warning; SessionStart stays in the bench budget` → no findings [tree 6c0afb8d7018] (2026-10-03T08:50:00Z)
## Log
- 2026-10-03T03:05:24Z created
- 2026-10-03T08:48:28Z planned from capture
- 2026-10-03T08:48:29Z focused
- 2026-10-03T08:50:00Z done
- 2026-10-03T08:50:00Z committed bb843a7 (6 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0071-de-review: MEDIUM — `plugin/lib/fmcost.py:546` — `cmd_usage`'s Next-follow regex `\bfm [a-z-]+(?: (?:prep|step|done|new|evidence|ac|audit|finish|prove))?`…
- research t0036-intent: MEDIUM** — `plugin/lib/fmplugins.py:388-398` (`content_hash`) — For a plugin that is not locally mirrored by its marketplace (a genuinely remote s…
- research t0071-fg-review: Each piece does what it claims end-to-end (verified by reading each call site): the mtime union in `fm task done` (fmcli.py:219-226), `--fail-f…
- research t0036-operator: The implementation matches its documented contract and is well tested. Findings below are minor.
- likely tests for the scope: plugin/tests/test_core.py, plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-10-03): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py; re-ground the plan against them before editing
## Lessons
- Staleness is 'existed then, gone now', not 'missing': comparing against the task's own start point is what keeps a tripwire from crying wolf over files still to be written.
## Files touched
- plugin/tests/test_stale.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
