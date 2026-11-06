Wave 3 maintainer audit. Verdict: approve with nits.
MED fmguard _FM_INTERNALS (5 modules) vs _FM_MUTATORS (4, no fmcore); neither has fmdocs → one FM module list.
MED ASK_TTL named in fmhooks but bare 300 in fmcli _take_seen_ask → share it.
LOW/MED lock timeouts 1/3/2/5/1 unnamed; _record_asks contention misreported as "never ran" → name + message allows retry.
LOW check_state_dir WARN doesn't say sticky/how to reverse.
Obs: worktree_id cost; check_self_docs does four checks in one function.
