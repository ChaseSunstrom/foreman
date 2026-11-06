# Super brainstorm 2026-10-02 (brainstorm-20261002-215842): grounding

171 titles (6 lenses × 2 rounds + 3 deepen rounds: speed, gates, autonomy). Grounded against the code:

## Dropped: already built
- Gate cache by tree hash: `fm check` reuses a pass on the same tree (`_cached_pass`, fmcli.py).
- Affected tests first: `fm check --affected`.
- Doc drift at close: fmdocs.task_docs / `fm docs`.
- Usage receipt, weekly digest: `fm cost`, `fm digest`.
- Snapshot before compaction: PreCompact checkpoint.
- Skip ceremony for small tasks / one-call close: `fm task new … --focus`, `fm task finish` (T-0097).
- Hook speed budget: tests/test_speed.py.

## Grounded, slated
1. Background work visible + Claude-like mascot (T-0109, user ask). Premise checked: the mod's `prompt.submit`
   fires for task notifications (origin.kind 'task-notification', idle or mid-turn), Bash background results carry
   the task id, so the mod can track shells live; Claude Code's Stop hook input carries `background_tasks`
   (in-flight shells/agents/monitors), the authoritative list drive should trust over its event scan. value 5 · M.
2. Drive trusts Stop's `background_tasks` (the Volt stall root cause was a stale event-derived list). value 4 · S.
3. Size words with meaning: typical time per type and size from the ledger beside the chip, time on task, gate
   ETA from the last run. value 4 · S.
4. "While you were away" row: what drive finished since the user's last prompt. value 3 · S.

## Kept for later (inbox, followup)
- One yes for several queued core tasks (queue preflight of predictable yeses) — security-sensitive.
- Rank the inbox by value for effort.
- Taste profile from what the user accepts and corrects.
- Stale-fact tripwire on resume.
- Overnight dry run of the queue in a worktree.

## Not pursued
Voice/radio, task cinema, mascot conversation, auto-deleting features, hiding Foreman entirely (conflicts with
the user's discipline layer), speculative twin execution (cost).
