T-2416 review (coordinator, main thread: the pace gate held fm-reviewer subagents).
Intent met: verdict runs each done item's done-when on the earliest c.task_base of its done tasks via fmcli._run_at (guarded), caches pass/fail per (done-when, base) in meta goal_red (capped 500), never caches timeouts or scratch failures, and names no-base items unproven with lint_verify kept as fallback.
Finding fixed: items drift didn't reach (deadline) still got the start-tree run under the active task's grants: skipped like drift-refused items (their cause already blocks).
Checked: only fm goal verdict calls it (the Stop hook reads the stored verdict, so no hook-time runs); T-2333's lint_verify/_hollow untouched.
Open: a check red at the start only for a missing artifact still reads proven (same as fm task prove --vacuous); fm goal show and drift still read passing-at-start as met; timeout branches untested (300 s).
