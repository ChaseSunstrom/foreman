---
id: T-1400
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmmandate.py, plugin/lib/fmscout.py, plugin/lib/fmcli.py, plugin/tests/test_scout.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-10-23T10:04:06Z
inferred_deps: [T-1382]
inferred_why: T-1382: named in its request
base: 35a9f34251f1dbb0ebc07ea8ba53e23f574fdcef
base_tree: 57d1a0c579aa674782487b3d3e958a1a25070a85
plan0_at: 2026-10-23T10:01:35Z
plan0_scope: [plugin/lib/fmmandate.py, plugin/lib/fmscout.py, plugin/lib/fmcli.py, plugin/tests/test_scout.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# A standing mandate: a sweeping request becomes one record (its text, its clauses from fm c
## Raw request
> FEATURE: A standing mandate: a sweeping request becomes one record (its text, its clauses from fm clauses, fm contract bounds, an expiry) that fm night and fm scout read; at expiry it becomes one decision in the inbox and capturing under it stops (S13, B16)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: a mandate with a past expiry makes fm night --dry (or fm scout --json) emit one decision and capture nothing more under it
## Interpretation
fm mandate set "<request>" --until YYYY-MM-DD [--usd N] keeps a sweeping request as one record in the project meta: its text, its clauses (fm clauses), the end, a recorded spend bound. fm scout reads it (and fm night, which runs scout first): while it stands its findings say they were found under it; once it ends scout captures one RESEARCH decision (renew or lapse), keyed by when the mandate was set so it is captured once, and runs no probe until the mandate is renewed or cleared (fm mandate off).
## Assumptions (confidence)
## Acceptance criteria
- [x] a mandate with a past end makes fm scout --json (and so fm night) emit one decision and capture nothing more under it; clearing it lets scout run again — verify with `python3 plugin/tests/run.py test_scout.Mandate`
## Non-goals
## Approach (options → choice → why)
Options: a task holding the mandate (tasks close; a mandate stands); fm contract extended with text (contract bounds a run, a mandate scopes self-directed capture); a small record in meta with get/put/clear and one check at scout's start. Choice: the last; spend stays fm contract's job, the mandate records it only.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then fmmandate, the verb and scout's check
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_scout.Mandate` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Mandate 0s) / FAILED (1 classes) [ran] [tree a39c4bb3095a] (2026-10-23T10:01:42Z)
- (step 1) `python3 plugin/tests/run.py test_scout test_docs` → ✗ exit 1 · Ran 89 tests in 11.5s (21 classes, 16 at a time; slowest: Scout 11s, Fences 8s, ScoutDrive 2s) / FAILED (1 classes) [ran] [tree bed2568cf260] (2026-10-23T10:02:56Z)
- (step 1) `python3 plugin/tests/run.py test_scout test_docs` → exit 0 · Ran 89 tests in 11.5s (21 classes, 16 at a time; slowest: Scout 11s, Fences 8s, ScoutDrive 2s) / OK [ran] [tree b399090b0cd0] (2026-10-23T10:03:27Z)
- (ac 1) `python3 plugin/tests/run.py test_scout.Mandate` → exit 0 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: Mandate 1s) / OK [ran] [tree b399090b0cd0] (2026-10-23T10:03:34Z)
- (audit intent) `self review; test_scout, test_cli and test_docs green` → an ended mandate makes fm scout --json emit exactly one decision keyed by when it was set, captured once, with no probe run; clearing it lets scout run again (test) [tree b399090b0cd0] (2026-10-23T10:03:34Z)
- (audit edge) `self review; test_scout, test_cli and test_docs green` → a date already past is refused at set; a damaged until never ends the mandate; while it stands each finding says it was found under it; fm night inherits it by running scout first [tree b399090b0cd0] (2026-10-23T10:03:34Z)
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-23T09:47:34Z set tier=M, scope=['plugin/lib/fmmandate.py', 'plugin/lib/fmscout.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_scout.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-23T10:01:34Z focused
- 2026-10-23T10:04:05Z done
- 2026-10-23T10:04:06Z committed 69e3b1db (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1397 [FEATURE M, done, 1 steps] Intake offer: fm code prints one line when an indexed skill matches the request (name, lic — lesson: Stack cards name tools (cargo) mor…
- T-1391 [FEATURE M, done, 1 steps] Upstream watch: when a pinned source's sha moves, one finding lists added, removed and ren — lesson: Ask the remote before fetching it:…
- T-1405 [FIX M, done, 4 steps] Crash hygiene: stack dumps for hung verbs, safe stale index.lock removal, a lock probe in doctor — lesson: A safety rule written as 'unknow…
- decision 2026-10-15: Round 7 slate: 8 small reliability/delight builds (bare fm answers what now, close shows undo, demo ends in this repo, doctor state budget, night le…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_scout.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmscout.py, plugin/tests/test_scout.py; re-ground the plan against them before editing
## Lessons
- parse_ts returns a datetime, not epoch seconds: compare its .timestamp() with time.time()
## Plan gaps
- failed first: step 1 failing test, then fmmandate, the verb and scout's check
## Files touched
- plugin/lib/fmmandate.py
- MASTER.md
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/lib/fmscout.py
- plugin/tests/test_scout.py
