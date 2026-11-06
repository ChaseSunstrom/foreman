# Critique — Mission 7, proof (gen 1, #6 and #10)

Tasks: T-2284, T-2381, T-2385, T-2386, T-2387, T-2389, T-2393, T-2273, T-2391, T-2392, T-2388, T-2390, T-2394, T-2395, T-2451, T-2453 (all done). Mission: gen-1/mission-proof.md.

## Closed vs planned
- Every planned gap has its briefs closed (see the Mission's table); none is closed in the exam's sense until the
  end-of-run exam's session arms grade it.

## Outside signals
- None from outside Foreman yet: #6 and #10's kinds need the session arms (end-of-run exam).

## Signals from Foreman's own tooling
- fm prove --rollup (2026-11-01): 1042 unproven claims across closed work: docs 580, meaning 576, ui-unshot 57,
  perf-typed 52, red 52, typed 46, research-uncited 31, infra 7, data 4, perf-noise 1 (one claim can count in more than one kind). Most predate
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
- A sweep that proves or labels the 580 docs and 576 meaning claims, oldest first, as zero-token work.
- A check that a new exam kind is mapped in KIND_WORDS and has an outside author before its task can close.
