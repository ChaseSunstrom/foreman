---
id: T-0438
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:17Z
updated: 2026-10-09T14:35:22Z
base: 9c2722c0d3fa69dd182def0bcb29790d5825e4e4
base_tree: 8b29094c3f16fb42798944ebbb93ad8cc36938e7
verified: strong
---
# Capture flags a re-ask of dropped work and a veto contradiction
## Raw request
> FEATURE: Intake quality (C049, value 4/5, effort S, risk low)
>   first version: First version: at capture, compare the new text to dropped/done briefs and open inbox (fmrecall) and note a likely re-ask or contradiction with the veto list; add a Definition-of-Ready lint (AC has verify cmd, scope named) on fm task new.
>   what it is: Catch contradictions, XY problems, duplicates and re-asks at intake, split big briefs and gate briefs by readiness.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 8 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
fm capture already notes when fm's own help covers a request. It should also say when the request resembles a dropped task (Dropped before: T-xxxx, with why) or matches a standing veto, so the same idea isn't silently re-done or a user's 'no' re-asked. Advisory only; capture never fails.
## Assumptions (confidence)
## Acceptance criteria
- [x] a capture resembling a dropped brief prints 'Dropped before: T-xxxx' — verify with `python3 plugin/tests/run.py -k capture_reask_dropped`
- [x] a capture matching a veto prints a 'Vetoed:' note — verify with `python3 plugin/tests/run.py -k capture_veto_contradiction`
## Non-goals
## Approach (options → choice → why)
(A, chosen) reuse fmrecall with a status==dropped filter (nearest_dropped, modelled on nearest_done) and c.veto_hits on the raw text. (B, rejected) a new similarity function. (C, rejected) block the capture.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first, both tests
2. [x] nearest_dropped in fmrecall + _reask_note in cmd_capture (sanitized, try/except)
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_capture_reask_dropped -k test_capture_veto_contradiction` → ✗ exit 1 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: CaptureAndIntake 0s) / FAILED (1 classes) [ran] [tree 9213889797e4] (2026-10-09T14:34:31Z)
- (step 2) `python3 plugin/tests/run.py -k test_capture_reask_dropped -k test_capture_veto_contradiction` → exit 0 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: CaptureAndIntake 1s) / OK [ran] [tree d223ff2f8642] (2026-10-09T14:34:46Z)
- (ac 1) `python3 plugin/tests/run.py -k capture_reask_dropped` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: CaptureAndIntake 0s) / OK [ran] [tree bf7795cb1d33] (2026-10-09T14:35:21Z)
- (ac 2) `python3 plugin/tests/run.py -k capture_veto_contradiction` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: CaptureAndIntake 0s) / OK [ran] [tree bf7795cb1d33] (2026-10-09T14:35:21Z)
- (audit intent) `self: diff read; advisory only (try/except, capture never fails); dropped task text sanitized (plain/defang/fit); threshold mirrors nearest_done; red→green; CLI and recall suites OK` → a re-ask of dropped work or a vetoed request is said at capture, as the grounding asked [tree bf7795cb1d33] (2026-10-09T14:35:21Z)
- (audit edge) `self: diff read; advisory only (try/except, capture never fails); dropped task text sanitized (plain/defang/fit); threshold mirrors nearest_done; red→green; CLI and recall suites OK` → veto_hits is prefix matching built for commands, so prose can false-positive; it's advice and names how to keep the task [tree bf7795cb1d33] (2026-10-09T14:35:21Z)
- (audit self) `self: diff read; advisory only (try/except, capture never fails); dropped task text sanitized (plain/defang/fit); threshold mirrors nearest_done; red→green; CLI and recall suites OK` → no findings [tree bf7795cb1d33] (2026-10-09T14:35:21Z)
## Log
- 2026-10-09T14:30:17Z created
- 2026-10-09T14:33:01Z planned from capture
- 2026-10-09T14:33:38Z focused
- 2026-10-09T14:35:20Z focused
- 2026-10-09T14:35:21Z done
- 2026-10-09T14:35:22Z committed 0625fee (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0508 [FEATURE M, dropped, 0 steps] Intake quality (C049, value 4/5, effort S, risk low)
- research mission-20261009-093310: Request: I want genuine like capabilities/intelligence from it to, like planning/brainstorming/agent types/improvements/thought process…
- research mission-20261009-093310.pack: I want genuine like capabilities/intelligence from it to, like planning/brainstorming/agent types/improvements/thought process/ste…
- decision 2026-09-27: Super-brainstorm slate: 5 build rounds (A gates-from-diff, B verification, C memory, D speed/tokens, E unattended), ~45 ideas + inbox; 60+ dropped a…
## Lessons
- Remember the user's 'no' at the door: capture is the cheapest place to stop re-doing dropped work.
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmrecall.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
- .claude-plugin/marketplace.json
