---
id: T-0435
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:17Z
updated: 2026-10-09T14:36:54Z
base: 47a66dd137a6d8395990ba36384c7b3ade5d4081
base_tree: f07326fd84db07c39a8ea369555ee84b84d46073
verified: strong
---
# fm friction reads every project's friction, labelled by project
## Raw request
> FEATURE: Friction capture and self-improvement loop (C040, value 5/5, effort M, risk low)
>   first version: Let fm friction read other registered projects' ledgers (guard blocks, user corrections, taste) read-only and file self-inbox items; postmortem line on each correction. Skip mood detection and weather report.
>   what it is: Collect friction from the user, downstream projects and Foreman's own runs and turn it into improvement tasks with proof it helped.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 7 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
_ledgers already reads every project's ledger but drops which project a line came from. Label the ledger-derived lines (corrections, steers, blocks, escapes) with the project slug and add a per-project count of guard blocks and corrections, so JARVIS's friction surfaces in Foreman's self-improvement pass. Read-only; sensitive projects skipped.
## Assumptions (confidence)
## Acceptance criteria
- [x] a correction in another registered project appears in the digest, labelled with its slug; sensitive projects are left out — verify with `python3 plugin/tests/run.py -k test_digest_labels_downstream_project_friction`
## Non-goals
## Approach (options → choice → why)
(A, chosen) slug labels + a 'downstream projects' section in digest(); capturing stays the pass's job (fm capture --source self). (B, rejected) auto-capture into the inbox: speculative.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first with two projects
2. [x] slug labels + downstream section, bounded by MAX_LINES
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_digest_labels_downstream_project_friction` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Friction 1s) / FAILED (1 classes) [ran] [tree f651a4e3f7bd] (2026-10-09T14:36:18Z)
- (step 2) `python3 plugin/tests/run.py -k test_digest_labels_downstream_project_friction` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Friction 1s) / OK [ran] [tree 0eeac98af831] (2026-10-09T14:36:42Z)
- (ac 1) `python3 plugin/tests/run.py -k test_digest_labels_downstream_project_friction` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Friction 1s) / OK [ran] [tree 3ccfb942141e] (2026-10-09T14:36:54Z)
- (audit intent) `self: labels + per-project counts + sensitive projects skipped; read-only; lines sanitized and bounded; red→green; friction suite OK; the real digest shows the other-projects section` → downstream friction is visible in Foreman's own pass, labelled; capturing stays the pass's job [tree 3ccfb942141e] (2026-10-09T14:36:54Z)
- (audit edge) `self: labels + per-project counts + sensitive projects skipped; read-only; lines sanitized and bounded; red→green; friction suite OK; the real digest shows the other-projects section` → projects on other machines (JARVIS) aren't registered here, so their friction still needs the machines capability (T-0574) [tree 3ccfb942141e] (2026-10-09T14:36:54Z)
## Log
- 2026-10-09T14:30:17Z created
- 2026-10-09T14:32:35Z planned from capture
- 2026-10-09T14:36:00Z focused
- 2026-10-09T14:36:54Z done
- 2026-10-09T14:36:54Z committed d1eaa38 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0505 [FEATURE M, dropped, 0 steps] Friction capture and self-improvement loop (C040, value 5/5, effort M, risk low)
- research mission-20261009-093310: Request: I want genuine like capabilities/intelligence from it to, like planning/brainstorming/agent types/improvements/thought process…
- research mission-20261009-093310.pack: I want genuine like capabilities/intelligence from it to, like planning/brainstorming/agent types/improvements/thought process/ste…
- decision 2026-10-04: Landscape 2026-10-04 grounded: no new work
## Lessons
- Aggregated signals need their source kept: a line without its project can't be acted on.
## Files touched
- plugin/tests/test_friction.py
- plugin/lib/fmfriction.py
- CHANGELOG.md
