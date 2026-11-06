---
id: T-0881
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T15:14:54Z
updated: 2026-10-15T15:15:24Z
base: ef97387dfd75da7cdf8b56fc6ac8092607c0d790
base_tree: f7716b332d9f30addf6d8ffa85a2996d5dea3d25
verified: ok
---
# CHANGELOG: round 4 and its fixes (T-0854..T-0880)
## Raw request
> CHANGELOG: round 4 and its fixes (T-0854..T-0880)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] Unreleased names every shipped round-4 task — verify with `python3 -c "import re,sys; t=open('CHANGELOG.md').read().split('## 1.2.27')[0]; m=[i for i in ('T-0854','T-0855','T-0856','T-0857','T-0858','T-0859','T-0860','T-0870','T-0871','T-0872','T-0873','T-0874','T-0875','T-0876','T-0880') if i not in t]; sys.exit(print(m) or 1) if m else None"`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] write the lines
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 -c "import re,sys; t=open('CHANGELOG.md').read().split('## 1.2.27')[0]; m=[i for i in ('T-0854','T-0855','T-0856','T-0857','T-0858','T-0859','T-0860','T-0870','T-0871','T-0872','T-0873','T-0874','T-0875','T-0876','T-0880') if i not in t]; sys.exit(print(m) or 1) if m else None"` → exit 0 · (no output) [ran] [tree 74f586d26101] (2026-10-15T15:15:23Z)
- (step 1) `fm doctor` → exit 0 · WARN  briefs               foreman-desktop-d33873: STATE.md differs from the briefs (fm tidy --apply regenerates it); foreman-improve-20260927-4cffe6: STATE.md differs from the briefs (fm tidy --apply [ran] [tree 74f586d26101] (2026-10-15T15:15:23Z)
- (audit self) `self review: every line checked against its commit message; criterion script lists none missing` → no findings [tree 74f586d26101] (2026-10-15T15:15:23Z)
## Log
- 2026-10-15T15:14:54Z created
- 2026-10-15T15:14:55Z focused
- 2026-10-15T15:15:24Z done
- 2026-10-15T15:15:24Z committed e336902 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0590 [SECURITY M, done, 2 steps] Guard: IFS review round 2 — eval/source/quoted IFS sets, # after a rewritten IFS, quoted spans, read across a newline — lesson: a text…
- T-0840 [CLEAN S, done, 1 steps] CHANGELOG: add round 2's late items (T-0759, T-0833, T-0836, T-0837, T-0839) — lesson: none: bookkeeping
- research brainstorm-round4-20261015: 437 ideas (9 lenses x 4 rounds + 3 deepen rounds, past every earlier run) from new evidence: a clean-HOME newcomer install, a survey…
- T-0835 [CLEAN S, done, 1 steps] CHANGELOG: Unreleased entries for the 2026-10-14 rounds (CC integration, compact output, fm page, review fixes) — lesson: Write the chang…
- similar finished tasks took 1–2 steps
## Behaviour lock
none: documentation only, no code changes
## Files touched
- CHANGELOG.md
