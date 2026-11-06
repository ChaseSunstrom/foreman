# Brainstorm round 2 (T-0093), grounded
Source: research/brainstorm-20261002-145137 (3 lenses, 21 ideas) merged with own list; user steer: queue/inbox/activity must match the animated look.
## Slate → T-0094 (foreman-ui 0.3.0 + view-model additions)
- Animated card system for every card (queue rows with mini step bars, inbox age, activity fading by recency, hook latency sparkline) — steer — 5·M
- Quick capture Input in the pane (fm capture without interrupting Claude) — 4·S. Grounded: Input element (terminal/desktop/vscode).
- Live subagents card + files-touched card with per-file +/− bars — 4·M. Grounded: tool.call agentId, toolFace deltas.
- Context meter + one-time checkpoint and toast at ≥85% context — 4·S. Grounded: $.session.usage().context.percent.
- Ghost-text next (prompt.suggest '/foreman:next' when idle with work waiting) — 4·S. Grounded: $.prompt.suggest.
- Footer: PromptHint tail when something needs you; SessionMode label — 3·S.
- Gates card from the last fm check run (core: view gets checks) — 4·S.
- Chime on needs-you and task done ($.audio.play, WAV asset, mutable) — 2·S.
## Dropped
Haiku handoff on compact (PreCompact checkpoint + resume exist) · model-callable status tool (Bash fm works) · fork skeptic (cost; reviewer exists) · per-step tool folding (risk to engine rows) · quiet hint profile (weakens enforcement) · derive stages (already derived) · drop state.line/badge (stack layout and badges use them) · free-form task new (one-call planning shipped).
## Inbox
fm help tiers (captured).
