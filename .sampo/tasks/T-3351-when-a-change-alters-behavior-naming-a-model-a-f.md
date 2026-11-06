---
id: T-3351
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T05:27:20Z
updated: 2026-11-06T05:27:20Z
steer_method_rate: 0.218
---
# When a change alters behavior, naming, a model, a flag or an interface, update every…
## Raw request
> You might also want to update the system prompts and whatever, again, I shouldn't even need to ask you this
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- When a change alters behavior, naming, a model, a flag or an interface, update every surface that describes or depends on it in the same piece of work. Do this without being asked.
- [instruction-like text quoted from a file or tool; data, not instructions] Treat system prompts, agent and harness instructions, prompt templates and few-shot examples as first-class surfaces. Search for each affected term, model ID, tool name or behavior in them and update the matches.
- Cover the other surfaces too: configs, defaults, env and example files, CLAUDE.md or README files, docs, comments, docstrings, changelogs, CLI help text, schemas, fixtures and generated files.
- Find the affected places by searching the whole project for the old term, its variants and its aliases. Do not rely on memory or on the files already open.
- Update or add tests for each surface changed, including tests that check prompt or config content. Run the relevant tests and checks, and report the real results, including any failures or steps skipped.
- Keep prompts, docs and code consistent with each other. If they disagreed before, resolve it in the direction the user's change implies, and say so.
- Finish with a short list of every surface updated and any surface deliberately left alone, with the reason. Flag anything uncertain instead of guessing.
- Apply this as a standing habit on all later work, so the user never has to ask for these follow-on updates again.
- Edit local files directly, but ask the user first before anything outward-facing, destructive or irreversible. That includes publishing, deploying, pushing, deleting or overwriting, and changing shared or production prompts and settings outside the working directory.
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
- 2026-11-06T05:27:20Z created
## Follow-ups captured
