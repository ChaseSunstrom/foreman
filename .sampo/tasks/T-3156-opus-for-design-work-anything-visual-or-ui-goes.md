---
id: T-3156
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-05T05:58:28Z
updated: 2026-11-05T05:58:28Z
steer_method_rate: 0.218
---
# **Opus for design work.** Anything visual or UI goes to Opus: SVGs, art, illustrations,…
## Raw request
> how good is the jeff trained model? also, I want opus to design the svg/art walk through cards and such, as it is the best model for UI and stuff, and you can use haiku for moon ideas and cards and whatever if the locals aren't cutting it
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- **Opus for design work.** Anything visual or UI goes to Opus: SVGs, art, illustrations, icons, diagrams, walkthrough cards, layouts and styling. Local models and Haiku don't produce the final version of these.
- **Local first, Haiku as fallback for ideation.** Moon ideas, card concepts and copy, brainstorming and similar light creative work go to the local models (including the jeff-trained one) first. Haiku takes over only when the local output isn't good enough.
- **"Not cutting it" is a checkable test.** Local output counts as failing if it misses the brief, is malformed (an SVG that won't parse or render, a card that breaks its schema), or is clearly below the quality of existing material after one retry. Record the failure reason before escalating.
- **Verify Opus output.** Each SVG or card must parse and render, fit its container at the real sizes, and match the existing visual style. Wire it into every place it appears: the walkthrough flow, the card set, the docs and any tests or snapshots.
- **Record provenance.** Note which model produced each artifact and why it was chosen, so routing decisions can be audited.
- **Evaluate the jeff-trained model with evidence.** Run it on a representative sample of the real tasks (moon ideas, card text, SVG attempts) against a fixed rubric, and run the same prompts through Haiku and Opus as baselines. Report scores, concrete failure examples and where it is and isn't usabl…
- **Use the evaluation to tune routing.** Set the local-versus-Haiku threshold from the results, and update the routing config and docs to match.
- **Make the routing persistent.** Store it in the project's config or CLAUDE.md so it applies to future sessions, not only this one.
- **No silent substitution.** If Opus or Haiku is unavailable or errors out, say so and stop on that artifact. Don't quietly fall back to a weaker model for design work.
- **Keep spend in bounds.** Paid Opus and Haiku calls are authorized only for the task types above. Report spend per model, stay within the remaining budget, and ask before going over it.
- **Ask before anything outward or irreversible.** Publishing assets, calling other external services, or overwriting existing art or cards needs a fresh grant. Inspect the target before replacing it.
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
- 2026-11-05T05:58:28Z created
## Follow-ups captured
