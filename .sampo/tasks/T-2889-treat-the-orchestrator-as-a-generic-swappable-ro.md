---
id: T-2889
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-04T03:55:40Z
updated: 2026-11-05T04:44:33Z
steer_method_rate: 0.218
---
# Treat the orchestrator as a generic, swappable role. "Jarvis" is only the name of an LLM…
## Raw request
> dont showcase it as jarvis in the animation, and don't say its you specifically, as we will want any orchestrator to work, jarvis is just an LLM served at that endpoint, its not actually jarvis
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Treat the orchestrator as a generic, swappable role. "Jarvis" is only the name of an LLM served at one endpoint. It is not a persona or a product identity, and Sampo must work with any orchestrator.
- In the animation, don't present the orchestrator as Jarvis or as any named character. Use a neutral label such as "Orchestrator" or "Planner", or a name read from config.
- Don't write copy in which the orchestrator claims to be, or is said to be, one specific agent, model or assistant (including me). Describe the role instead of the identity.
- Take any displayed orchestrator or model name from configuration or runtime data, such as the endpoint or model id. Never hardcode it in animation frames, UI strings, prompts, logs or error messages.
- Sweep every surface where the name or identity could appear, and fix what you find. That covers the animation source and assets, UI text, README and docs, demo scripts, code comments, identifiers, config defaults, tests and fixtures, and screenshots or recordings that can be regenerated.
- Make the endpoint and model a configurable provider setting. Jarvis may stay as an example value or default in config, but nothing else may depend on it.
- Add a check, such as a test or grep-based lint, that fails when "jarvis" or another hardcoded orchestrator identity appears in user-facing strings or animation code. Allow only the config example.
- Verify the result by running the animation and any tests with a differently named orchestrator config. Confirm that nothing Jarvis-specific shows up, and report what was changed and what was left.
- Apply this to all future UI, animation, docs and copy, not only this animation. Don't introduce orchestrator-specific branding again.
- Make these edits directly rather than proposing them. Don't publish, push or overwrite shared or generated artifacts without the user's go-ahead.
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-04T03:55:40Z created
- 2026-11-05T04:44:33Z dropped: done and being finished: the pages read a model by its role (T-2852), and T-2895 moves that into the exported data so no page says jarvis or names the orchestrator
## Follow-ups captured
