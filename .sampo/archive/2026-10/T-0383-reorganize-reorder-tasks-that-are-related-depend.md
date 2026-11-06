---
id: T-0383
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T00:59:17Z
updated: 2026-10-09T01:56:07Z
base: a9e5ca96f40769339c639df42fb76e47ae2fb369
base_tree: d322b3c86ec6fb56f3763ba72277cb354d768434
verified: strong
---
# Reorganize/reorder tasks that are related/depend/implement things others might need/build
## Raw request
> reorganize/reorder tasks that are related/depend/implement things others might need/build on/look at: infer dependencies between queued tasks and order (and group) them so the ones others build on go first
## Interpretation
The user wants the queue and inbox reorganised by how tasks relate: one that builds what others need goes first, related ones are done together, and nobody has to write #T- dependencies by hand. Today order_queue and rank_inbox honour only depends_on set at intake, which captured items almost never carry (JARVIS: 108 inbox items, none linked).
## Assumptions (confidence)
## Acceptance criteria
- [x] id mentions and a stubbed child's edges and groups reorder fm queue and the inbox; cycles and unknown ids are dropped; --clear undoes — verify with `python3 plugin/tests/run.py -p test_relate.py`
## Non-goals
## Approach (options → choice → why)
Chosen (D): fm relate. (1) Deterministic, always on: a task id mentioned in another open task's title or request becomes an inferred edge. (2) Semantic, a tool-less child (fmideas.run_child, budgeted, feature 'relate'): it reads the open tasks (id, type, tier, title, first 300 chars of the request) and replies with lines 'T-B -> T-A: <why>' (B builds on, needs or should follow A) and 'group: T-1 T-2 T-3 — <theme>'. fm keeps only ids that exist and edges that make no cycle, and stores them as meta inferred_deps (separate from depends_on, so they are visible and can be undone with fm relate --clear) and group. order_queue and rank_inbox treat inferred_deps like depends_on, and keep a group's members adjacent after the first one is placed. It runs automatically, at most once a day and only when at least 3 open tasks are new since the last run: from the SessionStart hook (detached, like fm second session) and after an fm intake that adds 3 or more items. fm queue shows each task's inferred reason. Rejected: (A) shared scope or files only, since captured items rarely carry scope; (B) the child alone, since the id-mention edges are free and certain; (C) a rules line telling Claude to add #T- deps, which already exists and isn't followed.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: test_relate.py (mentions → edge; stubbed child edges/groups → queue and inbox order; cycle and unknown id dropped; --clear; once-a-day trigger)
2. [x] fmrelate.py + fmcore order_queue/rank_inbox honour inferred_deps and group; fm relate CLI; SessionStart and intake triggers
3. [x] docs: CHANGELOG, MASTER file map, help tier; gate
## Resume here
## Docs impact
CHANGELOG Unreleased, MASTER file map (fmrelate), fm help tier
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_relate.py` → ✗ exit 1 · Ran 7 tests in 21.1s (3 classes, 16 at a time; slowest: Due 21s, Child 2s, Mentions 0s) / FAILED (3 classes) [ran] [tree da4f961bb533] (2026-10-09T01:24:48Z)
- (step 2) `python3 plugin/tests/run.py -p test_relate.py` → exit 0 · Ran 7 tests in 2.9s (3 classes, 16 at a time; slowest: Child 3s, Due 2s, Mentions 0s) / OK [ran] [tree d821cf4c5d0d] (2026-10-09T01:29:10Z)
- (step 3) `python3 plugin/tests/run.py -p test_doc*.py` → exit 0 · Ran 45 tests in 5.9s (13 classes, 16 at a time; slowest: Command 6s, DocsDrift 0s, RestoreState 0s) / OK [ran] [tree cfc1504901a6] (2026-10-09T01:30:43Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (26 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.9    34.7     150  [0] / SessionEnd                  29.3    32.5     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/run.py → exit 0 · Ran 913 tests in [ran] [tree cfc1504901a6] (2026-10-09T01:31:55Z)
- (step 1) `python3 plugin/tests/run.py -p test_relate.py` → ✗ exit 1 · Ran 18 tests in 5.9s (5 classes, 16 at a time; slowest: Review 6s, Child 3s, Due 2s) / FAILED (2 classes) [ran] [tree cc6b52cf832d] (2026-10-09T01:40:20Z)
- (step 2) `python3 plugin/tests/run.py -p test_relate.py` → exit 0 · Ran 18 tests in 6.4s (5 classes, 16 at a time; slowest: Review 6s, Child 3s, Due 2s) / OK [ran] [tree 88bad7eac278] (2026-10-09T01:44:17Z)
- (step 3) `python3 plugin/tests/run.py -p test_doc*.py` → exit 0 · Ran 45 tests in 5.9s (13 classes, 16 at a time; slowest: Command 6s, DocsDrift 0s, RestoreState 0s) / OK [ran] [tree 88bad7eac278] (2026-10-09T01:44:23Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (27 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.3    33.3     150  [0] / SessionEnd                  28.9    29.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/run.py → exit 0 · Ran 926 tests in [ran] [tree 88bad7eac278] (2026-10-09T01:45:38Z)
- (step 2) `python3 plugin/tests/run.py -p test_relate.py` → exit 0 · Ran 18 tests in 6.5s (5 classes, 16 at a time; slowest: Review 6s, Child 3s, Due 2s) / OK [ran] [tree 4e24a08e0187] (2026-10-09T01:53:45Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (27 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.3    34.5     150  [0] / SessionEnd                  29.6    31.6     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/run.py → exit 0 · Ran 928 tests in [ran] [tree 4e24a08e0187] (2026-10-09T01:54:57Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed on this tree (run at 01:54 UTC) [ran] [tree 4e24a08e0187] (2026-10-09T01:56:00Z)
- (ac 1) `python3 plugin/tests/run.py -p test_relate.py` → exit 0 · Ran 18 tests in 6.4s (5 classes, 16 at a time; slowest: Review 6s, Child 3s, Due 2s) / OK [ran] [tree 4e24a08e0187] (2026-10-09T01:56:07Z)
- (audit intent) `built in a builder lane; one foreman:fm-reviewer pass (merge after fixes: 4 medium, 6 low); all 9 fixes landed test-first (18 tests); two claims spot-checked in the merged code; dry run on this project` → open tasks that build on each other are ordered and grouped automatically, from id mentions and a cheap child, with no #T- written by hand; fm queue shows why [tree 4e24a08e0187] (2026-10-09T01:56:07Z)
- (audit adversary) `built in a builder lane; one foreman:fm-reviewer pass (merge after fixes: 4 medium, 6 low); all 9 fixes landed test-first (18 tests); two claims spot-checked in the merged code; dry run on this project` → the child's reply is data — only open ids pass, reasons go through _clean; no injection into brief frontmatter (reviewer traced); runs carry FOREMAN_NO_BACKGROUND [tree 4e24a08e0187] (2026-10-09T01:56:07Z)
- (audit edge) `built in a builder lane; one foreman:fm-reviewer pass (merge after fixes: 4 medium, 6 low); all 9 fixes landed test-first (18 tests); two claims spot-checked in the merged code; dry run on this project` → child failure keeps earlier inferences and retries; cycles and unknown ids dropped; urgent never held back; batched tasks map to their host; cap 5 edges per task [tree 4e24a08e0187] (2026-10-09T01:56:07Z)
- (audit operator) `built in a builder lane; one foreman:fm-reviewer pass (merge after fixes: 4 medium, 6 low); all 9 fixes landed test-first (18 tests); two claims spot-checked in the merged code; dry run on this project` → at most once a day, after 3+ new open tasks, detached; --clear turns it off until --on; --drop vetoes one edge for good [tree 4e24a08e0187] (2026-10-09T01:56:07Z)
## Log
- 2026-10-09T00:59:17Z created
- 2026-10-09T01:19:26Z set approved=True
- 2026-10-09T01:19:26Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0383.builder.md
- 2026-10-09T01:19:40Z focused
- 2026-10-09T01:55:21Z merged worktree-agent-a7ba3635d5b5b3025 (9 file(s))
- 2026-10-09T01:55:25Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a7ba3635d5b5b3025
- 2026-10-09T01:55:26Z focused
- 2026-10-09T01:56:07Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0146 [FEATURE M, done, 3 steps] Dashboard: no duplicates between band and pane, nothing stale or cut without saying so, controls that read as actions — lesson: Record …
- research mission-20261008-195201: Request: super improve foreman
- research mission-20261008-195201.pack: super improve foreman
- decision 2026-09-26: Order after T-0016: T-0022 and T-0023 (user requests, explore items: take the recommendation after self-critique in full autonomy), then T-0018's ro…
- the similar finished task took 3 steps
## Lessons
- A builder lane plus one review round and a fix round lands an M feature while the main thread does other work; tell the builder the main checkout's HEAD, since its isolation can't read it
## Files touched
- .claude/worktrees/agent-a7ba3635d5b5b3025/plugin/tests/test_relate.py
- .claude/worktrees/agent-a7ba3635d5b5b3025/plugin/lib/fmrelate.py
- .claude/worktrees/agent-a7ba3635d5b5b3025/plugin/lib/fmcore.py
- .claude/worktrees/agent-a7ba3635d5b5b3025/plugin/lib/fmcli.py
- .claude/worktrees/agent-a7ba3635d5b5b3025/plugin/lib/fmhooks.py
- .claude/worktrees/agent-a7ba3635d5b5b3025/CHANGELOG.md
- .claude/worktrees/agent-a7ba3635d5b5b3025/MASTER.md
- .claude/worktrees/agent-a7ba3635d5b5b3025/plugin/lib/fmserve.py
- .claude/worktrees/agent-a7ba3635d5b5b3025/plugin/lib/fmtidy.py
- .claude-plugin/marketplace.json
- CHANGELOG.md
- MASTER.md
- plugin/.claude-plugin/plugin.json
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmguard.py
- plugin/lib/fmhooks.py
- plugin/lib/fmrelate.py
- plugin/lib/fmserve.py
- plugin/lib/fmtidy.py
- plugin/tests/test_guard.py
- plugin/tests/test_guard_diff.py
- plugin/tests/test_hooks.py
- plugin/tests/test_relate.py
