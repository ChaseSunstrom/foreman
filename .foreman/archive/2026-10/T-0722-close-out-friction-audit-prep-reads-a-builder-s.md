---
id: T-0722
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T17:06:10Z
updated: 2026-10-09T17:10:13Z
batch: [T-0718, T-0720]
base: a3de9b785a8f7c9193342061d9b1769e6f90f27e
base_tree: 4c548934bc4bcb62a194948fb9bb8232c07e75a6
verified: strong
---
# Close-out friction: audit prep reads a builder's branch; a refused commit can be retried
## Raw request
> T-0718: fm audit prep for a builder task diffs the main checkout (other tasks' commits), not the lane branch: T-0701's brief listed fmguard/fmideas changes from T-0716/T-0671 instead of fminstr.py
> T-0720: fm task finish refused its commit (a fixture looked like a secret) and left the task done but its files uncommitted; nothing retries the commit for a done task, so it took a new task (T-0719) and a raw git commit: add fm task finish ID --commit-only (or let --commit rerun on a done task)
## Interpretation
Do T-0718, T-0720 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0722. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0718 audit prep of a lane task diffs the builder's branch from where it left main — verify with `python3 plugin/tests/run.py -p test_builder.py -k Flow`
- [x] T-0720 a credential in finish --commit is found before the close (the task stays open), and a done task's commit can be retried — verify with `python3 plugin/tests/run.py -p test_secrets.py`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] both failing tests first
2. [x] audit prep: lane branch diff (fmcli cmd_audit)
3. [x] finish: leak check before the close; --commit on a done task commits only (fmcli task_finish/_commit_task)
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_builder.py -p test_secrets.py` → ✗ exit 1 · Ran 23 tests in 4.8s (5 classes, 16 at a time; slowest: Contract 5s, Brief 2s, Secrets 2s) / FAILED (2 classes) [ran] [tree 878f9657e3c7] (2026-10-09T17:07:22Z)
- (step 2) `python3 plugin/tests/run.py -p test_builder.py -k Flow` → exit 0 · Ran 2 tests in 0.9s (1 classes, 16 at a time; slowest: Flow 1s) / OK [ran] [tree e0c275b54b55] (2026-10-09T17:09:51Z)
- (step 3) `python3 plugin/tests/run.py -p test_secrets.py` → exit 0 · Ran 6 tests in 1.9s (1 classes, 16 at a time; slowest: Secrets 2s) / OK [ran] [tree e0c275b54b55] (2026-10-09T17:09:54Z)
- (ac 1) `python3 plugin/tests/run.py -p test_builder.py -k Flow` → exit 0 · Ran 2 tests in 0.9s (1 classes, 16 at a time; slowest: Flow 1s) / OK [ran] [tree a2328bd4b18d] (2026-10-09T17:10:12Z)
- (ac 2) `python3 plugin/tests/run.py -p test_secrets.py` → exit 0 · Ran 6 tests in 1.9s (1 classes, 16 at a time; slowest: Secrets 2s) / OK [ran] [tree a2328bd4b18d] (2026-10-09T17:10:12Z)
- (step 1) `python3 plugin/tests/run.py -p test_builder.py -p test_secrets.py` → exit 0 · Ran 23 tests in 4.8s (5 classes, 16 at a time; slowest: Contract 5s, Brief 2s, Secrets 2s) / OK [ran] [tree a2328bd4b18d] (2026-10-09T17:10:12Z)
- (audit edge) `self: both changes read back; the dry check stages, scans and unstages only the task's files, so the index is as it was; a lane brief without its branch falls back to the old diff` → lane branch gone (merged and removed) → rev-parse fails → main-checkout diff as before; --audit now optional only for the done+--commit retry, else a clear UsageError [tree a2328bd4b18d] (2026-10-09T17:10:12Z)
- (audit adversary) `self: both changes read back; the dry check stages, scans and unstages only the task's files, so the index is as it was; a lane brief without its branch falls back to the old diff` → the retry path commits through the same _commit_task (secret scan, task-only files); nothing skips the leak check [tree a2328bd4b18d] (2026-10-09T17:10:12Z)
- (audit self) `self: both changes read back; the dry check stages, scans and unstages only the task's files, so the index is as it was; a lane brief without its branch falls back to the old diff` → no findings [tree a2328bd4b18d] (2026-10-09T17:10:12Z)
## Log
- 2026-10-09T17:06:10Z created
- 2026-10-09T17:07:05Z focused
- 2026-10-09T17:10:12Z done
- 2026-10-09T17:10:13Z committed 2611634 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0681 [FEATURE M, planned, 3 steps] Milestone: Features — UI and motion
- T-0678 [FEATURE M, planned, 2 steps] Milestone: Features — Releases and delivery
- T-0692 [FEATURE M, planned, 2 steps] Milestone: Intelligence — Planning and decomposition (2)
- decision 2026-10-04: Inbox build order: review family (T-0230, T-0232, T-0233, T-0235) and research family (T-0229, T-0237, T-0238, T-0239) are each built as one batch, …
## Files touched
- plugin/tests/test_builder.py
- plugin/tests/test_secrets.py
- plugin/lib/fmcli.py
- CHANGELOG.md
