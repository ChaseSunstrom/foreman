---
id: T-2330
type: FEATURE
tier: L
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T13:39:48Z
updated: 2026-11-06T03:54:38Z
---
# Mission 7 (proof, #6 #10): write gen-1/mission-proof.md, build its open briefs, write its critique
## Raw request
> Mission 7 (proof, #6 #10): write gen-1/mission-proof.md, build its open briefs, write its critique
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] the Mission file passes its cold read and is filed — verify with `test -f state/projects/foreman-4a056f/research/genesis/gen-1/mission-proof.md`
- [ ] each open brief is built test-first and its tests pass — verify with `python3 plugin/tests/run.py test_proof test_evidence_quality test_docsdrift`
- [ ] its critique passes its cold read and is filed — verify with `test -f state/projects/foreman-4a056f/research/genesis/gen-1/critique-proof.md`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Write the Mission from its pack and brainstorm, grounded in what's built (T-2273, T-2284, T-2288, T-2303); fm genesis put it until its cold read passes  <- CURRENT
2. [ ] Build each open brief test-first (red, then green), one commit each
3. [ ] Write its critique (closed vs planned, zero-token outside signals, coverage cells, not-yet, spike verdicts, what failed); fm genesis put it
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-31T13:39:48Z created
- 2026-10-31T13:40:31Z plan: main-thread L umbrella (fm lane refuses L); Mission file drafted by one agent and filed via fm genesis put; open briefs intaken as S/M tasks and built in fm lanes in parallel; merged in mission order; critique after its briefs merge. Approaches: (1) Mission file in main thread + S/M brief lanes [chosen], (2) one raw worktree agent per Mission [no lane tracking], (3) sequential Missions [ignores the steer]
- 2026-10-31T13:40:42Z set approved=True
- 2026-10-31T15:00:17Z blocked: step 1 (file the Mission) waits on the user's call on the cold-read rule (decision 2026-10-31: tower filing waits; the draft is in the scratchpad, one fm genesis put away); step 2's briefs build in fm lanes meanwhile and close on their own tasks
- 2026-11-06T03:54:38Z dropped: superseded: Rune ran gens 2-4 since (seeds and critiques filed); gen-1's narrative filing no longer changes anything (2026-11-06 blocked review)
## Follow-ups captured
## Build vs reuse
Reuses the tower (fm genesis put/step, cold read), fm mission + fm ideas for the brainstorm, fm intake for its briefs, fm lane brief/merge for building, and the modules its built briefs already extended; nothing new outside its briefs
## Draft: Mission file and critique (unfiled, 2026-11-01)
# Mission 7 — proof (gen 1, #6 verifying anything, #10 beyond code): as built, and its critique

Umbrella: T-2330. Parent: gen-1/seed.md row 7 → gen-0.md §2 #6 and #10, §3 (gaps: proof kinds for docs, infra, data and perf, tier 3; unproven
rollup, tier 4). Written after its briefs were built (the tower filing waits on the user's call on the cold-read rule).
Numbers: exam run s21-013 (2026-11-01, zero-token arms) and fm proof.

## Briefs (14 built)
| Gap | Briefs | State |
|---|---|---|
| Proof kinds | T-2284 (perf: timed on the start tree and the task's), T-2381 (docs: the repo's own flags, paths and commands), T-2385 (infra validators), T-2386 (migrations up, down, up), T-2387 (data on a throwaway copy), T-2389 (release: build, install, run offline), T-2393 (meaning: each request clause bound to a green criterion) | done |
| Unproven rollup | T-2273 (rollup), T-2391 (by domain), T-2392 (where the user sees a claim) | done |
| Beyond code | T-2388 (incident ritual), T-2390 (fm release in any repo) | done |
| Exam and surfaces | T-2394 (proof, beyond kinds), T-2395 (surfaces) | done |

## Exam
Kinds proof (#6) and beyond (#10), with slow and docs: s21-013 oracle 18/18 for proof and beyond, empty 0. Two gaps
found in this critique pass: neither kind was mapped to its capability, so the scorecard graded #6 on slow and docs only
and #10 on docs only (fixed by T-2451), and neither had an outside author (fixed by T-2453). The session arms run at the
end-of-run exam.

## Outside signals
- fm proof: 1030 unproven claims across closed work: docs 576, meaning 572, ui-unshot 57, perf-typed 52, typed 46,
  red 40, research-uncited 30, infra 7, data 6, perf-noise 1 (one claim can count in more than one kind). Most predate
  Mission 7; the rollup now makes them visible.
- Every close today printed "docs proof: 2 checkable claims in CHANGELOG.md, not verified": the rollup works, and the
  closes still don't run fm prove --docs on their own changelog lines.

## What failed
- A kind added without its mapping and its outside author is invisible to the scorecard; T-2394 shipped both gaps and
  the scorecard's own "no outside author" line was the only sign.
- T-2446: the release-proof tests failed on CI runners without setuptools (fixed by skipping there).
- The docs and meaning backlogs grow with each close because nothing runs those proofs by default.

## What the next Seed should change
- Run fm prove --docs at fm task finish whenever CHANGELOG.md or README.md changed, so new claims are proven at the
  source and the docs backlog only shrinks.
- A sweep that proves or labels the 576 docs and 572 meaning claims, oldest first, as zero-token work.
- A check that a new exam kind is mapped in KIND_WORDS and has an outside author before its task can close.
## Briefs (14 built)
| Gap | Briefs | State |
|---|---|---|
| Proof kinds | T-2284 (perf: timed on the start tree and the task's), T-2381 (docs: the repo's own flags, paths and commands), T-2385 (infra validators), T-2386 (migrations up, down, up), T-2387 (data on a throwaway copy), T-2389 (release: build, install, run offline), T-2393 (meaning: each request clause bound to a green criterion) | done |
| Unproven rollup | T-2273 (rollup), T-2391 (by domain), T-2392 (where the user sees a claim) | done |
| Beyond code | T-2388 (incident ritual), T-2390 (fm release in any repo) | done |
| Exam and surfaces | T-2394 (proof, beyond kinds), T-2395 (surfaces) | done |

## Exam
Kinds proof (#6) and beyond (#10), with slow and docs: s21-013 oracle 18/18 for proof and beyond, empty 0. Two gaps
found in this critique pass: neither kind was mapped to its capability, so the scorecard graded #6 on slow and docs only
and #10 on docs only (fixed by T-2451), and neither had an outside author (fixed by T-2453). The session arms run at the
end-of-run exam.

## Outside signals
- fm proof: 1030 unproven claims across closed work: docs 576, meaning 572, ui-unshot 57, perf-typed 52, typed 46,
  red 40, research-uncited 30, infra 7, data 6, perf-noise 1 (one claim can count in more than one kind). Most predate
  Mission 7; the rollup now makes them visible.
- Every close today printed "docs proof: 2 checkable claims in CHANGELOG.md, not verified": the rollup works, and the
  closes still don't run fm prove --docs on their own changelog lines.

## What failed
- A kind added without its mapping and its outside author is invisible to the scorecard; T-2394 shipped both gaps and
  the scorecard's own "no outside author" line was the only sign.
- T-2446: the release-proof tests failed on CI runners without setuptools (fixed by skipping there).
- The docs and meaning backlogs grow with each close because nothing runs those proofs by default.

## What the next Seed should change
- Run fm prove --docs at fm task finish whenever CHANGELOG.md or README.md changed, so new claims are proven at the
  source and the docs backlog only shrinks.
- A sweep that proves or labels the 576 docs and 572 meaning claims, oldest first, as zero-token work.
- A check that a new exam kind is mapped in KIND_WORDS and has an outside author before its task can close.
