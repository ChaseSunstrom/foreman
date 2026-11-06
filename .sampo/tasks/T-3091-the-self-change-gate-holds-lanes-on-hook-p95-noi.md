---
id: T-3091
type: FIX
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T01:16:46Z
updated: 2026-11-06T03:53:56Z
group: hook bench gate
---
# Self-change gate holds on T-3034, T-3047 and T-3053: bench each held hook on base and branch at low load, fix a real slowdown in its lane, or make the gate confirm before it holds
## Raw request
> The self-change gate holds lanes on hook p95 noise: a different hook each time at moderate load (T-3053 PostToolUse 34.9→43.7 ms +25%, T-3047 PreCompact 50.7→66.4 ms +31%, T-3034 likewise), and a hold removes the lane's worktree; hold only when the same hook regresses again on a second interleaved run (the gen-4 blind-spot rule: a single verdict that blocks work is confirmed before it blocks), and keep the worktree on a hold so a retry needs no rebuild
## Interpretation
Reading 1 (taken): three lanes were held for hook p95 rises (T-3034 PreToolUse:Bash:block 38.9→46.7 ms +20%, T-3053 PostToolUse 34.9→43.7 +25%, T-3047 PreCompact 50.7→66.4 +31%); the gate already needs a rise in 2 of 3 paired benches (T-2992), so first measure each at low load: a real rise is fixed in its lane (a hook path importing or scanning more), noise is fixed in the gate (a confirming bench before a hold) and the lane's worktree is kept on a hold. Reading 2 (ruled out): pass the gate by a decision or the standing yes: only the user's yes or a retry passes it.
## Assumptions (confidence)
## Acceptance criteria
- [ ] Each held hook is benched on base and branch at load under 4 (10 runs each, three pairs) and profiled on the branch; the finding (real cost with its function, or noise) is filed per lane — verify with `sampo research show T-3091-holds`
- [ ] A real slowdown is fixed in its lane (the hook path no longer pays for it, pinned by a test that the hook doesn't import or scan it) and that lane merges through the gate — verify with `python3 plugin/tests/run.py test_selfgate`
- [ ] A hold keeps the lane's worktree, so a retry needs no rebuild — verify with `python3 plugin/tests/run.py test_lanes`
- [ ] a rise counts only when it shows in the same hook in HOLD of PAIRS pairs, past RISE plus that hook's spread in an A/A bench of base against itself in the same window, and after dividing out the median ratio across all hooks (a uniform rise is the machine); the 8 recorded holds of 2026-11-04/05 replayed as fixtures pass, and a synthetic one-hook +60% rise held consistently across pairs still refuses — verify with `python3 plugin/tests/run.py test_selfgate`
## Non-goals
## Approach (options → choice → why)
1) use what exists: plugin/tests/bench_hooks.py on base and each branch, one hook at a time, at load under 4; cProfile the held hook on the branch to name the cost: likely outcome: each hold is either a named slowdown fixed in its lane or measured noise. 2) raise RISE or HOLD: fails if: a real slowdown slips through. 3) do less: keep retrying merges: fails if: a real slowdown never merges or merges by luck. Choice 1 (80%).
## Risks and rollback
## Execution prompt
## Steps
1. [ ] bench and profile each held hook at low load; file the findings  <- CURRENT
2. [ ] fix real slowdowns in their lanes; keep the worktree on a hold (tests first)
3. [ ] merge the lanes through the gate
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T01:16:46Z created
- 2026-11-05T01:30:31Z set title=Self-change gate holds on T-3034, T-3047 and T-3053: bench each held hook on base and branch at low load, fix a real slowdown in its lane, or make the gate confirm before it holds
- 2026-11-05T01:30:39Z planned: it has criteria and steps
- 2026-11-05T01:30:41Z set approved=True
- 2026-11-05T01:58:22Z blocked: waits for the merge chain's retries of T-3047, T-3034 and T-3053 at load under 9: its own hook benches would load the machine while the gate benches the same hooks, and a pass at low load answers step 1 for that lane
- 2026-11-05T03:22:30Z 2026-11-05: the merge queue's quiet window (my scripts' LOAD 9-12) is the main merge delay, and it exists only because of the T-3034, T-3047 and T-3053 holds; settle whether those were CPU-time rises or the wall fallback, and if noise, merges run at any load (T-3118 dropped into this)
- 2026-11-05T03:22:51Z finding 2026-11-05: the last 8 holds (T-3023, T-3026 x3, T-3029, T-3034, T-3053, T-3047) each name a different hook at +16% to +40%; T-3026's three runs held on three different sets, one with every hook up ~35% together: environment, not the branches. A real regression rises in the same hooks across pairs and relative to the others
- 2026-11-05T03:22:52Z blocked: approved; next builder slot after T-3092 and T-3113 (it unblocks merges at any load); changes the self-change gate, named for the user's review in the final report
- 2026-11-05T03:35:29Z 9th hold: T-3093 (SubagentStop, TaskCompleted +72%, PreCompact, SubagentStart +67%) on a diff that touches none of their work
- 2026-11-05T03:42:01Z 10th hold: T-3083 (PostToolUseFailure, UserPromptSubmit past budget, PreCompact) at load 16.7; merge queue paused; built in the main thread now as the bottleneck
- 2026-11-06T03:53:56Z unblocked
## Follow-ups captured
