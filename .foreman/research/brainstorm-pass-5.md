# Brainstorm pass 5 (2026-10-04) — grounded slate

Source: research/brainstorm-20261004-033458 (simplicity: what to cut, merge or make automatic; bold bets: what would make Foreman indispensable × 2 rounds, past passes 1–4; 41 new titles).

## Grounded and kept (built as T-0287)
1. Ask the guard about one command without running it — "make `fm guard check '<cmd>'` the way to probe the guard". This pass's grounding needed it twice (hand-built hook payloads, wrong argv). Built as `fm replay --cmd`, not a new verb. S.
2. The pre-audit's security patterns flagged their own docs — "fix the pre-audit patterns flagging their own source". The scan read added lines of every file; MASTER.md naming `requests.get(` made the pass-4 change "network code". Doc files are skipped now (fails closed). S.

## Grounded and dropped
- Run the review in the background of the next task / reviewer as a background pair — merges into T-0234 (lanes); the reviewer already reads a diff snapshot, and read-only grounding of the next item while it runs is already the practice.
- Merge the bench verbs into `fm bench --vs`, fold the review verbs into `fm review`, one-verb mode, auto-retire verbs — churn with no user-visible gain now; fm help's tiers and fm usage cover discoverability.
- Auto-tier from the diff footprint — exists (an S task spreading past two code files is told to re-tier).
- Mine git history / failures into bench cases — exists (fm bench build --commits, T-0222).
- Project constitution, state-of-the-project brief, "what's wrong with my project" — exist (fm export agents, fm digest, fm friction).
- Harness-neutral kernel / MCP read tools — T-0245 in the inbox.
- Self-trimming rules, ablation per feature — exist (fm evolve --drop).
- Put guard and pre-audit patterns in one data table — refactor without a behaviour change.

## Yield
2 grounded ideas of modest value (< 3): dry by the brainstorm skill's rule. One confirming probe with lenses not used recently (performance; unspoken needs) before the loop stops.
