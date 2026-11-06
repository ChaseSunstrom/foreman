Wave 3 edge audit. Verdict: changes needed.
1 HIGH is_plan_only false positives: "don't change the API", "the plan only covers X" set drive hold.
2 MED _QUESTION_LINE matches '?' line-ends inside fenced code in the reply tail → drive stops.
3 HIGH fallback marker is permanent; no way back when default becomes writable again; doctor only warns.
4 HIGH fallback path from each process's XDG_STATE_HOME → sandbox vs hooks may disagree.
5 HIGH worktree_id does a full git add -A into a fresh index on every audit/done; slow on big repos/LFS; timeout silently skips staleness check.
6 MED _record_asks lock timeout 2 s; lost race drops the ask record → fm ask refused.
7 LOW eval setup.sh depends on ../calc-setup.sh (unverified harness copy behaviour).
