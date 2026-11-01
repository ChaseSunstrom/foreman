# Sweep — gen-1 (gen-0 §7)

Verdict: red

✗ genesis check: gen-1/mission-genesis.md: no cold-read pass for its current text: fm genesis put it again
✓ steer checks: every rule from a user steer has a check, and each passes
✓ mission tasks: 94 brief(s) closed or blocked
✓ tasks: every task closed or blocked with a reason
✓ lanes: no unmerged lane
✓ docs: no docs drift
✓ doctor: no failures
✓ gates: full gates green on this tree, run at 16:02 UTC
✓ privileges: publish 237×; no new kind
✓ lean: rules chars 6395 -> 6391 (-4); descriptions chars 4237 -> 4236 (-1); largest SKILL chars 9742 -> 9269 (-473); removed: instruments, suspects, sweep; added: goal, prove, triggers; hook p95 not judged (no start time); measured from the seed's commit (no start record)
✓ exam: 4 foreman line(s) graded for gen 1

Fix tasks: T-2479

Fix the ✗ lines (one task each), then rerun fm genesis sweep 1; the next generation waits on a clean sweep.
