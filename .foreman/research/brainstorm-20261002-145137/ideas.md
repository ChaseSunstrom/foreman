# Ideas by round (deduplicated titles; details in the lens files)

## Round 1
- Suggest the next prompt as ghost text
- Show a "needs you" footer and prompt tail
- Fold tool rows into per-step groups
- Add a Haiku-written session handoff on compact and end
- Add a completion chime and desktop notification for waits on you
- Add an inbox triage Pane with Input and Select
- Show a per-turn context and cost burn meter
- Ship a model-callable `foreman_status` tool
- Register `mcp__foreman-ui__task` as a model-callable tool via `$.tool.register`
- Add a "verify with fork" step: `$.model.fork` skeptic before `fm task done`
- Add a ToolGroup/UserMessage "Foreman lane" that folds routine tool noise into step summaries
- Make an Input-based inline capture bar in the `/fm` Pane
- Compact-proof resume with `session.compact` plus `$.store` handoff
- Add a sound-and-attention profile with `$.audio.play` and idle-aware toasts
- Add a `CommandOutput` renderer that draws `fm` output as trees and tables
- Show the Foreman step in `PromptHint tail` and `SessionMode`, then remove the matching `state.line` and `badge.txt` writes
- Add `fm help` with three tiers (core 8 commands, advanced, internal)
- Make `fm task new` accept a free-form paragraph and auto-fill sections by fuzzy header matching
- Fold a "token receipt" into the TurnDuration line from `$.session.usage()`
- Cut the stage machine to a derived view: store only steps and criteria, compute stage
- Add a "quiet by default" Foreman profile: mod on means no hint injection unless a gate is about to fire

## New ideas per lens
- user value: 8
- bold bets: 7
- simplicity: 6
