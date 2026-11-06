---
id: T-2230
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T23:29:29Z
updated: 2026-11-06T03:54:33Z
base: 2cbec9f5561df77a780f9138cd12581ccbe373ca
base_tree: e1ef079446e836a47446452f7518e5688a4a064b
plan0_at: 2026-10-31T07:49:33Z
plan0_scope: []
paused_tree: e1ef079446e836a47446452f7518e5688a4a064b
---
# Re-add coverage cells find × CLI (fm find) and find × Claude Code (SessionStart leads)…
## Raw request
> Re-add coverage cells find × CLI (fm find) and find × Claude Code (SessionStart leads) once the exam reports finder recall per language and bug type (T-2185) and a foreman-arm run measures the leads note; the cold read dropped both for lacking that evidence
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] coverage.md's Initiative area has a find × Claude Code cell naming fmhooks.py's SessionStart leads note, filed through fm genesis put (cold read passed, so fm genesis check shows it read) — verify with `fm genesis check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] add the cell and put coverage.md  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-30T23:29:29Z created
- 2026-10-31T07:49:31Z set tier=S
- 2026-10-31T07:49:31Z planned: it has criteria and steps
- 2026-10-31T07:49:32Z focused
- 2026-10-31T07:52:46Z blocked: Diagnosis: adding one cell re-reads every coverage section (the outline changed), and the cold read raised 8+ new objections on long-filed cells across Initiative, Exhaustive thinking and Anticipation (the T-2221 non-convergence); one is fair and is folded in when it unblocks: the Initiative row should name the detection ladder (T-2185's rungs). Waits on T-2246 (the cold-read rule is the user's steer-2 call). coverage.md on disk is unchanged; the draft with the new cell is in the session scratchpad
- 2026-11-06T03:54:33Z dropped: superseded: Rune ran gens 2-4 since (seeds and critiques filed); gen-1's narrative filing no longer changes anything (2026-11-06 blocked review)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research draft-critique-initiative: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
- research draft-critique-initiative-gen1: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (fourth): standing rule for #1 detection] [check: pending T-2185] Standing rule: exam recall for #1 is reported …
- similar past tasks were M: consider --tier M
