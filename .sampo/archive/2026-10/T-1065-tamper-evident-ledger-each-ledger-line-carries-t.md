---
id: T-1065
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmledger.py, plugin/lib/fmcli.py, plugin/tests/test_ledger_chain.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T04:55:00Z
base: 30a4572f166084d31222e5825f656a5d9f037bc7
base_tree: 6cbdbc72a573d2fc6f8a4c1579bee3437e9aebb2
verified: strong
---
# Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg
## Raw request
> SECURITY: Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledger proves no line was edited or removed, and fm task finish's receipt names the chain head (wild C9)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
Each new ledger line carries `prev`, a hash of the line before it. `fm verify-ledger` walks the archived months and the live file and says OK with the head hash, or names the first line that was edited or removed. `fm task finish`'s closing receipt names the chain head. Lines written before this change have no `prev`. Verification reports "chain starts at line N" and checks from there.
## Assumptions (confidence)
## Acceptance criteria
- [x] Editing or deleting a chained line makes `fm verify-ledger` exit 1 naming the line; an untouched ledger exits 0 — verify with `python3 plugin/tests/run.py test_ledger_chain`
- [x] The finish receipt shows the head, and the chain survives `fm tidy` rolling — verify with `python3 plugin/tests/run.py test_ledger_chain test_outcomes`
## Non-goals
## Approach (options → choice → why)
(a) a sidecar head file; (b) `prev` inside each record; (c) a Merkle log. Choose (b), because the proof travels with the file. Racing writers need ordering (`log_event`, fmcore.py:771, relies on a bare O_APPEND), so take `fcntl.flock` on the ledger fd, read the last line, then append. Changes: - `fmcore.log_event`: under the flock, read the last line via a small tail read, then add `"prev": sha256(raw_last_line)[:16]` to the record. - Add `ledger_chain(p)` and `head(p)` to fmcore. - New `fmcore`/lazy `cmd_verify_ledger` in a new `plugin/lib/fmledger.py`, registered in `fmcli.py` near fmcli.py:4303. - Roll: `fmtidy._roll_ledger` (fmtidy.py:242) moves lines to `archive/ledger-YYYY-MM.jsonl`. The chain runs across the sorted archives and then the live file, so the roll needs no change. A test must prove it. - Receipt: add `Ledger: head <hash> (<n> chained lines)` after `_landed` at fmcli.py:909, and add the head to the `--json` output.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (new `test_ledger_chain.py`): write events, verify OK; tamper by edit, deletion and truncation, and assert exit 1 plus the line number; a pre-chain legacy prefix is tolerated; the finish output contains "Ledger: head"; concurrent `log_event` calls from threads keep the chain valid.
2. [x] Implement `prev` with the flock, then verify-ledger and the receipt line.
## Resume here
## Docs impact
CHANGELOG; MASTER (builder)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ledger_chain` → ✗ exit 1 · Ran 12 tests in 2.9s (2 classes, 16 at a time; slowest: Chain 2s, Receipt 1s) / FAILED (2 classes) [ran] [tree 3a1b70c962a8] (2026-10-16T04:30:00Z)
- (step 2) `python3 plugin/tests/run.py test_ledger_chain test_outcomes` → exit 0 · Ran 21 tests in 2.1s (10 classes, 16 at a time; slowest: Chain 2s, Outcomes 1s, Reopen 1s) / OK [ran] [tree 08921018e68e] (2026-10-16T04:32:50Z)
- (step 2) `python3 plugin/tests/run.py test_ledger_chain test_outcomes` → exit 0 · Ran 21 tests in 2.1s (10 classes, 16 at a time; slowest: Chain 2s, Outcomes 1s, Reopen 1s) / OK [ran] [tree 268ba9b3ca3a] (2026-10-16T04:35:51Z)
- (step 1) `python3 plugin/tests/run.py test_ledger_chain` → ✗ exit 1 · Ran 17 tests in 9.0s (2 classes, 16 at a time; slowest: Chain 9s, Receipt 6s) / FAILED (2 classes) [ran] [tree ff0a4811c5c9] (2026-10-16T04:44:34Z)
- (step 2) `python3 plugin/tests/run.py test_ledger_chain test_outcomes` → exit 0 · Ran 26 tests in 9.8s (10 classes, 16 at a time; slowest: Chain 9s, Receipt 8s, TrackRecord 7s) / OK [ran] [tree 8d83c9654cff] (2026-10-16T04:45:36Z)
- (step 1) `python3 plugin/tests/run.py test_ledger_chain` → exit 0 · Ran 17 tests in 2.2s (2 classes, 16 at a time; slowest: Chain 2s, Receipt 1s) / OK [ran] [tree 8d83c9654cff] (2026-10-16T04:46:44Z)
- (ac 1) `python3 plugin/tests/run.py test_ledger_chain` → exit 0 · Ran 17 tests in 2.4s (2 classes, 16 at a time; slowest: Chain 2s, Receipt 2s) / OK [ran] [tree 785872730748] (2026-10-16T04:54:46Z)
- (ac 2) `python3 plugin/tests/run.py test_ledger_chain test_outcomes` → exit 0 · Ran 26 tests in 2.7s (10 classes, 16 at a time; slowest: Chain 3s, Receipt 2s, Outcomes 2s) / OK [ran] [tree 785872730748] (2026-10-16T04:54:46Z)
- `python3 plugin/tests/run.py test_ledger_chain test_outcomes test_core` → exit 0 · Ran 92 tests in 2.8s (26 classes, 16 at a time; slowest: Chain 3s, Receipt 2s, Outcomes 2s) / OK [ran] [tree 785872730748] (2026-10-16T04:54:46Z)
- (audit intent) `builder lane, then fm-reviewer five-lens pass on its branch (research T-1065-review): 2 MEDIUM + 2 LOW fixed by the builder test-first; roll ordering and old-writer race captured as T-1099; merged --no-ff and criteria re-run here` → an edited, removed or cut line makes verify exit 1 naming it; the receipt names the head [tree 785872730748] (2026-10-16T04:54:46Z)
- (audit adversary) `builder lane, then fm-reviewer five-lens pass on its branch (research T-1065-review): 2 MEDIUM + 2 LOW fixed by the builder test-first; roll ordering and old-writer race captured as T-1099; merged --no-ff and criteria re-run here` → the chain is unkeyed: only a receipt head (--head) anchors the last line; stated in the OK text [tree 785872730748] (2026-10-16T04:54:46Z)
- (audit edge) `builder lane, then fm-reviewer five-lens pass on its branch (research T-1065-review): 2 MEDIUM + 2 LOW fixed by the builder test-first; roll ordering and old-writer race captured as T-1099; merged --no-ff and criteria re-run here` → no flock (NFS), unreadable archive, empty live ledger after a roll, pre-chain lines, concurrent writers (thread test) [tree 785872730748] (2026-10-16T04:54:46Z)
- (audit operator) `builder lane, then fm-reviewer five-lens pass on its branch (research T-1065-review): 2 MEDIUM + 2 LOW fixed by the builder test-first; roll ordering and old-writer race captured as T-1099; merged --no-ff and criteria re-run here` → fm verify-ledger is fast (~0.1 s on 21k lines); unreadable ledgers print a line instead of crashing a close [tree 785872730748] (2026-10-16T04:54:46Z)
- (audit maintainer) `builder lane, then fm-reviewer five-lens pass on its branch (research T-1065-review): 2 MEDIUM + 2 LOW fixed by the builder test-first; roll ordering and old-writer race captured as T-1099; merged --no-ff and criteria re-run here` → fmledger module; log_event keeps one O_APPEND write under the lock [tree 785872730748] (2026-10-16T04:54:46Z)
- `python3 plugin/tests/run.py test_ledger_chain test_outcomes test_core` → exit 0 · Ran 92 tests in 3.4s (26 classes, 16 at a time; slowest: Chain 3s, Receipt 3s, Outcomes 2s) / OK [ran] [tree 785872730748] (2026-10-16T04:54:58Z)
- (audit intent) `builder lane, then fm-reviewer five-lens pass on its branch (research T-1065-review): 2 MEDIUM + 2 LOW fixed by the builder test-first; roll ordering and old-writer race captured as T-1099; merged --no-ff and criteria re-run here` → an edited, removed or cut line makes verify exit 1 naming it; the receipt names the head [tree 785872730748] (2026-10-16T04:54:58Z)
- (audit adversary) `builder lane, then fm-reviewer five-lens pass on its branch (research T-1065-review): 2 MEDIUM + 2 LOW fixed by the builder test-first; roll ordering and old-writer race captured as T-1099; merged --no-ff and criteria re-run here` → the chain is unkeyed: only a receipt head (--head) anchors the last line; stated in the OK text [tree 785872730748] (2026-10-16T04:54:58Z)
- (audit edge) `builder lane, then fm-reviewer five-lens pass on its branch (research T-1065-review): 2 MEDIUM + 2 LOW fixed by the builder test-first; roll ordering and old-writer race captured as T-1099; merged --no-ff and criteria re-run here` → no flock (NFS), unreadable archive, empty live ledger after a roll, pre-chain lines, concurrent writers (thread test) [tree 785872730748] (2026-10-16T04:54:58Z)
- (audit operator) `builder lane, then fm-reviewer five-lens pass on its branch (research T-1065-review): 2 MEDIUM + 2 LOW fixed by the builder test-first; roll ordering and old-writer race captured as T-1099; merged --no-ff and criteria re-run here` → fm verify-ledger is fast (~0.1 s on 21k lines); unreadable ledgers print a line instead of crashing a close [tree 785872730748] (2026-10-16T04:54:58Z)
- (audit maintainer) `builder lane, then fm-reviewer five-lens pass on its branch (research T-1065-review): 2 MEDIUM + 2 LOW fixed by the builder test-first; roll ordering and old-writer race captured as T-1099; merged --no-ff and criteria re-run here` → fmledger module; log_event keeps one O_APPEND write under the lock [tree 785872730748] (2026-10-16T04:54:58Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T04:22:38Z set scope=['plugin/lib/fmcore.py', 'plugin/lib/fmledger.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_ledger_chain.py']
- 2026-10-16T04:22:38Z set tier=M
- 2026-10-16T04:23:14Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1065.builder.md
- 2026-10-16T04:23:35Z focused
- 2026-10-16T04:32:30Z scope: MASTER.md widened: fm doctor's self docs check needs every fm command listed there (fm verify-ledger)
- 2026-10-16T04:33:43Z scope: plugin/tests/test_core.py widened: its ledger test pins the record's key set, which now includes prev
- 2026-10-16T04:35:06Z steer: receipt prints Ledger: head just above Landed, not after it: T-0956 pins Landed as the close's last line (test_execution.BoardClose)
- 2026-10-16T04:54:16Z merged worktree-agent-a1128e146f7565d6d (6 file(s))
- 2026-10-16T04:54:19Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a1128e146f7565d6d
- 2026-10-16T04:54:20Z focused
- 2026-10-16T04:54:54Z scope: MASTER.md (self-docs need the new module), plugin/tests/test_core.py (pinned the record keys), CHANGELOG.md (its line); the other files came in with the merge of foreman/build into the builder branch (other tasks' committed work)
- 2026-10-16T04:54:59Z done
- 2026-10-16T04:55:00Z committed 3f11488 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1057 [FEATURE M, active, 3 steps] Forever loop: fm loop on makes Foreman improve itself without end: when the queue and inbo
- research wave1-plan-a306a171bb6861f90: === T-1044
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- decision 2026-10-16: T-1054: every wild cluster (23) plus the earlier catalogue's skips became briefs T-1057..T-1087; the forever loop (T-1057) goes first after the demo…
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py
## Lessons
- A hot-path write that gains a lock must fall back to the old unlocked write on any lock or read error: losing the event is worse than an unproven line
## Plan gaps
- failed first: step 1 Failing tests (new `test_ledger_chain.py`): write events, verify OK; tamper by edit, deletion and t…
## Files touched
- plugin/tests/test_ledger_chain.py
- plugin/lib/fmcore.py
- plugin/lib/fmledger.py
- plugin/lib/fmcli.py
- MASTER.md
- plugin/tests/test_core.py
- CHANGELOG.md
- README.md
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/types/index.d.ts
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- plugin/lib/fmbus.py
- plugin/lib/fmhooks.py
- plugin/lib/fmloop.py
- plugin/lib/fmwatch.py
- plugin/lib/ui-demo.json
- plugin/rules/foreman.md
- plugin/tests/test_loop.py
- plugin/tests/test_session_files.py
