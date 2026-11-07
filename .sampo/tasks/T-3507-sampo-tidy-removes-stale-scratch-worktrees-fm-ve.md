---
id: T-3507
type: CLEAN
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T19:06:02Z
updated: 2026-11-06T19:26:02Z
lane: ~/.claude/foreman.lanes/T-3507
lane_branch: foreman/T-3507
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: cc5fffae3f8171d193ad5413161d55c2c5e43df5
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-06T19:13:20Z
plan0_scope: []
---
# sampo tidy removes stale scratch worktrees (fm-verify-*, sampo-train-*) with no live owner and exam runs older than 7 days
## Raw request
> sampo tidy removes stale scratch worktrees (fm-verify-*, sampo-train-*) with no live owner and exam runs older than 7 days
## Interpretation
Two new tidy sweeps. (1) Scratch worktrees: git-listed worktrees at <temp>/fm-verify-*/wt (lanes.py pm_verify, lane verify) or <temp>/sampo-train-* (train.py), detached, nothing under them written in 2 h, no live process with its cwd inside (/proc/*/cwd) and, for names made from now on (fm-verify-<pid>-*), the creating pid dead: listed with size; --apply runs git worktree remove --force, removes the empty mkdtemp folder, prunes. Without /proc they are only listed. 'Never a worktree with uncommitted work' (the AC) is read as: never an authored tree. A lane or any branch-holding worktree, or any path of another shape, is never touched; a scratch tree is a detached machine copy whose dirty files (a verify's revert --no-commit) are recreated from commits, which is why --force is safe there and needed (4 of the 7 left here are dirty). (2) Exam runs: exam/s*-NNN and exam/long/lNNN folders with nothing written in 7 days, listed with size, deleted on --apply; the newest run of each tier is always kept so the next run number (max+1) never reuses a name exam.jsonl grades refer to. Dry run stays read-only and prints the total it would free.
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo tidy lists and, with --apply, removes scratch worktrees under the temp folder that git lists but no live process owns and exam runs older than 7 days, never a worktree with uncommitted work — verify with `python3 plugin/tests/run.py test_tidy`
## Non-goals
## Approach (options → choice → why)
1) do less: cwd scan + age only, exactly as asked. Likely outcome: clears the 7 trees; fails if: tidy runs during pm_verify's up-to-60 s load wait (no process inside) on a verify over 2 h old, removing a live tree and misjudging a merge.
2) use what exists: lanes.stale() already sweeps closed lanes and _prune_exam_work (T-2568) prunes graded runs' work copies; widening them. Fails if: stale() is lane/brief-keyed (scratch trees have no brief) and exam_work keeps answers/keys by design, so neither frees the old runs.
3) cwd scan + age, plus the creating pid in new scratch names (mkdtemp prefix fm-verify-<pid>-, constants VERIFY_PREFIX in lanes.py and TRAIN_PREFIX in train.py imported by tidy); old names fall back to cwd+age. Exam runs: whole-folder delete by newest mtime (walk, early exit), the max-numbered run per tier kept. Findings carry bytes; cmd_tidy prints Would free / Freed N MB. Likely outcome: 1.25 GB of trees now, old exam runs from Nov 7 on; fails if: a pid is reused (then the tree is kept until a later tidy, the safe side).
4) a claim/lock file per scratch tree. Fails if: two writers and stale-lock handling, more code than the pid.
Choice 3 (85%): the owner pid closes option 1's gap for a few lines; the rest is option 1 as asked, with helpers _du/_touched_since shared with exam_work and the temp-dir set factored from _dead_projects.
## Risks and rollback
## Execution prompt
## Steps
1. [x] stale scratch worktrees, test-first
2. [x] old exam runs
## Resume here
## Docs impact
docs/map/files-lib-1.md and MASTER.md: one bullet for fmtidy._prune_scratch / _prune_exam_runs (T-3507), beside T-2568's exam_work bullet.
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_tidy.ScratchWorktrees` → ✗ exit 1 · Ran 4 tests in 86.4s (1 jobs, 16 at a time; slowest: ScratchWorktrees 1s) / FAILED (1 classes: test_tidy.ScratchWorktrees) [ran] [tree 8131ba375fb3] [world 2f1906870a] (2026-11-06T19:17:52Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_tidy.ScratchWorktrees` → exit 0 · Ran 4 tests in 74.1s (1 jobs, 16 at a time; slowest: ScratchWorktrees 1s) / OK [ran] [tree c33e08866dc7] [world 2f1906870a] (2026-11-06T19:22:20Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 47 tests in 54.2s (16 jobs, 16 at a time; slowest: DeferredTriage 10s, StalePlans 9s, DecisionSunset 7s) / OK [ran] [tree c33e08866dc7] [world 2f1906870a] (2026-11-06T19:23:15Z)
## Log
- 2026-11-06T19:06:02Z created
- 2026-11-06T19:06:19Z lane: ~/.claude/foreman.lanes/T-3507 on foreman/T-3507
- 2026-11-06T19:13:19Z focused
- 2026-11-06T19:13:20Z predicted from its closes: 3 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2568 [FEATURE M, done, 4 steps] fm tidy --apply prunes graded exam runs' work copies past 14 days, keeping the newest run per tier and agent, answers, grades and keys …
- research T-1667-review: Verdict: changes needed.** One MEDIUM and one more MEDIUM-ish lead, both small to fix. I could only read files (no shell), so I did not run the t…
- research T-1405-review: Verdict:** approve with nits. I found no CRITICAL or HIGH defect. I read the code and tests in the worktree and ran nothing, because the tools I …
- decision 2026-11-04: [costly] [confidence: 85%] Sampo's trained models learn only from outcomes, user-written text and labels, and local-model traces graded by tests, ne…
