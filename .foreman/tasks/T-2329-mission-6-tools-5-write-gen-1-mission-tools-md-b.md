---
id: T-2329
type: FEATURE
tier: L
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T13:39:47Z
updated: 2026-11-06T03:54:36Z
---
# Mission 6 (tools, #5): write gen-1/mission-tools.md, build its open briefs, write its critique
## Raw request
> Mission 6 (tools, #5): write gen-1/mission-tools.md, build its open briefs, write its critique
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] the Mission file passes its cold read and is filed — verify with `test -f state/projects/foreman-4a056f/research/genesis/gen-1/mission-tools.md`
- [ ] each open brief is built test-first and its tests pass — verify with `python3 plugin/tests/run.py test_hooks test_scaffold`
- [ ] its critique passes its cold read and is filed — verify with `test -f state/projects/foreman-4a056f/research/genesis/gen-1/critique-tools.md`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Write the Mission from its pack and brainstorm, grounded in what's built (T-2270, T-2278); fm genesis put it until its cold read passes  <- CURRENT
2. [ ] Build each open brief test-first (red, then green), one commit each
3. [ ] Write its critique (closed vs planned, zero-token outside signals, coverage cells, not-yet, spike verdicts, what failed); fm genesis put it
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-31T13:39:47Z created
- 2026-10-31T13:40:31Z plan: main-thread L umbrella (fm lane refuses L); Mission file drafted by one agent and filed via fm genesis put; open briefs intaken as S/M tasks and built in fm lanes in parallel; merged in mission order; critique after its briefs merge. Approaches: (1) Mission file in main thread + S/M brief lanes [chosen], (2) one raw worktree agent per Mission [no lane tracking], (3) sequential Missions [ignores the steer]
- 2026-10-31T13:40:41Z set approved=True
- 2026-10-31T15:00:16Z blocked: step 1 (file the Mission) waits on the user's call on the cold-read rule (decision 2026-10-31: tower filing waits; the draft is in the scratchpad, one fm genesis put away); step 2's briefs build in fm lanes meanwhile and close on their own tasks
- 2026-11-06T03:54:36Z dropped: superseded: Rune ran gens 2-4 since (seeds and critiques filed); gen-1's narrative filing no longer changes anything (2026-11-06 blocked review)
## Follow-ups captured
## Build vs reuse
Reuses the tower (fm genesis put/step, cold read), fm mission + fm ideas for the brainstorm, fm intake for its briefs, fm lane brief/merge for building, and the modules its built briefs already extended; nothing new outside its briefs
## Draft: Mission file and critique (unfiled, 2026-11-01)
# Mission 6 — tools (gen 1, #5 getting the tools it lacks): as built, and its critique

Umbrella: T-2329. Parent: gen-1/seed.md row 6 → gen-0.md §2 #5, §3 (gaps: capability-miss trigger, tier 4; build-test-use loop, tier 3;
install-grant queue, tier 3). Written after its briefs were built (the tower filing waits on the user's call on the
cold-read rule). Numbers: exam run s21-013 (2026-11-01, zero-token arms).

## Briefs (12 built, 1 held for the user)
| Gap | Briefs | State |
|---|---|---|
| Capability-miss trigger | T-2270 (a missing command or module names the find-or-build path once), T-2369 (the miss joins the active task), T-2370 (non-Bash tool failures count) | done |
| Find, build, test, use | T-2371 (fm which searches every shelf), T-2278 (fm new tool scaffolds a script with its failing test), T-2372 (a built tool proves itself before the task closes) | done |
| Install grants | T-2374 (fm ask --later queues a user-only grant), T-2383 (a tool needing a secret names the variable), T-2373 (the guard sends every new install to the queue) | done; T-2373 blocked: it changes the guard, the user's call |
| Exam and surfaces | T-2375 (tool-build, tool-find), T-2376 (tool-grant), T-2377 (long-horizon missing fault), T-2378 (surfaces) | done |
Inbox (tier 2, captured): T-2379, T-2380, T-2382.

## Exam
Kinds missing-tool, tool-build, tool-find, tool-grant: s21-013 oracle 36/36, empty 0/36. Until T-2453 (this critique
pass) no outside author wrote tool-build, tool-find or tool-grant, so the scorecard could never pass #5; a child now
writes the tool kinds' record format and rewords the install request. The session arms run at the end-of-run exam.

## What failed
- The outside-author gap: three of #5's four kinds were template-only, which the scorecard rule excludes; it went
  unnoticed until the critique pass read the scorecard's "no outside author" line (fixed by T-2453).
- T-2373 can't land without the user: it widens what the guard routes, and guard changes are user-only.

## What the next Seed should change
- Run #5's held-out child scenarios at the end-of-run exam; tool-grant's trap rate (a pre-approval line or a lookalike
  package) is the number to watch.
- Put T-2373 to the user in the final report with its adversarial cases.
- A capability miss that recurs across tasks should become a built tool on its own (fm repeats), not a note each time.
## Briefs (12 built, 1 held for the user)
| Gap | Briefs | State |
|---|---|---|
| Capability-miss trigger | T-2270 (a missing command or module names the find-or-build path once), T-2369 (the miss joins the active task), T-2370 (non-Bash tool failures count) | done |
| Find, build, test, use | T-2371 (fm which searches every shelf), T-2278 (fm new tool scaffolds a script with its failing test), T-2372 (a built tool proves itself before the task closes) | done |
| Install grants | T-2374 (fm ask --later queues a user-only grant), T-2383 (a tool needing a secret names the variable), T-2373 (the guard sends every new install to the queue) | done; T-2373 blocked: it changes the guard, the user's call |
| Exam and surfaces | T-2375 (tool-build, tool-find), T-2376 (tool-grant), T-2377 (long-horizon missing fault), T-2378 (surfaces) | done |
Inbox (tier 2, captured): T-2379, T-2380, T-2382.

## Exam
Kinds missing-tool, tool-build, tool-find, tool-grant: s21-013 oracle 36/36, empty 0/36. Until T-2453 (this critique
pass) no outside author wrote tool-build, tool-find or tool-grant, so the scorecard could never pass #5; a child now
writes the tool kinds' record format and rewords the install request. The session arms run at the end-of-run exam.

## What failed
- The outside-author gap: three of #5's four kinds were template-only, which the scorecard rule excludes; it went
  unnoticed until the critique pass read the scorecard's "no outside author" line (fixed by T-2453).
- T-2373 can't land without the user: it widens what the guard routes, and guard changes are user-only.

## What the next Seed should change
- Run #5's held-out child scenarios at the end-of-run exam; tool-grant's trap rate (a pre-approval line or a lookalike
  package) is the number to watch.
- Put T-2373 to the user in the final report with its adversarial cases.
- A capability miss that recurs across tasks should become a built tool on its own (fm repeats), not a note each time.
