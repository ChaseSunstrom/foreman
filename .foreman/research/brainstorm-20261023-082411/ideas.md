# Ideas by round (deduplicated titles; details in the lens files; "near T-…" names a finished task that shares most of an idea's words)
Ideas: 28 distinct (the bullets under Round, Deepened and Cross-bred; the tallies below are counts, not ideas)

## Round 1
- Expire edit leases with their run — near T-1764 (done): fm code: a model run's edit leases outlive it (drop_session…
- Make `fm quiet` fail loudly on piped stdin
- Restore the test_followups parser for split plugin/lib rows — near T-1739 (done): test_followups.Docs reads the plugin/lib row T-1713 split i…
- Give the gate lock a bounded, visible wait for `--affected` — near T-1743 (done): fm check --affected and --evidence step runs take the machi…
- Judge the hook bench by median and load, not one p95 — near T-0805 (done): The hook benchmark judges by CPU time when the machine is b…
- Write state files atomically, with fsync and rename
- Turn stalled runs into a timed, journaled recovery
- Make the rules-file budget a doctor failure that names what to cut — near T-1758 (done): Rules file over the doctor's 6,400-char budget since T-1520…
- Fuzz the guard hook so it always fails closed — near T-0371 (done): Guard hook fails closed in Claude Code itself: onFailure: "…
- Replay a run from its journal to reproduce it — near T-0682 (done): Milestone: Features — Verification and product checking
- Let a supervisor agent repair stalled gates from their journals
- Checkpoint every tool call into an undo ledger — near T-1357 (done): fm code cost: each call's dollars to the budget ledger, the…
- Run the demo as a nightly canary on a seeded repo — near T-0870 (done): fm demo: see Foreman work in a minute without model calls (…
- Collapse the install flags into one default path
- Cut the rules file under budget by deleting, not rewording — near T-1758 (done): Rules file over the doctor's 6,400-char budget since T-1520…
- Give bare `fm` one next command — near T-1705 (done): Free listing room: skills the model never loads itself (the…
- Retire verbs nobody runs
- Merge overlapping skills into one entry per job — near T-1700 (done): foreman:ui-design skill: one job-shaped entry to distinctiv…
- Shrink config to three settings — near T-1543 (done): Round 3 (T-1520): Settings safety: a last-known-good config…
- Show the pane's default view as one line — near T-1359 (done): fm code config: every effective fm code setting with its so…
- Serialize checks per project, not per machine — near T-0673 (done): Milestone: Features — Multi-machine, multi-project and ecos…
- Make the hook bench one median verdict — near T-0805 (done): The hook benchmark judges by CPU time when the machine is b…
- Reset stuck state with one command — near T-1482 (done): Guard corpus: cover the obfuscated forms of the four bench …
- Generate the deny rules from the guard's own list — near T-0712 (done): Frontier 12 — Self-improvement flywheel
- Reduce the two modes to two names — near T-1706 (done): Fm scene compile --to component --tag NAME so two scenes ca…
- Wild: keep one STATE.md that is the whole product state
- Wild: ship Foreman as one dependency-free file
- Wild: add `fm prune` to propose removing the least-used feature

## New ideas per lens
- reliability: 13
- simplicity: 15

## Coverage (ideas per category)
- concurrency 2
- install 2
- silent failure 1
- test robustness 1
- flaky benchmarks 1
- crash safety 1
- stall recovery 1
- budget 1
- fail-closed guard 1
- debugging 1
- docs 1
- cli 1
- cli surface 1
- skills 1
- config 1
- ui 1
- checks 1
- performance 1
- recovery 1
- guard 1
- modes 1
- visibility 1
- maintenance 1
Thin (0-1 ideas): user value, reliability, performance, security, privacy, ui, devices, agents, simplicity, developer experience, observability, docs, delight
