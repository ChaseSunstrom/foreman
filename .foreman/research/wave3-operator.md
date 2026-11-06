Wave 3 operator audit. Verdict: changes needed (nits, no criticals).
1 MED doctor doesn't check fmsetup.ENV (autocompact override, stop cap) in settings.json.
2 MED session_context calls next_for without its own try/except → an exception blanks all SessionStart context.
3 LOW check_state_dir WARN gives no recovery path; tmp fallback lost at reboot; MASTER doesn't mention the fallback.
4 LOW worktree_id slow on huge repos, silent fallback on timeout, no log.
5 LOW stale pending approvals sit forever; recovery (re-run fm ask) undocumented.
Met: upgrade path, env var apply/record/reverse, gate messages name fixes, fm docs exit codes.
